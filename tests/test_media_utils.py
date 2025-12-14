import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.media import get_media_duration, get_media_duration_formatted


def test_media_duration():
    """测试媒体时长获取功能"""
    # 测试不存在的文件
    print("测试不存在的文件:")
    duration = get_media_duration("nonexistent.mp3")
    print(f"时长: {duration}")
    
    # 测试存在的音频文件
    print("\n测试存在的音频文件:")
    duration = get_media_duration("test_audio.wav")
    print(f"WAV文件时长(微秒): {duration}")
    
    formatted = get_media_duration_formatted("test_audio.wav")
    print(f"WAV文件时长(格式化): {formatted}")
    
    # 清理测试文件
    if os.path.exists("test_audio.wav"):
        os.remove("test_audio.wav")
        print("已清理测试文件")


if __name__ == "__main__":
    test_media_duration()