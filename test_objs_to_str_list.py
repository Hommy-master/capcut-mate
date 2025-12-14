import requests
import json

# 测试 objs_to_str_list 接口
def test_objs_to_str_list():
    url = "http://localhost:30000/openapi/capcut-mate/v1/objs_to_str_list"
    
    # 测试数据
    payload = {
        "outputs": [
            {
                "output": "https://assets.jcaigc.cn/min.mp4"
            },
            {
                "output": "https://assets.jcaigc.cn/max.mp4"
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print("Testing objs_to_str_list API...")
    print(f"Request URL: {url}")
    print(f"Request Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 验证响应
    if response.status_code == 200:
        result = response.json()
        expected_infos = [
            "https://assets.jcaigc.cn/min.mp4",
            "https://assets.jcaigc.cn/max.mp4"
        ]
        
        if result.get("infos") == expected_infos:
            print("\n✅ Test passed! Response matches expected output.")
        else:
            print(f"\n❌ Test failed! Expected {expected_infos}, got {result.get('infos')}")
    else:
        print(f"\n❌ Test failed! HTTP Status Code: {response.status_code}")

if __name__ == "__main__":
    test_objs_to_str_list()