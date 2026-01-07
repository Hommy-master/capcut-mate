from src.utils.logger import logger
import json
from typing import List, Optional, Dict, Any


def imgs_infos(
    imgs: List[str],
    timelines: List[Dict[str, int]],
    height: Optional[int] = None,
    width: Optional[int] = None,
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
    根据图片URL和时间线生成图片信息JSON字符串
    
    Args:
        imgs: 图片URL列表
        timelines: 时间线数组
        height: 视频高度（可选）
        width: 视频宽度（可选）
        in_animation: 入场动画名称（可选）
        in_animation_duration: 入场动画时长（可选）
        loop_animation: 组合动画名称（可选）
        loop_animation_duration: 组合动画时长（可选）
        out_animation: 出场动画名称（可选）
        out_animation_duration: 出场动画时长（可选）
        transition: 转场名称（可选）
        transition_duration: 转场时长（可选）
        
    Returns:
        str: JSON字符串格式的图片信息
        
    Raises:
        ValueError: 当imgs和timelines长度不匹配时
    """
    logger.info(f"imgs_infos called with {len(imgs)} images and {len(timelines)} timelines")
    
    # 检查参数长度是否匹配
    if len(imgs) != len(timelines):
        raise ValueError(f"imgs length ({len(imgs)}) does not match timelines length ({len(timelines)})")
    
    # 处理可能包含多个动画的参数，用 | 分隔
    in_animations = []
    if in_animation and isinstance(in_animation, str):
        in_animations = [anim.strip() for anim in in_animation.split('|') if anim.strip()]
    
    out_animations = []
    if out_animation and isinstance(out_animation, str):
        out_animations = [anim.strip() for anim in out_animation.split('|') if anim.strip()]
    
    loop_animations = []
    if loop_animation and isinstance(loop_animation, str):
        loop_animations = [anim.strip() for anim in loop_animation.split('|') if anim.strip()]
    
    # 构建图片信息列表
    infos = []
    for i, (img_url, timeline) in enumerate(zip(imgs, timelines)):
        info = {
            "image_url": img_url,
            "start": timeline["start"],
            "end": timeline["end"]
        }
        
        # 添加可选参数
        if height is not None:
            info["height"] = height
            
        if width is not None:
            info["width"] = width
            
        # 循环分配动画，如果动画列表为空则跳过
        if in_animations:
            info["in_animation"] = in_animations[i % len(in_animations)]
            
        if in_animation_duration is not None:
            info["in_animation_duration"] = in_animation_duration
            
        if loop_animations:
            info["loop_animation"] = loop_animations[i % len(loop_animations)]
            
        if loop_animation_duration is not None:
            info["loop_animation_duration"] = loop_animation_duration
            
        if out_animations:
            info["out_animation"] = out_animations[i % len(out_animations)]
            
        if out_animation_duration is not None:
            info["out_animation_duration"] = out_animation_duration
            
        if transition is not None:
            info["transition"] = transition
            
        if transition_duration is not None:
            info["transition_duration"] = transition_duration
            
        infos.append(info)
        logger.info(f"Processed image info {i+1}: {info}")
    
    # 转换为JSON字符串
    infos_json = json.dumps(infos, ensure_ascii=False)
    logger.info(f"Generated image infos JSON with {len(infos)} items")
    
    return infos_json