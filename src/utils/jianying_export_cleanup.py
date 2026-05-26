"""剪映导出失败后的恢复：强杀进程并按条件清理本地草稿目录。"""
from __future__ import annotations

import os
import shutil
import subprocess
import time
from typing import Iterable

import config
from src.utils.logger import logger

# 剪映专业版主进程及常见子进程映像名
JIANYING_PROCESS_IMAGE_NAMES: tuple[str, ...] = (
    "JianyingPro.exe",
)

ROOT_META_INFO_FILE = "root_meta_info.json"
DRAFT_CONTENT_FILE = "draft_content.json"

# 草稿目录删除阈值：draft_content.json 创建时间早于该秒数才删除整个草稿目录
DRAFT_CONTENT_MIN_AGE_SECONDS = 24 * 3600


def draft_save_path_exists() -> bool:
    """``config.DRAFT_SAVE_PATH`` 已配置且对应目录在磁盘上存在。"""
    base = config.DRAFT_SAVE_PATH
    return bool(base) and os.path.isdir(base)


def kill_jianying_process(
    image_names: Iterable[str] = JIANYING_PROCESS_IMAGE_NAMES,
) -> None:
    """强制结束剪映相关进程（含子进程树）。"""
    for image_name in image_names:
        try:
            result = subprocess.run(
                ["taskkill", "/F", "/T", "/IM", image_name],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            if result.returncode == 0:
                logger.info("Killed Jianying process: %s", image_name)
            else:
                logger.info(
                    "taskkill %s exit=%s (process may be absent): %s",
                    image_name,
                    result.returncode,
                    (result.stderr or result.stdout or "").strip(),
                )
        except Exception as exc:
            logger.warning("Failed to kill Jianying process %s: %s", image_name, exc)


def _file_creation_timestamp(path: str) -> float | None:
    """返回文件创建时间戳（秒）；Windows 下为创建时间。"""
    try:
        return os.path.getctime(path)
    except OSError as exc:
        logger.warning("Failed to read creation time: path=%s error=%s", path, exc)
        return None


def _draft_content_is_old_enough(
    draft_dir_path: str,
    min_age_seconds: float = DRAFT_CONTENT_MIN_AGE_SECONDS,
) -> bool:
    """
    判断草稿目录是否可删除：依据其中 draft_content.json 的创建时间，
    仅当该文件存在且创建时间早于 min_age_seconds 时返回 True。
    """
    content_path = os.path.join(draft_dir_path, DRAFT_CONTENT_FILE)
    if not os.path.isfile(content_path):
        logger.info(
            "Skip draft directory (missing %s): %s",
            DRAFT_CONTENT_FILE,
            draft_dir_path,
        )
        return False

    created_at = _file_creation_timestamp(content_path)
    if created_at is None:
        logger.info(
            "Skip draft directory (cannot read %s creation time): %s",
            DRAFT_CONTENT_FILE,
            draft_dir_path,
        )
        return False

    age_seconds = time.time() - created_at
    if age_seconds >= min_age_seconds:
        logger.info(
            "Draft directory eligible for removal: path=%s %s_age_hours=%.2f",
            draft_dir_path,
            DRAFT_CONTENT_FILE,
            age_seconds / 3600,
        )
        return True

    logger.info(
        "Skip draft directory (%s created within last 24h): path=%s age_hours=%.2f",
        DRAFT_CONTENT_FILE,
        draft_dir_path,
        age_seconds / 3600,
    )
    return False


def _remove_root_meta_info(base: str) -> bool:
    """删除草稿根目录下的 root_meta_info.json（无条件）。"""
    path = os.path.join(base, ROOT_META_INFO_FILE)
    if not os.path.isfile(path):
        return False
    try:
        os.remove(path)
        logger.info("Removed root meta file: %s", path)
        return True
    except OSError as exc:
        logger.warning("Failed to remove root meta file %s: %s", path, exc)
        return False


def _remove_draft_directory(draft_dir_path: str) -> bool:
    """删除整个草稿目录（含子目录与文件）。"""
    try:
        shutil.rmtree(draft_dir_path)
        logger.info("Removed draft directory: %s", draft_dir_path)
        return True
    except OSError as exc:
        logger.warning("Failed to remove draft directory %s: %s", draft_dir_path, exc)
        return False


def clear_draft_save_directory(
    min_age_seconds: float = DRAFT_CONTENT_MIN_AGE_SECONDS,
) -> bool:
    """
    按条件清理 ``config.DRAFT_SAVE_PATH``（保留根目录本身）。

    当且仅当 ``DRAFT_SAVE_PATH`` 对应目录存在时才执行；否则直接返回 False。

    清理规则：
    1. 根目录下的 ``root_meta_info.json``：直接删除。
    2. 子目录（草稿目录）：仅当其中 ``draft_content.json`` 的创建时间
       早于 ``min_age_seconds``（默认 24 小时）时，删除整个草稿目录。
    3. 其它根级条目：不处理。

    Returns:
        是否已执行清理（目录存在并完成扫描时为 True）。
    """
    if not draft_save_path_exists():
        logger.info(
            "Skip draft directory cleanup: DRAFT_SAVE_PATH does not exist (%s)",
            config.DRAFT_SAVE_PATH,
        )
        return False

    base = config.DRAFT_SAVE_PATH
    removed_meta = _remove_root_meta_info(base)

    removed_drafts = 0
    skipped_drafts = 0
    try:
        with os.scandir(base) as entries:
            child_names = [entry.name for entry in entries]
    except OSError as exc:
        logger.warning("Failed to list draft save directory %s: %s", base, exc)
        return False

    for name in child_names:
        if name == ROOT_META_INFO_FILE:
            continue
        path = os.path.join(base, name)
        if not os.path.isdir(path):
            continue
        if _draft_content_is_old_enough(path, min_age_seconds=min_age_seconds):
            if _remove_draft_directory(path):
                removed_drafts += 1
        else:
            skipped_drafts += 1

    logger.info(
        "Draft save directory cleanup finished: path=%s removed_root_meta=%s "
        "removed_draft_dirs=%s skipped_draft_dirs=%s",
        base,
        removed_meta,
        removed_drafts,
        skipped_drafts,
    )
    return True


def recover_from_export_failure() -> None:
    """导出失败后：强杀剪映；仅当 ``DRAFT_SAVE_PATH`` 目录存在时再做草稿清理。"""
    logger.warning(
        "Jianying export failed, recovering (draft path=%s, exists=%s)",
        config.DRAFT_SAVE_PATH,
        draft_save_path_exists(),
    )
    kill_jianying_process()
    if draft_save_path_exists():
        clear_draft_save_directory()
    else:
        logger.info(
            "Skip draft directory cleanup after export failure: "
            "DRAFT_SAVE_PATH does not exist (%s)",
            config.DRAFT_SAVE_PATH,
        )
