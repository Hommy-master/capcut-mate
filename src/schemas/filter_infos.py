from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from .audio_timelines import TimelineItem


class FilterInfosRequest(BaseModel):
    """滤镜信息请求参数"""
    filters: List[str] = Field(..., description="滤镜名称列表")
    timelines: List[TimelineItem] = Field(..., description="时间线数组")
    intensities: Optional[List[float]] = Field(default=None, description="滤镜强度列表(0-100)，可选")
    
    @field_validator('intensities', mode='before')
    @classmethod
    def validate_intensities(cls, v):
        """验证并限制 intensities 数组中的每个值在 0-100 范围内"""
        if v is None:
            return v
        return [max(0, min(100, val)) for val in v]


class FilterInfosResponse(BaseModel):
    """滤镜信息响应参数"""
    infos: str = Field(..., description="JSON字符串格式的滤镜信息")
