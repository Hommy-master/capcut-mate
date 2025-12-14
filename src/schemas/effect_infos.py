from pydantic import BaseModel, Field
from typing import List
from .audio_timelines import TimelineItem


class EffectInfosRequest(BaseModel):
    """特效信息请求参数"""
    effects: List[str] = Field(..., description="特效名称列表")
    timelines: List[TimelineItem] = Field(..., description="时间线数组")


class EffectInfosResponse(BaseModel):
    """特效信息响应参数"""
    infos: str = Field(..., description="JSON字符串格式的特效信息")