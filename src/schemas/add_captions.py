from pydantic import BaseModel, Field
from typing import List, Optional


class AddCaptionsRequest(BaseModel):
    """批量添加字幕请求参数"""
    draft_url: str = Field(default="", description="草稿URL")
    captions: str = Field(default="", description="字幕信息列表, 用JSON字符串表示")
    text_color: str = Field(default="#ffffff", description="文本颜色（十六进制）")
    border_color: Optional[str] = Field(default=None, description="边框颜色（十六进制）")
    alignment: int = Field(default=1, ge=0, le=5, description="文本对齐方式（0-5）")
    alpha: float = Field(default=1.0, ge=0.0, le=1.0, description="文本透明度（0.0-1.0）")
    font: Optional[str] = Field(default=None, description="字体名称")
    font_size: int = Field(default=15, ge=1, description="字体大小")
    letter_spacing: Optional[float] = Field(default=None, description="字间距")
    line_spacing: Optional[float] = Field(default=None, description="行间距")
    scale_x: float = Field(default=1.0, description="水平缩放")
    scale_y: float = Field(default=1.0, description="垂直缩放")
    transform_x: int = Field(default=0, description="水平位移")
    transform_y: int = Field(default=0, description="垂直位移")
    style_text: bool = Field(default=False, description="是否使用样式文本")


class CaptionItem(BaseModel):
    """单个字幕信息"""
    start: int = Field(..., description="字幕开始时间（微秒）")
    end: int = Field(..., description="字幕结束时间（微秒）")
    text: str = Field(..., description="字幕文本内容")
    keyword: Optional[str] = Field(default=None, description="关键词（用|分隔多个关键词）")
    keyword_color: str = Field(default="#ff7100", description="关键词颜色")
    keyword_font_size: int = Field(default=15, ge=1, description="关键词字体大小")
    font_size: int = Field(default=15, ge=1, description="文本字体大小")
    in_animation: Optional[str] = Field(default=None, description="入场动画")
    out_animation: Optional[str] = Field(default=None, description="出场动画")
    loop_animation: Optional[str] = Field(default=None, description="循环动画")
    in_animation_duration: Optional[int] = Field(default=None, description="入场动画时长")
    out_animation_duration: Optional[int] = Field(default=None, description="出场动画时长")
    loop_animation_duration: Optional[int] = Field(default=None, description="循环动画时长")


class AddCaptionsResponse(BaseModel):
    """添加字幕响应参数"""
    draft_url: str = Field(default="", description="草稿URL")
    track_id: str = Field(default="", description="字幕轨道ID")
    text_ids: List[str] = Field(default=[], description="字幕ID列表")
    segment_ids: List[str] = Field(default=[], description="字幕片段ID列表")