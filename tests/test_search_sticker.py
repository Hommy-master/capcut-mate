#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试 search_sticker 功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.service.search_sticker import search_sticker


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