from src.utils.logger import logger
from src.utils.download import download
from src.utils.media import get_media_duration
from exceptions import CustomException, CustomError
import config
import os
from typing import List, Tuple, Optional


def audio_timelines(links: List[str]) -> Tuple[List[dict], List[dict]]:
    """
    根据音频文件时长计算时间线分割点
    
    Args:
        links: 音频文件URL数组
        
    Returns:
        tuple: (timelines, all_timelines)
        
    Raises:
        CustomException: 处理过程中出现错误
    """
    logger.info(f"audio_timelines called with {len(links)} audio files")
    
    if not links:
        logger.warning("No audio links provided")
        return [], [{"start": 0, "end": 0}]
    
    temp_files = []
    durations = []
    
    try:
        # 1. 下载所有音频文件并获取时长
        for i, link in enumerate(links):
            logger.info(f"Processing audio file {i+1}/{len(links)}: {link}")
            temp_file_path = None
            try:
                # 下载音频文件
                temp_file_path = download(link, config.TEMP_DIR)
                temp_files.append(temp_file_path)
                
                # 获取音频时长
                duration_microseconds = get_media_duration(temp_file_path)
                if duration_microseconds is None:
                    raise CustomException(CustomError.AUDIO_DURATION_GET_FAILED, f"Failed to get duration for audio: {link}")
                
                durations.append(duration_microseconds)
                logger.info(f"Audio {i+1} duration: {duration_microseconds} microseconds")
                
            except CustomException:
                raise
            except Exception as e:
                logger.error(f"Error processing audio file {link}: {str(e)}")
                raise CustomException(CustomError.AUDIO_DURATION_GET_FAILED, f"Error processing audio file {link}: {str(e)}")
        
        # 2. 计算时间线
        timelines, all_timelines = _calculate_timelines(durations)
        
        logger.info(f"Calculated timelines for {len(links)} audio files")
        return timelines, all_timelines
        
    finally:
        # 3. 清理临时文件
        _cleanup_temp_files(temp_files)


def _calculate_timelines(durations: List[int]) -> Tuple[List[dict], List[dict]]:
    """
    根据音频时长计算时间线
    
    Args:
        durations: 音频时长列表（微秒）
        
    Returns:
        tuple: (timelines, all_timelines)
    """
    if not durations:
        return [], [{"start": 0, "end": 0}]
    
    # 计算累积时长
    cumulative_durations = []
    cumulative = 0
    for duration in durations:
        cumulative_durations.append({
            "start": cumulative,
            "end": cumulative + duration
        })
        cumulative += duration
    
    # 返回结果
    return cumulative_durations, [{"start": 0, "end": cumulative}]


def _cleanup_temp_files(temp_files: List[str]) -> None:
    """
    清理临时文件
    
    Args:
        temp_files: 临时文件路径列表
    """
    for temp_file_path in temp_files:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.info(f"Temporary file removed: {temp_file_path}")
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup temporary file {temp_file_path}: {cleanup_error}")