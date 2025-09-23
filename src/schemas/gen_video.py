from pydantic import BaseModel, Field


class GenVideoRequest(BaseModel):
    """根据草稿导出视频"""
    draft_url: str = Field(default="", description="草稿URL")


class GenVideoResponse(BaseModel):
    """生成视频响应参数"""
    video_url: str = Field(default="", description="视频URL")
