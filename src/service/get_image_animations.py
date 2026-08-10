"""
获取图片出入场动画的业务逻辑处理模块
"""
from typing import Dict, List, Any, Type, Optional
from src.utils.logger import logger
from exceptions import CustomException, CustomError
from src.pyJianYingDraft.metadata import IntroType, OutroType, GroupAnimationType
from src.pyJianYingDraft.metadata.effect_meta import EffectEnum, AnimationMeta


_CATEGORY_MAP = {
    "in": ("pic_ruchang", "图片入场"),
    "out": ("pic_chuchang", "图片出场"),
    "loop": ("pic_xunhuan", "图片循环"),
}

_ANIMATION_ENUM_MAP = {
    "in": IntroType,
    "out": OutroType,
    "loop": GroupAnimationType,
}


def get_image_animations(
    mode: int = 0, type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    获取图片出入场动画列表

    Args:
        mode: 动画模式，0=所有，1=VIP，2=免费，默认值为0
        type: 动画类型，in/out/loop；不传则返回全部

    Returns:
        effects: 图片出入场动画对象数组

    Raises:
        CustomException: 获取图片动画失败
    """
    logger.info(f"get_image_animations called with mode: {mode}, type: {type}")

    try:
        if type is not None and type not in _ANIMATION_ENUM_MAP:
            logger.error(f"Invalid animation type: {type}")
            raise CustomException(CustomError.IMAGE_ANIMATION_GET_FAILED)

        if mode not in [0, 1, 2]:
            logger.error(f"Invalid mode: {mode}")
            raise CustomException(CustomError.IMAGE_ANIMATION_GET_FAILED)

        grouped = _get_animations_by_mode(mode=mode, type=type)
        effects = _flatten_animations(grouped)
        logger.info(
            f"Successfully returned image animations: "
            f"in={len(grouped['in'])}, out={len(grouped['out'])}, "
            f"loop={len(grouped['loop'])}, total={len(effects)}"
        )

        return effects

    except CustomException:
        logger.error(f"Get image animations failed for mode: {mode}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_image_animations: {str(e)}")
        raise CustomException(CustomError.IMAGE_ANIMATION_GET_FAILED)


def _get_animations_by_mode(
    mode: int, type: Optional[str] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """
    根据模式和类型获取对应的图片动画数据

    Args:
        mode: 动画模式（0=所有，1=VIP，2=免费）
        type: 动画类型（in/out/loop），不传则返回全部

    Returns:
        按 in/out/loop 分类的动画列表
    """
    logger.info(f"Getting image animations for mode: {mode}, type: {type}")

    types_to_load = [type] if type else list(_ANIMATION_ENUM_MAP.keys())
    result = {anim_type: [] for anim_type in _ANIMATION_ENUM_MAP}

    for anim_type in types_to_load:
        enum_cls = _ANIMATION_ENUM_MAP[anim_type]
        all_items = _load_animations_from_enum(enum_cls, anim_type)
        result[anim_type] = _filter_by_mode(all_items, mode)
        logger.info(f"Filtered '{anim_type}' animations: {len(result[anim_type])}")

    return result


def _load_animations_from_enum(
    enum_cls: Type[EffectEnum], anim_type: str
) -> List[Dict[str, Any]]:
    """从枚举元数据加载动画列表"""
    category_id, category_name = _CATEGORY_MAP[anim_type]
    items = []

    for anim in enum_cls:
        meta: AnimationMeta = anim.value
        items.append({
            "resource_id": meta.resource_id,
            "type": anim_type,
            "category_id": category_id,
            "category_name": category_name,
            "duration": meta.duration,
            "id": meta.effect_id,
            "name": meta.title,
            "request_id": "",
            "start": 0,
            "icon_url": "",
            "material_type": "sticker",
            "panel": "",
            "path": "",
            "platform": "all",
            "_is_vip": meta.is_vip,
        })

    return items


def _flatten_animations(
    grouped: Dict[str, List[Dict[str, Any]]]
) -> List[Dict[str, Any]]:
    """将分类动画合并为 effects 数组"""
    effects = []
    for anim_type in _ANIMATION_ENUM_MAP:
        for item in grouped.get(anim_type, []):
            effects.append({k: v for k, v in item.items() if k != "_is_vip"})
    return effects


def _filter_by_mode(animations: List[Dict[str, Any]], mode: int) -> List[Dict[str, Any]]:
    """根据会员模式过滤动画列表"""
    if mode == 0:
        return animations
    if mode == 1:
        return [anim for anim in animations if anim.get("_is_vip", False)]
    if mode == 2:
        return [anim for anim in animations if not anim.get("_is_vip", False)]
    return []
