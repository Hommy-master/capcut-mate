import json

def audio_infos(
    mp3_urls: list,
    timelines: list,
    audio_effect: str = None,
    volume: float = None
) -> str:
    """
    根据音频URL和时间线生成音频信息JSON字符串
    """
    # 检查参数长度是否匹配
    if len(mp3_urls) != len(timelines):
        raise ValueError(f"mp3_urls length ({len(mp3_urls)}) does not match timelines length ({len(timelines)})")
    
    # 构建音频信息列表
    infos = []
    for i, (audio_url, timeline) in enumerate(zip(mp3_urls, timelines)):
        info = {
            "audio_url": audio_url,
            "start": timeline["start"],
            "end": timeline["end"]
        }
        
        # 添加可选参数
        if audio_effect is not None:
            info["audio_effect"] = audio_effect
            
        if volume is not None:
            info["volume"] = volume
            
        infos.append(info)
    
    # 转换为JSON字符串
    infos_json = json.dumps(infos, ensure_ascii=False)
    
    return infos_json


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
    
    print("\n所有测试通过!")


if __name__ == "__main__":
    test_audio_infos()