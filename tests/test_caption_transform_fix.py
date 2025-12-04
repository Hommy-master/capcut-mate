import requests
import json
import time

def test_caption_transform_fix():
    """测试修复后的字幕位置变换功能"""
    
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
        
        # 2. 添加带位置变换的字幕（测试修复后的transform参数）
        add_captions_url = "http://localhost:8000/v1/add_captions"
        captions = [
            {
                "start": 0,
                "end": 5000000,  # 5秒
                "text": "测试字幕位置变换修复"
            }
        ]
        
        add_captions_data = {
            "draft_url": draft_url,
            "captions": json.dumps(captions),
            "text_color": "#ffffff",  # 默认白色文本
            "font_size": 16,
            "transform_x": 200,  # X轴位置偏移200像素
            "transform_y": 100   # Y轴位置偏移100像素
        }
        
        print("Adding captions with fixed position transformation...")
        print(f"Setting transform_x={add_captions_data['transform_x']}, transform_y={add_captions_data['transform_y']}")
        add_response = requests.post(add_captions_url, json=add_captions_data)
        
        if add_response.status_code == 200:
            result = add_response.json()
            print(f"Captions added successfully!")
            print(f"Track ID: {result['track_id']}")
            print(f"Text IDs: {result['text_ids']}")
            print(f"Segment IDs: {result['segment_ids']}")
            print(f"Draft URL: {result['draft_url']}")
            print("\n注意：在剪映中验证时，transform_x=200应该精确移动200像素，而不是之前的400像素")
            print("修复说明：根据ClipSettings类定义，transform参数单位是'半个画布宽/高'，已使用正确的转换公式")
        else:
            print(f"Failed to add captions: {add_response.status_code}")
            print(add_response.text)
            
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Make sure the server is running on http://localhost:8000")


if __name__ == "__main__":
    test_caption_transform_fix()