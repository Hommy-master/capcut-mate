from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


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