from pydantic import BaseModel, Field, field_validator
from typing import Optional


class EasyCreateMaterialRequest(BaseModel):
    """快速创建素材轨道请求参数"""
    draft_url: str = Field(..., description="目标草稿的完整URL")
    audio_url: str = Field(..., description="音频文件URL，不能为空或null")
    text: Optional[str] = Field(default=None, description="要添加的文字内容")
    img_url: Optional[str] = Field(default=None, description="图片文件URL")
    video_url: Optional[str] = Field(default=None, description="视频文件URL")
    text_color: str = Field(default="#ffffff", description="文字颜色（十六进制格式）")
    font_size: int = Field(default=15, description="字体大小")
    text_transform_y: int = Field(default=0, description="文字Y轴位置偏移")

    @staticmethod
    def _is_http_url(url: str) -> bool:
        return isinstance(url, str) and url.startswith(("http://", "https://"))

    @field_validator("audio_url")
    @classmethod
    def validate_audio_url(cls, value: str) -> str:
        """音频 URL 必须为 http/https。"""
        if not cls._is_http_url(value):
            raise ValueError("audio_url must start with http:// or https://")
        return value

    @field_validator("img_url", "video_url")
    @classmethod
    def validate_optional_media_url(cls, value: Optional[str]) -> Optional[str]:
        """可选图片/视频 URL 如有传值，必须为 http/https。"""
        if value is None:
            return value
        if not cls._is_http_url(value):
            raise ValueError("optional media URL must start with http:// or https://")
        return value


class EasyCreateMaterialResponse(BaseModel):
    """快速创建素材轨道响应参数"""
    draft_url: str = Field(default="", description="草稿URL")