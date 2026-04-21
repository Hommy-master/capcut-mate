# 实现阿里云对象存储（OSS）的上传功能
import datetime
import os
from typing import Optional

import config
from exceptions import CustomError, CustomException
from src.utils.logger import logger


def oss_upload_file(file_path: str, expire_days: Optional[int] = None) -> str:
    """
    上传文件到OSS，返回带签名的临时URL，链接在指定天数后失效（见 config.VIDEO_GEN_RETENTION_DAYS）。

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
        import oss2
    except ImportError as e:
        logger.error(f"OSS SDK import failed: {e}")
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR, "OSS SDK not installed")

    try:
        # 1. 生成带日期和小时的目录路径（格式：2025-10-15/22/文件名）
        now = datetime.datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_hour = now.strftime("%H")  # 小时，取值0-23
        filename = os.path.basename(file_path)
        key = f"{current_date}/{current_hour}/{filename}"

        # 2. 上传文件；预签名 URL 在 expire_days 天后失效
        expire_time = datetime.datetime.now() + datetime.timedelta(days=expire_days)
        expire_time_str = expire_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        auth = oss2.Auth(config.OSS_ACCESS_KEY_ID, config.OSS_ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, config.OSS_ENDPOINT, config.OSS_BUCKET_NAME)
        response = bucket.put_object_from_file(key, file_path)
        logger.info(f"OSS upload success, key: {key}, expire time: {expire_time_str}, status: {response.status}")

        # 3. 生成带签名的临时下载URL（有效期为expire_days天）
        signed_url = bucket.sign_url(
            method="GET",
            key=key,
            expires=expire_days * 24 * 3600,
        )
        logger.info(f"Generated OSS signed URL valid for {expire_days} day(s), URL: {signed_url[:100]}...")
        return signed_url

    except Exception as e:
        logger.error(f"OSS upload failed: {e}")
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR, "OSS upload failed")
