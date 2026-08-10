#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试视频导出功能的错误处理
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.video_task_manager import VideoGenTaskManager
from src.utils.logger import logger

def test_export_error_handling():
    """测试导出功能的错误处理"""
    print("🧪 测试视频导出错误处理...")
    
    # 创建任务管理器实例
    task_manager = VideoGenTaskManager()
    
    # 创建一个测试任务
    test_task = type('TestTask', (), {
        'draft_id': 'test_draft_123',
        'progress': 0
    })()
    
    try:
        # 尝试调用导出功能（应该会抛出RuntimeError）
        result = task_manager._export_video(test_task, "test_output.mp4")
        print(f"❌ 预期应该抛出异常，但返回了: {result}")
    except RuntimeError as e:
        print(f"✅ 正确捕获RuntimeError: {e}")
        if "缺少Windows依赖" in str(e) or "仅在Windows平台可用" in str(e):
            print("✅ 错误信息符合预期")
        else:
            print(f"⚠️  错误信息不完全符合预期: {e}")
    except Exception as e:
        print(f"❌ 捕获到意外异常: {type(e).__name__}: {e}")
    
    print("✅ 错误处理测试完成")

if __name__ == "__main__":
    test_export_error_handling()