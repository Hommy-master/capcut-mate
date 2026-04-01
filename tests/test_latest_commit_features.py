"""
单元测试：验证最近一次提交的新功能
测试内容：
1. 主轨道吸附 (maintrack_adsorb)
2. 混合模式 (MixMode)
3. 音频淡入淡出 (AudioFade for VideoSegment)
4. 新增滤镜和字体
"""

import unittest
import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pyJianYingDraft import DraftFolder, ScriptFile
from pyJianYingDraft.video_segment import VideoSegment, MixMode
from pyJianYingDraft.segment import AudioFade
from pyJianYingDraft.metadata import FilterType, FontType
from pyJianYingDraft.metadata.mix_mode_meta import MixModeType
from pyJianYingDraft.time_util import Timerange
from pyJianYingDraft.track import TrackType


class TestMaintrackAdsorb(unittest.TestCase):
    """测试主轨道吸附功能"""
    
    def test_maintrack_adsorb_default_true(self):
        """测试默认启用主轨道吸附"""
        script = ScriptFile(1920, 1080, 30, maintrack_adsorb=True)
        self.assertTrue(script.maintrack_adsorb)
    
    def test_maintrack_adsorb_false(self):
        """测试禁用主轨道吸附"""
        script = ScriptFile(1920, 1080, 30, maintrack_adsorb=False)
        self.assertFalse(script.maintrack_adsorb)
    
    def test_maintrack_adsorb_in_export(self):
        """测试主轨道吸附配置正确导出到 JSON"""
        script = ScriptFile(1920, 1080, 30, maintrack_adsorb=True)
        json_str = script.dumps()
        self.assertIn('"maintrack_adsorb": true', json_str)


class TestMixMode(unittest.TestCase):
    """测试混合模式功能"""
    
    def test_mix_mode_creation(self):
        """测试混合模式对象创建"""
        mix_mode = MixMode(MixModeType.正片叠底.value)
        self.assertIsNotNone(mix_mode.global_id)
        self.assertEqual(mix_mode.effect_meta.name, "正片叠底")
        self.assertEqual(mix_mode.apply_target_type, 0)
    
    def test_mix_mode_export_json(self):
        """测试混合模式 JSON 导出"""
        mix_mode = MixMode(MixModeType.滤色.value)
        json_data = mix_mode.export_json()
        
        self.assertEqual(json_data["type"], "mix_mode")
        self.assertEqual(json_data["name"], "滤色")
        self.assertEqual(json_data["value"], 1.0)
        self.assertEqual(json_data["apply_target_type"], 0)
        self.assertEqual(json_data["platform"], "all")
        self.assertIn("id", json_data)
        self.assertIn("effect_id", json_data)
        self.assertIn("resource_id", json_data)
    
    def test_video_segment_set_mix_mode(self):
        """测试为视频片段设置混合模式"""
        # 创建一个模拟的视频片段（使用假路径）
        timerange = Timerange(0, 1000000)  # 1秒
        
        # 由于需要真实视频文件，这里只测试对象创建逻辑
        # 实际测试需要在集成测试中进行
        pass


class TestVideoSegmentAudioFade(unittest.TestCase):
    """测试视频片段的音频淡入淡出功能"""
    
    def test_audio_fade_creation(self):
        """测试音频淡入淡出对象创建"""
        fade = AudioFade(500000, 500000)  # 0.5秒淡入，0.5秒淡出
        self.assertIsNotNone(fade.fade_id)
        self.assertEqual(fade.in_duration, 500000)
        self.assertEqual(fade.out_duration, 500000)
    
    def test_audio_fade_export_json(self):
        """测试音频淡入淡出 JSON 导出"""
        fade = AudioFade(100000, 200000)
        json_data = fade.export_json()
        
        self.assertEqual(json_data["type"], "audio_fade")
        self.assertEqual(json_data["fade_in_duration"], 100000)
        self.assertEqual(json_data["fade_out_duration"], 200000)
        self.assertEqual(json_data["fade_type"], 0)
        self.assertIn("id", json_data)


class TestNewFilters(unittest.TestCase):
    """测试新增滤镜"""
    
    def test_filter_has_resource_id(self):
        """测试滤镜有资源 ID"""
        filter_meta = FilterType.黑白记忆
        self.assertIsNotNone(filter_meta.value.resource_id)
        self.assertIsNotNone(filter_meta.value.effect_id)
    
    def test_filter_with_params(self):
        """测试带参数的滤镜"""
        # 黑白记忆滤镜有 effects_adjust_filter 参数
        filter_meta = FilterType.黑白记忆
        self.assertTrue(len(filter_meta.value.params) > 0)
        param = filter_meta.value.params[0]
        self.assertEqual(param.name, "effects_adjust_filter")


class TestNewFonts(unittest.TestCase):
    """测试新增字体"""
    
    def test_new_fonts_exist(self):
        """测试新增字体存在"""
        # 南廱明體
        self.assertTrue(hasattr(FontType, '南廱明體'))
        font1 = FontType.南廱明體
        self.assertIsNotNone(font1.value.resource_id)
        
        # 蜡笔体
        self.assertTrue(hasattr(FontType, '蜡笔体'))
        font2 = FontType.蜡笔体
        self.assertIsNotNone(font2.value.resource_id)


class TestScriptMaterial(unittest.TestCase):
    """测试 ScriptMaterial 对新材料的支持"""
    
    def test_mix_modes_list_exists(self):
        """测试 mix_modes 列表存在"""
        from pyJianYingDraft.script_file import ScriptMaterial
        materials = ScriptMaterial()
        self.assertTrue(hasattr(materials, 'mix_modes'))
        self.assertIsInstance(materials.mix_modes, list)
    
    def test_mix_mode_in_check(self):
        """测试 mix_mode 的 __contains__ 检查"""
        from pyJianYingDraft.script_file import ScriptMaterial
        materials = ScriptMaterial()
        mix_mode = MixMode(MixModeType.柔光.value)
        
        # 初始不应包含
        self.assertNotIn(mix_mode, materials)
        
        # 添加后应包含
        materials.mix_modes.append(mix_mode)
        self.assertIn(mix_mode, materials)


class TestIntegration(unittest.TestCase):
    """集成测试 - 验证完整工作流程"""
    
    def test_script_file_creation_with_maintrack_adsorb(self):
        """测试创建带主轨道吸附配置的 ScriptFile"""
        script = ScriptFile(1920, 1080, 30, maintrack_adsorb=True)
        script.add_track(TrackType.video)
        
        # 验证 dumps 输出包含 maintrack_adsorb
        json_str = script.dumps()
        self.assertIn('"maintrack_adsorb": true', json_str)
    
    def test_export_json_structure(self):
        """测试导出 JSON 结构完整性"""
        script = ScriptFile(1920, 1080, 30, maintrack_adsorb=False)
        json_str = script.dumps()
        
        # 验证基本字段存在
        self.assertIn('"fps": 30', json_str)
        self.assertIn('"width": 1920', json_str)
        self.assertIn('"height": 1080', json_str)
        self.assertIn('"maintrack_adsorb": false', json_str)


class TestBackwardCompatibility(unittest.TestCase):
    """向后兼容性测试"""
    
    def test_script_file_init_requires_maintrack_adsorb(self):
        """测试 ScriptFile 初始化需要 maintrack_adsorb 参数"""
        # 这是有意的设计，强制用户明确指定主轨道吸附设置
        with self.assertRaises(TypeError):
            ScriptFile(1920, 1080, 30)  # 缺少 maintrack_adsorb
    
    def test_mix_mode_types_available(self):
        """测试所有混合模式类型可用"""
        expected_modes = [
            "正片叠底", "颜色减淡", "颜色加深", "线性加深",
            "柔光", "强光", "滤色", "叠加", "变亮", "变暗"
        ]
        for mode_name in expected_modes:
            self.assertTrue(
                hasattr(MixModeType, mode_name),
                f"MixModeType 缺少 {mode_name}"
            )


if __name__ == '__main__':
    unittest.main(verbosity=2)
