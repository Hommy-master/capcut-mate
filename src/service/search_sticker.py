from src.utils.logger import logger
from typing import List, Dict, Any
from src.schemas.search_sticker import StickerItem, StickerInfo, StickerPackage, LargeImage
import json
import config
import random


def search_sticker(keyword: str) -> List[Dict[str, Any]]:
    """
    搜索贴纸的业务逻辑
    
    Args:
        keyword: 搜索关键词
        
    Returns:
        List[Dict[str, Any]]: 贴纸数据列表，最多返回50条记录
    """
    logger.info(f"Searching stickers with keyword: {keyword}")
    
    # 从配置文件中读取贴纸数据
    try:
        with open(config.STICKER_CONFIG_PATH, 'r', encoding='utf-8') as f:
            sticker_data = json.load(f)
    except FileNotFoundError:
        logger.error(f"Sticker config file not found: {config.STICKER_CONFIG_PATH}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse sticker config file: {e}")
        return []
    except Exception as e:
        logger.error(f"Failed to read sticker config file: {e}")
        return []
    
    # 根据关键词过滤数据（简单匹配标题）
    filtered_data = []
    for item in sticker_data:
        if keyword in item["title"]:
            filtered_data.append(item)
    
    logger.info(f"Found {len(filtered_data)} stickers matching keyword: {keyword}")
    
    # 如果没有找到匹配的贴纸，随机返回50条记录
    if not filtered_data:
        logger.info("No matching stickers found, returning 50 random stickers")
        # 确保不会超出总数据量
        sample_size = min(50, len(sticker_data))
        filtered_data = random.sample(sticker_data, sample_size)
    
    # 如果找到的贴纸超过50条，只返回前50条
    if len(filtered_data) > 50:
        logger.info(f"Too many matching stickers ({len(filtered_data)}), returning only 50")
        filtered_data = filtered_data[:50]
    
    return filtered_data