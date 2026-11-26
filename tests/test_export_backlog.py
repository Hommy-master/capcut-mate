"""导出积压限流：下载前必须先取得「已下载待导出」名额。"""
import asyncio
import threading
from datetime import datetime
from unittest.mock import AsyncMock, patch

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


def _patch_pipeline(prepare, export=None):
    """替换下载/导出/上传阶段，隔离真实线程池与外部依赖。"""
    return (
        patch.object(
            VideoGenTaskManager,
            "_phase_download_and_prepare",
            side_effect=prepare,
        ),
        patch.object(
            VideoGenTaskManager,
            "_phase_export_only",
            side_effect=export or (lambda task: ""),
        ),
        patch.object(
            VideoGenTaskManager,
            "_run_upload_and_finalize",
            new_callable=AsyncMock,
        ),
    )


class TestExportBacklog:
    def test_download_waits_for_free_backlog_slot(self) -> None:
        manager = VideoGenTaskManager()
        original = manager._export_backlog
        manager._export_backlog = asyncio.Semaphore(1)

        first_started = threading.Event()
        release_first = threading.Event()
        downloads: list[str] = []

        def prepare(task: VideoGenTask) -> str:
            downloads.append(task.draft_id)
            if task.draft_id == "d1":
                first_started.set()
                release_first.wait(timeout=5)
            return ""

        async def scenario() -> None:
            p_dl, p_ex, p_up = _patch_pipeline(prepare)
            with p_dl, p_ex, p_up:
                t1 = asyncio.create_task(manager._process_task(_task("d1")))
                assert await asyncio.to_thread(first_started.wait, 5)

                t2 = asyncio.create_task(manager._process_task(_task("d2")))
                await asyncio.sleep(0.2)
                # d1 还占着名额、尚未导出，d2 不能开始下载
                assert downloads == ["d1"]

                release_first.set()
                await asyncio.wait_for(asyncio.gather(t1, t2), timeout=5)
                assert downloads == ["d1", "d2"]

        try:
            asyncio.run(scenario())
        finally:
            release_first.set()
            manager._export_backlog = original

    def test_failed_prepare_releases_backlog_slot(self) -> None:
        manager = VideoGenTaskManager()
        original = manager._export_backlog
        manager._export_backlog = asyncio.Semaphore(1)
        downloads: list[str] = []

        def prepare(task: VideoGenTask) -> str:
            downloads.append(task.draft_id)
            return "草稿下载失败: boom" if task.draft_id == "d1" else ""

        async def scenario() -> None:
            p_dl, p_ex, p_up = _patch_pipeline(prepare)
            with p_dl, p_ex, p_up, patch.object(
                VideoGenTaskManager, "_cleanup_files"
            ), patch.object(VideoGenTaskManager, "_persist_terminal_task"):
                t1 = asyncio.create_task(manager._process_task(_task("d1")))
                t2 = asyncio.create_task(manager._process_task(_task("d2")))
                # d1 下载失败后必须释放名额，否则 d2 会一直卡在信号量上
                await asyncio.wait_for(asyncio.gather(t1, t2), timeout=5)
                assert downloads == ["d1", "d2"]
                assert t1.result() is None

        try:
            asyncio.run(scenario())
        finally:
            manager._export_backlog = original
