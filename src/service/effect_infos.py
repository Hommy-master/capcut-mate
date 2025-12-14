from src.utils.logger import logger
import json
from typing import List, Dict


def effect_infos(
    effects: List[str],
    timelines: List[Dict[str, int]]
) -> str:
    """
    根据特效名称和时间线生成特效信息JSON字符串
    
    Args:
        effects: 特效名称列表
        timelines: 时间线数组
        
    Returns:
        str: JSON字符串格式的特效信息
        
    Raises:
        ValueError: 当effects和timelines长度不匹配时
    """
    logger.info(f"effect_infos called with {len(effects)} effects and {len(timelines)} timelines")
    
    # 检查参数长度是否匹配
    if len(effects) != len(timelines):
        raise ValueError(f"effects length ({len(effects)}) does not match timelines length ({len(timelines)})")
    
    # 构建特效信息列表
    infos = []
    for i, (effect, timeline) in enumerate(zip(effects, timelines)):
        info = {
            "effect_title": effect,
            "start": timeline["start"],
            "end": timeline["end"]
        }
        
        infos.append(info)
        logger.info(f"Processed effect info {i+1}: {info}")
    
    # 转换为JSON字符串
    infos_json = json.dumps(infos, ensure_ascii=False)
    logger.info(f"Generated effect infos JSON with {len(infos)} items")
    
    return infos_json