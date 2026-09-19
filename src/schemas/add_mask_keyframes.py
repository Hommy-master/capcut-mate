from pydantic import BaseModel, Field, model_validator
from typing import List, Optional


class MaskKeyframeItem(BaseModel):
    """单个时间点上的蒙版关键帧。X/Y/feather/rotation 均为可选，但至少提供一个。"""
    segment_id: str = Field(..., description="目标视频片段ID")
    offset: int = Field(..., ge=0, description="相对片段起点的时间偏移（微秒）")
    X: Optional[float] = Field(default=None, description="蒙版中心X坐标（像素，相对素材中心，右为正）")
    Y: Optional[float] = Field(default=None, description="蒙版中心Y坐标（像素，相对素材中心，下为正）")
    feather: Optional[float] = Field(default=None, ge=0, le=100, description="羽化程度（0-100）")
    rotation: Optional[float] = Field(default=None, description="旋转角度（度）")

    @model_validator(mode="after")
    def require_at_least_one_property(self):
        if self.X is None and self.Y is None and self.feather is None and self.rotation is None:
            raise ValueError("X、Y、feather、rotation 至少需要提供一个")
        return self


class AddMaskKeyframesRequest(BaseModel):
    """添加蒙版关键帧请求参数"""
    draft_url: str = Field(default="", description="草稿URL")
    keyframes: List[MaskKeyframeItem] = Field(default=[], description="蒙版关键帧列表")


class AddMaskKeyframesResponse(BaseModel):
    """添加蒙版关键帧响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    keyframes_added: int = Field(default=0, description="写入的草稿属性条数（X 与 Y 分别计 1）")
    affected_segments: List[str] = Field(default=[], description="受影响的片段ID列表")
