import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.service.add_captions import parse_captions_data, apply_keyword_highlight
from src.pyJianYingDraft.text_segment import TextSegment, TextStyle, Timerange


def test_keyword_font_size_parsing():
    """测试keyword_font_size参数解析"""
    print("Testing keyword_font_size parameter parsing...")
    
    # 测试数据
    test_captions = [
        {
            "start": 0,
            "end": 10000000,
            "text": "你好，剪映",
            "keyword": "剪映",
            "keyword_font_size": 20  # 设置关键词字体大小
        },
        {
            "start": 10000000,
            "end": 20000000,
            "text": "欢迎使用剪映字幕功能",
            "keyword": "功能",
            "keyword_font_size": 18  # 设置关键词字体大小
        }
    ]
    
    # 将测试数据转换为JSON字符串
    captions_json = json.dumps(test_captions)
    
    # 解析字幕数据
    parsed_captions = parse_captions_data(captions_json)
    
    # 验证解析结果
    assert len(parsed_captions) == 2
    assert parsed_captions[0]["keyword_font_size"] == 20
    assert parsed_captions[1]["keyword_font_size"] == 18
    print("✓ keyword_font_size parameter parsing test passed")


def test_keyword_font_size_application():
    """测试keyword_font_size参数应用"""
    print("Testing keyword_font_size parameter application...")
    
    # 创建一个文本片段
    text_segment = TextSegment(
        text="你好，剪映",
        timerange=Timerange(start=0, duration=5000000),
        style=TextStyle(size=15.0)  # 默认字体大小为15
    )
    
    # 应用关键词高亮，指定关键词字体大小为20
    apply_keyword_highlight(text_segment, "剪映", (1.0, 0.0, 0.0), 20.0)
    
    # 验证额外样式是否正确应用
    assert len(text_segment.extra_styles) == 1
    highlight_style = text_segment.extra_styles[0]
    assert highlight_style["size"] == 20.0  # 验证关键词字体大小是否为20
    assert highlight_style["range"] == [3, 5]  # 验证关键词位置是否正确
    print("✓ keyword_font_size parameter application test passed")


def test_keyword_font_size_default():
    """测试keyword_font_size参数默认值"""
    print("Testing keyword_font_size parameter default value...")
    
    # 创建一个文本片段
    text_segment = TextSegment(
        text="你好，剪映",
        timerange=Timerange(start=0, duration=5000000),
        style=TextStyle(size=15.0)  # 默认字体大小为15
    )
    
    # 应用关键词高亮，不指定关键词字体大小，应该使用默认值
    apply_keyword_highlight(text_segment, "剪映", (1.0, 0.0, 0.0))
    
    # 验证额外样式是否正确应用
    assert len(text_segment.extra_styles) == 1
    highlight_style = text_segment.extra_styles[0]
    assert highlight_style["size"] == 15.0  # 验证关键词字体大小是否为默认值15
    print("✓ keyword_font_size parameter default value test passed")


if __name__ == "__main__":
    print("Running keyword_font_size tests...")
    test_keyword_font_size_parsing()
    test_keyword_font_size_application()
    test_keyword_font_size_default()
    print("All tests passed!")