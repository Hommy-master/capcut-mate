from pydantic import BaseModel, Field
from typing import List


class BeautyItem(BaseModel):
    """单个美颜滑杆。intensity 默认 0，与剪映滑杆 0-100 一致。"""
    name: str = Field(..., description="美颜名称：匀肤、丰盈、磨皮、祛法令纹、亮眼、祛黑眼圈、美白、白牙、肤色/暖白")
    intensity: float = Field(default=0, ge=0, le=100, description="强度，0-100，与剪映滑杆一致")


class AddBeautyRequest(BaseModel):
    """添加美颜请求参数。10 个美颜参数均有默认值，非 0 / 非空时才会写入。"""
    draft_url: str = Field(default="", description="草稿URL")
    segment_ids: List[str] = Field(default=[], description="要应用美颜的视频片段ID数组")
    beauty_infos: List[BeautyItem] = Field(default=[], description="美颜滑杆列表，可与下方具名参数同时使用")
    匀肤: float = Field(default=0, ge=0, le=100, description="匀肤强度（0-100）")
    丰盈: float = Field(default=0, ge=0, le=100, description="丰盈强度（0-100）")
    磨皮: float = Field(default=0, ge=0, le=100, description="磨皮强度（0-100）")
    祛法令纹: float = Field(default=0, ge=0, le=100, description="祛法令纹强度（0-100）")
    亮眼: float = Field(default=0, ge=0, le=100, description="亮眼强度（0-100）")
    祛黑眼圈: float = Field(default=0, ge=0, le=100, description="祛黑眼圈强度（0-100）")
    美白: float = Field(default=0, ge=0, le=100, description="美白强度（0-100）")
    白牙: float = Field(default=0, ge=0, le=100, description="白牙强度（0-100）")
    肤色: str = Field(default="", description="肤色预设，空字符串表示不应用；当前支持暖白")
    肤色强度: float = Field(default=60, ge=0, le=100, description="肤色强度（0-100），仅在设置肤色时生效")


class AddBeautyResponse(BaseModel):
    """添加美颜响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    affected_segments: List[str] = Field(default=[], description="成功应用美颜的片段ID列表")
    figure_ids: List[str] = Field(default=[], description="美颜素材ID列表，含 makeup-root")
