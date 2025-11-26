"""
获取文字出入场动画的业务逻辑处理模块
"""
import json
from typing import List, Dict, Any
from src.utils.logger import logger
from exceptions import CustomException, CustomError


def get_text_animations(mode: int = 0, type: str = "in") -> List[Dict[str, Any]]:
    """
    获取文字出入场动画列表
    
    Args:
        mode: 动画模式，0=所有，1=VIP，2=免费，默认值为0
        type: 动画类型，in=入场，out=出场，loop=循环，默认值为"in"
    
    Returns:
        effects: 文字出入场动画对象数组
        
    Raises:
        CustomException: 获取文字动画失败
    """
    logger.info(f"get_text_animations called with mode: {mode}, type: {type}")
    
    try:
        # 1. 参数验证
        if type not in ["in", "out", "loop"]:
            logger.error(f"Invalid animation type: {type}")
            raise CustomException(CustomError.TEXT_ANIMATION_GET_FAILED)
        
        if mode not in [0, 1, 2]:
            logger.error(f"Invalid mode: {mode}")
            raise CustomException(CustomError.TEXT_ANIMATION_GET_FAILED)
        
        # 2. 根据类型和模式获取动画数据
        animations = _get_animations_by_type_and_mode(type=type, mode=mode)
        logger.info(f"Found {len(animations)} animations for type: {type}, mode: {mode}")
        
        # 3. 直接返回对象数组（不再转换为JSON字符串）
        logger.info(f"Successfully returned animations array with {len(animations)} items")
        
        return animations
        
    except CustomException:
        logger.error(f"Get text animations failed for type: {type}, mode: {mode}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_text_animations: {str(e)}")
        raise CustomException(CustomError.TEXT_ANIMATION_GET_FAILED)


def _get_animations_by_type_and_mode(type: str, mode: int) -> List[Dict[str, Any]]:
    """
    根据动画类型和模式获取对应的动画数据
    
    Args:
        type: 动画类型（in/out/loop）
        mode: 动画模式（0=所有，1=VIP，2=免费）
    
    Returns:
        包含动画信息的列表
    """
    logger.info(f"Getting animations for type: {type}, mode: {mode}")
    
    # 模拟动画数据库（实际项目中应该从数据库或API获取）
    all_animations = _get_mock_animation_data()
    
    # 1. 根据类型过滤
    filtered_by_type = [anim for anim in all_animations if anim["type"] == type]
    logger.info(f"Filtered by type '{type}': {len(filtered_by_type)} animations")
    
    # 2. 根据模式过滤
    if mode == 0:  # 所有
        result = filtered_by_type
    elif mode == 1:  # VIP
        result = [anim for anim in filtered_by_type if anim.get("is_vip", False)]
    elif mode == 2:  # 免费
        result = [anim for anim in filtered_by_type if not anim.get("is_vip", False)]
    else:
        result = []
    
    logger.info(f"Final filtered result: {len(result)} animations")
    return result


def _get_mock_animation_data() -> List[Dict[str, Any]]:
    """
    获取模拟的动画数据（实际项目中应该从真实数据源获取）
    
    Returns:
        包含所有动画数据的列表
    """
    return [
        # 入场动画
        {
            "resource_id": "7314291622525538843",
            "type": "in",
            "category_id": "ruchang",
            "category_name": "入场",
            "duration": 500000,
            "id": "35395178",
            "name": "冰雪飘动",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/459c196951cadbd024456a63db89481f",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": False
        },
        {
            "resource_id": "7397306443147252233",
            "type": "in",
            "category_id": "ruchang",
            "category_name": "入场",
            "duration": 500000,
            "id": "77035159",
            "name": "变色输入",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/c15f5c313f8170c558043abf300a0692",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": True
        },
        {
            "resource_id": "7298765432109876543",
            "type": "in",
            "category_id": "ruchang",
            "category_name": "入场",
            "duration": 750000,
            "id": "12345678",
            "name": "渐显入场",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/fade_in_icon",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": False
        },
        # 出场动画
        {
            "resource_id": "7314291622525538844",
            "type": "out",
            "category_id": "chuchang",
            "category_name": "出场",
            "duration": 600000,
            "id": "35395179",
            "name": "渐隐出场",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/fade_out_icon",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": False
        },
        {
            "resource_id": "7397306443147252234",
            "type": "out",
            "category_id": "chuchang",
            "category_name": "出场",
            "duration": 800000,
            "id": "77035160",
            "name": "旋转消失",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/rotate_out_icon",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": True
        },
        # 循环动画
        {
            "resource_id": "7314291622525538845",
            "type": "loop",
            "category_id": "xunhuan",
            "category_name": "循环",
            "duration": 1000000,
            "id": "35395180",
            "name": "心跳跳动",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/heartbeat_icon",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": False
        },
        {
            "resource_id": "7397306443147252235",
            "type": "loop",
            "category_id": "xunhuan",
            "category_name": "循环",
            "duration": 1200000,
            "id": "77035161",
            "name": "闪烁效果",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/blink_icon",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": True
        }
    ]