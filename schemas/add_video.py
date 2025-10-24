from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


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