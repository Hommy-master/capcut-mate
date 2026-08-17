from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional


class SrtInfosRequest(BaseModel):
    """根据 SRT 文件生成字幕信息请求参数"""
    srt_url: HttpUrl = Field(..., description="SRT 字幕文件的 URL，必须以 http:// 或 https:// 开头")
    font_size: Optional[int] = Field(None, description="字体大小")
    keyword_color: Optional[str] = Field(None, description="关键词颜色")
    keyword_border_color: Optional[str] = Field(None, description="关键词边框颜色")
    keyword_font_size: Optional[int] = Field(None, description="关键词字体大小")
    keywords: Optional[List[str]] = Field(None, description="文本里面的重点词列表，按字幕条目顺序对应")
    in_animation: Optional[str] = Field(None, description="入场动画名称")
    in_animation_duration: Optional[int] = Field(None, description="入场动画时长")
    loop_animation: Optional[str] = Field(None, description="组合动画名称")
    loop_animation_duration: Optional[int] = Field(
        None, description="循环动画单次循环时长（微秒），与 get_text_animations 中 loop 的 duration 一致"
    )
    out_animation: Optional[str] = Field(None, description="出场动画名称")
    out_animation_duration: Optional[int] = Field(None, description="出场动画时长")
    transition: Optional[str] = Field(None, description="转场名称")
    transition_duration: Optional[int] = Field(None, description="转场时长")

    class Config:
        json_schema_extra = {
            "example": {
                "srt_url": "https://example.com/subtitles/demo.srt",
                "font_size": 15
            }
        }


class SrtInfosResponse(BaseModel):
    """根据 SRT 文件生成字幕信息响应参数"""
    infos: str = Field(..., description="JSON 字符串格式的字幕信息，可直接作为 add_captions 的 captions 入参")
    count: int = Field(..., description="解析出的字幕条目数量", ge=0)
