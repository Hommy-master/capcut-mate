"""延迟删除队列与定时清扫。"""
import os
import tempfile
from unittest.mock import patch

import pytest

from src.utils import deferred_delete as dd


@pytest.fixture(autouse=True)
def _clear_queue():
    dd.clear_pending_for_tests()
    yield
    dd.clear_pending_for_tests()


class TestDeferredDeleteQueue:
    def test_enqueue_and_delete_file(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "a.mp4")
            open(path, "wb").close()
            dd.enqueue_path(path, is_dir=False)
            assert dd.pending_count() == 1

            removed, remaining = dd.run_pending_deletes()

            assert removed == 1
            assert remaining == 0
            assert not os.path.exists(path)

    def test_missing_file_removed_from_queue(self) -> None:
        dd.enqueue_path("/nonexistent/path/file.mp4", is_dir=False)
        removed, remaining = dd.run_pending_deletes()
        assert removed == 1
        assert remaining == 0

    def test_locked_file_stays_in_queue_until_success(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "locked.mp4")
            open(path, "wb").close()
            dd.enqueue_path(path, is_dir=False)

            calls = {"n": 0}
            real_remove = os.remove

            def flaky_remove(p: str) -> None:
                calls["n"] += 1
                if calls["n"] < 2:
                    raise PermissionError("in use")
                real_remove(p)

            with patch("os.remove", side_effect=flaky_remove):
                r1, rem1 = dd.run_pending_deletes()
                assert r1 == 0
                assert rem1 == 1
                assert os.path.exists(path)

                r2, rem2 = dd.run_pending_deletes()
                assert r2 == 1
                assert rem2 == 0
                assert not os.path.exists(path)

    def test_delete_directory(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sub = os.path.join(td, "draft_dir")
            os.makedirs(sub)
            open(os.path.join(sub, "x.txt"), "w").close()
            dd.enqueue_path(sub, is_dir=True)
            removed, remaining = dd.run_pending_deletes()
            assert removed == 1
            assert remaining == 0
            assert not os.path.exists(sub)

    def test_dequeue_path_removes_pending_entry(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            sub = os.path.join(td, "draft_dir")
            os.makedirs(sub)
            dd.enqueue_path(sub, is_dir=True)
            assert dd.pending_count() == 1

            assert dd.dequeue_path(sub) is True
            assert dd.pending_count() == 0

            removed, remaining = dd.run_pending_deletes()
            assert removed == 0
            assert remaining == 0
            assert os.path.exists(sub)

    def test_dequeue_path_noop_when_not_enqueued(self) -> None:
        assert dd.dequeue_path("/nonexistent/draft") is False
        assert dd.pending_count() == 0


class TestVideoTaskManagerDeferredCleanup:
    def test_cleanup_enqueues_mp4_and_draft_dir(self) -> None:
        from datetime import datetime

        from src.utils.video_task_manager import (
            TaskStatus,
            VideoGenTask,
            VideoGenTaskManager,
        )

        with tempfile.TemporaryDirectory() as td:
            mp4 = os.path.join(td, "out.mp4")
            open(mp4, "wb").close()
            draft_root = os.path.join(td, "drafts")
            draft_dir = os.path.join(draft_root, "d1")
            os.makedirs(draft_dir)

            task = VideoGenTask(
                draft_url="http://example/openapi?draft_id=d1",
                draft_id="d1",
                status=TaskStatus.PROCESSING,
                created_at=datetime.now(),
                outfile=mp4,
                export_outfile_history=[mp4],
            )

            with patch("src.utils.video_task_manager.config") as cfg:
                cfg.DRAFT_SAVE_PATH = draft_root
                VideoGenTaskManager()._cleanup_files(task)

            assert os.path.exists(mp4)
            assert os.path.exists(draft_dir)
            assert dd.pending_count() == 2
            pending = dd.list_pending_paths()
            assert dd._normalize_path(mp4) in pending
            assert dd._normalize_path(draft_dir) in pending

            dd.run_pending_deletes()
            assert not os.path.exists(mp4)
            assert not os.path.exists(draft_dir)
