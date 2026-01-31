# 实现腾讯云对象存储（COS）的上传功能
import os
import datetime
import config
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from src.utils.logger import logger
from exceptions import CustomException, CustomError

def cos_upload_file(file_path: str, expire_days: int = 1) -> str:
    """
    上传文件到COS，返回带签名的临时URL，文件会在指定天数后自动过期
    
    Args:
        file_path: 文件路径
        expire_days: URL有效期天数，默认1天

    Returns:
        str: 带签名的临时下载URL（有效期为expire_days天）
    
    Raises:
        CustomException: 上传失败
    """
    cfg = CosConfig(Region=config.COS_REGION, SecretId=config.COS_SECRET_ID, SecretKey=config.COS_SECRET_KEY, Token=None)
    cli = CosS3Client(cfg)
    try:
        # 1. 生成带日期和小时的目录路径（格式：2025-10-15/22/文件名）
        now = datetime.datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_hour = now.strftime("%H")  # 小时，取值0-23
        filename = os.path.basename(file_path)
        key = f"{current_date}/{current_hour}/{filename}"
        
        # 2. 上传文件，并设置1天后自动删除
        # 计算过期时间（当前时间 + expire_days天）
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
