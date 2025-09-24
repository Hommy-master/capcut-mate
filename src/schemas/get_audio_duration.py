from pydantic import BaseModel, Field, HttpUrl


class GetAudioDurationRequest(BaseModel):
    """获取音频时长请求参数"""
    mp3_url: HttpUrl = Field(
        ..., 
        description="音频文件URL，支持mp3、wav、m4a等常见音频格式"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "mp3_url": "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav"
            }
        }


class GetAudioDurationResponse(BaseModel):
    """获取音频时长响应参数"""
    duration: int = Field(
        ..., 
        description="音频时长，单位：微秒",
        ge=0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "duration": 2325333
            }
        }