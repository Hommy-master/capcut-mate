"""蒙版关键帧：单位换算、草稿字段拼写、缺蒙版报错、同时刻覆盖。"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from pydantic import ValidationError

from src.pyJianYingDraft import ScriptFile, TrackType, MaskType
from src.pyJianYingDraft.keyframe import KeyframeProperty
from src.pyJianYingDraft.local_materials import VideoMaterial
from src.pyJianYingDraft.time_util import Timerange
from src.pyJianYingDraft.video_segment import VideoSegment
from src.schemas.add_mask_keyframes import MaskKeyframeItem
from src.service.add_mask_keyframes import add_mask_keyframes
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError


def _video_segment(width: int = 1440, height: int = 2560, duration: int = 15_000_000) -> VideoSegment:
    material = VideoMaterial(
        "https://example.com/demo.mp4",
        duration=duration,
        width=width,
        height=height,
        material_type="video",
    )
    return VideoSegment(material, Timerange(0, duration))


def _segment_with_mask(**kwargs) -> VideoSegment:
    seg = _video_segment(**kwargs)
    seg.add_mask(MaskType.圆形)
    return seg


def _kf_list(seg: VideoSegment, prop: KeyframeProperty):
    for kf_list in seg.common_keyframes:
        if kf_list.keyframe_property == prop:
            return kf_list
    return None


def test_position_conversion_matches_half_material_size():
    seg = _segment_with_mask()
    added = seg.add_mask_keyframe(5_000_000, center_x=-360, center_y=-200)
    assert added == 2

    x_list = _kf_list(seg, KeyframeProperty.mask_position_x)
    y_list = _kf_list(seg, KeyframeProperty.mask_position_y)
    assert x_list is not None
    assert y_list is not None
    assert x_list.keyframes[0].values[0] == pytest.approx(-360 / 720)
    assert y_list.keyframes[0].values[0] == pytest.approx(-200 / 1280)


def test_size_conversion_matches_material_size():
    # 对齐剪映草稿：KFTypeMaskSizeX = width / material_width，SizeY = height / material_height
    seg = _segment_with_mask(width=1080, height=1920)
    added = seg.add_mask_keyframe(0, width=540, height=540)
    added += seg.add_mask_keyframe(5_000_000, width=1075.813953488372, height=1071.032558139535)
    assert added == 4

    size_x = _kf_list(seg, KeyframeProperty.mask_size_x)
    size_y = _kf_list(seg, KeyframeProperty.mask_size_y)
    assert size_x is not None and size_y is not None
    assert [kf.values[0] for kf in size_x.keyframes] == [
        pytest.approx(0.5),
        pytest.approx(0.9961240310077519),
    ]
    assert [kf.values[0] for kf in size_y.keyframes] == [
        pytest.approx(0.28125),
        pytest.approx(0.5578294573643412),
    ]


def test_feather_divided_by_100_rotation_in_degrees():
    seg = _segment_with_mask()
    added = seg.add_mask_keyframe(0, feather=0, rotation=0)
    added += seg.add_mask_keyframe(5_000_000, feather=100, rotation=180)
    assert added == 4

    feather = _kf_list(seg, KeyframeProperty.mask_feather)
    rotation = _kf_list(seg, KeyframeProperty.mask_rotation)
    assert feather is not None and rotation is not None
    assert [kf.values[0] for kf in feather.keyframes] == [pytest.approx(0.0), pytest.approx(1.0)]
    assert [kf.values[0] for kf in rotation.keyframes] == [pytest.approx(0.0), pytest.approx(180.0)]


def test_export_uses_capcut_postion_spelling():
    seg = _segment_with_mask()
    seg.add_mask_keyframe(0, center_x=0, center_y=0, width=512, height=512, feather=0, rotation=0)
    exported = {item["property_type"]: item for item in seg.export_json()["common_keyframes"]}
    assert "KFTypeMaskPostionX" in exported
    assert "KFTypeMaskPostionY" in exported
    assert "KFTypeMaskSizeX" in exported
    assert "KFTypeMaskSizeY" in exported
    assert "KFTypeMaskFeather" in exported
    assert "KFTypeMaskRotation" in exported
    assert "KFTypeMaskPositionX" not in exported


def test_missing_mask_raises():
    seg = _video_segment()
    with pytest.raises(ValueError, match="没有蒙版"):
        seg.add_mask_keyframe(0, feather=50)


def test_same_offset_overwrites():
    seg = _segment_with_mask()
    seg.add_mask_keyframe(5_000_000, feather=20)
    seg.add_mask_keyframe(5_000_000, feather=80)
    feather = _kf_list(seg, KeyframeProperty.mask_feather)
    assert feather is not None
    assert len(feather.keyframes) == 1
    assert feather.keyframes[0].values[0] == pytest.approx(0.8)


def test_does_not_change_mask_config():
    seg = _segment_with_mask()
    original = (
        seg.mask.center_x,
        seg.mask.center_y,
        seg.mask.width,
        seg.mask.height,
        seg.mask.feather,
        seg.mask.rotation,
    )
    seg.add_mask_keyframe(
        5_000_000,
        center_x=-360,
        center_y=-200,
        width=1080,
        height=1920,
        feather=100,
        rotation=180,
    )
    assert (
        seg.mask.center_x,
        seg.mask.center_y,
        seg.mask.width,
        seg.mask.height,
        seg.mask.feather,
        seg.mask.rotation,
    ) == original


def test_schema_requires_at_least_one_property():
    with pytest.raises(ValidationError):
        MaskKeyframeItem(segment_id="seg", offset=0)


def test_schema_accepts_width_height_only():
    item = MaskKeyframeItem(segment_id="seg", offset=0, width=540, height=540)
    assert item.width == 540
    assert item.height == 540


def test_schema_rejects_negative_size():
    with pytest.raises(ValidationError):
        MaskKeyframeItem(segment_id="seg", offset=0, width=-1)


def test_service_writes_keyframes_and_counts_xy_separately():
    draft_id = "mask-kf-draft"
    script = ScriptFile(1080, 1920, 30, True)
    script.save = lambda: None  # type: ignore[method-assign]
    script.add_track(TrackType.video)
    seg = _segment_with_mask()
    script.add_material(seg.material_instance)
    script.add_segment(seg)
    DRAFT_CACHE[draft_id] = script
    try:
        _, added, affected = add_mask_keyframes(
            draft_url=f"http://localhost/get_draft?draft_id={draft_id}",
            keyframes=[
                {
                    "segment_id": seg.segment_id,
                    "offset": 0,
                    "X": 0,
                    "Y": 0,
                    "width": 720,
                    "height": 1280,
                    "feather": 0,
                    "rotation": 0,
                },
                {
                    "segment_id": seg.segment_id,
                    "offset": 5_000_000,
                    "X": -360,
                    "Y": -200,
                    "width": 1440,
                    "height": 2560,
                    "feather": 100,
                    "rotation": 180,
                },
            ],
        )
        assert added == 12
        assert affected == [seg.segment_id]

        content = json.loads(script.dumps())
        kfs = content["tracks"][0]["segments"][0]["common_keyframes"]
        by_type = {item["property_type"]: item for item in kfs}
        assert by_type["KFTypeMaskPostionX"]["keyframe_list"][1]["values"][0] == pytest.approx(-0.5)
        assert by_type["KFTypeMaskSizeX"]["keyframe_list"][0]["values"][0] == pytest.approx(0.5)
        assert by_type["KFTypeMaskSizeY"]["keyframe_list"][1]["values"][0] == pytest.approx(1.0)
        assert by_type["KFTypeMaskFeather"]["keyframe_list"][1]["values"][0] == pytest.approx(1.0)
        assert by_type["KFTypeMaskRotation"]["keyframe_list"][1]["values"][0] == pytest.approx(180.0)
        mask_config = content["materials"]["masks"][0]["config"]
        assert mask_config["centerX"] == 0.0
        assert mask_config["feather"] == 0.0
        assert mask_config["width"] == pytest.approx(seg.mask.width)
        assert mask_config["height"] == pytest.approx(seg.mask.height)
    finally:
        DRAFT_CACHE.pop(draft_id, None)


def test_service_requires_existing_mask():
    draft_id = "mask-kf-missing"
    script = ScriptFile(1080, 1920, 30, True)
    script.save = lambda: None  # type: ignore[method-assign]
    script.add_track(TrackType.video)
    seg = _video_segment()
    script.add_segment(seg)
    DRAFT_CACHE[draft_id] = script
    try:
        with pytest.raises(CustomException) as exc:
            add_mask_keyframes(
                draft_url=f"http://localhost/get_draft?draft_id={draft_id}",
                keyframes=[{"segment_id": seg.segment_id, "offset": 0, "feather": 50}],
            )
        assert exc.value.err == CustomError.SEGMENT_MASK_NOT_FOUND
    finally:
        DRAFT_CACHE.pop(draft_id, None)
