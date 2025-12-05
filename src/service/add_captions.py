import json
from typing import List, Dict, Any, Tuple, Optional, Literal

from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile, TrackType, TextSegment, TextStyle, ClipSettings, Timerange, FontType, TextBorder
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
from src.utils import helper


def add_captions(
    draft_url: str,
    captions: str,
    text_color: str = "#ffffff",
    border_color: Optional[str] = None,
    alignment: int = 1,
    alpha: float = 1.0,
    font: Optional[str] = None,
    font_size: int = 15,
    letter_spacing: Optional[float] = None,
    line_spacing: Optional[float] = None,
    scale_x: float = 1.0,
    scale_y: float = 1.0,
    transform_x: float = 0.0,
    transform_y: float = 0.0,
    style_text: bool = False,
    underline: bool = False,
    italic: bool = False,
    bold: bool = False
) -> Tuple[str, str, List[str], List[str], List[dict]]:
    """
    批量添加字幕到剪映草稿的业务逻辑
    
    Args:
        draft_url: 草稿URL
        captions: 字幕信息列表的JSON字符串，格式如下：
            [
                {
                    "start": 0,  # 字幕开始时间（微秒）
                    "end": 10000000,  # 字幕结束时间（微秒）
                    "text": "你好，剪映",  # 字幕文本内容
                    "keyword": "好",  # 关键词（用|分隔多个关键词），可选参数
                    "keyword_color": "#457616",  # 关键词颜色，可选参数
                    "keyword_font_size": 15,  # 关键词字体大小，可选参数
                    "font_size": 15,  # 文本字体大小，可选参数
                    "in_animation": None,  # 入场动画，可选参数
                    "out_animation": None,  # 出场动画，可选参数
                    "loop_animation": None,  # 循环动画，可选参数
                    "in_animation_duration": None,  # 入场动画时长，可选参数
                    "out_animation_duration": None,  # 出场动画时长，可选参数
                    "loop_animation_duration": None  # 循环动画时长，可选参数
                }
            ]
        text_color: 文本颜色（十六进制），默认"#ffffff"
        border_color: 边框颜色（十六进制），默认None
        alignment: 文本对齐方式（0-5），默认1
        alpha: 文本透明度（0.0-1.0），默认1.0
        font: 字体名称，默认None
        font_size: 字体大小，默认15
        letter_spacing: 字间距，默认None
        line_spacing: 行间距，默认None
        scale_x: 水平缩放，默认1.0
        scale_y: 垂直缩放，默认1.0
        transform_x: 水平位移，默认0.0
        transform_y: 垂直位移，默认0.0
        style_text: 是否使用样式文本，默认False
        underline: 文字下划线开关，默认False
        italic: 文本斜体开关，默认False
        bold: 文本加粗开关，默认False
    
    Returns:
        draft_url: 草稿URL
        track_id: 字幕轨道ID
        text_ids: 字幕ID列表
        segment_ids: 字幕片段ID列表
        segment_infos: 片段信息列表
    
    Raises:
        CustomException: 字幕添加失败
    """
    logger.info(f"add_captions started, draft_url: {draft_url}, captions count: {len(json.loads(captions) if captions else [])}")

    # 1. 提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        logger.error(f"Invalid draft_url or draft not found in cache: {draft_url}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    # 2. 解析字幕信息
    caption_items = parse_captions_data(json_str=captions)
    if len(caption_items) == 0:
        logger.info(f"No caption info provided, draft_id: {draft_id}")
        raise CustomException(CustomError.INVALID_CAPTION_INFO)

    logger.info(f"Parsed {len(caption_items)} caption items")

    # 3. 从缓存中获取草稿
    script: ScriptFile = DRAFT_CACHE[draft_id]

    # 4. 添加字幕轨道
    track_name = f"caption_track_{helper.gen_unique_id()}"
    script.add_track(track_type=TrackType.text, track_name=track_name)
    logger.info(f"Added caption track: {track_name}")

    # 5. 遍历字幕信息，添加字幕到草稿中的指定轨道，收集片段ID
    segment_ids = []
    text_ids = []
    segment_infos = []
    for i, caption in enumerate(caption_items):
        try:
            logger.info(f"Processing caption {i+1}/{len(caption_items)}, text: {caption['text'][:20]}...")
            
            segment_id, text_id, segment_info = add_caption_to_draft(
                script, track_name,
                caption=caption,
                text_color=text_color,
                border_color=border_color,
                alignment=alignment,
                alpha=alpha,
                font=font,
                font_size=font_size,
                letter_spacing=letter_spacing,
                line_spacing=line_spacing,
                scale_x=scale_x,
                scale_y=scale_y,
                transform_x=transform_x,
                transform_y=transform_y,
                style_text=style_text,
                underline=underline,
                italic=italic,
                bold=bold
            )
            segment_ids.append(segment_id)
            text_ids.append(text_id)
            segment_infos.append(segment_info)
            logger.info(f"Added caption {i+1}/{len(caption_items)}, segment_id: {segment_id}")
        except Exception as e:
            logger.error(f"Failed to add caption {i+1}/{len(caption_items)}, error: {str(e)}")
            raise

    # 6. 保存草稿
    script.save()
    logger.info(f"Draft saved successfully")

    # 7. 获取当前字幕轨道ID
    track_id = ""
    for key in script.tracks.keys():
        if script.tracks[key].name == track_name:
            track_id = script.tracks[key].track_id
            break
    logger.info(f"Caption track created, draft_id: {draft_id}, track_id: {track_id}")

    logger.info(f"add_captions completed successfully - draft_id: {draft_id}, track_id: {track_id}, captions_added: {len(caption_items)}")
    
    return draft_url, track_id, text_ids, segment_ids, segment_infos


def add_caption_to_draft(
    script: ScriptFile,
    track_name: str,
    caption: dict,
    text_color: str = "#ffffff",
    border_color: Optional[str] = None,
    alignment: int = 1,
    alpha: float = 1.0,
    font: Optional[str] = None,
    font_size: int = 15,
    letter_spacing: Optional[float] = None,
    line_spacing: Optional[float] = None,
    scale_x: float = 1.0,
    scale_y: float = 1.0,
    transform_x: float = 0.0,
    transform_y: float = 0.0,
    style_text: bool = False,
    underline: bool = False,
    italic: bool = False,
    bold: bool = False
) -> Tuple[str, str, dict]:
    """
    向剪映草稿中添加单个字幕
    
    Args:
        script: 草稿文件对象
        track_name: 字幕轨道名称
        caption: 字幕信息字典，包含以下字段：
            start: 字幕开始时间（微秒）
            end: 字幕结束时间（微秒）
            text: 字幕文本内容
            keyword: 关键词（用|分隔多个关键词），可选
            keyword_color: 关键词颜色，可选
            keyword_font_size: 关键词字体大小，可选
            font_size: 文本字体大小，可选
            in_animation: 入场动画，可选
            out_animation: 出场动画，可选
            loop_animation: 循环动画，可选
            in_animation_duration: 入场动画时长，可选
            out_animation_duration: 出场动画时长，可选
            loop_animation_duration: 循环动画时长，可选
        其他参数：字幕样式设置
    
    Returns:
        segment_id: 片段ID
        text_id: 文本ID（material_id）
        segment_info: 片段信息字典，包含id、start、end
    
    Raises:
        CustomException: 添加字幕失败
    """
    try:
        # 1. 创建时间范围
        caption_duration = caption['end'] - caption['start']
        timerange = Timerange(start=caption['start'], duration=caption_duration)
        
        # 2. 解析颜色
        rgb_color = hex_to_rgb(text_color)
        
        # 3. 创建文本样式
        align_value: Literal[0, 1, 2] = 0
        if alignment == 1:
            align_value = 1
        elif alignment == 2:
            align_value = 2
        
        text_style = TextStyle(
            size=float(caption.get('font_size', font_size)),
            color=rgb_color,
            alpha=alpha,
            align=align_value,
            letter_spacing=int(letter_spacing) if letter_spacing is not None else 0,
            line_spacing=int(line_spacing) if line_spacing is not None else 0,
            auto_wrapping=True,  # 字幕默认开启自动换行
            underline=underline,
            italic=italic,
            bold=bold
        )
        
        # 4. 创建文本描边（如果提供了border_color）
        text_border = None
        if border_color:
            border_rgb_color = hex_to_rgb(border_color)
            text_border = TextBorder(color=border_rgb_color)
        
        # 5. 创建字体（如果提供了font）
        font_type = None
        if font:
            try:
                # 尝试根据字体名称查找对应的FontType
                font_type = getattr(FontType, font, None)
                if font_type is None:
                    logger.warning(f"Font '{font}' not found, using default font")
            except AttributeError:
                logger.warning(f"Font '{font}' not found, using default font")
        
        # 6. 创建图像调节设置
        clip_settings = ClipSettings(
            scale_x=scale_x,
            scale_y=scale_y,
            transform_x=transform_x / script.width,  # 转换为画布宽度单位
            transform_y=transform_y / script.height  # 转换为画布高度单位
        )
        
        # 7. 创建文本片段
        text_segment = TextSegment(
            text=caption['text'],
            timerange=timerange,
            style=text_style,
            border=text_border,  # 添加边框
            font=font_type,      # 添加字体
            clip_settings=clip_settings
        )
        
        logger.info(f"Created text segment, material_id: {text_segment.material_id}")
        logger.info(f"Text segment details - start: {caption['start']}, duration: {caption_duration}, text: {caption['text'][:50]}")

        # 8. 处理关键词高亮
        if caption.get('keyword'):
            keyword_color = caption.get('keyword_color', '#ff7100')  # 默认橙色
            keyword_rgb_color = hex_to_rgb(keyword_color)
            # 应用关键词颜色到文本样式中
            apply_keyword_highlight(text_segment, caption['keyword'], keyword_rgb_color)
            logger.info(f"Applied keyword highlighting: {caption['keyword']} with color {keyword_color}")
        
        # 9. TODO: 处理动画效果（需要导入相应的动画类型）
        if caption.get('in_animation'):
            logger.info(f"In animation specified but not implemented yet: {caption['in_animation']}")
        if caption.get('out_animation'):
            logger.info(f"Out animation specified but not implemented yet: {caption['out_animation']}")
        if caption.get('loop_animation'):
            logger.info(f"Loop animation specified but not implemented yet: {caption['loop_animation']}")

        # 10. 向指定轨道添加片段
        script.add_segment(text_segment, track_name)

        # 11. 构造片段信息
        segment_info = {
            "id": text_segment.segment_id,
            "start": caption['start'],
            "end": caption['end']
        }

        return text_segment.segment_id, text_segment.material_id, segment_info
        
    except CustomException:
        logger.error(f"Add caption to draft failed, caption: {caption}")
        raise
    except Exception as e:
        logger.error(f"Add caption to draft failed, error: {str(e)}")
        raise CustomException(CustomError.CAPTION_ADD_FAILED)


def apply_keyword_highlight(text_segment: TextSegment, keywords: str, keyword_color: tuple):
    """
    应用关键词高亮到文本片段
    
    Args:
        text_segment: 文本片段对象
        keywords: 关键词字符串，用'|'分隔多个关键词
        keyword_color: 关键词颜色的RGB元组 (0-1范围)
    """
    # 分割关键词
    keyword_list = keywords.split('|')
    text = text_segment.text
    
    # 为每个关键词创建高亮样式
    for keyword in keyword_list:
        keyword = keyword.strip()
        if not keyword:
            continue
            
        # 查找所有匹配的关键词位置
        start_pos = 0
        while start_pos < len(text):
            start_pos = text.find(keyword, start_pos)
            if start_pos == -1:
                break
                
            end_pos = start_pos + len(keyword)
            
            # 创建关键词高亮样式
            highlight_style = {
                "fill": {
                    "alpha": 1.0,
                    "content": {
                        "render_type": "solid",
                        "solid": {
                            "alpha": 1.0,
                            "color": list(keyword_color)  # 使用关键词颜色
                        }
                    }
                },
                "range": [start_pos, end_pos],
                "size": text_segment.style.size,
                "bold": text_segment.style.bold,
                "italic": text_segment.style.italic,
                "underline": text_segment.style.underline
            }
            
            # 只有在确实有描边时才添加描边信息，避免默认黑色描边的出现
            if text_segment.border:
                highlight_style["strokes"] = [text_segment.border.export_json()]
            
            # 添加到文本片段的额外样式中
            text_segment.extra_styles.append(highlight_style)
            start_pos = end_pos


def parse_captions_data(json_str: str) -> List[Dict[str, Any]]:
    """
    解析字幕数据的JSON字符串，处理可选字段的默认值
    
    Args:
        json_str: 包含字幕数据的JSON字符串，格式如下：
        [
            {
                "start": 0,  # [必选] 字幕开始时间（微秒）
                "end": 10000000,  # [必选] 字幕结束时间（微秒）
                "text": "你好，剪映",  # [必选] 字幕文本内容
                "keyword": "好",  # [可选] 关键词（用|分隔多个关键词）
                "keyword_color": "#457616",  # [可选] 关键词颜色，默认"#ff7100"
                "keyword_font_size": 15,  # [可选] 关键词字体大小，默认15
                "font_size": 15,  # [可选] 文本字体大小，默认15
                "in_animation": None,  # [可选] 入场动画，默认None
                "out_animation": None,  # [可选] 出场动画，默认None
                "loop_animation": None,  # [可选] 循环动画，默认None
                "in_animation_duration": None,  # [可选] 入场动画时长，默认None
                "out_animation_duration": None,  # [可选] 出场动画时长，默认None
                "loop_animation_duration": None  # [可选] 循环动画时长，默认None
            }
        ]
        
    Returns:
        包含字幕对象的数组，每个对象都处理了默认值
        
    Raises:
        CustomException: 当JSON格式错误或缺少必选字段时抛出
    """
    try:
        # 解析JSON字符串
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e.msg}")
        raise CustomException(CustomError.INVALID_CAPTION_INFO, f"JSON parse error: {e.msg}")
    
    # 确保输入是列表
    if not isinstance(data, list):
        logger.error("captions should be a list")
        raise CustomException(CustomError.INVALID_CAPTION_INFO, "captions should be a list")
    
    result = []
    
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            logger.error(f"the {i}th item should be a dict")
            raise CustomException(CustomError.INVALID_CAPTION_INFO, f"the {i}th item should be a dict")
        
        # 检查必选字段
        required_fields = ["start", "end", "text"]
        missing_fields = [field for field in required_fields if field not in item]
        
        if missing_fields:
            logger.error(f"the {i}th item is missing required fields: {', '.join(missing_fields)}")
            raise CustomException(CustomError.INVALID_CAPTION_INFO, f"the {i}th item is missing required fields: {', '.join(missing_fields)}")
        
        # 创建处理后的对象，设置默认值
        processed_item = {
            "start": item["start"],
            "end": item["end"],
            "text": item["text"],
            "keyword": item.get("keyword", None),
            "keyword_color": item.get("keyword_color", "#ff7100"),
            "keyword_font_size": item.get("keyword_font_size", 15),
            "font_size": item.get("font_size", 15),
            "in_animation": item.get("in_animation", None),
            "out_animation": item.get("out_animation", None),
            "loop_animation": item.get("loop_animation", None),
            "in_animation_duration": item.get("in_animation_duration", None),
            "out_animation_duration": item.get("out_animation_duration", None),
            "loop_animation_duration": item.get("loop_animation_duration", None)
        }
        
        # 验证数值类型和范围
        if not isinstance(processed_item["start"], (int, float)) or processed_item["start"] < 0:
            logger.error(f"the {i}th item has invalid start time: {processed_item['start']}")
            raise CustomException(CustomError.INVALID_CAPTION_INFO, f"the {i}th item has invalid start time")
        
        if not isinstance(processed_item["end"], (int, float)) or processed_item["end"] <= processed_item["start"]:
            logger.error(f"the {i}th item has invalid end time: {processed_item['end']}")
            raise CustomException(CustomError.INVALID_CAPTION_INFO, f"the {i}th item has invalid end time")
        
        if not isinstance(processed_item["text"], str) or len(processed_item["text"].strip()) == 0:
            logger.error(f"the {i}th item has invalid text: {processed_item['text']}")
            raise CustomException(CustomError.INVALID_CAPTION_INFO, f"the {i}th item has invalid text")
        
        # 验证字体大小
        if not isinstance(processed_item["font_size"], (int, float)) or processed_item["font_size"] <= 0:
            processed_item["font_size"] = 15
        if not isinstance(processed_item["keyword_font_size"], (int, float)) or processed_item["keyword_font_size"] <= 0:
            processed_item["keyword_font_size"] = 15
        
        result.append(processed_item)
    
    logger.info(f"Successfully parsed {len(result)} caption items")
    return result


def hex_to_rgb(hex_color: str) -> tuple:
    """
    将十六进制颜色值转换为RGB三元组（0-1范围）
    
    Args:
        hex_color: 十六进制颜色值，如"#ffffff"或"ffffff"
    
    Returns:
        RGB三元组，取值范围为[0, 1]
    """
    # 移除#号（如果存在）
    hex_color = hex_color.lstrip('#')
    
    # 确保是6位十六进制
    if len(hex_color) != 6:
        logger.warning(f"Invalid hex color format: {hex_color}, using white as default")
        return (1.0, 1.0, 1.0)
    
    try:
        # 转换为RGB值（0-255）
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # 转换为0-1范围
        return (r / 255.0, g / 255.0, b / 255.0)
    except ValueError:
        logger.warning(f"Invalid hex color format: {hex_color}, using white as default")
        return (1.0, 1.0, 1.0)