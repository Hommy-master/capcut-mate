from pydantic import BaseModel, Field


class GetUrlRequest(BaseModel):
    """提取链接请求参数"""
    output: str = Field(..., description='提取内容')


class GetUrlResponse(BaseModel):
    """提取链接响应参数"""
    output: str = Field(..., description='提取内容')