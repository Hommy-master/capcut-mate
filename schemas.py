from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# ==================== 请求模型定义 ====================

class AddVideoRequest(BaseModel):
    video_url: str = Field(..., description="视频 URL（必需）")
    draft_folder: Optional[str] = None
    draft_id: Optional[str] = None
    start: float = 0
    end: float = 0
    width: int = 1080
    height: int = 1920
    transform_y: float = 0
    scale_x: float = 1
    scale_y: float = 1
    transform_x: float = 0
    speed: float = 1.0
    target_start: float = 0
    track_name: str = "video_main"
    relative_index: int = 0
    duration: Optional[float] = None
    transition: Optional[str] = None
    transition_duration: float = 0.5
    volume: float = 1.0
    mask_type: Optional[str] = None
    mask_center_x: float = 0.5
    mask_center_y: float = 0.5
    mask_size: float = 1.0
    mask_rotation: float = 0.0
    mask_feather: float = 0.0
    mask_invert: bool = False
    mask_rect_width: Optional[float] = None
    mask_round_corner: Optional[float] = None
    background_blur: Optional[int] = None

class AddAudioRequest(BaseModel):
    audio_url: str = Field(..., description="音频 URL（必需）")
    draft_folder: Optional[str] = None
    draft_id: Optional[str] = None
    start: float = 0
    end: Optional[float] = None
    volume: float = 1.0
    target_start: float = 0
    speed: float = 1.0
    track_name: str = "audio_main"
    duration: Optional[float] = None
    effect_type: Optional[str] = None
    effect_params: Optional[List[Any]] = None
    width: int = 1080
    height: int = 1920

class CreateDraftRequest(BaseModel):
    width: int = 1080
    height: int = 1920

class AddSubtitleRequest(BaseModel):
    srt: str = Field(..., description="字幕内容或 URL（必需）")
    draft_id: Optional[str] = None
    time_offset: float = 0.0
    font: str = "思源粗宋"
    font_size: float = 5.0
    bold: bool = False
    italic: bool = False
    underline: bool = False
    font_color: str = "#FFFFFF"
    vertical: bool = False
    alpha: float = 1.0
    border_alpha: float = 1.0
    border_color: str = "#000000"
    border_width: float = 0.0
    background_color: str = "#000000"
    background_style: int = 0
    background_alpha: float = 0.0
    transform_x: float = 0.0
    transform_y: float = -0.8
    scale_x: float = 1.0
    scale_y: float = 1.0
    rotation: float = 0.0
    track_name: str = "subtitle"
    width: int = 1080
    height: int = 1920

class TextStyleData(BaseModel):
    start: int = 0
    end: int = 0
    font: Optional[str] = None
    style: Optional[Dict[str, Any]] = None
    border: Optional[Dict[str, Any]] = None

class AddTextRequest(BaseModel):
    text: str = Field(..., description="文字内容（必需）")
    start: float = Field(..., description="开始时间（必需）")
    end: float = Field(..., description="结束时间（必需）")
    draft_id: Optional[str] = None
    transform_y: float = 0
    transform_x: float = 0
    font: str = "文轩体"
    color: Optional[str] = None
    font_color: str = "#FF0000"
    size: Optional[float] = None
    font_size: float = 8.0
    track_name: str = "text_main"
    vertical: bool = False
    alpha: Optional[float] = None
    font_alpha: float = 1.0
    width: int = 1080
    height: int = 1920
    fixed_width: float = -1
    fixed_height: float = -1
    border_alpha: float = 1.0
    border_color: str = "#000000"
    border_width: float = 0.0
    background_color: str = "#000000"
    background_style: int = 0
    background_alpha: float = 0.0
    background_round_radius: float = 0.0
    background_height: float = 0.14
    background_width: float = 0.14
    background_horizontal_offset: float = 0.5
    background_vertical_offset: float = 0.5
    shadow_enabled: bool = False
    shadow_alpha: float = 0.9
    shadow_angle: float = -45.0
    shadow_color: str = "#000000"
    shadow_distance: float = 5.0
    shadow_smoothing: float = 0.15
    bubble_effect_id: Optional[str] = None
    bubble_resource_id: Optional[str] = None
    effect_effect_id: Optional[str] = None
    intro_animation: Optional[str] = None
    intro_duration: float = 0.5
    outro_animation: Optional[str] = None
    outro_duration: float = 0.5
    text_styles: List[TextStyleData] = []

class AddImageRequest(BaseModel):
    image_url: str = Field(..., description="图片 URL（必需）")
    draft_folder: Optional[str] = None
    draft_id: Optional[str] = None
    width: int = 1080
    height: int = 1920
    start: float = 0
    end: float = 3.0
    transform_y: float = 0
    scale_x: float = 1
    scale_y: float = 1
    transform_x: float = 0
    track_name: str = "image_main"
    relative_index: int = 0
    animation: Optional[str] = None
    animation_duration: float = 0.5
    intro_animation: Optional[str] = None
    intro_animation_duration: float = 0.5
    outro_animation: Optional[str] = None
    outro_animation_duration: float = 0.5
    combo_animation: Optional[str] = None
    combo_animation_duration: float = 0.5
    transition: Optional[str] = None
    transition_duration: float = 0.5
    mask_type: Optional[str] = None
    mask_center_x: float = 0.0
    mask_center_y: float = 0.0
    mask_size: float = 0.5
    mask_rotation: float = 0.0
    mask_feather: float = 0.0
    mask_invert: bool = False
    mask_rect_width: Optional[float] = None
    mask_round_corner: Optional[float] = None
    background_blur: Optional[int] = None

class AddVideoKeyframeRequest(BaseModel):
    draft_id: Optional[str] = None
    track_name: str = "video_main"
    property_type: str = "alpha"
    time: float = 0.0
    value: str = "1.0"
    property_types: Optional[List[str]] = None
    times: Optional[List[float]] = None
    values: Optional[List[str]] = None

class AddEffectRequest(BaseModel):
    effect_type: str = Field(..., description="特效类型（必需）")
    start: float = 0
    end: float = 3.0
    effect_category: str = "scene"
    draft_id: Optional[str] = None
    track_name: str = "effect_01"
    params: Optional[List[Any]] = None
    width: int = 1080
    height: int = 1920

class QueryScriptRequest(BaseModel):
    draft_id: str = Field(..., description="草稿 ID（必需）")
    force_update: bool = True

class SaveDraftRequest(BaseModel):
    draft_id: str = Field(..., description="草稿 ID（必需）")
    draft_folder: Optional[str] = None

class QueryDraftStatusRequest(BaseModel):
    task_id: str = Field(..., description="任务 ID（必需）")

class GenerateDraftURLRequest(BaseModel):
    draft_id: str = Field(..., description="草稿 ID（必需）")
    draft_folder: Optional[str] = None

class AddStickerRequest(BaseModel):
    sticker_id: str = Field(..., description="贴纸 ID（必需）")
    start: float = 0
    end: float = 5.0
    draft_id: Optional[str] = None
    transform_y: float = 0
    transform_x: float = 0
    alpha: float = 1.0
    flip_horizontal: bool = False
    flip_vertical: bool = False
    rotation: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    track_name: str = "sticker_main"
    relative_index: int = 0
    width: int = 1080
    height: int = 1920
