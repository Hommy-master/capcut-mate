import uuid
from pydantic import BaseModel, Field
from pydantic.functional_validators import field_validator
from typing import Optional


class GenVideoRequest(BaseModel):
    """根据草稿导出视频"""
    draft_url: str = Field(default="", description="草稿URL")
    apiKey: Optional[str] = Field(default=None, description="apiKey必须是合法的UUID格式")
    
    @field_validator('apiKey')
    @classmethod
    def validate_api_key(cls, v):
        if v is None or v == "":
            return None
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError('API密钥格式不正确，必须是合法的UUID')
        return v


class GenVideoResponse(BaseModel):
    """生成视频响应参数"""
    message: str = Field(..., description="响应消息")