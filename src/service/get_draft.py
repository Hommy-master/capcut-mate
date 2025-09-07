from exceptions import CustomException, CustomError
from src.utils.logger import logger
from src.utils import helper
import config
import os

def gen_download_url(file_path: str) -> str:
    """
    生成下载URL，将文件路径中的/app/替换成DOWNLOAD_URL
    
    Args:
        file_path: 文件路径
    
    Returns:
        download_url: 下载URL
    """
    # 替换文件路径中的/app/为DOWNLOAD_URL
    download_url = file_path.replace("/app/", config.DOWNLOAD_URL)
    return download_url

def batch_gen_download_url(file_paths: list) -> list:
    """
    批量生成下载URL
    
    Args:
        file_paths: 文件路径列表
    
    Returns:
        download_urls: 下载URL列表
    """
    download_urls = []
    for file_path in file_paths:
        download_url = gen_download_url(file_path)
        download_urls.append(download_url)
    return download_urls

def get_draft(draft_id: str) -> list[str]:
    """
    获取剪映草稿的业务逻辑
    
    Args:
        draft_url: 草稿URL
    
    Returns:
        files: 文件列表

    Raises:
        CustomException: 自定义异常
    """

    # 1. 从URL中提取草稿ID
    if not draft_id:
        logger.info("draft_id is empty")
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    draft_dir = os.path.join(config.DRAFT_DIR, draft_id)
    if not os.path.exists(draft_dir):
        logger.info(f"draft_dir not exists: {draft_dir}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)
    
    # 2. 从草稿目录中获取文件列表
    files = helper.get_all_files(draft_dir)

    # 3. 批量生成下载URL
    download_urls = batch_gen_download_url(files)

    logger.info(f"get draft success: {draft_id}, download urls: {download_urls}")
    return download_urls

