# 实现腾讯云对象存储（COS）的上传功能
import os
import datetime
from typing import Optional
import config
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from src.utils.logger import logger
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
    cfg = CosConfig(Region=config.COS_REGION, SecretId=config.COS_SECRET_ID, SecretKey=config.COS_SECRET_KEY, Token=None)
    cli = CosS3Client(cfg)
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
        
        logger.info(f"Generated signed URL valid for {expire_days} day(s), URL: {signed_url[:100]}...")
        return signed_url
        
    except Exception as e:
        logger.error(f"COS upload failed: {e}")
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR, "COS upload failed")
