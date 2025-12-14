from pydantic import BaseModel, Field
from typing import List, Optional, Any
from .audio_timelines import TimelineItem


class AudioInfosRequest(BaseModel):
    """音频信息请求参数"""
    mp3_urls: List[str] = Field(..., description="音频文件URL数组")
    timelines: List[TimelineItem] = Field(..., description="时间线数组")
    audio_effect: Optional[str] = Field(None, description="音频效果")
    volume: Optional[float] = Field(None, description="音量")


class AudioInfosResponse(BaseModel):
    """音频信息响应参数"""
    infos: str = Field(..., description="JSON字符串格式的音频信息")