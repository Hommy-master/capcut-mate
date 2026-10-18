"""验证 add_captions 的气泡（剪映「气泡」文字效果）功能，以及对普通字幕的零影响。

草稿结构参照剪映实际导出的 气泡1/draft_content.json：气泡是 materials.effects 中的
一条 type="text_shape" 素材，由文本片段的 extra_material_refs 引用（追加在
sticker_animation 之后）。与花字/文字模板不同，气泡的 effect_id 与 resource_id
**不是同一个值**；气泡只提供文字底下的装饰底板，不改动文字自身的填充/描边/阴影。
"""

from __future__ import annotations

import json
import os

from config import PROJECT_ROOT
from src.pyJianYingDraft import ScriptFile, TrackType
from src.service.add_captions import add_caption_to_draft
from src.service.get_text_bubbles import resolve_text_bubble

BUBBLE_CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "bubble.json")

# 取自剪映草稿 气泡1：默认文本2 应用的气泡
BUBBLE_NAME = "背景装饰54"
BUBBLE_EFFECT_ID = "716434"
BUBBLE_RESOURCE_ID = "6821385652727190024"
BUBBLE_PAIR = f"{BUBBLE_EFFECT_ID}:{BUBBLE_RESOURCE_ID}"


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


def _bubble_material(script):
    """取出草稿导出结果里唯一的气泡素材"""
    effects = json.loads(script.dumps())["materials"]["effects"]
    shapes = [effect for effect in effects if effect["type"] == "text_shape"]
    assert len(shapes) == 1
    return shapes[0]


# --------------------------------------------------------------------------- #
# 解析器
# --------------------------------------------------------------------------- #

def test_resolve_by_name_and_ids():
    by_name = resolve_text_bubble(BUBBLE_NAME)
    assert by_name is not None
    assert by_name["effect_id"] == BUBBLE_EFFECT_ID
    assert by_name["resource_id"] == BUBBLE_RESOURCE_ID
    assert by_name["name"] == BUBBLE_NAME
    assert by_name["category_id"] == "bubble"
    assert by_name["category_name"] == "气泡"

    # resource_id 与 effect_id 都能定位到同一条
    for identifier in (BUBBLE_RESOURCE_ID, BUBBLE_EFFECT_ID):
        resolved = resolve_text_bubble(identifier)
        assert resolved is not None
        assert resolved["effect_id"] == BUBBLE_EFFECT_ID
        assert resolved["resource_id"] == BUBBLE_RESOURCE_ID


def test_resolve_explicit_pair_outside_catalog():
    """清单外的气泡用 "effect_id:resource_id" 显式 ID 对"""
    resolved = resolve_text_bubble("123456:9876543210987654321")
    assert resolved is not None
    assert resolved["effect_id"] == "123456"
    assert resolved["resource_id"] == "9876543210987654321"
    # 清单外的气泡没有名称与分类
    assert resolved["name"] == ""
    assert resolved["category_id"] == ""
    assert resolved["category_name"] == ""
    assert resolved["extra_material"] == {}


def test_explicit_pair_tolerates_surrounding_whitespace():
    resolved = resolve_text_bubble(f"  {BUBBLE_EFFECT_ID} : {BUBBLE_RESOURCE_ID}  ")
    assert resolved is not None
    assert resolved["effect_id"] == BUBBLE_EFFECT_ID
    assert resolved["resource_id"] == BUBBLE_RESOURCE_ID


def test_single_id_misses_catalog_is_not_passed_through():
    """气泡的 effect_id 与 resource_id 不同，只给一个数字无法补全另一个。

    这里与 text_template 的「纯数字直接透传」刻意不同：不做猜测，直接判为未找到，
    由调用方回退为普通字幕。
    """
    assert resolve_text_bubble("1111111111111111111") is None
    # 短数字 effect_id 不在清单中时同样不猜测
    assert resolve_text_bubble("999999") is None


def test_invalid_identifiers_return_none():
    # 冒号两侧任一为空、冒号数量不为 1，都不算合法的 ID 对
    for bad in ("", "   ", ":", "716434:", ":6821385652727190024", "a:b:c", 123456, None):
        assert resolve_text_bubble(bad) is None


def test_config_entries_are_complete():
    """清单项必须同时给出 id(resource_id) 与 effect_id，且两者不同值。"""
    entries = json.load(open(BUBBLE_CONFIG_PATH, encoding="utf-8"))
    assert entries

    for entry in entries:
        assert entry["id"].isdigit()
        assert entry["effect_id"].isdigit()
        # 气泡的 id 是 resource_id，与 effect_id 不同值（这点与花字/文字模板相反）
        assert entry["id"] != entry["effect_id"]
        assert entry["title"].strip()
        assert entry["category_name"].strip()

        resolved = resolve_text_bubble(entry["id"])
        assert resolved["effect_id"] == entry["effect_id"]

    # 草稿实证过的那个气泡必须在清单里，且能按名称/两个 id 反查
    verified = next(e for e in entries if e["title"] == BUBBLE_NAME)
    assert verified["id"] == BUBBLE_RESOURCE_ID
    assert verified["effect_id"] == BUBBLE_EFFECT_ID
    assert resolve_text_bubble(BUBBLE_EFFECT_ID)["resource_id"] == BUBBLE_RESOURCE_ID


# --------------------------------------------------------------------------- #
# 气泡字幕的草稿结构
# --------------------------------------------------------------------------- #

def test_bubble_material_structure():
    script = _build_script()
    text_id, segment = _add_caption(script, text_bubble=BUBBLE_NAME)

    bubble = _bubble_material(script)
    assert bubble["type"] == "text_shape"
    assert bubble["effect_id"] == BUBBLE_EFFECT_ID
    assert bubble["resource_id"] == BUBBLE_RESOURCE_ID
    assert bubble["name"] == BUBBLE_NAME
    assert bubble["category_id"] == "bubble"
    assert bubble["category_name"] == "气泡"
    assert bubble["apply_target_type"] == 0
    assert bubble["value"] == 1.0

    # 片段通过 extra_material_refs 引用气泡，追加在 sticker_animation 之后
    refs = segment.export_json()["extra_material_refs"]
    assert refs[-1] == bubble["id"]
    assert len(refs) == 2

    # 气泡字幕仍是普通文本片段：material_id 指向文本素材
    assert segment.export_json()["material_id"] == text_id


def test_bubble_does_not_touch_text_styling():
    """气泡只加装饰底板，不重置文字颜色/描边/阴影（这点与花字相反）。"""
    script = _build_script()
    text_id, _ = _add_caption(
        script,
        text_bubble=BUBBLE_NAME,
        text_color="#123456",
        border_color="#ff0000",
        has_shadow=True,
    )

    material = next(item for item in script.materials.texts if item["id"] == text_id)
    content = json.loads(material["content"])
    style = content["styles"][0]

    assert material["text_color"] == "#123456"
    assert material["use_effect_default_color"] is True
    assert style["fill"]["content"]["solid"]["color"] != [1.0, 1.0, 1.0]
    assert "strokes" in style
    shadow = json.loads(script.dumps())["materials"]["texts"][0]["has_shadow"]
    assert shadow is True


def test_bubble_via_explicit_pair_and_per_caption():
    # 接口级默认值（清单外气泡）
    script = _build_script()
    _, segment = _add_caption(script, text_bubble=BUBBLE_PAIR)
    bubble = _bubble_material(script)
    assert bubble["effect_id"] == BUBBLE_EFFECT_ID
    assert bubble["resource_id"] == BUBBLE_RESOURCE_ID
    assert segment.export_json()["extra_material_refs"][-1] == bubble["id"]

    # 逐条覆盖接口级默认值
    script = _build_script()
    _, segment = _add_caption(
        script,
        caption_extra={"text_bubble": BUBBLE_NAME},
        text_bubble="111:999",
    )
    bubble = _bubble_material(script)
    assert bubble["effect_id"] == BUBBLE_EFFECT_ID
    assert segment.export_json()["extra_material_refs"][-1] == bubble["id"]


def test_unresolvable_bubble_falls_back_to_plain_caption():
    script = _build_script()
    text_id, segment = _add_caption(script, text_bubble="不存在的很长的气泡名称")

    effects = json.loads(script.dumps())["materials"]["effects"]
    assert [e for e in effects if e["type"] == "text_shape"] == []

    # 只有 sticker_animation 一个引用，与普通字幕一致
    assert len(segment.export_json()["extra_material_refs"]) == 1
    assert segment.export_json()["material_id"] == text_id


# --------------------------------------------------------------------------- #
# 与花字 / 文字模板的优先级：文字模板 > 气泡 > 花字
# --------------------------------------------------------------------------- #

def test_bubble_takes_precedence_over_text_effect():
    script = _build_script()
    _, segment = _add_caption(
        script,
        text_bubble=BUBBLE_NAME,
        text_effect="白字橘色发光花字",
    )

    bubble = _bubble_material(script)
    assert segment.export_json()["extra_material_refs"][-1] == bubble["id"]

    # 花字素材不应被添加
    effects = json.loads(script.dumps())["materials"]["effects"]
    assert [e for e in effects if e["type"] == "text_effect"] == []

    # 气泡生效时不做花字那套颜色重置，文字样式保持用户给定值
    material = next(item for item in script.materials.texts if item["id"] == segment.material_id)
    assert material["text_color"] == "#FFFFFF"
    assert material["use_effect_default_color"] is True


def test_text_template_takes_precedence_over_bubble():
    template_id = "7383613902744980770"
    script = _build_script()
    _, segment = _add_caption(script, text_template=template_id, text_bubble=BUBBLE_NAME)

    # 片段指向模板素材
    template = script.materials.text_templates[0]
    assert segment.export_json()["material_id"] == template["id"]
    assert template["effect_id"] == template_id

    # 模板优先时不写气泡素材
    effects = json.loads(script.dumps())["materials"]["effects"]
    assert [e for e in effects if e["type"] == "text_shape"] == []


# --------------------------------------------------------------------------- #
# 不回归
# --------------------------------------------------------------------------- #

def test_plain_caption_unchanged():
    """未使用气泡时，导出结果里不含任何 text_shape 素材。"""
    script = _build_script()
    text_id, segment = _add_caption(script)

    effects = json.loads(script.dumps())["materials"]["effects"]
    assert [e for e in effects if e["type"] == "text_shape"] == []

    assert len(segment.export_json()["extra_material_refs"]) == 1
    material = next(item for item in script.materials.texts if item["id"] == text_id)
    assert material["use_effect_default_color"] is True
    assert material["text_color"] == "#FFFFFF"


def test_mixed_batch_keeps_plain_caption_intact():
    """一条普通 + 一条气泡的混合批次：普通字幕不受影响。"""
    script = _build_script()
    plain_text_id, plain_segment = _add_caption(script)
    bubble_text_id, bubble_segment = _add_caption(
        script,
        caption_extra={"start": 3_000_000, "end": 6_000_000, "text": "第二条字幕"},
        text_bubble=BUBBLE_NAME,
    )

    assert len(script.materials.texts) == 2

    # 普通字幕没有气泡引用
    assert len(plain_segment.export_json()["extra_material_refs"]) == 1
    plain_material = next(item for item in script.materials.texts if item["id"] == plain_text_id)
    bubble_material = next(item for item in script.materials.texts if item["id"] == bubble_text_id)

    # 两条文本素材除文本内容外完全一致：气泡没有改动任何文字样式
    assert plain_material["content"] == bubble_material["content"].replace("第二条字幕", "第一行字幕")
    assert plain_material["use_effect_default_color"] is True
    assert bubble_material["use_effect_default_color"] is True

    # 只有气泡字幕引用气泡素材
    bubble = _bubble_material(script)
    assert bubble_segment.export_json()["extra_material_refs"][-1] == bubble["id"]
