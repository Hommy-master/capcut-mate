"""验证 add_captions 的「文字背景」（剪映字幕文字底下的纯色底板）功能。

草稿结构参照剪映实际导出的 背景/draft_content.json：该草稿有两条默认文本，
只有第二条开了背景。对比 materials.texts[0] 与 [1]，差异恰好只有三个字段：

    background_style:  0 → 1
    background_color:  "" → "#000000"
    check_flag:        7 → 23   (= 7 | 16)

其余 background_* 字段（alpha 1.0、height/width 0.14、round_radius 0.0、
offset 0.0）两段完全相同，即剪映的默认值。背景不透明度/圆角/宽高都不做单位换算，
background_color 也按原始 "#RRGGBB" 字符串写出（不像描边/阴影那样转成 RGB 三元组）。
"""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from src.pyJianYingDraft import ScriptFile, TrackType
from src.schemas.add_captions import TextBackgroundInfo
from src.service.add_captions import add_caption_to_draft

# 参照草稿 背景/draft_content.json 中「默认文本2」（唯一一条带背景的字幕）的原值
REFERENCE_BACKGROUND = {
    "background_alpha": 1.0,
    "background_color": "#000000",
    "background_height": 0.14,
    "background_horizontal_offset": 0.0,
    "background_round_radius": 0.0,
    "background_style": 1,
    "background_vertical_offset": 0.0,
    "background_width": 0.14,
}
# 同草稿中「默认文本1」（无背景）的原值
REFERENCE_NO_BACKGROUND = {
    "background_alpha": 1.0,
    "background_color": "",
    "background_height": 0.14,
    "background_horizontal_offset": 0.0,
    "background_round_radius": 0.0,
    "background_style": 0,
    "background_vertical_offset": 0.0,
    "background_width": 0.14,
}


def _build_script():
    script = ScriptFile(width=1920, height=1080, fps=30, maintrack_adsorb=False)
    script.add_track(TrackType.text, "caption_track")
    return script


def _add_caption(script, caption_extra=None, **kwargs):
    caption = {"start": 0, "end": 3_000_000, "text": "第一行字幕"}
    caption.update(caption_extra or {})
    call_kwargs = {"alignment": 1, "font_size": 15}
    call_kwargs.update(kwargs)
    _, text_id, _ = add_caption_to_draft(script, "caption_track", caption=caption, **call_kwargs)
    material = next(item for item in script.materials.texts if item["id"] == text_id)
    return text_id, material


def _background_fields(material):
    """取出导出结果里全部 background_* 字段"""
    return {key: value for key, value in material.items() if key.startswith("background_")}


# --------------------------------------------------------------------------- #
# 开关语义
# --------------------------------------------------------------------------- #

def test_background_off_by_default():
    """默认不启用背景，导出与参照草稿的无背景字幕逐字段一致，check_flag 仍为 7"""
    _, material = _add_caption(_build_script())

    assert _background_fields(material) == REFERENCE_NO_BACKGROUND
    assert material["check_flag"] == 7


def test_background_info_ignored_when_switch_off():
    """只传 background_info 而不开 has_background 时不生效（与 has_shadow 一致）"""
    _, material = _add_caption(
        _build_script(),
        has_background=False,
        background_info=TextBackgroundInfo(background_color="#ff0000"),
    )

    assert _background_fields(material) == REFERENCE_NO_BACKGROUND
    assert material["check_flag"] == 7


def test_default_background_matches_reference_draft():
    """has_background=True 且不给 background_info 时，即参照草稿的默认黑色背景"""
    _, material = _add_caption(_build_script(), has_background=True)

    assert _background_fields(material) == REFERENCE_BACKGROUND
    assert material["check_flag"] == 23


# --------------------------------------------------------------------------- #
# 字段映射
# --------------------------------------------------------------------------- #

def test_custom_background_values_are_written_verbatim():
    """除颜色大小写外，接口取值原样落进草稿的 background_* 字段"""
    _, material = _add_caption(
        _build_script(),
        has_background=True,
        background_info=TextBackgroundInfo(
            background_color="#ff7100",
            background_alpha=0.5,
            background_round_radius=0.3,
            background_height=0.2,
            background_width=0.35,
        ),
    )

    assert material["background_color"] == "#FF7100"
    assert material["background_alpha"] == 0.5
    assert material["background_round_radius"] == 0.3
    assert material["background_height"] == 0.2
    assert material["background_width"] == 0.35
    # 未指定的字段保持剪映默认值
    assert material["background_style"] == 1
    assert material["background_horizontal_offset"] == 0.0
    assert material["background_vertical_offset"] == 0.0


@pytest.mark.parametrize("offset", [-1.0, -0.3, 0.0, 0.1, 0.3, 0.5, 1.0])
def test_offset_round_trips_without_float_noise(offset: float):
    """偏移量接口与草稿同为 [-1, 1]（0 居中），须逐位相等，不能有 *2-1 往返噪声"""
    _, material = _add_caption(
        _build_script(),
        has_background=True,
        background_info=TextBackgroundInfo(
            background_horizontal_offset=offset,
            background_vertical_offset=offset,
        ),
    )

    assert material["background_horizontal_offset"] == offset
    assert material["background_vertical_offset"] == offset


def test_bare_hex_without_hash_and_case_are_normalized():
    """颜色不带 # 或大小写混用都能归一为草稿使用的 "#RRGGBB" """
    _, material = _add_caption(
        _build_script(),
        has_background=True,
        background_info=TextBackgroundInfo(background_color="00ff7f"),
    )

    assert material["background_color"] == "#00FF7F"


@pytest.mark.parametrize(
    "color",
    [
        "bogus",
        "",           # 空字符串
        "#fff",       # 缩写形式
        "#fffffff",   # 长度超了
        "#gggggg",    # 非十六进制字符
        "0x1234",     # int(s, 16) 会接受这种写法，须逐字符校验
        "#0x1234",
    ],
)
def test_invalid_hex_falls_back_to_black(color: str):
    """颜色非法时回退黑色并告警——背景色不经 RGB 转换，非法值会原样落进草稿"""
    _, material = _add_caption(
        _build_script(),
        has_background=True,
        background_info=TextBackgroundInfo(background_color=color),
    )

    assert material["background_color"] == "#000000"


# --------------------------------------------------------------------------- #
# check_flag 位组合
# --------------------------------------------------------------------------- #

def test_check_flag_combines_with_border_and_shadow():
    """check_flag 基值 7，描边 |= 8、背景 |= 16、阴影 |= 32，可叠加"""
    _, material = _add_caption(
        _build_script(),
        has_background=True,
        border_color="#000000",
        has_shadow=True,
    )

    assert material["check_flag"] == 7 | 8 | 16 | 32


def test_check_flag_background_and_shadow_only():
    _, material = _add_caption(_build_script(), has_background=True, has_shadow=True)

    assert material["check_flag"] == 7 | 16 | 32


# --------------------------------------------------------------------------- #
# 与其它文字效果共存
# --------------------------------------------------------------------------- #

def test_background_survives_text_template():
    """套用文字模板时背景仍然保留：模板素材与文本素材是两条独立素材"""
    script = _build_script()
    _, material = _add_caption(script, has_background=True, text_template="我的水印")

    assert _background_fields(material) == REFERENCE_BACKGROUND
    # 模板素材自身不带 background_* 字段，背景不会被重复套用
    dumped = json.loads(script.dumps())
    assert len(dumped["materials"]["text_templates"]) == 1
    assert not [k for k in dumped["materials"]["text_templates"][0] if k.startswith("background_")]


def test_background_survives_keyword_highlight():
    """关键词高亮走 styles 分区，不影响素材侧的 background_*"""
    _, material = _add_caption(
        _build_script(),
        caption_extra={"keyword": "字幕", "keyword_color": "#ff7100"},
        has_background=True,
    )

    assert _background_fields(material) == REFERENCE_BACKGROUND
    assert material["check_flag"] == 23


def test_caption_material_still_matches_jianying_with_background():
    """开背景后素材仍是 type=text 的普通字幕素材，其余关键字段不受影响"""
    _, material = _add_caption(_build_script(), has_background=True)

    assert material["type"] == "text"
    assert material["text_color"] == "#FFFFFF"
    assert material["font_size"] == 15
    assert material["content"]
    assert json.loads(material["content"])["text"] == "第一行字幕"


# --------------------------------------------------------------------------- #
# 参数校验
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "kwargs",
    [
        {"background_style": 0},          # 0 表示无背景，应改用 has_background=False
        {"background_style": 3},
        {"background_alpha": 1.5},
        {"background_alpha": -0.1},
        {"background_round_radius": 1.5},
        {"background_height": 1.5},
        {"background_width": -0.1},
        {"background_horizontal_offset": 1.5},
        {"background_vertical_offset": -1.5},
    ],
)
def test_out_of_range_values_are_rejected(kwargs):
    with pytest.raises(ValidationError):
        TextBackgroundInfo(**kwargs)


def test_defaults_match_reference_draft():
    """TextBackgroundInfo 的默认值即参照草稿里那条带背景字幕的原值"""
    assert TextBackgroundInfo().model_dump() == REFERENCE_BACKGROUND
