from src.utils.logger import logger
import json
from typing import List, Dict, Optional


def filter_infos(
    filters: List[str],
    timelines: List[Dict[str, int]],
    intensities: Optional[List[float]] = None
) -> str:
    """
    根据滤镜名称、时间线和强度生成滤镜信息JSON字符串
    
    Args:
        filters: 滤镜名称列表
        timelines: 时间线数组
        intensities: 滤镜强度列表(0-100)，可选，默认为100
        
    Returns:
        str: JSON字符串格式的滤镜信息
        
    Raises:
        无异常抛出，长度不匹配时以最短的为准
    """
    logger.info(f"filter_infos called with {len(filters)} filters, {len(timelines)} timelines, intensities: {intensities}")
    
    # 确定最终处理长度（以最短的为准）
    min_len = min(len(filters), len(timelines))
    if intensities is not None:
        min_len = min(min_len, len(intensities))
    
    if len(filters) != len(timelines) or (intensities is not None and len(intensities) != len(filters)):
        logger.warning(f"Length mismatch - filters: {len(filters)}, timelines: {len(timelines)}, intensities: {intensities}, using shorter length: {min_len}")
        filters = filters[:min_len]
        timelines = timelines[:min_len]
        if intensities is not None:
            intensities = intensities[:min_len]
    
    # 构建滤镜信息列表
    infos = []
    for i, (filter_name, timeline) in enumerate(zip(filters, timelines)):
        info = {
            "filter_title": filter_name,
            "start": timeline["start"],
            "end": timeline["end"],
            "intensity": intensities[i] if intensities else 100.0
        }
        
        infos.append(info)
        logger.info(f"Processed filter info {i+1}: {info}")
    
    # 转换为JSON字符串
    infos_json = json.dumps(infos, ensure_ascii=False)
    logger.info(f"Generated filter infos JSON with {len(infos)} items")
    
    return infos_json
