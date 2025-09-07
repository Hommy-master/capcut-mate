from pydantic import BaseModel, Field


class GetDraftRequest(BaseModel):
    """获取草稿请求参数"""
    draft_id: str = Field(..., min_length=20, max_length=32, description="草稿ID")


class GetDraftResponse(BaseModel):
    """获取草稿响应参数"""
    files: list[str] = Field(default=[], description="文件列表")
