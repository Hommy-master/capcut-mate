"""
草稿下载工具
用于从API下载草稿文件并保存到指定目录
"""
import os
import re
import json
import time
import mimetypes
import requests
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict, Any, List
from src.utils.logger import logger
import config
import subprocess
import os

_REQUEST_CONNECT_TIMEOUT = 10
_REQUEST_READ_TIMEOUT = 30
_MAX_RETRIES = 5

# 网关/限流等暂时不可用，退避重试有效（与 desktop-client 一致；不含 500 等持久故障）
_RETRYABLE_TRANSIENT_HTTP_STATUSES = frozenset({408, 429, 502, 503, 504})
_TRANSIENT_HTTP_BACKOFF_MAX_SECONDS = 30
_DEFAULT_NETWORK_RETRY_DELAY_SECONDS = 1.0

_NON_RETRYABLE_NETWORK_MARKERS = (
    "name or service not known",
    "getaddrinfo failed",
    "nodename nor servname provided",
    "connection refused",
    "failed to establish a new connection",
)


def _is_retryable_http_status(status_code: int) -> bool:
    return status_code in _RETRYABLE_TRANSIENT_HTTP_STATUSES


def _is_retryable_request_exception(exc: requests.exceptions.RequestException) -> bool:
    if isinstance(
        exc,
        (requests.exceptions.Timeout, requests.exceptions.ChunkedEncodingError),
    ):
        return True
    if isinstance(exc, requests.exceptions.ConnectionError):
        msg = str(exc).lower()
        if any(marker in msg for marker in _NON_RETRYABLE_NETWORK_MARKERS):
            return False
        return True
    return False


def _parse_retry_after_seconds(headers) -> Optional[float]:
    raw = headers.get("Retry-After") or headers.get("retry-after")
    if raw is None or raw == "":
        return None
    try:
        seconds = int(raw)
        if seconds >= 0:
            return min(float(seconds), _TRANSIENT_HTTP_BACKOFF_MAX_SECONDS)
    except (TypeError, ValueError):
        pass
    try:
        from email.utils import parsedate_to_datetime
        from datetime import datetime, timezone

        retry_at = parsedate_to_datetime(str(raw))
        if retry_at.tzinfo is None:
            retry_at = retry_at.replace(tzinfo=timezone.utc)
        delta = (retry_at - datetime.now(timezone.utc)).total_seconds()
        return min(max(0.0, delta), _TRANSIENT_HTTP_BACKOFF_MAX_SECONDS)
    except (TypeError, ValueError, OverflowError):
        return None
    return None


def _sleep_transient_http_backoff(
    retry_no: int, response: Optional[requests.Response] = None
) -> None:
    """限流/网关错误退避：优先 Retry-After，否则 1s 起指数增长，上限 30s。"""
    if response is not None:
        delay = _parse_retry_after_seconds(response.headers)
        if delay is not None:
            time.sleep(delay)
            return
    time.sleep(min(2 ** (retry_no - 1), _TRANSIENT_HTTP_BACKOFF_MAX_SECONDS))


def _sleep_network_retry_backoff() -> None:
    time.sleep(_DEFAULT_NETWORK_RETRY_DELAY_SECONDS)


def safe_write_file(file_path: str, file_content: bytes, is_binary: bool = True):
    """
    安全写入文件，使用 O_EXCL 标志确保原子创建
    
    Args:
        file_path: 文件路径
        file_content: 文件内容
        is_binary: 是否为二进制内容
    """
    # 使用 O_EXCL 标志确保原子创建
    if is_binary:
        flags = os.O_CREAT | os.O_EXCL | os.O_RDWR | getattr(os, "O_BINARY", 0)
    else:
        flags = os.O_CREAT | os.O_EXCL | os.O_RDWR
    
    try:
        fd = os.open(file_path, flags)
        
        # 写入内容
        if file_content:
            if isinstance(file_content, str):
                os.write(fd, file_content.encode('utf-8'))
            else:
                os.write(fd, file_content)
        
        # 强制同步到磁盘
        os.fsync(fd)
        
        os.close(fd)
    except FileExistsError:
        # 如果文件已存在，先删除再重新创建
        if os.path.exists(file_path):
            os.remove(file_path)
        fd = os.open(file_path, flags)
        
        # 写入内容
        if file_content:
            if isinstance(file_content, str):
                os.write(fd, file_content.encode('utf-8'))
            else:
                os.write(fd, file_content)
        
        # 强制同步到磁盘
        os.fsync(fd)
        
        os.close(fd)


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
        logger.error(f"Failed to parse URL: {url}, error: {e}")
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
        logger.error(f"Cannot extract draft_id from URL: {draft_url}")
        return False
    
    # 设置保存路径
    if save_path is None:
        save_path = config.DRAFT_SAVE_PATH
    
    # 构建并创建目标目录
    target_dir = prepare_target_directory(save_path, draft_id)
    
    logger.info(f"Downloading draft {draft_id} to {target_dir}")
    
    # 获取草稿文件列表
    files = get_draft_files_list(draft_url)
    if not files:
        logger.error(f"Cannot get draft file list: {draft_id}")
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
    for attempt in range(_MAX_RETRIES + 1):
        try:
            response = requests.get(
                draft_url,
                timeout=(_REQUEST_CONNECT_TIMEOUT, _REQUEST_READ_TIMEOUT),
            )

            if response.status_code != 200:
                if (
                    _is_retryable_http_status(response.status_code)
                    and attempt < _MAX_RETRIES
                ):
                    retry_no = attempt + 1
                    logger.warning(
                        "Transient HTTP %s while fetching draft file list, retry (%s/%s)",
                        response.status_code,
                        retry_no,
                        _MAX_RETRIES,
                    )
                    response.close()
                    _sleep_transient_http_backoff(retry_no, response)
                    continue
                logger.error(
                    f"Failed to get draft file list, HTTP status: {response.status_code}"
                )
                response.close()
                return []

            # 解析JSON响应
            try:
                json_data = response.json()
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse draft list JSON: {e}")
                return []

            # 检查响应状态
            if json_data.get('code') != 0:
                logger.error(
                    f"Failed to get draft file list: {json_data.get('message', 'unknown error')}"
                )
                return []

            # 返回files列表
            files = json_data.get('files', [])
            logger.info(f"Fetched {len(files)} draft file(s)")
            return files
        except requests.exceptions.RequestException as e:
            if not _is_retryable_request_exception(e) or attempt >= _MAX_RETRIES:
                if attempt >= _MAX_RETRIES:
                    logger.error(
                        f"Network error while fetching draft file list after {_MAX_RETRIES} retries: {e}"
                    )
                else:
                    logger.error(
                        f"Network error while fetching draft file list is not retryable: {e}"
                    )
                return []

            retry_no = attempt + 1
            logger.warning(
                f"Network error while fetching draft file list, retry ({retry_no}/{_MAX_RETRIES}): {e}"
            )
            _sleep_network_retry_backoff()
        except Exception as e:
            logger.error(f"Unexpected error while fetching draft file list: {e}")
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
            logger.error(f"Failed to download file: {file_url}")

    trigger_directory_scan_with_robocopy(target_dir)
    
    logger.info(
        f"Draft {draft_id} download finished: total={total_files}, "
        f"ok={success_count}, failed={total_files - success_count}"
    )
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
    max_retries = 5
    retry_count = 0

    # 仅从 URL 解析目标路径，避免请求挂起时无效等待；与原先路径规则一致
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.split("/")
    url_draft_id = None
    for part in path_parts:
        if re.match(r"^\d{8,}.*$", part) and len(part) >= 10:
            url_draft_id = part
            break
    draft_id_index = -1
    if url_draft_id:
        for i, part in enumerate(path_parts):
            if url_draft_id in part:
                draft_id_index = i
                break
    if draft_id_index != -1:
        rel_path_parts = path_parts[draft_id_index + 1:]
        rel_path = os.path.join(*rel_path_parts)
    else:
        rel_path = os.path.join(*path_parts[1:])
    full_file_path = os.path.join(target_dir, rel_path)

    while retry_count <= max_retries:
        try:
            response = requests.get(
                file_url,
                timeout=(_REQUEST_CONNECT_TIMEOUT, _REQUEST_READ_TIMEOUT),
                stream=True,
            )
            try:
                if response.status_code != 200:
                    if not _is_retryable_http_status(response.status_code):
                        logger.error(
                            "Download failed (HTTP %s, not retryable), URL: %s",
                            response.status_code,
                            file_url,
                        )
                        return False
                    retry_count += 1
                    if retry_count > max_retries:
                        logger.error(
                            "Transient HTTP %s, download failed after %s retries, URL: %s",
                            response.status_code,
                            max_retries,
                            file_url,
                        )
                        return False
                    logger.warning(
                        "Transient HTTP %s, retry (%s/%s), URL: %s",
                        response.status_code,
                        retry_count,
                        max_retries,
                        file_url,
                    )
                    _sleep_transient_http_backoff(retry_count, response)
                    continue

                parent_dir = os.path.dirname(full_file_path)
                if parent_dir:
                    os.makedirs(parent_dir, exist_ok=True)

                with open(full_file_path, "wb") as out:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            out.write(chunk)
            finally:
                response.close()

            # draft_info / draft_content：路径重写与 URL 素材本地化；失败则本文件下载失败
            if full_file_path.endswith(("draft_info.json", "draft_content.json")):
                if not update_json_file_paths(full_file_path, target_dir, url_draft_id):
                    return False

            return True

        except requests.exceptions.RequestException as e:
            if not _is_retryable_request_exception(e):
                logger.error(
                    f"Network error is not retryable: {e}, URL: {file_url}"
                )
                return False
            retry_count += 1
            if retry_count > max_retries:
                logger.error(
                    f"Network error, download failed after {max_retries} retries: {e}, URL: {file_url}"
                )
                return False
            logger.warning(
                f"Network error, retry ({retry_count}/{max_retries}): {e}, URL: {file_url}"
            )
            _sleep_network_retry_backoff()
        except OSError as e:
            logger.error(f"File write error, download failed: {e}, URL: {file_url}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error while downloading file: {e}, URL: {file_url}")
            return False


def update_json_file_paths(json_file_path: str, target_dir: str, draft_id: str) -> bool:
    """将服务端路径前缀换成本地，并下载 materials 中的 URL 素材；失败返回 False。"""
    try:
        # 读取JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 构造替换路径
        remote_prefix = f"/app/output/draft/{draft_id}/"
        local_prefix = os.path.join(config.DRAFT_SAVE_PATH, draft_id).replace('/', os.sep) + os.sep
        
        # 更新数据中的路径（服务端草稿内本地路径 -> 客户端目标路径）
        updated_data = update_material_paths(data, remote_prefix, local_prefix)

        # materials 中仍为 URL 的 path：下载到本地并回写；任一失败则整稿失败且不写回
        if not localize_remote_material_paths(updated_data, target_dir):
            logger.error(
                f"Remote material localization failed after retries; skip JSON update: {json_file_path}"
            )
            return False

        # 写回 JSON
        json_content = json.dumps(updated_data, ensure_ascii=False, indent=2)
        safe_write_file(json_file_path, json_content, is_binary=False)
        
        logger.debug(f"Updated paths in JSON file: {json_file_path}")
        return True
    
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}, file: {json_file_path}")
        return False
    except Exception as e:
        logger.error(f"Failed to update JSON paths: {e}, file: {json_file_path}")
        return False


def update_material_paths(data, remote_prefix: str, local_prefix: str):
    """
    更新材料路径，处理JSON中materials下的音频和视频路径
    
    Args:
        data: JSON数据
        remote_prefix: 远程路径前缀
        local_prefix: 本地路径前缀
        
    Returns:
        更新后的数据
    """
    if isinstance(data, dict):
        # 检查是否是materials结构
        if 'materials' in data:
            materials = data.get('materials', {})
            if isinstance(materials, dict):
                # 处理音频和视频路径
                audios = materials.get('audios', [])
                videos = materials.get('videos', [])
                
                # 更新音频路径
                for audio in audios:
                    if isinstance(audio, dict) and 'path' in audio:
                        audio['path'] = update_single_path(audio['path'], remote_prefix, local_prefix)
                
                # 更新视频路径
                for video in videos:
                    if isinstance(video, dict) and 'path' in video:
                        video['path'] = update_single_path(video['path'], remote_prefix, local_prefix)

        # 递归处理其他键值
        updated_dict = {}
        for key, value in data.items():
            updated_dict[key] = update_material_paths(value, remote_prefix, local_prefix)
        return updated_dict
    elif isinstance(data, list):
        # 处理列表中的每个元素
        return [update_material_paths(item, remote_prefix, local_prefix) for item in data]
    elif isinstance(data, str):
        # 检查是否是以远程路径开头的路径
        if data.startswith(remote_prefix):
            # 提取远程前缀后的相对路径部分
            relative_path = data[len(remote_prefix):]
            # 将相对路径部分从Linux风格转换为Windows风格
            relative_path_windows = relative_path.replace('/', os.sep)
            # 组合成本地路径
            new_path = local_prefix + relative_path_windows
            # 验证文件是否存在
            if not os.path.exists(new_path):
                logger.warning(f"File missing after path rewrite: {new_path}")
            return new_path
        return data
    else:
        # 其他类型的数据保持不变
        return data


def update_single_path(path: str, remote_prefix: str, local_prefix: str) -> str:
    """
    更新单个路径值
    
    Args:
        path: 原始路径
        remote_prefix: 远程路径前缀
        local_prefix: 本地路径前缀
        
    Returns:
        更新后的路径
    """
    if isinstance(path, str) and path.startswith(remote_prefix):
        # 提取远程前缀后的相对路径部分
        relative_path = path[len(remote_prefix):]
        # 将相对路径部分从Linux风格转换为Windows风格
        relative_path_windows = relative_path.replace('/', os.sep)
        # 组合成本地路径
        new_path = local_prefix + relative_path_windows
        return new_path
    return path


def _is_http_url(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def _safe_name(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]+', "_", name).strip(" .") or "material"


def _infer_local_subdir(material_type: str, material: Dict[str, Any]) -> str:
    if material_type == "audios":
        return "audios"
    if material_type == "videos":
        return "images" if material.get("type") == "photo" else "videos"
    return "misc"


_CONTENT_TYPE_EXT_OVERRIDES = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/bmp": ".bmp",
    "video/mp4": ".mp4",
    "video/quicktime": ".mov",
    "audio/mpeg": ".mp3",
    "audio/mp3": ".mp3",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
}


_GENERIC_MIME_TYPES = frozenset({
    "application/octet-stream",
    "binary/octet-stream",
})


def _infer_ext_from_content_type(content_type: Optional[str], fallback: str) -> str:
    if not content_type:
        return fallback
    mime = content_type.split(";")[0].strip().lower()
    if mime in _GENERIC_MIME_TYPES:
        return fallback
    ext = _CONTENT_TYPE_EXT_OVERRIDES.get(mime) or mimetypes.guess_extension(mime)
    if ext == ".jpe":
        ext = ".jpg"
    return ext or fallback


def _build_material_filename(base_name: str, ext: str) -> str:
    return base_name if base_name.lower().endswith(ext.lower()) else f"{base_name}{ext}"


def _download_remote_material(
    file_url: str,
    target_dir: str,
    sub_dir: str,
    base_name: str,
    fallback_ext: str,
) -> Optional[str]:
    """下载 URL 素材，根据响应 Content-Type 确定扩展名并保存到本地。"""
    for attempt in range(_MAX_RETRIES + 1):
        response = None
        try:
            response = requests.get(
                file_url,
                timeout=(_REQUEST_CONNECT_TIMEOUT, _REQUEST_READ_TIMEOUT),
                stream=True,
            )
            if response.status_code != 200:
                if not _is_retryable_http_status(response.status_code):
                    logger.error(
                        f"Remote material download failed (HTTP {response.status_code}), "
                        f"not retryable: {file_url}"
                    )
                    return None
                if attempt >= _MAX_RETRIES:
                    logger.error(
                        f"Remote material download failed (HTTP {response.status_code}) "
                        f"after {_MAX_RETRIES} retries: {file_url}"
                    )
                    return None
                retry_no = attempt + 1
                logger.warning(
                    f"Remote material download transient HTTP {response.status_code}, "
                    f"retry ({retry_no}/{_MAX_RETRIES}): {file_url}"
                )
                _sleep_transient_http_backoff(retry_no, response)
                response.close()
                continue

            ext = _infer_ext_from_content_type(
                response.headers.get("Content-Type"), fallback_ext
            )
            filename = _build_material_filename(base_name, ext)
            local_path = os.path.join(target_dir, "assets", sub_dir, filename)

            parent_dir = os.path.dirname(local_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return local_path
        except requests.exceptions.RequestException as e:
            if not _is_retryable_request_exception(e):
                logger.error(
                    f"Remote material download failed, not retryable: {file_url}, error: {e}"
                )
                return None
            if attempt >= _MAX_RETRIES:
                logger.error(
                    f"Remote material download failed after {_MAX_RETRIES} retries: {file_url}, error: {e}"
                )
                return None
            retry_no = attempt + 1
            logger.warning(
                f"Remote material download network error, retry ({retry_no}/{_MAX_RETRIES}): "
                f"{file_url}, {e}"
            )
            _sleep_network_retry_backoff()
        except OSError as e:
            logger.error(f"Failed to write remote material to disk: {file_url}, {e}")
            return None
        finally:
            if response is not None:
                response.close()
    return None


def _download_remote_file(file_url: str, local_path: str) -> bool:
    """下载单个 URL 素材；网络异常或非 200 时最多重试 _MAX_RETRIES 次。"""
    for attempt in range(_MAX_RETRIES + 1):
        try:
            response = requests.get(
                file_url,
                timeout=(_REQUEST_CONNECT_TIMEOUT, _REQUEST_READ_TIMEOUT),
                stream=True,
            )
            if response.status_code != 200:
                if not _is_retryable_http_status(response.status_code):
                    logger.error(
                        f"Remote material download failed (HTTP {response.status_code}), "
                        f"not retryable: {file_url}"
                    )
                    return False
                if attempt >= _MAX_RETRIES:
                    logger.error(
                        f"Remote material download failed (HTTP {response.status_code}) "
                        f"after {_MAX_RETRIES} retries: {file_url}"
                    )
                    return False
                retry_no = attempt + 1
                logger.warning(
                    f"Remote material download transient HTTP {response.status_code}, "
                    f"retry ({retry_no}/{_MAX_RETRIES}): {file_url}"
                )
                _sleep_transient_http_backoff(retry_no, response)
                response.close()
                continue

            parent_dir = os.path.dirname(local_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return True
        except requests.exceptions.RequestException as e:
            if not _is_retryable_request_exception(e):
                logger.error(
                    f"Remote material download failed, not retryable: {file_url}, error: {e}"
                )
                return False
            if attempt >= _MAX_RETRIES:
                logger.error(
                    f"Remote material download failed after {_MAX_RETRIES} retries: {file_url}, error: {e}"
                )
                return False
            retry_no = attempt + 1
            logger.warning(
                f"Remote material download network error, retry ({retry_no}/{_MAX_RETRIES}): "
                f"{file_url}, {e}"
            )
            _sleep_network_retry_backoff()
        except OSError as e:
            logger.error(f"Failed to write remote material to disk: {local_path}, {e}")
            return False
    return False


def localize_remote_material_paths(data: Dict[str, Any], target_dir: str) -> bool:
    """
    将 materials 里仍为 URL 的 path 下载到本地并回写。
    同一 URL 只拉取一次；任一 URL 重试仍失败则返回 False，且不写 JSON（由上层中止下载与导出）。
    """
    materials = data.get("materials", {}) if isinstance(data, dict) else {}
    if not isinstance(materials, dict):
        return True

    url_cache: Dict[str, str] = {}
    failed_urls: set = set()
    target_lists: Dict[str, List[Dict[str, Any]]] = {
        "audios": materials.get("audios", []),
        "videos": materials.get("videos", []),
    }

    for material_type, items in target_lists.items():
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            remote_path = item.get("path")
            if not _is_http_url(remote_path):
                continue

            if remote_path in failed_urls:
                continue

            if remote_path in url_cache:
                item["path"] = url_cache[remote_path]
                continue

            sub_dir = _infer_local_subdir(material_type, item)
            fallback_ext = ".mp3" if material_type == "audios" else ".mp4"
            base_name = _safe_name(str(item.get("material_name") or item.get("name") or item.get("id") or "material"))

            local_path = _download_remote_material(
                remote_path, target_dir, sub_dir, base_name, fallback_ext
            )
            if not local_path:
                failed_urls.add(remote_path)
                logger.error(
                    f"Remote material localization failed (draft download will fail): {remote_path}"
                )
                continue

            logger.info(f"Remote material saved and path updated: {remote_path} -> {local_path}")
            item["path"] = local_path
            url_cache[remote_path] = local_path

    return len(failed_urls) == 0

def trigger_directory_scan_with_robocopy(target_dir: str):
    """
    使用robocopy触发目录扫描，专门用于激活剪映的目录发现机制
    
    Args:
        target_dir: 目录路径
    """
    if target_dir and os.path.exists(target_dir):
        # 使用robocopy复制目录以触发剪映的目录扫描机制
        copy_with_robocopy(target_dir, target_dir + ".tmp")
        # 清理临时目录
        tmp_dir = target_dir + ".tmp"
        if os.path.exists(tmp_dir):
            try:
                import shutil
                shutil.rmtree(tmp_dir)
            except Exception as e:
                logger.warning(f"Failed to remove temp directory {tmp_dir}: {e}")

def copy_with_robocopy(src: str, dst: str, verbose: bool = False) -> bool:
    """
    使用robocopy复制目录，参数已验证可用
    
    参数:
        src: 源目录路径
        dst: 目标目录路径
        verbose: 是否显示详细输出，默认为False
    
    返回:
        成功返回True，失败返回False
    
    robocopy参数说明:
        /E: 复制所有子目录，包括空目录（递归复制）
        /COPY:DAT: 复制数据、属性和时间戳（无需管理员权限）
        /R:1: 失败重试1次
        /W:1: 重试等待1秒
        /NP: 不显示进度百分比（静默模式）
        /NJH: 不显示作业头（静默模式）
        /NJS: 不显示作业摘要（静默模式）
    """
    
    # 确保路径是字符串类型
    src = str(src)
    dst = str(dst)
    
    # 检查源目录是否存在
    if not os.path.exists(src):
        logger.error(f"Source directory does not exist - {src}")
        return False
    
    # 构建robocopy命令 - 使用已验证的参数组合
    cmd = [
        "robocopy",
        src,
        dst,
        "/E",          # 递归复制所有子目录
        "/COPY:DAT",   # 复制数据、属性和时间戳（无需管理员权限）
        "/R:1",        # 失败重试1次
        "/W:1",        # 重试等待1秒
        "/NP",         # 不显示进度百分比
        "/NJH",        # 不显示作业头
        "/NJS",        # 不显示作业摘要
    ]
    
    if verbose:
        logger.info(f"Executing command: {' '.join(cmd)}")
        # 在verbose模式下，不添加静默参数，以便看到输出
        cmd = cmd[:-3]  # 移除/NP, /NJH, /NJS参数
    
    try:
        if verbose:
            # 详细模式下，实时输出结果
            logger.info(f"Starting copy: {src} → {dst}")
            logger.info("-" * 50)
            
            result = subprocess.run(
                cmd, 
                capture_output=False,  # 实时显示输出
                text=True, 
                check=False,
                encoding='gbk'  # Windows命令行通常使用GBK编码
            )
            
            # 获取返回码
            return_code = result.returncode
            
            logger.info("-" * 50)
        else:
            # 静默模式下，捕获输出但不显示
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=False,
                encoding='gbk'
            )
            return_code = result.returncode
            
            # 即使静默模式，如果出错也要显示错误
            if return_code >= 8:
                logger.error(f"Copy failed! Return code: {return_code}")
                if result.stderr:
                    logger.error(f"Error message: {result.stderr}")
                elif result.stdout:
                    logger.error(f"Output message: {result.stdout}")
        
        # robocopy返回码处理:
        # 0-7: 成功或部分成功（0=无变化，1-7=有文件操作）
        # 8+: 严重错误
        if return_code <= 7:
            if verbose:
                logger.info(f"Copy completed! Return code: {return_code}")
                if return_code == 0:
                    logger.info("Return code 0 means no files need to be copied (source and target are the same)")
                elif return_code == 1:
                    logger.info("Return code 1 means some files were successfully copied")
                elif return_code == 2:
                    logger.info("Return code 2 means some files were skipped (may be temporary files or inaccessible)")
                elif return_code == 3:
                    logger.info("Return code 3 means some files were copied and some were skipped")
            return True
        else:
            # 返回码8+表示有严重错误
            error_messages = {
                8: "Files/directories copy failed",
                9: "Parameter error",
                10: "Source directory does not exist or no access permission",
                11: "Target directory creation failed",
                12: "File is in use and cannot be copied",
                13: "Insufficient disk space",
                14: "Source is a file instead of a directory",
                15: "Target is a file instead of a directory",
                16: "General error"
            }
            
            error_msg = error_messages.get(return_code, f"Unknown error (return code: {return_code})")
            logger.error(f"Copy failed! {error_msg}")
            
            # 显示更多信息（如果有）
            if not verbose and result.stderr:
                logger.error(f"Detailed error: {result.stderr}")
                
            return False
            
    except FileNotFoundError:
        logger.error("Error: robocopy command not found. Please ensure running on Windows system.")
        logger.info("Hint: robocopy is a built-in tool for Windows Vista and later versions.")
        return False
    except Exception as e:
        logger.error(f"An unknown error occurred during execution: {e}")
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
        response = requests.get(
            draft_url,
            timeout=(_REQUEST_CONNECT_TIMEOUT, _REQUEST_READ_TIMEOUT),
            stream=True,
        )
        try:
            if response.status_code != 200:
                logger.error(f"Draft download failed: {draft_id}, HTTP status: {response.status_code}")
                return False

            file_path = get_file_path(response, target_dir, draft_id)

            parent_dir = os.path.dirname(file_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            with open(file_path, "wb") as out:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        out.write(chunk)

            logger.info(f"Draft downloaded: {file_path}")
            return True
        finally:
            response.close()

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error, draft download failed: {draft_id}, error: {e}")
        return False
    except IOError as e:
        logger.error(f"File write error, draft download failed: {draft_id}, error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error, draft download failed: {draft_id}, error: {e}")
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
        logger.info(f"Batch download succeeded: {draft_id}")
    else:
        results['failure'].append({'url': url, 'draft_id': draft_id})
        logger.error(f"Batch download failed: {draft_id or url}")


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
    
    logger.info(
        f"Batch download finished: total={total}, ok={success_count}, failed={failure_count}"
    )


