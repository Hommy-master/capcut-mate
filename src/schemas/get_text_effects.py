from pydantic import BaseModel, Field
from typing import List, Optional


class GetTextEffectsRequest(BaseModel):
    """获取花字效果列表请求参数"""
    mode: Optional[int] = Field(default=0, ge=0, le=2, description="花字效果模式，0=所有，1=VIP，2=免费，默认值为 0")


class TextEffectItem(BaseModel):
    """花字效果信息项"""
    name: str = Field(..., description="花字效果名称")
    is_vip: bool = Field(..., description="是否为 VIP 效果")
    resource_id: str = Field(..., description="资源 ID")
    effect_id: str = Field(..., description="效果 ID")


class GetTextEffectsResponse(BaseModel):
    """获取花字效果列表响应参数"""
    text_effects: List[TextEffectItem] = Field(..., description="花字效果对象数组")
