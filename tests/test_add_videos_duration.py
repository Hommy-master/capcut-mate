import requests
import json
import time

def test_add_videos_with_duration():
    """测试带duration参数的视频添加接口"""
    
    # 1. 先创建一个草稿
    create_draft_url = "http://localhost:8000/v1/create_draft"
    create_draft_data = {
        "width": 1920,
        "height": 1080
    }
    
    try:
        print("Creating draft...")
        create_response = requests.post(create_draft_url, json=create_draft_data)
        
        if create_response.status_code != 200:
            print(f"Failed to create draft: {create_response.status_code}")
            print(create_response.text)
            return
            
        draft_url = create_response.json()["draft_url"]
        print(f"Draft created successfully: {draft_url}")
        
        # 2. 添加视频 - 测试指定duration的情况
        add_videos_url = "http://localhost:8000/v1/add_videos"
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
        
        add_videos_data = {
            "draft_url": draft_url,
            "video_infos": json.dumps(video_infos),
            "alpha": 1.0,
            "scale_x": 1.0,
            "scale_y": 1.0,
            "transform_x": 0,
            "transform_y": 0
        }
        
        print("Adding videos...")
        add_response = requests.post(add_videos_url, json=add_videos_data)
        
        if add_response.status_code == 200:
            result = add_response.json()
            print(f"Videos added successfully!")
            print(f"Track ID: {result['track_id']}")
            print(f"Video IDs: {result['video_ids']}")
            print(f"Segment IDs: {result['segment_ids']}")
            print(f"Draft URL: {result['draft_url']}")
        else:
            print(f"Failed to add videos: {add_response.status_code}")
            print(add_response.text)
            
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Make sure the server is running on http://localhost:8000")

if __name__ == "__main__":
    test_add_videos_with_duration()