"""记录各种特效/音效/滤镜等的元数据"""

from .effect_meta import Effect_meta, Effect_param_instance

from .font_meta import Font_type
from .mask_meta import Mask_type, Mask_meta
from .capcut_mask_meta import CapCut_Mask_type
from .filter_meta import Filter_type
from .transition_meta import Transition_type
from .capcut_transition_meta import CapCut_Transition_type
from .animation_meta import Intro_type, Outro_type, Group_animation_type
from .capcut_animation_meta import CapCut_Intro_type, CapCut_Outro_type, CapCut_Group_animation_type
from .animation_meta import Text_intro, Text_outro, Text_loop_anim
from .capcut_text_animation_meta import CapCut_Text_intro, CapCut_Text_outro, CapCut_Text_loop_anim
from .audio_effect_meta import Audio_scene_effect_type, Tone_effect_type, Speech_to_song_type
from .capcut_audio_effect_meta import CapCut_Voice_filters_effect_type, CapCut_Voice_characters_effect_type, CapCut_Speech_to_song_effect_type
from .video_effect_meta import Video_scene_effect_type, Video_character_effect_type
from .capcut_effect_meta import CapCut_Video_scene_effect_type, CapCut_Video_character_effect_type

__all__ = [
    "Effect_meta",
    "Effect_param_instance",
    "Mask_type",
    "Mask_meta",
    "CapCut_Mask_type",
    "Filter_type",
    "Font_type",
    "Transition_type",
    "CapCut_Transition_type",
    "Intro_type",
    "Outro_type",
    "Group_animation_type",
    "CapCut_Intro_type",
    "CapCut_Outro_type",
    "CapCut_Group_animation_type",
    "Text_intro",
    "Text_outro",
    "Text_loop_anim",
    "CapCut_Text_intro",
    "CapCut_Text_outro",
    "CapCut_Text_loop_anim",
    "Audio_scene_effect_type",
    "Tone_effect_type",
    "Speech_to_song_type",
    "CapCut_Voice_filters_effect_type",
    "CapCut_Voice_characters_effect_type",
    "CapCut_Speech_to_song_effect_type",
    "Video_scene_effect_type",
    "Video_character_effect_type",
    "CapCut_Video_scene_effect_type",
    "CapCut_Video_character_effect_type"
]
