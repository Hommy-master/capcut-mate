"""Unit tests for object storage key layout."""
import datetime
from unittest.mock import patch

import pytest

import config
from src.utils.storage_key import build_storage_object_key, build_upload_object_key, sanitize_object_filename


def test_sanitize_strips_path_traversal() -> None:
    assert sanitize_object_filename("../../etc/passwd") == "passwd"
    assert sanitize_object_filename("..\\..\\windows\\x.mp4") == "x.mp4"
    assert sanitize_object_filename("/tmp/a/b/clip.mp4") == "clip.mp4"


def test_sanitize_rejects_empty_name() -> None:
    for bad in ("..", "/", "", "   ", "///"):
        with pytest.raises(ValueError):
            sanitize_object_filename(bad)


def test_sanitize_keeps_cjk_and_lowercases_extension() -> None:
    assert sanitize_object_filename("我的视频 Demo.MP4") == "我的视频_Demo.mp4"


def test_sanitize_replaces_url_unsafe_chars() -> None:
    assert sanitize_object_filename("a b?c#d&e=f.mp4") == "a_b_c_d_e_f.mp4"


def test_build_upload_object_key_unique_and_dated() -> None:
    now = datetime.datetime(2026, 10, 5, 12, 0, 0)
    with patch.object(config, "STORAGE_UPLOAD_PREFIX", "jianchuang"):
        first = build_upload_object_key("demo.mp4", now=now)
        second = build_upload_object_key("demo.mp4", now=now)

    assert first.startswith("jianchuang/2026-10-05/")
    assert first.endswith("_demo.mp4")
    assert first != second  # 唯一前缀避免同名覆盖


def test_build_storage_object_key_without_prefix() -> None:
    fixed = datetime.datetime(2026, 6, 15, 14, 30)
    assert build_storage_object_key("video.mp4", now=fixed) == "2026-06-15/video.mp4"


def test_build_storage_object_key_with_prefix() -> None:
    fixed = datetime.datetime(2026, 6, 15, 14, 30)
    with patch("src.utils.storage_key.config.STORAGE_UPLOAD_PREFIX", "capcut-mate"):
        assert build_storage_object_key("video.mp4", now=fixed) == "capcut-mate/2026-06-15/video.mp4"


def test_build_storage_object_key_strips_slashes_from_prefix() -> None:
    fixed = datetime.datetime(2026, 6, 15, 14, 30)
    with patch("src.utils.storage_key.config.STORAGE_UPLOAD_PREFIX", "/capcut-mate/"):
        assert build_storage_object_key("video.mp4", now=fixed) == "capcut-mate/2026-06-15/video.mp4"
