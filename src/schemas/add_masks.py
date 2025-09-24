from pydantic import BaseModel, Field
from typing import List


class AddMasksRequest(BaseModel):
    """添加遮罩请求参数"""
    draft_url: str = Field(default="", description="草稿URL")
    segment_ids: List[str] = Field(default=[], description="要应用遮罩的片段ID数组")
    name: str = Field(default="线性", description="遮罩类型名称")
    X: int = Field(default=0, description="遮罩中心X坐标（像素）")
    Y: int = Field(default=0, description="遮罩中心Y坐标（像素）")
    width: int = Field(default=512, description="遮罩宽度（像素）")
    height: int = Field(default=512, description="遮罩高度（像素）")
    feather: int = Field(default=0, description="羽化程度（0-100）")
    rotation: int = Field(default=0, description="旋转角度（度）")
    invert: bool = Field(default=False, description="是否反转遮罩")
    roundCorner: int = Field(default=0, description="圆角半径（0-100）")


class AddMasksResponse(BaseModel):
    """添加遮罩响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    masks_added: int = Field(default=0, description="成功添加的遮罩数量")
    affected_segments: List[str] = Field(default=[], description="受影响的片段ID列表")
    mask_ids: List[str] = Field(default=[], description="遮罩ID列表")