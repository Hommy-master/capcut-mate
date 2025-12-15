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
    保存结果到 JSON 文件
    
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
        
        # 保存结果
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
        return output_file
    except Exception as e:
        print(f"保存结果失败: {e}")
        return None

def main():
    """主函数"""
    # 直接使用固定的关键词进行测试
    keyword = "人物"
    
    print(f"正在搜索关键词 '{keyword}' 的贴纸...")
    
    # 查询贴纸
    result = query_stickers(keyword)
    
    # 显示结果
    if "error" in result:
        print(f"查询失败: {result}")
        sys.exit(1)
    else:
        print("查询成功!")
        if "data" in result:
            print(f"找到 {len(result['data'])} 个贴纸")
        elif "output" in result:
            # 处理 workflow 的输出格式
            output = result["output"]
            if isinstance(output, dict) and "data" in output:
                print(f"找到 {len(output['data'])} 个贴纸")
        
        # 保存结果
        output_file = save_result(result)
        if output_file:
            print(f"结果已保存到: {output_file}")
        else:
            print("结果保存失败")


if __name__ == "__main__":
    main()