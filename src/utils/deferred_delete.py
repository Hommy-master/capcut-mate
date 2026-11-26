"""延迟删除队列：入队后由后台定时任务无限重试，直至删除成功或路径已不存在。"""
from __future__ import annotations

import asyncio
import os
import shutil
import threading
import time
from typing import Dict, Iterable, Optional, Tuple

from src.utils.logger import logger

# 定时扫描待删除队列的间隔（秒），可通过环境变量覆盖
DEFERRED_DELETE_INTERVAL_SECONDS = max(
    5,
    int(os.getenv("DEFERRED_DELETE_INTERVAL_SECONDS", "10")),
)

# 剪映草稿目录兜底扫描间隔（秒）：每 30 分钟执行一次，
# 删除超过 DRAFT_CONTENT_MIN_AGE_SECONDS（12 小时）的草稿目录。
STALE_DRAFT_SWEEP_INTERVAL_SECONDS = 30 * 60

_lock = threading.Lock()
# 规范化绝对路径 -> 是否为目录
_pending: Dict[str, bool] = {}


def _normalize_path(path: str) -> str:
    return os.path.normcase(os.path.normpath(os.path.abspath(path)))


def enqueue_path(path: str, *, is_dir: bool = False) -> None:
    """将文件或目录加入待删除队列（已存在则更新类型）。"""
    if not path or not str(path).strip():
        return
    key = _normalize_path(path)
    with _lock:
        _pending[key] = is_dir
    logger.info("Deferred delete enqueued: path=%s is_dir=%s", key, is_dir)


def enqueue_paths(paths: Iterable[str], *, is_dir: bool = False) -> None:
    for path in paths:
        enqueue_path(path, is_dir=is_dir)


def dequeue_path(path: str) -> bool:
    """从待删除队列中移除路径；重新下载同一草稿前应调用，避免与延迟删除竞态。"""
    if not path or not str(path).strip():
        return False
    key = _normalize_path(path)
    with _lock:
        removed = key in _pending
        if removed:
            del _pending[key]
    if removed:
        logger.info("Deferred delete dequeued: path=%s", key)
    return removed


def pending_count() -> int:
    with _lock:
        return len(_pending)


def list_pending_paths() -> list[str]:
    with _lock:
        return list(_pending.keys())


def _try_delete_path(path: str, is_dir: bool) -> bool:
    """
    尝试删除单条路径。

    Returns:
        True 表示可从队列移除（已删除或本就不存在）；False 表示下次继续重试。
    """
    if not os.path.lexists(path):
        logger.info("Deferred delete skip (not exists): path=%s", path)
        return True
    try:
        if is_dir:
            shutil.rmtree(path)
        else:
            os.remove(path)
        logger.info("Deferred delete succeeded: path=%s is_dir=%s", path, is_dir)
        return True
    except OSError as exc:
        logger.warning(
            "Deferred delete will retry later: path=%s is_dir=%s error=%s",
            path,
            is_dir,
            exc,
        )
        return False


def run_pending_deletes() -> Tuple[int, int]:
    """
    扫描并处理待删除队列。

    Returns:
        (本次移出队列的数量, 队列剩余数量)
    """
    with _lock:
        snapshot = list(_pending.items())

    if not snapshot:
        return 0, 0

    removed = 0
    for path, is_dir in snapshot:
        if _try_delete_path(path, is_dir):
            with _lock:
                _pending.pop(path, None)
            removed += 1

    with _lock:
        remaining = len(_pending)
    if removed or remaining:
        logger.info(
            "Deferred delete sweep finished: removed=%s remaining=%s",
            removed,
            remaining,
        )
    return removed, remaining


def clear_pending_for_tests() -> None:
    """仅用于单元测试：清空队列。"""
    with _lock:
        _pending.clear()


async def deferred_delete_background_loop(
    interval: Optional[float] = None,
    sweep_interval: Optional[float] = None,
) -> None:
    """
    后台定时删除循环，直至进程退出。

    每 ``interval`` 秒清空一次延迟删除队列；另按 ``sweep_interval``（默认 30
    分钟）兜底扫描剪映草稿目录，删除超过 12 小时的草稿。扫描与删除放到线程
    中执行，避免阻塞事件循环；启动后先扫一次，兜住重启时丢失的待删除项。
    """
    sleep_seconds = interval if interval is not None else DEFERRED_DELETE_INTERVAL_SECONDS
    sweep_seconds = (
        sweep_interval
        if sweep_interval is not None
        else STALE_DRAFT_SWEEP_INTERVAL_SECONDS
    )
    sweep_seconds = max(1.0, sweep_seconds)
    logger.info(
        "Deferred delete background loop started: interval_seconds=%s "
        "stale_draft_sweep_interval_seconds=%s",
        sleep_seconds,
        sweep_seconds,
    )
    # 启动后立即执行一次兜底扫描，之后按 sweep_seconds 周期执行
    next_sweep_at = time.monotonic()
    while True:
        try:
            run_pending_deletes()
        except Exception:
            logger.exception("Deferred delete sweep failed")

        if time.monotonic() >= next_sweep_at:
            next_sweep_at = time.monotonic() + sweep_seconds
            try:
                from src.utils.jianying_export_cleanup import (
                    sweep_stale_draft_directories,
                )

                removed = await asyncio.to_thread(sweep_stale_draft_directories)
                logger.info("Stale draft sweep removed %s directory(ies)", removed)
            except Exception:
                logger.exception("Stale draft sweep failed")

        await asyncio.sleep(sleep_seconds)
