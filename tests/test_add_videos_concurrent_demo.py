"""
add_videos 并发保护功能演示测试
简单演示锁机制如何防止同一草稿的并发写操作
"""
import asyncio
import pytest
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.draft_lock_manager import DraftLockManager


class TestConcurrentProtectionDemo:
    """并发保护演示测试"""
    
    @pytest.mark.asyncio
    async def test_same_draft_serialized_access(self):
        """演示：同一草稿的并发访问会被强制串行化"""
        lock_manager = DraftLockManager()
        draft_id = "demo-draft"
        
        execution_log = []
        
        async def worker(worker_id, work_duration=0.1):
            """模拟一个 add_videos 请求"""
            await lock_manager.acquire_lock(draft_id)
            try:
                # 开始处理
                execution_log.append(f"worker_{worker_id}_start")
                await asyncio.sleep(work_duration)  # 模拟写入草稿文件
                execution_log.append(f"worker_{worker_id}_end")
            finally:
                await lock_manager.release_lock(draft_id)
        
        # 启动 3 个并发请求（实际场景是 3 个 HTTP 请求同时调用 add_videos）
        tasks = [
            worker(1),
            worker(2),
            worker(3)
        ]
        
        await asyncio.gather(*tasks)
        
        # 验证：由于锁的保护，任务必须一个接一个执行
        # 每个 worker 的 start 和 end 必须是连续的
        print("\n执行日志:")
        for i, log in enumerate(execution_log):
            print(f"  {i+1}. {log}")
        
        # 验证没有并发冲突（不会有交叉执行）
        assert len(execution_log) == 6
        
        # 验证每个 worker 都是成对执行的
        for i in range(0, len(execution_log), 2):
            worker_num = execution_log[i].split('_')[1]
            assert execution_log[i].endswith('_start')
            assert execution_log[i+1].endswith('_end')
            assert execution_log[i+1].split('_')[1] == worker_num
    
    @pytest.mark.asyncio
    async def test_different_drafts_parallel_access(self):
        """演示：不同草稿可以并行访问"""
        lock_manager = DraftLockManager()
        
        execution_log = []
        
        async def worker(draft_id, worker_id):
            """模拟处理不同草稿的请求"""
            await lock_manager.acquire_lock(draft_id)
            try:
                execution_log.append(f"worker_{worker_id}_processing_{draft_id}")
                await asyncio.sleep(0.1)
            finally:
                await lock_manager.release_lock(draft_id)
        
        # 3 个 worker 处理不同的草稿
        tasks = [
            worker("draft-A", 1),
            worker("draft-B", 2),
            worker("draft-C", 3)
        ]
        
        await asyncio.gather(*tasks)
        
        print("\n不同草稿并行处理日志:")
        for log in execution_log:
            print(f"  {log}")
        
        # 验证：所有任务都完成了
        assert len(execution_log) == 3
        
        # 验证：每个草稿都被处理了
        drafts_processed = [log.split('_')[-1] for log in execution_log]
        assert "draft-A" in drafts_processed
        assert "draft-B" in drafts_processed
        assert "draft-C" in drafts_processed
    
    @pytest.mark.asyncio
    async def test_lock_prevents_concurrent_writes(self):
        """演示：锁机制防止并发写入导致文件损坏"""
        lock_manager = DraftLockManager()
        draft_id = "protected-draft"
        
        # 模拟共享资源（草稿文件）
        shared_data = {"counter": 0, "corrupted": False}
        
        async def unsafe_write(worker_id):
            """没有锁保护的写入（会导致损坏）"""
            # 读取
            current = shared_data["counter"]
            await asyncio.sleep(0.01)  # 模拟 I/O 延迟
            # 写入
            shared_data["counter"] = current + 1
            
            # 检查是否有并发修改
            if shared_data["counter"] > max(int(worker_id), 1):
                shared_data["corrupted"] = True
        
        async def safe_write(worker_id):
            """有锁保护的写入（安全）"""
            await lock_manager.acquire_lock(draft_id)
            try:
                current = shared_data["counter"]
                await asyncio.sleep(0.01)
                shared_data["counter"] = current + 1
            finally:
                await lock_manager.release_lock(draft_id)
        
        # 测试不安全的写入（注释掉，避免真正损坏数据）
        # unsafe_tasks = [unsafe_write(i) for i in range(1, 11)]
        # await asyncio.gather(*unsafe_tasks)
        # print(f"\n不安全写入结果：counter={shared_data['counter']}, corrupted={shared_data['corrupted']}")
        
        # 重置
        shared_data["counter"] = 0
        shared_data["corrupted"] = False
        
        # 测试安全的写入
        safe_tasks = [safe_write(i) for i in range(1, 11)]
        await asyncio.gather(*safe_tasks)
        
        print(f"\n安全写入结果：counter={shared_data['counter']}, corrupted={shared_data['corrupted']}")
        
        # 验证：有锁保护时，counter 应该正好是 10
        assert shared_data["counter"] == 10
        assert shared_data["corrupted"] is False


if __name__ == "__main__":
    # 运行演示
    async def main():
        tester = TestConcurrentProtectionDemo()
        
        print("=" * 60)
        print("测试 1: 同一草稿的串行访问")
        print("=" * 60)
        await tester.test_same_draft_serialized_access()
        
        print("\n" + "=" * 60)
        print("测试 2: 不同草稿的并行访问")
        print("=" * 60)
        await tester.test_different_drafts_parallel_access()
        
        print("\n" + "=" * 60)
        print("测试 3: 锁保护防止并发写入")
        print("=" * 60)
        await tester.test_lock_prevents_concurrent_writes()
        
        print("\n" + "=" * 60)
        print("所有演示完成！")
        print("=" * 60)
    
    asyncio.run(main())
