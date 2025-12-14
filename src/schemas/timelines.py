from pydantic import BaseModel, Field
from typing import List


class TimelineItem(BaseModel):
    """时间线项"""
    start: int = Field(..., description="开始时间")
    end: int = Field(..., description="结束时间")


class TimelinesRequest(BaseModel):
    """时间线请求参数"""
    duration: int = Field(..., description="总时长")
    num: int = Field(..., description="时间线的个数，值为2即表示将总时长分为2个小段")
    start: int = Field(..., description="开始时间")
    type: int = Field(..., description="0: 平均分，1：随机")


class TimelinesResponse(BaseModel):
    """时间线响应参数"""
    timelines: List[TimelineItem] = Field(..., description="分割后的时间线列表")
    all_timelines: List[TimelineItem] = Field(..., description="完整的时间线列表")