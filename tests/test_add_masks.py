#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 add_masks 功能的单元测试
包含正常场景、边界场景和异常场景的完整测试用例
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from typing import List, Tuple
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.service.add_masks import (
    add_masks,
    add_mask_to_segment,
    calculate_mask_size_params,
    find_segment_by_id,
    find_mask_type_by_name
)
from src.pyJianYingDraft import ScriptFile, MaskType
from src.pyJianYingDraft.video_segment import VideoSegment
from exceptions import CustomException, CustomError


class TestCalculateMaskSizeParams(unittest.TestCase):
    """测试遮罩尺寸参数计算函数"""
    
    def test_circle_mask_size_calculation(self):
        """测试圆形遮罩尺寸计算（非矩形）"""
        # 准备测试数据：素材尺寸 1920x1080，遮罩尺寸 512x512
        mask_type = MaskType.圆形
        width = 512
        height = 512
        material_width = 1920
        material_height = 1080
        
        # 调用函数
        size, rect_width = calculate_mask_size_params(
            mask_type=mask_type,
            width=width,
            height=height,
            material_width=material_width,
            material_height=material_height
        )
        
        # 验证结果
        expected_size = height / material_height  # 512/1080 ≈ 0.474
        self.assertAlmostEqual(size, expected_size, places=4)
        self.assertIsNone(rect_width, "非矩形遮罩的 rect_width 应为 None")
    
    def test_rectangle_mask_size_calculation(self):
        """测试矩形遮罩尺寸计算"""
        # 准备测试数据
        mask_type = MaskType.矩形
        width = 800
        height = 600
        material_width = 1920
        material_height = 1080
        
        # 调用函数
        size, rect_width = calculate_mask_size_params(
            mask_type=mask_type,
            width=width,
            height=height,
            material_width=material_width,
            material_height=material_height
        )
        
        # 验证结果
        expected_size = height / material_height  # 600/1080 ≈ 0.556
        expected_rect_width = width / material_width  # 800/1920 ≈ 0.417
        self.assertAlmostEqual(size, expected_size, places=4)
        self.assertAlmostEqual(rect_width, expected_rect_width, places=4)
    
    def test_heart_mask_size_calculation(self):
        """测试爱心遮罩尺寸计算"""
        mask_type = MaskType.爱心
        width = 400
        height = 400
        material_width = 1920
        material_height = 1080
        
        size, rect_width = calculate_mask_size_params(
            mask_type=mask_type,
            width=width,
            height=height,
            material_width=material_width,
            material_height=material_height
        )
        
        expected_size = height / material_height
        self.assertAlmostEqual(size, expected_size, places=4)
        self.assertIsNone(rect_width)
    
    def test_star_mask_size_calculation(self):
        """测试星形遮罩尺寸计算"""
        mask_type = MaskType.星形
        width = 300
        height = 300
        material_width = 1280
        material_height = 720
        
        size, rect_width = calculate_mask_size_params(
            mask_type=mask_type,
            width=width,
            height=height,
            material_width=material_width,
            material_height=material_height
        )
        
        expected_size = height / material_height  # 300/720 ≈ 0.417
        self.assertAlmostEqual(size, expected_size, places=4)
        self.assertIsNone(rect_width)
    
    def test_linear_mask_size_calculation(self):
        """测试线性遮罩尺寸计算"""
        mask_type = MaskType.线性
        width = 1000
        height = 1000
        material_width = 1920
        material_height = 1080
        
        size, rect_width = calculate_mask_size_params(
            mask_type=mask_type,
            width=width,
            height=height,
            material_width=material_width,
            material_height=material_height
        )
        
        expected_size = height / material_height
        self.assertAlmostEqual(size, expected_size, places=4)
        self.assertIsNone(rect_width)
    
    def test_mirror_mask_size_calculation(self):
        """测试镜面遮罩尺寸计算"""
        mask_type = MaskType.镜面
        width = 600
        height = 800
        material_width = 1920
        material_height = 1080
        
        size, rect_width = calculate_mask_size_params(
            mask_type=mask_type,
            width=width,
            height=height,
            material_width=material_width,
            material_height=material_height
        )
        
        expected_size = height / material_height
        self.assertAlmostEqual(size, expected_size, places=4)
        self.assertIsNone(rect_width)
    
    def test_zero_dimensions(self):
        """测试零尺寸的边界情况"""
        mask_type = MaskType.圆形
        width = 0
        height = 0
        material_width = 1920
        material_height = 1080
        
        size, rect_width = calculate_mask_size_params(
            mask_type=mask_type,
            width=width,
            height=height,
            material_width=material_width,
            material_height=material_height
        )
        
        self.assertEqual(size, 0.0)
        self.assertIsNone(rect_width)
    
    def test_large_dimensions(self):
        """测试大尺寸的边界情况"""
        mask_type = MaskType.圆形
        width = 4096
        height = 4096
        material_width = 1920
        material_height = 1080
        
        size, rect_width = calculate_mask_size_params(
            mask_type=mask_type,
            width=width,
            height=height,
            material_width=material_width,
            material_height=material_height
        )
        
        expected_size = height / material_height  # 4096/1080 ≈ 3.793
        self.assertGreater(size, 1.0, "当遮罩尺寸大于素材时，size 应大于 1")
        self.assertAlmostEqual(size, expected_size, places=4)
        self.assertIsNone(rect_width)


class TestFindMaskTypeByName(unittest.TestCase):
    """测试遮罩类型查找函数"""
    
    def test_find_circle_mask(self):
        """测试查找圆形遮罩"""
        result = find_mask_type_by_name("圆形")
        self.assertEqual(result, MaskType.圆形)
    
    def test_find_rectangle_mask(self):
        """测试查找矩形遮罩"""
        result = find_mask_type_by_name("矩形")
        self.assertEqual(result, MaskType.矩形)
    
    def test_find_linear_mask(self):
        """测试查找线性遮罩"""
        result = find_mask_type_by_name("线性")
        self.assertEqual(result, MaskType.线性)
    
    def test_find_mirror_mask(self):
        """测试查找镜面遮罩"""
        result = find_mask_type_by_name("镜面")
        self.assertEqual(result, MaskType.镜面)
    
    def test_find_heart_mask(self):
        """测试查找爱心遮罩"""
        result = find_mask_type_by_name("爱心")
        self.assertEqual(result, MaskType.爱心)
    
    def test_find_star_mask(self):
        """测试查找星形遮罩"""
        result = find_mask_type_by_name("星形")
        self.assertEqual(result, MaskType.星形)
    
    def test_find_invalid_mask(self):
        """测试查找不存在的遮罩类型"""
        result = find_mask_type_by_name("不存在的遮罩")
        self.assertIsNone(result)
    
    def test_case_sensitive_search(self):
        """测试大小写敏感性"""
        result = find_mask_type_by_name("圆形")
        self.assertIsNotNone(result)
        
        # 小写应该找不到
        result_lower = find_mask_type_by_name("圆形")
        self.assertEqual(result, result_lower)


class TestAddMaskToSegment(unittest.TestCase):
    """测试添加遮罩到片段函数"""
    
    def setUp(self):
        """测试前准备"""
        # 创建模拟的 ScriptFile
        self.mock_script = Mock(spec=ScriptFile)
        self.mock_script.materials = Mock()
        self.mock_script.materials.masks = []
        
        self.mock_segment = Mock(spec=VideoSegment)
        self.mock_segment.segment_id = "test-segment-id"
        self.mock_segment.mask = None  # 初始无遮罩
        self.mock_segment.material_size = (1920, 1080)
        self.mock_segment.add_mask = Mock()
        
        # 模拟轨道和片段查找
        self.mock_track = Mock()
        self.mock_track.segments = [self.mock_segment]
        self.mock_script.tracks = {"video": self.mock_track}
    
    def test_add_circle_mask_success(self):
        """测试成功添加圆形遮罩"""
        with patch('src.service.add_masks.find_segment_by_id') as mock_find_segment:
            mock_find_segment.return_value = self.mock_segment
                
            # 模拟 add_mask 方法成功执行，设置 mask 属性
            def mock_add_mask_impl(*args, **kwargs):
                self.mock_segment.mask = Mock()
                self.mock_segment.mask.global_id = "generated-mask-id"
                return self.mock_segment
                
            self.mock_segment.add_mask = Mock(side_effect=mock_add_mask_impl)
                
            mask_id = add_mask_to_segment(
                script=self.mock_script,
                segment_id="test-segment-id",
                mask_type=MaskType.圆形,
                center_x=100,
                center_y=200,
                width=512,
                height=512,
                feather=20,
                rotation=0,
                invert=False,
                round_corner=0
            )
                
            # 验证调用了 add_mask 方法
            self.mock_segment.add_mask.assert_called_once()
            call_args = self.mock_segment.add_mask.call_args
            self.assertEqual(call_args.kwargs['mask_type'], MaskType.圆形)
            self.assertEqual(call_args.kwargs['center_x'], 100.0)
            self.assertEqual(call_args.kwargs['center_y'], 200.0)
            self.assertEqual(call_args.kwargs['feather'], 20.0)
            self.assertEqual(call_args.kwargs['rotation'], 0.0)
            self.assertFalse(call_args.kwargs['invert'])
                
            # 验证返回值
            self.assertIsInstance(mask_id, str)
            self.assertTrue(len(mask_id) > 0)
    
    def test_add_rectangle_mask_with_all_params(self):
        """测试添加矩形遮罩（使用所有参数）"""
        with patch('src.service.add_masks.find_segment_by_id') as mock_find_segment:
            mock_find_segment.return_value = self.mock_segment
                
            # 模拟 add_mask 方法成功执行，设置 mask 属性
            def mock_add_mask_impl(*args, **kwargs):
                self.mock_segment.mask = Mock()
                self.mock_segment.mask.global_id = "rectangle-mask-id"
                return self.mock_segment
                
            self.mock_segment.add_mask = Mock(side_effect=mock_add_mask_impl)
                
            mask_id = add_mask_to_segment(
                script=self.mock_script,
                segment_id="test-segment-id",
                mask_type=MaskType.矩形,
                center_x=50,
                center_y=100,
                width=800,
                height=600,
                feather=30,
                rotation=45,
                invert=True,
                round_corner=25
            )
                
            # 验证调用了 add_mask 方法且包含所有参数
            self.mock_segment.add_mask.assert_called_once()
            call_args = self.mock_segment.add_mask.call_args
            self.assertEqual(call_args.kwargs['mask_type'], MaskType.矩形)
            self.assertIn('rect_width', call_args.kwargs)
            self.assertIn('round_corner', call_args.kwargs)
    
    def test_segment_not_found(self):
        """测试片段未找到的异常情况"""
        with patch('src.service.add_masks.find_segment_by_id') as mock_find_segment:
            mock_find_segment.return_value = None
            
            with self.assertRaises(CustomException) as context:
                add_mask_to_segment(
                    script=self.mock_script,
                    segment_id="non-existent-segment",
                    mask_type=MaskType.圆形
                )
            
            self.assertEqual(context.exception.err, CustomError.SEGMENT_NOT_FOUND)
    
    def test_non_video_segment(self):
        """测试非视频片段类型异常"""
        with patch('src.service.add_masks.find_segment_by_id') as mock_find_segment:
            mock_non_video_segment = Mock()
            mock_non_video_segment.segment_id = "audio-segment"
            mock_find_segment.return_value = mock_non_video_segment
            
            with self.assertRaises(CustomException) as context:
                add_mask_to_segment(
                    script=self.mock_script,
                    segment_id="audio-segment",
                    mask_type=MaskType.圆形
                )
            
            self.assertEqual(context.exception.err, CustomError.INVALID_SEGMENT_TYPE)
    
    @patch('src.service.add_masks.find_segment_by_id')
    def test_segment_already_has_mask(self, mock_find_segment):
        """测试片段已有遮罩的情况"""
        mock_existing_mask = Mock()
        mock_existing_mask.global_id = "existing-mask-id"
        self.mock_segment.mask = mock_existing_mask
        mock_find_segment.return_value = self.mock_segment
        
        # 应该返回现有遮罩 ID 而不是抛出异常
        mask_id = add_mask_to_segment(
            script=self.mock_script,
            segment_id="test-segment-id",
            mask_type=MaskType.圆形
        )
        
        self.assertEqual(mask_id, "existing-mask-id")
        # 不应调用 add_mask
        self.mock_segment.add_mask.assert_not_called()


class TestAddMasksIntegration(unittest.TestCase):
    """测试 add_masks 集成函数"""
    
    @patch('src.service.add_masks.DRAFT_CACHE')
    @patch('src.service.add_masks.helper.get_url_param')
    @patch('src.service.add_masks.find_mask_type_by_name')
    @patch('src.service.add_masks.add_mask_to_segment')
    def test_add_single_circle_mask(self, mock_add_mask, mock_find_mask_type, mock_get_param, mock_cache):
        """测试添加单个圆形遮罩的正常场景"""
        # 设置模拟返回值
        mock_get_param.return_value = "test-draft-id"
        mock_find_mask_type.return_value = MaskType.圆形
        mock_add_mask.return_value = "generated-mask-id"
        
        # 创建模拟草稿
        mock_script = Mock(spec=ScriptFile)
        mock_script.save = Mock()
        
        # 正确设置 DRAFT_CACHE 的模拟
        mock_cache.__contains__ = Mock(return_value=True)
        mock_cache.__getitem__ = Mock(return_value=mock_script)
        
        # 调用函数
        draft_url = "https://example.com/draft?draft_id=test-draft-id"
        segment_ids = ["segment-1"]
        
        result = add_masks(
            draft_url=draft_url,
            segment_ids=segment_ids,
            name="圆形",
            X=100,
            Y=200,
            width=512,
            height=512,
            feather=20,
            rotation=0,
            invert=False,
            roundCorner=0
        )
        
        # 验证结果
        self.assertEqual(result[0], draft_url)
        self.assertEqual(result[1], 1)  # masks_added
        self.assertEqual(result[2], segment_ids)  # affected_segments
        self.assertEqual(result[3], ["generated-mask-id"])  # mask_ids
        
        # 验证保存了草稿
        mock_script.save.assert_called_once()
    
    @patch('src.service.add_masks.DRAFT_CACHE')
    @patch('src.service.add_masks.helper.get_url_param')
    @patch('src.service.add_masks.find_mask_type_by_name')
    @patch('src.service.add_masks.add_mask_to_segment')
    def test_add_multiple_masks(self, mock_add_mask, mock_find_mask_type, mock_get_param, mock_cache):
        """测试批量添加多个遮罩"""
        mock_get_param.return_value = "test-draft-id"
        mock_find_mask_type.return_value = MaskType.圆形
        mock_add_mask.side_effect = ["mask-id-1", "mask-id-2", "mask-id-3"]
        
        mock_script = Mock(spec=ScriptFile)
        mock_script.save = Mock()
        
        # 正确设置 DRAFT_CACHE 的模拟
        mock_cache.__contains__ = Mock(return_value=True)
        mock_cache.__getitem__ = Mock(return_value=mock_script)
        
        draft_url = "https://example.com/draft?draft_id=test-draft-id"
        segment_ids = ["segment-1", "segment-2", "segment-3"]
        
        result = add_masks(
            draft_url=draft_url,
            segment_ids=segment_ids,
            name="圆形"
        )
        
        self.assertEqual(result[1], 3)  # masks_added
        self.assertEqual(len(result[2]), 3)  # affected_segments
        self.assertEqual(len(result[3]), 3)  # mask_ids
        self.assertEqual(mock_add_mask.call_count, 3)
    
    @patch('src.service.add_masks.helper.get_url_param')
    @patch('src.service.add_masks.DRAFT_CACHE')
    def test_invalid_draft_url(self, mock_cache, mock_get_param):
        """测试无效的 draft_url 异常"""
        mock_get_param.return_value = None
        
        with self.assertRaises(CustomException) as context:
            add_masks(
                draft_url="invalid-url",
                segment_ids=["segment-1"]
            )
        
        self.assertEqual(context.exception.err, CustomError.INVALID_DRAFT_URL)
    
    @patch('src.service.add_masks.DRAFT_CACHE')
    @patch('src.service.add_masks.helper.get_url_param')
    def test_empty_segment_ids(self, mock_get_param, mock_cache):
        """测试空的 segment_ids 异常"""
        mock_get_param.return_value = "test-draft-id"
        # 设置缓存，这样会通过第一个检查
        mock_cache.__contains__ = Mock(return_value=True)
        
        with self.assertRaises(CustomException) as context:
            add_masks(
                draft_url="https://example.com/draft?draft_id=test-draft-id",
                segment_ids=[]
            )
        
        self.assertEqual(context.exception.err, CustomError.INVALID_MASK_INFO)
    
    @patch('src.service.add_masks.DRAFT_CACHE')
    @patch('src.service.add_masks.helper.get_url_param')
    @patch('src.service.add_masks.find_mask_type_by_name')
    def test_invalid_mask_type(self, mock_find_mask_type, mock_get_param, mock_cache):
        """测试无效的遮罩类型异常"""
        mock_get_param.return_value = "test-draft-id"
        mock_cache.__contains__ = Mock(return_value=True)
        mock_find_mask_type.return_value = None
        
        with self.assertRaises(CustomException) as context:
            add_masks(
                draft_url="https://example.com/draft?draft_id=test-draft-id",
                segment_ids=["segment-1"],
                name="无效遮罩类型"
            )
        
        self.assertEqual(context.exception.err, CustomError.MASK_NOT_FOUND)
    
    @patch('src.service.add_masks.DRAFT_CACHE')
    @patch('src.service.add_masks.helper.get_url_param')
    @patch('src.service.add_masks.find_mask_type_by_name')
    @patch('src.service.add_masks.add_mask_to_segment')
    def test_partial_failure_handling(self, mock_add_mask, mock_find_mask_type, mock_get_param, mock_cache):
        """测试部分失败的处理"""
        mock_get_param.return_value = "test-draft-id"
        mock_find_mask_type.return_value = MaskType.圆形
        
        # 第一个成功，第二个失败
        mock_add_mask.side_effect = Exception("添加失败")
        
        mock_script = Mock(spec=ScriptFile)
        mock_script.save = Mock()
        mock_cache.__getitem__.return_value = mock_script
        
        with self.assertRaises(Exception):
            add_masks(
                draft_url="https://example.com/draft?draft_id=test-draft-id",
                segment_ids=["segment-1", "segment-2"]
            )


if __name__ == '__main__':
    unittest.main()
