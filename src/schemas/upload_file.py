from pydantic import BaseModel, Field


class UploadFileResponse(BaseModel):
    """上传文件到对象存储响应参数（请求为 multipart/form-data，无请求体模型）"""
    url: str = Field(..., description="对象存储带签名的临时下载地址，可直接用于其它接口")
    key: str = Field(..., description="对象存储 object key")
    size: int = Field(..., description="文件实际字节数")
    size_mb: float = Field(..., description="文件体积，单位：MB（保留 3 位小数）")
    cost: float = Field(..., description="本次上传费用，单位：元（0.0005 元/MB，上传成功后扣费；未启用计费时为 0）")
    url_expire_days: int = Field(..., description="url 有效期，单位：天")

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://bucket.oss-cn-hangzhou.aliyuncs.com/jianchuang/2026-10-06/8f3a1c2d5e6b7a90_demo.mp4?OSSAccessKeyId=xxx&Expires=xxx&Signature=xxx",
                "key": "jianchuang/2026-10-06/8f3a1c2d5e6b7a90_demo.mp4",
                "size": 10485760,
                "size_mb": 10.0,
                "cost": 0.005,
                "url_expire_days": 7
            }
        }
