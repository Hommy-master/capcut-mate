from pydantic import BaseModel, Field
from typing import List


class AddEffectsRequest(BaseModel):
    """添加特效请求参数"""
    draft_url: str = Field(default="", description="草稿URL")
    effect_infos: str = Field(default="", description="特效信息列表, 用JSON字符串表示")


class EffectItem(BaseModel):
    """单个特效信息"""
    effect_title: str = Field(..., description="特效名称/标题")
    start: int = Field(..., description="特效开始时间（微秒）")
    end: int = Field(..., description="特效结束时间（微秒）")


class AddEffectsResponse(BaseModel):
    """添加特效响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    track_id: str = Field(default="", description="特效轨道ID")
    effect_ids: List[str] = Field(default=[], description="特效ID列表")
    segment_ids: List[str] = Field(default=[], description="特效片段ID列表")