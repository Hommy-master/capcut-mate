"""
获取文字出入场动画的数据模型定义
"""
from typing import Literal, List, Dict, Any
from pydantic import BaseModel, Field


class GetTextAnimationsRequest(BaseModel):
    """获取文字出入场动画的请求模型"""
    mode: int = Field(default=0, description="动画模式：0=所有，1=VIP，2=免费")
    type: Literal["in", "out", "loop"] = Field(..., description="动画类型：in=入场，out=出场，loop=循环")


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
    icon_url: str = Field(..., description="动画图标URL")
    material_type: str = Field(default="sticker", description="素材类型")
    panel: str = Field(default="", description="面板信息")
    path: str = Field(default="", description="路径信息")
    platform: str = Field(default="all", description="支持平台")


class GetTextAnimationsResponse(BaseModel):
    """获取文字出入场动画的响应模型"""
    effects: List[TextAnimationItem] = Field(..., description="文字出入场动画对象数组")
