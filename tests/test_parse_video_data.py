import json

def parse_video_data(json_str: str) -> list:
    """
    解析视频数据的JSON字符串，处理可选字段的默认值
    这是add_videos.py中parse_video_data函数的简化版本，用于测试
    """
    try:
        # 解析JSON字符串
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise Exception(f"JSON parse error: {e.msg}")
    
    # 确保输入是列表
    if not isinstance(data, list):
        raise Exception("video_infos should be a list")
    
    result = []
    
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise Exception(f"the {i}th item should be a dict")
        
        # 检查必选字段
        required_fields = ["video_url", "width", "height", "start", "end"]
        missing_fields = [field for field in required_fields if field not in item]
        
        if missing_fields:
            raise Exception(f"the {i}th item is missing required fields: {', '.join(missing_fields)}")
        
        # 如果没有提供duration，则计算为end-start
        duration = item.get("duration", item["end"] - item["start"])
        
        # 创建处理后的对象，设置默认值
        processed_item = {
            "video_url": item["video_url"],
            "width": item["width"],
            "height": item["height"],
            "start": item["start"],
            "end": item["end"],
            "duration": duration,
            "mask": item.get("mask", None),  # 默认值 None
            "transition": item.get("transition", None),  # 默认值 None
            "transition_duration": item.get("transition_duration", 500000),  # 默认值 500000
            "volume": item.get("volume", 1.0)  # 默认值 1.0
        }
        
        # 验证数值范围
        if processed_item["volume"] < 0 or processed_item["volume"] > 1:
            # 音量值必须在[0, 1]范围内，给默认值
            processed_item["volume"] = 1.0
        
        if processed_item["transition_duration"] < 0:
            # 转场持续时间必须为非负数，给默认值
            processed_item["transition_duration"] = 500000
        
        result.append(processed_item)
    
    return result

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