from pydantic import BaseModel, Field
from typing import List


class BeautyItem(BaseModel):
    """单个美颜滑杆"""
    name: str = Field(..., description="美颜名称，支持：美白、磨皮、白牙")
    intensity: float = Field(..., ge=0, le=100, description="强度，0-100，与剪映滑杆一致")


class AddBeautyRequest(BaseModel):
    """添加美颜请求参数"""
    draft_url: str = Field(default="", description="草稿URL")
    segment_ids: List[str] = Field(default=[], description="要应用美颜的视频片段ID数组")
    beauty_infos: List[BeautyItem] = Field(default=[], description="美颜滑杆列表")


class AddBeautyResponse(BaseModel):
    """添加美颜响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    affected_segments: List[str] = Field(default=[], description="成功应用美颜的片段ID列表")
    figure_ids: List[str] = Field(default=[], description="美颜素材ID列表，含 makeup-root")
