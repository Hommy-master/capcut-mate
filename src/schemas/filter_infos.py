from pydantic import BaseModel, Field
from typing import List, Optional
from .audio_timelines import TimelineItem


class FilterInfosRequest(BaseModel):
    """滤镜信息请求参数"""
    filters: List[str] = Field(..., description="滤镜名称列表")
    timelines: List[TimelineItem] = Field(..., description="时间线数组")
    intensities: Optional[List[float]] = Field(default=None, ge=0, le=100, description="滤镜强度列表(0-100)，可选")


class FilterInfosResponse(BaseModel):
    """滤镜信息响应参数"""
    infos: str = Field(..., description="JSON字符串格式的滤镜信息")
