"""定义文本片段及其相关类"""

import json
import math
import uuid
from copy import deepcopy

from typing import Dict, Tuple, Any, List
from typing import Union, Optional, Literal

from .time_util import Timerange, tim
from .segment import ClipSettings, VisualSegment
from .animation import SegmentAnimations, Text_animation

from .metadata import FontType, EffectMeta
from .metadata import TextIntro, TextOutro, TextLoopAnim


def _rgb_to_hex(color: Tuple[float, float, float]) -> str:
    r, g, b = [max(0, min(255, int(round(c * 255)))) for c in color]
    return f"#{r:02X}{g:02X}{b:02X}"


def _style_range_end(text: str) -> int:
    """剪映 content.styles[].range 使用字符下标（非 UTF-16 字节长度）。"""
    return len(text)


def _font_content_json(font: Optional[EffectMeta]) -> Dict[str, str]:
    """styles[].font：系统字体 id 为空；自定义字体用 resource_id。
    path 必须为 \"D:\"，剪映打开后会自动搜索并改写为真实字体路径。
    """
    if font is None:
        return {"id": "", "path": "D:"}
    return {"id": font.resource_id, "path": "D:"}


def _build_fonts_material_entry(font: EffectMeta) -> Dict[str, Any]:
    """materials.texts[].fonts[] 单项，对齐剪映官方草稿结构。"""
    return {
        "category_id": "",
        "category_name": "",
        "effect_id": font.resource_id,
        "file_uri": "",
        "id": str(uuid.uuid4()).upper(),
        "path": "D:",
        "request_id": "",
        "resource_id": font.resource_id,
        "source_platform": 0,
        "team_id": "",
        "title": font.name,
    }


def _shadow_point(angle: float, distance: float) -> Dict[str, float]:
    """按角度/距离估算 shadow_point；默认 -45°/5 与官方草稿一致。"""
    rad = math.radians(angle)
    factor = 0.9 * (distance / 5.0)
    return {"x": math.cos(rad) * factor, "y": math.sin(rad) * factor}

class TextStyle:
    """字体样式类"""

    size: float
    """字体大小"""

    bold: bool
    """是否加粗"""
    italic: bool
    """是否斜体"""
    underline: bool
    """是否加下划线"""

    color: Tuple[float, float, float]
    """字体颜色, RGB三元组, 取值范围为[0, 1]"""
    alpha: float
    """字体不透明度"""

    align: Literal[0, 1, 2]
    """对齐方式"""
    vertical: bool
    """是否为竖排文本"""

    letter_spacing: int
    """字符间距"""
    line_spacing: int
    """行间距"""

    auto_wrapping: bool
    """是否自动换行"""
    max_line_width: float
    """最大行宽, 取值范围为[0, 1]"""

    def __init__(self, *, size: float = 8.0, bold: bool = False, italic: bool = False, underline: bool = False,
                 color: Tuple[float, float, float] = (1.0, 1.0, 1.0), alpha: float = 1.0,
                 align: Literal[0, 1, 2] = 0, vertical: bool = False,
                 letter_spacing: int = 0, line_spacing: int = 0,
                 auto_wrapping: bool = False, max_line_width: float = 0.82):
        """
        Args:
            size (`float`, optional): 字体大小, 默认为8.0
            bold (`bool`, optional): 是否加粗, 默认为否
            italic (`bool`, optional): 是否斜体, 默认为否
            underline (`bool`, optional): 是否加下划线, 默认为否
            color (`Tuple[float, float, float]`, optional): 字体颜色, RGB三元组, 取值范围为[0, 1], 默认为白色
            alpha (`float`, optional): 字体不透明度, 取值范围[0, 1], 默认不透明
            align (`int`, optional): 对齐方式, 0: 左对齐, 1: 居中, 2: 右对齐, 默认为左对齐
            vertical (`bool`, optional): 是否为竖排文本, 默认为否
            letter_spacing (`int`, optional): 字符间距, 定义与剪映中一致, 默认为0
            line_spacing (`int`, optional): 行间距, 定义与剪映中一致, 默认为0
            auto_wrapping (`bool`, optional): 是否自动换行, 默认关闭
            max_line_width (`float`, optional): 每行最大行宽占屏幕宽度比例, 取值范围为[0, 1], 默认为0.82
        """
        self.size = size
        self.bold = bold
        self.italic = italic
        self.underline = underline

        self.color = color
        self.alpha = alpha

        self.align = align
        self.vertical = vertical

        self.letter_spacing = letter_spacing
        self.line_spacing = line_spacing

        self.auto_wrapping = auto_wrapping
        self.max_line_width = max_line_width

class TextBorder:
    """文本描边的参数"""

    alpha: float
    """描边不透明度"""
    color: Tuple[float, float, float]
    """描边颜色, RGB三元组, 取值范围为[0, 1]"""
    width: float
    """描边宽度"""

    def __init__(self, *, alpha: float = 1.0, color: Tuple[float, float, float] = (0.0, 0.0, 0.0), width: float = 40.0):
        """
        Args:
            alpha (`float`, optional): 描边不透明度, 取值范围[0, 1], 默认为1.0
            color (`Tuple[float, float, float]`, optional): 描边颜色, RGB三元组, 取值范围为[0, 1], 默认为黑色
            width (`float`, optional): 描边宽度, 与剪映中一致, 取值范围为[0, 100], 默认为40.0
        """
        self.alpha = alpha
        self.color = color
        self.width = width / 100.0 * 0.2  # 此映射可能不完全正确

    def export_json(self) -> Dict[str, Any]:
        """导出JSON数据, 放置在素材content的styles中"""
        return {
            "content": {
                "solid": {
                    "alpha": self.alpha,
                    "color": list(self.color),
                }
            },
            "width": self.width
        }

class TextBackground:
    """文本背景参数"""

    style: Literal[1, 2]
    """背景样式"""

    alpha: float
    """背景不透明度"""
    color: str
    """背景颜色, 格式为'#RRGGBB'"""
    round_radius: float
    """背景圆角半径"""
    height: float
    """背景高度"""
    width: float
    """背景宽度"""
    horizontal_offset: float
    """背景水平偏移"""
    vertical_offset: float
    """背景竖直偏移"""

    def __init__(self, *, color: str, style: Literal[1, 2] = 1, alpha: float = 1.0, round_radius: float = 0.0,
                 height: float = 0.14, width: float = 0.14,
                 horizontal_offset: float = 0.5, vertical_offset: float = 0.5):
        """
        Args:
            color (`str`): 背景颜色, 格式为'#RRGGBB'
            style (`int`, optional): 背景样式, 1和2分别对应剪映中的两种样式, 默认为1
            alpha (`float`, optional): 背景不透明度, 与剪映中一致, 取值范围[0, 1], 默认为1.0
            round_radius (`float`, optional): 背景圆角半径, 与剪映中一致, 取值范围[0, 1], 默认为0.0
            height (`float`, optional): 背景高度, 与剪映中一致, 取值范围为[0, 1], 默认为0.14
            width (`float`, optional): 背景宽度, 与剪映中一致, 取值范围为[0, 1], 默认为0.14
            horizontal_offset (`float`, optional): 背景水平偏移, 与剪映中一致, 取值范围为[0, 1], 默认为0.5
            vertical_offset (`float`, optional): 背景竖直偏移, 与剪映中一致, 取值范围为[0, 1], 默认为0.5
        """
        self.style = style

        self.alpha = alpha
        self.color = color
        self.round_radius = round_radius
        self.height = height
        self.width = width
        self.horizontal_offset = horizontal_offset * 2 - 1
        self.vertical_offset = vertical_offset * 2 - 1

    def export_json(self) -> Dict[str, Any]:
        """生成子JSON数据, 在TextSegment导出时合并到其中"""
        return {
            "background_style": self.style,
            "background_color": self.color,
            "background_alpha": self.alpha,
            "background_round_radius": self.round_radius,
            "background_height": self.height,
            "background_width": self.width,
            "background_horizontal_offset": self.horizontal_offset,
            "background_vertical_offset": self.vertical_offset,
        }

class TextBubble:
    """文本气泡素材, 与滤镜素材本质上一致"""

    global_id: str
    """气泡全局id, 由程序自动生成"""

    effect_id: str
    resource_id: str

    def __init__(self, effect_id: str, resource_id: str):
        self.global_id = uuid.uuid4().hex
        self.effect_id = effect_id
        self.resource_id = resource_id

    def export_json(self) -> Dict[str, Any]:
        return {
            "apply_target_type": 0,
            "effect_id": self.effect_id,
            "id": self.global_id,
            "resource_id": self.resource_id,
            "type": "text_shape",
            "value": 1.0,
            # 不导出path和request_id
        }

class TextEffect(TextBubble):
    """文本花字素材, 与滤镜素材本质上也一致"""

    def export_json(self) -> Dict[str, Any]:
        ret = super().export_json()
        ret["type"] = "text_effect"
        ret["source_platform"] = 1
        return ret

class TextShadow:
    """文本阴影参数"""

    alpha: float
    """阴影不透明度, 取值范围为[0, 1]"""
    color: Tuple[float, float, float]
    """阴影颜色, RGB三元组, 取值范围为[0, 1]"""
    diffuse: float
    """阴影扩散程度, 此处定义与剪映中一致, 取值范围为[0, 100]"""
    distance: float
    """阴影距离, 取值范围为[0, 100]"""
    angle: float
    """阴影角度, 取值范围为[-180, 180]"""

    def __init__(self, *, alpha: float = 1.0, color: Tuple[float, float, float] = (0.0, 0.0, 0.0),
                 diffuse: float = 15.0, distance: float = 5.0, angle: float = -45.0):
        """
        Args:
            alpha (`float`, optional): 阴影不透明度, 取值范围为[0, 1], 默认为1.0
            color (`Tuple[float, float, float]`, optional): 阴影颜色, RGB三元组, 取值范围为[0, 1], 默认为黑色
            diffuse (`float`, optional): 阴影扩散程度, 此处定义与剪映中一致, 取值范围为[0, 100], 默认为15.0
            distance (`float`, optional): 阴影距离, 取值范围为[0, 100], 默认为5.0
            angle (`float`, optional): 阴影角度, 取值范围为[-180, 180], 默认为-45.0
        """
        self.alpha = alpha
        self.color = color
        self.diffuse = diffuse
        self.distance = distance
        self.angle = angle

    def export_json(self) -> Dict[str, Any]:
        return {
            "diffuse": self.diffuse / 100.0 / 6,  # /6是剪映自带的映射
            "alpha": self.alpha,
            "distance": self.distance,
            "content": {
                "solid": {
                    "color": list(self.color),
                }
            },
            "angle": self.angle
        }

class TextSegment(VisualSegment):
    """文本片段类, 目前仅支持设置基本的字体样式"""

    text: str
    """文本内容"""
    font: Optional[EffectMeta]
    """字体类型"""
    style: TextStyle
    """字体样式"""

    border: Optional[TextBorder]
    """文本描边参数, None表示无描边"""
    background: Optional[TextBackground]
    """文本背景参数, None表示无背景"""
    shadow: Optional[TextShadow]
    """文本阴影参数, None表示无阴影"""

    bubble: Optional[TextBubble]
    """文本气泡效果, 在放入轨道时加入素材列表中"""
    effect: Optional[TextEffect]
    """文本花字效果, 在放入轨道时加入素材列表中, 目前仅支持一部分花字效果"""
    extra_styles: List[Dict[str, Any]]
    """额外的文本样式，用于关键词高亮等特殊样式"""

    def __init__(self, text: str, timerange: Timerange, *,
                 font: Optional[FontType] = None,
                 style: Optional[TextStyle] = None, clip_settings: Optional[ClipSettings] = None,
                 border: Optional[TextBorder] = None, background: Optional[TextBackground] = None,
                 shadow: Optional[TextShadow] = None):
        """创建文本片段, 并指定其时间信息、字体样式及图像调节设置

        片段创建完成后, 可通过`ScriptFile.add_segment`方法将其添加到轨道中

        Args:
            text (`str`): 文本内容
            timerange (`Timerange`): 片段在轨道上的时间范围
            font (`Font_type`, optional): 字体类型, 默认为系统字体
            style (`TextStyle`, optional): 字体样式, 包含大小/颜色/对齐/透明度等.
            clip_settings (`ClipSettings`, optional): 图像调节设置, 默认不做任何变换
            border (`TextBorder`, optional): 文本描边参数, 默认无描边
            background (`TextBackground`, optional): 文本背景参数, 默认无背景
            shadow (`TextShadow`, optional): 文本阴影参数, 默认无阴影
        """
        super().__init__(uuid.uuid4().hex, None, timerange, 1.0, 1.0, False, clip_settings=clip_settings)

        self.text = text
        self.font = font.value if font else None
        self.style = style or TextStyle()
        self.border = border
        self.background = background
        self.shadow = shadow

        self.bubble = None
        self.effect = None
        self.extra_styles = []
        # 为 True 时 export 使用 extra_styles 作为完整 styles（互不重叠分区），不再叠加全量 base_style
        self.use_extra_styles_only = False

        # 剪映文本片段的 extra_material_refs 指向 sticker_animation，而非 speed
        self.animations_instance = SegmentAnimations()
        self.extra_material_refs = [self.animations_instance.animation_id]

    @classmethod
    def create_from_template(cls, text: str, timerange: Timerange, template: "TextSegment") -> "TextSegment":
        """根据模板创建新的文本片段, 并指定其文本内容"""
        new_segment = cls(text, timerange, style=deepcopy(template.style), clip_settings=deepcopy(template.clip_settings),
                          border=deepcopy(template.border), background=deepcopy(template.background),
                          shadow=deepcopy(template.shadow))
        new_segment.font = deepcopy(template.font)

        # 处理动画等
        if template.animations_instance:
            new_segment.animations_instance = deepcopy(template.animations_instance)
            new_segment.animations_instance.animation_id = uuid.uuid4().hex
            # 替换默认空动画引用，避免重复挂载
            new_segment.extra_material_refs = [new_segment.animations_instance.animation_id]
        if template.bubble:
            new_segment.add_bubble(template.bubble.effect_id, template.bubble.resource_id)
        if template.effect:
            new_segment.add_effect(template.effect.effect_id)

        return new_segment

    def add_animation(self, animation_type: Union[TextIntro, TextOutro, TextLoopAnim],
                      duration: Union[str, float, int, None] = None) -> "TextSegment":
        """将给定的入场/出场/循环动画添加到此片段的动画列表中, 出入场动画的持续时间可以自行设置.

        循环动画为剪映中的「循环」类型: ``duration`` 表示**单次循环**时长（微秒）, 与 ``get_text_animations``
        里 loop 的 ``duration`` 一致; 未指定时使用该动画元数据默认值. 循环从**入场结束之后**开始,
        至出场之前结束, 中间时段由剪映按该时长重复播放.

        注意: 若希望同时使用循环动画和入出场动画, 请**先添加出入场动画再添加循环动画**

        Args:
            animation_type (`TextIntro`, `TextOutro` or `TextLoopAnim`): 文本动画类型.
            duration (`str`, `int`, `float`, optional): 微秒; 字符串则调用 ``tim()`` 解析.
                对入场/出场为各自动画段时长; 对循环动画为单次循环时长.
        """
        if duration is None:
            duration = animation_type.value.duration
        duration = min(tim(duration), self.target_timerange.duration)

        if isinstance(animation_type, TextIntro):
            start = 0
        elif isinstance(animation_type, TextOutro):
            start = self.target_timerange.duration - duration
        elif isinstance(animation_type, TextLoopAnim):
            intro_trange = self.animations_instance and self.animations_instance.get_animation_trange("in")
            outro_trange = self.animations_instance and self.animations_instance.get_animation_trange("out")
            start = intro_trange.end if intro_trange else 0
            outro_dur = outro_trange.duration if outro_trange else 0
            available = self.target_timerange.duration - start - outro_dur
            cycle = duration
            span_cap = max(1, available)
            duration = max(1, min(cycle, span_cap))
        else:
            raise TypeError("Invalid animation type %s" % type(animation_type))

        if self.animations_instance is None:
            self.animations_instance = SegmentAnimations()
            self.extra_material_refs.append(self.animations_instance.animation_id)

        self.animations_instance.add_animation(Text_animation(animation_type, start, duration))

        return self

    def add_bubble(self, effect_id: str, resource_id: str) -> "TextSegment":
        """根据素材信息添加气泡效果, 相应素材信息可通过`ScriptFile.inspect_material`从模板中获取

        Args:
            effect_id (`str`): 气泡效果的effect_id
            resource_id (`str`): 气泡效果的resource_id
        """
        self.bubble = TextBubble(effect_id, resource_id)
        self.extra_material_refs.append(self.bubble.global_id)
        return self

    def add_effect(self, effect_id: str) -> "TextSegment":
        """根据素材信息添加花字效果, 相应素材信息可通过`ScriptFile.inspect_material`从模板中获取

        Args:
            effect_id (`str`): 花字效果的effect_id, 也同时是其resource_id
        """
        self.effect = TextEffect(effect_id, effect_id)
        self.extra_material_refs.append(self.effect.global_id)
        return self

    def export_json(self) -> Dict[str, Any]:
        """导出轨道片段 JSON，对齐剪映官方文本片段字段。"""
        json_dict = super().export_json()
        json_dict.update({
            "caption_info": None,
            "cartoon": False,
            "enable_adjust": False,
            "enable_lut": False,
            "group_id": "",
            "hdr_settings": None,
            "intensifies_audio": False,
            "is_placeholder": False,
            "responsive_layout": {
                "enable": False,
                "horizontal_pos_layout": 0,
                "size_layout": 0,
                "target_follow": "",
                "vertical_pos_layout": 0,
            },
            "template_id": "",
            "template_scene": "default",
        })
        return json_dict

    def export_material(self) -> Dict[str, Any]:
        """与此文本片段联系的素材，字段对齐剪映官方草稿以便二次编辑。"""
        check_flag: int = 7
        if self.border:
            check_flag |= 8
        if self.background:
            check_flag |= 16

        if self.use_extra_styles_only and self.extra_styles:
            styles = list(self.extra_styles)
        else:
            base_style: Dict[str, Any] = {
                "fill": {
                    "content": {
                        "solid": {
                            "color": list(self.style.color)
                        }
                    }
                },
                "range": [0, _style_range_end(self.text)],
                "size": self.style.size,
            }
            # 仅在启用时写出格式位，贴近官方草稿精简结构
            if self.style.bold:
                base_style["bold"] = True
            if self.style.italic:
                base_style["italic"] = True
            if self.style.underline:
                base_style["underline"] = True
            if self.border:
                base_style["strokes"] = [self.border.export_json()]
            styles = [base_style] + self.extra_styles

        has_style_shadows = any(
            isinstance(style, dict) and bool(style.get("shadows"))
            for style in styles
        )
        if self.shadow or has_style_shadows:
            check_flag |= 32

        content_json = {
            "styles": styles,
            "text": self.text
        }
        if styles:
            font_json = _font_content_json(self.font)
            for style in content_json["styles"]:
                if isinstance(style, dict) and "font" not in style:
                    style["font"] = dict(font_json)
            if self.effect:
                content_json["styles"][0]["effectStyle"] = {
                    "id": self.effect.effect_id,
                    "path": "C:"  # 花字占位路径，剪映会自行解析
                }
            if self.shadow:
                content_json["styles"][0]["shadows"] = [self.shadow.export_json()]

        # 保证 styles 中 font 键顺序贴近官方：fill → font → size → range
        normalized_styles: List[Dict[str, Any]] = []
        for style in content_json["styles"]:
            if not isinstance(style, dict):
                continue
            ordered: Dict[str, Any] = {}
            for key in ("fill", "font", "size", "range"):
                if key in style:
                    ordered[key] = style[key]
            for key, value in style.items():
                if key not in ordered:
                    ordered[key] = value
            normalized_styles.append(ordered)
        content_json["styles"] = normalized_styles

        shadow_alpha = 0.9
        shadow_angle = -45.0
        shadow_color = ""
        shadow_distance = 5.0
        shadow_smoothing = 0.45
        if self.shadow:
            shadow_alpha = self.shadow.alpha
            shadow_angle = self.shadow.angle
            shadow_color = _rgb_to_hex(self.shadow.color)
            shadow_distance = self.shadow.distance
            shadow_smoothing = self.shadow.diffuse / 100.0 * 3.0  # 15 → 0.45

        border_color = ""
        border_alpha = 1.0
        border_width = 0.08
        if self.border:
            border_color = _rgb_to_hex(self.border.color)
            border_alpha = self.border.alpha
            border_width = self.border.width

        fonts_list: List[Dict[str, Any]] = []
        font_path = "D:"
        font_resource_id = ""
        if self.font:
            font_resource_id = self.font.resource_id
            fonts_list.append(_build_fonts_material_entry(self.font))

        ret: Dict[str, Any] = {
            "add_type": 0,
            "alignment": self.style.align,
            "background_alpha": 1.0,
            "background_color": "",
            "background_height": 0.14,
            "background_horizontal_offset": 0.0,
            "background_round_radius": 0.0,
            "background_style": 0,
            "background_vertical_offset": 0.0,
            "background_width": 0.14,
            "base_content": "",
            "bold_width": 0.0,
            "border_alpha": border_alpha,
            "border_color": border_color,
            "border_width": border_width,
            "caption_template_info": {
                "category_id": "",
                "category_name": "",
                "effect_id": "",
                "is_new": False,
                "path": "",
                "request_id": "",
                "resource_id": "",
                "resource_name": "",
                "source_platform": 0,
            },
            "check_flag": check_flag,
            "combo_info": {"text_templates": []},
            "content": json.dumps(content_json, ensure_ascii=False),
            "fixed_height": -1.0,
            "fixed_width": -1.0,
            "font_category_id": "",
            "font_category_name": "",
            "font_id": "",
            "font_name": "",
            "font_path": font_path,
            "font_resource_id": font_resource_id,
            "font_size": self.style.size,
            "font_source_platform": 0,
            "font_team_id": "",
            "font_title": "none",
            "font_url": "",
            "fonts": fonts_list,
            "force_apply_line_max_width": False,
            "global_alpha": self.style.alpha,
            "group_id": "",
            "has_shadow": bool(self.shadow or has_style_shadows),
            "id": self.material_id,
            "initial_scale": 1.0,
            "inner_padding": -1.0,
            "is_rich_text": False,
            "italic_degree": 0,
            "ktv_color": "",
            "language": "",
            "layer_weight": 1,
            "letter_spacing": self.style.letter_spacing * 0.05,
            "line_feed": 1,
            "line_max_width": self.style.max_line_width,
            "line_spacing": 0.02 + self.style.line_spacing * 0.05,
            "multi_language_current": "none",
            "name": "",
            "original_size": [],
            "preset_category": "",
            "preset_category_id": "",
            "preset_has_set_alignment": False,
            "preset_id": "",
            "preset_index": 0,
            "preset_name": "",
            "recognize_task_id": "",
            "recognize_type": 0,
            "relevance_segment": [],
            "shadow_alpha": shadow_alpha,
            "shadow_angle": shadow_angle,
            "shadow_color": shadow_color,
            "shadow_distance": shadow_distance,
            "shadow_point": _shadow_point(shadow_angle, shadow_distance),
            "shadow_smoothing": shadow_smoothing,
            "shape_clip_x": False,
            "shape_clip_y": False,
            "source_from": "",
            "style_name": "",
            "sub_type": 0,
            "subtitle_keywords": None,
            "subtitle_template_original_fontsize": 0,
            "text_alpha": self.style.alpha,
            "text_color": _rgb_to_hex(self.style.color),
            "text_curve": None,
            "text_preset_resource_id": "",
            "text_size": 30,
            "text_to_audio_ids": [],
            "tts_auto_update": False,
            # 官方手动添加字幕使用 type=text（非 subtitle），否则二次编辑兼容性差
            "type": "text",
            "typesetting": int(self.style.vertical),
            "underline": bool(self.style.underline),
            "underline_offset": 0.22,
            "underline_width": 0.05,
            "use_effect_default_color": True,
            "words": {
                "end_time": [],
                "start_time": [],
                "text": [],
            },
        }

        if self.background:
            ret.update(self.background.export_json())

        return ret
