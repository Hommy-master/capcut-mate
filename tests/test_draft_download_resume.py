"""草稿下载：资源文件断点续传；JSON 等非资源仍整文件重下。"""
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


def _stream_response(
    chunks,
    status: int = 200,
    headers=None,
    raise_after=None,
) -> MagicMock:
    r = MagicMock()
    r.status_code = status
    r.headers = headers or {}
    r.close = MagicMock()

    def iter_content(chunk_size=8192):
        for chunk in chunks:
            yield chunk
        if raise_after is not None:
            raise raise_after

    r.iter_content = iter_content
    return r


def _range_from_call(call) -> str:
    headers = call.kwargs.get("headers") or {}
    return headers.get("Range", "")


class TestIsMediaResource:
    @pytest.mark.parametrize(
        "value",
        [
            "clip.mp4",
            "https://cdn.example.com/a.MP4?token=1",
            r"C:\draft\assets\videos\x.mov",
            "photo.PNG",
            "https://x.test/img.jpg",
            "audio.mp3",
            "track.wav",
            "pic.webp",
        ],
    )
    def test_media_extensions_are_detected(self, value: str) -> None:
        assert dd._is_media_resource(value) is True

    @pytest.mark.parametrize(
        "value",
        [
            "draft_content.json",
            "draft_meta_info.json",
            "https://cdn.example.com/app/output/draft/20251204214904ccb1af38/a.bin",
            "notes.txt",
            "https://x.test/foo.image?sig=1",
            "",
        ],
    )
    def test_non_media_extensions_are_excluded(self, value: str) -> None:
        assert dd._is_media_resource(value) is False


class TestResumeHelpers:
    def test_resume_headers_none_when_file_missing(self, tmp_path) -> None:
        headers, resume_from = dd._resume_request_headers(str(tmp_path / "miss.mp4"))
        assert headers is None
        assert resume_from == 0

    def test_resume_headers_use_existing_size(self, tmp_path) -> None:
        path = tmp_path / "part.mp4"
        path.write_bytes(b"hello")
        headers, resume_from = dd._resume_request_headers(str(path))
        assert resume_from == 5
        assert headers == {"Range": "bytes=5-"}

    def test_success_status_206_only_when_resuming(self) -> None:
        assert dd._is_download_success_status(200, 0) is True
        assert dd._is_download_success_status(200, 10) is True
        assert dd._is_download_success_status(206, 10) is True
        assert dd._is_download_success_status(206, 0) is False
        assert dd._is_download_success_status(404, 10) is False


class TestDownloadSingleFileResume:
    _BASE = "https://capcut.example.com"
    _DRAFT = "20251204214904ccb1af38"
    _TIMEOUT = (dd._REQUEST_CONNECT_TIMEOUT, dd._REQUEST_READ_TIMEOUT)
    _HEADERS = dd._REQUEST_HEADERS

    def _url(self, name: str) -> str:
        return f"{self._BASE}/app/output/draft/{self._DRAFT}/{name}"

    def test_first_media_request_has_no_range_header(self, no_sleep) -> None:
        """首次下载资源文件不带 Range，GET 形态与改造前一致。"""
        file_url = self._url("Resources/clip.mp4")
        with tempfile.TemporaryDirectory() as td:
            resp = _stream_response([b"ab", b"cd"])
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = resp
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is True
            m_req.get.assert_called_once_with(
                file_url,
                timeout=self._TIMEOUT,
                stream=True,
                headers=self._HEADERS,
            )
            out = os.path.join(td, "Resources", "clip.mp4")
            with open(out, "rb") as f:
                assert f.read() == b"abcd"

    def test_media_retry_sends_range_and_appends(self, no_sleep) -> None:
        """中途断开后，重试从已写入字节续传，206 响应追加到原文件。"""
        file_url = self._url("assets/clip.mp4")
        first = _stream_response(
            [b"hello"],
            raise_after=requests.exceptions.ChunkedEncodingError("truncated"),
        )
        second = _stream_response([b"world"], status=206)

        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = [first, second]
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is True

            assert m_req.get.call_count == 2
            assert "Range" not in (m_req.get.call_args_list[0].kwargs.get("headers") or {})
            assert _range_from_call(m_req.get.call_args_list[1]) == "bytes=5-"
            out = os.path.join(td, "assets", "clip.mp4")
            with open(out, "rb") as f:
                assert f.read() == b"helloworld"

    def test_media_retry_overwrites_when_server_ignores_range(self, no_sleep) -> None:
        """服务端忽略 Range 返回 200 时，整文件覆盖，避免拼出损坏文件。"""
        file_url = self._url("assets/clip.mp4")
        first = _stream_response(
            [b"hello"],
            raise_after=requests.exceptions.ChunkedEncodingError("truncated"),
        )
        second = _stream_response([b"FULLFILE"], status=200)

        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = [first, second]
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is True
            out = os.path.join(td, "assets", "clip.mp4")
            with open(out, "rb") as f:
                assert f.read() == b"FULLFILE"

    def test_json_retry_overwrites_without_range(self, no_sleep) -> None:
        """JSON 失败重试必须整文件重下，即使本地已有半成品也不发 Range。"""
        file_url = self._url("draft_meta_info.json")
        first = _stream_response(
            [b'{"x":'],
            raise_after=requests.exceptions.ChunkedEncodingError("truncated"),
        )
        second = _stream_response([b'{"ok": true}'])

        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = [first, second]
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is True

            second_headers = m_req.get.call_args_list[1].kwargs.get("headers") or {}
            assert "Range" not in second_headers
            out = os.path.join(td, "draft_meta_info.json")
            with open(out, "rb") as f:
                assert f.read() == b'{"ok": true}'

    def test_bin_retry_overwrites_without_range(self, no_sleep) -> None:
        file_url = self._url("assets/x.bin")
        first = _stream_response(
            [b"123"],
            raise_after=requests.exceptions.ReadTimeout("stalled"),
        )
        second = _stream_response([b"abc"])
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = [first, second]
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is True
            assert "Range" not in (m_req.get.call_args_list[1].kwargs.get("headers") or {})
            out = os.path.join(td, "assets", "x.bin")
            with open(out, "rb") as f:
                assert f.read() == b"abc"

    def test_image_resume_same_as_video(self, no_sleep) -> None:
        file_url = self._url("Resources/pic.png")
        first = _stream_response(
            [b"PNG"],
            raise_after=requests.exceptions.ChunkedEncodingError("truncated"),
        )
        second = _stream_response([b"DATA"], status=206)
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = [first, second]
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, td) is True
            assert _range_from_call(m_req.get.call_args_list[1]) == "bytes=3-"
            out = os.path.join(td, "Resources", "pic.png")
            with open(out, "rb") as f:
                assert f.read() == b"PNGDATA"


class TestDownloadRemoteMaterialResume:
    def test_extensionless_cdn_url_still_resumes(self, no_sleep) -> None:
        """无扩展名的图片 CDN URL 也走续传（本函数只下载素材）。"""
        url = "https://p3-bot-workflow-sign.byteimg.com/tos-cn-i-mdko3gqilj/foo.png~tplv.image?x=1"
        first = _stream_response(
            [b"img-"],
            headers={"Content-Type": "image/png"},
            raise_after=requests.exceptions.ChunkedEncodingError("truncated"),
        )
        second = _stream_response(
            [b"rest"],
            status=206,
            headers={"Content-Type": "image/png"},
        )
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = [first, second]
                m_req.exceptions = requests.exceptions
                path = dd._download_remote_material(url, td, "images", "双行", ".mp4")
            assert path is not None
            assert path.endswith(".png")
            with open(path, "rb") as f:
                assert f.read() == b"img-rest"
            assert _range_from_call(m_req.get.call_args_list[1]) == "bytes=4-"

    def test_first_material_request_has_no_range(self, no_sleep) -> None:
        url = "https://cdn.example.com/v?id=1"
        resp = _stream_response([b"mp4"], headers={"Content-Type": "video/mp4"})
        with tempfile.TemporaryDirectory() as td:
            with patch.object(dd, "requests") as m_req:
                m_req.get.return_value = resp
                m_req.exceptions = requests.exceptions
                path = dd._download_remote_material(url, td, "videos", "clip1", ".bin")
            assert path is not None
            first_headers = m_req.get.call_args.kwargs.get("headers") or {}
            assert "Range" not in first_headers
            m_req.get.assert_called_once()


class TestDownloadRemoteFileResume:
    def test_mp4_retry_appends_on_206(self, no_sleep) -> None:
        first = _stream_response(
            [b"AAA"],
            raise_after=requests.exceptions.ChunkedEncodingError("truncated"),
        )
        second = _stream_response([b"BBB"], status=206)
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "a.mp4")
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = [first, second]
                m_req.exceptions = requests.exceptions
                assert dd._download_remote_file("https://x.test/a.mp4", out) is True
            assert _range_from_call(m_req.get.call_args_list[1]) == "bytes=3-"
            with open(out, "rb") as f:
                assert f.read() == b"AAABBB"

    def test_non_media_remote_file_does_not_resume(self, no_sleep) -> None:
        first = _stream_response(
            [b"AAA"],
            raise_after=requests.exceptions.ChunkedEncodingError("truncated"),
        )
        second = _stream_response([b"ZZZ"])
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "a.bin")
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = [first, second]
                m_req.exceptions = requests.exceptions
                assert dd._download_remote_file("https://x.test/a.bin", out) is True
            assert "Range" not in (m_req.get.call_args_list[1].kwargs.get("headers") or {})
            with open(out, "rb") as f:
                assert f.read() == b"ZZZ"

