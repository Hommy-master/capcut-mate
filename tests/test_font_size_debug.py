def test_font_size_logic():
    """测试字体大小逻辑"""
    
    # 模拟caption数据
    caption = {
        "start": 0,
        "end": 5000000,
        "text": "测试字体大小"
    }
    
    # 模拟函数参数
    font_size = 15  # add_captions函数的默认值
    
    # 模拟add_caption_to_draft中的逻辑
    size = float(caption.get('font_size', font_size))
    
    print(f"caption: {caption}")
    print(f"font_size参数: {font_size}")
    print(f"计算出的字体大小: {size}")
    
    # 测试当caption中有font_size时的情况
    caption_with_font_size = {
        "start": 0,
        "end": 5000000,
        "text": "测试字体大小",
        "font_size": 20
    }
    
    size2 = float(caption_with_font_size.get('font_size', font_size))
    
    print(f"\ncaption_with_font_size: {caption_with_font_size}")
    print(f"font_size参数: {font_size}")
    print(f"计算出的字体大小: {size2}")

if __name__ == "__main__":
    test_font_size_logic()