#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简化测试 search_sticker 功能
"""

import sys
import os
import json
import random
import config

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def search_sticker(keyword: str) -> list:
    """
    搜索贴纸的业务逻辑（简化版）
    
    Args:
        keyword: 搜索关键词
        
    Returns:
        list: 贴纸数据列表，最多返回50条记录
    """
    print(f"Searching stickers with keyword: {keyword}")
    
    # 从配置文件中读取贴纸数据
    try:
        with open(config.STICKER_CONFIG_PATH, 'r', encoding='utf-8') as f:
            sticker_data = json.load(f)
    except FileNotFoundError:
        print(f"Sticker config file not found: {config.STICKER_CONFIG_PATH}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to parse sticker config file: {e}")
        return []
    except Exception as e:
        print(f"Failed to read sticker config file: {e}")
        return []
    
    # 根据关键词过滤数据（简单匹配标题）
    filtered_data = []
    for item in sticker_data:
        if keyword in item["title"]:
            filtered_data.append(item)
    
    print(f"Found {len(filtered_data)} stickers matching keyword: {keyword}")
    
    # 如果没有找到匹配的贴纸，随机返回50条记录
    if not filtered_data:
        print("No matching stickers found, returning 50 random stickers")
        # 确保不会超出总数据量
        sample_size = min(50, len(sticker_data))
        filtered_data = random.sample(sticker_data, sample_size)
    
    # 如果找到的贴纸超过50条，只返回前50条
    if len(filtered_data) > 50:
        print(f"Too many matching stickers ({len(filtered_data)}), returning only 50")
        filtered_data = filtered_data[:50]
    
    return filtered_data


def test_search_sticker():
    """测试搜索贴纸功能"""
    
    print("测试搜索贴纸功能")
    
    # 测试正常搜索
    print("\n1. 测试正常搜索 '梦幻':")
    result = search_sticker("梦幻")
    print(f"   找到 {len(result)} 条记录")
    if result:
        print(f"   第一条记录标题: {result[0]['title']}")
    
    # 测试搜索不到内容的情况
    print("\n2. 测试搜索不存在的关键词 '不存在的关键词':")
    result = search_sticker("不存在的关键词")
    print(f"   找到 {len(result)} 条记录（应该是随机的50条）")
    if result:
        print(f"   第一条记录标题: {result[0]['title']}")
    
    # 测试空关键词
    print("\n3. 测试空关键词:")
    result = search_sticker("")
    print(f"   找到 {len(result)} 条记录")
    if len(result) > 50:
        print("   应该只返回前50条记录")
    else:
        print(f"   返回了 {len(result)} 条记录")
    
    print("\n测试完成!")


if __name__ == "__main__":
    test_search_sticker()