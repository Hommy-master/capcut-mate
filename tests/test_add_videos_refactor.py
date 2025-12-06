import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.service.add_videos import parse_video_data
import json

def test_parse_video_data_with_duration():
    """测试解析带duration参数的视频数据"""
    
    # 测试数据：指定duration与实际播放时长不同
    video_infos = [
        {
            "video_url": "https://example.com/video1.mp4",
            "width": 1920,
            "height": 1080,
            "start": 0,
            "end": 3000000,  # 3秒
            "duration": 6000000,  # 指定6秒，比实际播放时长长
            "volume": 0.8
        },
        {
            "video_url": "https://example.com/video2.mp4",
            "width": 1280,
            "height": 720,
            "start": 3000000,  # 从第3秒开始
            "end": 5000000,    # 到第5秒结束
            "duration": 1000000,  # 指定1秒，比实际播放时长短
            "volume": 1.0
        },
        # 测试不提供duration字段的情况
        {
            "video_url": "https://example.com/video3.mp4",
            "width": 1920,
            "height": 1080,
            "start": 5000000,  # 从第5秒开始
            "end": 8000000,    # 到第8秒结束
            "volume": 0.5
        }
    ]
    
    json_str = json.dumps(video_infos)
    parsed_videos = parse_video_data(json_str)
    
    print("Parsed video data:")
    for i, video in enumerate(parsed_videos):
        print(f"Video {i+1}:")
        print(f"  URL: {video['video_url']}")
        print(f"  Width: {video['width']}")
        print(f"  Height: {video['height']}")
        print(f"  Start: {video['start']}")
        print(f"  End: {video['end']}")
        print(f"  Duration: {video['duration']}")
        print(f"  Play Duration (end-start): {video['end'] - video['start']}")
        print(f"  Volume: {video['volume']}")
        print()
    
    # 验证第一个视频：指定duration为6秒，播放时长为3秒
    assert parsed_videos[0]['duration'] == 6000000
    assert parsed_videos[0]['end'] - parsed_videos[0]['start'] == 3000000
    
    # 验证第二个视频：指定duration为1秒，播放时长为2秒
    assert parsed_videos[1]['duration'] == 1000000
    assert parsed_videos[1]['end'] - parsed_videos[1]['start'] == 2000000
    
    # 验证第三个视频：未指定duration，应该等于end-start
    assert parsed_videos[2]['duration'] == 3000000
    assert parsed_videos[2]['end'] - parsed_videos[2]['start'] == 3000000
    
    print("All tests passed!")

if __name__ == "__main__":
    test_parse_video_data_with_duration()