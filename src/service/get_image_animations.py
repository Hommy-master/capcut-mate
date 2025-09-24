"""
获取图片出入场动画的业务逻辑处理模块
"""
import json
from typing import List, Dict, Any
from src.utils.logger import logger
from exceptions import CustomException, CustomError


def get_image_animations(mode: int = 0, type: str = "in") -> str:
    """
    获取图片出入场动画列表
    
    Args:
        mode: 动画模式，0=所有，1=VIP，2=免费，默认值为0
        type: 动画类型，in=入场，out=出场，loop=循环，默认值为"in"
    
    Returns:
        effects: 图片出入场动画数组的JSON字符串
        
    Raises:
        CustomException: 获取图片动画失败
    """
    logger.info(f"get_image_animations called with mode: {mode}, type: {type}")
    
    try:
        # 1. 参数验证
        if type not in ["in", "out", "loop"]:
            logger.error(f"Invalid animation type: {type}")
            raise CustomException(CustomError.IMAGE_ANIMATION_GET_FAILED)
        
        if mode not in [0, 1, 2]:
            logger.error(f"Invalid mode: {mode}")
            raise CustomException(CustomError.IMAGE_ANIMATION_GET_FAILED)
        
        # 2. 根据类型和模式获取动画数据
        animations = _get_animations_by_type_and_mode(type=type, mode=mode)
        logger.info(f"Found {len(animations)} image animations for type: {type}, mode: {mode}")
        
        # 3. 转换为JSON字符串并返回
        effects_json = json.dumps(animations, ensure_ascii=False)
        logger.info(f"Successfully generated image animations JSON with {len(animations)} items")
        
        return effects_json
        
    except CustomException:
        logger.error(f"Get image animations failed for type: {type}, mode: {mode}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_image_animations: {str(e)}")
        raise CustomException(CustomError.IMAGE_ANIMATION_GET_FAILED)


def _get_animations_by_type_and_mode(type: str, mode: int) -> List[Dict[str, Any]]:
    """
    根据动画类型和模式获取对应的图片动画数据
    
    Args:
        type: 动画类型（in/out/loop）
        mode: 动画模式（0=所有，1=VIP，2=免费）
    
    Returns:
        包含图片动画信息的列表
    """
    logger.info(f"Getting image animations for type: {type}, mode: {mode}")
    
    # 模拟图片动画数据库（实际项目中应该从数据库或API获取）
    all_animations = _get_mock_image_animation_data()
    
    # 1. 根据类型过滤
    filtered_by_type = [anim for anim in all_animations if anim["type"] == type]
    logger.info(f"Filtered by type '{type}': {len(filtered_by_type)} image animations")
    
    # 2. 根据模式过滤
    if mode == 0:  # 所有
        result = filtered_by_type
    elif mode == 1:  # VIP
        result = [anim for anim in filtered_by_type if anim.get("is_vip", False)]
    elif mode == 2:  # 免费
        result = [anim for anim in filtered_by_type if not anim.get("is_vip", False)]
    else:
        result = []
    
    logger.info(f"Final filtered image animation result: {len(result)} animations")
    return result


def _get_mock_image_animation_data() -> List[Dict[str, Any]]:
    """
    获取模拟的图片动画数据（实际项目中应该从真实数据源获取）
    
    Returns:
        包含所有图片动画数据的列表
    """
    return [
        # 入场动画
        {
            "resource_id": "7314291622525538844",
            "type": "in",
            "category_id": "pic_ruchang",
            "category_name": "图片入场",
            "duration": 600000,
            "id": "35395179",
            "name": "渐显出现",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/fade_in_pic_icon",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": False
        },
        {
            "resource_id": "7397306443147252234",
            "type": "in",
            "category_id": "pic_ruchang", 
            "category_name": "图片入场",
            "duration": 800000,
            "id": "77035160",
            "name": "缩放入场",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/scale_in_pic_icon",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": True
        },
        {
            "resource_id": "7298765432109876544",
            "type": "in",
            "category_id": "pic_ruchang",
            "category_name": "图片入场", 
            "duration": 700000,
            "id": "12345679",
            "name": "飞入效果",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/fly_in_pic_icon",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": False
        },
        {
            "resource_id": "7456789012345678901",
            "type": "in",
            "category_id": "pic_ruchang",
            "category_name": "图片入场",
            "duration": 900000,
            "id": "98765432",
            "name": "光影浮现",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/light_emerge_pic_icon",
            "material_type": "sticker", 
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": True
        },
        # 出场动画
        {
            "resource_id": "7314291622525538845",
            "type": "out",
            "category_id": "pic_chuchang",
            "category_name": "图片出场",
            "duration": 650000,
            "id": "35395180",
            "name": "渐隐消失",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/fade_out_pic_icon",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": False
        },
        {
            "resource_id": "7397306443147252235",
            "type": "out",
            "category_id": "pic_chuchang",
            "category_name": "图片出场",
            "duration": 750000,
            "id": "77035161",
            "name": "翻转消失",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/flip_out_pic_icon",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": True
        },
        {
            "resource_id": "7123456789012345678",
            "type": "out",
            "category_id": "pic_chuchang",
            "category_name": "图片出场",
            "duration": 550000,
            "id": "11223344",
            "name": "碎片散落",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/shatter_out_pic_icon",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": False
        },
        # 循环动画
        {
            "resource_id": "7314291622525538846",
            "type": "loop",
            "category_id": "pic_xunhuan", 
            "category_name": "图片循环",
            "duration": 1200000,
            "id": "35395181",
            "name": "轻微摆动",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/sway_pic_icon",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": False
        },
        {
            "resource_id": "7397306443147252236",
            "type": "loop",
            "category_id": "pic_xunhuan",
            "category_name": "图片循环",
            "duration": 1500000,
            "id": "77035162",
            "name": "呼吸缩放",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/breath_scale_pic_icon",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": True
        },
        {
            "resource_id": "7987654321098765432",
            "type": "loop",
            "category_id": "pic_xunhuan",
            "category_name": "图片循环",
            "duration": 1000000,
            "id": "55667788",
            "name": "光晕流转",
            "request_id": "",
            "start": 0,
            "icon_url": "https://lf5-hl-hw-effectcdn-tos.byteeffecttos.com/obj/ies.fe.effect/halo_flow_pic_icon",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "is_vip": False
        }
    ]