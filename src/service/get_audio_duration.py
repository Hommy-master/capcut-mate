from src.utils.logger import logger
from src.utils import helper
from exceptions import CustomException, CustomError
import config
import os
import subprocess
import json
from typing import Dict, Any, Optional


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
        temp_file_path = helper.download(mp3_url, config.TEMP_DIR)
        
        # 2. 使用ffprobe分析音频文件获取时长
        duration_microseconds = _analyze_audio_with_ffprobe(temp_file_path)
        
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


def _analyze_audio_with_ffprobe(file_path: str) -> int:
    """
    使用ffprobe分析音频文件获取时长
    
    Args:
        file_path: 音频文件路径
    
    Returns:
        duration: 音频时长，单位：微秒
    
    Raises:
        CustomException: 音频分析失败
    """
    logger.info(f"Using ffprobe to analyze audio file: {file_path}")
    
    try:
        # 构建ffprobe命令 - 根据记忆中的配置
        cmd = [
            'ffprobe', 
            '-i', file_path,
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams'
        ]
        
        logger.info(f"Executing ffprobe command: {' '.join(cmd)}")
        
        # 执行ffprobe命令
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=30,
            check=True
        )
        
        logger.info("FFprobe analysis completed successfully")
        
        # 解析ffprobe输出
        ffprobe_data = _parse_ffprobe_output(result.stdout)
        
        # 提取时长信息
        duration_seconds = _extract_duration_from_ffprobe_data(ffprobe_data)
        
        # 验证并转换时长
        return _validate_and_convert_duration(duration_seconds)
        
    except subprocess.TimeoutExpired:
        logger.error("FFprobe command timed out")
        raise CustomException(CustomError.AUDIO_DURATION_GET_FAILED, "Audio analysis timed out")
    except subprocess.CalledProcessError as e:
        logger.error(f"FFprobe command failed with return code {e.returncode}")
        logger.error(f"FFprobe stderr: {e.stderr}")
        raise CustomException(CustomError.AUDIO_DURATION_GET_FAILED, f"FFprobe analysis failed: {e.stderr}")
    except FileNotFoundError:
        logger.error("FFprobe command not found. Please ensure FFprobe is installed and in PATH")
        raise CustomException(CustomError.AUDIO_DURATION_GET_FAILED, "FFprobe tool not available")


def _parse_ffprobe_output(stdout: str) -> Dict[str, Any]:
    """
    解析ffprobe的JSON输出
    
    Args:
        stdout: ffprobe的标准输出
    
    Returns:
        解析后的JSON数据
    
    Raises:
        CustomException: JSON解析失败
    """
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse ffprobe JSON output: {e}")
        logger.error(f"FFprobe stdout: {stdout}")
        raise CustomException(CustomError.AUDIO_DURATION_GET_FAILED, "Failed to parse audio analysis result")


def _extract_duration_from_ffprobe_data(ffprobe_data: Dict[str, Any]) -> float:
    """
    从ffprobe数据中提取时长信息
    
    Args:
        ffprobe_data: ffprobe解析后的数据
    
    Returns:
        时长（秒）
    
    Raises:
        CustomException: 无法提取时长信息
    """
    # 优先从format信息中获取时长
    if 'format' in ffprobe_data and 'duration' in ffprobe_data['format']:
        duration_seconds = float(ffprobe_data['format']['duration'])
        logger.info(f"Got duration from format info: {duration_seconds}s")
        return duration_seconds
    
    # 如果format中没有时长，尝试从音频流中获取
    if 'streams' in ffprobe_data:
        for stream in ffprobe_data['streams']:
            if stream.get('codec_type') == 'audio' and 'duration' in stream:
                duration_seconds = float(stream['duration'])
                logger.info(f"Got duration from audio stream: {duration_seconds}s")
                return duration_seconds
    
    # 无法提取时长
    logger.error("Unable to extract duration from ffprobe output")
    logger.error(f"FFprobe output: {json.dumps(ffprobe_data, indent=2)}")
    raise CustomException(CustomError.AUDIO_DURATION_GET_FAILED, "Unable to extract duration from audio file")


def _validate_and_convert_duration(duration_seconds: float) -> int:
    """
    验证时长的合理性并转换为微秒
    
    Args:
        duration_seconds: 时长（秒）
    
    Returns:
        时长（微秒）
    
    Raises:
        CustomException: 时长无效
    """
    # 验证时长合理性
    if duration_seconds <= 0:
        logger.error(f"Invalid duration: {duration_seconds}s")
        raise CustomException(CustomError.AUDIO_DURATION_GET_FAILED, "Invalid audio duration")
    
    # 转换为微秒（保证精度）
    duration_microseconds = int(duration_seconds * 1_000_000)
    
    return duration_microseconds


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