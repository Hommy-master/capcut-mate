"""人像美化（skin/shape/makeup/body）目录、导出结构与服务行为测试。

目录期望值逐条来自剪映真实导出的对照草稿（10月5日-02/draft_content.json），
修改 beauty_meta.py 时若与真实草稿不符，这些用例应当失败。

接口字段名为英文（BeautyMeta.name）；写进草稿 name 字段的仍是剪映中文显示名
（BeautyMeta.draft_name），因此导出断言里出现的仍是中文。
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from pydantic import ValidationError

from src.pyJianYingDraft import ScriptFile, TrackType
from src.pyJianYingDraft.local_materials import VideoMaterial
from src.pyJianYingDraft.metadata.beauty_meta import (
    BEAUTY_CATALOG,
    GROUP_BODY,
    GROUP_MAKEUP,
    GROUP_SHAPE,
    GROUP_SKIN,
    MAKEUP_EXCLUSION_GROUP,
    MAKEUP_ROOT,
    SKIN_TONE_PRESETS,
    build_figure_algorithm_path,
    find_beauty_type,
    find_skin_tone,
)
from src.pyJianYingDraft.time_util import Timerange
from src.pyJianYingDraft.video_segment import FigureEffect, VideoSegment
from src.schemas.add_beauty import (
    AddBeautyRequest,
    BeautyBodyGroup,
    BeautyMakeupGroup,
    BeautyShapeGroup,
    BeautySkinGroup,
)
from src.service.add_beauty import add_beauty
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError


ALGO = build_figure_algorithm_path("PLACEHOLDER", "video-mat-1")

# (group, name, draft_name, resource_id, category_id, sub_type, intensity_mode,
#  needs_path, adjust_param_name, intensity_key)
GROUND_TRUTH = [
    # skin
    (GROUP_SKIN, "even", "匀肤", "7106322605304451614", "auto-beauty2", "auto_beauty", "adjust_param", True, "0", "face_adjust_yunfu"),
    (GROUP_SKIN, "plump", "丰盈", "7165761391037518350", "auto-beauty2", "auto_beauty", "adjust_param", True, "0", "face_adjust_fuling"),
    (GROUP_SKIN, "smooth", "磨皮", "6976822940608238093", "auto-beauty2", "auto_beauty", "value", True, "0", ""),
    (GROUP_SKIN, "dewrinkle", "祛法令纹", "7127560078508429831", "auto-beauty2", "auto_beauty", "adjust_param", True, "0", "face_adjust_NasolabialFolds"),
    (GROUP_SKIN, "bright_eye", "亮眼", "7210363411970921017", "auto-beauty2", "auto_beauty", "adjust_param", True, "0", "face_adjust_BrightEye"),
    (GROUP_SKIN, "dark_circle", "祛黑眼圈", "7127559798861599268", "auto-beauty2", "auto_beauty", "adjust_param", True, "0", "face_adjust_Pouch"),
    (GROUP_SKIN, "whitening", "美白", "6998408303826965006", "auto-beauty2", "none", "value", False, "0", ""),
    (GROUP_SKIN, "white_teeth", "白牙", "6998408263892996639", "auto-beauty2", "auto_beauty", "adjust_param", True, "0", ""),
    # shape
    (GROUP_SHAPE, "small_face", "小脸", "7325345220688613914", "auto-beauty", "auto_beauty", "adjust_param", True, "0", "face_adjust_YouTaiFace"),
    (GROUP_SHAPE, "slim", "瘦脸", "7126765507457323557", "auto-beauty", "auto_beauty", "adjust_param", True, "0", "face_adjust_TotalFace"),
    (GROUP_SHAPE, "v_shape", "V脸", "7358087335411454501", "auto-beauty", "auto_beauty", "adjust_param", True, "0", "face_adjust_VFace"),
    (GROUP_SHAPE, "jaw", "下颌骨", "7126764917918536199", "auto-beauty", "auto_beauty", "adjust_param", True, "0", "face_adjust_ZoomJawbone"),
    (GROUP_SHAPE, "cheekbone", "颧骨", "7127587811795931662", "auto-beauty", "auto_beauty", "adjust_param", True, "0", "face_adjust_ZoomCheekbone"),
    (GROUP_SHAPE, "shorten", "短脸", "7126865570653278751", "auto-beauty", "auto_beauty", "adjust_param", True, "0", "face_adjust_SmallFace"),
    (GROUP_SHAPE, "contour_smooth", "流畅脸", "7165761469231927838", "auto-beauty", "auto_beauty", "adjust_param", True, "0", "face_adjust_lunkuopinghua"),
    (GROUP_SHAPE, "lower", "下庭", "7130850220891443725", "auto-beauty", "auto_beauty", "adjust_param", True, "0", "face_adjust_lower_atrium"),
    (GROUP_SHAPE, "middle", "中庭", "7130850182488396325", "auto-beauty", "auto_beauty", "adjust_param", True, "0", "face_adjust_mid_atrium"),
    (GROUP_SHAPE, "upper", "上庭", "7130849819957924389", "auto-beauty", "auto_beauty", "adjust_param", True, "0", "face_adjust_upper_atrium"),
    (GROUP_SHAPE, "hairline", "发际线", "7126865429154238984", "auto-beauty", "auto_beauty", "adjust_param", True, "0", "face_adjust_Forehead"),
    # body
    (GROUP_BODY, "small_head", "小头", "6976812039847023111", "auto-beauty3", "none", "value", False, "0", "body_adjust_SmallHead"),
    (GROUP_BODY, "swan_neck", "天鹅颈", "7187453444146336313", "auto-beauty3", "none", "value", False, "0", "body_adjust_SwanNeck"),
    (GROUP_BODY, "slim_arm", "瘦手臂", "7187394795965256247", "auto-beauty3", "none", "value", False, "0", "body_adjust_SlimArm"),
    (GROUP_BODY, "straight_shoulder", "直角肩", "7246635041663488567", "auto-beauty3", "none", "value", False, "0", "body_adjust_OrthoShoulder"),
    (GROUP_BODY, "slim_body", "瘦身", "6976812219048661540", "auto-beauty3", "none", "value", False, "0", "body_adjust_SlimBody"),
    (GROUP_BODY, "slim_waist", "瘦腰", "6976812120591569416", "auto-beauty3", "none", "value", False, "0", "body_adjust_SlimWaist"),
    (GROUP_BODY, "long_leg", "长腿", "6956089104412971534", "auto-beauty3", "none", "value", False, "0", "body_adjust_StretchLeg"),
    (GROUP_BODY, "plump_breast", "丰胸", "7168288902728389157", "auto-beauty3", "none", "value", False, "0", "body_adjust_SlimBreast"),
    (GROUP_BODY, "slim_hip", "美胯", "7168289037562679838", "auto-beauty3", "none", "value", False, "0", "body_adjust_SlimHip"),
    (GROUP_BODY, "smooth", "磨皮", "7125729150572171812", "auto-beauty3", "none", "value", False, "0", ""),
    (GROUP_BODY, "whitening", "美白", "7125780457576206879", "auto-beauty3", "none", "value", False, "0", ""),
    # makeup（预设值即剪映妆容名，接口名与草稿显示名都是中文）
    (GROUP_MAKEUP, "淡人妆", "淡人妆", "7376172391774294554", "makeup", "exclusion_face", "face_adjust", True, "0", ""),
    (GROUP_MAKEUP, "氧气感", "氧气感", "7154258998315717150", "makeup", "exclusion_face", "face_adjust", True, "0", ""),
]


def _video_segment() -> VideoSegment:
    material = VideoMaterial(
        "https://example.com/demo.mp4",
        duration=5_000_000,
        width=1080,
        height=1920,
        material_type="video",
    )
    return VideoSegment(material, Timerange(0, 5_000_000))


def _effect(meta, intensity: float, cold_warm: float = 0.0, algorithm_path: str = "") -> dict:
    return FigureEffect(meta, intensity, cold_warm=cold_warm,
                        algorithm_artifact_path=algorithm_path).export_json()


def _make_draft(draft_id: str):
    """构造只含一个视频片段的草稿并放入缓存，返回 (script, segment)。"""
    script = ScriptFile(1080, 1920, 30, True)
    script.save = lambda: None  # type: ignore[method-assign]
    script.add_track(TrackType.video)
    seg = _video_segment()
    script.add_material(seg.material_instance)
    script.add_segment(seg)
    DRAFT_CACHE[draft_id] = script
    return script, seg


# ===== 目录（ground truth）=====

@pytest.mark.parametrize(
    "group,name,draft_name,resource_id,category_id,sub_type,mode,needs_path,param_name,intensity_key",
    GROUND_TRUTH,
    ids=[f"{item[0]}-{item[1]}" for item in GROUND_TRUTH],
)
def test_catalog_matches_reference_draft(group, name, draft_name, resource_id, category_id, sub_type,
                                         mode, needs_path, param_name, intensity_key):
    meta = find_beauty_type(group, name)
    assert meta is not None, f"{group}/{name} 未在目录中"
    assert meta.draft_name == draft_name
    assert meta.resource_id == resource_id
    assert meta.category_id == category_id
    assert meta.sub_type == sub_type
    assert meta.intensity_mode == mode
    assert meta.needs_algorithm_path is needs_path
    assert meta.adjust_param_name == param_name
    assert meta.intensity_key == intensity_key


def test_catalog_resource_ids_are_unique():
    ids = [meta.resource_id for group in BEAUTY_CATALOG.values() for meta in group.values() if meta.supported]
    ids += [meta.resource_id for meta in SKIN_TONE_PRESETS.values()]
    assert len(ids) == len(set(ids))


def test_schema_fields_match_catalog():
    # 滑杆组：schema 字段去掉「预设选择 / 预设参数」后必须与目录一一对应
    extras = {
        GROUP_SKIN: {"skin_tone", "temperature", "intensity"},
        GROUP_SHAPE: set(),
        GROUP_BODY: set(),
    }
    schema_fields = {
        GROUP_SKIN: set(BeautySkinGroup.model_fields),
        GROUP_SHAPE: set(BeautyShapeGroup.model_fields),
        GROUP_BODY: set(BeautyBodyGroup.model_fields),
    }
    for group in (GROUP_SKIN, GROUP_SHAPE, GROUP_BODY):
        assert schema_fields[group] - extras[group] == set(BEAUTY_CATALOG[group]), group

    # 美妆组：目录里是套装预设，schema 用 look 字段选择
    assert set(BeautyMakeupGroup.model_fields) == {"look", "intensity"}
    assert set(BEAUTY_CATALOG[GROUP_MAKEUP]) == {"淡人妆", "氧气感"}


def test_reserved_sliders_have_no_resource_id():
    for group, name in ((GROUP_SHAPE, "width"), (GROUP_SHAPE, "chin_length"), (GROUP_BODY, "wide_shoulder")):
        meta = find_beauty_type(group, name)
        assert meta is not None and meta.supported is False
        assert meta.resource_id == ""


def test_skin_tone_presets():
    assert find_skin_tone("冷白").resource_id == "7148720872105185800"
    assert find_skin_tone("暖白").resource_id == "7148720647714116132"
    assert find_skin_tone("小麦") is None


def test_makeup_exclusion_group_is_the_11_item_list():
    assert list(MAKEUP_EXCLUSION_GROUP) == [
        "face_adjust_brow", "face_adjust_eyeshadow", "face_adjust_eyeline",
        "face_adjust_eyelash", "face_adjust_pupil", "face_adjust_eyelight",
        "face_adjust_stereo", "face_adjust_blusher", "face_adjust_lip",
        "face_adjust_mask", "face_adjust_highlight",
    ]


# ===== 导出结构 =====

def test_value_mode_uses_top_level_value():
    meta = find_beauty_type(GROUP_BODY, "small_head")
    data = _effect(meta, 33)
    assert data["value"] == pytest.approx(0.33)
    assert data["adjust_params"] == []
    assert data["sub_type"] == "none"
    assert data["category_id"] == "auto-beauty3"
    assert data["intensity_key"] == "body_adjust_SmallHead"
    assert data["algorithm_artifact_path"] == ""


def test_skin_value_mode_and_no_path():
    data = _effect(find_beauty_type(GROUP_SKIN, "smooth"), 52, algorithm_path=ALGO)
    assert data["value"] == pytest.approx(0.52)
    assert data["algorithm_artifact_path"] == ALGO

    whitening = _effect(find_beauty_type(GROUP_SKIN, "whitening"), 67, algorithm_path=ALGO)
    assert whitening["value"] == pytest.approx(0.67)
    assert whitening["sub_type"] == "none"
    assert whitening["algorithm_artifact_path"] == ""  # 美白不需要算法路径


def test_adjust_param_mode():
    data = _effect(find_beauty_type(GROUP_SKIN, "even"), 21, algorithm_path=ALGO)
    assert data["value"] == 0.0
    assert data["adjust_params"] == [{"default_value": 0.0, "name": "0", "value": pytest.approx(0.21)}]
    assert data["intensity_key"] == "face_adjust_yunfu"
    assert data["category_id"] == "auto-beauty2"


def test_teeth_adjust_param_name_is_zero():
    """回归：真实草稿里白牙的 adjust_params.name 是 "0"（旧实现误写为 "1"）。"""
    data = _effect(find_beauty_type(GROUP_SKIN, "white_teeth"), 41, algorithm_path=ALGO)
    assert data["adjust_params"][0]["name"] == "0"
    assert data["adjust_params"][0]["value"] == pytest.approx(0.41)


def test_shape_slider_uses_shape_category():
    data = _effect(find_beauty_type(GROUP_SHAPE, "small_face"), 19, algorithm_path=ALGO)
    assert data["category_id"] == "auto-beauty"
    assert data["intensity_key"] == "face_adjust_YouTaiFace"
    assert data["adjust_params"][0] == {"default_value": 0.0, "name": "0", "value": pytest.approx(0.19)}
    assert data["algorithm_artifact_path"] == ALGO


def test_skin_tone_cold_warm_divides_by_99():
    data = _effect(SKIN_TONE_PRESETS["冷白"], 60, cold_warm=11)
    assert data["sub_type"] == "exclusion"
    assert data["value"] == 0.0
    assert data["exclusion_group"] == ["face_adjust_skin"]
    assert data["algorithm_artifact_path"] == ""
    params = data["face_adjust_params"][0]
    assert params["face_id"] == "-1" and params["enable"] is True
    assert params["adjust_params"] == [
        {"default_value": 0.0, "name": "face_adjust_skin_ColdWarm", "value": pytest.approx(11 / 99)},
        {"default_value": 0.0, "name": "face_adjust_skin_Intensity", "value": pytest.approx(0.6)},
    ]


def test_skin_tone_warm_defaults_cold_warm_to_zero():
    data = _effect(SKIN_TONE_PRESETS["暖白"], 60)
    assert data["resource_id"] == "7148720647714116132"
    by_name = {item["name"]: item["value"] for item in data["face_adjust_params"][0]["adjust_params"]}
    assert by_name["face_adjust_skin_ColdWarm"] == pytest.approx(0.0)
    assert by_name["face_adjust_skin_Intensity"] == pytest.approx(0.6)


@pytest.mark.parametrize("name,face_id", [("淡人妆", "1"), ("氧气感", "0")])
def test_makeup_material_shape(name, face_id):
    data = _effect(find_beauty_type(GROUP_MAKEUP, name), 80, algorithm_path=ALGO)
    assert data["category_id"] == "makeup"
    assert data["sub_type"] == "exclusion_face"
    assert data["value"] == 0.0
    assert data["adjust_params"] == []
    assert list(data["exclusion_group"]) == list(MAKEUP_EXCLUSION_GROUP)
    assert data["algorithm_artifact_path"] == ALGO
    assert data["face_adjust_params"] == [{
        "adjust_params": [{"default_value": 0.0, "name": "face_adjust_whole", "value": pytest.approx(0.8)}],
        "disable_part": [],
        "enable": True,
        "face_id": face_id,
    }]


def test_makeup_root_shape():
    data = FigureEffect(MAKEUP_ROOT, 0.0, algorithm_artifact_path=ALGO).export_json()
    assert data["name"] == "makeup-root"
    assert data["type"] == "makeup_root"
    assert data["resource_id"] == "7273096354098844221"
    assert data["category_id"] == ""
    assert data["value"] == 0.0


def test_same_name_in_skin_and_body_are_distinct_materials():
    seg = _video_segment()
    skin = seg.add_beauty(find_beauty_type(GROUP_SKIN, "smooth"), 52)
    body = seg.add_beauty(find_beauty_type(GROUP_BODY, "smooth"), 19)
    assert skin is not body
    assert skin.meta.resource_id != body.meta.resource_id
    assert seg.extra_material_refs.count(skin.global_id) == 1
    assert seg.extra_material_refs.count(body.global_id) == 1


def test_add_beauty_updates_in_place():
    seg = _video_segment()
    first = seg.add_beauty(find_beauty_type(GROUP_SKIN, "whitening"), 60)
    second = seg.add_beauty(find_beauty_type(GROUP_SKIN, "whitening"), 30)
    assert first is second
    assert second.intensity == pytest.approx(0.3)
    assert seg.extra_material_refs.count(first.global_id) == 1

    skin = seg.add_beauty(SKIN_TONE_PRESETS["冷白"], 60, cold_warm=11)
    seg.add_beauty(SKIN_TONE_PRESETS["冷白"], 90, cold_warm=99)
    assert skin.cold_warm == pytest.approx(1.0)
    assert skin.intensity == pytest.approx(0.9)
    assert seg.extra_material_refs.count(skin.global_id) == 1


def test_makeup_root_added_once():
    seg = _video_segment()
    first = seg.ensure_makeup_root(ALGO)
    second = seg.ensure_makeup_root(ALGO)
    assert first is second
    assert seg.extra_material_refs.count(first.global_id) == 1


# ===== 服务层 =====

def test_groups_are_written_in_order_and_exported_into_effects():
    script, seg = _make_draft("beauty-order")
    try:
        _, affected, figure_ids = add_beauty(
            draft_url="http://localhost/get_draft?draft_id=beauty-order",
            segment_ids=[seg.segment_id],
            skin={"smooth": 52, "skin_tone": "冷白", "temperature": 11, "intensity": 60},
            shape={"small_face": 19},
            makeup={"look": "淡人妆"},
            body={"small_head": 33},
        )
        assert affected == [seg.segment_id]

        content = json.loads(script.dumps())
        effects = content["materials"]["effects"]
        # 草稿内 name 仍是剪映中文显示名，顺序为 skin → shape → makeup → body → makeup-root
        assert [item["name"] for item in effects] == ["磨皮", "冷白", "小脸", "淡人妆", "小头", "makeup-root"]
        assert content["materials"]["video_effects"] == []

        refs = content["tracks"][0]["segments"][0]["extra_material_refs"]
        for figure_id in figure_ids:
            assert refs.count(figure_id) == 1
    finally:
        DRAFT_CACHE.pop("beauty-order", None)


def test_update_in_place_keeps_material_id():
    script, seg = _make_draft("beauty-update")
    try:
        url = "http://localhost/get_draft?draft_id=beauty-update"
        add_beauty(draft_url=url, segment_ids=[seg.segment_id], skin={"whitening": 60})
        first_id = json.loads(script.dumps())["materials"]["effects"][0]["id"]

        add_beauty(draft_url=url, segment_ids=[seg.segment_id], skin={"whitening": 40})
        effects = json.loads(script.dumps())["materials"]["effects"]
        assert len(effects) == 2  # 美白 + makeup-root
        assert effects[0]["id"] == first_id
        assert effects[0]["value"] == pytest.approx(0.4)
    finally:
        DRAFT_CACHE.pop("beauty-update", None)


@pytest.mark.parametrize("group,data,name", [
    (GROUP_SHAPE, {"width": 10}, "width"),
    (GROUP_SHAPE, {"chin_length": 10}, "chin_length"),
    (GROUP_BODY, {"wide_shoulder": 10}, "wide_shoulder"),
])
def test_reserved_slider_nonzero_rejected(group, data, name):
    script, seg = _make_draft("beauty-reserved")
    try:
        kwargs = {"shape": data} if group == GROUP_SHAPE else {"body": data}
        with pytest.raises(CustomException) as ei:
            add_beauty(
                draft_url="http://localhost/get_draft?draft_id=beauty-reserved",
                segment_ids=[seg.segment_id],
                **kwargs,
            )
        assert ei.value.err == CustomError.BEAUTY_NOT_FOUND
        assert name in str(ei.value.detail)
        assert json.loads(script.dumps())["materials"]["effects"] == []  # 未被部分写入
    finally:
        DRAFT_CACHE.pop("beauty-reserved", None)


def test_zero_values_and_empty_preset_are_skipped():
    script, seg = _make_draft("beauty-zero")
    try:
        add_beauty(
            draft_url="http://localhost/get_draft?draft_id=beauty-zero",
            segment_ids=[seg.segment_id],
            skin={"smooth": 0, "whitening": 67, "skin_tone": ""},
        )
        names = [item["name"] for item in json.loads(script.dumps())["materials"]["effects"]]
        assert names == ["美白", "makeup-root"]
    finally:
        DRAFT_CACHE.pop("beauty-zero", None)


def test_no_effective_params_raises():
    _make_draft("beauty-empty")
    try:
        with pytest.raises(CustomException) as ei:
            add_beauty(
                draft_url="http://localhost/get_draft?draft_id=beauty-empty",
                segment_ids=["s1"],
                skin={"skin_tone": ""},
            )
        assert ei.value.err == CustomError.INVALID_BEAUTY_INFO
    finally:
        DRAFT_CACHE.pop("beauty-empty", None)


def test_unknown_preset_raises():
    _make_draft("beauty-preset")
    try:
        for kwargs in ({"skin": {"skin_tone": "小麦"}}, {"makeup": {"look": "裸妆"}}):
            with pytest.raises(CustomException) as ei:
                add_beauty(
                    draft_url="http://localhost/get_draft?draft_id=beauty-preset",
                    segment_ids=["s1"],
                    **kwargs,
                )
            assert ei.value.err == CustomError.BEAUTY_NOT_FOUND
    finally:
        DRAFT_CACHE.pop("beauty-preset", None)


@pytest.mark.parametrize("data", [{"Mopi": 52}, {"磨皮": 52}])
def test_unknown_key_rejected_for_direct_calls(data):
    """中文键已废弃：磨皮 现在是 smooth，旧写法必须被拒绝而不是静默忽略。"""
    _make_draft("beauty-unknown")
    try:
        with pytest.raises(CustomException) as ei:
            add_beauty(
                draft_url="http://localhost/get_draft?draft_id=beauty-unknown",
                segment_ids=["s1"],
                skin=data,
            )
        assert ei.value.err == CustomError.BEAUTY_NOT_FOUND
    finally:
        DRAFT_CACHE.pop("beauty-unknown", None)


def test_slim_hip_writes_meikua_material():
    """"美膀" 别名已随改名合并进 slim_hip，直接传 slim_hip 即可。"""
    script, seg = _make_draft("beauty-hip")
    try:
        add_beauty(
            draft_url="http://localhost/get_draft?draft_id=beauty-hip",
            segment_ids=[seg.segment_id],
            body={"slim_hip": 30},
        )
        effects = json.loads(script.dumps())["materials"]["effects"]
        assert effects[0]["name"] == "美胯"
        assert effects[0]["value"] == pytest.approx(0.3)
    finally:
        DRAFT_CACHE.pop("beauty-hip", None)


# ===== Schema =====

def test_schema_ranges_and_unknown_keys():
    with pytest.raises(ValidationError):
        BeautySkinGroup(smooth=101)
    with pytest.raises(ValidationError):
        BeautySkinGroup(temperature=100)  # temperature 范围为 0-99
    with pytest.raises(ValidationError):
        BeautyShapeGroup(slim=-1)
    with pytest.raises(ValidationError):
        BeautyBodyGroup(not_a_slider=10)  # extra=forbid
    with pytest.raises(ValidationError):
        BeautySkinGroup(磨皮=52)  # extra=forbid，中文键不再接受
    assert BeautySkinGroup().intensity == 60
    assert BeautyMakeupGroup().intensity == 80
    assert BeautyMakeupGroup().look == ""


def test_request_groups_are_optional():
    req = AddBeautyRequest(draft_url="u", segment_ids=["s"])
    assert req.skin is None and req.shape is None and req.makeup is None and req.body is None


# ===== 还原度验收 =====

def test_reference_draft_fidelity():
    """按 10月5日-02 的全部取值构造一次请求，逐条比对素材 id 与强度。"""
    script, seg = _make_draft("beauty-fidelity")
    try:
        add_beauty(
            draft_url="http://localhost/get_draft?draft_id=beauty-fidelity",
            segment_ids=[seg.segment_id],
            skin={
                "even": 21, "plump": 30, "smooth": 52, "dewrinkle": 38, "bright_eye": 29,
                "dark_circle": 57, "whitening": 67, "white_teeth": 41,
                "skin_tone": "冷白", "temperature": 11, "intensity": 60,
            },
            shape={
                "small_face": 19, "slim": 33, "v_shape": 25, "jaw": 31, "cheekbone": 40,
                "shorten": 34, "contour_smooth": 44, "lower": 13, "middle": 15, "upper": 17, "hairline": 12,
            },
            makeup={"look": "淡人妆", "intensity": 80},
            body={
                "small_head": 33, "swan_neck": 69, "slim_arm": 43, "straight_shoulder": 61, "slim_body": 45,
                "slim_waist": 60, "long_leg": 24, "plump_breast": 0, "slim_hip": 0, "smooth": 19, "whitening": 26,
            },
        )

        effects = json.loads(script.dumps())["materials"]["effects"]
        by_rid = {item["resource_id"]: item for item in effects}

        # resource_id -> (草稿内中文显示名, 期望强度 0~1, 强度落点)：磨皮/美白在 skin 与 body 下各有一条
        expected = {
            # skin：adjust_param
            "7106322605304451614": ("匀肤", 0.21, "adjust"),
            "7165761391037518350": ("丰盈", 0.30, "adjust"),
            "6976822940608238093": ("磨皮", 0.52, "value"),
            "7127560078508429831": ("祛法令纹", 0.38, "adjust"),
            "7210363411970921017": ("亮眼", 0.29, "adjust"),
            "7127559798861599268": ("祛黑眼圈", 0.57, "adjust"),
            "6998408303826965006": ("美白", 0.67, "value"),
            "6998408263892996639": ("白牙", 0.41, "adjust"),
            # shape：adjust_param
            "7325345220688613914": ("小脸", 0.19, "adjust"),
            "7126765507457323557": ("瘦脸", 0.33, "adjust"),
            "7358087335411454501": ("V脸", 0.25, "adjust"),
            "7126764917918536199": ("下颌骨", 0.31, "adjust"),
            "7127587811795931662": ("颧骨", 0.40, "adjust"),
            "7126865570653278751": ("短脸", 0.34, "adjust"),
            "7165761469231927838": ("流畅脸", 0.44, "adjust"),
            "7130850220891443725": ("下庭", 0.13, "adjust"),
            "7130850182488396325": ("中庭", 0.15, "adjust"),
            "7130849819957924389": ("上庭", 0.17, "adjust"),
            "7126865429154238984": ("发际线", 0.12, "adjust"),
            # body：顶层 value（含与 skin 同名的磨皮/美白）
            "6976812039847023111": ("小头", 0.33, "value"),
            "7187453444146336313": ("天鹅颈", 0.69, "value"),
            "7187394795965256247": ("瘦手臂", 0.43, "value"),
            "7246635041663488567": ("直角肩", 0.61, "value"),
            "6976812219048661540": ("瘦身", 0.45, "value"),
            "6976812120591569416": ("瘦腰", 0.60, "value"),
            "6956089104412971534": ("长腿", 0.24, "value"),
            "7125729150572171812": ("磨皮", 0.19, "value"),
            "7125780457576206879": ("美白", 0.26, "value"),
        }
        assert len(effects) == len(expected) + 3  # 28 条滑杆 + 冷白 + 淡人妆 + makeup-root
        for rid, (name, value, mode) in expected.items():
            item = by_rid[rid]
            assert item["name"] == name, rid
            if mode == "value":
                assert item["value"] == pytest.approx(value), name
                assert item["adjust_params"] == [], name
            else:
                assert item["adjust_params"][0]["value"] == pytest.approx(value), name

        skin = by_rid["7148720872105185800"]
        assert skin["name"] == "冷白"
        skin_params = {item["name"]: item["value"] for item in skin["face_adjust_params"][0]["adjust_params"]}
        assert skin_params["face_adjust_skin_ColdWarm"] == pytest.approx(11 / 99)
        assert skin_params["face_adjust_skin_Intensity"] == pytest.approx(0.6)

        makeup = by_rid["7376172391774294554"]
        assert makeup["name"] == "淡人妆"
        assert makeup["face_adjust_params"][0]["adjust_params"][0] == {
            "default_value": 0.0, "name": "face_adjust_whole", "value": pytest.approx(0.8),
        }
        assert makeup["face_adjust_params"][0]["face_id"] == "1"

        names = [item["name"] for item in effects]
        assert names.count("makeup-root") == 1 and effects[-1]["type"] == "makeup_root"
        # 丰胸/美胯 传 0 → 不写入
        assert "丰胸" not in names and "美胯" not in names
    finally:
        DRAFT_CACHE.pop("beauty-fidelity", None)
