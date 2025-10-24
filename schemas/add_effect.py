from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


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