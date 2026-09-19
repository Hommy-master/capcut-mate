"""美颜导出结构与挂接到视频片段的测试。"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from src.pyJianYingDraft import ScriptFile, TrackType
from src.pyJianYingDraft.local_materials import VideoMaterial
from src.pyJianYingDraft.metadata.beauty_meta import (
    MAKEUP_ROOT,
    BeautyType,
    build_figure_algorithm_path,
)
from src.pyJianYingDraft.time_util import Timerange
from src.pyJianYingDraft.video_segment import FigureEffect, VideoSegment
from src.service.add_beauty import add_beauty
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError


ALGO = build_figure_algorithm_path("PLACEHOLDER", "video-mat-1")


def _effect(beauty_type: BeautyType, intensity_0_1: float, algorithm_path: str = "") -> dict:
    return FigureEffect(
        beauty_type.value,
        intensity_0_1,
        algorithm_artifact_path=algorithm_path,
    ).export_json()


def test_whitening_uses_value_and_empty_algorithm_path():
    data = _effect(BeautyType.美白, 0.6, ALGO)
    assert data["name"] == "美白"
    assert data["type"] == "figure"
    assert data["sub_type"] == "none"
    assert data["resource_id"] == "6998408303826965006"
    assert data["category_id"] == "auto-beauty2"
    assert data["value"] == pytest.approx(0.6)
    assert data["adjust_params"] == []
    assert data["algorithm_artifact_path"] == ""
    assert data["source_platform"] == 0
    assert data["effect_id"] == ""
    assert "path" not in data


def test_smooth_uses_value_and_algorithm_path():
    data = _effect(BeautyType.磨皮, 0.19, ALGO)
    assert data["name"] == "磨皮"
    assert data["sub_type"] == "auto_beauty"
    assert data["resource_id"] == "6976822940608238093"
    assert data["value"] == pytest.approx(0.19)
    assert data["adjust_params"] == []
    assert data["algorithm_artifact_path"] == ALGO


def test_teeth_uses_adjust_params_and_keeps_value_zero():
    data = _effect(BeautyType.白牙, 0.17, ALGO)
    assert data["name"] == "白牙"
    assert data["resource_id"] == "6998408263892996639"
    assert data["value"] == 0.0
    assert data["adjust_params"] == [{"default_value": 0.0, "name": "1", "value": pytest.approx(0.17)}]
    assert data["algorithm_artifact_path"] == ALGO


def test_makeup_root_shape():
    data = FigureEffect(MAKEUP_ROOT, 0.0, algorithm_artifact_path=ALGO).export_json()
    assert data["name"] == "makeup-root"
    assert data["type"] == "makeup_root"
    assert data["resource_id"] == "7273096354098844221"
    assert data["category_id"] == ""
    assert data["value"] == 0.0
    assert data["algorithm_artifact_path"] == ALGO
    assert "path" not in data


def _video_segment() -> VideoSegment:
    material = VideoMaterial(
        "https://example.com/demo.mp4",
        duration=5_000_000,
        width=1080,
        height=1920,
        material_type="video",
    )
    return VideoSegment(material, Timerange(0, 5_000_000))


def test_add_beauty_updates_intensity_without_duplicating_refs():
    seg = _video_segment()
    first = seg.add_beauty(BeautyType.美白, 60)
    second = seg.add_beauty(BeautyType.美白, 30)
    assert first is second
    assert second.intensity == pytest.approx(0.3)
    assert seg.extra_material_refs.count(first.global_id) == 1
    assert len([item for item in seg.figures if item.meta.name == "美白"]) == 1


def test_makeup_root_added_once():
    seg = _video_segment()
    first = seg.ensure_makeup_root(ALGO)
    second = seg.ensure_makeup_root(ALGO)
    assert first is second
    assert seg.extra_material_refs.count(first.global_id) == 1


def test_add_beauty_exports_into_effects_not_video_effects():
    draft_id = "beauty-test-draft"
    script = ScriptFile(1080, 1920, 30, True)
    script.save = lambda: None  # type: ignore[method-assign]
    script.add_track(TrackType.video)
    seg = _video_segment()
    script.add_material(seg.material_instance)
    script.add_segment(seg)

    DRAFT_CACHE[draft_id] = script
    try:
        _, affected, figure_ids = add_beauty(
            draft_url=f"http://localhost/get_draft?draft_id={draft_id}",
            segment_ids=[seg.segment_id],
            beauty_infos=[
                {"name": "美白", "intensity": 60},
                {"name": "磨皮", "intensity": 19},
                {"name": "白牙", "intensity": 17},
            ],
        )
        assert affected == [seg.segment_id]

        content = json.loads(script.dumps())
        effects = content["materials"]["effects"]
        names = [item["name"] for item in effects]
        assert names == ["美白", "磨皮", "白牙", "makeup-root"]
        assert content["materials"]["video_effects"] == []

        whitening = effects[0]
        smooth = effects[1]
        teeth = effects[2]
        root = effects[3]
        assert whitening["value"] == pytest.approx(0.6)
        assert whitening["algorithm_artifact_path"] == ""
        assert smooth["value"] == pytest.approx(0.19)
        assert smooth["algorithm_artifact_path"].endswith(seg.material_instance.material_id)
        assert teeth["value"] == 0.0
        assert teeth["adjust_params"][0]["name"] == "1"
        assert teeth["adjust_params"][0]["value"] == pytest.approx(0.17)
        assert root["type"] == "makeup_root"
        assert smooth["algorithm_artifact_path"] == root["algorithm_artifact_path"]

        refs = content["tracks"][0]["segments"][0]["extra_material_refs"]
        for figure_id in figure_ids:
            assert figure_id in refs
        assert refs.count(root["id"]) == 1

        # 再次调用只更新强度，不追加素材
        add_beauty(
            draft_url=f"http://localhost/get_draft?draft_id={draft_id}",
            segment_ids=[seg.segment_id],
            beauty_infos=[{"name": "美白", "intensity": 40}],
        )
        content = json.loads(script.dumps())
        effects = content["materials"]["effects"]
        assert [item["name"] for item in effects] == ["美白", "磨皮", "白牙", "makeup-root"]
        assert effects[0]["value"] == pytest.approx(0.4)
        assert effects[0]["id"] == whitening["id"]
    finally:
        DRAFT_CACHE.pop(draft_id, None)


def test_unknown_beauty_name_raises():
    draft_id = "beauty-missing"
    script = ScriptFile(1080, 1920, 30, True)
    script.save = lambda: None  # type: ignore[method-assign]
    script.add_track(TrackType.video)
    seg = _video_segment()
    script.add_segment(seg)
    DRAFT_CACHE[draft_id] = script
    try:
        with pytest.raises(CustomException) as exc:
            add_beauty(
                draft_url=f"http://localhost/get_draft?draft_id={draft_id}",
                segment_ids=[seg.segment_id],
                beauty_infos=[{"name": "瘦脸", "intensity": 20}],
            )
        assert exc.value.err == CustomError.BEAUTY_NOT_FOUND
    finally:
        DRAFT_CACHE.pop(draft_id, None)
