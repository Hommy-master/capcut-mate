from pydantic import BaseModel, Field
from typing import List

class AddStickerRequest(BaseModel):
    """添加贴纸请求参数"""
    draft_url: str = Field(..., description="草稿URL")
    sticker_id: str = Field(..., description="贴纸的唯一标识ID")
    start: int = Field(..., description="贴纸开始时间（微秒）")
    end: int = Field(..., description="贴纸结束时间（微秒）")
    scale: float = Field(default=1.0, description="贴纸缩放比例，建议范围[0.1, 5.0]")
    transform_x: int = Field(default=0, description="X轴位置偏移（像素），以画布中心为原点")
    transform_y: int = Field(default=0, description="Y轴位置偏移（像素），以画布中心为原点")

class AddStickerResponse(BaseModel):
    """添加贴纸响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    sticker_id: str = Field(default="", description="贴纸的唯一标识ID")
    track_id: str = Field(default="", description="轨道ID")
    segment_id: str = Field(default="", description="片段ID")
    duration: int = Field(default=0, description="贴纸显示时长（微秒）")