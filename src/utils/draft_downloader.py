"""
草稿下载工具
用于从API下载草稿文件并保存到指定目录
"""
import os
import re
import json
import requests
from urllib.parse import urlparse, parse_qs, urljoin
from typing import Optional
from src.utils.logger import logger
import config


def extract_draft_id_from_url(url: str) -> Optional[str]:
    """
    从URL中提取draft_id参数
    
    Args:
        url: 草稿URL
        
    Returns:
        draft_id: 草稿ID，如果找不到则返回None
    """
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        draft_ids = query_params.get('draft_id', [])
        return draft_ids[0] if draft_ids else None
    except Exception as e:
        logger.error(f"解析URL失败: {url}, 错误: {e}")
        return None


def download_draft(draft_url: str, save_path: Optional[str] = None) -> bool:
    """
    下载草稿文件到指定目录
    
    Args:
        draft_url: 草稿URL
        save_path: 保存路径，默认为config.DRAFT_SAVE_PATH
        
    Returns:
        bool: 下载是否成功
    """
    # 提取draft_id
    draft_id = extract_draft_id_from_url(draft_url)
    if not draft_id:
        logger.error(f"无法从URL中提取draft_id: {draft_url}")
        return False
    
    # 设置保存路径
    if save_path is None:
        save_path = config.DRAFT_SAVE_PATH
    
    # 构建并创建目标目录
    target_dir = prepare_target_directory(save_path, draft_id)
    
    logger.info(f"准备下载草稿: {draft_id} 到目录: {target_dir}")
    
    # 获取草稿文件列表
    files = get_draft_files_list(draft_url)
    if not files:
        logger.error(f"无法获取草稿文件列表: {draft_id}")
        return False
    
    # 下载所有文件
    return download_all_files(files, target_dir, draft_id)


def get_draft_files_list(draft_url: str) -> list:
    """
    获取草稿文件列表
    
    Args:
        draft_url: 草稿URL
        
    Returns:
        list: 文件URL列表
    """
    try:
        response = requests.get(draft_url)
        
        if response.status_code != 200:
            logger.error(f"获取草稿文件列表失败，状态码: {response.status_code}")
            return []
        
        # 解析JSON响应
        try:
            json_data = response.json()
        except json.JSONDecodeError as e:
            logger.error(f"解析草稿JSON响应失败: {e}")
            return []
        
        # 检查响应状态
        if json_data.get('code') != 0:
            logger.error(f"获取草稿文件列表失败: {json_data.get('message', '未知错误')}")
            return []
        
        # 返回files列表
        files = json_data.get('files', [])
        logger.info(f"获取到 {len(files)} 个草稿文件")
        return files
    except requests.exceptions.RequestException as e:
        logger.error(f"网络请求错误，获取草稿文件列表失败: {e}")
        return []
    except Exception as e:
        logger.error(f"获取草稿文件列表时发生未知错误: {e}")
        return []


def download_all_files(files: list, target_dir: str, draft_id: str) -> bool:
    """
    下载所有草稿文件
    
    Args:
        files: 文件URL列表
        target_dir: 目标目录
        draft_id: 草稿ID
        
    Returns:
        bool: 是否全部下载成功
    """
    success_count = 0
    total_files = len(files)
    
    for file_url in files:
        if download_single_file(file_url, target_dir):
            success_count += 1
        else:
            logger.error(f"下载单个文件失败: {file_url}")
    
    logger.info(f"草稿 {draft_id} 下载完成: 总计{total_files}, 成功{success_count}, 失败{total_files-success_count}")
    return success_count == total_files


def download_single_file(file_url: str, target_dir: str) -> bool:
    """
    下载单个文件并保持目录结构
    
    Args:
        file_url: 文件URL
        target_dir: 目标目录
        
    Returns:
        bool: 是否下载成功
    """
    try:
        # 发起请求下载文件
        response = requests.get(file_url)
        
        if response.status_code != 200:
            logger.error(f"下载文件失败，状态码: {response.status_code}, URL: {file_url}")
            return False
        
        # 解析文件URL以获得相对路径
        parsed_url = urlparse(file_url)
        path_parts = parsed_url.path.split('/')
        
        # 从文件URL中提取draft_id（通过路径部分）
        url_draft_id = None
        for part in path_parts:
            # 匹配类似20251204214904ccb1af38的格式，即以年份开头的长字符串
            if re.match(r'^\d{8,}.*$', part) and len(part) >= 10:  # 匹配以至少8位数字开头的字符串
                url_draft_id = part
                break
        
        # 找到包含draft_id的路径部分，然后保留其后的路径结构
        draft_id_index = -1
        if url_draft_id:
            for i, part in enumerate(path_parts):
                if url_draft_id in part:
                    draft_id_index = i
                    break
        
        if draft_id_index != -1:
            # 使用从包含draft_id部分的下一个位置开始的路径（跳过draft_id本身）
            rel_path_parts = path_parts[draft_id_index + 1:]  # 跳过draft_id本身
            rel_path = os.path.join(*rel_path_parts)
        else:
            # 如果没找到draft_id，使用整个路径（去除第一个空字符串）
            rel_path = os.path.join(*path_parts[1:])  # 跳过第一个空字符串
        
        # 构建完整的目标文件路径
        full_file_path = os.path.join(target_dir, rel_path)
        
        # 创建目录
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        
        # 写入文件
        with open(full_file_path, 'wb') as f:
            f.write(response.content)
        
        logger.debug(f"文件下载成功: {full_file_path}")
        return True
    
    except requests.exceptions.RequestException as e:
        logger.error(f"网络请求错误，下载文件失败: {e}, URL: {file_url}")
        return False
    except IOError as e:
        logger.error(f"文件写入错误，下载文件失败: {e}, URL: {file_url}")
        return False
    except Exception as e:
        logger.error(f"下载文件时发生未知错误: {e}, URL: {file_url}")
        return False


def prepare_target_directory(save_path: str, draft_id: str) -> str:
    """
    准备目标下载目录
    
    Args:
        save_path: 基础保存路径
        draft_id: 草稿ID
        
    Returns:
        str: 目标目录路径
    """
    target_dir = os.path.join(save_path, draft_id)
    os.makedirs(target_dir, exist_ok=True)
    return target_dir


def execute_download(draft_url: str, target_dir: str, draft_id: str) -> bool:
    """
    执行下载操作
    
    Args:
        draft_url: 草稿URL
        target_dir: 目标目录
        draft_id: 草稿ID
        
    Returns:
        bool: 下载是否成功
    """
    try:
        response = requests.get(draft_url)
        
        if response.status_code != 200:
            logger.error(f"下载草稿失败: {draft_id}, 状态码: {response.status_code}")
            return False
        
        file_path = get_file_path(response, target_dir, draft_id)
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"草稿下载成功: {file_path}")
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"网络请求错误，下载草稿失败: {draft_id}, 错误: {e}")
        return False
    except IOError as e:
        logger.error(f"文件写入错误，下载草稿失败: {draft_id}, 错误: {e}")
        return False
    except Exception as e:
        logger.error(f"未知错误，下载草稿失败: {draft_id}, 错误: {e}")
        return False


def get_file_path(response: requests.Response, target_dir: str, draft_id: str) -> str:
    """
    根据响应头或默认规则确定文件路径
    
    Args:
        response: HTTP响应对象
        target_dir: 目标目录
        draft_id: 草稿ID
        
    Returns:
        str: 完整的文件路径
    """
    filename = extract_filename_from_response(response, draft_id)
    filename = sanitize_filename(filename)
    return os.path.join(target_dir, filename)


def extract_filename_from_response(response: requests.Response, draft_id: str) -> str:
    """
    从HTTP响应头中提取文件名
    
    Args:
        response: HTTP响应对象
        draft_id: 草稿ID
        
    Returns:
        str: 文件名
    """
    content_disposition = response.headers.get('content-disposition', '')
    
    if content_disposition:
        import re
        fname_match = re.search(r'filename[^;=\n]*=(([\'\"]).*?\2|[^;\n]*)', content_disposition)
        if fname_match:
            return fname_match.group(1).strip('\'"')
    
    # 如果没有从响应头获取到文件名，使用默认名称
    return f"{draft_id}.draft"


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除不安全的字符
    
    Args:
        filename: 原始文件名
        
    Returns:
        str: 清理后的文件名
    """
    # 替换不安全的字符
    unsafe_chars = ['<', '>', ':', '"', '|', '?', '*']
    safe_filename = filename
    for char in unsafe_chars:
        safe_filename = safe_filename.replace(char, '_')
    
    # 移除开头和结尾的空格和点号
    safe_filename = safe_filename.strip(' .')
    
    return safe_filename


def batch_download_drafts(draft_urls: list, save_path: Optional[str] = None) -> dict:
    """
    批量下载草稿
    
    Args:
        draft_urls: 草稿URL列表
        save_path: 保存路径
        
    Returns:
        dict: 包含成功和失败统计的字典
    """
    results = initialize_batch_results()
    
    for url in draft_urls:
        process_single_draft(url, save_path, results)
    
    finalize_batch_results(results, draft_urls)
    return results


def initialize_batch_results() -> dict:
    """
    初始化批量下载结果字典
    
    Returns:
        dict: 初始化的结果字典
    """
    return {
        'success': [],
        'failure': [],
        'summary': {}
    }


def process_single_draft(url: str, save_path: Optional[str], results: dict) -> None:
    """
    处理单个草稿下载
    
    Args:
        url: 草稿URL
        save_path: 保存路径
        results: 结果统计字典
    """
    draft_id = extract_draft_id_from_url(url)
    if draft_id and download_draft(url, save_path):
        results['success'].append(draft_id)
        logger.info(f"批量下载成功: {draft_id}")
    else:
        results['failure'].append({'url': url, 'draft_id': draft_id})
        logger.error(f"批量下载失败: {draft_id or url}")


def finalize_batch_results(results: dict, draft_urls: list) -> None:
    """
    完成批量下载结果统计
    
    Args:
        results: 结果统计字典
        draft_urls: 草稿URL列表
    """
    total = len(draft_urls)
    success_count = len(results['success'])
    failure_count = len(results['failure'])
    
    results['summary'] = {
        'total': total,
        'success': success_count,
        'failure': failure_count
    }
    
    logger.info(f"批量下载完成: 总计{total}, 成功{success_count}, 失败{failure_count}")
