"""验证 add_captions 的描边不透明度（border_alpha）与宽度（border_width）。

描边宽度对外沿用剪映 UI 的 0-100 语义，落到草稿时换算为 0-0.2
（与 pyJianYingDraft.TextBorder 的换算一致）；不透明度直接取 0-1。
关键词描边与普通描边共用这两个接口级取值。
"""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from src.pyJianYingDraft import ScriptFile, TrackType
from src.schemas.add_captions import AddCaptionsRequest
from src.service.add_captions import add_caption_to_draft, _border_width_to_draft

DEFAULT_DRAFT_WIDTH = 0.08  # 40 / 100 * 0.2，改动前的写死值


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
    return material


def _styles(material):
    return json.loads(material["content"])["styles"]


def test_border_defaults_keep_previous_output():
    """不传新参数时，描边仍是 1.0 / 0.08，与改动前逐值一致"""
    material = _add_caption(_build_script(), border_color="#000000")
    stroke = _styles(material)[0]["strokes"][0]

    assert material["border_alpha"] == 1.0
    assert material["border_width"] == pytest.approx(DEFAULT_DRAFT_WIDTH)
    assert stroke["content"]["solid"]["alpha"] == 1.0
    assert stroke["width"] == pytest.approx(DEFAULT_DRAFT_WIDTH)


def test_custom_border_alpha_and_width():
    """接口取值落到素材级 border_alpha/border_width 与 styles[].strokes"""
    material = _add_caption(
        _build_script(),
        border_color="#ff0000",
        border_alpha=0.35,
        border_width=75,
    )
    stroke = _styles(material)[0]["strokes"][0]

    assert material["border_alpha"] == 0.35
    assert material["border_width"] == pytest.approx(_border_width_to_draft(75))
    assert stroke["content"]["solid"]["alpha"] == 0.35
    assert stroke["width"] == pytest.approx(_border_width_to_draft(75))


def test_border_params_ignored_without_border_color():
    """不传描边颜色时不会凭空产生描边，也不会写出 strokes"""
    material = _add_caption(_build_script(), border_alpha=0.5, border_width=10)

    assert "strokes" not in _styles(material)[0]
    assert material["border_alpha"] == 1.0
    assert material["border_width"] == pytest.approx(DEFAULT_DRAFT_WIDTH)


def test_keyword_highlight_shares_border_alpha_and_width():
    """关键词高亮路径（无关键词阴影）的普通/关键词分区共用同一组描边参数"""
    material = _add_caption(
        _build_script(),
        caption_extra={
            "keyword": "字幕",
            "keyword_color": "#ff7100",
            "keyword_border_color": "#00ff00",
        },
        border_color="#000000",
        border_alpha=0.6,
        border_width=20,
    )
    styles = _styles(material)
    keyword_style = next(s for s in styles if s["range"] == [3, 5])
    stroke = keyword_style["strokes"][0]

    assert stroke["content"]["solid"]["alpha"] == 0.6
    assert stroke["width"] == pytest.approx(_border_width_to_draft(20))
    # 普通文字仍走素材级描边，两者参数同源
    assert material["border_alpha"] == 0.6
    assert material["border_width"] == pytest.approx(_border_width_to_draft(20))


def test_keyword_partitioned_styles_share_border_alpha_and_width():
    """关键词阴影走完整分区路径时，普通分区与关键词分区同样使用新参数"""
    material = _add_caption(
        _build_script(),
        caption_extra={
            "keyword": "字幕",
            "keyword_border_color": "#00ff00",
            "keyword_has_shadow": True,
        },
        border_color="#000000",
        border_alpha=0.4,
        border_width=90,
    )
    styles = _styles(material)
    keyword_style = next(s for s in styles if s["range"] == [3, 5])
    normal_style = next(s for s in styles if s["range"] == [0, 3])

    expected_width = pytest.approx(_border_width_to_draft(90))
    for style in (keyword_style, normal_style):
        stroke = style["strokes"][0]
        assert stroke["content"]["solid"]["alpha"] == 0.4
        assert stroke["width"] == expected_width


def test_border_width_conversion_matches_vendored_text_border():
    """对外 0-100 与草稿 0-0.2 的换算须与 TextBorder 内部保持一致"""
    for width in (0, 20, 40, 75, 100):
        assert _border_width_to_draft(width) == pytest.approx(width / 100.0 * 0.2)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"border_alpha": -0.1},
        {"border_alpha": 1.1},
        {"border_width": -1},
        {"border_width": 101},
    ],
)
def test_out_of_range_border_params_are_rejected(kwargs):
    with pytest.raises(ValidationError):
        AddCaptionsRequest(**kwargs)
