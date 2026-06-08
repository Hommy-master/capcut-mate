"""
获取文字出入场动画的数据模型定义
"""
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class GetTextAnimationsRequest(BaseModel):
    """获取文字出入场动画的请求模型"""
    mode: Optional[int] = Field(default=0, description="动画模式：0=所有，1=VIP，2=免费")


class TextAnimationItem(BaseModel):
    """单个文字动画项的数据模型"""
    resource_id: str = Field(..., description="动画资源ID")
    type: str = Field(..., description="动画类型")
    category_id: str = Field(..., description="动画分类ID")
    category_name: str = Field(..., description="动画分类名称")
    duration: int = Field(..., description="动画时长（微秒）")
    id: str = Field(..., description="动画唯一标识ID")
    name: str = Field(..., description="动画名称")
    request_id: str = Field(default="", description="请求ID")
    start: int = Field(default=0, description="动画开始时间")
    icon_url: str = Field(default="", description="动画图标URL")
    material_type: str = Field(default="sticker", description="素材类型")
    panel: str = Field(default="", description="面板信息")
    path: str = Field(default="", description="路径信息")
    platform: str = Field(default="all", description="支持平台")
    is_vip: bool = Field(default=False, description="是否为VIP动画")


class GetTextAnimationsResponse(BaseModel):
    """获取文字出入场动画的响应模型"""
    model_config = ConfigDict(populate_by_name=True)

    in_animations: List[TextAnimationItem] = Field(
        ..., alias="in", description="入场动画列表"
    )
    out_animations: List[TextAnimationItem] = Field(
        ..., alias="out", description="出场动画列表"
    )
    loop_animations: List[TextAnimationItem] = Field(
        ..., alias="loop", description="循环动画列表"
    )
