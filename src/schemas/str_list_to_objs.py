from pydantic import BaseModel, Field
from typing import List, Optional


class StrListToObjsItem(BaseModel):
    """字符串列表转对象列表项"""
    output: str = Field(..., description="URL地址")


class StrListToObjsRequest(BaseModel):
    """字符串列表转对象列表请求参数"""
    infos: List[str] = Field(..., description="字符串列表")


class StrListToObjsResponse(BaseModel):
    """字符串列表转对象列表响应参数"""
    infos: List[StrListToObjsItem] = Field(..., description="对象列表")