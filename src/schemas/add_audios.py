import json
from pydantic import BaseModel, Field, field_validator
from typing import List


class AddAudiosRequest(BaseModel):
    """批量添加音频请求参数"""
    draft_url: str = Field(..., description="草稿URL")
    audio_infos: str = Field(..., description="音频信息列表, 用JSON字符串表示")

    @field_validator("audio_infos")
    @classmethod
    def validate_audio_infos_http_urls(cls, value: str) -> str:
        """在 schema 层校验 audio_url 必须为 http/https。"""
        try:
            data = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"audio_infos JSON parse error: {exc.msg}") from exc

        if not isinstance(data, list):
            raise ValueError("audio_infos should be a list")

        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(f"audio_infos[{idx}] should be an object")
            audio_url = item.get("audio_url")
            if not isinstance(audio_url, str) or not audio_url.startswith(("http://", "https://")):
                raise ValueError(f"audio_infos[{idx}].audio_url must start with http:// or https://")
        return value


class AddAudiosResponse(BaseModel):
    """添加音频响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    track_id: str = Field(default="", description="音频轨道ID")
    audio_ids: List[str] = Field(default=[], description="音频ID列表")