"""云渲染进行中数量查询"""
from pydantic import BaseModel, Field


class GenVideoActiveCountResponse(BaseModel):
    """当前排队与渲染中的云渲染草稿数量"""
    count: int = Field(..., description="排队中(pending)与渲染中(processing)的草稿数量，不含已完成/失败")
