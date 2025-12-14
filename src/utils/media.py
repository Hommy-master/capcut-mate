import subprocess
import os
from typing import Optional
from src.utils.logger import logger


def get_media_duration(file_path: str) -> Optional[int]:
    """
    获取音视频文件的时长，返回微秒数
    
    Args:
        file_path (str): 音视频文件的路径
        
    Returns:
        Optional[int]: 文件时长（微秒），如果获取失败则返回 None
        
    Example:
        duration_us = get_media_duration("test.mp3")
        if duration_us:
            print(f"文件时长: {duration_us} 微秒")
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在: {file_path}")
            return None
            
        # 使用 ffprobe 获取媒体信息
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ]
        
        # 执行命令并获取输出
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30  # 设置超时时间
        )
        
        # 检查命令执行是否成功
        if result.returncode != 0:
            logger.error(f"ffprobe 执行失败: {result.stderr}")
            return None
            
        # 解析输出
        duration_str = result.stdout.strip()
        if not duration_str:
            logger.warning(f"未能获取到文件时长: {file_path}")
            return None
            
        # 转换为浮点数（秒）
        duration_seconds = float(duration_str)
        
        # 转换为微秒
        duration_microseconds = int(duration_seconds * 1_000_000)
        
        logger.info(f"文件 {file_path} 的时长: {duration_microseconds} 微秒")
        return duration_microseconds
        
    except subprocess.TimeoutExpired:
        logger.error(f"ffprobe 执行超时: {file_path}")
        return None
    except ValueError as e:
        logger.error(f"解析时长失败: {e}, 输出内容: {result.stdout if 'result' in locals() else 'N/A'}")
        return None
    except Exception as e:
        logger.error(f"获取媒体文件时长时发生未知错误: {e}")
        return None


def get_media_duration_formatted(file_path: str) -> Optional[str]:
    """
    获取音视频文件的时长，返回格式化的字符串 (HH:MM:SS.mmm)
    
    Args:
        file_path (str): 音视频文件的路径
        
    Returns:
        Optional[str]: 格式化的时长字符串，如果获取失败则返回 None
    """
    duration_us = get_media_duration(file_path)
    if duration_us is None:
        return None
        
    # 转换为秒和毫秒
    total_seconds = duration_us / 1_000_000
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds % 1) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"