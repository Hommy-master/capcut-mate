from pydantic import BaseModel, Field
from typing import List, Optional


class AudioTimelinesRequest(BaseModel):
    """音频时间线请求参数"""
    links: List[str] = Field(..., description="音频文件URL数组")


class TimelineItem(BaseModel):
    """时间线项"""
    start: int = Field(..., description="开始时间（微秒）")
    end: int = Field(..., description="结束时间（微秒）")


class AudioTimelinesResponse(BaseModel):
    """音频时间线响应参数"""
    timelines: List[TimelineItem] = Field(..., description="分割后的时间线列表")
    all_timelines: List[TimelineItem] = Field(..., description="完整的时间线列表")