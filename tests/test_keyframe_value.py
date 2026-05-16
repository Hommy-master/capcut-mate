"""keyframe_value 归一化工具单元测试。"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.keyframe_value import normalize_keyframe_value


def test_normalize_pixel_position_x():
    assert normalize_keyframe_value("KFTypePositionX", -2608.0, width=1920) == -2608.0 / 1920
    assert normalize_keyframe_value("KFTypePositionX", -699.0, width=1920) == -699.0 / 1920


def test_normalize_already_normalized_position_x():
    assert normalize_keyframe_value("KFTypePositionX", -0.1, width=1920) == -0.1
    assert normalize_keyframe_value("KFTypePositionX", 1.0, width=1920) == 1.0


def test_normalize_pixel_position_y():
    assert normalize_keyframe_value("KFTypePositionY", 540.0, height=1080) == 0.5


def test_keyframes_infos_assume_pixel_normalizes_small_values():
    assert normalize_keyframe_value(
        "KFTypePositionX", 1.0, width=1920, assume_pixel=True
    ) == 1.0 / 1920


def test_rotation_scale_alpha_unchanged():
    canvas = dict(width=1920, height=1080)
    assert normalize_keyframe_value("KFTypeRotation", 90.0, **canvas) == 90.0
    assert normalize_keyframe_value("UNIFORM_SCALE", 1.3, **canvas) == 1.3
    assert normalize_keyframe_value("KFTypeAlpha", 0.5, **canvas) == 0.5


def test_rotation_scale_alpha_unchanged_with_assume_pixel():
    canvas = dict(width=1920, height=1080, assume_pixel=True)
    assert normalize_keyframe_value("KFTypeRotation", 45.0, **canvas) == 45.0
    assert normalize_keyframe_value("UNIFORM_SCALE", 1.5, **canvas) == 1.5
    assert normalize_keyframe_value("KFTypeAlpha", 0.8, **canvas) == 0.8
