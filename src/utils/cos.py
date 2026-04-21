# 实现对象存储上传功能（优先COS，未配置时回退OSS）
import os
import datetime
from typing import Optional
import config
from src.utils.logger import logger
from exceptions import CustomException, CustomError


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


def _upload_file_to_cos(file_path: str, expire_days: int) -> str:
    """上传文件到COS并返回预签名URL。"""
    try:
        from qcloud_cos import CosConfig, CosS3Client
    except ImportError as e:
        logger.error(f"COS SDK import failed: {e}")
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR, "COS SDK not installed")

    cfg = CosConfig(
        Region=config.COS_REGION,
        SecretId=config.COS_SECRET_ID,
        SecretKey=config.COS_SECRET_KEY,
        Token=None,
    )
    cli = CosS3Client(cfg)

    # 1. 生成带日期和小时的目录路径（格式：2025-10-15/22/文件名）
    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_hour = now.strftime("%H")  # 小时，取值0-23
    filename = os.path.basename(file_path)
    key = f"{current_date}/{current_hour}/{filename}"

    # 2. 上传文件；预签名 URL 在 expire_days 天后失效
    expire_time = datetime.datetime.now() + datetime.timedelta(days=expire_days)
    expire_time_str = expire_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    response = cli.upload_file(
        Bucket=config.COS_BUCKET_NAME,
        Key=key,
        LocalFilePath=file_path
    )
    logger.info(f"COS upload success, key: {key}, expire time: {expire_time_str}, response: {response}")

    # 3. 生成带签名的临时下载URL（有效期为expire_days天）
    signed_url = cli.get_presigned_url(
        Method='GET',
        Bucket=config.COS_BUCKET_NAME,
        Key=key,
        Expired=expire_days * 24 * 3600  # 转换为秒数
    )
    logger.info(f"Generated COS signed URL valid for {expire_days} day(s), URL: {signed_url[:100]}...")
    return signed_url

def cos_upload_file(file_path: str, expire_days: Optional[int] = None) -> str:
    """
    上传文件到对象存储，返回带签名的临时URL，链接在指定天数后失效（见 config.VIDEO_GEN_RETENTION_DAYS）。

    选择策略：
    1. 若 COS 配置完整，优先使用 COS
    2. 否则若 OSS 配置完整，使用 OSS
    3. 都未配置时抛出异常

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
        if _is_cos_configured():
            logger.info("Detected COS config, using COS upload")
            return _upload_file_to_cos(file_path=file_path, expire_days=expire_days)

        if _is_oss_configured():
            logger.info("COS config not found, fallback to OSS upload")
            from src.utils.oss import oss_upload_file
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
