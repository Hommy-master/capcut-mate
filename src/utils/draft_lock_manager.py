"""
草稿并发锁管理器
用于防止同一草稿的并发写操作导致文件损坏
"""
import asyncio
import time
from typing import Dict, Optional
from src.utils.logger import logger


class DraftLockManager:
    """
    草稿锁管理器 - 单例模式
    
    功能：
    1. 为每个草稿 ID 维护一个独立的锁
    2. 支持异步获取和释放锁
    3. 自动清理已释放的锁以节省内存
    4. 提供锁状态查询功能
    
    使用场景：
    - add_videos: 防止并发写入同一草稿文件
    - add_audios: 防止并发修改同一草稿配置
    - save_draft: 防止并发保存导致数据丢失
    """
    
    _instance = None
    _init_lock = asyncio.Lock()
    
    def __new__(cls):
        """确保单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化管理器"""
        # 如果已经初始化过，则跳过
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        # 存储每个草稿的锁：{draft_id: asyncio.Lock}
        self._locks: Dict[str, asyncio.Lock] = {}
        # 存储每个锁的持有者数量（用于引用计数）
        self._lock_counts: Dict[str, int] = {}
        # 诊断信息：记录最近持有者与持锁开始时间（用于定位“为什么会等满timeout”）
        self._lock_owner: Dict[str, str] = {}
        self._lock_acquired_at: Dict[str, float] = {}
        # 初始化锁（用于保护_locks 字典的修改）
        self._manager_lock = asyncio.Lock()
        # 标记初始化完成
        self._initialized = True
        
        logger.info("DraftLockManager initialized")
    
    async def acquire_lock(self, draft_id: str, timeout: Optional[float] = None) -> bool:
        """
        获取指定草稿的锁
        
        Args:
            draft_id: 草稿 ID
            timeout: 超时时间（秒），None 表示无限等待
        
        Returns:
            bool: 是否成功获取锁
        
        Raises:
            asyncio.TimeoutError: 等待超时时抛出
        
        Example:
            >>> lock_manager = DraftLockManager()
            >>> success = await lock_manager.acquire_lock("2025092811473036584258", timeout=5.0)
            >>> if success:
            ...     try:
            ...         # 执行草稿写操作
            ...         pass
            ...     finally:
            ...         await lock_manager.release_lock("2025092811473036584258")
        """
        async with self._manager_lock:
            # 如果草稿 ID 没有锁，则创建新锁
            if draft_id not in self._locks:
                self._locks[draft_id] = asyncio.Lock()
                self._lock_counts[draft_id] = 0
            
            lock = self._locks[draft_id]
        
        # 尝试获取锁（带超时）
        wait_started_at = time.monotonic()
        try:
            if timeout is not None:
                # 使用 wait_for 实现超时
                await asyncio.wait_for(lock.acquire(), timeout=timeout)
            else:
                # 无限等待
                await lock.acquire()
            
            # 增加引用计数
            async with self._manager_lock:
                self._lock_counts[draft_id] = self._lock_counts.get(draft_id, 0) + 1
                task = asyncio.current_task()
                task_name = task.get_name() if task and hasattr(task, "get_name") else None
                self._lock_owner[draft_id] = task_name or "unknown"
                self._lock_acquired_at[draft_id] = time.monotonic()
            
            waited = time.monotonic() - wait_started_at
            logger.info(
                f"Lock acquired for draft_id: {draft_id}, waited: {waited:.3f}s, count: {self._lock_counts[draft_id]}"
            )
            return True
            
        except asyncio.TimeoutError:
            waited = time.monotonic() - wait_started_at
            async with self._manager_lock:
                owner = self._lock_owner.get(draft_id)
                acquired_at = self._lock_acquired_at.get(draft_id)
                held_for = (time.monotonic() - acquired_at) if acquired_at else None
                count = self._lock_counts.get(draft_id, 0)
                locked = self._locks.get(draft_id).locked() if draft_id in self._locks else False
            if held_for is not None:
                logger.warning(
                    f"Timeout waiting for lock on draft_id: {draft_id}, waited: {waited:.3f}s, "
                    f"locked: {locked}, holders: {count}, owner: {owner}, held_for: {held_for:.3f}s"
                )
            else:
                logger.warning(
                    f"Timeout waiting for lock on draft_id: {draft_id}, waited: {waited:.3f}s, "
                    f"locked: {locked}, holders: {count}, owner: {owner}"
                )
            raise
    
    async def release_lock(self, draft_id: str) -> None:
        """
        释放指定草稿的锁
        
        Args:
            draft_id: 草稿 ID
        
        Raises:
            RuntimeError: 当尝试释放未持有的锁时抛出
            KeyError: 当草稿 ID 不存在时抛出
        
        Example:
            >>> lock_manager = DraftLockManager()
            >>> await lock_manager.acquire_lock("draft-123")
            >>> try:
            ...     # 执行写操作
            ...     pass
            ... finally:
            ...     await lock_manager.release_lock("draft-123")
        """
        async with self._manager_lock:
            if draft_id not in self._locks:
                raise KeyError(f"No lock found for draft_id: {draft_id}")
            
            lock = self._locks[draft_id]
            self._lock_counts[draft_id] = max(0, self._lock_counts.get(draft_id, 0) - 1)
            acquired_at = self._lock_acquired_at.get(draft_id)
            owner = self._lock_owner.get(draft_id)
        
        # 释放锁（在 manager_lock 之外，避免死锁）
        try:
            lock.release()
            held_for = (time.monotonic() - acquired_at) if acquired_at else None
            logger.info(
                f"Lock released for draft_id: {draft_id}, held_for: {held_for:.3f}s, owner: {owner}"
                if held_for is not None else
                f"Lock released for draft_id: {draft_id}, owner: {owner}"
            )
        except RuntimeError as e:
            logger.error(f"Failed to release lock for draft_id {draft_id}: {str(e)}")
            raise
        finally:
            async with self._manager_lock:
                # 无持有者、未锁定、且无等待者时回收锁对象，避免 draft_id 维度常驻增长
                lock_obj = self._locks.get(draft_id)
                if lock_obj is not None:
                    waiters = getattr(lock_obj, "_waiters", None)
                    has_waiters = bool(waiters) if waiters is not None else False
                    if (
                        self._lock_counts.get(draft_id, 0) <= 0
                        and not lock_obj.locked()
                        and not has_waiters
                    ):
                        self._locks.pop(draft_id, None)
                        self._lock_counts.pop(draft_id, None)
                self._lock_owner.pop(draft_id, None)
                self._lock_acquired_at.pop(draft_id, None)

    def is_locked(self, draft_id: str) -> bool:
        """
        检查指定草稿是否被锁定
        
        Args:
            draft_id: 草稿 ID
        
        Returns:
            bool: 如果草稿被锁定返回 True，否则返回 False
        
        Example:
            >>> lock_manager = DraftLockManager()
            >>> await lock_manager.acquire_lock("draft-123")
            >>> print(lock_manager.is_locked("draft-123"))  # True
            >>> await lock_manager.release_lock("draft-123")
            >>> print(lock_manager.is_locked("draft-123"))  # False
        """
        if draft_id not in self._locks:
            return False
        
        return self._locks[draft_id].locked()
    
    def get_lock_count(self, draft_id: str) -> int:
        """
        获取指定草稿的锁持有计数
        
        Args:
            draft_id: 草稿 ID
        
        Returns:
            int: 锁持有次数（重入次数）
        
        Example:
            >>> lock_manager = DraftLockManager()
            >>> await lock_manager.acquire_lock("draft-123")
            >>> print(lock_manager.get_lock_count("draft-123"))  # 1
        """
        return self._lock_counts.get(draft_id, 0)
    
    def get_all_locked_drafts(self) -> list:
        """
        获取所有当前被锁定的草稿 ID 列表
        
        Returns:
            list: 被锁定的草稿 ID 列表
        
        Example:
            >>> lock_manager = DraftLockManager()
            >>> await lock_manager.acquire_lock("draft-123")
            >>> locked = lock_manager.get_all_locked_drafts()
            >>> print(locked)  # ["draft-123"]
        """
        return [
            draft_id for draft_id, lock in self._locks.items()
            if lock.locked()
        ]
    
    async def clear_all_locks(self) -> None:
        """
        清除所有锁（仅在紧急情况下使用）
        
        Warning: 此方法会强制释放所有锁，可能导致数据不一致
        仅应在系统异常或死锁检测时使用
        
        Example:
            >>> lock_manager = DraftLockManager()
            >>> # 检测到死锁时
            >>> await lock_manager.clear_all_locks()
        """
        async with self._manager_lock:
            released_count = len(self._locks)
            self._locks.clear()
            self._lock_counts.clear()
            
        if released_count > 0:
            logger.warning(f"Cleared all locks, released {released_count} locks")
    
    def get_stats(self) -> dict:
        """
        获取锁管理器统计信息
        
        Returns:
            dict: 包含锁统计信息的字典
        
        Example:
            >>> lock_manager = DraftLockManager()
            >>> stats = lock_manager.get_stats()
            >>> print(stats)  # {"total_locks": 5, "locked_drafts": 2}
        """
        locked_count = sum(1 for lock in self._locks.values() if lock.locked())
        return {
            "total_locks": len(self._locks),
            "locked_drafts": locked_count,
            "total_holders": sum(self._lock_counts.values())
        }


# 全局单例
_draf_lock_manager: Optional[DraftLockManager] = None


def get_draft_lock_manager() -> DraftLockManager:
    """
    获取全局草稿锁管理器实例
    
    Returns:
        DraftLockManager: 单例锁管理器实例
    
    Example:
        >>> lock_manager = get_draft_lock_manager()
        >>> await lock_manager.acquire_lock("draft-123")
    """
    global _draf_lock_manager
    if _draf_lock_manager is None:
        _draf_lock_manager = DraftLockManager()
    return _draf_lock_manager
