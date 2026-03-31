"""
草稿并发锁功能单元测试 - 所有支持锁的 API
测试异步锁机制防止同一草稿的并发写操作

测试覆盖：
1. 正常场景：带锁的操作成功执行
2. 边界场景：超时、并发访问同一草稿
3. 异常场景：锁获取失败、无效草稿 ID

测试的 API 列表：
- add_audios_async
- add_images_async
- save_draft_async
- add_captions_async
- add_effects_async
- add_keyframes_async
- add_sticker_async
- add_filters_async
- easy_create_material_async
- add_masks_async
"""
import asyncio
import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import json

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.service.add_audios import add_audios_async
from src.service.add_images import add_images_async
from src.service.save_draft import save_draft_async
from src.service.add_captions import add_captions_async
from src.service.add_effects import add_effects_async
from src.service.add_keyframes import add_keyframes_async
from src.service.add_sticker import add_sticker_async
from src.service.add_filters import add_filters_async
from src.service.easy_create_material import easy_create_material_async
from src.service.add_masks import add_masks_async
from src.utils.draft_lock_manager import DraftLockManager
from exceptions import CustomException, CustomError


class TestAllAsyncLockAPIs:
    """所有带锁异步 API 的测试类"""
    
    @pytest.fixture
    def mock_draft_data(self):
        """模拟草稿数据"""
        return {
            "draft_url": "http://localhost/v1/get_draft?draft_id=test-draft-001",
            "draft_id": "test-draft-001"
        }
    
    @pytest.mark.asyncio
    async def test_save_draft_async_normal(self, mock_draft_data):
        """测试 save_draft_async 正常场景"""
        with patch('src.service.save_draft.DRAFT_CACHE') as mock_cache, \
             patch('src.service.save_draft.helper.get_url_param', return_value=mock_draft_data['draft_id']):
            
            # 模拟草稿对象
            mock_script = MagicMock()
            mock_script.save.return_value = None
            mock_cache.__getitem__.return_value = mock_script
            
            # 执行测试
            result = await save_draft_async(draft_url=mock_draft_data['draft_url'])
            
            # 验证结果
            assert result == mock_draft_data['draft_url']
            mock_script.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_add_audios_async_normal(self, mock_draft_data):
        """测试 add_audios_async 正常场景"""
        audio_infos = json.dumps([
            {
                "audio_url": "https://example.com/audio.mp3",
                "start": 0,
                "end": 5000000
            }
        ])
        
        with patch('src.service.add_audios.DRAFT_CACHE') as mock_cache, \
             patch('src.service.add_audios.helper.get_url_param', return_value=mock_draft_data['draft_id']), \
             patch('src.service.add_audios.download') as mock_download, \
             patch('src.service.add_audios.AudioMaterial') as mock_audio_material, \
             patch('src.service.add_audios.os.makedirs'):
            
            # 模拟草稿对象
            mock_script = MagicMock()
            mock_script.save.return_value = None
            mock_script.tracks = {'track1': MagicMock(track_id='track-id-123', name='audio_track')}
            mock_script.width = 1920
            mock_script.height = 1080
            mock_cache.__getitem__.return_value = mock_script
            
            # 模拟下载和音频处理
            mock_download.return_value = '/tmp/audio.mp3'
            mock_audio_material.return_value.duration = 5000000
            
            # 执行测试
            result = await add_audios_async(
                draft_url=mock_draft_data['draft_url'],
                audio_infos=audio_infos
            )
            
            # 验证结果
            assert len(result) == 3
            assert result[0] == mock_draft_data['draft_url']
    
    @pytest.mark.asyncio
    async def test_add_images_async_normal(self, mock_draft_data):
        """测试 add_images_async 正常场景"""
        image_infos = json.dumps([
            {
                "image_url": "https://example.com/image.jpg",
                "width": 1024,
                "height": 1024,
                "start": 0,
                "end": 5000000
            }
        ])
        
        with patch('src.service.add_images.DRAFT_CACHE') as mock_cache, \
             patch('src.service.add_images.helper.get_url_param', return_value=mock_draft_data['draft_id']), \
             patch('src.service.add_images.download') as mock_download, \
             patch('src.service.add_images.os.makedirs'):
            
            # 模拟草稿对象
            mock_script = MagicMock()
            mock_script.save.return_value = None
            mock_script.tracks = {'track1': MagicMock(track_id='track-id-123', name='image_track')}
            mock_script.width = 1920
            mock_script.height = 1080
            mock_cache.__getitem__.return_value = mock_script
            
            # 模拟下载
            mock_download.return_value = '/tmp/image.jpg'
            
            # 执行测试
            result = await add_images_async(
                draft_url=mock_draft_data['draft_url'],
                image_infos=image_infos
            )
            
            # 验证结果
            assert len(result) == 5
            assert result[0] == mock_draft_data['draft_url']
    
    @pytest.mark.asyncio
    async def test_add_captions_async_normal(self, mock_draft_data):
        """测试 add_captions_async 正常场景"""
        captions = json.dumps([
            {
                "start": 0,
                "end": 5000000,
                "text": "你好，剪映"
            }
        ])
        
        with patch('src.service.add_captions.DRAFT_CACHE') as mock_cache, \
             patch('src.service.add_captions.helper.get_url_param', return_value=mock_draft_data['draft_id']):
            
            # 模拟草稿对象
            mock_script = MagicMock()
            mock_script.save.return_value = None
            mock_script.tracks = {'track1': MagicMock(track_id='track-id-123', name='caption_track')}
            mock_script.width = 1920
            mock_script.height = 1080
            mock_cache.__getitem__.return_value = mock_script
            
            # 执行测试
            result = await add_captions_async(
                draft_url=mock_draft_data['draft_url'],
                captions=captions
            )
            
            # 验证结果
            assert len(result) == 5
            assert result[0] == mock_draft_data['draft_url']
    
    @pytest.mark.asyncio
    async def test_add_effects_async_normal(self, mock_draft_data):
        """测试 add_effects_async 正常场景"""
        effect_infos = json.dumps([
            {
                "effect_title": "录制边框 III",
                "start": 0,
                "end": 5000000
            }
        ])
        
        with patch('src.service.add_effects.DRAFT_CACHE') as mock_cache, \
             patch('src.service.add_effects.helper.get_url_param', return_value=mock_draft_data['draft_id']):
            
            # 模拟草稿对象
            mock_script = MagicMock()
            mock_script.save.return_value = None
            mock_script.tracks = {'track1': MagicMock(track_id='track-id-123', name='effect_track')}
            mock_cache.__getitem__.return_value = mock_script
            
            # 执行测试
            result = await add_effects_async(
                draft_url=mock_draft_data['draft_url'],
                effect_infos=effect_infos
            )
            
            # 验证结果
            assert len(result) == 4
            assert result[0] == mock_draft_data['draft_url']
    
    @pytest.mark.asyncio
    async def test_add_keyframes_async_normal(self, mock_draft_data):
        """测试 add_keyframes_async 正常场景"""
        keyframes = json.dumps([
            {
                "segment_id": "segment-uuid-123",
                "property": "KFTypePositionX",
                "offset": 0.5,
                "value": -0.1
            }
        ])
        
        with patch('src.service.add_keyframes.DRAFT_CACHE') as mock_cache, \
             patch('src.service.add_keyframes.helper.get_url_param', return_value=mock_draft_data['draft_id']):
            
            # 模拟草稿对象
            mock_script = MagicMock()
            mock_script.save.return_value = None
            mock_cache.__getitem__.return_value = mock_script
            
            # 模拟片段
            mock_segment = MagicMock()
            mock_segment.segment_id = "segment-uuid-123"
            mock_segment.duration = 5000000
            mock_script.find_segment_by_id.return_value = mock_segment
            
            # 执行测试
            result = await add_keyframes_async(
                draft_url=mock_draft_data['draft_url'],
                keyframes=keyframes
            )
            
            # 验证结果
            assert len(result) == 3
            assert result[0] == mock_draft_data['draft_url']
    
    @pytest.mark.asyncio
    async def test_add_sticker_async_normal(self, mock_draft_data):
        """测试 add_sticker_async 正常场景"""
        with patch('src.service.add_sticker.DRAFT_CACHE') as mock_cache, \
             patch('src.service.add_sticker.helper.get_url_param', return_value=mock_draft_data['draft_id']):
            
            # 模拟草稿对象
            mock_script = MagicMock()
            mock_script.save.return_value = None
            mock_script.tracks = {'track1': MagicMock(track_id='track-id-123', name='sticker_track')}
            mock_script.width = 1920
            mock_script.height = 1080
            mock_cache.__getitem__.return_value = mock_script
            
            # 执行测试
            result = await add_sticker_async(
                draft_url=mock_draft_data['draft_url'],
                sticker_id="sticker-uuid-123",
                start=0,
                end=5000000
            )
            
            # 验证结果
            assert len(result) == 5
            assert result[0] == mock_draft_data['draft_url']
    
    @pytest.mark.asyncio
    async def test_add_filters_async_normal(self, mock_draft_data):
        """测试 add_filters_async 正常场景"""
        filter_infos = json.dumps([
            {
                "filter_title": "复古",
                "start": 0,
                "end": 5000000
            }
        ])
        
        with patch('src.service.add_filters.DRAFT_CACHE') as mock_cache, \
             patch('src.service.add_filters.helper.get_url_param', return_value=mock_draft_data['draft_id']):
            
            # 模拟草稿对象
            mock_script = MagicMock()
            mock_script.save.return_value = None
            mock_script.tracks = {'track1': MagicMock(track_id='track-id-123', name='filter_track')}
            mock_cache.__getitem__.return_value = mock_script
            
            # 执行测试
            result = await add_filters_async(
                draft_url=mock_draft_data['draft_url'],
                filter_infos=filter_infos
            )
            
            # 验证结果
            assert len(result) == 4
            assert result[0] == mock_draft_data['draft_url']
    
    @pytest.mark.asyncio
    async def test_add_masks_async_normal(self, mock_draft_data):
        """测试 add_masks_async 正常场景"""
        segment_ids = ["segment-uuid-123"]
        
        with patch('src.service.add_masks.DRAFT_CACHE') as mock_cache, \
             patch('src.service.add_masks.helper.get_url_param', return_value=mock_draft_data['draft_id']):
            
            # 模拟草稿对象
            mock_script = MagicMock()
            mock_script.save.return_value = None
            mock_cache.__getitem__.return_value = mock_script
            
            # 模拟片段
            mock_segment = MagicMock()
            mock_segment.segment_id = "segment-uuid-123"
            mock_script.find_segment_by_id.return_value = mock_segment
            
            # 执行测试
            result = await add_masks_async(
                draft_url=mock_draft_data['draft_url'],
                segment_ids=segment_ids
            )
            
            # 验证结果
            assert len(result) == 4
            assert result[0] == mock_draft_data['draft_url']
    
    @pytest.mark.asyncio
    async def test_easy_create_material_async_normal(self, mock_draft_data):
        """测试 easy_create_material_async 正常场景"""
        with patch('src.service.easy_create_material.DRAFT_CACHE') as mock_cache, \
             patch('src.service.easy_create_material.helper.get_url_param', return_value=mock_draft_data['draft_id']), \
             patch('src.service.easy_create_material.download') as mock_download, \
             patch('src.service.easy_create_material.os.makedirs'):
            
            # 模拟草稿对象
            mock_script = MagicMock()
            mock_script.save.return_value = None
            mock_script.width = 1920
            mock_script.height = 1080
            mock_cache.__getitem__.return_value = mock_script
            
            # 模拟下载
            mock_download.return_value = '/tmp/audio.mp3'
            
            # 执行测试
            result = await easy_create_material_async(
                draft_url=mock_draft_data['draft_url'],
                audio_url="https://example.com/audio.mp3"
            )
            
            # 验证结果
            assert result == mock_draft_data['draft_url']
    
    @pytest.mark.asyncio
    async def test_concurrent_access_same_draft_serialized(self, mock_draft_data):
        """测试同一草稿的并发访问会被串行化"""
        lock_manager = DraftLockManager()
        execution_log = []
        
        async def worker(worker_id, work_duration=0.1):
            """模拟一个 API 请求"""
            try:
                await lock_manager.acquire_lock(mock_draft_data['draft_id'], timeout=5.0)
                execution_log.append(f"worker_{worker_id}_start")
                await asyncio.sleep(work_duration)  # 模拟写入草稿文件
                execution_log.append(f"worker_{worker_id}_end")
            finally:
                await lock_manager.release_lock(mock_draft_data['draft_id'])
        
        # 启动 3 个并发请求
        tasks = [
            worker(1),
            worker(2),
            worker(3)
        ]
        
        # 等待所有任务完成
        await asyncio.gather(*tasks)
        
        # 验证执行顺序是串行的（不是交错的）
        # 正确的串行执行应该是：worker_1_start, worker_1_end, worker_2_start, worker_2_end...
        assert len(execution_log) == 6
        # 检查每个 worker 的 start 和 end 是连续的
        for i in range(0, len(execution_log), 2):
            assert execution_log[i].endswith('_start')
            assert execution_log[i+1].endswith('_end')
            # 确保是同一个 worker
            worker_id = execution_log[i].split('_')[1]
            assert execution_log[i+1].split('_')[1] == worker_id
    
    @pytest.mark.asyncio
    async def test_invalid_draft_id_raises_error(self):
        """测试无效草稿 ID 抛出错误"""
        with patch('src.service.save_draft.helper.get_url_param', return_value=None):
            with pytest.raises(CustomException) as exc_info:
                await save_draft_async(draft_url="http://invalid-url")
            
            assert exc_info.value.err == CustomError.INVALID_DRAFT_URL
    
    @pytest.mark.asyncio
    async def test_lock_timeout_raises_error(self, mock_draft_data):
        """测试锁超时抛出错误"""
        lock_manager = DraftLockManager()
        
        # 先获取锁并不释放
        await lock_manager.acquire_lock(mock_draft_data['draft_id'])
        
        # 尝试再次获取锁，应该超时
        with pytest.raises(CustomException) as exc_info:
            with patch('src.service.save_draft.DRAFT_CACHE') as mock_cache, \
                 patch('src.service.save_draft.helper.get_url_param', return_value=mock_draft_data['draft_id']):
                
                mock_script = MagicMock()
                mock_cache.__getitem__.return_value = mock_script
                
                await save_draft_async(
                    draft_url=mock_draft_data['draft_url'],
                    lock_timeout=0.1  # 很短的超时时间
                )
        
        assert exc_info.value.err == CustomError.DRAFT_LOCK_TIMEOUT
        
        # 清理：释放锁
        await lock_manager.release_lock(mock_draft_data['draft_id'])


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
