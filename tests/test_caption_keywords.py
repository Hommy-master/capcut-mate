import requests
import json
import time

def test_caption_keywords():
    """测试字幕关键词高亮功能"""
    
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
        
        # 2. 添加带关键词高亮的字幕
        add_captions_url = "http://localhost:8000/v1/add_captions"
        captions = [
            {
                "start": 0,
                "end": 5000000,  # 5秒
                "text": "欢迎使用剪映字幕功能",
                "keyword": "剪映|功能",  # 关键词
                "keyword_color": "#ff0000"  # 红色高亮
            },
            {
                "start": 5000000,
                "end": 10000000,  # 10秒
                "text": "这是一个测试字幕",
                "keyword": "测试",
                "keyword_color": "#00ff00"  # 绿色高亮
            }
        ]
        
        add_captions_data = {
            "draft_url": draft_url,
            "captions": json.dumps(captions),
            "text_color": "#ffffff",  # 默认白色文本
            "font_size": 16
        }
        
        print("Adding captions with keyword highlighting...")
        add_response = requests.post(add_captions_url, json=add_captions_data)
        
        if add_response.status_code == 200:
            result = add_response.json()
            print(f"Captions added successfully!")
            print(f"Track ID: {result['track_id']}")
            print(f"Text IDs: {result['text_ids']}")
            print(f"Segment IDs: {result['segment_ids']}")
            print(f"Draft URL: {result['draft_url']}")
        else:
            print(f"Failed to add captions: {add_response.status_code}")
            print(add_response.text)
            
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Make sure the server is running on http://localhost:8000")


if __name__ == "__main__":
    test_caption_keywords()