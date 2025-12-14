import json

def caption_infos(
    texts: list,
    timelines: list,
    font_size: int = None,
    keyword_color: str = None,
    keyword_font_size: int = None,
    keywords: list = None,
    in_animation: str = None,
    in_animation_duration: int = None,
    loop_animation: str = None,
    loop_animation_duration: int = None,
    out_animation: str = None,
    out_animation_duration: int = None,
    transition: str = None,
    transition_duration: int = None
) -> str:
    """
    根据文本和时间线生成字幕信息JSON字符串
    """
    # 检查参数长度是否匹配
    if len(texts) != len(timelines):
        raise ValueError(f"texts length ({len(texts)}) does not match timelines length ({len(timelines)})")
    
    # 检查keywords长度是否匹配
    if keywords is not None and len(keywords) != len(texts):
        raise ValueError(f"keywords length ({len(keywords)}) does not match texts length ({len(texts)})")
    
    # 构建字幕信息列表
    infos = []
    for i, (text, timeline) in enumerate(zip(texts, timelines)):
        info = {
            "start": timeline["start"],
            "end": timeline["end"],
            "text": text
        }
        
        # 添加关键词信息
        if keywords is not None:
            info["keyword"] = keywords[i]
            
        # 添加可选参数
        if keyword_color is not None:
            info["keyword_color"] = keyword_color
            
        if keyword_font_size is not None:
            info["keyword_font_size"] = keyword_font_size
            
        if font_size is not None:
            info["font_size"] = font_size
            
        if in_animation is not None:
            info["in_animation"] = in_animation
            
        if in_animation_duration is not None:
            info["in_animation_duration"] = in_animation_duration
            
        if loop_animation is not None:
            info["loop_animation"] = loop_animation
            
        if loop_animation_duration is not None:
            info["loop_animation_duration"] = loop_animation_duration
            
        if out_animation is not None:
            info["out_animation"] = out_animation
            
        if out_animation_duration is not None:
            info["out_animation_duration"] = out_animation_duration
            
        if transition is not None:
            info["transition"] = transition
            
        if transition_duration is not None:
            info["transition_duration"] = transition_duration
            
        infos.append(info)
    
    # 转换为JSON字符串
    infos_json = json.dumps(infos, ensure_ascii=False)
    
    return infos_json


def test_caption_infos():
    """测试字幕信息生成功能"""
    # 测试基本功能
    print("测试基本功能:")
    texts = [
        "床前明月光",
        "明天我发光"
    ]
    
    timelines = [
        {"start": 0, "end": 284891428},
        {"start": 284891428, "end": 579578774}
    ]
    
    font_size = 15
    keyword_color = "#ff0000"
    keyword_font_size = 15
    keywords = ["明月", "明天"]
    in_animation = "展开"
    in_animation_duration = 1
    loop_animation = "分身"
    loop_animation_duration = 2
    out_animation = "闪现"
    out_animation_duration = 3
    transition = "推近"
    transition_duration = 1
    
    infos_json = caption_infos(
        texts, timelines, font_size, keyword_color, keyword_font_size, keywords,
        in_animation, in_animation_duration, loop_animation, loop_animation_duration,
        out_animation, out_animation_duration, transition, transition_duration
    )
    print(f"Infos JSON: {infos_json}")
    
    # 解析JSON验证内容
    infos = json.loads(infos_json)
    print(f"Parsed infos: {infos}")
    
    # 验证内容
    assert len(infos) == 2
    assert infos[0]["start"] == 0
    assert infos[0]["end"] == 284891428
    assert infos[0]["text"] == "床前明月光"
    assert infos[0]["keyword"] == "明月"
    assert infos[0]["keyword_color"] == "#ff0000"
    assert infos[0]["keyword_font_size"] == 15
    assert infos[0]["font_size"] == 15
    assert infos[0]["in_animation"] == "展开"
    assert infos[0]["in_animation_duration"] == 1
    assert infos[0]["loop_animation"] == "分身"
    assert infos[0]["loop_animation_duration"] == 2
    assert infos[0]["out_animation"] == "闪现"
    assert infos[0]["out_animation_duration"] == 3
    assert infos[0]["transition"] == "推近"
    assert infos[0]["transition_duration"] == 1
    
    assert infos[1]["start"] == 284891428
    assert infos[1]["end"] == 579578774
    assert infos[1]["text"] == "明天我发光"
    assert infos[1]["keyword"] == "明天"
    assert infos[1]["keyword_color"] == "#ff0000"
    assert infos[1]["keyword_font_size"] == 15
    assert infos[1]["font_size"] == 15
    assert infos[1]["in_animation"] == "展开"
    assert infos[1]["in_animation_duration"] == 1
    assert infos[1]["loop_animation"] == "分身"
    assert infos[1]["loop_animation_duration"] == 2
    assert infos[1]["out_animation"] == "闪现"
    assert infos[1]["out_animation_duration"] == 3
    assert infos[1]["transition"] == "推近"
    assert infos[1]["transition_duration"] == 1
    
    print("基本功能测试通过")
    
    # 测试可选参数为None的情况
    print("\n测试可选参数为None的情况:")
    infos_json_no_optional = caption_infos(texts, timelines)
    infos_no_optional = json.loads(infos_json_no_optional)
    print(f"Infos without optional params: {infos_no_optional}")
    
    # 验证可选参数不存在
    optional_params = [
        "keyword_color", "keyword_font_size", "font_size", "in_animation", 
        "in_animation_duration", "loop_animation", "loop_animation_duration", 
        "out_animation", "out_animation_duration", "transition", "transition_duration"
    ]
    
    for param in optional_params:
        assert param not in infos_no_optional[0]
        assert param not in infos_no_optional[1]
        
    # 验证没有keyword参数时不会添加keyword字段
    assert "keyword" not in infos_no_optional[0]
    assert "keyword" not in infos_no_optional[1]
    
    print("可选参数测试通过")
    
    print("\n所有测试通过!")


if __name__ == "__main__":
    test_caption_infos()