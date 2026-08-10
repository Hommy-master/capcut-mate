#!/usr/bin/env python3
"""
跨平台兼容性测试脚本
验证在不同平台上的导入和基本功能
"""

import sys
import platform

def test_cross_platform_compatibility():
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python version: {sys.version}")
    print("=" * 50)
    
    # 测试基础导入
    try:
        import src.pyJianYingDraft as draft
        print("✅ 基础导入成功")
        print(f"   ISWIN: {draft.ISWIN}")
        print(f"   JianyingController available: {draft.JianyingController is not None}")
    except Exception as e:
        print(f"❌ 基础导入失败: {e}")
        return False
    
    # 测试服务层导入
    try:
        from src import service
        print("✅ 服务层导入成功")
    except Exception as e:
        print(f"❌ 服务层导入失败: {e}")
        return False
    
    # 测试API层导入
    try:
        from src.router import v1
        print("✅ API层导入成功")
    except Exception as e:
        print(f"❌ API层导入失败: {e}")
        return False
    
    # 测试工具层导入
    try:
        from src.utils import helper
        print("✅ 工具层导入成功")
    except Exception as e:
        print(f"❌ 工具层导入失败: {e}")
        return False
    
    print("=" * 50)
    print("🎉 所有基础导入测试通过!")
    
    # 平台特定测试
    if draft.ISWIN:
        print("\n🖥️  Windows平台特定测试:")
        try:
            # 测试UI自动化相关导入
            from src.utils.video_task_manager import UIAutomationInitializerInThread
            print("✅ UI自动化初始化器导入成功")
            
            # 测试剪映控制器
            if draft.JianyingController:
                print("✅ 剪映控制器可用")
            else:
                print("⚠️  剪映控制器不可用")
                
        except Exception as e:
            print(f"❌ Windows特定功能测试失败: {e}")
    else:
        print("\n🐧 Linux平台特定测试:")
        try:
            # 测试UI自动化占位符
            from src.utils.video_task_manager import UIAutomationInitializerInThread
            print("✅ UI自动化占位符导入成功")
            
            # 测试占位符功能
            with UIAutomationInitializerInThread():
                print("✅ UI自动化占位符上下文管理器工作正常")
                
        except Exception as e:
            print(f"❌ Linux特定功能测试失败: {e}")
    
    return True

if __name__ == "__main__":
    success = test_cross_platform_compatibility()
    sys.exit(0 if success else 1)