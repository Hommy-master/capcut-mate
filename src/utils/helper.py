from urllib.parse import urlparse, parse_qs
import os
import requests
import mimetypes
import datetime
import uuid
from pathlib import Path
from src.utils.logger import logger


def get_url_param(url: str, key: str, default=None):
    """
    从 URL 中提取指定查询参数的值（返回第一个值）。
    若参数不存在，返回 default。
    """
    query = parse_qs(urlparse(url).query)
    return query.get(key, [default])[0]

def download(url, save_dir, filename, limit=512*1024*1024, timeout=180) -> str:
    """
    下载文件并根据Content-Type判断文件类型
    
    Args:
        url: 文件的URL地址
        save_dir: 文件保存目录
        filename: 文件名
        limit: 文件大小限制（字节），默认512MB
        timeout: 整体下载超时时间（秒），默认3分钟
    
    Returns:
        如果下载成功，则返回完整的文件路径，如果失败，则返回空字符串，并输出错误日志
    """
    save_path = os.path.join(save_dir, filename)
    
    try:
        # 1. 发送GET请求下载文件
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Referer': 'https://www.163.com/',  # 网易的Referer
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        response = requests.get(url, stream=True, timeout=timeout, headers=headers)
        response.raise_for_status()
        
        # 2. 获取Content-Type，判断文件类型
        content_type = response.headers.get('Content-Type', '').split(';')[0].strip()
        
        # 如果没有扩展名，则根据Content-Type猜测扩展名
        if '.' not in filename:
            extension = mimetypes.guess_extension(content_type)
            if extension:
                filename += extension
                # 更新保存路径
                save_path = os.path.join(save_dir, filename)

        # 3. 下载文件并实时检查大小
        downloaded_size = 0
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    
                    # 检查文件大小是否超过限制
                    if downloaded_size > limit:
                        # 删除部分下载的文件
                        f.close()
                        os.remove(save_path)
                        
                        logger.info(f"Download failed, url: {url}, error: File size exceeds the limit of {limit/1024/1024:.2f}MB")
                        return ""
        
        # 4. 验证下载完整性（如果服务器提供了Content-Length）
        content_length = response.headers.get('Content-Length')
        if content_length and os.path.getsize(save_path) != int(content_length):
            os.remove(save_path)
            logger.info(f"Download failed, url: {url}, error: File download incomplete: expected {content_length} bytes, actual {os.path.getsize(save_path)} bytes")
            return ""
        
        return save_path
    except Exception as e:
        # 清理可能已部分下载的文件
        if os.path.exists(save_path):
            os.remove(save_path)
        logger.info(f"Download failed, url: {url}, error: {str(e)}")
        return ""

def gen_unique_id() -> str:
    """
    生成唯一ID
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:8]

    return f"{timestamp}{unique_id}"

def get_all_files(dir: str) -> list:
    """
    使用 pathlib.Path.rglob() 递归获取目录下所有文件的路径列表。

    参数:
        dir (str): 要遍历的目录路径。

    返回:
        list: 包含所有文件完整路径的列表。
    """
    path_obj = Path(dir)
    
    # 检查目录是否存在
    if not path_obj.exists():
        return []
    
    # 使用 rglob('*') 递归匹配所有条目，并用 is_file() 过滤出文件
    file_list = [str(file_path) for file_path in path_obj.rglob('*') if file_path.is_file()]
    return file_list