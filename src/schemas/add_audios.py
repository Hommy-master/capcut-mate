from pydantic import BaseModel, Field
from typing import List


class AddAudiosRequest(BaseModel):
    """批量添加音频请求参数"""
    draft_url: str = Field(..., description="草稿URL")
    audio_infos: str = Field(..., description="音频信息列表, 用JSON字符串表示")


class AddAudiosResponse(BaseModel):
    """添加音频响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    track_id: str = Field(default="", description="音频轨道ID")
    audio_ids: List[str] = Field(default=[], description="音频ID列表")