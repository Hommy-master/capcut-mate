"""导出 rename src None 错误时仅重试导出阶段（复用已下载草稿）。"""
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from src.utils.video_task_manager import (
    EXPORT_RENAME_SRC_NONE_ERROR_MARKER,
    EXPORT_RENAME_SRC_NONE_MAX_RETRIES,
    TaskStatus,
    VideoGenTask,
    VideoGenTaskManager,
)


def _task(draft_id: str = "d_retry") -> VideoGenTask:
    return VideoGenTask(
        draft_url=f"http://example/openapi?draft_id={draft_id}",
        draft_id=draft_id,
        status=TaskStatus.PROCESSING,
        created_at=datetime.now(),
        outfile="/tmp/first.mp4",
    )


RENAME_ERROR = (
    f"导出草稿失败: {EXPORT_RENAME_SRC_NONE_ERROR_MARKER}"
)


class TestExportRenameSrcNoneRetry:
    def test_is_export_rename_src_none_error(self) -> None:
        mgr = VideoGenTaskManager()
        assert mgr._is_export_rename_src_none_error(RENAME_ERROR) is True
        assert mgr._is_export_rename_src_none_error("导出草稿失败: other") is False

    @patch.object(VideoGenTaskManager, "_export_video")
    def test_retries_twice_then_succeeds(self, m_export: MagicMock) -> None:
        rename_exc = Exception(EXPORT_RENAME_SRC_NONE_ERROR_MARKER)
        m_export.side_effect = [rename_exc, rename_exc, True]
        task = _task()

        with patch.object(
            VideoGenTaskManager, "_prepare_export_retry_outfile"
        ) as m_prepare:
            err = VideoGenTaskManager()._phase_export_only(task)

        assert err == ""
        assert m_export.call_count == 3
        assert m_prepare.call_count == 2

    @patch.object(VideoGenTaskManager, "_export_video")
    def test_exhausts_retries_returns_last_error(self, m_export: MagicMock) -> None:
        rename_exc = Exception(EXPORT_RENAME_SRC_NONE_ERROR_MARKER)
        m_export.side_effect = rename_exc
        task = _task()

        with patch.object(
            VideoGenTaskManager, "_prepare_export_retry_outfile"
        ) as m_prepare:
            err = VideoGenTaskManager()._phase_export_only(task)

        assert EXPORT_RENAME_SRC_NONE_ERROR_MARKER in err
        assert m_export.call_count == 1 + EXPORT_RENAME_SRC_NONE_MAX_RETRIES
        assert m_prepare.call_count == EXPORT_RENAME_SRC_NONE_MAX_RETRIES

    @patch.object(VideoGenTaskManager, "_export_video")
    def test_other_export_error_not_retried(self, m_export: MagicMock) -> None:
        m_export.side_effect = Exception("导出超时")
        task = _task()

        with patch.object(
            VideoGenTaskManager, "_prepare_export_retry_outfile"
        ) as m_prepare:
            err = VideoGenTaskManager()._phase_export_only(task)

        assert err == "导出草稿失败: 导出超时"
        assert m_export.call_count == 1
        m_prepare.assert_not_called()

    @patch.object(VideoGenTaskManager, "_export_video", return_value=False)
    def test_export_returns_false_not_retried(self, m_export: MagicMock) -> None:
        task = _task()
        err = VideoGenTaskManager()._phase_export_only(task)
        assert err == "导出草稿失败"
        assert m_export.call_count == 1
