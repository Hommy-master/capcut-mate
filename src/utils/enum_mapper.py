"""枚举类型映射模块

将字符串名称映射到 pyJianYingDraft 的枚举类型，用于 API 层的参数解析
"""

from typing import Optional, Union
from src.pyJianYingDraft.metadata import (
    MaskType, TransitionType, FilterType, FontType,
    IntroType, OutroType, GroupAnimationType,
    TextIntro, TextOutro, TextLoopAnim,
    AudioSceneEffectType, ToneEffectType, SpeechToSongType,
    VideoSceneEffectType, VideoCharacterEffectType
)
from src.utils.logger import logger


def find_enum_by_name(enum_class, name: str):
    """通用枚举查找函数，根据名称查找枚举成员

    Args:
        enum_class: 枚举类
        name: 枚举成员名称

    Returns:
        枚举成员，如果未找到则返回 None
    """
    if not name:
        return None

    # 尝试直接通过名称访问
    try:
        return enum_class[name]
    except KeyError:
        pass

    # 尝试通过 value.name 查找
    for member in enum_class:
        if hasattr(member.value, 'name') and member.value.name == name:
            return member
        # 也尝试匹配枚举成员名称本身
        if member.name == name:
            return member

    logger.warning(f"未找到枚举类型 {enum_class.__name__} 中的成员: {name}")
    return None


def map_mask_type(mask_name: str) -> Optional[MaskType]:
    """将遮罩名称映射到 MaskType 枚举

    Args:
        mask_name: 遮罩名称，如 "圆形"、"矩形"、"爱心" 等

    Returns:
        MaskType 枚举成员，如果未找到则返回 None
    """
    return find_enum_by_name(MaskType, mask_name)


def map_transition_type(transition_name: str) -> Optional[TransitionType]:
    """将转场名称映射到 TransitionType 枚举

    Args:
        transition_name: 转场名称，如 "淡入淡出"、"闪黑" 等

    Returns:
        TransitionType 枚举成员，如果未找到则返回 None
    """
    return find_enum_by_name(TransitionType, transition_name)


def map_filter_type(filter_name: str) -> Optional[FilterType]:
    """将滤镜名称映射到 FilterType 枚举

    Args:
        filter_name: 滤镜名称

    Returns:
        FilterType 枚举成员，如果未找到则返回 None
    """
    return find_enum_by_name(FilterType, filter_name)


def map_font_type(font_name: str) -> Optional[FontType]:
    """将字体名称映射到 FontType 枚举

    Args:
        font_name: 字体名称

    Returns:
        FontType 枚举成员，如果未找到则返回 None
    """
    return find_enum_by_name(FontType, font_name)


def map_video_intro_type(animation_name: str) -> Optional[IntroType]:
    """将视频入场动画名称映射到 IntroType 枚举

    Args:
        animation_name: 动画名称

    Returns:
        IntroType 枚举成员，如果未找到则返回 None
    """
    return find_enum_by_name(IntroType, animation_name)


def map_video_outro_type(animation_name: str) -> Optional[OutroType]:
    """将视频出场动画名称映射到 OutroType 枚举

    Args:
        animation_name: 动画名称

    Returns:
        OutroType 枚举成员，如果未找到则返回 None
    """
    return find_enum_by_name(OutroType, animation_name)


def map_video_group_animation_type(animation_name: str) -> Optional[GroupAnimationType]:
    """将视频组合动画名称映射到 GroupAnimationType 枚举

    Args:
        animation_name: 动画名称

    Returns:
        GroupAnimationType 枚举成员，如果未找到则返回 None
    """
    return find_enum_by_name(GroupAnimationType, animation_name)


def map_text_intro_type(animation_name: str) -> Optional[TextIntro]:
    """将文本入场动画名称映射到 TextIntro 枚举

    Args:
        animation_name: 动画名称

    Returns:
        TextIntro 枚举成员，如果未找到则返回 None
    """
    return find_enum_by_name(TextIntro, animation_name)


def map_text_outro_type(animation_name: str) -> Optional[TextOutro]:
    """将文本出场动画名称映射到 TextOutro 枚举

    Args:
        animation_name: 动画名称

    Returns:
        TextOutro 枚举成员，如果未找到则返回 None
    """
    return find_enum_by_name(TextOutro, animation_name)


def map_text_loop_animation_type(animation_name: str) -> Optional[TextLoopAnim]:
    """将文本循环动画名称映射到 TextLoopAnim 枚举

    Args:
        animation_name: 动画名称

    Returns:
        TextLoopAnim 枚举成员，如果未找到则返回 None
    """
    return find_enum_by_name(TextLoopAnim, animation_name)


def map_audio_effect_type(effect_name: str) -> Optional[Union[AudioSceneEffectType, ToneEffectType, SpeechToSongType]]:
    """将音频效果名称映射到相应的枚举类型

    Args:
        effect_name: 音效名称

    Returns:
        AudioSceneEffectType、ToneEffectType 或 SpeechToSongType 枚举成员，如果未找到则返回 None
    """
    # 依次尝试三种音频效果类型
    result = find_enum_by_name(AudioSceneEffectType, effect_name)
    if result:
        return result

    result = find_enum_by_name(ToneEffectType, effect_name)
    if result:
        return result

    result = find_enum_by_name(SpeechToSongType, effect_name)
    if result:
        return result

    return None


def map_video_effect_type(effect_name: str) -> Optional[Union[VideoSceneEffectType, VideoCharacterEffectType]]:
    """将视频效果名称映射到相应的枚举类型

    Args:
        effect_name: 特效名称

    Returns:
        VideoSceneEffectType 或 VideoCharacterEffectType 枚举成员，如果未找到则返回 None
    """
    # 依次尝试两种视频效果类型
    result = find_enum_by_name(VideoSceneEffectType, effect_name)
    if result:
        return result

    result = find_enum_by_name(VideoCharacterEffectType, effect_name)
    if result:
        return result

    return None
