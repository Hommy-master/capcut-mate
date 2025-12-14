import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.service.audio_infos import audio_infos


def test_audio_infos():
    """测试音频信息生成功能"""
    # 测试基本功能
    print("测试基本功能:")
    mp3_urls = [
        "https://assets.jcaigc.cn/test1.mp3",
        "https://assets.jcaigc.cn/test2.mp3"
    ]
    
    timelines = [
        {"start": 0, "end": 284891428},
        {"start": 284891428, "end": 579578774}
    ]
    
    audio_effect = "教堂"
    volume = 1.0
    
    infos_json = audio_infos(mp3_urls, timelines, audio_effect, volume)
    print(f"Infos JSON: {infos_json}")
    
    # 解析JSON验证内容
    infos = json.loads(infos_json)
    print(f"Parsed infos: {infos}")
    
    # 验证内容
    assert len(infos) == 2
    assert infos[0]["audio_url"] == "https://assets.jcaigc.cn/test1.mp3"
    assert infos[0]["start"] == 0
    assert infos[0]["end"] == 284891428
    assert infos[0]["audio_effect"] == "教堂"
    assert infos[0]["volume"] == 1.0
    
    assert infos[1]["audio_url"] == "https://assets.jcaigc.cn/test2.mp3"
    assert infos[1]["start"] == 284891428
    assert infos[1]["end"] == 579578774
    assert infos[1]["audio_effect"] == "教堂"
    assert infos[1]["volume"] == 1.0
    
    print("基本功能测试通过")
    
    # 测试可选参数为None的情况
    print("\n测试可选参数为None的情况:")
    infos_json_no_optional = audio_infos(mp3_urls, timelines)
    infos_no_optional = json.loads(infos_json_no_optional)
    print(f"Infos without optional params: {infos_no_optional}")
    
    # 验证可选参数不存在
    assert "audio_effect" not in infos_no_optional[0]
    assert "volume" not in infos_no_optional[0]
    assert "audio_effect" not in infos_no_optional[1]
    assert "volume" not in infos_no_optional[1]
    
    print("可选参数测试通过")
    
    # 测试长度不匹配的情况
    print("\n测试长度不匹配的情况:")
    try:
        audio_infos(["url1"], timelines, audio_effect, volume)
        assert False, "应该抛出ValueError异常"
    except ValueError as e:
        print(f"正确捕获异常: {e}")
        print("长度不匹配测试通过")


if __name__ == "__main__":
    test_audio_infos()
    print("\n所有测试通过!")