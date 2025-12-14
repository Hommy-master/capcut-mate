from pydantic import BaseModel, Field
from typing import List, Optional


class ObjItem(BaseModel):
    """对象项"""
    output: str = Field(..., description="URL地址")


class ObjsToStrListRequest(BaseModel):
    """对象列表转化成字符串列表请求参数"""
    outputs: List[ObjItem] = Field(..., description="数据对象")


class ObjsToStrListResponse(BaseModel):
    """对象列表转化成字符串列表响应参数"""
    infos: List[str] = Field(..., description="字符串列表")