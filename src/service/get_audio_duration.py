from src.utils.logger import logger
from src.utils.download import download
from src.utils.media import get_media_duration
from exceptions import CustomException, CustomError
import config
import os
from typing import Optional


def get_audio_duration(mp3_url: str) -> int:
    """
    获取音频文件的时长
    
    Args:
        mp3_url: 音频文件URL，支持mp3等常见音频格式
    
    Returns:
        duration: 音频时长，单位：微秒
    
    Raises:
        CustomException: 获取音频时长失败
    """
    logger.info(f"get_audio_duration called with mp3_url: {mp3_url}")
    
    temp_file_path = None
    try:
        # 1. 下载音频文件到临时目录
        logger.info(f"Starting to download audio file from URL: {mp3_url}")
        temp_file_path = download(mp3_url, config.TEMP_DIR)
        
        # 2. 使用我们新创建的工具函数获取媒体时长
        duration_microseconds = get_media_duration(temp_file_path)
        
        if duration_microseconds is None:
            logger.error("Failed to get audio duration")
            raise CustomException(CustomError.AUDIO_DURATION_GET_FAILED, "Failed to get audio duration")
        
        logger.info(f"Audio duration extracted successfully: {duration_microseconds/1_000_000:.6f}s ({duration_microseconds} microseconds)")
        return duration_microseconds
        
    except CustomException:
        # CustomException 直接重新抛出，保持原有的错误信息
        raise
    except Exception as e:
        logger.error(f"Get audio duration failed with unexpected error: {str(e)}")
        raise CustomException(CustomError.AUDIO_DURATION_GET_FAILED, f"Unexpected error: {str(e)}")
    finally:
        # 3. 清理临时文件
        _cleanup_temp_file(temp_file_path)




def _cleanup_temp_file(temp_file_path: Optional[str]) -> None:
    """
    清理临时文件
    
    Args:
        temp_file_path: 临时文件路径，可能为None
    """
    if temp_file_path and os.path.exists(temp_file_path):
        try:
            os.remove(temp_file_path)
            logger.info(f"Temporary file removed: {temp_file_path}")
        except Exception as cleanup_error:
            logger.warning(f"Failed to cleanup temporary file {temp_file_path}: {cleanup_error}")

