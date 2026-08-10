"""
获取特效列表的业务逻辑处理模块
"""
import json
from typing import List, Dict, Any
from src.utils.logger import logger
from exceptions import CustomException, CustomError


def get_effects(mode: int = 0) -> List[Dict[str, Any]]:
    """
    获取特效列表
    
    Args:
        mode: 特效模式，0=所有，1=VIP，2=免费，默认值为 0
    
    Returns:
        effects: 特效对象数组
        
    Raises:
        CustomException: 获取特效列表失败
    """
    logger.info(f"get_effects called with mode: {mode}")
    
    try:
        # 1. 参数验证
        if mode not in [0, 1, 2]:
            logger.error(f"Invalid mode: {mode}")
            raise CustomException(CustomError.EFFECT_GET_FAILED)
        
        # 2. 根据模式获取特效数据
        effects = _get_effects_by_mode(mode=mode)
        logger.info(f"Found {len(effects)} effects for mode: {mode}")
        
        # 3. 直接返回对象数组
        logger.info(f"Successfully returned effects array with {len(effects)} items")
        
        return effects
        
    except CustomException:
        logger.error(f"Get effects failed for mode: {mode}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_effects: {str(e)}")
        raise CustomException(CustomError.EFFECT_GET_FAILED)


def _get_effects_by_mode(mode: int) -> List[Dict[str, Any]]:
    """
    根据模式获取对应的特效数据
    
    Args:
        mode: 特效模式（0=所有，1=VIP，2=免费）
    
    Returns:
        包含特效信息的列表
    """
    logger.info(f"Getting effects for mode: {mode}")
    
    # 从 VideoSceneEffectType 枚举中获取所有特效
    from src.pyJianYingDraft.metadata.video_scene_effect import VideoSceneEffectType
    
    all_effects = []
    for effect_type in VideoSceneEffectType:
        effect_info = {
            "name": effect_type.value.name,
            "is_vip": effect_type.value.is_vip,
            "resource_id": effect_type.value.resource_id,
            "effect_id": effect_type.value.effect_id,
            "icon_url": "",  # 特效元数据中没有 icon_url
            "has_params": len(effect_type.value.params) > 0
        }
        all_effects.append(effect_info)
    
    logger.info(f"Total effects loaded: {len(all_effects)}")
    
    # 根据模式过滤
    if mode == 0:  # 所有
        result = all_effects
    elif mode == 1:  # VIP
        result = [e for e in all_effects if e.get("is_vip", False)]
    elif mode == 2:  # 免费
        result = [e for e in all_effects if not e.get("is_vip", False)]
    else:
        result = []
    
    logger.info(f"Final filtered result: {len(result)} effects")
    return result
