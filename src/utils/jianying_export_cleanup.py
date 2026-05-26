"""剪映导出失败后的恢复：强杀进程并清空本地草稿目录。"""
from __future__ import annotations

import os
import shutil
import subprocess
from typing import Iterable

import config
from src.utils.logger import logger

# 剪映专业版主进程及常见子进程映像名
JIANYING_PROCESS_IMAGE_NAMES: tuple[str, ...] = (
    "JianyingPro.exe",
)


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


def clear_draft_save_directory() -> None:
    """删除 ``config.DRAFT_SAVE_PATH`` 下的全部文件、目录及子目录（保留根目录本身）。"""
    base = config.DRAFT_SAVE_PATH
    if not base:
        logger.warning("DRAFT_SAVE_PATH is empty, skip draft directory cleanup")
        return
    if not os.path.isdir(base):
        logger.warning("Draft save path is not a directory, skip cleanup: %s", base)
        return

    removed = 0
    try:
        with os.scandir(base) as entries:
            names = [entry.name for entry in entries]
    except OSError as exc:
        logger.warning("Failed to list draft save directory %s: %s", base, exc)
        return

    for name in names:
        path = os.path.join(base, name)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            removed += 1
            logger.info("Removed draft save entry: %s", path)
        except OSError as exc:
            logger.warning("Failed to remove draft save entry %s: %s", path, exc)

    logger.info(
        "Cleared draft save directory: path=%s removed_entries=%s",
        base,
        removed,
    )


def recover_from_export_failure() -> None:
    """导出失败后：强杀剪映并清空 ``config.DRAFT_SAVE_PATH`` 下的全部内容。"""
    logger.warning(
        "Jianying export failed, recovering: kill process and clear draft dir %s",
        config.DRAFT_SAVE_PATH,
    )
    kill_jianying_process()
    clear_draft_save_directory()
