"""验证 add_captions 的发光（剪映「发光」文字效果）功能，以及对普通字幕的零影响。

草稿结构参照剪映实际导出的 发光/draft_content.json：该草稿有三条默认文本，
默认文本1 是普通字幕，默认文本2 加了「外发光」，默认文本3 加了「轮廓光」。

对比带发光的文本素材与普通字幕，差异**只有 check_flag**（7 → 71，即 7 | 64）；
发光本身是 materials.effects 里一条 type="bloom" 的素材，由文本片段的
extra_material_refs 引用（追加在 sticker_animation 之后）。与气泡一样，
发光的 effect_id 与 resource_id **不是同一个值**；又比气泡多一个 bloom_params
（颜色/强度/范围/方向），各预设的取值不同。
"""

from __future__ import annotations

import json
import os

import pytest

from config import PROJECT_ROOT
from src.pyJianYingDraft import ScriptFile, TrackType
from src.pyJianYingDraft.text_segment import DEFAULT_BLOOM_PARAMS
from src.service.add_captions import add_caption_to_draft
from src.service.get_text_glows import resolve_text_glow

GLOW_CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "glow.json")

# 取自 发光 草稿实证的两个预设
OUTER_NAME = "外发光"
OUTER_EFFECT_ID = "9762443"
OUTER_RESOURCE_ID = "7202576698775179837"
OUTER_BLOOM_PARAMS = {"color": "#FFFFFF", "dir_x": 0.5, "dir_y": 0.5, "range": 0.2, "strength": 0.3}

RIM_NAME = "轮廓光"
RIM_EFFECT_ID = "9762325"
RIM_RESOURCE_ID = "7202575978646737469"
RIM_BLOOM_PARAMS = {"color": "#ffffff", "dir_x": 0.5, "dir_y": 0.5, "range": 0.4, "strength": 0.5}

CATALOG = {
    OUTER_NAME: (OUTER_EFFECT_ID, OUTER_RESOURCE_ID, OUTER_BLOOM_PARAMS),
    RIM_NAME: (RIM_EFFECT_ID, RIM_RESOURCE_ID, RIM_BLOOM_PARAMS),
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
    segment = list(script.tracks.values())[0].segments[-1]
    return text_id, segment


def _text_material(script, text_id):
    return next(item for item in script.materials.texts if item["id"] == text_id)


def _glow_materials(script):
    """取出草稿导出结果里全部发光素材"""
    effects = json.loads(script.dumps())["materials"]["effects"]
    return [effect for effect in effects if effect["type"] == "bloom"]


def _glow_material(script):
    glows = _glow_materials(script)
    assert len(glows) == 1
    return glows[0]


# --------------------------------------------------------------------------- #
# 解析器
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("name", list(CATALOG))
def test_resolve_by_name(name: str):
    effect_id, resource_id, bloom_params = CATALOG[name]
    resolved = resolve_text_glow(name)

    assert resolved is not None
    assert resolved["effect_id"] == effect_id
    assert resolved["resource_id"] == resource_id
    assert resolved["name"] == name
    assert resolved["panel_id"] == "text_glow"
    assert resolved["bloom_params"] == bloom_params


@pytest.mark.parametrize("name", list(CATALOG))
def test_resolve_by_resource_id_and_effect_id(name: str):
    effect_id, resource_id, _ = CATALOG[name]

    for identifier in (resource_id, effect_id):
        resolved = resolve_text_glow(identifier)
        assert resolved is not None
        assert resolved["name"] == name
        assert resolved["effect_id"] == effect_id
        assert resolved["resource_id"] == resource_id


def test_resolve_explicit_pair_outside_catalog():
    """清单外的发光用 "effect_id:resource_id" 显式 ID 对，bloom_params 落到默认值"""
    resolved = resolve_text_glow("123456:9876543210987654321")

    assert resolved is not None
    assert resolved["effect_id"] == "123456"
    assert resolved["resource_id"] == "9876543210987654321"
    assert resolved["name"] == ""
    assert resolved["panel_id"] == "text_glow"
    # 剪映不会按 resource_id 重新推导颜色/强度/范围，故用实证过的默认值兜底
    assert resolved["bloom_params"] == DEFAULT_BLOOM_PARAMS
    assert resolved["extra_material"] == {}


def test_resolve_tolerates_surrounding_whitespace():
    assert resolve_text_glow(f"  {OUTER_NAME}  ")["name"] == OUTER_NAME
    assert resolve_text_glow(f" {OUTER_EFFECT_ID}:{OUTER_RESOURCE_ID} ")["resource_id"] == OUTER_RESOURCE_ID


def test_resolve_does_not_pass_through_bare_numeric_id():
    """只给一个数字无法补全另一个 id（发光与气泡同理），不透传"""
    assert resolve_text_glow(OUTER_EFFECT_ID) is not None  # 清单内有
    assert resolve_text_glow("999999999") is None          # 清单外的不透传


@pytest.mark.parametrize("identifier", [None, "", "   ", 123, [], {}, "a:b:c", ":x", "x:", "不存在的光效"])
def test_resolve_invalid_identifiers(identifier):
    assert resolve_text_glow(identifier) is None


def test_catalog_contains_both_verified_presets():
    with open(GLOW_CONFIG_PATH, "r", encoding="utf-8") as f:
        entries = json.load(f)

    assert len(entries) == 2
    for name, (effect_id, resource_id, bloom_params) in CATALOG.items():
        entry = next(item for item in entries if item["title"] == name)
        # id 即 resource_id，与 effect_id 不是同一个值
        assert entry["id"] == resource_id
        assert entry["effect_id"] == effect_id
        assert entry["id"] != entry["effect_id"]
        assert entry["bloom_params"] == bloom_params
        assert entry["panel_id"] == "text_glow"


# --------------------------------------------------------------------------- #
# 草稿结构
# --------------------------------------------------------------------------- #

def test_glow_material_structure():
    script = _build_script()
    text_id, segment = _add_caption(script, text_glow=OUTER_NAME)
    glow = _glow_material(script)

    assert glow["type"] == "bloom"
    assert glow["panel_id"] == "text_glow"
    assert glow["value"] == 0.0            # 气泡是 1.0，发光是 0.0
    assert glow["effect_id"] == OUTER_EFFECT_ID
    assert glow["resource_id"] == OUTER_RESOURCE_ID
    assert glow["name"] == OUTER_NAME
    assert glow["bloom_params"] == OUTER_BLOOM_PARAMS
    # 本机缓存相关字段由剪映自行拉取，不导出
    assert "path" not in glow
    # 片段通过 extra_material_refs 引用，且追加在 sticker_animation 之后
    assert segment.extra_material_refs == [segment.animations_instance.animation_id, glow["id"]]


def test_glow_sets_check_flag_bit_64():
    script = _build_script()
    text_id, _ = _add_caption(script, text_glow=OUTER_NAME)

    assert _text_material(script, text_id)["check_flag"] == 7 | 64 == 71


@pytest.mark.parametrize("name", list(CATALOG))
def test_glow_uses_catalog_bloom_params(name: str):
    script = _build_script()
    _add_caption(script, text_glow=name)

    assert _glow_material(script)["bloom_params"] == CATALOG[name][2]


def test_explicit_pair_uses_default_bloom_params():
    script = _build_script()
    _add_caption(script, text_glow="123456:9876543210987654321")
    glow = _glow_material(script)

    assert glow["effect_id"] == "123456"
    assert glow["resource_id"] == "9876543210987654321"
    assert glow["bloom_params"] == DEFAULT_BLOOM_PARAMS
    # name 未知时不写该键
    assert "name" not in glow


def test_glow_does_not_touch_text_styling():
    """除 check_flag 外，带发光的文本素材与普通字幕逐字段相同"""
    plain_script = _build_script()
    plain_id, _ = _add_caption(plain_script)
    plain = _text_material(plain_script, plain_id)

    glow_script = _build_script()
    glow_id, _ = _add_caption(glow_script, text_glow=OUTER_NAME)
    glowed = _text_material(glow_script, glow_id)

    ignored = {"id", "check_flag"}
    assert {k: v for k, v in glowed.items() if k not in ignored} == \
           {k: v for k, v in plain.items() if k not in ignored}


def test_each_caption_gets_its_own_glow_material():
    """整批字幕各自挂一条发光素材，id 互不相同（与剪映草稿一致）"""
    script = _build_script()
    _add_caption(script, text_glow=OUTER_NAME)
    _add_caption(script, caption_extra={"start": 3_000_000, "end": 6_000_000, "text": "第二行"}, text_glow=OUTER_NAME)

    glows = _glow_materials(script)
    assert len(glows) == 2
    assert glows[0]["id"] != glows[1]["id"]


# --------------------------------------------------------------------------- #
# 与其它文字效果共存（发光不互斥）
# --------------------------------------------------------------------------- #

def test_glow_stacks_with_background():
    script = _build_script()
    text_id, _ = _add_caption(script, text_glow=OUTER_NAME, has_background=True)
    material = _text_material(script, text_id)

    assert material["check_flag"] == 7 | 16 | 64 == 87
    assert material["background_style"] == 1
    assert len(_glow_materials(script)) == 1


def test_glow_stacks_with_bubble():
    script = _build_script()
    _, segment = _add_caption(script, text_glow=OUTER_NAME, text_bubble="背景装饰54")
    effects = json.loads(script.dumps())["materials"]["effects"]

    kinds = sorted(effect["type"] for effect in effects)
    assert kinds == ["bloom", "text_shape"]
    # 两条素材都在引用列表里，互不覆盖
    assert segment.extra_material_refs[0] == segment.animations_instance.animation_id
    assert len(segment.extra_material_refs) == 3
    assert segment.bubble.global_id in segment.extra_material_refs
    assert segment.glow.global_id in segment.extra_material_refs


def test_glow_not_suppressed_by_text_template():
    """发光挂在 extra_material_refs 上，不掌管素材身份，故模板生效时仍保留"""
    script = _build_script()
    _, segment = _add_caption(script, text_glow=OUTER_NAME, text_template="我的水印")

    assert segment.text_template is not None
    assert segment.glow is not None
    assert len(_glow_materials(script)) == 1


def test_glow_survives_keyword_highlight():
    script = _build_script()
    text_id, _ = _add_caption(
        script,
        caption_extra={"keyword": "字幕", "keyword_color": "#ff7100"},
        text_glow=OUTER_NAME,
    )

    assert _text_material(script, text_id)["check_flag"] == 7 | 64
    assert len(_glow_materials(script)) == 1


# --------------------------------------------------------------------------- #
# 不回归
# --------------------------------------------------------------------------- #

def test_plain_caption_unchanged():
    """不传 text_glow 时不产生任何发光素材，check_flag 仍为 7"""
    script = _build_script()
    text_id, _ = _add_caption(script)

    assert _glow_materials(script) == []
    assert _text_material(script, text_id)["check_flag"] == 7


@pytest.mark.parametrize("identifier", ["不存在的光效", "999999999", "a:b:c"])
def test_unresolvable_glow_falls_back_to_plain_caption(identifier: str):
    script = _build_script()
    text_id, _ = _add_caption(script, text_glow=identifier)

    assert _glow_materials(script) == []
    assert _text_material(script, text_id)["check_flag"] == 7


def test_mixed_batch_keeps_plain_caption_byte_identical():
    """批量调用里，未解析到发光的字幕其文本素材与普通字幕完全一致"""
    reference_script = _build_script()
    reference_id, _ = _add_caption(reference_script)
    reference = _text_material(reference_script, reference_id)

    script = _build_script()
    _add_caption(script, text_glow=OUTER_NAME)
    # 同一批里的第二条：文本与参照字幕相同，只是发光解析失败
    _add_caption(
        script,
        caption_extra={"start": 3_000_000, "end": 6_000_000},
        text_glow="不存在的光效",
    )
    plain = list(script.materials.texts)[1]

    ignored = {"id"}
    assert {k: v for k, v in plain.items() if k not in ignored} == \
           {k: v for k, v in reference.items() if k not in ignored}
