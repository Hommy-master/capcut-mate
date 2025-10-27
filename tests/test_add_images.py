import requests
import json
import time

def test_add_images():
    """测试图片添加接口"""
    
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
        
        # 2. 添加图片
        add_images_url = "http://localhost:8000/v1/add_images"
        image_infos = [
            {
                "image_url": "https://example.com/image1.jpg",
                "width": 1024,
                "height": 1024,
                "start": 0,
                "end": 2000000,  # 显示2秒
                "in_animation": "淡入",
                "out_animation": "淡出",
                "in_animation_duration": 500000,  # 0.5秒
                "out_animation_duration": 500000,  # 0.5秒
                "transition": "淡入淡出",
                "transition_duration": 500000  # 0.5秒
            },
            {
                "image_url": "https://example.com/image2.png", 
                "width": 800,
                "height": 600,
                "start": 2000000,  # 从第2秒开始
                "end": 5000000,    # 显示到第5秒
                "loop_animation": "呼吸",
                "loop_animation_duration": 1000000  # 1秒循环
            }
        ]
        
        add_images_data = {
            "draft_url": draft_url,
            "image_infos": json.dumps(image_infos),
            "alpha": 0.9,
            "scale_x": 1.2,
            "scale_y": 1.2,
            "transform_x": 50,
            "transform_y": -30
        }
        
        print("Adding images...")
        add_response = requests.post(add_images_url, json=add_images_data)
        
        if add_response.status_code == 200:
            result = add_response.json()
            print(f"Images added successfully!")
            print(f"Track ID: {result['track_id']}")
            print(f"Image IDs: {result['image_ids']}")
            print(f"Segment IDs: {result['segment_ids']}")
            print(f"Segment Infos:")
            for seg_info in result['segment_infos']:
                print(f"  - ID: {seg_info['id']}, Start: {seg_info['start']}, End: {seg_info['end']}")
            print(f"Draft URL: {result['draft_url']}")
        else:
            print(f"Failed to add images: {add_response.status_code}")
            print(add_response.text)
            
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Make sure the server is running on http://localhost:8000")


if __name__ == "__main__":
    test_add_images()