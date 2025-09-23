from pydantic import BaseModel, Field
from typing import List


class AddVideosRequest(BaseModel):
    """批量添加视频请求参数"""
    draft_url: str = Field(default="", description="草稿URL")
    video_infos: str = Field(default="", description="视频信息列表, 用JSON字符串表示")
    alpha: float = Field(default=1.0, description="全局透明度[0, 1]")
    scale_x: float = Field(default=1.0, description="X轴缩放比例, 建议范围[0.1, 5.0]")
    scale_y: float = Field(default=1.0, description="Y轴缩放比例, 建议范围[0.1, 5.0]")
    transform_x: int = Field(default=0, description="X轴位置偏移(像素)")
    transform_y: int = Field(default=0, description="Y轴位置偏移(像素)")

class AddVideosResponse(BaseModel):
    """添加视频响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    track_id: str = Field(default="", description="轨道ID")
    video_ids: List[str] = Field(default=[], description="视频ID列表")
    segment_ids: List[str] = Field(default=[], description="片段ID列表")
