"""Unit tests for the upload request body size guard (请求体超限前置拦截)."""
from src.middlewares.upload_size_guard import _exceeds_body_limit
from src.service.upload_file import MAX_UPLOAD_BODY_BYTES, MAX_UPLOAD_SIZE_BYTES

_UPLOAD_PATH = "/openapi/capcut-mate/v1/upload_file"


def test_oversized_post_is_rejected() -> None:
    assert _exceeds_body_limit("POST", _UPLOAD_PATH, str(MAX_UPLOAD_BODY_BYTES + 1)) is True


def test_limit_boundary_is_allowed() -> None:
    assert _exceeds_body_limit("POST", _UPLOAD_PATH, str(MAX_UPLOAD_BODY_BYTES)) is False


def test_500mb_file_plus_overhead_is_allowed() -> None:
    # 合法上限文件 + multipart 封装开销不能被误杀
    assert _exceeds_body_limit("POST", _UPLOAD_PATH, str(MAX_UPLOAD_SIZE_BYTES + 100)) is False


def test_missing_or_invalid_content_length_is_not_guarded() -> None:
    for content_length in (None, "", "abc", "-1", "1.5"):
        assert _exceeds_body_limit("POST", _UPLOAD_PATH, content_length) is False


def test_other_methods_and_paths_are_not_guarded() -> None:
    assert _exceeds_body_limit("GET", _UPLOAD_PATH, str(MAX_UPLOAD_BODY_BYTES + 1)) is False
    assert _exceeds_body_limit("POST", "/openapi/capcut-mate/v1/gen_video", str(MAX_UPLOAD_BODY_BYTES + 1)) is False
