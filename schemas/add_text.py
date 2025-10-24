from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


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