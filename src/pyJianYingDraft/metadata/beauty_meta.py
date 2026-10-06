"""人像美化（figure）元数据。

强度在剪映界面是 0~100，写入草稿时为 0~1（肤色 temperature 除外，按 ÷99 归一）。
写入位置有三种：
- value：顶层 value（skin.smooth / skin.whitening、全部 body 滑杆）；
- adjust_param：adjust_params（全部 shape 滑杆，以及 skin.even / skin.plump / skin.dewrinkle /
  skin.bright_eye / skin.dark_circle / skin.white_teeth）；
- face_adjust：face_adjust_params（skin.skin_tone、makeup.look）。

滑杆按剪映面板分组：skin / shape / makeup / body；smooth 与 whitening 在 skin 与 body 下是两个不同素材。
接口字段名（`name`）取自剪映自身导出的草稿标识（intensity_key）与海外版剪映 UI 文案；
写进草稿的 `name` 字段（`draft_name`）仍是剪映面板的中文显示名，与真实草稿逐条一致。
预设条目（makeup.look、skin.skin_tone）的键是剪映预设值本身，保持中文。
所有 resource_id 均已与剪映真实导出的草稿（10月5日-02/draft_content.json）逐条核对。
"""

from dataclasses import dataclass
from typing import Dict, Literal, Optional, Tuple

# 分组名，与接口请求体中的四个键一致
GROUP_SKIN = "skin"
GROUP_SHAPE = "shape"
GROUP_MAKEUP = "makeup"
GROUP_BODY = "body"
BEAUTY_GROUPS: Tuple[str, ...] = (GROUP_SKIN, GROUP_SHAPE, GROUP_MAKEUP, GROUP_BODY)

# 肤色 face_adjust_params 的参数名；temperature 按 ÷99 归一（实测 11 → 0.1111111068725586）
SKIN_COLD_WARM_KEY = "face_adjust_skin_ColdWarm"
SKIN_INTENSITY_KEY = "face_adjust_skin_Intensity"
SKIN_COLD_WARM_DIVISOR = 99.0

# 美妆 face_adjust_params 的强度参数名
MAKEUP_WHOLE_KEY = "face_adjust_whole"

# face_adjust 的 face_id 取该值表示作用于全部人脸（与剪映「全局应用」一致）
ALL_FACES = "-1"

# 美妆固定的排除组（剪映写入 11 项，避免与其它妆容部件叠加）
MAKEUP_EXCLUSION_GROUP: Tuple[str, ...] = (
    "face_adjust_brow",
    "face_adjust_eyeshadow",
    "face_adjust_eyeline",
    "face_adjust_eyelash",
    "face_adjust_pupil",
    "face_adjust_eyelight",
    "face_adjust_stereo",
    "face_adjust_blusher",
    "face_adjust_lip",
    "face_adjust_mask",
    "face_adjust_highlight",
)


@dataclass(frozen=True)
class BeautyMeta:
    """单个滑杆 / 肤色预设 / 美妆套装在草稿中的资源定义。"""

    name: str
    """分组内唯一键，也是接口中的英文字段名；预设类条目为剪映预设值本身（如 淡人妆）。"""
    draft_name: str
    """写入草稿 `name` 字段的剪映显示名（中文），用于剪映面板展示；预设类条目与 name 相同。"""
    group: str
    """所属分组：skin / shape / makeup / body。"""
    resource_id: str
    """素材 resource_id；预留（unsupported）条目为空串。"""
    intensity_mode: Literal["value", "adjust_param", "face_adjust"]
    """强度落点：value 写顶层 value；adjust_param 写 adjust_params；face_adjust 写 face_adjust_params。"""
    sub_type: str
    """figure 的 sub_type：滑杆多为 auto_beauty，肤色 exclusion，美妆 exclusion_face，美体 none。"""
    category_id: str
    """面板分类：skin auto-beauty2 / shape auto-beauty / makeup makeup / body auto-beauty3。"""
    needs_algorithm_path: bool
    supported: bool = True
    """False 表示剪映草稿中无对应素材（预留字段），仅允许传 0。"""
    intensity_key: str = ""
    adjust_param_name: str = "0"
    """adjust_param 模式下 adjust_params[0].name，剪映实测恒为 "0"。"""
    face_adjust_param_name: str = ""
    """face_adjust 模式下强度参数名：肤色 face_adjust_skin_Intensity，美妆 face_adjust_whole。"""
    cold_warm_key: str = ""
    """仅肤色：face_adjust_skin_ColdWarm。"""
    cold_warm_divisor: float = 100.0
    """仅肤色：temperature 归一除数（99）。"""
    face_id: str = "-1"
    """face_adjust 模式下 face_adjust_params[0].face_id：检出的第几张人脸（0 起），"-1" 表示全部人脸。"""
    exclusion_group: Tuple[str, ...] = ()
    material_type: str = "figure"


def _skin(name: str, draft_name: str, resource_id: str, intensity_key: str = "", *,
          mode: str = "adjust_param", sub_type: str = "auto_beauty",
          needs_algorithm_path: bool = True) -> BeautyMeta:
    """skin 组滑杆（category_id auto-beauty2）。"""
    return BeautyMeta(
        name, draft_name, GROUP_SKIN, resource_id, mode, sub_type, "auto-beauty2",
        needs_algorithm_path, intensity_key=intensity_key,
    )


def _shape(name: str, draft_name: str, resource_id: str, intensity_key: str, *,
           supported: bool = True) -> BeautyMeta:
    """shape 组滑杆（category_id auto-beauty，adjust_param + 算法路径）。"""
    return BeautyMeta(
        name, draft_name, GROUP_SHAPE, resource_id, "adjust_param", "auto_beauty", "auto-beauty",
        True, supported=supported, intensity_key=intensity_key,
    )


def _body(name: str, draft_name: str, resource_id: str, intensity_key: str = "", *,
          supported: bool = True) -> BeautyMeta:
    """body 组滑杆（category_id auto-beauty3，顶层 value，无算法路径）。"""
    return BeautyMeta(
        name, draft_name, GROUP_BODY, resource_id, "value", "none", "auto-beauty3",
        False, supported=supported, intensity_key=intensity_key,
    )


def _makeup(name: str, draft_name: str, resource_id: str, face_id: str = ALL_FACES) -> BeautyMeta:
    """美妆套装（category_id makeup，face_adjust + face_adjust_whole）。

    face_id 默认 ALL_FACES：妆容落到哪张人脸由视频里检出的顺序决定（与剪映「全局应用」一致），
    不能固定成某张脸 —— 参考草稿里的 "1" 是该视频第 2 张人脸的序号，换一段素材就会指空。
    """
    return BeautyMeta(
        name, draft_name, GROUP_MAKEUP, resource_id, "face_adjust", "exclusion_face", "makeup",
        True, face_adjust_param_name=MAKEUP_WHOLE_KEY, face_id=face_id,
        exclusion_group=MAKEUP_EXCLUSION_GROUP,
    )


def _skin_tone(name: str, draft_name: str, resource_id: str) -> BeautyMeta:
    """肤色预设（category_id auto-beauty2，face_adjust + temperature/intensity 双参数）。"""
    return BeautyMeta(
        name, draft_name, GROUP_SKIN, resource_id, "face_adjust", "exclusion", "auto-beauty2",
        False, face_adjust_param_name=SKIN_INTENSITY_KEY,
        cold_warm_key=SKIN_COLD_WARM_KEY, cold_warm_divisor=SKIN_COLD_WARM_DIVISOR,
        face_id="-1", exclusion_group=("face_adjust_skin",),
    )


BEAUTY_CATALOG: Dict[str, Dict[str, BeautyMeta]] = {
    GROUP_SKIN: {
        "even": _skin("even", "匀肤", "7106322605304451614", "face_adjust_yunfu"),
        "plump": _skin("plump", "丰盈", "7165761391037518350", "face_adjust_fuling"),
        "smooth": _skin("smooth", "磨皮", "6976822940608238093", mode="value"),
        "dewrinkle": _skin("dewrinkle", "祛法令纹", "7127560078508429831", "face_adjust_NasolabialFolds"),
        "bright_eye": _skin("bright_eye", "亮眼", "7210363411970921017", "face_adjust_BrightEye"),
        "dark_circle": _skin("dark_circle", "祛黑眼圈", "7127559798861599268", "face_adjust_Pouch"),
        "whitening": _skin("whitening", "美白", "6998408303826965006", mode="value", sub_type="none", needs_algorithm_path=False),
        "white_teeth": _skin("white_teeth", "白牙", "6998408263892996639"),
    },
    GROUP_SHAPE: {
        "small_face": _shape("small_face", "小脸", "7325345220688613914", "face_adjust_YouTaiFace"),
        "slim": _shape("slim", "瘦脸", "7126765507457323557", "face_adjust_TotalFace"),
        "v_shape": _shape("v_shape", "V脸", "7358087335411454501", "face_adjust_VFace"),
        "jaw": _shape("jaw", "下颌骨", "7126764917918536199", "face_adjust_ZoomJawbone"),
        "cheekbone": _shape("cheekbone", "颧骨", "7127587811795931662", "face_adjust_ZoomCheekbone"),
        "shorten": _shape("shorten", "短脸", "7126865570653278751", "face_adjust_SmallFace"),
        "contour_smooth": _shape("contour_smooth", "流畅脸", "7165761469231927838", "face_adjust_lunkuopinghua"),
        "lower": _shape("lower", "下庭", "7130850220891443725", "face_adjust_lower_atrium"),
        "middle": _shape("middle", "中庭", "7130850182488396325", "face_adjust_mid_atrium"),
        "upper": _shape("upper", "上庭", "7130849819957924389", "face_adjust_upper_atrium"),
        "hairline": _shape("hairline", "发际线", "7126865429154238984", "face_adjust_Forehead"),
        # 预留：剪映草稿中值为 0 时未写出素材，暂无 resource_id
        "width": _shape("width", "窄脸", "", "", supported=False),
        "chin_length": _shape("chin_length", "下巴长短", "", "", supported=False),
    },
    GROUP_MAKEUP: {
        # 预设值本身即剪映妆容名，接口值与草稿显示名相同；
        # face_id 默认全部人脸，调用方可在请求里指定具体人脸序号
        "淡人妆": _makeup("淡人妆", "淡人妆", "7376172391774294554"),
        "氧气感": _makeup("氧气感", "氧气感", "7154258998315717150"),
    },
    GROUP_BODY: {
        "small_head": _body("small_head", "小头", "6976812039847023111", "body_adjust_SmallHead"),
        "swan_neck": _body("swan_neck", "天鹅颈", "7187453444146336313", "body_adjust_SwanNeck"),
        "slim_arm": _body("slim_arm", "瘦手臂", "7187394795965256247", "body_adjust_SlimArm"),
        "straight_shoulder": _body("straight_shoulder", "直角肩", "7246635041663488567", "body_adjust_OrthoShoulder"),
        "slim_body": _body("slim_body", "瘦身", "6976812219048661540", "body_adjust_SlimBody"),
        "slim_waist": _body("slim_waist", "瘦腰", "6976812120591569416", "body_adjust_SlimWaist"),
        "long_leg": _body("long_leg", "长腿", "6956089104412971534", "body_adjust_StretchLeg"),
        "plump_breast": _body("plump_breast", "丰胸", "7168288902728389157", "body_adjust_SlimBreast"),
        "slim_hip": _body("slim_hip", "美胯", "7168289037562679838", "body_adjust_SlimHip"),
        "smooth": _body("smooth", "磨皮", "7125729150572171812"),
        "whitening": _body("whitening", "美白", "7125780457576206879"),
        # 预留：剪映草稿中值为 0 时未写出素材，暂无 resource_id
        "wide_shoulder": _body("wide_shoulder", "宽肩", "", supported=False),
    },
}

SKIN_TONE_PRESETS: Dict[str, BeautyMeta] = {
    # 预设值本身即剪映肤色名，接口值与草稿显示名相同
    "冷白": _skin_tone("冷白", "冷白", "7148720872105185800"),
    "暖白": _skin_tone("暖白", "暖白", "7148720647714116132"),
}

MAKEUP_ROOT = BeautyMeta(
    name="makeup-root",
    draft_name="makeup-root",
    group="",
    resource_id="7273096354098844221",
    intensity_mode="value",
    sub_type="auto_beauty",
    category_id="",
    needs_algorithm_path=True,
    material_type="makeup_root",
)
"""人像美化伴随素材。任意滑杆生效时每个片段补一条，强度固定为 0。"""


def find_beauty_type(group: str, name: str) -> Optional[BeautyMeta]:
    """按分组 + 名称查找滑杆 / 美妆套装（同名滑杆在 skin 与 body 下是两个不同素材）。"""
    return BEAUTY_CATALOG.get(group, {}).get(name)


def find_skin_tone(name: str) -> Optional[BeautyMeta]:
    """按名称查找肤色预设（冷白 / 暖白）。"""
    return SKIN_TONE_PRESETS.get(name)


def supported_sliders(group: str) -> Dict[str, BeautyMeta]:
    """返回分组内已支持（有真实 resource_id）的滑杆。"""
    return {name: meta for name, meta in BEAUTY_CATALOG.get(group, {}).items() if meta.supported}


def build_figure_algorithm_path(placeholder_id: str, video_material_id: str) -> str:
    """smooth、white_teeth、makeup-root 等共用的算法产物路径。

    后缀是视频素材 id，不是随机目录。同一草稿的 placeholder 保持不变。
    """
    return (
        f"##_draftpath_placeholder_{placeholder_id}_##"
        f"/video/figure_algorithm/{video_material_id}"
    )
