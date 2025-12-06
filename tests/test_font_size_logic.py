import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_font_size_logic():
    """测试字体大小逻辑"""
    
    # 模拟caption数据，不指定font_size
    caption_without_font_size = {
        "start": 0,
        "end": 5000000,
        "text": "测试字体大小"
    }
    
    # 模拟函数参数
    font_size = 20  # add_captions函数的默认值
    
    # 模拟add_caption_to_draft中的逻辑
    # 使用一个特殊值来表示未设置字体大小
    FONT_SIZE_NOT_SET = -1.0
    font_size_value = FONT_SIZE_NOT_SET
    if 'font_size' in caption_without_font_size and caption_without_font_size['font_size'] is not None:
        font_size_value = float(caption_without_font_size['font_size'])
    
    print(f"caption_without_font_size: {caption_without_font_size}")
    print(f"font_size参数: {font_size}")
    print(f"计算出的字体大小值: {font_size_value}")
    print(f"最终使用的字体大小: {font_size_value if font_size_value != FONT_SIZE_NOT_SET else 8.0}")
    
    # 测试当caption中有font_size时的情况
    caption_with_font_size = {
        "start": 0,
        "end": 5000000,
        "text": "测试字体大小",
        "font_size": 25
    }
    
    font_size_value2 = FONT_SIZE_NOT_SET
    if 'font_size' in caption_with_font_size and caption_with_font_size['font_size'] is not None:
        font_size_value2 = float(caption_with_font_size['font_size'])
    
    print(f"\ncaption_with_font_size: {caption_with_font_size}")
    print(f"font_size参数: {font_size}")
    print(f"计算出的字体大小值: {font_size_value2}")
    print(f"最终使用的字体大小: {font_size_value2}")

if __name__ == "__main__":
    test_font_size_logic()