import json

def imgs_infos(
    imgs: list,
    timelines: list,
    height: int = None,
    width: int = None,
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
    根据图片URL和时间线生成图片信息JSON字符串
    """
    # 检查参数长度是否匹配
    if len(imgs) != len(timelines):
        raise ValueError(f"imgs length ({len(imgs)}) does not match timelines length ({len(timelines)})")
    
    # 构建图片信息列表
    infos = []
    for i, (img_url, timeline) in enumerate(zip(imgs, timelines)):
        info = {
            "image_url": img_url,
            "start": timeline["start"],
            "end": timeline["end"]
        }
        
        # 添加可选参数
        if height is not None:
            info["height"] = height
            
        if width is not None:
            info["width"] = width
            
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


def test_imgs_infos():
    """测试图片信息生成功能"""
    # 测试基本功能
    print("测试基本功能:")
    imgs = [
        "https://assets.jcaigc.cn/demo.png",
        "https://assets.jcaigc.cn/demo1.png"
    ]
    
    timelines = [
        {"start": 0, "end": 284891428},
        {"start": 284891428, "end": 579578774}
    ]
    
    height = 1080
    width = 1920
    in_animation = "展开"
    in_animation_duration = 1
    loop_animation = "分身"
    loop_animation_duration = 2
    out_animation = "闪现"
    out_animation_duration = 3
    transition = "推近"
    transition_duration = 1
    
    infos_json = imgs_infos(
        imgs, timelines, height, width, in_animation, in_animation_duration,
        loop_animation, loop_animation_duration, out_animation, out_animation_duration,
        transition, transition_duration
    )
    print(f"Infos JSON: {infos_json}")
    
    # 解析JSON验证内容
    infos = json.loads(infos_json)
    print(f"Parsed infos: {infos}")
    
    # 验证内容
    assert len(infos) == 2
    assert infos[0]["image_url"] == "https://assets.jcaigc.cn/demo.png"
    assert infos[0]["start"] == 0
    assert infos[0]["end"] == 284891428
    assert infos[0]["height"] == 1080
    assert infos[0]["width"] == 1920
    assert infos[0]["in_animation"] == "展开"
    assert infos[0]["in_animation_duration"] == 1
    assert infos[0]["loop_animation"] == "分身"
    assert infos[0]["loop_animation_duration"] == 2
    assert infos[0]["out_animation"] == "闪现"
    assert infos[0]["out_animation_duration"] == 3
    assert infos[0]["transition"] == "推近"
    assert infos[0]["transition_duration"] == 1
    
    assert infos[1]["image_url"] == "https://assets.jcaigc.cn/demo1.png"
    assert infos[1]["start"] == 284891428
    assert infos[1]["end"] == 579578774
    assert infos[1]["height"] == 1080
    assert infos[1]["width"] == 1920
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
    infos_json_no_optional = imgs_infos(imgs, timelines)
    infos_no_optional = json.loads(infos_json_no_optional)
    print(f"Infos without optional params: {infos_no_optional}")
    
    # 验证可选参数不存在
    optional_params = [
        "height", "width", "in_animation", "in_animation_duration",
        "loop_animation", "loop_animation_duration", "out_animation",
        "out_animation_duration", "transition", "transition_duration"
    ]
    
    for param in optional_params:
        assert param not in infos_no_optional[0]
        assert param not in infos_no_optional[1]
    
    print("可选参数测试通过")
    
    print("\n所有测试通过!")


if __name__ == "__main__":
    test_imgs_infos()