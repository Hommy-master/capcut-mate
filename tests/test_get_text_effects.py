"""
测试获取花字效果列表 API
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.service.get_text_effects import get_text_effects


def test_get_all_text_effects():
    """测试获取所有花字效果"""
    print("=" * 60)
    print("测试：获取所有花字效果 (mode=0)")
    print("=" * 60)
    
    try:
        effects = get_text_effects(mode=0)
        print(f"\n✅ 成功获取 {len(effects)} 个花字效果")
        
        # 显示前 20 个
        print("\n前 20 个花字效果:")
        for i, effect in enumerate(effects[:20], 1):
            vip_tag = " [VIP]" if effect.get('is_vip') else ""
            print(f"  {i}. {effect['name']}{vip_tag} (ID: {effect['effect_id']})")
        
        # 统计 VIP 和免费
        vip_count = sum(1 for e in effects if e.get('is_vip', False))
        free_count = len(effects) - vip_count
        
        print(f"\n📊 统计:")
        print(f"   • VIP 效果：{vip_count} 个")
        print(f"   • 免费效果：{free_count} 个")
        print(f"   • 总计：{len(effects)} 个")
        
    except Exception as e:
        print(f"\n❌ 测试失败：{str(e)}")
        import traceback
        traceback.print_exc()


def test_get_vip_text_effects():
    """测试获取 VIP 花字效果"""
    print("\n" + "=" * 60)
    print("测试：获取 VIP 花字效果 (mode=1)")
    print("=" * 60)
    
    try:
        effects = get_text_effects(mode=1)
        print(f"\n✅ 成功获取 {len(effects)} 个 VIP 花字效果")
        
        if effects:
            print("\n前 10 个 VIP 花字效果:")
            for i, effect in enumerate(effects[:10], 1):
                print(f"  {i}. {effect['name']} (ID: {effect['effect_id']})")
        else:
            print("\nℹ️ 当前没有 VIP 花字效果")
        
    except Exception as e:
        print(f"\n❌ 测试失败：{str(e)}")


def test_get_free_text_effects():
    """测试获取免费花字效果"""
    print("\n" + "=" * 60)
    print("测试：获取免费花字效果 (mode=2)")
    print("=" * 60)
    
    try:
        effects = get_text_effects(mode=2)
        print(f"\n✅ 成功获取 {len(effects)} 个免费花字效果")
        
        # 显示前 20 个
        print("\n前 20 个免费花字效果:")
        for i, effect in enumerate(effects[:20], 1):
            print(f"  {i}. {effect['name']} (ID: {effect['effect_id']})")
        
        print(f"\n📊 总计：{len(effects)} 个免费花字效果")
        
    except Exception as e:
        print(f"\n❌ 测试失败：{str(e)}")


def test_invalid_mode():
    """测试无效模式"""
    print("\n" + "=" * 60)
    print("测试：无效模式 (mode=3)")
    print("=" * 60)
    
    try:
        effects = get_text_effects(mode=3)
        print(f"\n❌ 应该抛出异常但没有")
    except Exception as e:
        print(f"\n✅ 正确抛出异常：{type(e).__name__}")


if __name__ == "__main__":
    print("\n🚀 开始测试获取花字效果列表 API\n")
    
    test_get_all_text_effects()
    test_get_vip_text_effects()
    test_get_free_text_effects()
    test_invalid_mode()
    
    print("\n" + "=" * 60)
    print("✅ 所有测试完成！")
    print("=" * 60)
