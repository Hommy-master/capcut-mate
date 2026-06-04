"""
Unit tests for src.utils.draft_downloader remote material download and path localization.
"""
import json
import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest
import requests

import src.utils.draft_downloader as dd


@pytest.fixture
def no_sleep():
    with patch.object(dd, "time") as m_time:
        m_time.sleep = MagicMock()
        yield m_time


class TestInferExtFromContentType:
    def test_image_png(self) -> None:
        assert dd._infer_ext_from_content_type("image/png", ".mp4") == ".png"

    def test_image_png_with_charset(self) -> None:
        assert dd._infer_ext_from_content_type("image/png; charset=binary", ".mp4") == ".png"

    def test_video_mp4(self) -> None:
        assert dd._infer_ext_from_content_type("video/mp4", ".bin") == ".mp4"

    def test_audio_mpeg(self) -> None:
        assert dd._infer_ext_from_content_type("audio/mpeg", ".mp4") == ".mp3"

    def test_missing_content_type_uses_fallback(self) -> None:
        assert dd._infer_ext_from_content_type(None, ".mp4") == ".mp4"
        assert dd._infer_ext_from_content_type("", ".mp3") == ".mp3"

    def test_unknown_content_type_uses_fallback(self) -> None:
        assert dd._infer_ext_from_content_type("application/octet-stream", ".mp4") == ".mp4"


class TestDownloadRemoteMaterial:
    BYTEIMG_PNG_URL = (
        "https://p3-bot-workflow-sign.byteimg.com/tos-cn-i-mdko3gqilj/"
        "fdbbff0d6626486eb67b8940f33e2b2f.png~tplv-mdko3gqilj-image.image"
        "?rk3s=81d4c505&x-expires=1810794498&x-signature=FlZnzzCcNuzdqyBQDYj584F9Qfc%3D"
        "&x-wf-file_name=%E5%8F%8C%E8%A1%8C.png"
    )

    def _ok_response(self, content: bytes = b"png-bytes", content_type: str = "image/png") -> MagicMock:
        r = MagicMock()
        r.status_code = 200
        r.headers = {"Content-Type": content_type}
        r.iter_content = MagicMock(return_value=[content])
        r.close = MagicMock()
        return r

    def test_byteimg_url_saved_as_png_from_content_type(self, no_sleep) -> None:
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = self._ok_response()
                m_req.exceptions = requests.exceptions
                local_path = dd._download_remote_material(
                    self.BYTEIMG_PNG_URL, td, "images", "双行", ".mp4"
                )
            assert local_path is not None
            assert local_path.endswith(".png")
            assert not local_path.endswith(".image")
            assert os.path.isfile(local_path)

    def test_mp4_content_type_uses_mp4_extension(self, no_sleep) -> None:
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = self._ok_response(
                    content=b"mp4", content_type="video/mp4"
                )
                m_req.exceptions = requests.exceptions
                local_path = dd._download_remote_material(
                    "https://cdn.example.com/v?id=1", td, "videos", "clip1", ".bin"
                )
            assert local_path is not None
            assert local_path.endswith(".mp4")

    def test_non200_404_does_not_retry(self, no_sleep) -> None:
        bad = MagicMock()
        bad.status_code = 404
        bad.close = MagicMock()
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = bad
                m_req.exceptions = requests.exceptions
                assert dd._download_remote_material(
                    "https://cdn.example.com/miss.png", td, "images", "x", ".png"
                ) is None
                assert m_req.get.call_count == 1


class TestRetryHelpers:
    @pytest.mark.parametrize(
        "status, expected",
        [
            (404, False),
            (400, False),
            (500, False),
            (408, True),
            (429, True),
            (502, True),
            (503, True),
            (504, True),
        ],
    )
    def test_is_retryable_http_status(self, status: int, expected: bool) -> None:
        assert dd._is_retryable_http_status(status) is expected

    def test_connection_refused_not_retryable(self) -> None:
        exc = requests.exceptions.ConnectionError("Connection refused")
        assert dd._is_retryable_request_exception(exc) is False

    def test_read_timeout_retryable(self) -> None:
        exc = requests.exceptions.ReadTimeout("read timed out")
        assert dd._is_retryable_request_exception(exc) is True


class TestDownloadRemoteFile:
    def _ok_response(self, content: bytes = b"data") -> MagicMock:
        r = MagicMock()
        r.status_code = 200
        r.iter_content = MagicMock(return_value=[content])
        return r

    def test_succeeds_first_request(self, no_sleep) -> None:
        out = os.path.join(tempfile.gettempdir(), "t_dl_first.bin")
        try:
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = self._ok_response()
                m_req.exceptions = requests.exceptions
                assert dd._download_remote_file("https://x.test/a.mp4", out) is True
                m_req.get.assert_called_once()
            with open(out, "rb") as f:
                assert f.read() == b"data"
        finally:
            if os.path.isfile(out):
                os.remove(out)

    def test_retries_then_success_on_timeout(self, no_sleep) -> None:
        calls = []

        def side_effect(*_a, **_kw):
            calls.append(1)
            if len(calls) < 3:
                raise requests.exceptions.ReadTimeout("read timed out")
            return self._ok_response()

        out = os.path.join(tempfile.gettempdir(), "t_dl_retry.bin")
        try:
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = side_effect
                m_req.exceptions = requests.exceptions
                assert dd._download_remote_file("https://x.test/b.mp4", out) is True
            assert len(calls) == 3
        finally:
            if os.path.isfile(out):
                os.remove(out)

    def test_returns_false_immediately_on_connection_refused(self, no_sleep) -> None:
        with patch.object(dd, "requests") as m_req:
            m_req.get.side_effect = requests.exceptions.ConnectionError("Connection refused")
            m_req.exceptions = requests.exceptions
            out = os.path.join(tempfile.gettempdir(), "t_dl_fail.bin")
            assert dd._download_remote_file("https://x.test/c.mp4", out) is False
            assert m_req.get.call_count == 1

    def test_non200_404_does_not_retry(self, no_sleep) -> None:
        bad = MagicMock()
        bad.status_code = 404
        bad.close = MagicMock()
        out = os.path.join(tempfile.gettempdir(), "t_dl_404.bin")
        with patch.object(dd, "requests") as m_req:
            m_req.get.return_value = bad
            m_req.exceptions = requests.exceptions
            assert dd._download_remote_file("https://x.test/miss.mp4", out) is False
            assert m_req.get.call_count == 1
        bad.close.assert_not_called()

    def test_non200_retries_then_success(self, no_sleep) -> None:
        bad = MagicMock()
        bad.status_code = 503
        good = self._ok_response()
        out = os.path.join(tempfile.gettempdir(), "t_dl_503.bin")
        try:
            with patch.object(dd, "_MAX_RETRIES", 2):
                with patch.object(dd, "requests") as m_req:
                    m_req.get.side_effect = [bad, bad, good]
                    m_req.exceptions = requests.exceptions
                    assert dd._download_remote_file("https://x.test/d.mp4", out) is True
        finally:
            if os.path.isfile(out):
                os.remove(out)


class TestLocalizeRemoteMaterialPaths:
    def test_no_materials_returns_true(self) -> None:
        assert dd.localize_remote_material_paths({}, "/tmp/x") is True

    def test_no_urls_returns_true(self) -> None:
        data = {"materials": {"audios": [], "videos": [{"path": "C:\\local\\x.mp4"}]}}
        assert dd.localize_remote_material_paths(data, "/tmp/y") is True

    @patch.object(dd, "_download_remote_material")
    def test_rewrites_path_on_success(self, m_dl) -> None:
        with tempfile.TemporaryDirectory() as td:
            url = "https://cdn.example.com/v.mp4"
            expected = os.path.join(td, "assets", "videos", "clip1.mp4")
            m_dl.return_value = expected
            data: dict = {
                "materials": {
                    "audios": [],
                    "videos": [
                        {
                            "path": url,
                            "material_name": "clip1",
                        }
                    ],
                }
            }
            assert dd.localize_remote_material_paths(data, td) is True
            m_dl.assert_called_once()
            new_path = data["materials"]["videos"][0]["path"]
            assert new_path == expected
            assert new_path.startswith(td)
            assert "assets" in new_path.replace("\\", "/")
            assert new_path.endswith(".mp4")

    @patch.object(dd, "_download_remote_material")
    def test_byteimg_png_url_saved_with_png_extension(self, m_dl) -> None:
        url = TestDownloadRemoteMaterial.BYTEIMG_PNG_URL
        with tempfile.TemporaryDirectory() as td:
            expected = os.path.join(td, "assets", "images", "双行.png")
            m_dl.return_value = expected
            data: dict = {
                "materials": {
                    "audios": [],
                    "videos": [
                        {
                            "path": url,
                            "type": "photo",
                            "material_name": "双行",
                        }
                    ],
                }
            }
            assert dd.localize_remote_material_paths(data, td) is True
            new_path = data["materials"]["videos"][0]["path"]
            assert new_path == expected
            assert new_path.endswith(".png")
            assert not new_path.endswith(".image")
            m_dl.assert_called_once_with(url, td, "images", "双行", ".mp4")

    @patch.object(dd, "_download_remote_material", return_value=None)
    def test_returns_false_when_download_fails(self, m_dl) -> None:
        with tempfile.TemporaryDirectory() as td:
            url = "https://cdn.example.com/miss.mp4"
            data: dict = {
                "materials": {
                    "audios": [],
                    "videos": [{"path": url, "id": "1"}],
                }
            }
            assert dd.localize_remote_material_paths(data, td) is False
            assert data["materials"]["videos"][0]["path"] == url

    @patch.object(dd, "_download_remote_material")
    def test_same_url_shared_across_items(self, m_dl) -> None:
        u = "https://cdn.example.com/same.mp3"
        with tempfile.TemporaryDirectory() as td:
            shared = os.path.join(td, "assets", "audios", "a.mp3")
            m_dl.return_value = shared
            data: dict = {
                "materials": {
                    "audios": [
                        {"path": u, "name": "a"},
                        {"path": u, "name": "b"},
                    ],
                    "videos": [],
                }
            }
            assert dd.localize_remote_material_paths(data, td) is True
            assert m_dl.call_count == 1
            p0 = data["materials"]["audios"][0]["path"]
            p1 = data["materials"]["audios"][1]["path"]
            assert p0 == p1
            assert p0.startswith(td)


class TestUpdateJsonFilePaths:
    def test_skips_write_when_localize_fails(self) -> None:
        body = {
            "materials": {"audios": [], "videos": []},
            "duration": 1000,
        }
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "draft_content.json")
            original = json.dumps(body, ensure_ascii=False)
            with open(path, "w", encoding="utf-8") as f:
                f.write(original)

            with patch.object(dd, "localize_remote_material_paths", return_value=False):
                assert (
                    dd.update_json_file_paths(path, td, "20260101120000abc")
                    is False
                )

            with open(path, "r", encoding="utf-8") as f:
                assert f.read() == original

    @patch.object(dd, "localize_remote_material_paths", return_value=True)
    @patch.object(dd, "config")
    def test_writes_when_localize_ok(self, m_config, m_loc) -> None:
        m_config.DRAFT_SAVE_PATH = "D:/mock/draft"
        base = {
            "materials": {"audios": [], "videos": []},
        }
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "draft_content.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(base, f, ensure_ascii=False)
            did = "20260101120000abc"
            assert dd.update_json_file_paths(path, td, did) is True
            m_loc.assert_called_once()
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert "materials" in data
            assert isinstance(data["materials"], dict)


class TestDownloadSingleFile:
    """download_single_file：流式写入 + 超时与关闭行为；路径与结果应与优化前语义一致。"""

    _BASE = "https://capcut.example.com"
    _TIMEOUT = (
        dd._REQUEST_CONNECT_TIMEOUT,
        dd._REQUEST_READ_TIMEOUT,
    )

    def _stream_response(
        self,
        chunks: list,
        status: int = 200,
    ) -> MagicMock:
        r = MagicMock()
        r.status_code = status
        r.iter_content = MagicMock(side_effect=lambda chunk_size=8192: iter(chunks))
        r.close = MagicMock()
        return r

    def test_success_writes_concatenated_chunks_and_relative_path(self, no_sleep) -> None:
        """URL 中带草稿 ID 时，相对路径为 draft_id 之后的路径段；内容与分块顺序一致。"""
        file_url = (
            f"{self._BASE}/app/output/draft/20251204214904ccb1af38/Resources/pic.png"
        )
        with tempfile.TemporaryDirectory() as td:
            resp = self._stream_response([b"hel", b"lo"])
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = resp
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is True

            expected = os.path.join(td, "Resources", "pic.png")
            assert os.path.isfile(expected)
            with open(expected, "rb") as f:
                assert f.read() == b"hello"

            m_req.get.assert_called_once_with(
                file_url,
                timeout=self._TIMEOUT,
                stream=True,
            )
            resp.close.assert_called_once()

    def test_fallback_relative_path_without_draft_segment(self, no_sleep) -> None:
        """路径中无草稿 ID 段时，与原先一致：使用 path 第一段子路径之后部分。"""
        file_url = f"{self._BASE}/static/assets/logo.bin"
        with tempfile.TemporaryDirectory() as td:
            resp = self._stream_response([b"z"])
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = resp
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is True

            expected = os.path.join(td, "static", "assets", "logo.bin")
            assert os.path.isfile(expected)
            with open(expected, "rb") as f:
                assert f.read() == b"z"

    def test_non200_returns_false_and_closes(self, no_sleep) -> None:
        """非网关类 4xx/5xx 不重试，立即失败并关闭响应。"""
        file_url = f"{self._BASE}/app/output/draft/20251204214904ccb1af38/x.bin"
        with tempfile.TemporaryDirectory() as td:
            resp = self._stream_response([], status=404)
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = resp
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is False
            resp.close.assert_called_once()

    def test_gateway_503_retries_until_exhausted(self, no_sleep) -> None:
        """503 退避重试，耗尽后与网络重试一致共 6 次请求。"""
        file_url = f"{self._BASE}/app/output/draft/20251204214904ccb1af38/x.bin"
        with tempfile.TemporaryDirectory() as td:
            resp = self._stream_response([], status=503)
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = resp
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is False
                assert m_req.get.call_count == 6
            assert resp.close.call_count == 6

    def test_retries_then_success_on_read_timeout(self, no_sleep) -> None:
        calls: list = []

        def side_effect(*_a, **_kw):
            calls.append(1)
            if len(calls) < 3:
                raise requests.exceptions.ReadTimeout("stalled")
            return self._stream_response([b"ok"])

        file_url = (
            f"{self._BASE}/app/output/draft/20251204214904ccb1af38/data.bin"
        )
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = side_effect
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is True
            assert len(calls) == 3
            out = os.path.join(td, "data.bin")
            with open(out, "rb") as f:
                assert f.read() == b"ok"

    def test_connection_refused_does_not_retry(self, no_sleep) -> None:
        file_url = (
            f"{self._BASE}/app/output/draft/20251204214904ccb1af38/miss.bin"
        )
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = requests.exceptions.ConnectionError(
                    "Connection refused"
                )
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is False
                assert m_req.get.call_count == 1

    def test_returns_false_after_exhausting_retries(self, no_sleep) -> None:
        file_url = (
            f"{self._BASE}/app/output/draft/20251204214904ccb1af38/miss.bin"
        )
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = requests.exceptions.ConnectionError("down")
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is False
                # retry_count 0..5 共 6 次尝试后放弃（与原先 max_retries=5 语义一致）
                assert m_req.get.call_count == 6

    @patch.object(dd, "update_json_file_paths")
    def test_plain_file_does_not_touch_json_paths(self, m_upd, no_sleep) -> None:
        file_url = (
            f"{self._BASE}/app/output/draft/20251204214904ccb1af38/only.bin"
        )
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = self._stream_response([b"\x00"])
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is True
            m_upd.assert_not_called()

    @patch.object(dd, "update_json_file_paths", return_value=True)
    def test_json_files_invoke_path_update(self, m_upd, no_sleep) -> None:
        file_url = (
            f"{self._BASE}/app/output/draft/20251204214904ccb1af38/"
            f"draft_content.json"
        )
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = self._stream_response([b"{}\n"])
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is True
            m_upd.assert_called_once()
            call_kw = m_upd.call_args
            assert call_kw[0][1] == td
            assert call_kw[0][2] == "20251204214904ccb1af38"

    @patch.object(dd, "update_json_file_paths", return_value=False)
    def test_json_update_failure_returns_false(self, m_upd, no_sleep) -> None:
        file_url = (
            f"{self._BASE}/app/output/draft/20251204214904ccb1af38/"
            f"draft_info.json"
        )
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = self._stream_response([b"{}\n"])
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is False


class TestExecuteDownload:
    """execute_download：超时 + 流式写入 + 关闭连接。"""

    _TIMEOUT = (
        dd._REQUEST_CONNECT_TIMEOUT,
        dd._REQUEST_READ_TIMEOUT,
    )

    def test_streams_body_to_default_filename_and_closes(self, no_sleep) -> None:
        draft_url = "https://api.example.com/get?draft_id=x"
        did = "mydraftid001"
        with tempfile.TemporaryDirectory() as td:
            r = MagicMock()
            r.status_code = 200
            r.headers = {}
            r.iter_content = MagicMock(
                side_effect=lambda chunk_size=8192: iter([b"a", b"bc"])
            )
            r.close = MagicMock()
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = r
                m_req.exceptions = requests.exceptions
                assert dd.execute_download(draft_url, td, did) is True

            out = os.path.join(td, f"{did}.draft")
            with open(out, "rb") as f:
                assert f.read() == b"abc"
            m_req.get.assert_called_once_with(
                draft_url,
                timeout=self._TIMEOUT,
                stream=True,
            )
            r.close.assert_called_once()

    def test_non200_returns_false(self, no_sleep) -> None:
        r = MagicMock()
        r.status_code = 500
        r.close = MagicMock()
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = r
                m_req.exceptions = requests.exceptions
                assert dd.execute_download("https://u", td, "d") is False
        r.close.assert_called_once()

    def test_request_exception_returns_false(self, no_sleep) -> None:
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = requests.exceptions.ConnectTimeout("t")
                m_req.exceptions = requests.exceptions
                assert dd.execute_download("https://u", td, "d") is False
