from pydantic import BaseModel, Field
from typing import List, Optional
from .audio_timelines import TimelineItem


class VideoInfosRequest(BaseModel):
    """视频信息请求参数"""
    video_urls: List[str] = Field(..., description="视频列表")
    timelines: List[TimelineItem] = Field(..., description="时间线数组")
    height: Optional[int] = Field(None, description="视频高")
    width: Optional[int] = Field(None, description="视频宽")
    mask: Optional[str] = Field(None, description="视频蒙版，可填写值：圆形，矩形，爱心，星形")
    transition: Optional[str] = Field(None, description="转场名称")
    transition_duration: Optional[int] = Field(None, description="转场时长，整数")
    volume: Optional[float] = Field(1.0, description="float类型，音量大小，0-10,默认1")


class VideoInfosResponse(BaseModel):
    """视频信息响应参数"""
    infos: str = Field(..., description="JSON字符串格式的视频信息")