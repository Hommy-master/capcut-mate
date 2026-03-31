"""
获取花字效果列表和解析花字效果标识符的业务逻辑处理模块
"""
from typing import List, Dict, Any, Optional
from src.utils.logger import logger
from exceptions import CustomException, CustomError


# 导入自动生成的花字效果映射表
try:
    from .text_effect_map_generated import TEXT_EFFECT_MAP
except ImportError:
    # Fallback: use empty map if generated file doesn't exist
    TEXT_EFFECT_MAP = {}


def resolve_text_effect(effect_identifier: str) -> Optional[Dict[str, Any]]:
    """
    解析花字效果标识符，返回对应的效果信息
    
    Args:
        effect_identifier: 可以是 effect_id（数字字符串）或效果名称（中文名称）
    
    Returns:
        花字效果信息字典，包含 resource_id 和 effect_id，如果未找到则返回 None
    """
    logger.debug(f"Resolving text effect: {effect_identifier}")
    
    # 1. 尝试作为 effect_id 查找
    if effect_identifier.isdigit() or effect_identifier in [v["effect_id"] for v in TEXT_EFFECT_MAP.values()]:
        for effect_name, effect_data in TEXT_EFFECT_MAP.items():
            if effect_data["effect_id"] == effect_identifier:
                return {
                    "resource_id": effect_data["resource_id"],
                    "effect_id": effect_data["effect_id"]
                }
        # 如果是数字但不在映射表中，直接使用（可能是新的 effect_id）
        return {
            "resource_id": effect_identifier,
            "effect_id": effect_identifier
        }
    
    # 2. 尝试作为中文名称查找
    if effect_identifier in TEXT_EFFECT_MAP:
        effect_data = TEXT_EFFECT_MAP[effect_identifier]
        return {
            "resource_id": effect_data["resource_id"],
            "effect_id": effect_data["effect_id"]
        }
    
    # 3. 未找到
    logger.warning(f"Text effect not found: {effect_identifier}")
    return None


def get_text_effects(mode: int = 0) -> List[Dict[str, Any]]:
    """
    获取花字效果列表
    
    Args:
        mode: 花字效果模式，0=所有，1=VIP，2=免费，默认值为 0
    
    Returns:
        text_effects: 花字效果对象数组
        
    Raises:
        CustomException: 获取花字效果列表失败
    """
    logger.info(f"get_text_effects called with mode: {mode}")
    
    try:
        # 1. 参数验证
        if mode not in [0, 1, 2]:
            logger.error(f"Invalid mode: {mode}")
            raise CustomException(CustomError.FILTER_GET_FAILED)
        
        # 2. 根据模式获取花字效果数据
        text_effects = _get_text_effects_by_mode(mode=mode)
        logger.info(f"Found {len(text_effects)} text effects for mode: {mode}")
        
        # 3. 直接返回对象数组
        logger.info(f"Successfully returned text effects array with {len(text_effects)} items")
        
        return text_effects
        
    except CustomException:
        logger.error(f"Get text effects failed for mode: {mode}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_text_effects: {str(e)}")
        raise CustomException(CustomError.FILTER_GET_FAILED)


def _get_text_effects_by_mode(mode: int) -> List[Dict[str, Any]]:
    """
    根据模式获取对应的花字效果数据
    
    Args:
        mode: 花字效果模式（0=所有，1=VIP，2=免费）
    
    Returns:
        包含花字效果信息的列表
    """
    logger.info(f"Getting text effects for mode: {mode}")
    
    # 从自动生成的映射表中获取所有花字效果
    try:
        from src.service.text_effect_map_generated import TEXT_EFFECT_MAP
    except ImportError:
        logger.warning("text_effect_map_generated not found, using empty map")
        TEXT_EFFECT_MAP = {}
    
    all_text_effects = []
    for effect_name, effect_data in TEXT_EFFECT_MAP.items():
        effect_info = {
            "name": effect_data.get("name", effect_name),
            "is_vip": effect_data.get("is_vip", False),
            "resource_id": effect_data.get("resource_id", ""),
            "effect_id": effect_data.get("effect_id", "")
        }
        all_text_effects.append(effect_info)
    
    logger.info(f"Total text effects loaded: {len(all_text_effects)}")
    
    # 根据模式过滤
    if mode == 0:  # 所有
        result = all_text_effects
    elif mode == 1:  # VIP
        result = [f for f in all_text_effects if f.get("is_vip", False)]
    elif mode == 2:  # 免费
        result = [f for f in all_text_effects if not f.get("is_vip", False)]
    else:
        result = []
    
    logger.info(f"Final filtered result: {len(result)} text effects")
    return result
