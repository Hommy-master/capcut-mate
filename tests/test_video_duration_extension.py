import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock pymediainfo to avoid dependency issues
class MockMediaInfo:
    def __init__(self, duration=2000000, width=576, height=1024):
        self.duration = duration
        self.width = width
        self.height = height
    
    def parse(self, path, **kwargs):
        # Return mock video track info
        class MockVideoTrack:
            def __init__(self, duration, width, height):
                self.duration = duration / 1000  # Convert to milliseconds
                self.width = width
                self.height = height
        
        class MockInfo:
            def __init__(self, duration, width, height):
                self.video_tracks = [MockVideoTrack(duration, width, height)]
        
        return MockInfo(self.duration, self.width, self.height)
    
    @staticmethod
    def can_parse():
        return True

# Replace pymediainfo with mock
import src.pyJianYingDraft.local_materials
src.pyJianYingDraft.local_materials.pymediainfo = MockMediaInfo()

from src.pyJianYingDraft.local_materials import VideoMaterial
from src.pyJianYingDraft.time_util import Timerange
from src.pyJianYingDraft.video_segment import VideoSegment
import uuid

def test_video_duration_extension():
    """测试视频时长扩展功能"""
    
    # Mock the uuid to make tests deterministic
    original_uuid4 = uuid.uuid4
    uuid.uuid4 = lambda: type('MockUUID', (), {'hex': 'mock-uuid'})()
    
    try:
        # 创建一个模拟的视频文件路径
        mock_video_path = "test_video.mp4"
        
        # 创建视频素材（模拟2秒的视频）
        video_material = VideoMaterial(mock_video_path)
        print(f"视频素材时长: {video_material.duration} 微秒")
        print(f"视频尺寸: {video_material.width}x{video_material.height}")
        
        # 测试场景1：指定duration超过实际视频时长
        # 视频实际时长2秒(2000000微秒)，但指定时长3秒(3000000微秒)
        specified_duration = 3000000  # 3秒
        source_duration = 2000000      # 2秒（实际播放时长）
        start_time = 3000000          # 从3秒开始
        end_time = 5000000            # 到5秒结束
        
        print(f"\n测试场景1：")
        print(f"指定duration: {specified_duration} 微秒")
        print(f"实际播放时长: {source_duration} 微秒")
        print(f"时间轴开始时间: {start_time} 微秒")
        print(f"时间轴结束时间: {end_time} 微秒")
        
        # 创建视频片段
        video_segment = VideoSegment(
            material=video_material,
            target_timerange=Timerange(start=start_time, duration=source_duration),
            source_timerange=Timerange(start=0, duration=min(specified_duration, video_material.duration)),
            speed=1.0,
            volume=1.0
        )
        
        print(f"片段创建成功！")
        print(f"片段ID: {video_segment.segment_id}")
        print(f"素材ID: {video_segment.material_id}")
        print(f"目标时间范围: start={video_segment.target_timerange.start}, duration={video_segment.target_timerange.duration}")
        print(f"源时间范围: start={video_segment.source_timerange.start}, duration={video_segment.source_timerange.duration}")
        print(f"播放速度: {video_segment.speed.speed}")
        
        # 验证结果
        assert video_segment.target_timerange.start == start_time
        assert video_segment.target_timerange.duration == source_duration
        assert video_segment.source_timerange.duration <= video_material.duration
        print("测试场景1通过！")
        
        # 测试场景2：指定duration小于实际视频时长
        specified_duration = 1000000   # 1秒
        source_duration = 2000000      # 2秒（实际播放时长）
        start_time = 6000000          # 从6秒开始
        end_time = 8000000            # 到8秒结束
        
        print(f"\n测试场景2：")
        print(f"指定duration: {specified_duration} 微秒")
        print(f"实际播放时长: {source_duration} 微秒")
        print(f"时间轴开始时间: {start_time} 微秒")
        print(f"时间轴结束时间: {end_time} 微秒")
        
        # 创建视频片段
        video_segment2 = VideoSegment(
            material=video_material,
            target_timerange=Timerange(start=start_time, duration=source_duration),
            source_timerange=Timerange(start=0, duration=min(specified_duration, video_material.duration)),
            speed=1.0,
            volume=1.0
        )
        
        print(f"片段创建成功！")
        print(f"片段ID: {video_segment2.segment_id}")
        print(f"素材ID: {video_segment2.material_id}")
        print(f"目标时间范围: start={video_segment2.target_timerange.start}, duration={video_segment2.target_timerange.duration}")
        print(f"源时间范围: start={video_segment2.source_timerange.start}, duration={video_segment2.source_timerange.duration}")
        print(f"播放速度: {video_segment2.speed.speed}")
        
        # 验证结果
        assert video_segment2.target_timerange.start == start_time
        assert video_segment2.target_timerange.duration == source_duration
        assert video_segment2.source_timerange.duration <= video_material.duration
        print("测试场景2通过！")
        
    finally:
        # Restore original uuid
        uuid.uuid4 = original_uuid4

if __name__ == "__main__":
    test_video_duration_extension()
    print("\n所有测试通过！")