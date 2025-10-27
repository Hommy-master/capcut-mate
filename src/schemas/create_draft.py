from pydantic import BaseModel, Field


class CreateDraftRequest(BaseModel):
    """创建草稿请求参数"""
    height: int = Field(default=1080, ge=1, description="视频高度")
    width: int = Field(default=1920, ge=1, description="视频宽度")


class CreateDraftResponse(BaseModel):
    """创建草稿响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    tip_url: str = Field(default="", description="草稿提示URL，获取帮助文档")
