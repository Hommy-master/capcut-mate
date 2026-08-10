from pydantic import BaseModel, Field
from typing import List, Optional


class GetFiltersRequest(BaseModel):
    """获取滤镜列表请求参数"""
    mode: Optional[int] = Field(default=0, ge=0, le=2, description="滤镜模式，0=所有，1=VIP，2=免费，默认值为 0")


class FilterItem(BaseModel):
    """滤镜信息项"""
    name: str = Field(..., description="滤镜名称")
    is_vip: bool = Field(..., description="是否为 VIP 滤镜")
    resource_id: str = Field(..., description="资源 ID")
    effect_id: str = Field(..., description="效果 ID")
    has_params: bool = Field(..., description="是否有额外参数")


class GetFiltersResponse(BaseModel):
    """获取滤镜列表响应参数"""
    filters: List[FilterItem] = Field(..., description="滤镜对象数组")
