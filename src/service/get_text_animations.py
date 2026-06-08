"""
获取文字出入场动画的业务逻辑处理模块
"""
from typing import Dict, List, Any, Type
from src.utils.logger import logger
from exceptions import CustomException, CustomError
from src.pyJianYingDraft.metadata import TextIntro, TextOutro, TextLoopAnim
from src.pyJianYingDraft.metadata.effect_meta import EffectEnum, AnimationMeta


_CATEGORY_MAP = {
    "in": ("ruchang", "入场"),
    "out": ("chuchang", "出场"),
    "loop": ("xunhuan", "循环"),
}

_ANIMATION_ENUM_MAP = {
    "in": TextIntro,
    "out": TextOutro,
    "loop": TextLoopAnim,
}


def get_text_animations(mode: int = 0) -> Dict[str, List[Dict[str, Any]]]:
    """
    获取文字出入场动画列表

    Args:
        mode: 动画模式，0=所有，1=VIP，2=免费，默认值为0

    Returns:
        包含 in/out/loop 三类动画的对象

    Raises:
        CustomException: 获取文字动画失败
    """
    logger.info(f"get_text_animations called with mode: {mode}")

    try:
        if mode not in [0, 1, 2]:
            logger.error(f"Invalid mode: {mode}")
            raise CustomException(CustomError.TEXT_ANIMATION_GET_FAILED)

        animations = _get_animations_by_mode(mode=mode)
        total = sum(len(items) for items in animations.values())
        logger.info(
            f"Successfully returned text animations: "
            f"in={len(animations['in'])}, out={len(animations['out'])}, "
            f"loop={len(animations['loop'])}, total={total}"
        )

        return animations

    except CustomException:
        logger.error(f"Get text animations failed for mode: {mode}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_text_animations: {str(e)}")
        raise CustomException(CustomError.TEXT_ANIMATION_GET_FAILED)


def _get_animations_by_mode(mode: int) -> Dict[str, List[Dict[str, Any]]]:
    """
    根据模式获取对应的文字动画数据

    Args:
        mode: 动画模式（0=所有，1=VIP，2=免费）

    Returns:
        按 in/out/loop 分类的动画列表
    """
    logger.info(f"Getting text animations for mode: {mode}")

    result = {}
    for anim_type, enum_cls in _ANIMATION_ENUM_MAP.items():
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
            "is_vip": meta.is_vip,
        })

    return items


def _filter_by_mode(animations: List[Dict[str, Any]], mode: int) -> List[Dict[str, Any]]:
    """根据会员模式过滤动画列表"""
    if mode == 0:
        return animations
    if mode == 1:
        return [anim for anim in animations if anim.get("is_vip", False)]
    if mode == 2:
        return [anim for anim in animations if not anim.get("is_vip", False)]
    return []
