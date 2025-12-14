import json


def keyframes_infos(
    ctype: str,
    offsets: str,
    values: str,
    segment_infos: list,
    height: int = None,
    width: int = None
) -> str:
    """
    根据关键帧类型、位置比例和值生成关键帧信息JSON字符串
    """
    # 解析offsets和values
    offset_list = [int(x) for x in offsets.split("|")]
    value_list = [float(x) for x in values.split("|")]
    
    # 检查offsets和values长度是否匹配
    if len(offset_list) != len(value_list):
        raise ValueError(f"offsets length ({len(offset_list)}) does not match values length ({len(value_list)})")
    
    # 构建关键帧信息列表
    keyframes = []
    
    # 处理每个片段信息
    for segment_info in segment_infos:
        segment_id = segment_info["id"]
        start = segment_info["start"]
        end = segment_info["end"]
        duration = end - start
        
        # 为每个offset创建关键帧
        for offset_percent, value in zip(offset_list, value_list):
            # 计算实际的时间偏移（微秒）
            time_offset = int(start + (offset_percent / 100.0) * duration)
            
            # 根据关键帧类型处理值的归一化
            normalized_value = value
            if ctype == "KFTypePositionX" and width is not None and width > 0:
                normalized_value = value / width
            elif ctype == "KFTypePositionY" and height is not None and height > 0:
                normalized_value = value / height
            
            keyframe = {
                "offset": time_offset,
                "property": ctype,
                "segment_id": segment_id,
                "value": normalized_value
            }
            
            keyframes.append(keyframe)
    
    # 转换为JSON字符串
    keyframes_json = json.dumps(keyframes, ensure_ascii=False)
    
    return keyframes_json


def test_keyframes_infos():
    """测试关键帧信息生成功能"""
    # 测试基本功能
    print("测试基本功能:")
    
    # 示例输入参数
    ctype = "KFTypePositionX"
    offsets = "0|100"
    values = "1|2"
    segment_infos = [
        {
            "end": 5000000,
            "id": "c1369c795ca64fe38bac1f2a93e8a811",
            "start": 0
        }
    ]
    width = 1920
    height = 1080
    
    keyframes_json = keyframes_infos(ctype, offsets, values, segment_infos, height, width)
    print(f"Keyframes JSON: {keyframes_json}")
    
    # 解析JSON验证内容
    keyframes = json.loads(keyframes_json)
    print(f"Parsed keyframes: {keyframes}")
    
    # 验证内容
    assert len(keyframes) == 2
    assert keyframes[0]["offset"] == 0
    assert keyframes[0]["property"] == "KFTypePositionX"
    assert keyframes[0]["segment_id"] == "c1369c795ca64fe38bac1f2a93e8a811"
    # 由于是KFTypePositionX类型并且提供了width，值应该被归一化
    assert keyframes[0]["value"] == 1 / 1920
    
    assert keyframes[1]["offset"] == 5000000
    assert keyframes[1]["property"] == "KFTypePositionX"
    assert keyframes[1]["segment_id"] == "c1369c795ca64fe38bac1f2a93e8a811"
    # 由于是KFTypePositionX类型并且提供了width，值应该被归一化
    assert keyframes[1]["value"] == 2 / 1920
    
    print("基本功能测试通过")
    
    # 测试不提供width和height的情况
    print("\n测试不提供width和height的情况:")
    keyframes_json_no_dim = keyframes_infos(ctype, offsets, values, segment_infos)
    keyframes_no_dim = json.loads(keyframes_json_no_dim)
    print(f"Keyframes without dimensions: {keyframes_no_dim}")
    
    # 验证值没有被归一化
    assert keyframes_no_dim[0]["value"] == 1
    assert keyframes_no_dim[1]["value"] == 2
    
    print("不提供width和height测试通过")
    
    # 测试KFTypePositionY类型
    print("\n测试KFTypePositionY类型:")
    ctype_y = "KFTypePositionY"
    keyframes_json_y = keyframes_infos(ctype_y, offsets, values, segment_infos, height, width)
    keyframes_y = json.loads(keyframes_json_y)
    print(f"Keyframes Y: {keyframes_y}")
    
    # 验证值被height归一化
    assert keyframes_y[0]["value"] == 1 / 1080
    assert keyframes_y[1]["value"] == 2 / 1080
    
    print("KFTypePositionY类型测试通过")
    
    # 测试多个offset和value
    print("\n测试多个offset和value:")
    offsets_multi = "0|50|100"
    values_multi = "1|2|1"
    keyframes_json_multi = keyframes_infos(ctype, offsets_multi, values_multi, segment_infos, height, width)
    keyframes_multi = json.loads(keyframes_json_multi)
    print(f"Keyframes multi: {keyframes_multi}")
    
    # 验证生成了3个关键帧
    assert len(keyframes_multi) == 3
    assert keyframes_multi[0]["offset"] == 0
    assert keyframes_multi[1]["offset"] == 2500000  # 50% of 5000000
    assert keyframes_multi[2]["offset"] == 5000000
    
    print("多个offset和value测试通过")
    
    print("\n所有测试通过!")


if __name__ == "__main__":
    test_keyframes_infos()