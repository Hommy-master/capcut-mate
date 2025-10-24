from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class QueryScriptRequest(BaseModel):
    draft_id: str = Field(..., description="草稿 ID（必需）")
    force_update: bool = True