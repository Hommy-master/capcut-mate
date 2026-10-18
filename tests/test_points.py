"""余额接口客户端：请求字段、重试幂等与余额不足处理。"""
from unittest.mock import Mock, patch

import pytest
import requests

from src.utils.points import deduct_user_points

_API_KEY = "11111111-1111-1111-1111-111111111111"


def _response(code: int = 0, data=None) -> Mock:
    resp = Mock()
    resp.json.return_value = {
        "code": code,
        "message": "ok" if code == 0 else "error",
        "traceid": "trace",
        "data": data if data is not None else {},
    }
    resp.raise_for_status.return_value = None
    return resp


def test_deduct_sends_request_id_and_payload() -> None:
    with patch("src.utils.points.requests.post", return_value=_response()) as m_post:
        assert deduct_user_points(_API_KEY, 0.5, "上传文件") is True

    payload = m_post.call_args.kwargs["json"]
    assert payload["apiKey"] == _API_KEY
    assert payload["points"] == 0.5
    assert payload["desc"] == "上传文件"
    # 未显式传入时自动生成 UUID，满足服务端 64 字符上限
    assert len(payload["requestId"]) == 36


def test_deduct_honours_explicit_request_id() -> None:
    with patch("src.utils.points.requests.post", return_value=_response()) as m_post:
        assert deduct_user_points(_API_KEY, 0.5, "上传文件", request_id="req-1") is True

    assert m_post.call_args.kwargs["json"]["requestId"] == "req-1"


def test_deduct_retry_reuses_same_request_id() -> None:
    """超时重试必须复用同一个幂等键，否则服务端会重复扣费。"""
    with (
        patch(
            "src.utils.points.requests.post",
            side_effect=[requests.exceptions.Timeout(), _response()],
        ) as m_post,
        patch("src.utils.points.time.sleep"),
    ):
        assert deduct_user_points(_API_KEY, 0.5, "上传文件") is True

    assert m_post.call_count == 2
    request_ids = {call.kwargs["json"]["requestId"] for call in m_post.call_args_list}
    assert len(request_ids) == 1


def test_deduct_insufficient_balance_returns_false() -> None:
    """服务端不再允许透支：余额不足返回 10008，客户端按失败处理。"""
    with patch("src.utils.points.requests.post", return_value=_response(code=10008)):
        assert deduct_user_points(_API_KEY, 0.5, "上传文件") is False


def test_deduct_invalid_apikey_returns_false() -> None:
    with patch("src.utils.points.requests.post", return_value=_response(code=10007)):
        assert deduct_user_points(_API_KEY, 0.5, "上传文件") is False
