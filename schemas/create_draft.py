from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class CreateDraftRequest(BaseModel):
    width: int = 1080
    height: int = 1920