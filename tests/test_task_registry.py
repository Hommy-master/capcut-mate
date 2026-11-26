"""终态任务内存回收：落库成功后才从 self.tasks 移除。"""
import asyncio
import threading
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


async def _wait_until(predicate, timeout: float = 5.0) -> None:
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    while not predicate() and loop.time() < deadline:
        await asyncio.sleep(0.01)


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

    def test_persist_leaves_other_tasks_intact(self) -> None:
        manager = VideoGenTaskManager()
        done = _task("reg_done")
        done.status = TaskStatus.COMPLETED
        other = _task("reg_other")
        other.status = TaskStatus.PROCESSING
        manager.tasks[done.draft_url] = done
        manager.tasks[other.draft_url] = other

        try:
            with patch("src.utils.video_task_manager.save_completed_result"):
                manager._persist_terminal_task(done)

            assert done.draft_url not in manager.tasks
            assert manager.tasks.get(other.draft_url) is other
        finally:
            manager.tasks.pop(done.draft_url, None)
            manager.tasks.pop(other.draft_url, None)

    def test_persist_twice_after_removal_is_safe(self) -> None:
        manager = VideoGenTaskManager()
        task = _task("reg_twice")
        task.status = TaskStatus.COMPLETED
        manager.tasks[task.draft_url] = task

        with patch(
            "src.utils.video_task_manager.save_completed_result"
        ) as m_save:
            manager._persist_terminal_task(task)
            manager._persist_terminal_task(task)

        assert m_save.call_count == 2
        assert task.draft_url not in manager.tasks

    def test_non_terminal_task_not_persisted_or_removed(self) -> None:
        manager = VideoGenTaskManager()
        task = _task("reg_active")
        task.status = TaskStatus.PROCESSING
        manager.tasks[task.draft_url] = task

        try:
            with patch(
                "src.utils.video_task_manager.save_completed_result"
            ) as m_save:
                manager._persist_terminal_task(task)

            m_save.assert_not_called()
            assert manager.tasks.get(task.draft_url) is task
        finally:
            manager.tasks.pop(task.draft_url, None)

    def test_get_task_status_prefers_memory_for_active_task(self) -> None:
        manager = VideoGenTaskManager()
        task = _task("reg_memory")
        task.status = TaskStatus.PROCESSING
        manager.tasks[task.draft_url] = task

        try:
            with patch(
                "src.utils.video_task_manager.get_completed_by_draft_id"
            ) as m_db:
                info = manager.get_task_status(task.draft_url)

            m_db.assert_not_called()
            assert info is not None
            assert info["status"] == "processing"
        finally:
            manager.tasks.pop(task.draft_url, None)

    def test_active_count_excludes_terminal_tasks(self) -> None:
        manager = VideoGenTaskManager()
        baseline = manager.get_active_render_count()

        pending = _task("reg_pending")
        pending.status = TaskStatus.PENDING
        processing = _task("reg_processing")
        processing.status = TaskStatus.PROCESSING
        done = _task("reg_completed")
        done.status = TaskStatus.COMPLETED
        failed = _task("reg_failed")
        failed.status = TaskStatus.FAILED
        tasks = (pending, processing, done, failed)
        for task in tasks:
            manager.tasks[task.draft_url] = task

        try:
            assert manager.get_active_render_count() == baseline + 2
        finally:
            for task in tasks:
                manager.tasks.pop(task.draft_url, None)

    def test_active_count_thread_safe_with_concurrent_mutation(self) -> None:
        manager = VideoGenTaskManager()
        errors: list[BaseException] = []
        stop = threading.Event()

        def reader() -> None:
            try:
                while not stop.is_set():
                    manager.get_active_render_count()
            except BaseException as exc:  # noqa: BLE001 - 记录后由主线程断言
                errors.append(exc)

        readers = [threading.Thread(target=reader) for _ in range(4)]
        for thread in readers:
            thread.start()

        try:
            for i in range(300):
                url = f"http://example/get_draft?draft_id=reg_stress_{i}"
                with manager._tasks_lock:
                    manager.tasks[url] = _task(f"reg_stress_{i}")
                with manager._tasks_lock:
                    manager.tasks.pop(url, None)
        finally:
            stop.set()
            for thread in readers:
                thread.join(timeout=5)

        assert not errors


class TestTerminalTaskLifecycle:
    def test_submit_task_dedupes_active_and_replaces_terminal(self) -> None:
        manager = VideoGenTaskManager()
        url = "http://example/get_draft?draft_id=reg_submit"
        manager.tasks.pop(url, None)

        try:
            with patch.object(
                VideoGenTaskManager, "_ensure_worker_running"
            ), patch.object(
                VideoGenTaskManager, "_add_task_to_queue_sync"
            ) as m_queue:
                manager.submit_task(url)
                first = manager.tasks[url]
                assert first.status is TaskStatus.PENDING

                # 进行中的任务不能被重复提交
                manager.submit_task(url)
                assert manager.tasks[url] is first
                assert m_queue.call_count == 1

                # 终态任务允许被新任务覆盖
                first.status = TaskStatus.COMPLETED
                manager.submit_task(url)
                assert manager.tasks[url] is not first
                assert m_queue.call_count == 2
        finally:
            manager.tasks.pop(url, None)

    def test_process_task_download_failure_removes_task_from_memory(self) -> None:
        manager = VideoGenTaskManager()
        original_backlog = manager._export_backlog
        manager._export_backlog = asyncio.Semaphore(3)
        task = _task("flow_download_fail")
        task.status = TaskStatus.PROCESSING
        manager.tasks[task.draft_url] = task

        async def scenario():
            with patch.object(
                VideoGenTaskManager,
                "_phase_download_and_prepare",
                return_value="草稿下载失败: boom",
            ), patch.object(
                VideoGenTaskManager, "_cleanup_files"
            ), patch(
                "src.utils.video_task_manager.save_completed_result"
            ) as m_save:
                await manager._process_task(task)
            return m_save

        try:
            m_save = asyncio.run(scenario())
        finally:
            manager.tasks.pop(task.draft_url, None)
            manager._export_backlog = original_backlog

        m_save.assert_called_once()
        assert task.status is TaskStatus.FAILED
        assert task.draft_url not in manager.tasks

    def test_process_task_keeps_task_when_persist_fails(self) -> None:
        manager = VideoGenTaskManager()
        original_backlog = manager._export_backlog
        manager._export_backlog = asyncio.Semaphore(3)
        task = _task("flow_persist_fail")
        task.status = TaskStatus.PROCESSING
        manager.tasks[task.draft_url] = task

        async def scenario() -> bool:
            with patch.object(
                VideoGenTaskManager,
                "_phase_download_and_prepare",
                return_value="草稿下载失败: boom",
            ), patch.object(
                VideoGenTaskManager, "_cleanup_files"
            ), patch(
                "src.utils.video_task_manager.save_completed_result",
                side_effect=RuntimeError("db down"),
            ):
                await manager._process_task(task)
            # 在清理前记录内存里是否还保留该任务
            return manager.tasks.get(task.draft_url) is task

        try:
            kept_in_memory = asyncio.run(scenario())
        finally:
            manager.tasks.pop(task.draft_url, None)
            manager._export_backlog = original_backlog

        assert task.status is TaskStatus.FAILED
        assert kept_in_memory is True

    def test_upload_finalize_success_removes_task(self) -> None:
        manager = VideoGenTaskManager()
        task = _task("flow_upload_ok")
        task.status = TaskStatus.PROCESSING
        task.outfile = "/tmp/out.mp4"
        manager.tasks[task.draft_url] = task

        async def scenario():
            with patch.object(
                VideoGenTaskManager,
                "_phase_cos_upload_finalize",
                return_value=("http://example/out.mp4", ""),
            ), patch(
                "src.utils.video_task_manager.save_completed_result"
            ) as m_save:
                await manager._run_upload_and_finalize(task)
            return m_save

        try:
            m_save = asyncio.run(scenario())
        finally:
            manager.tasks.pop(task.draft_url, None)

        m_save.assert_called_once()
        assert task.status is TaskStatus.COMPLETED
        assert task.video_url == "http://example/out.mp4"
        assert task.draft_url not in manager.tasks

    def test_process_task_keeps_task_until_upload_finalizes(self) -> None:
        """成功后任务在上传期间仍在内存，上传落库后才移除。"""
        manager = VideoGenTaskManager()
        original_backlog = manager._export_backlog
        manager._export_backlog = asyncio.Semaphore(3)
        task = _task("flow_success")
        manager.tasks[task.draft_url] = task

        upload_started = threading.Event()
        upload_release = threading.Event()

        def fake_upload_finalize(t: VideoGenTask):
            upload_started.set()
            upload_release.wait(timeout=5)
            return "http://example/out.mp4", ""

        async def scenario() -> None:
            with patch.object(
                VideoGenTaskManager,
                "_phase_download_and_prepare",
                return_value="",
            ), patch.object(
                VideoGenTaskManager,
                "_phase_export_only",
                return_value="",
            ), patch.object(
                VideoGenTaskManager,
                "_phase_cos_upload_finalize",
                side_effect=fake_upload_finalize,
            ), patch(
                "src.utils.video_task_manager.save_completed_result"
            ) as m_save:
                await manager._process_task(task)

                # 上传还没结束，任务不能被提前移除
                assert await asyncio.to_thread(upload_started.wait, 5)
                assert manager.tasks.get(task.draft_url) is task

                upload_release.set()
                await _wait_until(lambda: task.draft_url not in manager.tasks)
                assert task.status is TaskStatus.COMPLETED
                m_save.assert_called_once()

        try:
            asyncio.run(scenario())
        finally:
            upload_release.set()
            manager.tasks.pop(task.draft_url, None)
            manager._export_backlog = original_backlog

    def test_upload_finalize_failure_removes_task(self) -> None:
        manager = VideoGenTaskManager()
        task = _task("flow_upload_fail")
        task.status = TaskStatus.PROCESSING
        task.outfile = "/tmp/out.mp4"
        manager.tasks[task.draft_url] = task

        async def scenario():
            with patch.object(
                VideoGenTaskManager,
                "_phase_cos_upload_finalize",
                return_value=("", "视频上传失败"),
            ), patch(
                "src.utils.video_task_manager.save_completed_result"
            ) as m_save:
                await manager._run_upload_and_finalize(task)
            return m_save

        try:
            m_save = asyncio.run(scenario())
        finally:
            manager.tasks.pop(task.draft_url, None)

        m_save.assert_called_once()
        assert task.status is TaskStatus.FAILED
        assert task.error_message == "视频上传失败"
        assert task.draft_url not in manager.tasks
