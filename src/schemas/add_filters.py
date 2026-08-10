from pydantic import BaseModel, Field
from typing import List


class AddFiltersRequest(BaseModel):
    """添加滤镜请求参数"""
    draft_url: str = Field(default="", description="草稿URL")
    filter_infos: str = Field(default="", description="滤镜信息列表, 用JSON字符串表示")


class FilterItem(BaseModel):
    """单个滤镜信息"""
    filter_title: str = Field(..., description="滤镜名称/标题")
    start: int = Field(..., description="滤镜开始时间（微秒）")
    end: int = Field(..., description="滤镜结束时间（微秒）")
    intensity: float = Field(default=100.0, ge=0, le=100, description="滤镜强度(0-100)")


class AddFiltersResponse(BaseModel):
    """添加滤镜响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    track_id: str = Field(default="", description="滤镜轨道ID")
    filter_ids: List[str] = Field(default=[], description="滤镜ID列表")
    segment_ids: List[str] = Field(default=[], description="滤镜片段ID列表")
