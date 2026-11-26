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


def _patch_pipeline(prepare, export=None, upload=None):
    """替换下载/导出/上传阶段，隔离真实线程池与外部依赖。"""
    if upload is None:
        upload_patch = patch.object(
            VideoGenTaskManager,
            "_run_upload_and_finalize",
            new_callable=AsyncMock,
        )
    else:
        upload_patch = patch.object(
            VideoGenTaskManager,
            "_run_upload_and_finalize",
            side_effect=upload,
        )
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
        upload_patch,
    )


async def _wait_until(predicate, timeout: float = 5.0) -> None:
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    while not predicate() and loop.time() < deadline:
        await asyncio.sleep(0.01)


def _raise_export(task: VideoGenTask) -> str:
    raise RuntimeError("boom")


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

    def test_backlog_limit_caps_concurrent_downloads(self) -> None:
        """名额为 2 时，即使提交 5 个任务也最多只有 2 个在下载。"""
        manager = VideoGenTaskManager()
        original = manager._export_backlog
        manager._export_backlog = asyncio.Semaphore(2)

        gate = threading.Event()
        counter_lock = threading.Lock()
        downloads: list[str] = []
        active = 0
        peak = 0

        def prepare(task: VideoGenTask) -> str:
            nonlocal active, peak
            with counter_lock:
                downloads.append(task.draft_id)
                active += 1
                peak = max(peak, active)
            try:
                gate.wait(timeout=5)
            finally:
                with counter_lock:
                    active -= 1
            return ""

        async def scenario() -> None:
            tasks = []
            p_dl, p_ex, p_up = _patch_pipeline(prepare)
            with p_dl, p_ex, p_up:
                tasks = [
                    asyncio.create_task(manager._process_task(_task(f"cap{i}")))
                    for i in range(5)
                ]
                await _wait_until(lambda: len(downloads) >= 2)
                await asyncio.sleep(0.2)
                # 第 3 个任务不能越过名额开始下载
                assert len(downloads) == 2

                gate.set()
                await asyncio.wait_for(asyncio.gather(*tasks), timeout=10)
                assert sorted(downloads) == [f"cap{i}" for i in range(5)]
                assert peak == 2

        try:
            asyncio.run(scenario())
        finally:
            gate.set()
            manager._export_backlog = original

    def test_slot_released_when_export_fails(self) -> None:
        manager = VideoGenTaskManager()
        original = manager._export_backlog
        manager._export_backlog = asyncio.Semaphore(1)
        downloads: list[str] = []

        def prepare(task: VideoGenTask) -> str:
            downloads.append(task.draft_id)
            return ""

        async def scenario():
            p_dl, p_ex, p_up = _patch_pipeline(
                prepare, export=lambda task: "导出草稿失败"
            )
            with p_dl, p_ex, p_up, patch.object(
                VideoGenTaskManager, "_cleanup_files"
            ), patch(
                "src.utils.video_task_manager.save_completed_result"
            ) as m_save:
                t1 = asyncio.create_task(manager._process_task(_task("expfail1")))
                t2 = asyncio.create_task(manager._process_task(_task("expfail2")))
                await asyncio.wait_for(asyncio.gather(t1, t2), timeout=5)
                assert downloads == ["expfail1", "expfail2"]
            return m_save

        try:
            m_save = asyncio.run(scenario())
        finally:
            manager._export_backlog = original

        # 两个任务都以 FAILED 走了真实落库流程
        assert m_save.call_count == 2

    def test_slot_released_when_export_raises(self) -> None:
        manager = VideoGenTaskManager()
        original = manager._export_backlog
        manager._export_backlog = asyncio.Semaphore(1)
        downloads: list[str] = []

        def prepare(task: VideoGenTask) -> str:
            downloads.append(task.draft_id)
            return ""

        async def scenario():
            p_dl, p_ex, p_up = _patch_pipeline(prepare, export=_raise_export)
            with p_dl, p_ex, p_up, patch.object(
                VideoGenTaskManager, "_cleanup_files"
            ), patch(
                "src.utils.video_task_manager.save_completed_result"
            ) as m_save:
                t1 = asyncio.create_task(manager._process_task(_task("raise1")))
                t2 = asyncio.create_task(manager._process_task(_task("raise2")))
                await asyncio.wait_for(asyncio.gather(t1, t2), timeout=5)
                assert downloads == ["raise1", "raise2"]
            return m_save

        try:
            m_save = asyncio.run(scenario())
        finally:
            manager._export_backlog = original

        assert m_save.call_count == 2

    def test_slot_released_before_upload_completes(self) -> None:
        """名额在导出结束时就释放，不能被上传阶段继续占用。"""
        manager = VideoGenTaskManager()
        original = manager._export_backlog
        manager._export_backlog = asyncio.Semaphore(1)
        downloads: list[str] = []

        def prepare(task: VideoGenTask) -> str:
            downloads.append(task.draft_id)
            return ""

        async def scenario() -> None:
            upload_started = asyncio.Event()
            upload_release = asyncio.Event()

            async def fake_upload(task: VideoGenTask) -> None:
                upload_started.set()
                await upload_release.wait()

            p_dl, p_ex, p_up = _patch_pipeline(prepare, upload=fake_upload)
            with p_dl, p_ex, p_up:
                t1 = asyncio.create_task(manager._process_task(_task("up1")))
                # 导出已结束、上传尚未完成
                await asyncio.wait_for(upload_started.wait(), timeout=5)
                assert downloads == ["up1"]

                t2 = asyncio.create_task(manager._process_task(_task("up2")))
                await _wait_until(lambda: len(downloads) >= 2)
                assert downloads == ["up1", "up2"]

                upload_release.set()
                await asyncio.wait_for(asyncio.gather(t1, t2), timeout=5)

        try:
            asyncio.run(scenario())
        finally:
            manager._export_backlog = original
