from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

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