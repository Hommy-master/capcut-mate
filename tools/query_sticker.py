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
    "output_file": os.path.join(OUTPUT_DIR, "sticker.json")
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
                try:
                    data_content = json.loads(data_content)
                except json.JSONDecodeError as e:
                    print(f"解析JSON数据失败: {e}")
                    data_content = {}
                
            if isinstance(data_content, dict) and "data" in data_content:
                sticker_data = data_content["data"]
                # 确保sticker_data是一个列表，即使它是None
                if sticker_data is None:
                    sticker_data = []
                elif not isinstance(sticker_data, list):
                    print(f"警告: sticker_data不是列表类型，而是 {type(sticker_data)}")
                    sticker_data = []        
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
                    try:
                        data_content = json.loads(data_content)
                    except json.JSONDecodeError as e:
                        print(f"解析JSON数据失败: {e}")
                        data_content = {}
                    
                if isinstance(data_content, dict) and "data" in data_content:
                    sticker_data = data_content["data"]
                    # 确保sticker_data是一个列表，即使它是None
                    if sticker_data is None:
                        sticker_data = []
                    elif not isinstance(sticker_data, list):
                        print(f"警告: sticker_data不是列表类型，而是 {type(sticker_data)}")
                        sticker_data = []
            
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
    # 剪映贴纸搜索关键词大全 - 按功能/风格等维度分类的字符串数组
    # 核心功能类
    function_keywords = [
        "箭头", "圆圈", "高亮", "进度条", "序号", "标签", "重点", "划重点",
        "标题", "字幕", "弹幕", "泡泡字", "立体字", "花字", "手写体", "空心字",
        "按钮", "图标", "导航栏", "弹窗", "加载", "二维码", "水印",
        "马赛克", "遮挡", "模糊", "相框", "边框", "画框", "圆角", "虚线框",
        "点赞", "关注", "收藏", "评论", "分享", "箭头指示", "手势"
    ]

    # 风格/质感类
    style_keywords = [
        "动态", "静态", "透明", "渐变", "发光", "闪烁", "粒子", "线条风",
        "手绘", "卡通", "简约", "复古", "国潮", "赛博朋克", "科技感", "ins风",
        "梦幻", "唯美", "治愈", "暗黑", "清新", "可爱", "搞怪", "酷飒",
        "3D", "立体", "浮雕", "水墨", "剪纸", "像素", "涂鸦", "水彩"
    ]

    # 情绪/表情类
    emotion_keywords = [
        "爱心", "星星眼", "撒花", "开心", "快乐", "感动", "惊喜", "比心",
        "无语", "满头问号", "难过", "生气", "尴尬", "流汗", "晕", "崩溃",
        "震惊", "吐槽", "吃瓜", "doge", "捂脸", "大笑", "嘘", "害羞",
        "优雅永不过时", "可云式震惊", "电子包浆", "栓Q", "绝绝子"
    ]

    # 场景/节日类
    scene_keywords = [
        "vlog", "美食", "旅行", "运动", "学习", "办公", "游戏", "宠物",
        "春日", "夏日", "秋日", "冬日", "美拉德", "雪景", "落叶", "樱花",
        "春节", "中秋", "国庆", "圣诞", "元旦", "情人节", "七夕", "端午", "开学季",
        "直播", "促销", "抽奖", "婚礼", "生日", "派对", "毕业", "年会"
    ]

    # 元素/对象类
    element_keywords = [
        "太阳", "月亮", "星星", "云朵", "雨滴", "雪花", "火焰", "植物", "花朵",
        "爱心", "气球", "礼物", "蛋糕", "汽车", "飞机", "动物", "水果", "零食",
        "emoji", "标点", "数学符号", "货币符号", "国旗", "logo", "徽章",
        "彩带", "气球", "烟花", "光斑", "爱心雨", "花瓣", "蝴蝶", "星星"
    ]

    # 热门/分类类
    hot_keywords = [
        "热门", "推荐", "爆款", "新贴纸", "VIP", "免费",
        "抖音", "快手", "小红书", "B站", "视频号",
        "脸部装饰", "手势识别", "AR贴纸", "特效贴纸", "动态贴纸"
    ]

    # 合并所有关键词到一个总数组（去重）
    keywords = list(set(
        function_keywords + style_keywords + emotion_keywords + scene_keywords + element_keywords + hot_keywords
    ))
    
    # 查询多个关键词并合并结果
    output_file = query_multiple_keywords(keywords)
    if not output_file:
        print("查询或保存结果失败")
        sys.exit(1)

if __name__ == "__main__":
    main()