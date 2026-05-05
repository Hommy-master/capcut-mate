"""Unit tests for src.utils.upload_file routing (COS / OSS selection)."""
from unittest.mock import patch

import pytest

from exceptions import CustomError, CustomException


@pytest.fixture
def upload_mocks():
    with (
        patch("src.utils.upload_file.cos_upload_file") as m_cos,
        patch("src.utils.upload_file.oss_upload_file") as m_oss,
        patch("src.utils.upload_file._is_cos_configured") as m_ic,
        patch("src.utils.upload_file._is_oss_configured") as m_io,
    ):
        yield m_cos, m_oss, m_ic, m_io


def test_upload_file_prefers_cos_when_configured(upload_mocks) -> None:
    m_cos, m_oss, m_ic, m_io = upload_mocks
    m_ic.return_value = True
    m_io.return_value = True
    m_cos.return_value = "https://cos.example/signed"
    from src.utils.upload_file import upload_file

    assert upload_file("/tmp/a.mp4") == "https://cos.example/signed"
    m_cos.assert_called_once()
    m_oss.assert_not_called()


def test_upload_file_fallback_oss_when_cos_not_configured(upload_mocks) -> None:
    m_cos, m_oss, m_ic, m_io = upload_mocks
    m_ic.return_value = False
    m_io.return_value = True
    m_oss.return_value = "https://oss.example/signed"
    from src.utils.upload_file import upload_file

    assert upload_file("/tmp/b.mp4") == "https://oss.example/signed"
    m_oss.assert_called_once()
    m_cos.assert_not_called()


def test_upload_file_neither_storage_raises(upload_mocks) -> None:
    m_cos, m_oss, m_ic, m_io = upload_mocks
    m_ic.return_value = False
    m_io.return_value = False
    from src.utils.upload_file import upload_file

    with pytest.raises(CustomException) as ei:
        upload_file("/tmp/c.mp4")
    assert ei.value.err == CustomError.INTERNAL_SERVER_ERROR
    m_cos.assert_not_called()
    m_oss.assert_not_called()


def test_upload_file_passes_expire_days(upload_mocks) -> None:
    m_cos, m_oss, m_ic, m_io = upload_mocks
    m_ic.return_value = True
    m_cos.return_value = "u"
    from src.utils.upload_file import upload_file

    upload_file("/x", expire_days=14)
    m_cos.assert_called_once_with(file_path="/x", expire_days=14)
