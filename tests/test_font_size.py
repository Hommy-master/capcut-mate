import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pyJianYingDraft.text_segment import TextStyle, TextSegment
from src.pyJianYingDraft.time_util import Timerange

def test_font_size():
    """测试字体大小设置"""
    
    # 创建一个文本样式，指定字体大小为20
    text_style = TextStyle(
        size=20.0,
        color=(1.0, 1.0, 1.0),  # 白色
        alpha=1.0,
        align=1,  # 居中
        auto_wrapping=True
    )
    
    print(f"创建的TextStyle字体大小: {text_style.size}")
    
    # 创建一个时间范围
    timerange = Timerange(start=0, duration=5000000)  # 5秒
    
    # 创建文本片段
    text_segment = TextSegment(
        text="测试字体大小",
        timerange=timerange,
        style=text_style
    )
    
    print(f"TextSegment的style.size: {text_segment.style.size}")
    
    # 导出材质并检查字体大小
    material_json = text_segment.export_material()
    content = material_json["content"]
    print(f"导出的content: {content}")
    
    # 解析content JSON
    import json
    content_data = json.loads(content)
    styles = content_data["styles"]
    base_style = styles[0]
    print(f"基础样式中的字体大小: {base_style['size']}")

if __name__ == "__main__":
    test_font_size()