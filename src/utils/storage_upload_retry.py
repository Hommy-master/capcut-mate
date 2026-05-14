# 对象存储上传：可重试错误识别与退避重试（独立模块，供 cos/oss 使用，避免与 upload_file 相向依赖）
import errno
import random
import time
from collections.abc import Callable
from typing import Iterator, TypeVar

import requests
import urllib3.exceptions
from qcloud_cos.cos_exception import CosClientError, CosServiceError

from src.utils.logger import logger

try:
    import oss2.exceptions as oss_exc
except ImportError:  # pragma: no cover
    oss_exc = None  # type: ignore[assignment]

# 业务层整次重试（与 COS SDK 内重试等叠加）
_STORAGE_UPLOAD_MAX_ATTEMPTS = 5
_STORAGE_UPLOAD_BASE_DELAY_SEC = 1.0
_STORAGE_UPLOAD_MAX_DELAY_SEC = 30.0

T = TypeVar("T")

_RETRYABLE_ERRNOS = frozenset(
    {
        errno.ECONNRESET,
        errno.ETIMEDOUT,
        errno.EPIPE,
        errno.ECONNABORTED,
        errno.ENETUNREACH,
        errno.EHOSTUNREACH,
        10053,
        10054,
    }
)


def _iter_exception_chain(exc: BaseException) -> Iterator[BaseException]:
    seen: set[int] = set()
    e: BaseException | None = exc
    while e is not None and id(e) not in seen:
        yield e
        seen.add(id(e))
        nxt = e.__cause__ or e.__context__
        e = nxt if nxt is not e else None


def is_retryable_storage_error(exc: BaseException) -> bool:
    """
    判断是否为“整次重试”可能恢复的错误：网络/超时/连接类、云端临时性 5xx 等。
    非幂等或确定性的客户端错误（4xx 业务、鉴权等）返回 False。
    """
    for e in _iter_exception_chain(exc):
        if isinstance(
            e,
            (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.ChunkedEncodingError,
                urllib3.exceptions.ConnectTimeoutError,
                urllib3.exceptions.ReadTimeoutError,
                urllib3.exceptions.NewConnectionError,
                urllib3.exceptions.ProtocolError,
            ),
        ):
            return True
        if isinstance(e, OSError) and getattr(e, "errno", None) in _RETRYABLE_ERRNOS:
            return True
        if isinstance(e, CosClientError):
            return True
        if isinstance(e, CosServiceError):
            try:
                code = e.get_status_code()
            except Exception:
                code = None
            if code is not None and int(code) >= 500:
                return True
            return False
        if oss_exc is not None:
            if isinstance(e, oss_exc.RequestError):
                return True
            if isinstance(e, oss_exc.OssError):
                st = getattr(e, "status", None)
                if st == oss_exc.OSS_REQUEST_ERROR_STATUS:
                    return True
                if isinstance(st, int) and st >= 500:
                    return True
                if isinstance(st, int) and st == 408:
                    return True
    return False


def run_with_storage_retry(operation: Callable[[], T], *, context: str = "") -> T:
    """对上传/签名等操作做有限次重试，指数退避 + 全抖动。"""
    max_attempts = max(1, _STORAGE_UPLOAD_MAX_ATTEMPTS)
    base = max(0.05, _STORAGE_UPLOAD_BASE_DELAY_SEC)
    cap = max(base, _STORAGE_UPLOAD_MAX_DELAY_SEC)

    prefix = f"{context} " if context else ""
    last: BaseException | None = None
    for attempt in range(max_attempts):
        try:
            return operation()
        except Exception as e:
            last = e
            if attempt >= max_attempts - 1 or not is_retryable_storage_error(e):
                raise
            upper = min(cap, base * (2**attempt))
            delay = random.uniform(0.0, upper)
            logger.warning(
                "%sstorage upload attempt %d/%d failed: %s; retrying in %.2fs",
                prefix,
                attempt + 1,
                max_attempts,
                e,
                delay,
            )
            time.sleep(delay)
    assert last is not None
    raise last
