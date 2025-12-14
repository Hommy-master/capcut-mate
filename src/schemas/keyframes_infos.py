from pydantic import BaseModel, Field
from typing import List, Optional


class SegmentInfoItem(BaseModel):
    """轨道数据项"""
    id: str = Field(..., description="片段ID")
    start: int = Field(..., description="开始时间（微秒）")
    end: int = Field(..., description="结束时间（微秒）")


class KeyframesInfosRequest(BaseModel):
    """关键帧信息请求参数"""
    ctype: str = Field(..., description="关键帧类型：KFTypePositionX: X轴移动，需要提供width参数，值会被除以width进行归一化 KFTypePositionY: Y轴移动，需要提供height参数，值会被除以height进行归一化 KFTypeRotation: 旋转角度，值范围必须在0-360度之间 UNIFORM_SCALE: 均匀缩放，值范围必须在0.01-5之间 KFTypeAlpha: 透明度，值范围必须在0-1之间")
    offsets: str = Field(..., description="需要放置关键帧的位置比例，eg：0|100 这个就是代表在开始和结尾放置，0|50|100代表在开头，中间，结尾放置3个关键帧")
    values: str = Field(..., description="对应offsets的值，长度要一致，比如1|2，或者1|2|1")
    segment_infos: List[SegmentInfoItem] = Field(..., description="轨道数据，对象数组")
    height: Optional[int] = Field(None, description="视频高，可选参数")
    width: Optional[int] = Field(None, description="视频宽，可选参数")


class KeyframesInfosResponse(BaseModel):
    """关键帧信息响应参数"""
    keyframes_infos: str = Field(..., description="JSON字符串格式的关键帧信息")