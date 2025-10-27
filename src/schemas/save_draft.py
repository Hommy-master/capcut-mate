from pydantic import BaseModel, Field


class SaveDraftRequest(BaseModel):
    """创建草稿请求参数"""
    draft_url: str = Field(default="", description="草稿URL")


class SaveDraftResponse(BaseModel):
    """创建草稿响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
