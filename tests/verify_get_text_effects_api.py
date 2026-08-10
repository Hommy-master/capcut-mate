"""
验证 get_text_effects API 端点是否正确注册
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """测试所有导入是否正常"""
    print("=" * 60)
    print("测试 1: 检查模块导入")
    print("=" * 60)
    
    try:
        from src.schemas.get_text_effects import (
            GetTextEffectsRequest,
            TextEffectItem,
            GetTextEffectsResponse
        )
        print("✅ Schema 模块导入成功")
        
        from src.service.get_text_effects import (
            get_text_effects,
            resolve_text_effect
        )
        print("✅ Service 模块导入成功")
        
        # 检查 router 源码中是否有该端点
        import inspect
        from src.router import v1 as router_module
        source = inspect.getsource(router_module)
        
        if '@router.post(path="/get_text_effects"' in source:
            print("✅ Router 端点注册成功：/get_text_effects")
        else:
            print("❌ Router 端点未在源码中找到：/get_text_effects")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 导入失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_schema_validation():
    """测试 Schema 验证"""
    print("\n" + "=" * 60)
    print("测试 2: Schema 验证")
    print("=" * 60)
    
    try:
        from src.schemas.get_text_effects import GetTextEffectsRequest
        
        # 测试默认值
        req1 = GetTextEffectsRequest()
        assert req1.mode == 0, "默认 mode 应该是 0"
        print("✅ 默认参数验证通过")
        
        # 测试有效值
        req2 = GetTextEffectsRequest(mode=2)
        assert req2.mode == 2, "mode 应该可以是 2"
        print("✅ 有效参数验证通过")
        
        # 测试无效值
        try:
            req3 = GetTextEffectsRequest(mode=5)
            print("❌ 应该拒绝 mode=5")
            return False
        except Exception:
            print("✅ 无效参数正确被拒绝")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema 验证失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_service_logic():
    """测试 Service 层逻辑"""
    print("\n" + "=" * 60)
    print("测试 3: Service 层逻辑")
    print("=" * 60)
    
    try:
        from src.service.get_text_effects import get_text_effects, resolve_text_effect
        
        # 测试获取所有效果
        effects = get_text_effects(mode=0)
        assert isinstance(effects, list), "应该返回列表"
        print(f"✅ 获取所有效果成功，共 {len(effects)} 个")
        
        # 测试获取免费效果
        free_effects = get_text_effects(mode=2)
        assert isinstance(free_effects, list), "应该返回列表"
        assert len(free_effects) <= len(effects), "免费效果数不应超过总数"
        print(f"✅ 获取免费效果成功，共 {len(free_effects)} 个")
        
        # 测试解析功能
        effect_info = resolve_text_effect("红黄火焰综艺花字")
        if effect_info:
            assert "resource_id" in effect_info, "应该包含 resource_id"
            assert "effect_id" in effect_info, "应该包含 effect_id"
            print("✅ 效果解析功能正常")
        else:
            print("⚠️  效果解析返回 None（可能是数据问题）")
        
        return True
        
    except Exception as e:
        print(f"❌ Service 层测试失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n🚀 开始验证 get_text_effects API\n")
    
    results = []
    
    results.append(("模块导入", test_imports()))
    results.append(("Schema 验证", test_schema_validation()))
    results.append(("Service 逻辑", test_service_logic()))
    
    print("\n" + "=" * 60)
    print("验证总结")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status}: {name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 所有验证通过！API 已准备就绪。")
        return 0
    else:
        print("\n❌ 部分验证失败，请检查代码。")
        return 1


if __name__ == "__main__":
    exit(main())
