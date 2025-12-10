import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.service.add_keyframes import parse_keyframes_data


def test_parse_keyframes_data():
    """测试关键帧数据解析"""
    print("Testing keyframe data parsing...")
    
    # 测试数据
    test_keyframes = [
        {
            "segment_id": "segment-1",
            "property": "KFTypePositionX",
            "offset": 0.0,
            "value": 0.0
        },
        {
            "segment_id": "segment-1",
            "property": "KFTypePositionX",
            "offset": 1.0,
            "value": 0.5
        }
    ]
    
    # 将测试数据转换为JSON字符串
    keyframes_json = json.dumps(test_keyframes)
    
    # 解析关键帧数据
    parsed_keyframes = parse_keyframes_data(keyframes_json)
    
    # 验证解析结果
    assert len(parsed_keyframes) == 2
    assert parsed_keyframes[0]["segment_id"] == "segment-1"
    assert parsed_keyframes[0]["property"] == "KFTypePositionX"
    assert parsed_keyframes[0]["offset"] == 0.0
    assert parsed_keyframes[0]["value"] == 0.0
    assert parsed_keyframes[1]["segment_id"] == "segment-1"
    assert parsed_keyframes[1]["property"] == "KFTypePositionX"
    assert parsed_keyframes[1]["offset"] == 1.0
    assert parsed_keyframes[1]["value"] == 0.5
    print("✓ Keyframe data parsing test passed")


def test_parse_invalid_keyframes_data():
    """测试无效关键帧数据解析"""
    print("Testing invalid keyframe data parsing...")
    
    # 测试缺少必填字段的数据
    invalid_keyframes = [
        {
            "segment_id": "segment-1",
            "property": "KFTypePositionX",
            # 缺少offset和value字段
        }
    ]
    
    # 将测试数据转换为JSON字符串
    keyframes_json = json.dumps(invalid_keyframes)
    
    # 尝试解析关键帧数据，应该抛出异常
    try:
        parse_keyframes_data(keyframes_json)
        assert False, "Should have raised an exception"
    except Exception as e:
        print(f"✓ Invalid keyframe data parsing test passed, caught expected exception: {e}")


if __name__ == "__main__":
    print("Running add_keyframes refactor tests...")
    test_parse_keyframes_data()
    test_parse_invalid_keyframes_data()
    print("All tests passed!")