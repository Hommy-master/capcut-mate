from pydantic import BaseModel, Field
from typing import List, Optional
from .audio_timelines import TimelineItem


class CaptionInfosRequest(BaseModel):
    """字幕信息请求参数"""
    texts: List[str] = Field(..., description="文本列表")
    timelines: List[TimelineItem] = Field(..., description="时间线数组")
    font_size: Optional[int] = Field(None, description="字体大小")
    keyword_color: Optional[str] = Field(None, description="关键词颜色")
    keyword_font_size: Optional[int] = Field(None, description="关键词字体大小")
    keywords: Optional[List[str]] = Field(None, description="文本里面的重点词列表")
    in_animation: Optional[str] = Field(None, description="入场动画名称")
    in_animation_duration: Optional[int] = Field(None, description="入场动画时长")
    loop_animation: Optional[str] = Field(None, description="组合动画名称")
    loop_animation_duration: Optional[int] = Field(None, description="组合动画时长")
    out_animation: Optional[str] = Field(None, description="出场动画名称")
    out_animation_duration: Optional[int] = Field(None, description="出场动画时长")
    transition: Optional[str] = Field(None, description="转场名称")
    transition_duration: Optional[int] = Field(None, description="转场时长")


class CaptionInfosResponse(BaseModel):
    """字幕信息响应参数"""
    infos: str = Field(..., description="JSON字符串格式的字幕信息")