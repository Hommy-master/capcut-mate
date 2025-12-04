import requests
import json
import time

def test_add_audios():
    """测试音频添加接口"""
    
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
        
        # 2. 添加音频
        add_audios_url = "http://localhost:8000/v1/add_audios"
        audio_infos = [
            {
                "audio_url": "https://example.com/audio1.mp3",
                "duration": 10000000,  # 10秒 (微秒)
                "start": 0,
                "end": 5000000,  # 前5秒
                "volume": 0.8,
                "audio_effect": "reverb"
            },
            {
                "audio_url": "https://example.com/audio2.mp3",
                "duration": 15000000,  # 15秒 (微秒)
                "start": 5000000,  # 从第5秒开始
                "end": 10000000,   # 到第10秒结束
                "volume": 1.0
            },
            # 测试不提供duration字段的情况
            {
                "audio_url": "https://example.com/audio3.mp3",
                "start": 10000000,  # 从第10秒开始
                "end": 15000000,    # 到第15秒结束
                "volume": 0.5
            }
        ]
        
        add_audios_data = {
            "draft_url": draft_url,
            "audio_infos": json.dumps(audio_infos)
        }
        
        print("Adding audios...")
        add_response = requests.post(add_audios_url, json=add_audios_data)
        
        if add_response.status_code == 200:
            result = add_response.json()
            print(f"Audios added successfully!")
            print(f"Track ID: {result['track_id']}")
            print(f"Audio IDs: {result['audio_ids']}")
            print(f"Draft URL: {result['draft_url']}")
        else:
            print(f"Failed to add audios: {add_response.status_code}")
            print(add_response.text)
            
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Make sure the server is running on http://localhost:8000")


if __name__ == "__main__":
    test_add_audios()