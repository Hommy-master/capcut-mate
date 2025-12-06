import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.service.add_captions import add_caption_to_draft
from src.pyJianYingDraft import ScriptFile

def test_font_size_not_set():
    """测试未设置字体大小的情况"""
    
    # 创建一个模拟的草稿文件对象
    script = ScriptFile()
    
    # 创建一个字幕项，不指定font_size
    caption = {
        "start": 0,
        "end": 5000000,  # 5秒
        "text": "测试未设置字体大小"
    }
    
    try:
        # 调用add_caption_to_draft函数
        segment_id, text_id, segment_info = add_caption_to_draft(
            script=script,
            track_name="test_track",
            caption=caption,
            text_color="#ffffff",
            font_size=20  # 这是接口级别的默认值
        )
        
        print(f"成功添加字幕，segment_id: {segment_id}")
        print(f"text_id: {text_id}")
        print(f"segment_info: {segment_info}")
        
        # 检查导出的材质
        # 获取刚刚添加的文本片段
        text_segment = None
        for segment in script.segments.values():
            if segment.segment_id == segment_id:
                text_segment = segment
                break
        
        if text_segment:
            material_json = text_segment.export_material()
            print(f"导出的材质: {material_json}")
            
            # 检查content中的size字段
            import json
            content_data = json.loads(material_json["content"])
            styles = content_data["styles"]
            base_style = styles[0]
            
            if "size" in base_style:
                print(f"基础样式中的字体大小: {base_style['size']}")
            else:
                print("基础样式中没有size字段，表示未设置字体大小")
        else:
            print("未找到添加的文本片段")
            
    except Exception as e:
        print(f"添加字幕时出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_font_size_not_set()