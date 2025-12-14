from pydantic import BaseModel, Field
from typing import List


class StrToListRequest(BaseModel):
    """字符转列表请求参数"""
    obj: str = Field(..., description="对象内容")


class StrToListResponse(BaseModel):
    """字符转列表响应参数"""
    infos: List[str] = Field(..., description="字符串列表")