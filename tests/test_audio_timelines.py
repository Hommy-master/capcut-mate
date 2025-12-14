import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.service.audio_timelines import audio_timelines


def test_audio_timelines():
    """测试音频时间线计算功能"""
    # 测试空链接列表
    print("测试空链接列表:")
    timelines, all_timelines = audio_timelines([])
    print(f"Timelines: {timelines}")
    print(f"All timelines: {all_timelines}")
    
    # 测试正常情况（这里只是模拟，实际测试需要真实的音频文件URL）
    # 我们可以在这里添加更多的测试用例


if __name__ == "__main__":
    test_audio_timelines()