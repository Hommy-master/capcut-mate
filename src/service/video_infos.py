from src.utils.logger import logger
import json
from typing import List, Optional, Dict, Any


def video_infos(
    video_urls: List[str],
    timelines: List[Dict[str, int]],
    height: Optional[int] = None,
    width: Optional[int] = None,
    mask: Optional[str] = None,
    transition: Optional[str] = None,
    transition_duration: Optional[int] = None,
    volume: float = 1.0
) -> str:
    """
    根据视频URL和时间线生成视频信息JSON字符串
    
    Args:
        video_urls: 视频URL列表
        timelines: 时间线数组
        height: 视频高（可选）
        width: 视频宽（可选）
        mask: 视频蒙版（可选）
        transition: 转场名称（可选）
        transition_duration: 转场时长（可选）
        volume: 音量大小，默认1.0
        
    Returns:
        str: JSON字符串格式的视频信息
        
    Raises:
        ValueError: 当video_urls和timelines长度不匹配时
    """
    logger.info(f"video_infos called with {len(video_urls)} videos and {len(timelines)} timelines")
    
    # 检查参数长度是否匹配
    if len(video_urls) != len(timelines):
        raise ValueError(f"video_urls length ({len(video_urls)}) does not match timelines length ({len(timelines)})")
    
    # 构建视频信息列表
    infos = []
    for i, (video_url, timeline) in enumerate(zip(video_urls, timelines)):
        start = timeline["start"]
        end = timeline["end"]
        duration = end - start
        
        info = {
            "video_url": video_url,
            "start": start,
            "end": end,
            "duration": duration
        }
        
        # 添加可选参数
        if width is not None:
            info["width"] = width
            
        if height is not None:
            info["height"] = height
            
        if mask is not None:
            info["mask"] = mask
            
        if transition is not None:
            info["transition"] = transition
            
        if transition_duration is not None:
            info["transition_duration"] = transition_duration
            
        if volume is not None:
            info["volume"] = volume
            
        infos.append(info)
        logger.info(f"Processed video info {i+1}: {info}")
    
    # 转换为JSON字符串
    infos_json = json.dumps(infos, ensure_ascii=False)
    logger.info(f"Generated video infos JSON with {len(infos)} items")
    
    return infos_json