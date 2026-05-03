# 实现腾讯云对象存储（COS）的上传功能
import os
import datetime
from typing import Optional
import config
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from src.utils.logger import logger
from src.utils.storage_upload_retry import run_with_storage_retry
from exceptions import CustomException, CustomError


def cos_upload_file(file_path: str, expire_days: Optional[int] = None) -> str:
    """
    上传文件到COS，返回带签名的临时URL，链接在指定天数后失效（见 config.VIDEO_GEN_RETENTION_DAYS）。

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

    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_hour = now.strftime("%H")
    filename = os.path.basename(file_path)
    key = f"{current_date}/{current_hour}/{filename}"

    cfg = CosConfig(
        Region=config.COS_REGION,
        SecretId=config.COS_SECRET_ID,
        SecretKey=config.COS_SECRET_KEY,
        Token=None
    )

    def do_upload() -> str:
        # SDK 内 retry；业务层在 storage_upload_retry 中再套一层
        cli = CosS3Client(cfg, retry=5)
        expire_time = datetime.datetime.now() + datetime.timedelta(days=expire_days)
        expire_time_str = expire_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        response = cli.upload_file(
            Bucket=config.COS_BUCKET_NAME,
            Key=key,
            LocalFilePath=file_path
        )
        logger.info(f"COS upload success, key: {key}, expire time: {expire_time_str}, response: {response}")

        signed_url = cli.get_presigned_url(
            Method='GET',
            Bucket=config.COS_BUCKET_NAME,
            Key=key,
            Expired=expire_days * 24 * 3600
        )
        logger.info(f"Generated COS signed URL valid for {expire_days} day(s), URL: {signed_url[:100]}...")
        return signed_url

    try:
        return run_with_storage_retry(do_upload, context="COS")
    except Exception as e:
        logger.error(f"COS upload failed: {e}")
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR, "COS upload failed")
