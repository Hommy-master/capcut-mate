"""add_keyframes / keyframes_infos 位置关键帧归一化集成测试。"""
import json
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pyJianYingDraft.segment import VisualSegment
from src.service.add_keyframes import add_keyframes
from src.service.keyframes_infos import keyframes_infos


@pytest.fixture
def visual_segment():
    seg = MagicMock(spec=VisualSegment)
    seg.duration = 10_000_000
    seg.segment_id = "533f9ef5f7d341a2ad3f18eb4cb0f9b0"
    return seg


def test_add_keyframes_normalizes_pixel_position_x(visual_segment):
    """回归：像素位移 -2608 / -699 应除以画布宽度。"""
    keyframes = json.dumps([
        {
            "segment_id": "533f9ef5f7d341a2ad3f18eb4cb0f9b0",
            "property": "KFTypePositionX",
            "offset": 0,
            "value": -2608.0,
        },
        {
            "segment_id": "533f9ef5f7d341a2ad3f18eb4cb0f9b0",
            "property": "KFTypePositionX",
            "offset": 3_345_600,
            "value": -699.0,
        },
    ])
    mock_script = MagicMock()
    mock_script.width = 1920
    mock_script.height = 1080

    with patch("src.service.add_keyframes.helper.get_url_param", return_value="draft-kf"), \
            patch("src.service.add_keyframes.DRAFT_CACHE", {"draft-kf": mock_script}), \
            patch("src.service.add_keyframes.find_segment_by_id", return_value=visual_segment):
        draft_url, added, affected = add_keyframes(
            "http://localhost/v1/get_draft?draft_id=draft-kf",
            keyframes,
        )

    assert added == 2
    calls = visual_segment.add_keyframe.call_args_list
    assert calls[0][0][2] == pytest.approx(-2608.0 / 1920)
    assert calls[1][0][2] == pytest.approx(-699.0 / 1920)
    assert affected == ["533f9ef5f7d341a2ad3f18eb4cb0f9b0"]
    assert "draft-kf" in draft_url


def test_add_keyframes_rotation_value_unchanged(visual_segment):
    mock_script = MagicMock(width=1920, height=1080)
    keyframes = json.dumps([{
        "segment_id": "533f9ef5f7d341a2ad3f18eb4cb0f9b0",
        "property": "KFTypeRotation",
        "offset": 0,
        "value": 90.0,
    }])

    with patch("src.service.add_keyframes.helper.get_url_param", return_value="draft-kf"), \
            patch("src.service.add_keyframes.DRAFT_CACHE", {"draft-kf": mock_script}), \
            patch("src.service.add_keyframes.find_segment_by_id", return_value=visual_segment):
        add_keyframes("http://localhost/v1/get_draft?draft_id=draft-kf", keyframes)

    assert visual_segment.add_keyframe.call_args[0][2] == 90.0


def test_add_keyframes_uniform_scale_and_alpha_unchanged(visual_segment):
    mock_script = MagicMock(width=1920, height=1080)
    keyframes = json.dumps([
        {
            "segment_id": "533f9ef5f7d341a2ad3f18eb4cb0f9b0",
            "property": "UNIFORM_SCALE",
            "offset": 0,
            "value": 1.3,
        },
        {
            "segment_id": "533f9ef5f7d341a2ad3f18eb4cb0f9b0",
            "property": "KFTypeAlpha",
            "offset": 1_000_000,
            "value": 0.5,
        },
    ])

    with patch("src.service.add_keyframes.helper.get_url_param", return_value="draft-kf"), \
            patch("src.service.add_keyframes.DRAFT_CACHE", {"draft-kf": mock_script}), \
            patch("src.service.add_keyframes.find_segment_by_id", return_value=visual_segment):
        add_keyframes("http://localhost/v1/get_draft?draft_id=draft-kf", keyframes)

    calls = visual_segment.add_keyframe.call_args_list
    assert calls[0][0][2] == 1.3
    assert calls[1][0][2] == 0.5


def test_keyframes_infos_normalizes_pixels_for_position():
    out = keyframes_infos(
        ctype="KFTypePositionX",
        offsets="0|50",
        values="-2608|-699",
        segment_infos=[{"id": "seg-1", "start": 0, "end": 10_000_000}],
        width=1920,
        height=1080,
    )
    items = json.loads(out)
    assert len(items) == 2
    assert items[0]["value"] == pytest.approx(-2608.0 / 1920)
    assert items[1]["value"] == pytest.approx(-699.0 / 1920)
    assert items[0]["offset"] == 0
    assert items[1]["offset"] == 5_000_000
