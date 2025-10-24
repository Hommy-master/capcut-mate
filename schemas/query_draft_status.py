from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class QueryDraftStatusRequest(BaseModel):
    task_id: str = Field(..., description="任务 ID（必需）")
