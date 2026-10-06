from pydantic import BaseModel, Field
from pydantic.functional_validators import field_validator
from typing import Optional

from src.schemas.validators import validate_api_key_uuid


class GenVideoRequest(BaseModel):
    """根据草稿导出视频"""
    draft_url: str = Field(default="", description="草稿URL")
    apiKey: Optional[str] = Field(
        default=None,
        description="apiKey 必须是合法的 UUID 格式；可登录官网 https://jcaigc.cn 获取",
    )
    
    @field_validator('apiKey')
    @classmethod
    def validate_api_key(cls, v):
        return validate_api_key_uuid(v)


class GenVideoResponse(BaseModel):
    """生成视频响应参数"""
    message: str = Field(..., description="响应消息")