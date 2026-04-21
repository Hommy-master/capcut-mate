# 对象存储统一上传入口（配置判断 + 路由分发）
from typing import Optional

import config
from exceptions import CustomError, CustomException
from src.utils.logger import logger
from src.utils.cos import cos_upload_file
from src.utils.oss import oss_upload_file


def _is_valid_storage_config(value: str) -> bool:
    """判断存储配置项是否有效（空串和占位符视为未配置）。"""
    normalized = (value or "").strip()
    return normalized != "" and normalized.lower() != "xxx"


def _is_cos_configured() -> bool:
    """判断 COS 配置是否完整有效。"""
    return all(
        _is_valid_storage_config(item)
        for item in (config.COS_SECRET_ID, config.COS_SECRET_KEY, config.COS_BUCKET_NAME, config.COS_REGION)
    )


def _is_oss_configured() -> bool:
    """判断 OSS 配置是否完整有效。"""
    return all(
        _is_valid_storage_config(item)
        for item in (
            config.OSS_ACCESS_KEY_ID,
            config.OSS_ACCESS_KEY_SECRET,
            config.OSS_BUCKET_NAME,
            config.OSS_ENDPOINT,
        )
    )


def upload_file(file_path: str, expire_days: Optional[int] = None) -> str:
    """
    上传文件到对象存储并返回带签名的临时URL。

    选择策略：
    1. 若 COS 配置完整，优先使用 COS
    2. 否则若 OSS 配置完整，使用 OSS
    3. 都未配置时抛出异常
    """
    if expire_days is None:
        expire_days = config.VIDEO_GEN_RETENTION_DAYS

    try:
        if _is_cos_configured():
            logger.info("Detected COS config, using COS upload")
            return cos_upload_file(file_path=file_path, expire_days=expire_days)

        if _is_oss_configured():
            logger.info("COS config not found, fallback to OSS upload")
            return oss_upload_file(file_path=file_path, expire_days=expire_days)

        raise CustomException(
            CustomError.INTERNAL_SERVER_ERROR,
            "Neither COS nor OSS storage config is available"
        )
    except Exception as e:
        if isinstance(e, CustomException):
            raise
        logger.error(f"Storage upload failed: {e}")
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR, "Storage upload failed")
