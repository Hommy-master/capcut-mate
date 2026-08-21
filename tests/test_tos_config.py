"""Unit tests for TOS helpers (endpoint resolution / config gate)."""
from unittest.mock import patch

import config
from src.utils.tos import _resolve_tos_endpoint
from src.utils.upload_file import _is_tos_configured, _is_valid_storage_config


def test_is_valid_storage_config_rejects_placeholder() -> None:
    assert _is_valid_storage_config("") is False
    assert _is_valid_storage_config("xxx") is False
    assert _is_valid_storage_config(" real ") is True


def test_resolve_tos_endpoint_uses_explicit_value() -> None:
    with (
        patch.object(config, "TOS_ENDPOINT", "tos-cn-shanghai.volces.com"),
        patch.object(config, "TOS_REGION", "cn-beijing"),
    ):
        assert _resolve_tos_endpoint() == "tos-cn-shanghai.volces.com"


def test_resolve_tos_endpoint_auto_from_region() -> None:
    with (
        patch.object(config, "TOS_ENDPOINT", ""),
        patch.object(config, "TOS_REGION", "cn-beijing"),
    ):
        assert _resolve_tos_endpoint() == "tos-cn-beijing.volces.com"


def test_is_tos_configured_requires_ak_sk_bucket_region() -> None:
    with (
        patch.object(config, "TOS_ACCESS_KEY_ID", "ak"),
        patch.object(config, "TOS_ACCESS_KEY_SECRET", "sk"),
        patch.object(config, "TOS_BUCKET_NAME", "bucket"),
        patch.object(config, "TOS_REGION", "cn-beijing"),
        patch.object(config, "TOS_ENDPOINT", ""),
    ):
        assert _is_tos_configured() is True

    with (
        patch.object(config, "TOS_ACCESS_KEY_ID", "ak"),
        patch.object(config, "TOS_ACCESS_KEY_SECRET", "sk"),
        patch.object(config, "TOS_BUCKET_NAME", "bucket"),
        patch.object(config, "TOS_REGION", ""),
    ):
        assert _is_tos_configured() is False
