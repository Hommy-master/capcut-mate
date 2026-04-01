"""
获取花字效果列表和解析花字效果标识符的业务逻辑处理模块
"""
import json
from typing import List, Dict, Any, Optional
from src.utils.logger import logger
from exceptions import CustomException, CustomError
from config import HUAZI_CONFIG_PATH


# 进程启动时加载花字数据到内存
_HUAZI_DATA: List[Dict[str, Any]] = []
_HUAZI_MAP_BY_NAME: Dict[str, Dict[str, Any]] = {}
_HUAZI_MAP_BY_ID: Dict[str, Dict[str, Any]] = {}


def _load_huazi_data() -> None:
    """在进程启动时加载花字数据到内存"""
    global _HUAZI_DATA, _HUAZI_MAP_BY_NAME, _HUAZI_MAP_BY_ID
    
    try:
        with open(HUAZI_CONFIG_PATH, "r", encoding="utf-8") as f:
            _HUAZI_DATA = json.load(f)
        
        # 构建映射表以便快速查找
        for item in _HUAZI_DATA:
            title = item.get("title", "")
            resource_id = item.get("id", "")
            
            # 标准化花字数据格式（匹配接口返回格式）
            effect_data = {
                "id": resource_id,
                "title": title,
                "is_vip": item.get("is_vip", False)
            }
            
            if title:
                _HUAZI_MAP_BY_NAME[title] = effect_data
            if resource_id:
                _HUAZI_MAP_BY_ID[resource_id] = effect_data
        
        logger.info(f"成功加载 {len(_HUAZI_DATA)} 个花字效果到内存")
        
    except Exception as e:
        logger.error(f"加载花字数据失败: {str(e)}")
        _HUAZI_DATA = []
        _HUAZI_MAP_BY_NAME = {}
        _HUAZI_MAP_BY_ID = {}


# 模块导入时自动加载数据
_load_huazi_data()


def resolve_text_effect(effect_identifier: str) -> Optional[Dict[str, Any]]:
    """
    解析花字效果标识符，返回对应的效果信息
    
    Args:
        effect_identifier: 可以是 effect_id（数字字符串）或效果名称（中文名称）
    
    Returns:
        花字效果信息字典，包含 id 和 title，如果未找到则返回 None
    """
    logger.debug(f"Resolving text effect: {effect_identifier}")
    
    # 1. 尝试作为 id 查找
    if effect_identifier in _HUAZI_MAP_BY_ID:
        effect_data = _HUAZI_MAP_BY_ID[effect_identifier]
        return {
            "id": effect_data["id"],
            "title": effect_data["title"]
        }
    
    # 2. 尝试作为中文名称查找
    if effect_identifier in _HUAZI_MAP_BY_NAME:
        effect_data = _HUAZI_MAP_BY_NAME[effect_identifier]
        return {
            "id": effect_data["id"],
            "title": effect_data["title"]
        }
    
    # 3. 如果是纯数字但不在映射表中，直接使用（可能是新的 effect_id）
    if effect_identifier.isdigit():
        return {
            "id": effect_identifier,
            "title": effect_identifier
        }
    
    # 4. 未找到
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
    
    # 从内存中直接获取所有花字效果
    all_text_effects = list(_HUAZI_MAP_BY_NAME.values())
    
    logger.info(f"Total text effects loaded from memory: {len(all_text_effects)}")
    
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
