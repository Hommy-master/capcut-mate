from src.utils.logger import logger
import src.pyJianYingDraft as draft
from src.utils.draft_cache import DRAFT_CACHE
from src.utils import helper
from exceptions import CustomException, CustomError
import config
import os
import asyncio
from src.utils.draft_lock_manager import DraftLockManager


def save_draft(draft_url: str) -> str:
    """
    保存剪映草稿的业务逻辑
    
    Args:
        draft_url: 草稿URL
    
    Returns:
        draft_url: 草稿URL
        message: 响应消息，如果成功就返回"草稿保存成功"，失败就返回具体错误信息
    """

    # 从URL中提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        logger.info("invalid draft url: %s", draft_url)
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    # 从缓存中获取草稿
    script = DRAFT_CACHE[draft_id]

    # 保存草稿
    script.save()

    logger.info(f"save draft success: %s", os.path.join(config.DRAFT_DIR, draft_id))
    return draft_url


async def save_draft_async(draft_url: str, lock_timeout: float = 30.0) -> str:
    """
    保存剪映草稿的异步版本（带并发锁保护）
    
    功能：
    1. 使用 DraftLockManager 防止同一草稿的并发写操作
    2. 支持超时控制，避免无限等待
    3. 自动释放锁，即使发生异常
    
    Args:
        draft_url: 草稿 URL，格式：".../get_draft?draft_id=xxx"
        lock_timeout: 获取锁的超时时间（秒），默认 30 秒
    
    Returns:
        draft_url: 草稿 URL
    
    Raises:
        CustomException: 草稿保存失败或获取锁超时
        asyncio.TimeoutError: 等待锁超时时抛出
    
    Example:
        >>> result = await save_draft_async(draft_url="http://.../draft_id=123")
    """
    # 提取草稿 ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if not draft_id:
        raise CustomException(CustomError.INVALID_DRAFT_URL)
    
    # 获取锁管理器
    lock_manager = DraftLockManager()
    
    # 尝试获取锁
    try:
        await lock_manager.acquire_lock(draft_id, timeout=lock_timeout)
        logger.info(f"Lock acquired for draft_id: {draft_id}")
    except asyncio.TimeoutError:
        logger.error(f"Timeout waiting for lock on draft_id: {draft_id}")
        raise CustomException(
            CustomError.DRAFT_LOCK_TIMEOUT,
            f"Failed to acquire lock for draft {draft_id} within {lock_timeout}s"
        )
    
    try:
        # 调用内部处理函数（不获取锁，由外层控制）
        return save_draft(draft_url=draft_url)
    finally:
        # 释放锁
        await lock_manager.release_lock(draft_id)
        logger.info(f"Lock released for draft_id: {draft_id}")
