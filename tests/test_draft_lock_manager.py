"""
草稿并发锁管理器单元测试
测试 DraftLockManager 的所有功能

测试覆盖：
1. 正常场景：锁的获取和释放
2. 边界场景：超时、重入、并发访问
3. 异常场景：无效输入、重复释放
"""
import asyncio
import pytest
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.draft_lock_manager import DraftLockManager, get_draft_lock_manager


class TestDraftLockManager:
    """DraftLockManager 测试类"""
    
    @pytest.fixture
    def lock_manager(self):
        """创建锁管理器实例"""
        return DraftLockManager()
    
    @pytest.mark.asyncio
    async def test_acquire_and_release_lock(self, lock_manager):
        """测试基本的锁获取和释放"""
        draft_id = "test-draft-001"
        
        # 获取锁
        result = await lock_manager.acquire_lock(draft_id)
        assert result is True
        assert lock_manager.is_locked(draft_id) is True
        assert lock_manager.get_lock_count(draft_id) == 1
        
        # 释放锁
        await lock_manager.release_lock(draft_id)
        assert lock_manager.is_locked(draft_id) is False
        assert lock_manager.get_lock_count(draft_id) == 0
    
    @pytest.mark.asyncio
    async def test_acquire_lock_with_timeout(self, lock_manager):
        """测试带超时的锁获取"""
        draft_id = "test-draft-002"
        
        # 立即获取锁（无超时）
        result = await lock_manager.acquire_lock(draft_id, timeout=None)
        assert result is True
        
        await lock_manager.release_lock(draft_id)
        
        # 带超时获取锁
        result = await lock_manager.acquire_lock(draft_id, timeout=5.0)
        assert result is True
        
        await lock_manager.release_lock(draft_id)
    
    @pytest.mark.asyncio
    async def test_acquire_lock_timeout_exception(self, lock_manager):
        """测试锁获取超时异常"""
        draft_id = "test-draft-003"
        
        # 第一次获取锁
        await lock_manager.acquire_lock(draft_id)
        
        # 尝试再次获取（应该超时）
        with pytest.raises(asyncio.TimeoutError):
            await lock_manager.acquire_lock(draft_id, timeout=0.1)
        
        # 清理
        await lock_manager.release_lock(draft_id)
    
    @pytest.mark.asyncio
    async def test_release_nonexistent_lock(self, lock_manager):
        """测试释放不存在的锁"""
        draft_id = "nonexistent-draft"
        
        with pytest.raises(KeyError):
            await lock_manager.release_lock(draft_id)
    
    @pytest.mark.asyncio
    async def test_is_locked_method(self, lock_manager):
        """测试 is_locked 方法"""
        draft_id = "test-draft-004"
        
        # 未锁定时
        assert lock_manager.is_locked(draft_id) is False
        
        # 锁定后
        await lock_manager.acquire_lock(draft_id)
        assert lock_manager.is_locked(draft_id) is True
        
        # 释放后
        await lock_manager.release_lock(draft_id)
        assert lock_manager.is_locked(draft_id) is False
    
    @pytest.mark.asyncio
    async def test_get_lock_count(self, lock_manager):
        """测试获取锁计数"""
        draft_id = "test-draft-005"
        
        # 初始计数为 0
        assert lock_manager.get_lock_count(draft_id) == 0
        
        # 获取一次锁
        await lock_manager.acquire_lock(draft_id)
        assert lock_manager.get_lock_count(draft_id) == 1
        
        # 释放锁
        await lock_manager.release_lock(draft_id)
        assert lock_manager.get_lock_count(draft_id) == 0
    
    @pytest.mark.asyncio
    async def test_get_all_locked_drafts(self, lock_manager):
        """测试获取所有被锁定的草稿"""
        draft_ids = ["test-draft-006-a", "test-draft-006-b", "test-draft-006-c"]
        
        # 锁定前两个
        await lock_manager.acquire_lock(draft_ids[0])
        await lock_manager.acquire_lock(draft_ids[1])
        
        locked = lock_manager.get_all_locked_drafts()
        assert len(locked) == 2
        assert draft_ids[0] in locked
        assert draft_ids[1] in locked
        assert draft_ids[2] not in locked
        
        # 释放一个
        await lock_manager.release_lock(draft_ids[0])
        locked = lock_manager.get_all_locked_drafts()
        assert len(locked) == 1
        assert draft_ids[1] in locked
        
        # 全部释放
        await lock_manager.release_lock(draft_ids[1])
        locked = lock_manager.get_all_locked_drafts()
        assert len(locked) == 0
    
    @pytest.mark.asyncio
    async def test_clear_all_locks(self, lock_manager):
        """测试清除所有锁"""
        draft_ids = ["test-draft-007-a", "test-draft-007-b"]
        
        # 获取多个锁
        for draft_id in draft_ids:
            await lock_manager.acquire_lock(draft_id)
        
        # 验证都被锁定
        for draft_id in draft_ids:
            assert lock_manager.is_locked(draft_id) is True
        
        # 清除所有锁
        await lock_manager.clear_all_locks()
        
        # 验证都已释放（锁对象已被删除）
        for draft_id in draft_ids:
            assert lock_manager.is_locked(draft_id) is False
    
    @pytest.mark.asyncio
    async def test_get_stats(self, lock_manager):
        """测试获取统计信息"""
        draft_ids = ["test-draft-008-a", "test-draft-008-b"]
        
        # 初始状态
        stats = lock_manager.get_stats()
        assert stats["total_locks"] == 0
        assert stats["locked_drafts"] == 0
        
        # 获取锁后
        for draft_id in draft_ids:
            await lock_manager.acquire_lock(draft_id)
        
        stats = lock_manager.get_stats()
        assert stats["total_locks"] == 2
        assert stats["locked_drafts"] == 2
        assert stats["total_holders"] == 2
        
        # 清理
        for draft_id in draft_ids:
            await lock_manager.release_lock(draft_id)
    
    @pytest.mark.asyncio
    async def test_concurrent_access_different_drafts(self, lock_manager):
        """测试并发访问不同草稿"""
        results = []
        
        async def acquire_and_release(draft_id):
            await lock_manager.acquire_lock(draft_id)
            await asyncio.sleep(0.1)  # 模拟工作
            results.append(draft_id)
            await lock_manager.release_lock(draft_id)
        
        # 并发访问 3 个不同的草稿
        tasks = [
            acquire_and_release("draft-a"),
            acquire_and_release("draft-b"),
            acquire_and_release("draft-c")
        ]
        
        await asyncio.gather(*tasks)
        
        # 所有任务都应该完成
        assert len(results) == 3
        assert "draft-a" in results
        assert "draft-b" in results
        assert "draft-c" in results
    
    @pytest.mark.asyncio
    async def test_serial_access_same_draft(self, lock_manager):
        """测试串行访问同一草稿"""
        draft_id = "test-draft-same"
        execution_order = []
        
        async def worker(worker_id):
            await lock_manager.acquire_lock(draft_id)
            try:
                execution_order.append(f"{worker_id}_start")
                await asyncio.sleep(0.1)
                execution_order.append(f"{worker_id}_end")
            finally:
                await lock_manager.release_lock(draft_id)
        
        # 3 个 worker 按顺序访问同一草稿（不是并发）
        # 因为 asyncio.gather 会同时启动所有任务，但锁会强制它们串行执行
        tasks = [
            worker(1),
            worker(2),
            worker(3)
        ]
        
        await asyncio.gather(*tasks)
        
        # 验证执行顺序是串行的（每个 worker 必须等待前一个完成）
        # 由于锁的保护，应该是一个接一个执行
        assert len(execution_order) == 6
        
        # 验证每个 worker 都是成对的 start->end
        for i in range(0, len(execution_order), 2):
            worker_num = execution_order[i].split('_')[0]
            assert execution_order[i+1] == f"{worker_num}_end"
    
    @pytest.mark.asyncio
    async def test_singleton_pattern(self):
        """测试单例模式"""
        manager1 = DraftLockManager()
        manager2 = DraftLockManager()
        
        # 应该是同一个实例
        assert manager1 is manager2
    
    @pytest.mark.asyncio
    async def test_get_draft_lock_manager_function(self):
        """测试全局获取器函数"""
        manager1 = get_draft_lock_manager()
        manager2 = get_draft_lock_manager()
        
        # 应该是同一个实例
        assert manager1 is manager2


class TestDraftLockManagerEdgeCases:
    """DraftLockManager 边界情况测试"""
    
    @pytest.mark.asyncio
    async def test_empty_draft_id(self):
        """测试空字符串草稿 ID"""
        lock_manager = DraftLockManager()
        
        # 空字符串也应该能获取锁
        draft_id = ""
        result = await lock_manager.acquire_lock(draft_id)
        assert result is True
        
        await lock_manager.release_lock(draft_id)
    
    @pytest.mark.asyncio
    async def test_special_characters_in_draft_id(self):
        """测试特殊字符的草稿 ID"""
        lock_manager = DraftLockManager()
        
        special_ids = [
            "draft-with-dash",
            "draft_with_underscore",
            "draft.with.dots",
            "draft/with/slashes",
            "draft@with#special$chars"
        ]
        
        for draft_id in special_ids:
            await lock_manager.acquire_lock(draft_id)
            assert lock_manager.is_locked(draft_id) is True
            await lock_manager.release_lock(draft_id)
            assert lock_manager.is_locked(draft_id) is False
    
    @pytest.mark.asyncio
    async def test_very_long_draft_id(self):
        """测试超长草稿 ID"""
        lock_manager = DraftLockManager()
        
        # 创建一个很长的 ID
        long_id = "draft-" + "a" * 1000
        
        await lock_manager.acquire_lock(long_id)
        assert lock_manager.is_locked(long_id) is True
        await lock_manager.release_lock(long_id)
    
    @pytest.mark.asyncio
    async def test_rapid_acquire_release_cycle(self):
        """测试快速连续获取释放循环"""
        lock_manager = DraftLockManager()
        draft_id = "rapid-cycle"
        
        # 快速循环 100 次
        for i in range(100):
            await lock_manager.acquire_lock(draft_id)
            await lock_manager.release_lock(draft_id)
        
        # 最后应该是未锁定状态
        assert lock_manager.is_locked(draft_id) is False
    
    @pytest.mark.asyncio
    async def test_multiple_workers_same_draft_stress(self):
        """测试多 worker 压力测试"""
        lock_manager = DraftLockManager()
        draft_id = "stress-test"
        counter = 0
        
        async def increment_counter():
            nonlocal counter
            await lock_manager.acquire_lock(draft_id)
            try:
                current = counter
                await asyncio.sleep(0.01)  # 增加竞争
                counter = current + 1
            finally:
                await lock_manager.release_lock(draft_id)
        
        # 10 个 worker 同时尝试增加计数器
        tasks = [increment_counter() for _ in range(10)]
        await asyncio.gather(*tasks)
        
        # 由于锁的保护，counter 应该正好是 10
        assert counter == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
