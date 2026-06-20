"""Unit tests for object storage key layout."""
import datetime
from unittest.mock import patch

from src.utils.storage_key import build_storage_object_key


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
