from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any



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