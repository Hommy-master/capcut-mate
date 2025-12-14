from src.utils.logger import logger
import json
from typing import List, Optional, Dict, Any


def caption_infos(
    texts: List[str],
    timelines: List[Dict[str, int]],
    font_size: Optional[int] = None,
    keyword_color: Optional[str] = None,
    keyword_font_size: Optional[int] = None,
    keywords: Optional[List[str]] = None,
    in_animation: Optional[str] = None,
    in_animation_duration: Optional[int] = None,
    loop_animation: Optional[str] = None,
    loop_animation_duration: Optional[int] = None,
    out_animation: Optional[str] = None,
    out_animation_duration: Optional[int] = None,
    transition: Optional[str] = None,
    transition_duration: Optional[int] = None
) -> str:
    """
    根据文本和时间线生成字幕信息JSON字符串
    
    Args:
        texts: 文本列表
        timelines: 时间线数组
        font_size: 字体大小（可选）
        keyword_color: 关键词颜色（可选）
        keyword_font_size: 关键词字体大小（可选）
        keywords: 文本里面的重点词列表（可选）
        in_animation: 入场动画名称（可选）
        in_animation_duration: 入场动画时长（可选）
        loop_animation: 组合动画名称（可选）
        loop_animation_duration: 组合动画时长（可选）
        out_animation: 出场动画名称（可选）
        out_animation_duration: 出场动画时长（可选）
        transition: 转场名称（可选）
        transition_duration: 转场时长（可选）
        
    Returns:
        str: JSON字符串格式的字幕信息
        
    Raises:
        ValueError: 当texts和timelines长度不匹配时，或者keywords长度与texts不匹配时
    """
    logger.info(f"caption_infos called with {len(texts)} texts and {len(timelines)} timelines")
    
    # 检查参数长度是否匹配
    if len(texts) != len(timelines):
        raise ValueError(f"texts length ({len(texts)}) does not match timelines length ({len(timelines)})")
    
    # 检查keywords长度是否匹配
    if keywords is not None and len(keywords) != len(texts):
        raise ValueError(f"keywords length ({len(keywords)}) does not match texts length ({len(texts)})")
    
    # 构建字幕信息列表
    infos = []
    for i, (text, timeline) in enumerate(zip(texts, timelines)):
        info = {
            "start": timeline["start"],
            "end": timeline["end"],
            "text": text
        }
        
        # 添加关键词信息
        if keywords is not None:
            info["keyword"] = keywords[i]
            
        # 添加可选参数
        if keyword_color is not None:
            info["keyword_color"] = keyword_color
            
        if keyword_font_size is not None:
            info["keyword_font_size"] = keyword_font_size
            
        if font_size is not None:
            info["font_size"] = font_size
            
        if in_animation is not None:
            info["in_animation"] = in_animation
            
        if in_animation_duration is not None:
            info["in_animation_duration"] = in_animation_duration
            
        if loop_animation is not None:
            info["loop_animation"] = loop_animation
            
        if loop_animation_duration is not None:
            info["loop_animation_duration"] = loop_animation_duration
            
        if out_animation is not None:
            info["out_animation"] = out_animation
            
        if out_animation_duration is not None:
            info["out_animation_duration"] = out_animation_duration
            
        if transition is not None:
            info["transition"] = transition
            
        if transition_duration is not None:
            info["transition_duration"] = transition_duration
            
        infos.append(info)
        logger.info(f"Processed caption info {i+1}: {info}")
    
    # 转换为JSON字符串
    infos_json = json.dumps(infos, ensure_ascii=False)
    logger.info(f"Generated caption infos JSON with {len(infos)} items")
    
    return infos_json