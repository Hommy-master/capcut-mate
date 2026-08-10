"""
strict unit tests for src.utils.storage_upload_retry
"""
import errno
from unittest.mock import MagicMock, patch

import pytest
import requests
import urllib3.exceptions
from requests.exceptions import ChunkedEncodingError
from qcloud_cos.cos_exception import CosClientError, CosServiceError

import src.utils.storage_upload_retry as sur


@pytest.fixture
def no_sleep_no_random_delay():
    """Make retries cheap and deterministic in tests."""
    with (
        patch.object(sur, "time") as m_time,
        patch.object(sur, "random") as m_random,
    ):
        m_time.sleep = MagicMock()
        m_random.uniform = MagicMock(return_value=0.0)
        yield m_time


class TestIterExceptionChain:
    def test_yields_self_then_cause(self) -> None:
        root = requests.ConnectionError("outer")
        root.__cause__ = OSError(errno.ETIMEDOUT, "inner")
        seen = list(sur._iter_exception_chain(root))
        assert len(seen) == 2
        assert seen[0] is root
        assert seen[1] is root.__cause__

    def test_stops_on_cycle(self) -> None:
        a = Exception("a")
        b = Exception("b")
        a.__context__ = b
        b.__context__ = a
        seen = list(sur._iter_exception_chain(a))
        assert len(seen) == 2


class TestIsRetryableStorageError:
    @pytest.mark.parametrize(
        "exc",
        [
            requests.ConnectionError("refused"),
            requests.Timeout("t"),
            ChunkedEncodingError(),
        ],
    )
    def test_requests_transient(self, exc: Exception) -> None:
        assert sur.is_retryable_storage_error(exc) is True

    def test_urllib3_new_connection(self) -> None:
        from urllib3.connection import HTTPConnection

        exc = urllib3.exceptions.NewConnectionError(HTTPConnection("127.0.0.1", 9), "nope")
        assert sur.is_retryable_storage_error(exc) is True

    def test_urllib3_read_timeout(self) -> None:
        pool = MagicMock()
        exc = urllib3.exceptions.ReadTimeoutError(pool, "http://example", "read")
        assert sur.is_retryable_storage_error(exc) is True

    def test_urllib3_connect_timeout(self) -> None:
        assert sur.is_retryable_storage_error(urllib3.exceptions.ConnectTimeoutError("c")) is True

    def test_urllib3_protocol(self) -> None:
        assert sur.is_retryable_storage_error(urllib3.exceptions.ProtocolError("p")) is True

    @pytest.mark.parametrize("code", (errno.ECONNRESET, errno.ETIMEDOUT, 10054))
    def test_oserror_errno(self, code: int) -> None:
        assert sur.is_retryable_storage_error(OSError(code, "x")) is True

    def test_oserror_not_retryable(self) -> None:
        assert sur.is_retryable_storage_error(OSError(errno.ENOENT, "nope")) is False

    def test_cos_client_error(self) -> None:
        assert sur.is_retryable_storage_error(CosClientError("timeout")) is True

    @pytest.mark.parametrize("status, expected", [(503, True), (500, True), (400, False), (404, False)])
    def test_cos_service_error(self, status: int, expected: bool) -> None:
        err = CosServiceError("PUT", {"code": "K", "message": "m", "resource": "r", "requestid": "q", "traceid": "t"}, status)
        assert sur.is_retryable_storage_error(err) is expected

    def test_exception_chain_finds_cause(self) -> None:
        inner = requests.ConnectionError("c")
        outer = ValueError("wrap")
        outer.__cause__ = inner
        assert sur.is_retryable_storage_error(outer) is True

    def test_exception_chain_valueerror_first_in_chain_still_finds_cause(self) -> None:
        """Outer not retryable, __cause__ is: must still return True."""
        inner = requests.ConnectionError("c")
        outer = ValueError("v")
        outer.__cause__ = inner
        assert sur.is_retryable_storage_error(outer) is True

    def test_oss_request_error(self) -> None:
        import oss2.exceptions as ox

        e = ox.RequestError(requests.ConnectionError("r"))
        assert sur.is_retryable_storage_error(e) is True

    @pytest.mark.parametrize("status, expected", [(503, True), (500, True), (408, True), (400, False), (404, False)])
    def test_oss_oss_error_status(self, status: int, expected: bool) -> None:
        import oss2.exceptions as ox

        e = ox.OssError(status, {}, "", {})
        assert sur.is_retryable_storage_error(e) is expected


class TestRunWithStorageRetry:
    def test_success_first_call(self, no_sleep_no_random_delay) -> None:
        op = MagicMock(return_value="ok")
        assert sur.run_with_storage_retry(op, context="T") == "ok"
        op.assert_called_once()

    def test_retries_then_success(self, no_sleep_no_random_delay) -> None:
        m_time = no_sleep_no_random_delay
        op = MagicMock(side_effect=[requests.ConnectionError("1"), requests.ConnectionError("2"), "done"])
        assert sur.run_with_storage_retry(op) == "done"
        assert op.call_count == 3
        assert m_time.sleep.call_count == 2

    def test_non_retryable_raises_immediately(self, no_sleep_no_random_delay) -> None:
        m_time = no_sleep_no_random_delay
        op = MagicMock(side_effect=ValueError("bad"))
        with pytest.raises(ValueError, match="bad"):
            sur.run_with_storage_retry(op)
        op.assert_called_once()
        m_time.sleep.assert_not_called()

    def test_exhausts_attempts(self, no_sleep_no_random_delay) -> None:
        m_time = no_sleep_no_random_delay
        err = requests.ConnectionError("x")
        with patch.object(sur, "_STORAGE_UPLOAD_MAX_ATTEMPTS", 3):
            op = MagicMock(side_effect=err)
            with pytest.raises(requests.ConnectionError):
                sur.run_with_storage_retry(op, context="X")
        assert op.call_count == 3
        assert m_time.sleep.call_count == 2

    def test_context_passed_to_warning_logger(self, no_sleep_no_random_delay) -> None:
        op = MagicMock(side_effect=[requests.ConnectionError("f"), "ok"])
        with patch.object(sur.logger, "warning") as m_warn:
            sur.run_with_storage_retry(op, context="COS")
        m_warn.assert_called_once()
        assert m_warn.call_args is not None
        flat = " ".join(str(x) for x in m_warn.call_args[0])
        assert "COS" in flat and "storage upload attempt" in flat
