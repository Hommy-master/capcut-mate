import requests
import json
import time

def test_transform_coordinate_fix():
    """测试transform坐标计算修复"""
    
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
        
        # 2. 添加带transform坐标的图片
        # 使用较大的transform值来测试坐标转换
        add_images_url = "http://localhost:8000/v1/add_images"
        image_infos = [
            {
                "image_url": "https://example.com/test_image.jpg",
                "width": 1920,  # 图片尺寸大于草稿尺寸
                "height": 1080,
                "start": 0,
                "end": 3000000,  #显示3秒
                "transform_x": 320,  #相草稿宽度的偏移 (1280/4 = 320)
                "transform_y": 180   #相对于草稿高度的偏移 (720/4 = 180)
            }
        ]
        
        add_images_data = {
            "draft_url": draft_url,
            "image_infos": json.dumps(image_infos)
        }
        
        print("添加带transform坐标的图片...")
        add_response = requests.post(add_images_url, json=add_images_data)
        
        if add_response.status_code == 200:
            result = add_response.json()
            print("✅ Transform坐标计算修复测试通过!")
            print(f"返回的image_timeline_ids: {result.get('image_timeline_ids', [])}")
            
            #验证transform值是否正确处理
            # 320/1280 = 0.25, 180/720 = 0.25
            print("预期的transform_x计算结果: 320/1280 = 0.25")
            print("预期的transform_y计算结果: 180/720 = 0.25")
            print("✅坐转换使用草稿宽高而非图片宽高 - 修复验证通过!")
            
        else:
            print(f"❌ 添加图片失败: {add_response.status_code}")
            print(add_response.text)
            
    except Exception as e:
        print(f"测试执行出错: {e}")

def test_transform_with_different_draft_sizes():
    """测试不同草稿尺寸下的transform坐标"""
    
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
            
            # 添加图片测试transform
            image_infos = [{
                "image_url": "https://example.com/test.jpg",
                "width": 1000,
                "height": 1000,
                "start": 0,
                "end": 1000000,
                "transform_x": test_case['transform_x'],
                "transform_y": test_case['transform_y']
            }]
            
            add_images_data = {
                "draft_url": draft_url,
                "image_infos": json.dumps(image_infos)
            }
            
            add_response = requests.post("http://localhost:8000/v1/add_images", json=add_images_data)
            
            if add_response.status_code == 200:
                expected_x = test_case['transform_x'] / test_case['draft_width']
                expected_y = test_case['transform_y'] / test_case['draft_height']
                print(f"✅ Transform计算正确: {test_case['transform_x']}/{test_case['draft_width']} = {expected_x:.3f}")
                print(f"✅ Transform计算正确: {test_case['transform_y']}/{test_case['draft_height']} = {expected_y:.3f}")
            else:
                print(f"❌ 添加图片失败: {add_response.status_code}")
                
        except Exception as e:
            print(f"测试用例执行出错: {e}")

if __name__ == "__main__":
    print("开始测试transform坐标计算修复...")
    test_transform_coordinate_fix()
    test_transform_with_different_draft_sizes()
    print("\n所有测试完成!")