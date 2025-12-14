from pydantic import BaseModel, Field
from typing import List, Optional
from .audio_timelines import TimelineItem


class ImgsInfosRequest(BaseModel):
    """图片信息请求参数"""
    imgs: List[str] = Field(..., description="图片URL列表")
    timelines: List[TimelineItem] = Field(..., description="时间线数组")
    height: Optional[int] = Field(None, description="视频高度")
    width: Optional[int] = Field(None, description="视频宽度")
    in_animation: Optional[str] = Field(None, description="入场动画名称")
    in_animation_duration: Optional[int] = Field(None, description="入场动画时长")
    loop_animation: Optional[str] = Field(None, description="组合动画名称")
    loop_animation_duration: Optional[int] = Field(None, description="组合动画时长")
    out_animation: Optional[str] = Field(None, description="出场动画名称")
    out_animation_duration: Optional[int] = Field(None, description="出场动画时长")
    transition: Optional[str] = Field(None, description="转场名称")
    transition_duration: Optional[int] = Field(None, description="转场时长")


class ImgsInfosResponse(BaseModel):
    """图片信息响应参数"""
    infos: str = Field(..., description="JSON字符串格式的图片信息")