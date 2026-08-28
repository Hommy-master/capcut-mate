"""add_captions alignment：0/1/2 横排保持不变，3/4/5 映射为竖排。"""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from src.pyJianYingDraft import ScriptFile, TrackType
from src.schemas.add_captions import AddCaptionsRequest
from src.service.add_captions import (
    add_caption_to_draft,
    resolve_caption_alignment,
)


def _make_script(track_name: str = "caption_track") -> ScriptFile:
    script = ScriptFile(width=1920, height=1080, fps=30, maintrack_adsorb=False)
    script.add_track(TrackType.text, track_name)
    return script


def _add_and_export_material(alignment: int, *, caption_extra: dict | None = None, **kwargs):
    script = _make_script()
    caption = {"start": 0, "end": 1_000_000, "text": "你好世界"}
    if caption_extra:
        caption.update(caption_extra)
    _, text_id, _ = add_caption_to_draft(
        script,
        "caption_track",
        caption=caption,
        alignment=alignment,
        **kwargs,
    )
    material = next((item for item in script.materials.texts if item["id"] == text_id), None)
    assert material is not None
    return script, material


@pytest.mark.parametrize(
    "alignment, expected_align, expected_vertical",
    [
        (0, 0, False),
        (1, 1, False),
        (2, 2, False),
        (3, 1, True),
        (4, 0, True),
        (5, 2, True),
    ],
)
def test_resolve_caption_alignment_mapping(alignment, expected_align, expected_vertical):
    assert resolve_caption_alignment(alignment) == (expected_align, expected_vertical)


def test_resolve_caption_alignment_unknown_falls_back_to_horizontal_left():
    """与历史实现一致：无法识别的值回退为横排左对齐。"""
    assert resolve_caption_alignment(-1) == (0, False)
    assert resolve_caption_alignment(6) == (0, False)


@pytest.mark.parametrize(
    "alignment, expected_align, expected_typesetting",
    [
        (0, 0, 0),
        (1, 1, 0),
        (2, 2, 0),
        (3, 1, 1),
        (4, 0, 1),
        (5, 2, 1),
    ],
)
def test_add_caption_to_draft_writes_alignment_and_typesetting(
    alignment, expected_align, expected_typesetting
):
    _, material = _add_and_export_material(alignment)
    assert material["alignment"] == expected_align
    assert material["typesetting"] == expected_typesetting


def test_default_alignment_remains_center_horizontal():
    """默认 alignment=1：居中横排，不影响既有默认行为。"""
    _, material = _add_and_export_material(1)
    assert material["alignment"] == 1
    assert material["typesetting"] == 0
    assert material["type"] == "subtitle"


def test_horizontal_alignment_keeps_existing_style_fields():
    """0/1/2 不应改变字号、颜色、自动换行等既有样式。"""
    _, material = _add_and_export_material(
        0,
        text_color="#ff0000",
        font_size=22,
        underline=True,
        italic=True,
        bold=True,
    )
    content = json.loads(material["content"])
    base_style = content["styles"][0]

    assert material["alignment"] == 0
    assert material["typesetting"] == 0
    assert material["type"] == "subtitle"
    assert base_style["size"] == 22
    assert base_style["underline"] is True
    assert base_style["italic"] is True
    assert base_style["bold"] is True
    assert base_style["fill"]["content"]["solid"]["color"] == [1.0, 0.0, 0.0]


def test_vertical_alignment_does_not_break_font_size_or_wrapping():
    """3/4/5 只打开竖排，字号与自动换行保持原逻辑。"""
    _, material = _add_and_export_material(
        3,
        caption_extra={"font_size": 18},
        font_size=15,
    )
    content = json.loads(material["content"])
    base_style = content["styles"][0]

    assert material["alignment"] == 1
    assert material["typesetting"] == 1
    assert material["type"] == "subtitle"
    assert base_style["size"] == 18.0


def test_vertical_alignment_keeps_keyword_highlight():
    """竖排不应打断关键词高亮分区。"""
    _, material = _add_and_export_material(
        5,
        caption_extra={"keyword": "世界", "keyword_color": "#ff7100", "keyword_font_size": 20},
    )
    content = json.loads(material["content"])

    assert material["alignment"] == 2
    assert material["typesetting"] == 1
    assert len(content["styles"]) >= 2
    highlight = next(style for style in content["styles"] if style.get("size") == 20)
    assert highlight["range"] == [2, 4]


def test_schema_accepts_alignment_0_to_5():
    captions = json.dumps([{"start": 0, "end": 1000, "text": "hi"}])
    for value in range(6):
        req = AddCaptionsRequest(draft_url="http://x?draft_id=1", captions=captions, alignment=value)
        assert req.alignment == value


def test_schema_rejects_alignment_out_of_range():
    captions = json.dumps([{"start": 0, "end": 1000, "text": "hi"}])
    with pytest.raises(ValidationError):
        AddCaptionsRequest(draft_url="http://x?draft_id=1", captions=captions, alignment=6)
    with pytest.raises(ValidationError):
        AddCaptionsRequest(draft_url="http://x?draft_id=1", captions=captions, alignment=-1)
