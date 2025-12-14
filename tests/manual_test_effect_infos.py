import json


def effect_infos(
    effects: list,
    timelines: list
) -> str:
    """
    根据特效名称和时间线生成特效信息JSON字符串
    """
    # 检查参数长度是否匹配
    if len(effects) != len(timelines):
        raise ValueError(f"effects length ({len(effects)}) does not match timelines length ({len(timelines)})")
    
    # 构建特效信息列表
    infos = []
    for i, (effect, timeline) in enumerate(zip(effects, timelines)):
        info = {
            "effect_title": effect,
            "start": timeline["start"],
            "end": timeline["end"]
        }
        
        infos.append(info)
    
    # 转换为JSON字符串
    infos_json = json.dumps(infos, ensure_ascii=False)
    
    return infos_json


def test_effect_infos():
    """测试特效信息生成功能"""
    # 测试基本功能
    print("测试基本功能:")
    effects = [
        "红包来了",
        "雪花"
    ]
    
    timelines = [
        {"start": 0, "end": 284891428},
        {"start": 284891428, "end": 579578774}
    ]
    
    infos_json = effect_infos(effects, timelines)
    print(f"Infos JSON: {infos_json}")
    
    # 解析JSON验证内容
    infos = json.loads(infos_json)
    print(f"Parsed infos: {infos}")
    
    # 验证内容
    assert len(infos) == 2
    assert infos[0]["effect_title"] == "红包来了"
    assert infos[0]["start"] == 0
    assert infos[0]["end"] == 284891428
    
    assert infos[1]["effect_title"] == "雪花"
    assert infos[1]["start"] == 284891428
    assert infos[1]["end"] == 579578774
    
    print("基本功能测试通过")
    
    print("\n所有测试通过!")


if __name__ == "__main__":
    test_effect_infos()