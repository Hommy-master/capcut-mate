from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class AddVideoKeyframeRequest(BaseModel):
    draft_id: Optional[str] = None
    track_name: str = "video_main"
    property_type: str = "alpha"
    time: float = 0.0
    value: str = "1.0"
    property_types: Optional[List[str]] = None
    times: Optional[List[float]] = None
    values: Optional[List[str]] = None
