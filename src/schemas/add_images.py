import json
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any


class AddImagesRequest(BaseModel):
    """批量添加图片请求参数"""
    draft_url: str = Field(..., description="草稿URL")
    image_infos: str = Field(..., description="图片信息列表, 用JSON字符串表示")
    alpha: float = Field(default=1.0, description="全局透明度[0, 1]")
    scale_x: float = Field(default=1.0, description="X轴缩放比例")
    scale_y: float = Field(default=1.0, description="Y轴缩放比例")
    transform_x: int = Field(default=0, description="X轴位置偏移(像素)")
    transform_y: int = Field(default=0, description="Y轴位置偏移(像素)")

    @field_validator("image_infos")
    @classmethod
    def validate_image_infos_http_urls(cls, value: str) -> str:
        """在 schema 层校验 image_url 必须为 http/https。"""
        try:
            data = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"image_infos JSON parse error: {exc.msg}") from exc

        if not isinstance(data, list):
            raise ValueError("image_infos should be a list")

        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(f"image_infos[{idx}] should be an object")
            image_url = item.get("image_url")
            if not isinstance(image_url, str) or not image_url.startswith(("http://", "https://")):
                raise ValueError(f"image_infos[{idx}].image_url must start with http:// or https://")
        return value


class SegmentInfo(BaseModel):
    """片段信息"""
    id: str = Field(..., description="片段ID")
    start: int = Field(..., description="开始时间(微秒)")
    end: int = Field(..., description="结束时间(微秒)")


class AddImagesResponse(BaseModel):
    """添加图片响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    track_id: str = Field(default="", description="视频轨道ID")
    image_ids: List[str] = Field(default=[], description="图片ID列表")
    segment_ids: List[str] = Field(default=[], description="片段ID列表")
    segment_infos: List[SegmentInfo] = Field(default=[], description="片段信息列表")