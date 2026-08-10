"""
获取滤镜列表的业务逻辑处理模块
"""
import json
from typing import List, Dict, Any
from src.utils.logger import logger
from exceptions import CustomException, CustomError


def get_filters(mode: int = 0) -> List[Dict[str, Any]]:
    """
    获取滤镜列表
    
    Args:
        mode: 滤镜模式，0=所有，1=VIP，2=免费，默认值为 0
    
    Returns:
        filters: 滤镜对象数组
        
    Raises:
        CustomException: 获取滤镜列表失败
    """
    logger.info(f"get_filters called with mode: {mode}")
    
    try:
        # 1. 参数验证
        if mode not in [0, 1, 2]:
            logger.error(f"Invalid mode: {mode}")
            raise CustomException(CustomError.FILTER_GET_FAILED)
        
        # 2. 根据模式获取滤镜数据
        filters = _get_filters_by_mode(mode=mode)
        logger.info(f"Found {len(filters)} filters for mode: {mode}")
        
        # 3. 直接返回对象数组
        logger.info(f"Successfully returned filters array with {len(filters)} items")
        
        return filters
        
    except CustomException:
        logger.error(f"Get filters failed for mode: {mode}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_filters: {str(e)}")
        raise CustomException(CustomError.FILTER_GET_FAILED)


def _get_filters_by_mode(mode: int) -> List[Dict[str, Any]]:
    """
    根据模式获取对应的滤镜数据
    
    Args:
        mode: 滤镜模式（0=所有，1=VIP，2=免费）
    
    Returns:
        包含滤镜信息的列表
    """
    logger.info(f"Getting filters for mode: {mode}")
    
    # 从 FilterType 枚举中获取所有滤镜
    from src.pyJianYingDraft.metadata.filter_meta import FilterType
    
    all_filters = []
    for filter_type in FilterType:
        filter_info = {
            "name": filter_type.value.name,
            "is_vip": filter_type.value.is_vip,
            "resource_id": filter_type.value.resource_id,
            "effect_id": filter_type.value.effect_id,
            "has_params": len(filter_type.value.params) > 0
        }
        all_filters.append(filter_info)
    
    logger.info(f"Total filters loaded: {len(all_filters)}")
    
    # 根据模式过滤
    if mode == 0:  # 所有
        result = all_filters
    elif mode == 1:  # VIP
        result = [f for f in all_filters if f.get("is_vip", False)]
    elif mode == 2:  # 免费
        result = [f for f in all_filters if not f.get("is_vip", False)]
    else:
        result = []
    
    logger.info(f"Final filtered result: {len(result)} filters")
    return result
