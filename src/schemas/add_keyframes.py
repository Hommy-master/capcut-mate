from pydantic import BaseModel, Field
from typing import List


class AddKeyframesRequest(BaseModel):
    """添加关键帧请求参数"""
    draft_url: str = Field(default="", description="草稿URL")
    keyframes: str = Field(default="", description="关键帧信息列表, 用JSON字符串表示")


class KeyframeItem(BaseModel):
    """单个关键帧信息"""
    segment_id: str = Field(..., description="目标片段的唯一标识ID")
    property: str = Field(..., description="动画属性类型 (KFTypePositionX, KFTypePositionY, KFTypeScaleX, KFTypeScaleY, KFTypeRotation, KFTypeAlpha)")
    offset: float = Field(..., ge=0.0, le=1.0, description="关键帧在片段中的时间偏移 (0-1范围)")
    value: float = Field(..., description="属性在该时间点的值")


class AddKeyframesResponse(BaseModel):
    """添加关键帧响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    keyframes_added: int = Field(default=0, description="添加的关键帧数量")
    affected_segments: List[str] = Field(default=[], description="受影响的片段ID列表")