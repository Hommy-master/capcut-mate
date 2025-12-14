from pydantic import BaseModel, Field
from typing import List, Optional


class StickerPackage(BaseModel):
    """贴纸包信息"""
    height_per_frame: int = Field(..., description="每帧高度")
    size: int = Field(..., description="贴纸包大小")
    width_per_frame: int = Field(..., description="每帧宽度")


class LargeImage(BaseModel):
    """大图信息"""
    image_url: str = Field(..., description="图片URL")


class StickerInfo(BaseModel):
    """贴纸信息"""
    large_image: LargeImage = Field(..., description="大图信息")
    preview_cover: str = Field(..., description="预览封面")
    sticker_package: StickerPackage = Field(..., description="贴纸包信息")
    sticker_type: int = Field(..., description="贴纸类型")
    track_thumbnail: str = Field(..., description="轨道缩略图")


class StickerItem(BaseModel):
    """贴纸项"""
    sticker: StickerInfo = Field(..., description="贴纸信息")
    sticker_id: str = Field(..., description="贴纸ID")
    title: str = Field(..., description="贴纸标题")


class SearchStickerRequest(BaseModel):
    """搜索贴纸请求参数"""
    keyword: str = Field(..., description="关键词，必选参数")


class SearchStickerResponse(BaseModel):
    """搜索贴纸响应参数"""
    data: List[StickerItem] = Field(..., description="贴纸数据列表")