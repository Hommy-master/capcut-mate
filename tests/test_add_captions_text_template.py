"""验证 add_captions 的文字模板（文字模板）功能，以及对普通字幕的零影响。

草稿结构参考剪映实际导出的 draft_content.json：套用文字模板时，片段的
material_id 指向 materials.text_templates 中的模板素材，文本素材则改由模板的
text_info_resources[].text_material_id 反向关联。
"""

from __future__ import annotations

import json

from src.pyJianYingDraft import ScriptFile, TrackType
from src.service.add_captions import add_caption_to_draft
from src.service.get_text_templates import resolve_text_template

TEMPLATE_NAME = "嘎嘎香！红色 简约 美食 情绪表达 字幕"
TEMPLATE_ID = "7383613902744980770"


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
    segment = list(script.tracks.values())[0].segments[-1]
    return text_id, segment


# --------------------------------------------------------------------------- #
# 解析器
# --------------------------------------------------------------------------- #

def test_resolve_by_name_and_id():
    by_name = resolve_text_template(TEMPLATE_NAME)
    assert by_name is not None
    assert by_name["effect_id"] == TEMPLATE_ID
    assert by_name["resource_id"] == TEMPLATE_ID
    assert by_name["name"] == TEMPLATE_NAME
    assert by_name["category_id"] == "10577"
    assert by_name["category_name"] == "热门"

    by_id = resolve_text_template(TEMPLATE_ID)
    assert by_id is not None
    assert by_id["effect_id"] == TEMPLATE_ID
    assert by_id["name"] == TEMPLATE_NAME


def test_resolve_numeric_passthrough_and_unknown():
    # 不在映射表中的纯数字 id 直接透传
    passthrough = resolve_text_template("1234567890123456789")
    assert passthrough is not None
    assert passthrough["effect_id"] == "1234567890123456789"
    assert passthrough["name"] == ""

    # 非数字且未命中映射表
    assert resolve_text_template("不存在的文字模板") is None
    # 非法输入不应抛异常
    assert resolve_text_template("") is None
    assert resolve_text_template(None) is None
    assert resolve_text_template(123) is None


# --------------------------------------------------------------------------- #
# 模板字幕的草稿结构
# --------------------------------------------------------------------------- #

def test_text_template_material_structure():
    script = _build_script()
    text_id, segment = _add_caption(script, text_template=TEMPLATE_ID)

    assert len(script.materials.text_templates) == 1
    template = script.materials.text_templates[0]

    # 模板素材基本字段
    assert template["type"] == "text_template"
    assert template["version"] == "1.0.0"
    assert template["effect_id"] == TEMPLATE_ID
    assert template["resource_id"] == TEMPLATE_ID
    assert template["name"] == TEMPLATE_NAME
    assert template["category_id"] == "10577"
    assert template["category_name"] == "热门"
    assert template["check_flag"] == 7
    assert template["platform"] == "all"
    assert template["source_platform"] == 1
    assert template["non_text_info_resources"] == []
    assert template["resources"] == []

    # 片段指向模板素材，而非文本素材
    seg_json = segment.export_json()
    assert seg_json["material_id"] == template["id"]
    assert seg_json["material_id"] != text_id

    # 文本素材仍在 materials.texts，且只能由模板反向关联
    text_material = next(item for item in script.materials.texts if item["id"] == text_id)
    assert text_material["id"] == text_id
    assert text_material["use_effect_default_color"] is False
    assert text_material["text_color"] == ""

    # 模板 -> 文本素材 的关联
    resources = template["text_info_resources"]
    assert len(resources) == 1
    assert resources[0]["text_material_id"] == text_id
    assert resources[0]["extra_material_refs"] == seg_json["extra_material_refs"]
    assert resources[0]["attach_info"]["duration"] == 3_000_000
    assert resources[0]["attach_info"]["start_time"] == 0


def test_text_template_via_name_and_per_caption():
    # 接口级默认值
    script = _build_script()
    _, segment = _add_caption(script, text_template=TEMPLATE_NAME)
    assert segment.export_json()["material_id"] == script.materials.text_templates[0]["id"]

    # 逐条覆盖接口级默认值
    script = _build_script()
    _, segment = _add_caption(
        script,
        caption_extra={"text_template": TEMPLATE_NAME},
        text_template="1234567890123456789",
    )
    template = script.materials.text_templates[0]
    assert template["effect_id"] == TEMPLATE_ID
    assert segment.export_json()["material_id"] == template["id"]


def test_unresolvable_template_falls_back_to_plain_caption():
    script = _build_script()
    text_id, segment = _add_caption(script, text_template="不存在的文字模板")

    assert script.materials.text_templates == []
    assert segment.export_json()["material_id"] == text_id
    material = next(item for item in script.materials.texts if item["id"] == text_id)
    assert material["use_effect_default_color"] is True
    assert material["text_color"] == "#FFFFFF"


# --------------------------------------------------------------------------- #
# 与花字互斥
# --------------------------------------------------------------------------- #

def test_text_template_takes_precedence_over_text_effect():
    script = _build_script()
    _, segment = _add_caption(
        script,
        text_template=TEMPLATE_ID,
        text_effect="白字橘色发光花字",
    )

    template = script.materials.text_templates[0]
    assert segment.export_json()["material_id"] == template["id"]
    # 花字素材不应被添加
    assert [f for f in script.materials.filters if f.export_json()["type"] == "text_effect"] == []


# --------------------------------------------------------------------------- #
# 不回归
# --------------------------------------------------------------------------- #

def test_plain_caption_unchanged():
    """未使用模板时，导出结果与既有实现完全一致。"""
    script = _build_script()
    text_id, segment = _add_caption(script)

    assert script.materials.text_templates == []
    assert segment.export_json()["material_id"] == text_id

    material = next(item for item in script.materials.texts if item["id"] == text_id)
    content = json.loads(material["content"])
    style = content["styles"][0]

    assert material["type"] == "text"
    assert material["text_color"] == "#FFFFFF"
    assert material["font_size"] == 15
    assert material["font_resource_id"] == ""
    assert material["fonts"] == []
    assert material["words"] == {"end_time": [], "start_time": [], "text": []}
    assert material["use_effect_default_color"] is True
    assert style["range"] == [0, 5]
    assert style["font"] == {"id": "", "path": "D:"}
    assert "strokes" not in style

    # 无模板草稿的导出仍为空数组
    assert json.loads(script.dumps())["materials"]["text_templates"] == []


def test_mixed_batch_keeps_plain_caption_intact():
    """一条普通 + 一条模板的混合批次：普通字幕不受影响。"""
    script = _build_script()
    plain_text_id, plain_segment = _add_caption(script)
    template_text_id, template_segment = _add_caption(
        script,
        caption_extra={"start": 3_000_000, "end": 6_000_000, "text": "第二条"},
        text_template=TEMPLATE_ID,
    )

    assert len(script.materials.text_templates) == 1
    assert len(script.materials.texts) == 2

    # 普通字幕依然被片段直接引用
    assert plain_segment.export_json()["material_id"] == plain_text_id
    plain_material = next(item for item in script.materials.texts if item["id"] == plain_text_id)
    assert plain_material["use_effect_default_color"] is True
    assert plain_material["text_color"] == "#FFFFFF"

    # 模板字幕引用模板素材
    template = script.materials.text_templates[0]
    assert template_segment.export_json()["material_id"] == template["id"]
    assert template["text_info_resources"][0]["text_material_id"] == template_text_id
    template_material = next(item for item in script.materials.texts if item["id"] == template_text_id)
    assert template_material["use_effect_default_color"] is False
