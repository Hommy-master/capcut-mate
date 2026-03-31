"""
获取花字列表的业务逻辑处理模块
"""
import json
from typing import List, Dict, Any, Optional
from src.utils.logger import logger
from exceptions import CustomException, CustomError

# 导入自动生成的花字效果映射表
try:
    from .text_effect_map_generated import TEXT_EFFECT_MAP
except ImportError:
    # 如果生成的文件不存在，使用默认的映射表
    TEXT_EFFECT_MAP = {
        # 热门花字效果
        "白字橘色发光花字": {
            "resource_id": "7296357486490144036",
            "effect_id": "7296357486490144036",
            "name": "白字橘色发光花字",
            "is_vip": False
        },
        "黄字白色发光花字": {
            "resource_id": "7296357486490144037",
            "effect_id": "7296357486490144037",
            "name": "黄字白色发光花字",
            "is_vip": False
        },
        "粉字白色发光花字": {
            "resource_id": "7296357486490144038",
            "effect_id": "7296357486490144038",
            "name": "粉字白色发光花字",
            "is_vip": False
        },
        "绿字白色发光花字": {
            "resource_id": "7296357486490144039",
            "effect_id": "7296357486490144039",
            "name": "绿字白色发光花字",
            "is_vip": False
        },
        "蓝字白色发光花字": {
            "resource_id": "7296357486490144040",
            "effect_id": "7296357486490144040",
            "name": "蓝字白色发光花字",
            "is_vip": False
        },
        "紫字白色发光花字": {
            "resource_id": "7296357486490144041",
            "effect_id": "7296357486490144041",
            "name": "紫字白色发光花字",
            "is_vip": False
        },
    }


def get_text_effects(mode: int = 0) -> List[Dict[str, Any]]:
    """
    获取花字列表
    
    Args:
        mode: 花字模式，0=所有，1=VIP，2=免费，默认值为 0
    
    Returns:
        effects: 花字对象数组
        
    Raises:
        CustomException: 获取花字列表失败
    """
    logger.info(f"get_text_effects called with mode: {mode}")
    
    try:
        # 1. 参数验证
        if mode not in [0, 1, 2]:
            logger.error(f"Invalid mode: {mode}")
            raise CustomException(CustomError.EFFECT_GET_FAILED)
        
        # 2. 根据模式获取花字数据
        effects = _get_text_effects_by_mode(mode=mode)
        logger.info(f"Found {len(effects)} text effects for mode: {mode}")
        
        # 3. 直接返回对象数组
        logger.info(f"Successfully returned text effects array with {len(effects)} items")
        
        return effects
        
    except CustomException:
        logger.error(f"Get text effects failed for mode: {mode}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_text_effects: {str(e)}")
        raise CustomException(CustomError.EFFECT_GET_FAILED)


def _get_text_effects_by_mode(mode: int) -> List[Dict[str, Any]]:
    """
    根据模式获取对应的花字数据
    
    Args:
        mode: 花字模式（0=所有，1=VIP，2=免费）
    
    Returns:
        包含花字信息的列表
    """
    logger.info(f"Getting text effects for mode: {mode}")
    
    all_effects = []
    for effect_name, effect_data in TEXT_EFFECT_MAP.items():
        effect_info = {
            "name": effect_data["name"],
            "is_vip": effect_data.get("is_vip", False),
            "resource_id": effect_data["resource_id"],
            "effect_id": effect_data["effect_id"],
            "icon_url": "",  # 花字元数据中没有 icon_url
        }
        all_effects.append(effect_info)
    
    logger.info(f"Total text effects loaded: {len(all_effects)}")
    
    # 根据模式过滤
    if mode == 0:  # 所有
        result = all_effects
    elif mode == 1:  # VIP
        result = [e for e in all_effects if e.get("is_vip", False)]
    elif mode == 2:  # 免费
        result = [e for e in all_effects if not e.get("is_vip", False)]
    else:
        result = []
    
    logger.info(f"Final filtered result: {len(result)} text effects")
    return result


def resolve_text_effect(effect_identifier: str) -> Optional[Dict[str, Any]]:
    """
    解析花字标识符，返回对应的花字信息
    
    Args:
        effect_identifier: 花字标识符，可以是 effect_id（数字字符串）或花字名称（中文名称）
    
    Returns:
        花字信息字典，包含 resource_id 和 effect_id，如果未找到则返回 None
    """
    logger.info(f"Resolving text effect identifier: {effect_identifier}")
    
    # 1. 首先尝试直接作为 effect_id 查找
    if effect_identifier.isdigit() or effect_identifier in [v["effect_id"] for v in TEXT_EFFECT_MAP.values()]:
        # 直接是 effect_id，返回对应的信息
        for effect_name, effect_data in TEXT_EFFECT_MAP.items():
            if effect_data["effect_id"] == effect_identifier:
                logger.info(f"Found text effect by ID: {effect_identifier}")
                return {
                    "resource_id": effect_data["resource_id"],
                    "effect_id": effect_data["effect_id"]
                }
        # 如果是数字但不在映射表中，也直接返回（可能是新的 effect_id）
        logger.info(f"Using effect_id directly: {effect_identifier}")
        return {
            "resource_id": effect_identifier,
            "effect_id": effect_identifier
        }
    
    # 2. 尝试作为花字名称查找
    if effect_identifier in TEXT_EFFECT_MAP:
        effect_data = TEXT_EFFECT_MAP[effect_identifier]
        logger.info(f"Found text effect by name: {effect_identifier}")
        return {
            "resource_id": effect_data["resource_id"],
            "effect_id": effect_data["effect_id"]
        }
    
    # 3. 未找到匹配项
    logger.warning(f"Text effect not found: {effect_identifier}")
    return None
