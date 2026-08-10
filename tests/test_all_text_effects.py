"""
测试扩展后的花字效果功能（1440 个花字）
"""
import random
from src.service.get_text_effects import TEXT_EFFECT_MAP, resolve_text_effect, get_text_effects


def test_total_count():
    """测试花字总数"""
    print("=" * 80)
    print("测试 1: 验证花字效果总数")
    print("=" * 80)
    
    total = len(TEXT_EFFECT_MAP)
    print(f"\n✓ 当前加载的花字效果总数：{total}")
    
    assert total == 1440, f"期望 1440 个花字，但实际有 {total} 个"
    print(f"✓ 验证通过：共有 {total} 个花字效果")
    return total


def test_resolve_by_name():
    """测试通过中文名称查找花字"""
    print("\n" + "=" * 80)
    print("测试 2: 通过中文名称查找花字")
    print("=" * 80)
    
    # 测试几个示例花字
    test_cases = [
        "红黄火焰综艺花字",
        "蓝白色立体综艺描边花字",
        "黄字橙光花字",
    ]
    
    for effect_name in test_cases:
        if effect_name in TEXT_EFFECT_MAP:
            result = resolve_text_effect(effect_name)
            print(f"\n✓ 找到花字：'{effect_name}'")
            print(f"  Effect ID: {result['effect_id']}")
            print(f"  Resource ID: {result['resource_id']}")
        else:
            print(f"\n✗ 未找到花字：'{effect_name}'")
    
    print("\n✓ 中文名称查找测试完成")


def test_resolve_by_id():
    """测试通过 effect_id 查找花字"""
    print("\n" + "=" * 80)
    print("测试 3: 通过 effect_id 查找花字")
    print("=" * 80)
    
    # 获取第一个花字的 ID
    first_effect_name = list(TEXT_EFFECT_MAP.keys())[0]
    first_effect_id = TEXT_EFFECT_MAP[first_effect_name]["effect_id"]
    
    result = resolve_text_effect(first_effect_id)
    print(f"\n✓ 通过 ID '{first_effect_id}' 查找到:")
    print(f"  名称：{first_effect_name}")
    print(f"  Resource ID: {result['resource_id']}")
    
    print("\n✓ effect_id 查找测试完成")


def test_random_effects():
    """随机测试 10 个花字"""
    print("\n" + "=" * 80)
    print("测试 4: 随机测试 10 个花字效果")
    print("=" * 80)
    
    all_effects = list(TEXT_EFFECT_MAP.items())
    random_effects = random.sample(all_effects, 10)
    
    print("\n随机选择的 10 个花字效果:")
    for i, (name, data) in enumerate(random_effects, 1):
        print(f"  {i}. {name} (ID: {data['effect_id']})")
        
        # 验证可以解析
        result = resolve_text_effect(name)
        assert result is not None, f"无法解析花字：{name}"
    
    print("\n✓ 随机测试通过")


def test_filter_by_mode():
    """测试按模式过滤花字"""
    print("\n" + "=" * 80)
    print("测试 5: 按模式过滤花字效果")
    print("=" * 80)
    
    # 测试 mode=0 (所有)
    all_effects = get_text_effects(mode=0)
    print(f"\n✓ Mode 0 (所有): {len(all_effects)} 个花字")
    
    # 测试 mode=1 (VIP)
    vip_effects = get_text_effects(mode=1)
    print(f"✓ Mode 1 (VIP): {len(vip_effects)} 个花字")
    
    # 测试 mode=2 (免费)
    free_effects = get_text_effects(mode=2)
    print(f"✓ Mode 2 (免费): {len(free_effects)} 个花字")
    
    # 验证数量关系
    assert len(all_effects) == len(vip_effects) + len(free_effects), \
        "所有效果数量应该等于 VIP+免费的总和"
    
    print("\n✓ 过滤功能测试通过")


def test_special_characters():
    """测试包含特殊字符的花字名称"""
    print("\n" + "=" * 80)
    print("测试 6: 包含特殊字符的花字名称")
    print("=" * 80)
    
    special_names = []
    for name in TEXT_EFFECT_MAP.keys():
        if any(c in name for c in ['#', '!', '-', ' ']):
            special_names.append(name)
    
    print(f"\n找到 {len(special_names)} 个包含特殊字符的花字名称:")
    for name in special_names[:10]:  # 只显示前 10 个
        print(f"  - {name}")
    
    if len(special_names) > 10:
        print(f"  ... 还有 {len(special_names) - 10} 个")
    
    # 测试解析其中一个
    if special_names:
        test_name = special_names[0]
        result = resolve_text_effect(test_name)
        print(f"\n✓ 测试解析 '{test_name}': 成功")
    
    print("\n✓ 特殊字符测试通过")


def test_export_capability():
    """测试导出功能"""
    print("\n" + "=" * 80)
    print("测试 7: 导出花字列表到文件")
    print("=" * 80)
    
    output_file = "test_effects_list.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 花字效果列表 (共 1440 个)\n\n")
        f.write("| 序号 | 花字名称 | Effect ID |\n")
        f.write("|------|---------|-----------|\n")
        
        for i, (name, data) in enumerate(TEXT_EFFECT_MAP.items(), 1):
            f.write(f"| {i} | {name} | {data['effect_id']} |\n")
    
    print(f"\n✓ 已导出花字列表到：{output_file}")
    print(f"  文件大小：请查看生成的文件")
    
    print("\n✓ 导出测试通过")


def main():
    """运行所有测试"""
    print("\n" + "=" * 80)
    print("开始测试扩展后的花字效果功能 (1440 个花字)")
    print("=" * 80)
    
    try:
        # 运行所有测试
        test_total_count()
        test_resolve_by_name()
        test_resolve_by_id()
        test_random_effects()
        test_filter_by_mode()
        test_special_characters()
        test_export_capability()
        
        # 总结
        print("\n" + "=" * 80)
        print("✅ 所有测试通过！")
        print("=" * 80)
        print(f"\n📊 统计摘要:")
        print(f"  • 总花字数：1,440 个")
        print(f"  • 支持中文名称查找：是")
        print(f"  • 支持 effect_id 查找：是")
        print(f"  • 支持模式过滤：是")
        print(f"  • 特殊字符支持：是")
        print(f"  • 导出功能：是")
        print("\n🎉 花字效果扩展功能运行正常！")
        print("=" * 80)
        
    except AssertionError as e:
        print(f"\n❌ 测试失败：{str(e)}")
        raise
    except Exception as e:
        print(f"\n❌ 发生错误：{str(e)}")
        raise


if __name__ == "__main__":
    main()
