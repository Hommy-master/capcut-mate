"""验证 add_captions.line_max_width：超长字幕写入草稿后可按行宽自动换行。"""

from __future__ import annotations

import json

from src.pyJianYingDraft import ScriptFile, TrackType
from src.schemas.add_captions import AddCaptionsRequest
from src.service.add_captions import add_caption_to_draft

# 故意超长，超过常见画布宽度，用于验证换行相关字段被正确写入
LONG_TEXT = (
    "我研究这些水清村的土壤的 AI 工具能够帮助我加快对它的微生物的一个研究，"
    "同时还会把采样点坐标、湿度、酸碱度与菌群丰度一并写入实验记录，"
    "方便后续在剪映草稿里用超长字幕验证自动换行是否按 line_max_width 生效。"
)


def _add_long_caption(*, line_max_width: float, transform_y: float = -1000.0):
    script = ScriptFile(width=1080, height=1920, fps=30, maintrack_adsorb=False)
    script.add_track(TrackType.text, "caption_track")
    caption = {
        "start": 0,
        "end": 5_000_000,
        "text": LONG_TEXT,
        "font_size": 8,
    }
    _, text_id, _ = add_caption_to_draft(
        script,
        "caption_track",
        caption=caption,
        text_color="#ffffff",
        border_color="#1a1a1a",
        alignment=1,
        font="得意黑",
        font_size=8,
        bold=True,
        line_max_width=line_max_width,
        transform_y=transform_y,
    )
    material = next(item for item in script.materials.texts if item["id"] == text_id)
    return script, material


def test_schema_default_line_max_width():
    req = AddCaptionsRequest(
        draft_url="https://example.com/?draft_id=demo",
        captions="[]",
    )
    assert req.line_max_width == 0.82


def test_long_caption_writes_line_max_width_and_force_apply():
    """超长字幕：line_max_width 落盘，且开启自动换行时 force_apply=true。"""
    _, material = _add_long_caption(line_max_width=0.82)

    content = json.loads(material["content"])
    assert content["text"] == LONG_TEXT
    assert len(LONG_TEXT) > 40

    assert material["line_max_width"] == 0.82
    assert material["force_apply_line_max_width"] is True
    assert material["line_feed"] == 1


def test_long_caption_custom_line_max_width_values():
    """不同 line_max_width 应原样写入素材（窄/默认/宽）。"""
    cases = (0.45, 0.82, 0.95)
    for width in cases:
        _, material = _add_long_caption(line_max_width=width, transform_y=-200.0)
        assert material["line_max_width"] == width
        assert material["force_apply_line_max_width"] is True
        assert json.loads(material["content"])["text"] == LONG_TEXT
