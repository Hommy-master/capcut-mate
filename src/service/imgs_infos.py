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
    
    # 解析动画参数
    parsed_animations = _parse_animation_params(in_animation, out_animation, loop_animation, transition)
    in_animations, out_animations, loop_animations, transition_animations = parsed_animations
    
    # 构建图片信息列表
    infos = []
    for i, (img_url, timeline) in enumerate(zip(imgs, timelines)):
        info = _build_image_info(img_url, timeline, height, width, i, 
                                in_animations, out_animations, loop_animations, transition_animations,
                                in_animation_duration, out_animation_duration, 
                                loop_animation_duration, transition_duration)
        infos.append(info)
        logger.info(f"Processed image info {i+1}: {info}")
    
    # 转换为JSON字符串
    infos_json = json.dumps(infos, ensure_ascii=False)
    logger.info(f"Generated image infos JSON with {len(infos)} items")
    
    return infos_json


def _parse_animation_params(in_animation, out_animation, loop_animation, transition):
    """解析动画参数，将用|分隔的字符串转换为列表"""
    def parse_single_param(param):
        if param is not None and isinstance(param, str):
            return [anim.strip() for anim in param.split('|') if anim.strip()]
        return []
    
    in_animations = parse_single_param(in_animation)
    out_animations = parse_single_param(out_animation)
    loop_animations = parse_single_param(loop_animation)
    transition_animations = parse_single_param(transition)
    
    return in_animations, out_animations, loop_animations, transition_animations


def _build_image_info(img_url, timeline, height, width, i,
                      in_animations, out_animations, loop_animations, transition_animations,
                      in_animation_duration, out_animation_duration,
                      loop_animation_duration, transition_duration):
    """构建单个图片信息字典"""
    info = {
        "image_url": img_url,
        "start": timeline["start"],
        "end": timeline["end"]
    }
    
    # 添加尺寸参数
    if height is not None:
        info["height"] = height
    if width is not None:
        info["width"] = width
    
    # 添加动画参数，只有当动画存在时才添加对应的duration
    _add_animation_if_exists(info, "in_animation", in_animations, i, in_animation_duration)
    _add_animation_if_exists(info, "out_animation", out_animations, i, out_animation_duration)
    _add_animation_if_exists(info, "loop_animation", loop_animations, i, loop_animation_duration)
    _add_animation_if_exists(info, "transition", transition_animations, i, transition_duration)
    
    return info


def _add_animation_if_exists(info, animation_key, animations, index, duration):
    """如果动画存在，则添加动画和对应的duration"""
    if animations and index < len(animations):
        info[animation_key] = animations[index]
        # 只有当动画存在时才添加对应的duration
        if duration is not None:
            duration_key = animation_key + "_duration"
            info[duration_key] = duration