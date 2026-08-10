"""
测试 add_captions 接口的 text_effect 功能
"""
import json
from src.service.add_captions import add_captions
from src.service.get_text_effects import resolve_text_effect, TEXT_EFFECT_MAP


def test_resolve_text_effect():
    """测试花字效果解析功能"""
    print("=" * 60)
    print("测试花字效果解析功能")
    print("=" * 60)
    
    # 测试 1: 通过中文名称查找
    print("\n测试 1: 通过中文名称查找 '白字橘色发光花字'")
    result = resolve_text_effect("白字橘色发光花字")
    if result:
        print(f"✓ 找到花字效果：{result}")
        assert result['effect_id'] == "7296357486490144036"
        assert result['resource_id'] == "7296357486490144036"
    else:
        print("✗ 未找到花字效果")
    
    # 测试 2: 通过 effect_id 查找
    print("\n测试 2: 通过 effect_id 查找 '7296357486490144036'")
    result = resolve_text_effect("7296357486490144036")
    if result:
        print(f"✓ 找到花字效果：{result}")
    else:
        print("✗ 未找到花字效果")
    
    # 测试 3: 不存在的名称
    print("\n测试 3: 查找不存在的花字效果 '不存在的花字'")
    result = resolve_text_effect("不存在的花字")
    if result is None:
        print("✓ 正确返回 None")
    else:
        print(f"✗ 应该返回 None，但返回了：{result}")
    
    print("\n" + "=" * 60)
    print("花字效果解析功能测试完成")
    print("=" * 60)


def test_text_effect_map():
    """测试花字映射表"""
    print("\n" + "=" * 60)
    print("测试花字映射表内容")
    print("=" * 60)
    
    print(f"\n花字映射表包含 {len(TEXT_EFFECT_MAP)} 个花字效果:")
    for name, data in TEXT_EFFECT_MAP.items():
        print(f"  - {name}: {data['effect_id']}")


def test_add_captions_with_text_effect():
    """测试添加字幕时应用花字效果（需要实际草稿环境）"""
    print("\n" + "=" * 60)
    print("测试 add_captions 集成花字效果功能")
    print("=" * 60)
    
    # 这是一个示例测试，实际需要有效的草稿 URL
    print("\n注意：此测试需要有效的草稿环境")
    print("示例调用代码:")
    print("""
    draft_url = "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=YOUR_DRAFT_ID"
    captions = json.dumps([
        {
            "start": 0,
            "end": 5000000,
            "text": "测试花字效果",
            "text_effect": "白字橘色发光花字"
        }
    ])
    
    # 使用全局 text_effect 参数
    draft_url, track_id, text_ids, segment_ids, segment_infos = add_captions(
        draft_url=draft_url,
        captions=captions,
        text_effect="白字橘色发光花字"  # 全局花字效果
    )
    
    # 或者在每个 caption 中单独指定
    captions = json.dumps([
        {
            "start": 0,
            "end": 5000000,
            "text": "测试花字效果 1",
            "text_effect": "白字橘色发光花字"  # 单个 caption 的花字
        },
        {
            "start": 5000000,
            "end": 10000000,
            "text": "测试花字效果 2",
            "text_effect": "黄字白色发光花字"  # 不同的花字
        }
    ])
    """)
    
    print("\n" + "=" * 60)
    print("集成测试示例完成")
    print("=" * 60)


if __name__ == "__main__":
    # 运行所有测试
    test_text_effect_map()
    test_resolve_text_effect()
    test_add_captions_with_text_effect()
    
    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("=" * 60)
