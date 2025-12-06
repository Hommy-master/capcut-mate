import sys
import os
import json
import requests

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_video_transform():
    """测试视频位置变换功能"""
    
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
        
        # 2. 添加带位置变换的视频
        add_videos_url = "http://localhost:8000/v1/add_videos"
        video_infos = [
            {
                "video_url": "https://example.com/test.mp4",
                "width": 1920,
                "height": 1080,
                "start": 0,
                "end": 5000000,  # 5秒
                "duration": 5000000
            }
        ]
        
        add_videos_data = {
            "draft_url": draft_url,
            "video_infos": json.dumps(video_infos),
            "transform_x": 100,  # X轴位置偏移100像素
            "transform_y": -50   # Y轴位置偏移-50像素
        }
        
        print("Adding videos with position transformation...")
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
    test_video_transform()