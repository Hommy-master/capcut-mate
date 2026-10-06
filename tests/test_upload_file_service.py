"""Unit tests for the upload_file service (服务端中转上传：体积上限 / 计费 / 临时文件清理)."""
import io
from unittest.mock import patch

import pytest
from starlette.datastructures import Headers, UploadFile

import config
from exceptions import CustomError, CustomException
from src.service.upload_file import MAX_UPLOAD_SIZE_BYTES, UPLOAD_PRICE_PER_MB, upload_file

_API_KEY = "11111111-1111-1111-1111-111111111111"


def _make_file(payload: bytes, filename: str = "demo.mp4") -> UploadFile:
    return UploadFile(
        file=io.BytesIO(payload),
        size=len(payload),
        filename=filename,
        headers=Headers({"content-type": "video/mp4"}),
    )


@pytest.fixture
def service_mocks(tmp_path):
    with (
        patch("src.service.upload_file.upload_file_to_storage") as m_upload,
        patch("src.service.upload_file.get_user_points") as m_points,
        patch("src.service.upload_file.deduct_user_points") as m_deduct,
        patch.object(config, "TEMP_DIR", str(tmp_path)),
    ):
        m_upload.return_value = "https://bucket.example/signed-url"
        m_points.return_value = 100.0
        m_deduct.return_value = True
        yield m_upload, m_points, m_deduct, tmp_path


def test_requires_apikey_when_enabled(service_mocks) -> None:
    m_upload, m_points, m_deduct, _ = service_mocks
    with patch.object(config, "ENABLE_APIKEY", True):
        with pytest.raises(CustomException) as ei:
            upload_file(_make_file(b"x"))
    assert ei.value.err == CustomError.INVALID_APIKEY
    m_points.assert_not_called()
    m_upload.assert_not_called()


def test_invalid_apikey_format_rejected(service_mocks) -> None:
    m_upload, m_points, m_deduct, _ = service_mocks
    with patch.object(config, "ENABLE_APIKEY", True):
        with pytest.raises(CustomException) as ei:
            upload_file(_make_file(b"x"), api_key="not-a-uuid")
    assert ei.value.err == CustomError.PARAM_VALIDATION_FAILED
    m_upload.assert_not_called()


def test_invalid_apikey_propagates(service_mocks) -> None:
    m_upload, m_points, m_deduct, _ = service_mocks
    m_points.side_effect = CustomException(CustomError.INVALID_APIKEY)
    with patch.object(config, "ENABLE_APIKEY", True):
        with pytest.raises(CustomException) as ei:
            upload_file(_make_file(b"x"), api_key=_API_KEY)
    assert ei.value.err == CustomError.INVALID_APIKEY
    m_upload.assert_not_called()


def test_low_balance_rejected_before_upload(service_mocks) -> None:
    m_upload, m_points, m_deduct, _ = service_mocks
    m_points.return_value = 1.0  # 与 gen_video 一致：余额需大于 1
    with patch.object(config, "ENABLE_APIKEY", True):
        with pytest.raises(CustomException) as ei:
            upload_file(_make_file(b"x" * 1024), api_key=_API_KEY)
    assert ei.value.err == CustomError.INSUFFICIENT_ACCOUNT_BALANCE
    m_upload.assert_not_called()
    m_deduct.assert_not_called()


def test_disallowed_extension_rejected(service_mocks) -> None:
    m_upload, m_points, m_deduct, tmp_path = service_mocks
    with patch.object(config, "ENABLE_APIKEY", False):
        with pytest.raises(CustomException) as ei:
            upload_file(_make_file(b"x", filename="evil.exe"))
    assert ei.value.err == CustomError.FILE_TYPE_NOT_ALLOWED
    m_upload.assert_not_called()
    assert list(tmp_path.iterdir()) == []


def test_no_extension_rejected(service_mocks) -> None:
    m_upload, m_points, m_deduct, _ = service_mocks
    with patch.object(config, "ENABLE_APIKEY", False):
        with pytest.raises(CustomException) as ei:
            upload_file(_make_file(b"x", filename="README"))
    assert ei.value.err == CustomError.FILE_TYPE_NOT_ALLOWED


def test_invalid_file_name_rejected(service_mocks) -> None:
    m_upload, m_points, m_deduct, _ = service_mocks
    with patch.object(config, "ENABLE_APIKEY", False):
        with pytest.raises(CustomException) as ei:
            upload_file(_make_file(b"x", filename=None))
        assert ei.value.err == CustomError.INVALID_FILE_NAME

        with pytest.raises(CustomException) as ei:
            upload_file(_make_file(b"x", filename=".."))
        assert ei.value.err == CustomError.INVALID_FILE_NAME
    m_upload.assert_not_called()


def test_oversize_rejected_and_temp_cleaned(service_mocks) -> None:
    m_upload, m_points, m_deduct, tmp_path = service_mocks
    with (
        patch.object(config, "ENABLE_APIKEY", False),
        patch("src.service.upload_file.MAX_UPLOAD_SIZE_BYTES", 1024),
    ):
        with pytest.raises(CustomException) as ei:
            upload_file(_make_file(b"x" * 2048))
        assert ei.value.err == CustomError.FILE_SIZE_LIMIT_EXCEEDED
    m_upload.assert_not_called()
    m_deduct.assert_not_called()
    assert list(tmp_path.iterdir()) == []


def test_empty_file_rejected_and_temp_cleaned(service_mocks) -> None:
    m_upload, m_points, m_deduct, tmp_path = service_mocks
    with patch.object(config, "ENABLE_APIKEY", False):
        with pytest.raises(CustomException) as ei:
            upload_file(_make_file(b""))
    assert ei.value.err == CustomError.PARAM_VALIDATION_FAILED
    m_upload.assert_not_called()
    assert list(tmp_path.iterdir()) == []


def test_success_charges_by_size(service_mocks) -> None:
    m_upload, m_points, m_deduct, tmp_path = service_mocks
    payload = b"x" * (1024 * 1024)  # 1MB

    with patch.object(config, "ENABLE_APIKEY", True):
        result = upload_file(_make_file(payload, filename="../../tmp/我的 视频.MP4"), api_key=_API_KEY)

    size_mb = len(payload) / (1024 * 1024)
    expected_cost = round(size_mb * UPLOAD_PRICE_PER_MB, 6)

    assert set(result) == {"url", "key", "size", "size_mb", "cost", "url_expire_days"}
    assert result["url"] == "https://bucket.example/signed-url"
    assert result["size"] == len(payload)
    assert result["size_mb"] == round(size_mb, 3)
    assert result["cost"] == expected_cost == 0.0005
    assert result["url_expire_days"] == config.VIDEO_GEN_RETENTION_DAYS
    assert result["key"].endswith("_我的_视频.mp4")

    m_upload.assert_called_once()
    upload_kwargs = m_upload.call_args.kwargs
    assert upload_kwargs["object_key"] == result["key"]
    assert upload_kwargs["expire_days"] == config.VIDEO_GEN_RETENTION_DAYS
    m_deduct.assert_called_once()
    assert m_deduct.call_args.kwargs["points"] == expected_cost
    assert "1.00MB" in m_deduct.call_args.kwargs["desc"]
    assert list(tmp_path.iterdir()) == []  # 临时文件已清理


def test_storage_failure_does_not_charge(service_mocks) -> None:
    m_upload, m_points, m_deduct, tmp_path = service_mocks
    m_upload.side_effect = CustomException(CustomError.INTERNAL_SERVER_ERROR)

    with patch.object(config, "ENABLE_APIKEY", True):
        with pytest.raises(CustomException) as ei:
            upload_file(_make_file(b"x" * 1024), api_key=_API_KEY)
    assert ei.value.err == CustomError.INTERNAL_SERVER_ERROR
    m_deduct.assert_not_called()
    assert list(tmp_path.iterdir()) == []


def test_charge_failure_still_returns_success(service_mocks) -> None:
    m_upload, m_points, m_deduct, _ = service_mocks

    with patch.object(config, "ENABLE_APIKEY", True):
        m_deduct.return_value = False
        assert upload_file(_make_file(b"x" * 1024), api_key=_API_KEY)["url"] == "https://bucket.example/signed-url"

        m_deduct.side_effect = RuntimeError("points api down")
        assert upload_file(_make_file(b"x" * 1024), api_key=_API_KEY)["url"] == "https://bucket.example/signed-url"


def test_tiny_file_cost_rounds_to_zero_and_skips_charge(service_mocks) -> None:
    m_upload, m_points, m_deduct, _ = service_mocks
    with patch.object(config, "ENABLE_APIKEY", True):
        result = upload_file(_make_file(b"x" * 100), api_key=_API_KEY)
    assert result["cost"] == 0.0
    m_deduct.assert_not_called()


def test_apikey_disabled_skips_billing(service_mocks) -> None:
    m_upload, m_points, m_deduct, _ = service_mocks
    with patch.object(config, "ENABLE_APIKEY", False):
        result = upload_file(_make_file(b"x" * 1024))
    assert result["cost"] == 0.0
    m_points.assert_not_called()
    m_deduct.assert_not_called()
    assert result["url"] == "https://bucket.example/signed-url"


def test_default_max_size_is_500mb() -> None:
    assert MAX_UPLOAD_SIZE_BYTES == 500 * 1024 * 1024
    assert UPLOAD_PRICE_PER_MB == 0.0005
