"""云渲染三阶段性能统计：下载 / 导出 / 上传耗时日志。"""
import time
from datetime import datetime
from unittest.mock import MagicMock, patch

from src.utils.video_task_manager import (
    TaskStatus,
    VideoGenTask,
    VideoGenTaskManager,
)


def _task() -> VideoGenTask:
    return VideoGenTask(
        draft_url="http://example/openapi?draft_id=d_timing",
        draft_id="d_timing",
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
    )


def _log_messages(mock_logger) -> list[str]:
    return [str(call.args[0]) for call in mock_logger.info.call_args_list if call.args]


class TestDownloadPhaseTiming:
    @patch("src.utils.video_task_manager.sys.platform", "win32")
    @patch.object(VideoGenTaskManager, "_assign_export_outfile", return_value=None)
    @patch.object(VideoGenTaskManager, "_ensure_export_balance", return_value="")
    @patch.object(VideoGenTaskManager, "_check_draft_duration", return_value=True)
    @patch.object(VideoGenTaskManager, "_ensure_local_draft_ready", return_value="")
    @patch.object(VideoGenTaskManager, "_download_draft")
    def test_download_phase_records_timing_and_logs(
        self, m_download, _m_ready, _m_duration, _m_balance, _m_outfile
    ) -> None:
        m_download.side_effect = lambda task: (time.sleep(0.02), "")[1]

        with patch("src.utils.video_task_manager.logger") as m_logger:
            task = _task()
            assert VideoGenTaskManager()._phase_download_and_prepare(task) == ""

        assert task.download_seconds >= 0.02
        assert task.download_phase_seconds >= task.download_seconds
        assert any("phase=download" in msg for msg in _log_messages(m_logger))


class TestUploadPhaseTiming:
    @patch.object(VideoGenTaskManager, "_cleanup_files")
    @patch.object(VideoGenTaskManager, "_handle_result", return_value=("url", ""))
    @patch.object(VideoGenTaskManager, "_calculate_and_charge")
    @patch.object(VideoGenTaskManager, "_upload_video_to_cos")
    def test_upload_phase_records_timing_and_logs(
        self, m_upload, _m_charge, _m_result, _m_cleanup
    ) -> None:
        m_upload.side_effect = lambda outfile: (time.sleep(0.02), ("url", False))[1]

        with patch("src.utils.video_task_manager.logger") as m_logger:
            task = _task()
            upload_url, error = VideoGenTaskManager()._phase_cos_upload_finalize(task)

        assert (upload_url, error) == ("url", "")
        assert task.upload_seconds >= 0.02
        assert task.upload_phase_seconds >= task.upload_seconds
        assert any("phase=upload" in msg for msg in _log_messages(m_logger))


class TestTotalTimingLog:
    @patch("src.utils.video_task_manager.save_completed_result")
    def test_terminal_task_logs_all_phase_timings(self, _m_save) -> None:
        task = _task()
        task.status = TaskStatus.FAILED
        task.error_message = "boom"
        task.performance_started_at = time.monotonic() - 1.0
        task.download_seconds = 0.1
        task.download_phase_seconds = 0.2
        task.export_seconds = 0.3
        task.export_lock_wait_seconds = 0.05
        task.upload_seconds = 0.4
        task.upload_phase_seconds = 0.5

        with patch("src.utils.video_task_manager.logger") as m_logger:
            VideoGenTaskManager()._persist_terminal_task(task)

        total_call = next(
            call
            for call in m_logger.info.call_args_list
            if call.args and "Render total timing" in str(call.args[0])
        )
        assert total_call.args[1] == task.draft_id
        assert total_call.args[2] == "failed"
        assert total_call.args[3] == 0.1
        assert total_call.args[4] == 0.2
        assert total_call.args[5] == 0.3
        assert total_call.args[6] == 0.05
        assert total_call.args[7] == 0.4
        assert total_call.args[8] == 0.5
        assert total_call.args[9] > 0.9
        assert total_call.args[10] == "boom"
