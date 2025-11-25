from urllib.parse import urlparse, parse_qs
import os
import requests
import mimetypes
import datetime
import uuid
from pathlib import Path
from src.utils.logger import logger
from exceptions import CustomException, CustomError


def get_url_param(url: str, key: str, default=None):
    """
    从 URL 中提取指定查询参数的值（返回第一个值）。
    若参数不存在，返回 default。
    """
    query = parse_qs(urlparse(url).query)
    return query.get(key, [default])[0]

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