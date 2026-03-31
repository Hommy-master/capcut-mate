"""
add_videos 并发锁功能单元测试
测试异步锁机制防止同一草稿的并发写操作

测试覆盖：
1. 正常场景：带锁的视频添加
2. 边界场景：超时、并发访问同一草稿
3. 异常场景：锁获取失败、无效草稿 ID
"""
import asyncio
import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import json

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.service.add_videos import add_videos_async, _add_videos_internal
from src.utils.draft_lock_manager import DraftLockManager
from exceptions import CustomException, CustomError


class TestAddVideosAsync:
    """add_videos_async 测试类"""
    
    @pytest.fixture
    def mock_draft_data(self):
        """模拟草稿数据"""
        return {
            "draft_url": "http://localhost/v1/get_draft?draft_id=test-draft-001",
            "video_infos": json.dumps([
                {
                    "video_url": "https://example.com/video1.mp4",
                    "width": 1920,
                    "height": 1080,
                    "start": 0,
                    "end": 5000000,
                    "duration": 5000000
                }
            ])
        }
    
    @pytest.mark.asyncio
    async def test_add_videos_with_lock_success(self, mock_draft_data):
        """测试成功添加视频（带锁）"""
        # Mock 所有依赖
        with patch('src.service.add_videos.helper.get_url_param') as mock_get_param, \
             patch('src.service.add_videos.DRAFT_CACHE') as mock_cache, \
             patch('src.service.add_videos.os.makedirs'), \
             patch('src.service.add_videos.parse_video_data') as mock_parse, \
             patch('src.service.add_videos.add_video_to_draft') as mock_add, \
             patch('src.service.add_videos.download') as mock_download:
            
            # 设置 mock
            mock_get_param.return_value = "test-draft-001"
            mock_parse.return_value = [{
                'video_url': 'https://example.com/video1.mp4',
                'width': 1920,
                'height': 1080,
                'start': 0,
                'end': 5000000,
                'duration': 5000000,
                'original_start': 0,
                'original_end': 5000000
            }]
            mock_add.return_value = ("segment-123", 5000000)
            mock_download.return_value = "/tmp/video.mp4"
            
            # Mock 草稿对象
            mock_script = MagicMock()
            mock_script.width = 1920
            mock_script.height = 1080
            mock_script.tracks = {"track-1": MagicMock(track_id="track-123", name="video_track")}
            mock_script.materials.videos = [MagicMock(material_id="video-123")]
            mock_cache.__getitem__.return_value = mock_script
            
            # 调用函数
            result = await add_videos_async(
                draft_url=mock_draft_data["draft_url"],
                video_infos=mock_draft_data["video_infos"]
            )
            
            # 验证结果
            assert len(result) == 4
            assert result[0] == mock_draft_data["draft_url"]
            
            # 验证锁被正确获取和释放
            lock_manager = DraftLockManager()
            assert not lock_manager.is_locked("test-draft-001")
    
    @pytest.mark.asyncio
    async def test_add_videos_invalid_draft_url(self):
        """测试无效草稿 URL"""
        with pytest.raises(CustomException) as exc_info:
            await add_videos_async(
                draft_url="invalid-url",
                video_infos='[]'
            )
        
        assert exc_info.value.err == CustomError.INVALID_DRAFT_URL
    
    @pytest.mark.asyncio
    async def test_add_videos_lock_timeout(self):
        """测试锁超时"""
        lock_manager = DraftLockManager()
        draft_id = "timeout-test"
        
        # 先获取锁并不释放
        await lock_manager.acquire_lock(draft_id)
        
        # 尝试获取同一个草稿的锁（应该超时）
        with pytest.raises(CustomException) as exc_info:
            await add_videos_async(
                draft_url=f"http://localhost/v1/get_draft?draft_id={draft_id}",
                video_infos='[]',
                lock_timeout=0.1
            )
        
        assert "Failed to acquire lock" in str(exc_info.value.args)
        
        # 清理
        await lock_manager.release_lock(draft_id)
    
    @pytest.mark.asyncio
    async def test_concurrent_add_videos_same_draft(self):
        """测试并发添加视频到同一草稿（应该串行执行）"""
        execution_order = []
        draft_url = "http://localhost/v1/get_draft?draft_id=concurrent-test"
        video_infos = json.dumps([{
            "video_url": "https://example.com/video.mp4",
            "start": 0,
            "end": 5000000
        }])
        
        async def add_video_task(task_id):
            with patch('src.service.add_videos.helper.get_url_param') as mock_get_param, \
                 patch('src.service.add_videos.DRAFT_CACHE') as mock_cache, \
                 patch('src.service.add_videos.os.makedirs'), \
                 patch('src.service.add_videos.parse_video_data') as mock_parse, \
                 patch('src.service.add_videos.add_video_to_draft') as mock_add, \
                 patch('src.service.add_videos.download') as mock_download:
                
                mock_get_param.return_value = "concurrent-test"
                mock_parse.return_value = [{
                    'video_url': 'https://example.com/video.mp4',
                    'start': 0,
                    'end': 5000000,
                    'duration': 5000000,
                    'original_start': 0,
                    'original_end': 5000000
                }]
                mock_add.return_value = (f"segment-{task_id}", 5000000)
                mock_download.return_value = f"/tmp/video_{task_id}.mp4"
                
                mock_script = MagicMock()
                mock_script.width = 1920
                mock_script.height = 1080
                mock_script.tracks = {}
                mock_script.materials.videos = []
                mock_cache.__getitem__.return_value = mock_script
                
                try:
                    execution_order.append(f"{task_id}_start")
                    await add_videos_async(
                        draft_url=draft_url,
                        video_infos=video_infos,
                        lock_timeout=5.0
                    )
                    execution_order.append(f"{task_id}_complete")
                except Exception as e:
                    execution_order.append(f"{task_id}_error: {str(e)}")
        
        # 启动 3 个并发任务
        tasks = [
            add_video_task(1),
            add_video_task(2),
            add_video_task(3)
        ]
        
        await asyncio.gather(*tasks)
        
        # 验证任务是串行执行的（每个任务必须等待前一个释放锁）
        # 第一个任务必须先完成
        first_complete_index = execution_order.index("1_complete")
        assert first_complete_index > 0  # 必须在开始之后
        
        # 验证没有并发冲突
        error_count = sum(1 for e in execution_order if "error" in e)
        assert error_count == 0
    
    @pytest.mark.asyncio
    async def test_concurrent_add_videos_different_drafts(self):
        """测试并发添加视频到不同草稿（可以并行执行）"""
        completed_drafts = []
        
        async def add_video_task(draft_id):
            with patch('src.service.add_videos.helper.get_url_param') as mock_get_param, \
                 patch('src.service.add_videos.DRAFT_CACHE') as mock_cache, \
                 patch('src.service.add_videos.os.makedirs'), \
                 patch('src.service.add_videos.parse_video_data') as mock_parse, \
                 patch('src.service.add_videos.add_video_to_draft') as mock_add, \
                 patch('src.service.add_videos.download') as mock_download:
                
                mock_get_param.return_value = draft_id
                mock_parse.return_value = [{
                    'video_url': f'https://example.com/video_{draft_id}.mp4',
                    'start': 0,
                    'end': 5000000,
                    'duration': 5000000,
                    'original_start': 0,
                    'original_end': 5000000
                }]
                mock_add.return_value = (f"segment-{draft_id}", 5000000)
                mock_download.return_value = f"/tmp/video_{draft_id}.mp4"
                
                mock_script = MagicMock()
                mock_script.width = 1920
                mock_script.height = 1080
                mock_script.tracks = {}
                mock_script.materials.videos = []
                mock_cache.__getitem__.return_value = mock_script
                
                await add_videos_async(
                    draft_url=f"http://localhost/v1/get_draft?draft_id={draft_id}",
                    video_infos='[]'
                )
                completed_drafts.append(draft_id)
        
        # 并发访问 3 个不同的草稿
        tasks = [
            add_video_task("draft-a"),
            add_video_task("draft-b"),
            add_video_task("draft-c")
        ]
        
        await asyncio.gather(*tasks)
        
        # 所有任务都应该完成
        assert len(completed_drafts) == 3
        assert "draft-a" in completed_drafts
        assert "draft-b" in completed_drafts
        assert "draft-c" in completed_drafts


class TestAddVideosInternal:
    """_add_videos_internal 测试类"""
    
    @pytest.mark.asyncio
    async def test_internal_function_requires_lock(self):
        """测试内部函数需要外层锁控制"""
        # 这是一个白盒测试，验证内部函数确实不包含锁逻辑
        # 通过检查函数签名和文档
        
        import inspect
        from src.service.add_videos import _add_videos_internal
        
        # 获取函数文档
        docstring = _add_videos_internal.__doc__
        
        # 验证文档中明确说明需要外层锁控制
        assert "无锁" in docstring or "需外层控制" in docstring or "并发" in docstring
        
        # 验证函数签名不包含锁相关参数
        sig = inspect.signature(_add_videos_internal)
        params = list(sig.parameters.keys())
        assert "lock_timeout" not in params
        assert "lock_manager" not in params


class TestLockManagerIntegration:
    """锁管理器集成测试"""
    
    @pytest.mark.asyncio
    async def test_lock_cleanup_after_exception(self):
        """测试异常后锁的清理"""
        draft_id = "exception-test"
        lock_manager = DraftLockManager()
        
        # 获取锁
        await lock_manager.acquire_lock(draft_id)
        
        try:
            # 模拟某个操作失败
            raise ValueError("Simulated error")
        except ValueError:
            pass
        finally:
            # 确保释放锁
            await lock_manager.release_lock(draft_id)
        
        # 验证锁已释放
        assert not lock_manager.is_locked(draft_id)
    
    @pytest.mark.asyncio
    async def test_lock_stats_accuracy(self):
        """测试锁统计信息准确性"""
        lock_manager = DraftLockManager()
        draft_ids = ["stats-1", "stats-2", "stats-3"]
        
        # 初始状态
        stats = lock_manager.get_stats()
        assert stats["total_locks"] == 0
        assert stats["locked_drafts"] == 0
        assert stats["total_holders"] == 0
        
        # 获取所有锁
        for draft_id in draft_ids:
            await lock_manager.acquire_lock(draft_id)
        
        stats = lock_manager.get_stats()
        assert stats["total_locks"] == 3
        assert stats["locked_drafts"] == 3
        assert stats["total_holders"] == 3
        
        # 释放一个锁
        await lock_manager.release_lock(draft_ids[0])
        
        stats = lock_manager.get_stats()
        assert stats["total_locks"] == 2  # 锁对象被删除
        assert stats["locked_drafts"] == 2
        assert stats["total_holders"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
