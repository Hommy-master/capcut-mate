"""
草稿目录定期清理：超出数量上限时按创建时间从旧到新删除目录，并跳过受保护、
已加锁、仍在内存缓存中的草稿，避免影响正常读写。
"""
from __future__ import annotations

import asyncio
import datetime
import os
import re
import shutil
from typing import Iterable, Optional

import config
from src.utils.draft_cache import DRAFT_CACHE
from src.utils.draft_lock_manager import get_draft_lock_manager
from src.utils.logger import logger

# 草稿清理策略（本模块内定义；保留数量可由环境变量 DRAFT_CLEANUP_MAX_DRAFT_COUNT 覆盖，默认 1000）
DRAFT_CLEANUP_MAX_DRAFT_COUNT = max(0, int(os.getenv("DRAFT_CLEANUP_MAX_DRAFT_COUNT", "1000")))
DRAFT_CLEANUP_INTERVAL_SECONDS = 3600
DRAFT_CLEANUP_PROTECTED_DRAFT_IDS = frozenset(
    {
        "20251204214904ccb1af38",
        "2025120421372636a27729",
    }
)

_DRAFT_ID_RE = re.compile(r"^\d{14}[a-f0-9]{8}$")


def is_draft_directory_name(name: str) -> bool:
    return bool(_DRAFT_ID_RE.match(name))


def _draft_sort_key(draft_id: str) -> tuple[datetime.datetime, str]:
    ts = draft_id[:14]
    dt = datetime.datetime.strptime(ts, "%Y%m%d%H%M%S")
    return dt, draft_id


def list_sorted_draft_ids(draft_dir: str) -> list[str]:
    if not os.path.isdir(draft_dir):
        return []
    names: list[str] = []
    with os.scandir(draft_dir) as it:
        for ent in it:
            if ent.is_dir() and is_draft_directory_name(ent.name):
                names.append(ent.name)
    names.sort(key=_draft_sort_key)
    return names


def select_drafts_for_deletion(
    sorted_oldest_first: list[str], max_keep: int, skip_ids: set[str]
) -> list[str]:
    n = len(sorted_oldest_first)
    need = max(0, n - max_keep)
    if need == 0:
        return []
    out: list[str] = []
    for did in sorted_oldest_first:
        if len(out) >= need:
            break
        if did in skip_ids:
            continue
        out.append(did)
    return out


def delete_draft_folders(draft_dir: str, draft_ids: Iterable[str]) -> list[str]:
    deleted: list[str] = []
    for did in draft_ids:
        path = os.path.join(draft_dir, did)
        logger.info(
            "DRAFT_CLEANUP_DELETE draft_id=%s path=%s action=shutil.rmtree",
            did,
            path,
        )
        try:
            shutil.rmtree(path, ignore_errors=False)
            deleted.append(did)
            logger.info(
                "DRAFT_CLEANUP_DELETED draft_id=%s path=%s status=success",
                did,
                path,
            )
        except OSError as e:
            logger.warning(
                "DRAFT_CLEANUP_DELETE_FAILED draft_id=%s path=%s error=%s",
                did,
                path,
                e,
            )
    return deleted


def run_one_draft_cleanup(
    draft_dir: Optional[str] = None,
    max_keep: Optional[int] = None,
    protected_ids: Optional[Iterable[str]] = None,
    locked_ids: Optional[Iterable[str]] = None,
    cached_ids: Optional[Iterable[str]] = None,
) -> list[str]:
    base = draft_dir if draft_dir is not None else config.DRAFT_DIR
    limit = max_keep if max_keep is not None else DRAFT_CLEANUP_MAX_DRAFT_COUNT
    protected = frozenset(
        protected_ids
        if protected_ids is not None
        else DRAFT_CLEANUP_PROTECTED_DRAFT_IDS
    )
    locked = (
        set(locked_ids)
        if locked_ids is not None
        else set(get_draft_lock_manager().get_all_locked_drafts())
    )
    cached = set(cached_ids) if cached_ids is not None else set(DRAFT_CACHE.keys())
    skip = set(protected) | locked | cached
    sorted_ids = list_sorted_draft_ids(base)
    to_remove = select_drafts_for_deletion(sorted_ids, limit, skip)
    if not to_remove:
        reason = "under_limit" if len(sorted_ids) <= limit else "all_excess_protected_or_active"
        logger.info(
            "DRAFT_CLEANUP_SKIP total_drafts=%s max_keep=%s skip_count=%s reason=%s",
            len(sorted_ids),
            limit,
            len(skip),
            reason,
        )
        return []
    logger.info(
        "DRAFT_CLEANUP_PLAN total_drafts=%s max_keep=%s to_delete=%s protected=%s locked=%s cached=%s",
        len(sorted_ids),
        limit,
        len(to_remove),
        len(protected),
        len(locked),
        len(cached),
    )
    return delete_draft_folders(base, to_remove)


async def draft_cleanup_background_loop() -> None:
    interval = DRAFT_CLEANUP_INTERVAL_SECONDS
    while True:
        try:
            run_one_draft_cleanup()
        except Exception:
            logger.exception("DRAFT_CLEANUP_ERROR phase=run_one_draft_cleanup")
        await asyncio.sleep(interval)
