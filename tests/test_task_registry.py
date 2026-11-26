"""终态任务内存回收：落库成功后才从 self.tasks 移除。"""
from datetime import datetime
from unittest.mock import patch

from src.utils.video_task_manager import (
    TaskStatus,
    VideoGenTask,
    VideoGenTaskManager,
)


def _task(draft_id: str) -> VideoGenTask:
    return VideoGenTask(
        draft_url=f"http://example/get_draft?draft_id={draft_id}",
        draft_id=draft_id,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
    )


class TestTerminalTaskRegistry:
    def test_terminal_task_removed_after_successful_persist(self) -> None:
        manager = VideoGenTaskManager()
        task = _task("reg_removed")
        task.status = TaskStatus.COMPLETED
        manager.tasks[task.draft_url] = task

        with patch(
            "src.utils.video_task_manager.save_completed_result"
        ) as m_save:
            manager._persist_terminal_task(task)

        m_save.assert_called_once()
        assert task.draft_url not in manager.tasks

    def test_terminal_task_kept_when_persist_fails(self) -> None:
        manager = VideoGenTaskManager()
        task = _task("reg_kept")
        task.status = TaskStatus.FAILED
        manager.tasks[task.draft_url] = task

        try:
            with patch(
                "src.utils.video_task_manager.save_completed_result",
                side_effect=RuntimeError("db down"),
            ):
                manager._persist_terminal_task(task)

            # 落库失败不能移除，否则状态查询会变成「任务不存在」
            assert manager.tasks.get(task.draft_url) is task
        finally:
            manager.tasks.pop(task.draft_url, None)

    def test_persist_does_not_remove_newer_task_for_same_url(self) -> None:
        manager = VideoGenTaskManager()
        old = _task("reg_race")
        old.status = TaskStatus.COMPLETED
        newer = _task("reg_race")
        manager.tasks[old.draft_url] = newer

        try:
            with patch("src.utils.video_task_manager.save_completed_result"):
                manager._persist_terminal_task(old)

            # 同名 draft_url 已被重新提交，旧任务的收尾不能误删新任务
            assert manager.tasks.get(old.draft_url) is newer
        finally:
            manager.tasks.pop(old.draft_url, None)

    def test_status_falls_back_to_db_after_removal(self) -> None:
        manager = VideoGenTaskManager()
        task = _task("reg_fallback")
        task.status = TaskStatus.COMPLETED
        manager.tasks[task.draft_url] = task

        stored = {
            "draft_url": task.draft_url,
            "status": "completed",
            "progress": 100,
            "video_url": "http://example/out.mp4",
            "error_message": "",
            "created_at": task.created_at.isoformat(),
            "started_at": None,
            "completed_at": datetime.now().isoformat(),
        }

        with patch("src.utils.video_task_manager.save_completed_result"):
            manager._persist_terminal_task(task)

        with patch("src.utils.video_task_manager.prune_if_needed"), patch(
            "src.utils.video_task_manager.get_completed_by_draft_id",
            return_value=stored,
        ) as m_get:
            result = manager.get_task_status(task.draft_url)

        m_get.assert_called_once_with(task.draft_id)
        assert result == stored
