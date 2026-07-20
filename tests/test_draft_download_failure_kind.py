"""草稿下载失败分类：404/资源不可用 vs 网络重试耗尽。"""
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
import requests

import src.utils.draft_downloader as dd
from src.utils.video_task_manager import TaskStatus, VideoGenTask, VideoGenTaskManager


@pytest.fixture
def no_sleep():
    with patch.object(dd, "time") as m_time:
        m_time.sleep = MagicMock()
        yield m_time


def _task(draft_id: str = "d_fail") -> VideoGenTask:
    return VideoGenTask(
        draft_url=f"http://example/openapi?draft_id={draft_id}",
        draft_id=draft_id,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
    )


class TestFormatDraftDownloadFailureMessage:
    def test_network_retry_exhausted(self) -> None:
        result = dd.DraftDownloadResult(
            ok=False,
            kind=dd.DraftDownloadFailureKind.NETWORK_RETRY_EXHAUSTED,
        )
        assert (
            dd.format_draft_download_failure_message(result)
            == "草稿下载失败: 网络不稳定，已多次重试仍失败，请稍后重试"
        )

    def test_resource_unavailable_with_http_status(self) -> None:
        result = dd.DraftDownloadResult(
            ok=False,
            kind=dd.DraftDownloadFailureKind.RESOURCE_UNAVAILABLE,
            http_status=404,
        )
        assert (
            dd.format_draft_download_failure_message(result)
            == "草稿下载失败: 草稿或素材不存在/URL无效 (HTTP 404)"
        )

    def test_local_io(self) -> None:
        result = dd.DraftDownloadResult(
            ok=False,
            kind=dd.DraftDownloadFailureKind.LOCAL_IO,
        )
        assert (
            dd.format_draft_download_failure_message(result)
            == "草稿下载失败: 本地文件写入失败"
        )


class TestDownloadSingleFileFailureKind:
    _URL = "https://cdn.example.com/app/output/draft/20251204214904ccb1af38/a.bin"

    def test_404_is_resource_unavailable(self, no_sleep) -> None:
        bad = MagicMock()
        bad.status_code = 404
        bad.close = MagicMock()
        with patch.object(dd, "requests") as m_req:
            m_req.get.return_value = bad
            m_req.exceptions = requests.exceptions
            with pytest.raises(dd.DraftDownloadAbort) as ei:
                dd._download_single_file(self._URL, "/tmp/unused")
            assert ei.value.kind == dd.DraftDownloadFailureKind.RESOURCE_UNAVAILABLE
            assert ei.value.http_status == 404
            assert m_req.get.call_count == 1

    def test_503_exhausted_is_network_retry_exhausted(self, no_sleep) -> None:
        bad = MagicMock()
        bad.status_code = 503
        bad.headers = {}
        bad.close = MagicMock()
        with patch.object(dd, "requests") as m_req:
            m_req.get.return_value = bad
            m_req.exceptions = requests.exceptions
            with pytest.raises(dd.DraftDownloadAbort) as ei:
                dd._download_single_file(self._URL, "/tmp/unused")
            assert ei.value.kind == dd.DraftDownloadFailureKind.NETWORK_RETRY_EXHAUSTED
            assert ei.value.http_status == 503
            assert m_req.get.call_count == 6

    def test_timeout_exhausted_is_network_retry_exhausted(self, no_sleep) -> None:
        with patch.object(dd, "requests") as m_req:
            m_req.get.side_effect = requests.exceptions.ReadTimeout("read timed out")
            m_req.exceptions = requests.exceptions
            with pytest.raises(dd.DraftDownloadAbort) as ei:
                dd._download_single_file(self._URL, "/tmp/unused")
            assert ei.value.kind == dd.DraftDownloadFailureKind.NETWORK_RETRY_EXHAUSTED
            assert m_req.get.call_count == 6

    def test_connection_refused_is_resource_unavailable(self, no_sleep) -> None:
        with patch.object(dd, "requests") as m_req:
            m_req.get.side_effect = requests.exceptions.ConnectionError(
                "Connection refused"
            )
            m_req.exceptions = requests.exceptions
            with pytest.raises(dd.DraftDownloadAbort) as ei:
                dd._download_single_file(self._URL, "/tmp/unused")
            assert ei.value.kind == dd.DraftDownloadFailureKind.RESOURCE_UNAVAILABLE
            assert m_req.get.call_count == 1


class TestDownloadDraftWithResult:
    def test_invalid_draft_url(self) -> None:
        result = dd.download_draft_with_result("not-a-url")
        assert result.ok is False
        assert result.kind == dd.DraftDownloadFailureKind.RESOURCE_UNAVAILABLE
        assert dd.download_draft("not-a-url") is False

    def test_file_list_404(self, no_sleep) -> None:
        draft_id = "20251204214904ccb1af38"
        draft_url = f"https://api.example.com/get_draft?draft_id={draft_id}"
        bad = MagicMock()
        bad.status_code = 404
        bad.close = MagicMock()
        with patch.object(dd, "prepare_target_directory", return_value="/tmp/d"):
            with patch.object(dd, "dequeue_path"):
                with patch.object(dd, "requests") as m_req:
                    m_req.get.return_value = bad
                    m_req.exceptions = requests.exceptions
                    result = dd.download_draft_with_result(draft_url)
        assert result.ok is False
        assert result.kind == dd.DraftDownloadFailureKind.RESOURCE_UNAVAILABLE
        assert result.http_status == 404

    def test_file_list_503_exhausted(self, no_sleep) -> None:
        draft_id = "20251204214904ccb1af38"
        draft_url = f"https://api.example.com/get_draft?draft_id={draft_id}"
        bad = MagicMock()
        bad.status_code = 503
        bad.headers = {}
        bad.close = MagicMock()
        with patch.object(dd, "_MAX_RETRIES", 2):
            with patch.object(dd, "prepare_target_directory", return_value="/tmp/d"):
                with patch.object(dd, "dequeue_path"):
                    with patch.object(dd, "requests") as m_req:
                        m_req.get.return_value = bad
                        m_req.exceptions = requests.exceptions
                        result = dd.download_draft_with_result(draft_url)
        assert result.ok is False
        assert result.kind == dd.DraftDownloadFailureKind.NETWORK_RETRY_EXHAUSTED
        assert result.http_status == 503

    def test_bool_api_matches_with_result(self, no_sleep) -> None:
        draft_id = "20251204214904ccb1af38"
        draft_url = f"https://api.example.com/get_draft?draft_id={draft_id}"
        bad = MagicMock()
        bad.status_code = 404
        bad.close = MagicMock()
        with patch.object(dd, "prepare_target_directory", return_value="/tmp/d"):
            with patch.object(dd, "dequeue_path"):
                with patch.object(dd, "requests") as m_req:
                    m_req.get.return_value = bad
                    m_req.exceptions = requests.exceptions
                    assert dd.download_draft(draft_url) is False
                    assert dd.download_draft_with_result(draft_url).ok is False


class TestRemoteMaterialFailureKind:
    def test_404_resource_unavailable(self, no_sleep) -> None:
        bad = MagicMock()
        bad.status_code = 404
        bad.close = MagicMock()
        with patch.object(dd, "requests") as m_req:
            m_req.get.return_value = bad
            m_req.exceptions = requests.exceptions
            with pytest.raises(dd.DraftDownloadAbort) as ei:
                dd._download_remote_material_raising(
                    "https://cdn.example.com/miss.png",
                    "/tmp",
                    "images",
                    "x",
                    ".png",
                )
            assert ei.value.kind == dd.DraftDownloadFailureKind.RESOURCE_UNAVAILABLE
            assert ei.value.http_status == 404

    def test_timeout_exhausted_network(self, no_sleep) -> None:
        with patch.object(dd, "_MAX_RETRIES", 1):
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = requests.exceptions.ReadTimeout("t")
                m_req.exceptions = requests.exceptions
                with pytest.raises(dd.DraftDownloadAbort) as ei:
                    dd._download_remote_material_raising(
                        "https://cdn.example.com/x.mp4",
                        "/tmp",
                        "videos",
                        "c",
                        ".mp4",
                    )
                assert ei.value.kind == dd.DraftDownloadFailureKind.NETWORK_RETRY_EXHAUSTED


class TestVideoTaskManagerDownloadMessages:
    @patch("src.utils.video_task_manager.sys.platform", "win32")
    def test_resource_unavailable_message(self) -> None:
        result = dd.DraftDownloadResult(
            ok=False,
            kind=dd.DraftDownloadFailureKind.RESOURCE_UNAVAILABLE,
            http_status=404,
        )
        with patch(
            "src.utils.draft_downloader.download_draft_with_result",
            return_value=result,
        ):
            msg = VideoGenTaskManager()._download_draft(_task())
        assert msg == "草稿下载失败: 草稿或素材不存在/URL无效 (HTTP 404)"

    @patch("src.utils.video_task_manager.sys.platform", "win32")
    def test_network_retry_exhausted_message(self) -> None:
        result = dd.DraftDownloadResult(
            ok=False,
            kind=dd.DraftDownloadFailureKind.NETWORK_RETRY_EXHAUSTED,
        )
        with patch(
            "src.utils.draft_downloader.download_draft_with_result",
            return_value=result,
        ):
            msg = VideoGenTaskManager()._download_draft(_task())
        assert msg == "草稿下载失败: 网络不稳定，已多次重试仍失败，请稍后重试"

    @patch("src.utils.video_task_manager.sys.platform", "win32")
    def test_success_returns_empty(self) -> None:
        with patch(
            "src.utils.draft_downloader.download_draft_with_result",
            return_value=dd.DraftDownloadResult(ok=True),
        ):
            assert VideoGenTaskManager()._download_draft(_task()) == ""

    @patch("src.utils.video_task_manager.sys.platform", "win32")
    @patch.object(VideoGenTaskManager, "_assign_export_outfile")
    def test_phase_propagates_classified_message(self, m_out) -> None:
        fail_msg = "草稿下载失败: 网络不稳定，已多次重试仍失败，请稍后重试"
        with patch.object(
            VideoGenTaskManager, "_download_draft", return_value=fail_msg
        ):
            out = VideoGenTaskManager()._phase_download_and_prepare(_task())
        assert out == fail_msg
