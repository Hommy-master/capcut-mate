from pydantic import BaseModel, Field


class AddTextStyleRequest(BaseModel):
    """创建文本富文本样式请求参数"""
    text: str = Field(..., description="要处理的文本内容")
    keyword: str = Field(..., description="关键词，多个用 | 分隔")
    font_size: int = Field(default=12, description="普通文本的字体大小")
    keyword_color: str = Field(default="#ff7100", description="关键词文本颜色（十六进制）")
    keyword_font_size: int = Field(default=15, description="关键词字体大小")


class AddTextStyleResponse(BaseModel):
    """创建文本富文本样式响应参数"""
    text_style: str = Field(default="", description="文本样式JSON字符串")