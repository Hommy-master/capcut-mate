from src.utils.logger import logger
import json
from typing import List, Dict, Any


def calculate_relative_time_offset(offset_percent: int, duration: int) -> int:
    """
    根据百分比和持续时间计算相对时间偏移
    
    Args:
        offset_percent: 时间百分比 (0-100)
        duration: 片段持续时间（微秒）
        
    Returns:
        int: 相对时间偏移（微秒）
    """
    return int((offset_percent / 100.0) * duration)


def normalize_keyframe_value(ctype: str, value: float, height: int = None, width: int = None) -> float:
    """
    根据关键帧类型对值进行归一化处理
    
    Args:
        ctype: 关键帧类型
        value: 原始值
        height: 视频高度
        width: 视频宽度
        
    Returns:
        float: 归一化后的值
    """
    normalized_value = value
    if ctype == "KFTypePositionX" and width is not None and width > 0:
        normalized_value = value / width
    elif ctype == "KFTypePositionY" and height is not None and height > 0:
        normalized_value = value / height
    
    return normalized_value


def keyframes_infos(
    ctype: str,
    offsets: str,
    values: str,
    segment_infos: List[Dict[str, Any]],
    height: int = None,
    width: int = None
) -> str:
    """
    根据关键帧类型、位置比例和值生成关键帧信息JSON字符串
    
    Args:
        ctype: 关键帧类型
        offsets: 需要放置关键帧的位置比例
        values: 对应offsets的值
        segment_infos: 轨道数据数组
        height: 视频高，可选参数
        width: 视频宽，可选参数
        
    Returns:
        str: JSON字符串格式的关键帧信息
        
    Raises:
        ValueError: 当offsets和values长度不匹配时，或其他参数验证失败时
    """
    logger.info(f"keyframes_infos called with ctype={ctype}, offsets={offsets}, values={values}")
    
    # 解析offsets和values
    offset_list = [int(x) for x in offsets.split("|")]
    value_list = [float(x) for x in values.split("|")]
    
    # 检查offsets和values长度是否匹配
    if len(offset_list) != len(value_list):
        raise ValueError(f"offsets length ({len(offset_list)}) does not match values length ({len(value_list)})")
    
    # 构建关键帧信息列表
    keyframes = []
    
    # 处理每个片段信息
    for segment_info in segment_infos:
        segment_id = segment_info["id"]
        start = segment_info["start"]
        end = segment_info["end"]
        duration = end - start
        
        # 为每个offset创建关键帧
        for offset_percent, value in zip(offset_list, value_list):
            # 计算片段内的相对时间偏移（微秒）
            relative_time_offset = calculate_relative_time_offset(offset_percent, duration)
            
            # 根据关键帧类型处理值的归一化
            normalized_value = normalize_keyframe_value(ctype, value, height, width)
            
            keyframe = {
                "offset": relative_time_offset,  # 使用片段相对时间而不是轨道绝对时间
                "property": ctype,
                "segment_id": segment_id,
                "value": normalized_value
            }
            
            keyframes.append(keyframe)
            logger.info(f"Processed keyframe: {keyframe}")
    
    # 转换为JSON字符串
    keyframes_json = json.dumps(keyframes, ensure_ascii=False)
    logger.info(f"Generated keyframes infos JSON with {len(keyframes)} items")
    
    return keyframes_json