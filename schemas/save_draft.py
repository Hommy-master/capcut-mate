from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class SaveDraftRequest(BaseModel):
    draft_id: str = Field(..., description="草稿 ID（必需）")
    draft_folder: Optional[str] = None
