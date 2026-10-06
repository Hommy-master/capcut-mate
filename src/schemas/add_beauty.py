from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.pyJianYingDraft.metadata.beauty_meta import ALL_FACES


class BeautySkinGroup(BaseModel):
    """skin 参数组（剪映「美颜」面板）。滑杆为 0 表示不写入，与剪映「关闭」= 素材缺失一致。"""

    model_config = ConfigDict(extra="forbid")

    even: float = Field(default=0, ge=0, le=100, description="Even 匀肤强度（0-100）")
    plump: float = Field(default=0, ge=0, le=100, description="Plump 丰盈强度（0-100）")
    smooth: float = Field(default=0, ge=0, le=100, description="Smooth 磨皮强度（0-100），与 body.smooth 是两个素材")
    dewrinkle: float = Field(default=0, ge=0, le=100, description="Dewrinkle 祛法令纹强度（0-100）")
    bright_eye: float = Field(default=0, ge=0, le=100, description="Bright Eye 亮眼强度（0-100）")
    dark_circle: float = Field(default=0, ge=0, le=100, description="Dark circles 祛黑眼圈强度（0-100）")
    whitening: float = Field(default=0, ge=0, le=100, description="Whitening 美白强度（0-100），与 body.whitening 是两个素材")
    white_teeth: float = Field(default=0, ge=0, le=100, description="White teeth 白牙强度（0-100）")
    skin_tone: str = Field(default="", description="肤色预设：空字符串表示不应用；支持 冷白 / 暖白")
    temperature: float = Field(default=0, ge=0, le=99, description="肤色冷暖（0-99），仅设置 skin_tone 时生效")
    intensity: float = Field(default=60, ge=0, le=100, description="肤色程度（0-100），仅设置 skin_tone 时生效")


class BeautyShapeGroup(BaseModel):
    """shape 参数组（剪映「美型」- 面部面板）。滑杆为 0 表示不写入。"""

    model_config = ConfigDict(extra="forbid")

    small_face: float = Field(default=0, ge=0, le=100, description="Small Face 小脸强度（0-100）")
    slim: float = Field(default=0, ge=0, le=100, description="Slim 瘦脸强度（0-100）")
    v_shape: float = Field(default=0, ge=0, le=100, description="V shape V脸强度（0-100）")
    jaw: float = Field(default=0, ge=0, le=100, description="Jaw 下颌骨强度（0-100）")
    cheekbone: float = Field(default=0, ge=0, le=100, description="Cheekbones 颧骨强度（0-100）")
    shorten: float = Field(default=0, ge=0, le=100, description="Shorten 短脸强度（0-100）")
    contour_smooth: float = Field(default=0, ge=0, le=100, description="Contour smooth 流畅脸强度（0-100）")
    lower: float = Field(default=0, ge=0, le=100, description="Lower 下庭强度（0-100）")
    middle: float = Field(default=0, ge=0, le=100, description="Middle 中庭强度（0-100）")
    upper: float = Field(default=0, ge=0, le=100, description="Upper 上庭强度（0-100）")
    hairline: float = Field(default=0, ge=0, le=100, description="Hairline 发际线强度（0-100）")
    width: float = Field(default=0, ge=0, le=100, description="Width 窄脸。预留字段，暂不支持，仅允许 0")
    chin_length: float = Field(default=0, ge=0, le=100, description="Chin Length 下巴长短。预留字段，暂不支持，仅允许 0")


class BeautyMakeupGroup(BaseModel):
    """makeup 参数组（剪映「美妆」面板）。"""

    model_config = ConfigDict(extra="forbid")

    look: str = Field(default="", description="妆容套装预设（剪映中文名，如 淡人妆 / 裸妆 / 原生 / 初恋）：空字符串表示不应用，全部取值见 docs/add_beauty.zh.md")
    intensity: float = Field(default=80, ge=0, le=100, description="套装程度（0-100），仅设置 look 时生效")
    face_id: str = Field(
        default=ALL_FACES,
        description='妆容作用的人脸：默认 "-1" 全部人脸（等价剪映「全局应用」）；也可指定检出的人脸序号 "0" / "1" / "2"…',
    )

    @field_validator("face_id")
    @classmethod
    def _validate_face_id(cls, value: str) -> str:
        """只接受 "-1"（全部人脸）或非负整数的人脸序号。"""
        normalized = str(value).strip()
        if normalized != ALL_FACES and not normalized.isdigit():
            raise ValueError(f"face_id must be {ALL_FACES} (all faces) or a non-negative face index, got {value!r}")
        return normalized


class BeautyBodyGroup(BaseModel):
    """body 参数组（剪映「美体」面板）。滑杆为 0 表示不写入。"""

    model_config = ConfigDict(extra="forbid")

    small_head: float = Field(default=0, ge=0, le=100, description="Small head 小头强度（0-100）")
    swan_neck: float = Field(default=0, ge=0, le=100, description="Swan neck 天鹅颈强度（0-100）")
    slim_arm: float = Field(default=0, ge=0, le=100, description="Slim arm 瘦手臂强度（0-100）")
    straight_shoulder: float = Field(default=0, ge=0, le=100, description="Straight shoulder 直角肩强度（0-100）")
    slim_body: float = Field(default=0, ge=0, le=100, description="Slim body 瘦身强度（0-100）")
    slim_waist: float = Field(default=0, ge=0, le=100, description="Slim waist 瘦腰强度（0-100）")
    long_leg: float = Field(default=0, ge=0, le=100, description="Long leg 长腿强度（0-100）")
    plump_breast: float = Field(default=0, ge=0, le=100, description="Plump breast 丰胸强度（0-100）")
    slim_hip: float = Field(default=0, ge=0, le=100, description="Slim hip 美胯强度（0-100）")
    smooth: float = Field(default=0, ge=0, le=100, description="美体磨皮强度（0-100），与 skin.smooth 是两个素材")
    whitening: float = Field(default=0, ge=0, le=100, description="美体美白强度（0-100），与 skin.whitening 是两个素材")
    wide_shoulder: float = Field(default=0, ge=0, le=100, description="Wide shoulder 宽肩。预留字段，暂不支持，仅允许 0")


class AddBeautyRequest(BaseModel):
    """添加美颜/美型/美妆/美体请求参数。

    四个分组 skin / shape / makeup / body 均可选，组内滑杆为 0 时不写入。
    分组键与滑杆键为英文，预设值（skin.skin_tone、makeup.look）沿用剪映预设名，为中文。
    """

    draft_url: str = Field(default="", description="草稿URL")
    segment_ids: List[str] = Field(default=[], description="要应用美颜的视频片段ID数组")
    skin: Optional[BeautySkinGroup] = Field(default=None, description="美颜参数组（剪映「美颜」面板）")
    shape: Optional[BeautyShapeGroup] = Field(default=None, description="美型参数组（剪映「美型」- 面部面板）")
    makeup: Optional[BeautyMakeupGroup] = Field(default=None, description="美妆参数组（剪映「美妆」面板）")
    body: Optional[BeautyBodyGroup] = Field(default=None, description="美体参数组（剪映「美体」面板）")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=2026xxxx",
                "segment_ids": ["segment-id-1"],
                "skin": {"smooth": 52, "whitening": 67, "skin_tone": "冷白", "temperature": 11, "intensity": 60},
                "shape": {"small_face": 19, "slim": 33},
                "makeup": {"look": "淡人妆", "intensity": 80},
                "body": {"small_head": 33, "slim_waist": 60, "smooth": 19, "whitening": 26},
            }
        }
    )


class AddBeautyResponse(BaseModel):
    """添加美颜/美型/美妆/美体响应参数"""

    draft_url: str = Field(default="", description="草稿URL")
    affected_segments: List[str] = Field(default=[], description="成功应用美颜的片段ID列表")
    figure_ids: List[str] = Field(default=[], description="人像美化素材ID列表，含 makeup-root")
