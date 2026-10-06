# 客户端上传文件到服务器，服务端中转上传到对象存储；仅上传成功后按文件体积计费，并返回带签名的下载 URL
import os
import tempfile
from typing import Optional

from fastapi import UploadFile

import config
from exceptions import CustomError, CustomException
from src.schemas.validators import validate_api_key_uuid
from src.utils.deferred_delete import enqueue_path
from src.utils.logger import logger
from src.utils.points import deduct_user_points, get_user_points
from src.utils.storage_key import build_upload_object_key, sanitize_object_filename
from src.utils.upload_file import upload_file as upload_file_to_storage

# 上传计费单价（元/MB；1 积分 = 1 元），按文件实际字节数计费
UPLOAD_PRICE_PER_MB = 0.0005

# 单文件大小上限（500MB）
MAX_UPLOAD_SIZE_BYTES = 500 * 1024 * 1024

# 请求体上限（文件上限 + multipart 封装开销），供中间件按 Content-Length 提前拦截
MAX_UPLOAD_BODY_BYTES = MAX_UPLOAD_SIZE_BYTES + 1024 * 1024

# 落盘分块大小（1MB），边读边计数，避免超大文件占满内存
_CHUNK_SIZE = 1024 * 1024

# 允许上传的文件扩展名（不含点，大小写不敏感）：只放行常见音视频/图片格式，避免对象存储被当作任意文件托管
_ALLOWED_EXTENSIONS = frozenset({
    "mp4", "mov", "m4v", "avi", "mkv", "flv", "webm", "wmv",
    "mp3", "wav", "m4a", "aac", "flac", "ogg",
    "jpg", "jpeg", "png", "gif", "webp", "bmp",
})


def _ensure_api_key(api_key: Optional[str]) -> None:
    """
    校验 apiKey 与余额门槛；开启 apiKey 时余额需大于 1 才可继续（与 gen_video 一致）。

    Raises:
        CustomException: apiKey 格式非法（1001）、缺失（2036）或余额不足（2035）
    """
    try:
        api_key = validate_api_key_uuid(api_key)
    except ValueError as e:
        raise CustomException(CustomError.PARAM_VALIDATION_FAILED, detail=str(e))

    if not config.ENABLE_APIKEY:
        return

    if not api_key:  # 未传或空字符串
        raise CustomException(CustomError.INVALID_APIKEY)

    if get_user_points(api_key) <= 1:
        raise CustomException(CustomError.INSUFFICIENT_ACCOUNT_BALANCE)


def _extract_extension(file_name: str) -> str:
    """取小写扩展名（不含点）；没有扩展名时返回空串。"""
    _, _, extension = file_name.rpartition(".")
    if not extension or extension == file_name:
        return ""
    return extension.lower()


def _ensure_extension_allowed(extension: str) -> None:
    """按扩展名白名单校验。"""
    if extension not in _ALLOWED_EXTENSIONS:
        raise CustomException(
            CustomError.FILE_TYPE_NOT_ALLOWED,
            detail=f"extension: {extension or '(none)'}"
        )


def _save_upload_to_temp(file: UploadFile, suffix: str) -> tuple:
    """
    把上传文件流式写入临时文件，同时统计字节数。

    Returns:
        tuple: (临时文件路径, 字节数)

    Raises:
        CustomException: 空文件（1001）或超过大小上限（2004）
    """
    os.makedirs(config.TEMP_DIR, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix="upload_", suffix=suffix or ".bin", dir=config.TEMP_DIR)

    total = 0
    try:
        with os.fdopen(fd, "wb") as tmp_out:
            while True:
                chunk = file.file.read(_CHUNK_SIZE)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_UPLOAD_SIZE_BYTES:
                    raise CustomException(
                        CustomError.FILE_SIZE_LIMIT_EXCEEDED,
                        detail=f"{MAX_UPLOAD_SIZE_BYTES / 1024 / 1024:.2f} MB"
                    )
                tmp_out.write(chunk)
    except Exception:
        _cleanup_temp_file(tmp_path)
        raise

    if total == 0:
        _cleanup_temp_file(tmp_path)
        raise CustomException(CustomError.PARAM_VALIDATION_FAILED, detail="empty file")

    return tmp_path, total


def _cleanup_temp_file(temp_file_path: Optional[str]) -> None:
    """清理临时文件；删除失败时交给后台延迟删除兜底。"""
    if not temp_file_path or not os.path.exists(temp_file_path):
        return
    try:
        os.remove(temp_file_path)
    except Exception as cleanup_error:
        logger.warning(f"Failed to cleanup temporary file {temp_file_path}: {cleanup_error}")
        enqueue_path(temp_file_path, is_dir=False)


def upload_file(file: UploadFile, api_key: Optional[str] = None) -> dict:
    """
    服务端中转上传：接收客户端文件 → 落盘统计体积 → 上传对象存储 → 上传成功后按体积扣费 → 返回签名 URL。

    计费规则：0.0005 元/MB，按实际字节数计算（保留 6 位小数）；仅在对象存储上传成功后扣费，
    扣费失败只记日志，不影响本次上传结果。

    Args:
        file: 客户端上传的文件（multipart/form-data 的 file 字段）
        api_key: 可选 API 密钥，config.ENABLE_APIKEY 为 true 时必传

    Returns:
        dict: url / key / size / size_mb / cost / url_expire_days

    Raises:
        CustomException: apiKey 非法、余额不足、文件名非法、文件类型不允许、文件为空或超限、上传失败
    """
    tmp_path: Optional[str] = None
    try:
        # 校验 apiKey 与余额门槛（余额需大于 1，与 gen_video 一致），在接收文件之前拦截
        _ensure_api_key(api_key)

        if not file.filename:
            raise CustomException(CustomError.INVALID_FILE_NAME)
        try:
            safe_name = sanitize_object_filename(file.filename)
        except ValueError as e:
            logger.warning(f"Invalid upload file name: {e}")
            raise CustomException(CustomError.INVALID_FILE_NAME)

        extension = _extract_extension(safe_name)
        _ensure_extension_allowed(extension)

        object_key = build_upload_object_key(safe_name)
        tmp_path, size = _save_upload_to_temp(file, suffix=os.path.splitext(safe_name)[1])

        size_mb = size / (1024 * 1024)
        cost = round(size_mb * UPLOAD_PRICE_PER_MB, 6)

        # 签名下载 URL 的有效期与草稿成片一致，共用 config.VIDEO_GEN_RETENTION_DAYS
        expire_days = config.VIDEO_GEN_RETENTION_DAYS
        url = upload_file_to_storage(tmp_path, expire_days=expire_days, object_key=object_key)

        charged = _charge_upload(api_key, cost, size_mb, object_key)

        logger.info(
            "Upload file success, key=%s, size_bytes=%s, cost=%s, charged=%s",
            object_key, size, cost, charged,
        )
        return {
            "url": url,
            "key": object_key,
            "size": size,
            "size_mb": round(size_mb, 3),
            "cost": cost if config.ENABLE_APIKEY else 0.0,
            "url_expire_days": expire_days,
        }
    except CustomException:
        raise
    except Exception as e:
        logger.error(f"Upload file failed: {e}")
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR)
    finally:
        _cleanup_temp_file(tmp_path)


def _charge_upload(api_key: Optional[str], cost: float, size_mb: float, object_key: str) -> bool:
    """
    上传成功后的扣费（尽力而为）：失败只记日志，不影响已完成的上传。

    Returns:
        bool: 是否实际扣费成功
    """
    if not config.ENABLE_APIKEY or not api_key or cost <= 0:
        return False

    try:
        charged = deduct_user_points(
            api_key=api_key,
            points=cost,
            desc=f"上传文件，体积{size_mb:.2f}MB，费用{cost:.6f}元"
        )
        if charged:
            logger.info(f"Upload file charged, key={object_key}, cost={cost}")
        else:
            logger.warning(f"Upload file charge failed, key={object_key}, cost={cost}")
        return charged
    except Exception as charge_error:
        logger.warning(f"Upload file charge error, key={object_key}, cost={cost}: {charge_error}")
        return False
