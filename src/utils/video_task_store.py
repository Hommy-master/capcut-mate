"""
视频生成任务完成结果持久化（SQLite）。
进行中的任务仅存在于内存，完成（成功或失败）后写入本模块。
"""
from __future__ import annotations

import os
import sqlite3
import threading
import time
from datetime import datetime
from typing import Any, Dict, Optional

import config
from src.utils.logger import logger

_MAX_ROWS = 100_000
_PRUNE_BATCH = 1_000
# 高并发下避免每次状态查询都跑 COUNT/竞争锁；超过间隔才真正检查是否需清理
_PRUNE_MIN_INTERVAL_SEC = 60.0
_last_prune_at: Optional[float] = None

_lock = threading.Lock()


def _connect() -> sqlite3.Connection:
    path = config.VIDEO_GEN_TASK_DB_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _init_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS video_gen_task_results (
            draft_id TEXT PRIMARY KEY NOT NULL,
            draft_url TEXT NOT NULL,
            status TEXT NOT NULL,
            progress INTEGER NOT NULL,
            video_url TEXT NOT NULL DEFAULT '',
            error_message TEXT NOT NULL DEFAULT '',
            created_at TEXT,
            started_at TEXT,
            completed_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_vgtr_completed_at
        ON video_gen_task_results(completed_at)
        """
    )
    conn.commit()


def _ensure_schema() -> None:
    with _lock:
        conn = _connect()
        try:
            _init_schema(conn)
        finally:
            conn.close()


_ensure_schema()


def prune_if_needed() -> None:
    """
    若表中记录数超过 10 万，按 completed_at 最旧优先删除 1000 条。
    在查询已落库任务前可调用；高并发下通过时间间隔节流，避免每次请求都 COUNT(*)。
    """
    global _last_prune_at
    now = time.monotonic()
    if _last_prune_at is not None and now - _last_prune_at < _PRUNE_MIN_INTERVAL_SEC:
        return
    with _lock:
        now2 = time.monotonic()
        if _last_prune_at is not None and now2 - _last_prune_at < _PRUNE_MIN_INTERVAL_SEC:
            return
        _last_prune_at = now2
        conn = _connect()
        try:
            (cnt,) = conn.execute(
                "SELECT COUNT(*) FROM video_gen_task_results"
            ).fetchone()
            if cnt <= _MAX_ROWS:
                return
            conn.execute(
                """
                DELETE FROM video_gen_task_results WHERE rowid IN (
                    SELECT rowid FROM video_gen_task_results
                    ORDER BY completed_at ASC, draft_id ASC
                    LIMIT ?
                )
                """,
                (_PRUNE_BATCH,),
            )
            conn.commit()
            logger.info(
                "video_gen_task_results pruned %s rows (count was %s)",
                _PRUNE_BATCH,
                cnt,
            )
        finally:
            conn.close()


def save_completed_result(
    draft_id: str,
    draft_url: str,
    status: str,
    progress: int,
    video_url: str,
    error_message: str,
    created_at: datetime,
    started_at: Optional[datetime],
    completed_at: datetime,
) -> None:
    """持久化已完成任务（成功或失败）。不在此保存进行中的任务。"""
    with _lock:
        conn = _connect()
        try:
            conn.execute(
                """
                INSERT OR REPLACE INTO video_gen_task_results (
                    draft_id, draft_url, status, progress,
                    video_url, error_message,
                    created_at, started_at, completed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    draft_id,
                    draft_url,
                    status,
                    progress,
                    video_url,
                    error_message,
                    created_at.isoformat(),
                    started_at.isoformat() if started_at else None,
                    completed_at.isoformat(),
                ),
            )
            conn.commit()
        finally:
            conn.close()


def get_completed_by_draft_id(draft_id: str) -> Optional[Dict[str, Any]]:
    """按 draft_id 读取已持久化的任务结果；无记录则返回 None。"""
    if not draft_id:
        return None
    with _lock:
        conn = _connect()
        try:
            row = conn.execute(
                """
                SELECT draft_url, status, progress, video_url, error_message,
                       created_at, started_at, completed_at
                FROM video_gen_task_results
                WHERE draft_id = ?
                """,
                (draft_id,),
            ).fetchone()
            if not row:
                return None
            return {
                "draft_url": row["draft_url"],
                "status": row["status"],
                "progress": row["progress"],
                "video_url": row["video_url"] or "",
                "error_message": row["error_message"] or "",
                "created_at": row["created_at"],
                "started_at": row["started_at"],
                "completed_at": row["completed_at"],
            }
        finally:
            conn.close()
