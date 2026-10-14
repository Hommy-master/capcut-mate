from pydantic import BaseModel, Field
from typing import List


class StickerItem(BaseModel):
    """贴纸项

    只保留检索与实际使用所需的三个字段：``title`` 是唯一的搜索键，
    ``sticker_id`` 是 add_sticker 唯一需要的入参，``image_url`` 供调用方展示预览。
    贴纸包体积/每帧尺寸、贴纸类型、预览封面等字段无任何代码读取，已从配置中移除。
    """
    title: str = Field(..., description="贴纸标题")
    sticker_id: str = Field(..., description="贴纸ID")
    image_url: str = Field(..., description="贴纸预览图URL")


class SearchStickerRequest(BaseModel):
    """搜索贴纸请求参数"""
    keyword: str = Field(..., description="关键词，必选参数")


class SearchStickerResponse(BaseModel):
    """搜索贴纸响应参数"""
    data: List[StickerItem] = Field(..., description="贴纸数据列表")
