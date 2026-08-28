# 实现火山引擎对象存储（TOS）的上传功能
import datetime
import os
import time
from typing import Optional

import config
from exceptions import CustomError, CustomException
from src.utils.logger import logger
from src.utils.storage_key import build_storage_object_key
from src.utils.storage_upload_retry import run_with_storage_retry

# 断点续传分片大小（与 SDK 文档示例一致）；小文件仍由 SDK 按单次/分片策略处理
_TOS_PART_SIZE_BYTES = 5 * 1024 * 1024
# 弱网可适当保留 2；并发过高易触发超时则改为 1
_TOS_UPLOAD_TASK_NUM = 2


def _resolve_tos_endpoint() -> str:
    """返回 TOS endpoint；未配置时按地域生成 tos-{region}.volces.com。"""
    endpoint = (config.TOS_ENDPOINT or "").strip()
    if endpoint:
        return endpoint
    region = (config.TOS_REGION or "").strip()
    return f"tos-{region}.volces.com"


def tos_upload_file(file_path: str, expire_days: Optional[int] = None) -> str:
    """
    上传文件到 TOS，返回带签名的临时URL，链接在指定天数后失效（见 config.VIDEO_GEN_RETENTION_DAYS）。
    使用 client.upload_file 断点续传分片上传。

    Args:
        file_path: 文件路径
        expire_days: URL 有效期天数；为 None 时使用 config.VIDEO_GEN_RETENTION_DAYS（视频生成任务默认）

    Returns:
        str: 带签名的临时下载URL（有效期为 expire_days 天）

    Raises:
        CustomException: 上传失败
    """
    if expire_days is None:
        expire_days = config.VIDEO_GEN_RETENTION_DAYS

    try:
        import tos
        from tos.enum import HttpMethodType
    except ImportError as e:
        logger.error(f"TOS SDK import failed: {e}")
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR, "TOS SDK not installed")

    filename = os.path.basename(file_path)
    key = build_storage_object_key(filename)
    endpoint = _resolve_tos_endpoint()

    def do_upload() -> str:
        expire_time = datetime.datetime.now() + datetime.timedelta(days=expire_days)
        expire_time_str = expire_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        client = tos.TosClientV2(
            config.TOS_ACCESS_KEY_ID,
            config.TOS_ACCESS_KEY_SECRET,
            endpoint,
            config.TOS_REGION,
        )
        response = client.upload_file(
            config.TOS_BUCKET_NAME,
            key,
            file_path,
            part_size=_TOS_PART_SIZE_BYTES,
            task_num=_TOS_UPLOAD_TASK_NUM,
        )
        status = getattr(response, "status_code", None)
        logger.info(f"TOS upload success, key: {key}, expire time: {expire_time_str}, status: {status}")

        signed = client.pre_signed_url(
            HttpMethodType.Http_Method_Get,
            config.TOS_BUCKET_NAME,
            key,
            expires=expire_days * 24 * 3600,
        )
        signed_url = signed.signed_url
        logger.info(f"Generated TOS signed URL valid for {expire_days} day(s), URL: {signed_url[:100]}...")
        return signed_url

    _t0 = time.perf_counter()
    success = False
    try:
        result = run_with_storage_retry(do_upload, context="TOS")
        success = True
        return result
    except Exception as e:
        logger.error(f"TOS upload failed: {e}")
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR, "TOS upload failed")
    finally:
        elapsed = time.perf_counter() - _t0
        logger.info(
            "TOS upload %s, file=%s, key=%s, total_duration_sec=%.3f",
            "success" if success else "failed",
            file_path,
            key,
            elapsed,
        )
