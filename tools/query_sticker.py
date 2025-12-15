#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
获取贴纸信息的工具脚本
通过调用 Coze API 的 workflow 接口获取贴纸信息，并将结果保存为 JSON 文件
"""

import json
import urllib.request
import sys
import os

# 配置文件路径
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# 默认配置
DEFAULT_CONFIG = {
    "workflow_id": "7583908377370361871",
    "auth_token": "pat_fUi05j4gGqMOPZMun2n3uRlK0o7SATWX3bPPh1lSJuFktmpJjRStWiG7LtlmIOrc",
    "output_file": os.path.join(OUTPUT_DIR, "sticker_result.json")
}

def query_stickers(keyword, workflow_id=None, auth_token=None):
    """
    调用 Coze API 获取贴纸信息
    
    Args:
        keyword (str): 搜索关键词
        workflow_id (str): workflow ID
        auth_token (str): 认证令牌
        
    Returns:
        dict: API 响应结果
    """
    
    # 使用传入参数或配置文件中的参数
    wid = workflow_id or DEFAULT_CONFIG["workflow_id"]
    token = auth_token or DEFAULT_CONFIG["auth_token"]
    
    # 构造请求
    url = "https://api.coze.cn/v1/workflow/run"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "workflow_id": wid,
        "parameters": {
            "keyword": keyword
        },
        "is_async": False
    }
    
    # 发送请求
    try:
        req = urllib.request.Request(
            url=url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        return result
    except urllib.error.HTTPError as e:
        error_response = e.read().decode('utf-8')
        print(f"HTTP 错误 {e.code}: {error_response}")
        return {"error": f"HTTP Error {e.code}", "message": error_response}
    except Exception as e:
        print(f"请求失败: {e}")
        return {"error": "Request Failed", "message": str(e)}


def save_result(result, output_file=None):
    """
    保存结果到 JSON 文件，格式与 config/sticker.json 一致
    
    Args:
        result (dict): 要保存的结果
        output_file (str): 输出文件路径
    """
    
    try:
        # 如果没有提供输出文件路径，则使用默认配置
        if output_file is None:
            output_file = DEFAULT_CONFIG["output_file"]
            
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 解析实际的贴纸数据
        sticker_data = []
        if "data" in result:
            # 解析嵌套的 JSON 数据
            data_content = result["data"]
            if isinstance(data_content, str):
                # 如果是字符串，需要再次解析为 JSON
                data_content = json.loads(data_content)
                
            if "data" in data_content:
                sticker_data = data_content["data"]
        
        # 保存结果，只保存贴纸数组部分
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sticker_data, f, indent=2, ensure_ascii=False)
            
        return output_file
    except Exception as e:
        print(f"保存结果失败: {e}")
        return None


def query_multiple_keywords(keywords, output_file=None):
    """
    循环调用query_stickers接口，查询多个关键词并将结果合并输出到文件
    
    Args:
        keywords (list): 关键词列表
        output_file (str): 输出文件路径
    """
    all_stickers = []
    
    for keyword in keywords:
        print(f"正在搜索关键词 '{keyword}' 的贴纸...")
        
        # 查询贴纸
        result = query_stickers(keyword)
        
        # 显示结果
        if "error" in result:
            print(f"查询关键词 '{keyword}' 失败: {result}")
        else:
            print(f"查询关键词 '{keyword}' 成功!")
            # 解析实际的贴纸数据
            sticker_data = []
            if "data" in result:
                data_content = result["data"]
                if isinstance(data_content, str):
                    # 如果是字符串，需要再次解析为 JSON
                    data_content = json.loads(data_content)
                    
                if "data" in data_content:
                    sticker_data = data_content["data"]
            
            print(f"关键词 '{keyword}' 找到 {len(sticker_data)} 个贴纸")
            # 合并贴纸数据
            all_stickers.extend(sticker_data)
    
    # 去重处理，根据sticker_id去重
    unique_stickers = []
    seen_ids = set()
    for sticker in all_stickers:
        sticker_id = sticker.get("sticker_id")
        if sticker_id and sticker_id not in seen_ids:
            unique_stickers.append(sticker)
            seen_ids.add(sticker_id)
    
    print(f"总共找到 {len(unique_stickers)} 个不重复的贴纸")
    
    # 保存合并后的结果
    try:
        # 如果没有提供输出文件路径，则使用默认配置
        if output_file is None:
            output_file = DEFAULT_CONFIG["output_file"]
            
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 保存结果，只保存贴纸数组部分
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(unique_stickers, f, indent=2, ensure_ascii=False)
            
        print(f"合并结果已保存到: {output_file}")
        return output_file
    except Exception as e:
        print(f"保存合并结果失败: {e}")
        return None


def main():
    """主函数"""
    # 定义要查询的关键词列表
    keywords = ["人物", "真理"]
    
    # 查询多个关键词并合并结果
    output_file = query_multiple_keywords(keywords)
    if not output_file:
        print("查询或保存结果失败")
        sys.exit(1)

if __name__ == "__main__":
    main()