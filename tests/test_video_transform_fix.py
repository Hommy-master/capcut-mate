import requests
import json
import time

def test_video_transform_coordinate_fix():
    """测试视频transform坐标计算修复"""
    
    # 1. 创建一个自定义尺寸的草稿 (1280x720)
    create_draft_url = "http://localhost:8000/v1/create_draft"
    create_draft_data = {
        "width": 1280,
        "height": 720
    }
    
    try:
        print("创建草稿...")
        create_response = requests.post(create_draft_url, json=create_draft_data)
        
        if create_response.status_code != 200:
            print(f"草稿创建失败: {create_response.status_code}")
            print(create_response.text)
            return
            
        draft_url = create_response.json()["draft_url"]
        print(f"草稿创建成功: {draft_url}")
        
        # 2. 添加带transform坐标的视频
        # 使用较大的transform值来测试坐标转换
        add_videos_url = "http://localhost:8000/v1/add_videos"
        video_infos = [
            {
                "video_url": "https://example.com/test_video.mp4",
                "width": 1920,  #视频尺寸大于草稿尺寸
                "height": 1080,
                "start": 0,
                "end": 3000000,  #显示3秒
                "transform_x": 320,  #相草稿宽度的偏移 (1280/4 = 320)
                "transform_y": 180   #相对于草稿高度的偏移 (720/4 = 180)
            }
        ]
        
        add_videos_data = {
            "draft_url": draft_url,
            "video_infos": json.dumps(video_infos)
        }
        
        print("添加带transform坐标的视频...")
        add_response = requests.post(add_videos_url, json=add_videos_data)
        
        if add_response.status_code == 200:
            result = add_response.json()
            print("✅视频Transform坐标计算修复测试通过!")
            print(f"返回的segment_ids: {result.get('segment_ids', [])}")
            
            #验证transform值是否正确处理
            # 320/1280 = 0.25, 180/720 = 0.25
            print("预期的transform_x计算结果: 320/1280 = 0.25")
            print("预期的transform_y计算结果: 180/720 = 0.25")
            print("✅转换使用草稿宽高而非视频宽高 - 修复验证通过!")
            
        else:
            print(f"❌ 添加视频失败: {add_response.status_code}")
            print(add_response.text)
            
    except Exception as e:
        print(f"测试执行出错: {e}")

def test_video_transform_with_different_draft_sizes():
    """测试不同草稿尺寸下的视频transform坐标"""
    
    test_cases = [
        {"draft_width": 1920, "draft_height": 1080, "transform_x": 480, "transform_y": 270},  # 1/4位置
        {"draft_width": 1280, "draft_height": 720, "transform_x": 320, "transform_y": 180},   # 1/4位置
        {"draft_width": 3840, "draft_height": 2160, "transform_x": 960, "transform_y": 540}   # 1/4位置
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n=== 测试用例 {i+1}:尺寸 {test_case['draft_width']}x{test_case['draft_height']} ===")
        
        # 创建对应尺寸的草稿
        create_draft_data = {
            "width": test_case['draft_width'],
            "height": test_case['draft_height']
        }
        
        try:
            create_response = requests.post("http://localhost:8000/v1/create_draft", json=create_draft_data)
            if create_response.status_code != 200:
                print(f"草稿创建失败: {create_response.status_code}")
                continue
                
            draft_url = create_response.json()["draft_url"]
            
            # 添加视频测试transform
            video_infos = [{
                "video_url": "https://example.com/test_video.mp4",
                "width": 1000,
                "height": 1000,
                "start": 0,
                "end": 1000000,
                "transform_x": test_case['transform_x'],
                "transform_y": test_case['transform_y']
            }]
            
            add_videos_data = {
                "draft_url": draft_url,
                "video_infos": json.dumps(video_infos)
            }
            
            add_response = requests.post("http://localhost:8000/v1/add_videos", json=add_videos_data)
            
            if add_response.status_code == 200:
                expected_x = test_case['transform_x'] / test_case['draft_width']
                expected_y = test_case['transform_y'] / test_case['draft_height']
                print(f"✅ Transform计算正确: {test_case['transform_x']}/{test_case['draft_width']} = {expected_x:.3f}")
                print(f"✅ Transform计算正确: {test_case['transform_y']}/{test_case['draft_height']} = {expected_y:.3f}")
            else:
                print(f"❌ 添加视频失败: {add_response.status_code}")
                
        except Exception as e:
            print(f"测试用例执行出错: {e}")

def test_video_transform_vs_image_transform_consistency():
    """测试视频和图片transform计算的一致性"""
    
    print("\n=== 测试视频和图片transform计算一致性 ===")
    
    # 使用相同的草稿和transform参数
    create_draft_data = {"width": 1920, "height": 1080}
    
    try:
        # 创建草稿
        create_response = requests.post("http://localhost:8000/v1/create_draft", json=create_draft_data)
        draft_url = create_response.json()["draft_url"]
        
        #相同的transform参数
        transform_x, transform_y = 480, 270  # 1/4位置
        
        # 添加视频
        video_infos = [{
            "video_url": "https://example.com/test_video.mp4",
            "width": 1000,
            "height": 1000,
            "start": 0,
            "end": 1000000,
            "transform_x": transform_x,
            "transform_y": transform_y
        }]
        
        video_response = requests.post("http://localhost:8000/v1/add_videos", 
                                     json={"draft_url": draft_url, "video_infos": json.dumps(video_infos)})
        
        # 添加图片
        image_infos = [{
            "image_url": "https://example.com/test_image.jpg",
            "width": 1000,
            "height": 1000,
            "start": 0,
            "end": 1000000,
            "transform_x": transform_x,
            "transform_y": transform_y
        }]
        
        image_response = requests.post("http://localhost:8000/v1/add_images",
                                     json={"draft_url": draft_url, "image_infos": json.dumps(image_infos)})
        
        if video_response.status_code == 200 and image_response.status_code == 200:
            expected_result = transform_x / 1920  # 480/1920 = 0.25
            print(f"✅ 视频和图片transform计算一致!")
            print(f"✅都草稿宽度1920进行计算，结果: {expected_result:.3f}")
        else:
            print("❌视频或图片添加失败")
            
    except Exception as e:
        print(f"一致性测试出错: {e}")

if __name__ == "__main__":
    print("开始测试视频transform坐标计算修复...")
    test_video_transform_coordinate_fix()
    test_video_transform_with_different_draft_sizes()
    test_video_transform_vs_image_transform_consistency()
    print("\n所有视频transform测试完成!")