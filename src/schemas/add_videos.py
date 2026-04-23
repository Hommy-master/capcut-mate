import json
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class SceneTimelineItem(BaseModel):
    """场景时间线项"""
    start: int = Field(..., description="场景开始时间（微秒）")
    end: int = Field(..., description="场景结束时间（微秒）")


class AddVideosRequest(BaseModel):
    """批量添加视频请求参数"""
    draft_url: str = Field(default="", description="草稿URL")
    video_infos: str = Field(default="", description="视频信息列表, 用JSON字符串表示")
    scene_timelines: Optional[List[SceneTimelineItem]] = Field(default=None, description="场景时间线列表，用于视频变速")
    alpha: float = Field(default=1.0, description="全局透明度[0, 1]")
    scale_x: float = Field(default=1.0, description="X轴缩放比例, 建议范围[0.1, 5.0]")
    scale_y: float = Field(default=1.0, description="Y轴缩放比例, 建议范围[0.1, 5.0]")
    transform_x: int = Field(default=0, description="X轴位置偏移(像素)")
    transform_y: int = Field(default=0, description="Y轴位置偏移(像素)")

    @field_validator("video_infos")
    @classmethod
    def validate_video_infos_http_urls(cls, value: str) -> str:
        """在 schema 层校验 video_url 必须为 http/https。"""
        try:
            data = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"video_infos JSON parse error: {exc.msg}") from exc

        if not isinstance(data, list):
            raise ValueError("video_infos should be a list")

        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(f"video_infos[{idx}] should be an object")
            video_url = item.get("video_url")
            if not isinstance(video_url, str) or not video_url.startswith(("http://", "https://")):
                raise ValueError(f"video_infos[{idx}].video_url must start with http:// or https://")
        return value

class AddVideosResponse(BaseModel):
    """添加视频响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    track_id: str = Field(default="", description="轨道ID")
    video_ids: List[str] = Field(default=[], description="视频ID列表")
    segment_ids: List[str] = Field(default=[], description="片段ID列表")
