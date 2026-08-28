"""延迟删除队列：入队后由后台定时任务无限重试，直至删除成功或路径已不存在。"""
from __future__ import annotations

import asyncio
import os
import shutil
import threading
from typing import Dict, Iterable, Optional, Tuple

from src.utils.logger import logger

# 定时扫描待删除队列的间隔（秒），可通过环境变量覆盖
DEFERRED_DELETE_INTERVAL_SECONDS = max(
    5,
    int(os.getenv("DEFERRED_DELETE_INTERVAL_SECONDS", "10")),
)

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
) -> None:
    """后台定时删除循环，直至进程退出。"""
    sleep_seconds = interval if interval is not None else DEFERRED_DELETE_INTERVAL_SECONDS
    logger.info(
        "Deferred delete background loop started: interval_seconds=%s",
        sleep_seconds,
    )
    while True:
        try:
            run_pending_deletes()
        except Exception:
            logger.exception("Deferred delete sweep failed")
        await asyncio.sleep(sleep_seconds)
