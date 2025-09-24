"""
视频生成状态查询的数据模型定义
"""
from typing import Optional
from pydantic import BaseModel, Field


class GenVideoStatusRequest(BaseModel):
    """查询视频生成状态的请求模型"""
    draft_url: str = Field(..., description="草稿URL")


class GenVideoStatusResponse(BaseModel):
    """查询视频生成状态的响应模型"""
    draft_url: str = Field(..., description="草稿URL")
    status: str = Field(..., description="任务状态：pending=等待中，processing=处理中，completed=已完成，failed=失败")
    progress: int = Field(..., description="任务进度（0-100）")
    video_url: str = Field(default="", description="生成的视频URL（仅在completed状态时有值）")
    error_message: str = Field(default="", description="错误信息（仅在failed状态时有值）")
    created_at: Optional[str] = Field(default=None, description="任务创建时间")
    started_at: Optional[str] = Field(default=None, description="任务开始时间")
    completed_at: Optional[str] = Field(default=None, description="任务完成时间")