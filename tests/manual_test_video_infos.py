import json


def video_infos(
    video_urls: list,
    timelines: list,
    height: int = None,
    width: int = None,
    mask: str = None,
    transition: str = None,
    transition_duration: int = None,
    volume: float = 1.0
) -> str:
    """
    根据视频URL和时间线生成视频信息JSON字符串
    """
    # 检查参数长度是否匹配
    if len(video_urls) != len(timelines):
        raise ValueError(f"video_urls length ({len(video_urls)}) does not match timelines length ({len(timelines)})")
    
    # 构建视频信息列表
    infos = []
    for i, (video_url, timeline) in enumerate(zip(video_urls, timelines)):
        start = timeline["start"]
        end = timeline["end"]
        duration = end - start
        
        info = {
            "video_url": video_url,
            "start": start,
            "end": end,
            "duration": duration
        }
        
        # 添加可选参数
        if width is not None:
            info["width"] = width
            
        if height is not None:
            info["height"] = height
            
        if mask is not None:
            info["mask"] = mask
            
        if transition is not None:
            info["transition"] = transition
            
        if transition_duration is not None:
            info["transition_duration"] = transition_duration
            
        if volume is not None:
            info["volume"] = volume
            
        infos.append(info)
    
    # 转换为JSON字符串
    infos_json = json.dumps(infos, ensure_ascii=False)
    
    return infos_json


def test_video_infos():
    """测试视频信息生成功能"""
    # 测试基本功能
    print("测试基本功能:")
    
    # 示例输入参数
    video_urls = [
        "https://assets.jcaigc.cn/min.mp4",
        "https://assets.jcaigc.cn/max.mp4"
    ]
    
    timelines = [
        {"end": 284891428, "start": 0},
        {"end": 579578774, "start": 284891428}
    ]
    
    height = 1080
    width = 1920
    mask = "爱心"
    transition = "推近"
    transition_duration = 1
    volume = 1.0
    
    infos_json = video_infos(
        video_urls, timelines, height, width, mask, 
        transition, transition_duration, volume
    )
    print(f"Infos JSON: {infos_json}")
    
    # 解析JSON验证内容
    infos = json.loads(infos_json)
    print(f"Parsed infos: {infos}")
    
    # 验证内容
    assert len(infos) == 2
    assert infos[0]["video_url"] == "https://assets.jcaigc.cn/min.mp4"
    assert infos[0]["start"] == 0
    assert infos[0]["end"] == 284891428
    assert infos[0]["duration"] == 284891428
    assert infos[0]["width"] == 1920
    assert infos[0]["height"] == 1080
    assert infos[0]["mask"] == "爱心"
    assert infos[0]["volume"] == 1.0
    assert infos[0]["transition"] == "推近"
    assert infos[0]["transition_duration"] == 1
    
    assert infos[1]["video_url"] == "https://assets.jcaigc.cn/max.mp4"
    assert infos[1]["start"] == 284891428
    assert infos[1]["end"] == 579578774
    assert infos[1]["duration"] == 294687346  # 579578774 - 284891428
    assert infos[1]["width"] == 1920
    assert infos[1]["height"] == 1080
    assert infos[1]["mask"] == "爱心"
    assert infos[1]["volume"] == 1.0
    assert infos[1]["transition"] == "推近"
    assert infos[1]["transition_duration"] == 1
    
    print("基本功能测试通过")
    
    # 测试可选参数为None的情况
    print("\n测试可选参数为None的情况:")
    infos_json_no_optional = video_infos(video_urls, timelines)
    infos_no_optional = json.loads(infos_json_no_optional)
    print(f"Infos without optional params: {infos_no_optional}")
    
    # 验证可选参数不存在
    optional_params = [
        "width", "height", "mask", "transition", 
        "transition_duration", "volume"
    ]
    
    for param in optional_params:
        # volume有默认值1.0，所以会存在
        if param != "volume":
            assert param not in infos_no_optional[0]
            assert param not in infos_no_optional[1]
        else:
            # volume有默认值1.0
            assert infos_no_optional[0]["volume"] == 1.0
            assert infos_no_optional[1]["volume"] == 1.0
    
    print("可选参数测试通过")
    
    print("\n所有测试通过!")


if __name__ == "__main__":
    test_video_infos()