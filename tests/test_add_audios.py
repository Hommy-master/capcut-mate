import requests
import json
import time

def test_add_audios():
    """测试音频添加接口"""
    
    # 1. 先创建一个草稿
    create_draft_url = "http://localhost:30000/openapi/capcut-mate/v1/create_draft"
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
        add_audios_url = "http://localhost:30000/openapi/capcut-mate/v1/add_audios"
        audio_infos = [
            {
                "audio_url": "https://assets.jcaigc.cn/test1.mp3",
                "duration": 10000000,  # 10秒 (微秒)
                "start": 0,
                "end": 5000000,  # 前5秒
                "volume": 0.8,
                "audio_effect": "教堂"
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
        print("确保服务器正在运行 http://localhost:30000")


if __name__ == "__main__":
    test_add_audios()