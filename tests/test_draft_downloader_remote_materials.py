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

    def test_returns_false_after_exhausting_retries(self, no_sleep) -> None:
        with patch.object(dd, "_MAX_RETRIES", 2):
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = requests.exceptions.ConnectionError("refused")
                m_req.exceptions = requests.exceptions
                out = os.path.join(tempfile.gettempdir(), "t_dl_fail.bin")
                assert dd._download_remote_file("https://x.test/c.mp4", out) is False
                assert m_req.get.call_count == 3

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

    @patch.object(dd, "_download_remote_file", return_value=True)
    def test_rewrites_path_on_success(self, m_dl) -> None:
        with tempfile.TemporaryDirectory() as td:
            url = "https://cdn.example.com/v.mp4"
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
            assert new_path.startswith(td)
            assert "assets" in new_path.replace("\\", "/")
            assert new_path.endswith(".mp4")

    @patch.object(dd, "_download_remote_file", return_value=False)
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

    @patch.object(dd, "_download_remote_file", return_value=True)
    def test_same_url_shared_across_items(self, m_dl) -> None:
        u = "https://cdn.example.com/same.mp3"
        with tempfile.TemporaryDirectory() as td:
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
