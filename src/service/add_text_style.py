import json
import re
from typing import List, Dict, Any, Tuple
from src.utils.logger import logger


def add_text_style(
    text: str,
    keyword: str,
    font_size: int = 12,
    keyword_color: str = "#ff7100",
    keyword_font_size: int = 15
) -> str:
    """
    为文本创建富文本样式，支持关键词高亮、颜色设置、字体大小调整等功能
    
    Args:
        text: 要处理的文本内容，必选参数
        keyword: 关键词，多个用 | 分隔，必选参数
        font_size: 普通文本的字体大小，默认值：12
        keyword_color: 关键词文本颜色（十六进制），默认值："#ff7100"
        keyword_font_size: 关键词字体大小，默认值：15
    
    Returns:
        text_style: 文本样式JSON字符串，包含styles数组和text字段
    
    Raises:
        Exception: 文本样式处理失败
    """
    logger.info(f"add_text_style started, text: {text[:20]}..., keyword: {keyword}")

    try:
        # 1. 解析关键词
        keywords = parse_keywords(keyword)
        if not keywords:
            logger.warning("No valid keywords found")
            return create_simple_text_style(text, font_size)

        logger.info(f"Parsed {len(keywords)} keywords: {keywords}")

        # 2. 查找关键词位置
        keyword_positions = find_keyword_positions(text, keywords)
        logger.info(f"Found {len(keyword_positions)} keyword matches")

        # 3. 解析颜色
        keyword_rgb = hex_to_rgb(keyword_color)
        normal_rgb = [1.0, 1.0, 1.0]  # 默认白色
        
        logger.info(f"Keyword color RGB: {keyword_rgb}")

        # 4. 生成文本样式
        styles = generate_text_styles(
            text, 
            keyword_positions, 
            font_size, 
            keyword_font_size, 
            normal_rgb, 
            keyword_rgb
        )

        # 5. 构建响应对象
        result = {
            "text": text,
            "styles": styles
        }

        # 6. 转换为JSON字符串
        text_style_json = json.dumps(result, ensure_ascii=False, separators=(',', ':'))
        
        logger.info(f"add_text_style completed successfully, generated {len(styles)} style segments")
        
        return text_style_json

    except Exception as e:
        logger.error(f"add_text_style failed, error: {str(e)}")
        raise


def parse_keywords(keyword_str: str) -> List[str]:
    """
    解析关键词字符串，支持多个关键词用 | 分隔
    
    Args:
        keyword_str: 关键词字符串，格式如 "快乐|顶级思维"
    
    Returns:
        关键词列表，按长度降序排列（先匹配长关键词）
    """
    if not keyword_str or not keyword_str.strip():
        return []
    
    # 分割关键词，去除空白
    keywords = [kw.strip() for kw in keyword_str.split('|') if kw.strip()]
    
    # 按长度降序排列，优先匹配长关键词
    keywords.sort(key=len, reverse=True)
    
    logger.info(f"Parsed keywords: {keywords}")
    return keywords


def find_keyword_positions(text: str, keywords: List[str]) -> List[Tuple[int, int, str]]:
    """
    在文本中查找所有关键词的位置
    
    Args:
        text: 目标文本
        keywords: 关键词列表
    
    Returns:
        位置列表，每个元素为 (start_pos, end_pos, keyword) 的元组
    """
    positions = []
    used_positions = set()  # 记录已使用的字符位置，避免重叠
    
    for keyword in keywords:
        # 使用正则表达式查找所有匹配位置
        for match in re.finditer(re.escape(keyword), text):
            start_pos = match.start()
            end_pos = match.end()
            
            # 检查是否与已有匹配重叠
            is_overlap = any(pos in used_positions for pos in range(start_pos, end_pos))
            
            if not is_overlap:
                positions.append((start_pos, end_pos, keyword))
                # 标记这些位置为已使用
                used_positions.update(range(start_pos, end_pos))
                logger.info(f"Found keyword '{keyword}' at position [{start_pos}, {end_pos})")
    
    # 按起始位置排序
    positions.sort(key=lambda x: x[0])
    
    return positions


def hex_to_rgb(hex_color: str) -> List[float]:
    """
    将十六进制颜色转换为RGB浮点数组
    
    Args:
        hex_color: 十六进制颜色，如 "#ff7100"
    
    Returns:
        RGB数组，值范围为0-1，如 [1.0, 0.44, 0.0]
    """
    # 移除 # 前缀
    hex_color = hex_color.lstrip('#')
    
    # 确保是6位十六进制
    if len(hex_color) != 6:
        logger.warning(f"Invalid hex color: {hex_color}, using default orange")
        hex_color = "ff7100"  # 默认橙色
    
    try:
        # 转换为RGB
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        
        return [r, g, b]
    except ValueError:
        logger.warning(f"Failed to parse hex color: {hex_color}, using default orange")
        return [1.0, 0.44313725490196076, 0.0]  # 默认橙色


def generate_text_styles(
    text: str,
    keyword_positions: List[Tuple[int, int, str]],
    normal_font_size: int,
    keyword_font_size: int,
    normal_color: List[float],
    keyword_color: List[float]
) -> List[Dict[str, Any]]:
    """
    生成文本样式数组
    
    Args:
        text: 原始文本
        keyword_positions: 关键词位置列表
        normal_font_size: 普通文本字体大小
        keyword_font_size: 关键词字体大小
        normal_color: 普通文本颜色RGB
        keyword_color: 关键词颜色RGB
    
    Returns:
        样式数组，每个元素包含range、size、fill等属性
    """
    styles = []
    current_pos = 0
    
    for start_pos, end_pos, keyword in keyword_positions:
        # 添加关键词前的普通文本样式
        if current_pos < start_pos:
            normal_style = create_text_style_segment(
                start=current_pos,
                end=start_pos,
                font_size=normal_font_size,
                color=normal_color,
                use_letter_color=False
            )
            styles.append(normal_style)
            logger.info(f"Added normal text style: [{current_pos}, {start_pos})")
        
        # 添加关键词样式
        keyword_style = create_text_style_segment(
            start=start_pos,
            end=end_pos,
            font_size=keyword_font_size,
            color=keyword_color,
            use_letter_color=True
        )
        styles.append(keyword_style)
        logger.info(f"Added keyword style for '{keyword}': [{start_pos}, {end_pos})")
        
        current_pos = end_pos
    
    # 添加最后剩余的普通文本样式
    if current_pos < len(text):
        normal_style = create_text_style_segment(
            start=current_pos,
            end=len(text),
            font_size=normal_font_size,
            color=normal_color,
            use_letter_color=False
        )
        styles.append(normal_style)
        logger.info(f"Added final normal text style: [{current_pos}, {len(text)})")
    
    return styles


def create_text_style_segment(
    start: int,
    end: int,
    font_size: int,
    color: List[float],
    use_letter_color: bool = False
) -> Dict[str, Any]:
    """
    创建单个文本样式片段
    
    Args:
        start: 起始位置
        end: 结束位置
        font_size: 字体大小
        color: 颜色RGB数组
        use_letter_color: 是否使用字母颜色
    
    Returns:
        样式片段字典
    """
    style = {
        "fill": {
            "content": {
                "solid": {
                    "color": color
                }
            }
        },
        "range": [start, end],
        "size": font_size,
        "font": {
            "id": "",
            "path": ""
        }
    }
    
    if use_letter_color:
        style["useLetterColor"] = True
    
    return style


def create_simple_text_style(text: str, font_size: int) -> str:
    """
    创建简单的文本样式（无关键词高亮）
    
    Args:
        text: 文本内容
        font_size: 字体大小
    
    Returns:
        简单的文本样式JSON字符串
    """
    result = {
        "text": text,
        "styles": [
            {
                "fill": {
                    "content": {
                        "solid": {
                            "color": [1.0, 1.0, 1.0]  # 白色
                        }
                    }
                },
                "range": [0, len(text)],
                "size": font_size,
                "font": {
                    "id": "",
                    "path": ""
                }
            }
        ]
    }
    
    return json.dumps(result, ensure_ascii=False, separators=(',', ':'))