"""草稿下载重构：单草稿并发、content.json 原子写、断点重试与耗时日志。"""
import threading
import time
from unittest.mock import MagicMock, patch

import pytest
import requests

import src.utils.draft_downloader as dd


def _stream_response(chunks, status: int = 200, raise_after=None) -> MagicMock:
    r = MagicMock()
    r.status_code = status
    r.headers = {}
    r.close = MagicMock()

    def iter_content(chunk_size=8192):
        for chunk in chunks:
            yield chunk
        if raise_after is not None:
            raise raise_after

    r.iter_content = iter_content
    return r


class TestConcurrentFileDownloads:
    def test_downloads_up_to_six_files_at_once(self, tmp_path) -> None:
        files = [
            f"https://capcut.example.com/app/output/draft/20251204214904ccb1af38/assets/{i}.bin"
            for i in range(12)
        ]
        lock = threading.Lock()
        barrier = threading.Barrier(dd.DRAFT_FILE_DOWNLOAD_MAX_CONCURRENT)
        active = 0
        peak = 0

        def fake_download(file_url, target_dir, **kwargs) -> None:
            nonlocal active, peak
            with lock:
                active += 1
                peak = max(peak, active)
            try:
                # 只有 6 个 worker 同时到达时 barrier 才会放行；低于 6 会超时。
                barrier.wait(timeout=3)
            except threading.BrokenBarrierError:
                pass
            finally:
                with lock:
                    active -= 1

        with patch.object(dd, "_download_single_file", side_effect=fake_download):
            with patch.object(dd, "_localize_draft_meta_info"):
                with patch.object(dd, "trigger_directory_scan_with_robocopy"):
                    dd._download_all_files(
                        files, str(tmp_path), "20251204214904ccb1af38"
                    )

        assert peak == dd.DRAFT_FILE_DOWNLOAD_MAX_CONCURRENT == 6

    def test_failure_sets_abort_and_cancels_remaining(self, tmp_path) -> None:
        """一个文件失败后，排队中的任务不再发起下载（保持快速失败）。"""
        files = [
            f"https://capcut.example.com/app/output/draft/20251204214904ccb1af38/assets/{i}.bin"
            for i in range(12)
        ]
        calls: list = []
        abort_events: list = []
        first_started = threading.Event()

        def fake_download(file_url, target_dir, **kwargs) -> None:
            calls.append(file_url)
            abort_events.append(kwargs.get("abort_event"))
            first_started.set()
            raise dd.DraftDownloadAbort(
                dd.DraftDownloadFailureKind.NETWORK_RETRY_EXHAUSTED,
                detail="boom",
                url=file_url,
            )

        with patch.object(dd, "_download_single_file", side_effect=fake_download):
            with patch.object(dd, "_localize_draft_meta_info"):
                with patch.object(dd, "trigger_directory_scan_with_robocopy"):
                    with pytest.raises(dd.DraftDownloadAbort):
                        dd._download_all_files(
                            files, str(tmp_path), "20251204214904ccb1af38"
                        )

        assert first_started.is_set()
        assert len(calls) < len(files)
        assert all(event.is_set() for event in abort_events)

    def test_abort_event_stops_stream_and_keeps_partial(self, tmp_path) -> None:
        """中止时保留已落盘的 chunk，下次续传可从断点继续。"""
        abort_event = threading.Event()

        def chunks():
            yield b"first"
            abort_event.set()
            yield b"second"

        response = MagicMock()
        response.iter_content = lambda chunk_size=8192: chunks()
        target = tmp_path / "assets" / "big.mp4"

        with pytest.raises(dd._DownloadCancelled):
            dd._write_http_body_to_file(
                response, str(target), append=False, abort_event=abort_event
            )

        assert target.read_bytes() == b"first"


class TestDraftConcurrencyLimit:
    def test_at_most_three_drafts_download_at_once(self, tmp_path) -> None:
        barrier = threading.Barrier(dd._MAX_CONCURRENT_DRAFT_DOWNLOADS)
        lock = threading.Lock()
        active = 0
        peak = 0
        errors: list = []

        def fake_download_all(files, target_dir, draft_id, **kwargs) -> None:
            nonlocal active, peak
            with lock:
                active += 1
                peak = max(peak, active)
            try:
                barrier.wait(timeout=3)
            except threading.BrokenBarrierError:
                pass
            finally:
                with lock:
                    active -= 1

        def run(index: int) -> None:
            try:
                dd.download_draft_with_result(
                    f"https://api.example.com/get?draft_id=draft{index:03d}",
                    save_path=str(tmp_path),
                )
            except Exception as exc:  # noqa: BLE001 - 线程内异常带回主线程
                errors.append(exc)

        threads = [threading.Thread(target=run, args=(i,)) for i in range(6)]
        with patch.object(dd, "_get_draft_files_list", return_value=["https://x/a.mp4"]):
            with patch.object(dd, "_download_all_files", side_effect=fake_download_all):
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join(timeout=10)

        assert errors == []
        assert peak == dd._MAX_CONCURRENT_DRAFT_DOWNLOADS == 3


class TestContentJsonWriteSafety:
    def test_safe_write_file_keeps_old_file_when_replace_fails(self, tmp_path) -> None:
        path = tmp_path / "draft_content.json"
        path.write_text('{"old": true}', encoding="utf-8")

        with patch.object(dd.os, "replace", side_effect=OSError("disk full")):
            with pytest.raises(OSError):
                dd.safe_write_file(str(path), '{"new": true}', is_binary=False)

        # os.replace 失败时目标文件保持原样，且临时文件被清理。
        assert path.read_text(encoding="utf-8") == '{"old": true}'
        assert list(tmp_path.glob(".*.tmp")) == []

    def test_concurrent_writes_never_interleave(self, tmp_path) -> None:
        path = tmp_path / "draft_content.json"
        payloads = [
            f'{{"writer": {i}, "padding": "'.encode()
            + (str(i % 10) * 200_000).encode()
            + b'"}'
            for i in range(8)
        ]
        barrier = threading.Barrier(len(payloads))
        errors: list = []

        def writer(payload: bytes) -> None:
            try:
                barrier.wait(timeout=3)
                dd.safe_write_file(str(path), payload, is_binary=True)
            except Exception as exc:  # noqa: BLE001 - 线程内异常带回主线程
                errors.append(exc)

        threads = [
            threading.Thread(target=writer, args=(payload,)) for payload in payloads
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)

        assert errors == []
        # 最终文件必须是某一次完整写入，不能是两次写入拼接后的损坏内容。
        assert path.read_bytes() in payloads

    def test_update_json_file_paths_writes_valid_json_under_lock(self, tmp_path) -> None:
        path = tmp_path / "draft_content.json"
        path.write_text('{"materials": {"audios": [], "videos": []}}', encoding="utf-8")

        with patch.object(dd, "_localize_remote_material_paths"):
            dd._update_json_file_paths(str(path), str(tmp_path), "20251204214904ccb1af38")

        import json

        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data["materials"], dict)


class TestRetryResume:
    _BASE = "https://capcut.example.com"
    _DRAFT = "20251204214904ccb1af38"

    def _url(self, name: str) -> str:
        return f"{self._BASE}/app/output/draft/{self._DRAFT}/{name}"

    def test_ten_retries_all_resume_from_breakpoint(self, tmp_path) -> None:
        """连续 10 次网络中断后第 11 次成功；每次重试都带正确的 Range 偏移。"""
        file_url = self._url("assets/big.mp4")
        responses = [
            _stream_response(
                [b"x"],
                status=206 if i > 0 else 200,
                raise_after=requests.exceptions.ChunkedEncodingError("truncated"),
            )
            for i in range(dd._MAX_RETRIES)
        ]
        responses.append(_stream_response([b"END"], status=206))

        with patch.object(dd, "time") as m_time:
            m_time.sleep = MagicMock()
            m_time.monotonic = time.monotonic
            with patch.object(dd, "requests") as m_req:
                m_req.get.side_effect = responses
                m_req.exceptions = requests.exceptions
                assert dd.download_single_file(file_url, str(tmp_path)) is True

        assert m_req.get.call_count == dd._MAX_RETRIES + 1
        for offset, call in enumerate(m_req.get.call_args_list[1:], start=1):
            headers = call.kwargs.get("headers") or {}
            assert headers.get("Range") == f"bytes={offset}-"

        target = tmp_path / "assets" / "big.mp4"
        assert target.read_bytes() == b"x" * dd._MAX_RETRIES + b"END"


class TestDurationLogging:
    def test_download_all_files_logs_elapsed(self, tmp_path) -> None:
        url = "https://capcut.example.com/app/output/draft/20251204214904ccb1af38/assets/a.bin"
        with patch.object(dd, "_download_single_file"):
            with patch.object(dd, "_localize_draft_meta_info"):
                with patch.object(dd, "trigger_directory_scan_with_robocopy"):
                    with patch.object(dd, "logger") as m_log:
                        dd._download_all_files(
                            [url], str(tmp_path), "20251204214904ccb1af38"
                        )

        messages = [str(call.args[0]) for call in m_log.info.call_args_list if call.args]
        assert any("download finished in %.2fs" in msg for msg in messages)

    def test_download_draft_logs_elapsed(self, tmp_path) -> None:
        draft_url = (
            "https://api.example.com/get_draft?draft_id=20251204214904ccb1af38"
        )
        with patch.object(dd, "prepare_target_directory", return_value=str(tmp_path)):
            with patch.object(dd, "dequeue_path"):
                with patch.object(dd, "_get_draft_files_list", return_value=["https://x/a.mp4"]):
                    with patch.object(dd, "_download_all_files"):
                        with patch.object(dd, "logger") as m_log:
                            result = dd.download_draft_with_result(
                                draft_url, save_path=str(tmp_path)
                            )

        assert result.ok is True
        assert any(
            "download %s in %.2fs" in str(call.args[0]) and "finished" in call.args
            for call in m_log.info.call_args_list
            if call.args
        )
