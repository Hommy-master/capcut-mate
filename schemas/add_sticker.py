from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


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
