from src.utils.logger import logger
import json
from typing import List, Optional, Dict, Any


def audio_infos(
    mp3_urls: List[str],
    timelines: List[Dict[str, int]],
    audio_effect: Optional[str] = None,
    volume: Optional[float] = None
) -> str:
    """
    根据音频URL和时间线生成音频信息JSON字符串
    
    Args:
        mp3_urls: 音频文件URL数组
        timelines: 时间线数组
        audio_effect: 音频效果（可选）
        volume: 音量（可选）
        
    Returns:
        str: JSON字符串格式的音频信息
        
    Raises:
        ValueError: 当mp3_urls和timelines长度不匹配时
    """
    logger.info(f"audio_infos called with {len(mp3_urls)} audio files and {len(timelines)} timelines")
    
    # 检查参数长度是否匹配
    if len(mp3_urls) != len(timelines):
        raise ValueError(f"mp3_urls length ({len(mp3_urls)}) does not match timelines length ({len(timelines)})")
    
    # 构建音频信息列表
    infos = []
    for i, (audio_url, timeline) in enumerate(zip(mp3_urls, timelines)):
        info = {
            "audio_url": audio_url,
            "start": timeline["start"],
            "end": timeline["end"]
        }
        
        # 添加可选参数
        if audio_effect is not None:
            info["audio_effect"] = audio_effect
            
        if volume is not None:
            info["volume"] = volume
            
        infos.append(info)
        logger.info(f"Processed audio info {i+1}: {info}")
    
    # 转换为JSON字符串
    infos_json = json.dumps(infos, ensure_ascii=False)
    logger.info(f"Generated audio infos JSON with {len(infos)} items")
    
    return infos_json