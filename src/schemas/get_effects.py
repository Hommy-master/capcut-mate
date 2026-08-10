from pydantic import BaseModel, Field
from typing import List, Optional


class GetEffectsRequest(BaseModel):
    """获取特效列表请求参数"""
    mode: Optional[int] = Field(default=0, ge=0, le=2, description="特效模式，0=所有，1=VIP，2=免费，默认值为 0")


class EffectItem(BaseModel):
    """特效信息项"""
    name: str = Field(..., description="特效名称")
    is_vip: bool = Field(..., description="是否为 VIP 特效")
    resource_id: str = Field(..., description="资源 ID")
    effect_id: str = Field(..., description="效果 ID")
    icon_url: str = Field(..., description="图标 URL")
    has_params: bool = Field(..., description="是否有额外参数")


class GetEffectsResponse(BaseModel):
    """获取特效列表响应参数"""
    effects: List[EffectItem] = Field(..., description="特效对象数组")
