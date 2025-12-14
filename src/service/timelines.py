from src.utils.logger import logger
from typing import List, Dict, Tuple


def timelines(duration: int, num: int, start: int, type: int) -> Tuple[List[Dict[str, int]], List[Dict[str, int]]]:
    """
    计算时间线分割点
    
    Args:
        duration: 总时长
        num: 分割段数
        start: 开始时间
        type: 分割类型 (0: 平均分, 1: 随机)
    
    Returns:
        tuple: (timelines, all_timelines)
    """
    logger.info(f"timelines, duration: {duration}, num: {num}, start: {start}, type: {type}")
    
    timelines = []
    all_timelines = [{"start": start, "end": start + duration}]
    
    if num <= 0:
        return [], all_timelines
        
    if type == 0:  # 平均分
        segment_duration = duration // num
        for i in range(num):
            seg_start = start + i * segment_duration
            seg_end = start + (i + 1) * segment_duration if i < num - 1 else start + duration
            timelines.append({"start": seg_start, "end": seg_end})
    else:  # 随机分 (简化实现，实际可能需要更复杂的随机算法)
        import random
        random.seed(42)  # 固定种子以便测试
        points = sorted([random.randint(start, start + duration) for _ in range(num - 1)])
        points = [start] + points + [start + duration]
        for i in range(len(points) - 1):
            timelines.append({"start": points[i], "end": points[i + 1]})
            
    return timelines, all_timelines
