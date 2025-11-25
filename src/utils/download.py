import os
import requests
import mimetypes
import time
from typing import Dict, Any, Optional
from src.utils import helper
from src.utils.logger import logger
from exceptions import CustomException, CustomError

# 常量配置
DEFAULT_FILE_SIZE_LIMIT = 200 * 1024 * 1024  # 200MB
DEFAULT_DOWNLOAD_TIMEOUT = 90  # 总下载超时时间90秒（用户要求）
DEFAULT_CONNECT_TIMEOUT = 10  # 连接超时10秒，快速失败
DEFAULT_READ_TIMEOUT = 15  # 读取超时15秒，平衡稳定性和速度
DEFAULT_API_TIMEOUT = 30  # 30秒
DEFAULT_FFPROBE_TIMEOUT = 30  # 30秒
DEFAULT_RETRY_COUNT = 3  # 重试次数改为3次，在90秒内完成
CHUNK_SIZE = 32768  # 32KB，增加块大小提高效率
CHUNK_READ_TIMEOUT = 10  # 每个块的读取超时10秒，快速检测网络中断
CONNECTION_RETRY_DELAY = 1  # 连接重试间隔时间（秒）
MAX_RETRY_DELAY = 8  # 最大重试等待时间8秒，控制总时间
MIN_PARTIAL_SIZE = 1024  # 最小部分下载大小（字节），小于此尺寸不使用断点续传

# 网络质量评估阈值
NETWORK_GOOD_THRESHOLD = 0.5  # 0.5秒内响应认为网络良好
NETWORK_MEDIUM_THRESHOLD = 2.0  # 2秒内响应认为网络中等

# HTTP连接池配置
CONNECTION_POOL_SIZE = 3  # 连接池大小
CONNECTION_POOL_MAXSIZE = 5  # 连接池最大连接数

# HTTP请求头（优化网络稳定性）
DOWNLOAD_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',  # 支持压缩提高传输效率
    'Connection': 'keep-alive',  # 保持连接
    'Cache-Control': 'no-cache',  # 不使用缓存
    'Pragma': 'no-cache',  # 兼容性缓存控制
    'Keep-Alive': 'timeout=30, max=3'  # Keep-Alive配置
}

def download(url: str, save_dir: str, limit: int = DEFAULT_FILE_SIZE_LIMIT, 
            timeout: int = DEFAULT_DOWNLOAD_TIMEOUT, retry: int = DEFAULT_RETRY_COUNT) -> str:
    """
    下载文件并根据Content-Type判断文件类型，支持高度稳定的断点续传和智能重试机制
    
    Args:
        url: 文件的URL地址
        save_dir: 文件保存目录
        limit: 文件大小限制（字节），默认300MB
        timeout: 整体下载超时时间（秒），默认5分钟
        retry: 下载失败时的重试次数，默认5次
    
    Returns:
        str: 完整的文件路径

    Raises:
        CustomException: 下载失败时抛出异常
    """
    # 初始化下载环境
    download_context = _prepare_download_context(url, save_dir, timeout)
    
    # 执行带重试的下载流程
    return _execute_download_with_retry(download_context, limit, retry)

def cleanup_temp_file(temp_file_path: Optional[str]) -> None:
    """
    清理临时文件
    
    Args:
        temp_file_path: 临时文件路径，可能为None
    """
    if temp_file_path and os.path.exists(temp_file_path):
        try:
            os.remove(temp_file_path)
            logger.info(f"Temporary file removed: {temp_file_path}")
        except Exception as cleanup_error:
            logger.warning(f"Failed to cleanup temporary file {temp_file_path}: {cleanup_error}")

def _prepare_download_context(url: str, save_dir: str, timeout: int) -> dict:
    """
    准备下载上下文信息
    
    Args:
        url: 文件URL
        save_dir: 保存目录
        timeout: 超时时间
    
    Returns:
        dict: 下载上下文字典
    """
    # 生成唯一的文件路径
    base_filename = helper.gen_unique_id()
    temp_save_path = os.path.join(save_dir, base_filename)
    
    # 评估网络环境
    network_quality = _assess_network_quality(url)
    supports_range = _check_range_support_with_retry(url)
    
    logger.info(f"Preparing download environment - Network quality: {network_quality}, Range support: {supports_range}, URL: {url}")
    
    # 计算自适应超时参数
    adaptive_timeouts = _calculate_adaptive_timeouts(network_quality, timeout)
    
    return {
        'url': url,
        'save_path': temp_save_path,
        'network_quality': network_quality,
        'supports_range': supports_range,
        'timeouts': adaptive_timeouts
    }


def _execute_download_with_retry(context: dict, limit: int, retry: int) -> str:
    """
    执行带重试机制的下载流程
    
    Args:
        context: 下载上下文
        limit: 文件大小限制
        retry: 重试次数
    
    Returns:
        str: 下载成功的文件路径
        
    Raises:
        CustomException: 下载失败时抛出异常
    """
    url = context['url']
    temp_save_path = context['save_path']
    supports_range = context['supports_range']
    timeouts = context['timeouts']
    
    last_exception = None
    consecutive_failures = 0  # 连续失败计数器
    
    for attempt in range(retry + 1):  # 总共尝试 retry + 1 次
        try:
            logger.info(f"Starting download attempt {attempt + 1}/{retry + 1}, URL: {url}")
            
            # 检查断点续传条件
            resume_info = _check_resume_conditions(temp_save_path, supports_range, 
                                                 attempt, consecutive_failures)
            
            # 执行单次下载
            response = _execute_single_download(url, resume_info, timeouts)
            
            # 确定最终文件路径（首次下载时添加扩展名）
            if resume_info['existing_size'] == 0:
                temp_save_path = _determine_file_path_with_extension(response, temp_save_path)
                context['save_path'] = temp_save_path
            
            # 下载文件内容
            _download_file_with_enhanced_stability(
                response, temp_save_path, limit, url, timeouts, 
                resume_info['existing_size'], resume_info['use_resume']
            )
            
            # 验证下载完整性
            _validate_download_integrity_with_resume(response, temp_save_path, 
                                                   url, resume_info['use_resume'])
            
            logger.info(f"Download completed successfully, attempts: {attempt + 1}, file path: {temp_save_path}")
            return temp_save_path
            
        except Exception as e:
            last_exception = e
            consecutive_failures += 1
            
            # 处理下载异常
            if not _handle_download_exception(e, attempt, retry, temp_save_path, 
                                            supports_range, consecutive_failures, context):
                break  # 致命错误，停止重试
    
    # 所有重试都失败，抛出异常
    return _handle_final_failure(last_exception, url)


def _check_resume_conditions(save_path: str, supports_range: bool, 
                           attempt: int, consecutive_failures: int) -> dict:
    """
    检查断点续传条件
    
    Args:
        save_path: 保存路径
        supports_range: 是否支持范围请求
        attempt: 当前尝试次数
        consecutive_failures: 连续失败次数
    
    Returns:
        dict: 断点续传信息字典
    """
    existing_size = 0
    if os.path.exists(save_path):
        existing_size = os.path.getsize(save_path)
        logger.info(f"Found existing partial file: {save_path}, size: {existing_size} bytes")
    
    # 判断是否使用断点续传（增强条件判断）
    use_resume = (
        supports_range and 
        existing_size >= MIN_PARTIAL_SIZE and 
        attempt > 0 and
        consecutive_failures <= 2  # 连续失败不超过2次才使用断点续传
    )
    
    return {
        'existing_size': existing_size,
        'use_resume': use_resume
    }


def _execute_single_download(url: str, resume_info: dict, timeouts: dict) -> requests.Response:
    """
    执行单次下载操作
    
    Args:
        url: 文件URL
        resume_info: 断点续传信息
        timeouts: 超时配置
    
    Returns:
        requests.Response: HTTP响应对象
    """
    if resume_info['use_resume']:
        logger.info(f"Using resume download from byte {resume_info['existing_size']}")
        return _download_with_resume_enhanced(url, resume_info['existing_size'], timeouts)
    else:
        logger.info("Starting fresh download")
        return _download_fresh_enhanced(url, timeouts)


def _handle_download_exception(exception: Exception, attempt: int, retry: int, 
                             save_path: str, supports_range: bool, 
                             consecutive_failures: int, context: dict) -> bool:
    """
    处理下载异常
    
    Args:
        exception: 异常对象
        attempt: 当前尝试次数
        retry: 总重试次数
        save_path: 保存路径
        supports_range: 是否支持范围请求
        consecutive_failures: 连续失败次数
        context: 下载上下文
    
    Returns:
        bool: True表示可以继续重试，False表示应该停止
    """
    url = context['url']
    
    # 错误分类
    error_category = _classify_download_error(exception)
    
    # 致命错误直接停止
    if error_category == 'fatal':
        if os.path.exists(save_path):
            _safe_remove_file(save_path)
        logger.error(f"Fatal error encountered, stopping retry, URL: {url}, error: {str(exception)}")
        raise exception
    
    # 非最后一次尝试，继续重试
    if attempt < retry:
        logger.warning(f"Download attempt {attempt + 1} failed, URL: {url}, error: {str(exception)}, category: {error_category}")
        
        # 决定是否清理文件
        should_cleanup = _should_cleanup_on_error(error_category, supports_range, consecutive_failures)
        if should_cleanup and os.path.exists(save_path):
            _safe_remove_file(save_path)
            logger.debug(f"Cleaned up partial download file: {save_path}")
        
        # 执行重试等待
        _execute_retry_wait(attempt, error_category, consecutive_failures, context)
        return True
    else:
        logger.error(f"All retry attempts failed, URL: {url}, final error: {str(exception)}")
        if os.path.exists(save_path):
            _safe_remove_file(save_path)
        return False


def _execute_retry_wait(attempt: int, error_category: str, consecutive_failures: int, context: dict) -> None:
    """
    执行重试等待逻辑
    
    Args:
        attempt: 当前尝试次数
        error_category: 错误类型
        consecutive_failures: 连续失败次数
        context: 下载上下文
    """
    # 计算等待时间
    wait_time = _calculate_retry_delay(attempt, error_category, consecutive_failures)
    logger.info(f"Waiting {wait_time} seconds before retry...")
    time.sleep(wait_time)
    
    # 网络错误后重新评估网络质量
    if error_category == 'network':
        url = context['url']
        network_quality = _assess_network_quality(url)
        context['timeouts'] = _calculate_adaptive_timeouts(network_quality, 
                                                          context['timeouts']['total_timeout'])
        logger.info(f"Re-assessed network quality: {network_quality}")


def _handle_final_failure(last_exception: Optional[Exception], url: str) -> str:
    """
    处理最终失败情况
    
    Args:
        last_exception: 最后一次异常（可能为None）
        url: 文件URL
    
    Raises:
        CustomException: 总是抛出异常
    """
    if last_exception and isinstance(last_exception, CustomException):
        raise last_exception
    
    error_detail = str(last_exception) if last_exception else "Unknown error"
    logger.error(f"All retries failed, URL: {url}, last error: {error_detail}")
    raise CustomException(CustomError.DOWNLOAD_FILE_FAILED)


def _determine_file_path_with_extension(response: requests.Response, save_path: str) -> str:
    """
    根据HTTP响应的Content-Type确定文件路径和扩展名
    
    Args:
        response: HTTP响应对象
        save_path: 原始保存路径
    
    Returns:
        str: 带扩展名的文件路径
    """
    content_type = response.headers.get('Content-Type', '').split(';')[0].strip()
    extension = mimetypes.guess_extension(content_type)
    
    if extension:
        return save_path + extension
    return save_path

def _parse_api_response(response: requests.Response) -> Dict[str, Any]:
    """
    解析API响应的JSON数据
    
    Args:
        response: HTTP响应对象
    
    Returns:
        Dict[str, Any]: 解析后的JSON数据
    
    Raises:
        CustomException: JSON解析失败时
    """
    try:
        return response.json()
    except ValueError:
        logger.error(f"Failed to parse API response as JSON: {response.text}")
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR, detail="API response format error")

def _validate_download_integrity_with_resume(
    response: requests.Response, 
    save_path: str, 
    url: str, 
    is_resume: bool = False
) -> None:
    """
    验证下载文件的完整性（支持断点续传）
    
    Args:
        response: HTTP响应对象
        save_path: 文件保存路径
        url: 文件URL（用于日志）
        is_resume: 是否为断点续传
    
    Raises:
        CustomException: 文件不完整时抛出
    """
    actual_size = os.path.getsize(save_path)
    
    if is_resume:
        # 断点续传时，检查Content-Range头
        content_range = response.headers.get('Content-Range')
        if content_range:
            # Content-Range: bytes 1024-2047/2048
            try:
                range_info = content_range.split('/')[-1]
                if range_info != '*':
                    expected_total_size = int(range_info)
                    if actual_size != expected_total_size:
                        os.remove(save_path)
                        logger.warning(
                            f"Resume download failed, url: {url}, "
                            f"error: File download incomplete: expected {expected_total_size} bytes, "
                            f"actual {actual_size} bytes"
                        )
                        raise CustomException(CustomError.DOWNLOAD_FILE_FAILED)
            except (ValueError, IndexError) as e:
                logger.warning(f"Failed to parse Content-Range header: {content_range}, error: {e}")
    else:
        # 全新下载时，检查Content-Length头
        content_length = response.headers.get('Content-Length')
        if content_length:
            expected_size = int(content_length)
            if actual_size != expected_size:
                os.remove(save_path)
                logger.warning(
                    f"Download failed, url: {url}, "
                    f"error: File download incomplete: expected {expected_size} bytes, "
                    f"actual {actual_size} bytes"
                )
                raise CustomException(CustomError.DOWNLOAD_FILE_FAILED)


def _safe_remove_file(file_path: str) -> None:
    """
    安全删除文件，忽略删除错误
    
    Args:
        file_path: 要删除的文件路径
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"Successfully removed file: {file_path}")
    except Exception as e:
        logger.warning(f"Failed to remove file {file_path}: {e}")


def _assess_network_quality(url: str) -> str:
    """
    评估网络质量（优化版）
    
    Args:
        url: 测试URL
    
    Returns:
        str: 网络质量 ('good', 'medium', 'poor')
    """
    try:
        import urllib.parse
        parsed_url = urllib.parse.urlparse(url)
        test_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        start_time = time.time()
        # 使用较短的超时时间快速测试
        response = requests.head(
            test_url,
            timeout=(3, 5),  # 更短的超时测试
            headers={'User-Agent': DOWNLOAD_HEADERS['User-Agent']},
            allow_redirects=True
        )
        response_time = time.time() - start_time
        
        # 根据响应时间判断网络质量
        if response_time < NETWORK_GOOD_THRESHOLD:
            logger.debug(f"Network quality: good ({response_time:.2f}s)")
            return 'good'
        elif response_time < NETWORK_MEDIUM_THRESHOLD:
            logger.debug(f"Network quality: medium ({response_time:.2f}s)")
            return 'medium'
        else:
            logger.debug(f"Network quality: poor ({response_time:.2f}s)")
            return 'poor'
            
    except Exception as e:
        logger.warning(f"Failed to assess network quality: {e}")
        return 'poor'  # 默认为较差的网络环境


def _check_range_support_with_retry(url: str, max_retries: int = 2) -> bool:
    """
    带重试的范围请求支持检测
    
    Args:
        url: 文件URL
        max_retries: 最大重试次数
    
    Returns:
        bool: 是否支持Range请求
    """
    for attempt in range(max_retries + 1):
        try:
            response = requests.head(
                url, 
                timeout=(DEFAULT_CONNECT_TIMEOUT, DEFAULT_READ_TIMEOUT),
                headers=DOWNLOAD_HEADERS
            )
            response.raise_for_status()
            
            accept_ranges = response.headers.get('Accept-Ranges', '').lower()
            supports_ranges = accept_ranges == 'bytes'
            
            logger.info(f"Range support check attempt {attempt + 1}: Accept-Ranges={accept_ranges}, supports={supports_ranges}")
            return supports_ranges
            
        except Exception as e:
            if attempt < max_retries:
                logger.warning(f"Range support check attempt {attempt + 1} failed: {e}, retrying...")
                time.sleep(1)
            else:
                logger.warning(f"Failed to check range support after {max_retries + 1} attempts: {e}")
                return False
    
    return False


def _calculate_adaptive_timeouts(network_quality: str, base_timeout: int) -> dict:
    """
    根据网络质量计算自适应超时参数（优化版）
    
    Args:
        network_quality: 网络质量 ('good', 'medium', 'poor')
        base_timeout: 基础超时时间
    
    Returns:
        dict: 超时参数字典
    """
    if network_quality == 'good':
        # 网络良好，使用较短超时
        connect_multiplier = 0.8
        read_multiplier = 0.8
        chunk_multiplier = 0.7
    elif network_quality == 'medium':
        # 网络中等，使用默认超时
        connect_multiplier = 1.0
        read_multiplier = 1.0
        chunk_multiplier = 1.0
    else:  # poor
        # 网络较差，适度增加超时但不过大
        connect_multiplier = 1.3
        read_multiplier = 1.2
        chunk_multiplier = 1.5
    
    return {
        'connect_timeout': max(5, int(DEFAULT_CONNECT_TIMEOUT * connect_multiplier)),
        'read_timeout': max(8, int(DEFAULT_READ_TIMEOUT * read_multiplier)),
        'total_timeout': base_timeout,  # 保持90秒限制
        'chunk_timeout': max(5, int(CHUNK_READ_TIMEOUT * chunk_multiplier))
    }


def _create_optimized_session() -> requests.Session:
    """
    创建优化的requests session，支持连接池和重试
    
    Returns:
        requests.Session: 配置好的session对象
    """
    session = requests.Session()
    
    # 设置重试适配器
    from urllib3.util.retry import Retry
    from requests.adapters import HTTPAdapter
    
    # 配置重试策略
    retry_strategy = Retry(
        total=0,  # 在session层级不做重试，由外层控制
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD"],
        raise_on_status=False
    )
    
    # 设置连接池
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=CONNECTION_POOL_SIZE,
        pool_maxsize=CONNECTION_POOL_MAXSIZE,
        pool_block=False
    )
    
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session


def _download_with_resume_enhanced(url: str, resume_pos: int, timeouts: dict) -> requests.Response:
    """
    增强版的断点续传下载（优化HTTP协议）
    
    Args:
        url: 文件URL
        resume_pos: 断点续传的起始位置
        timeouts: 超时参数字典
    
    Returns:
        requests.Response: HTTP响应对象
    """
    headers = DOWNLOAD_HEADERS.copy()
    headers['Range'] = f'bytes={resume_pos}-'
    
    # 使用优化的session
    session = _create_optimized_session()
    session.headers.update(headers)
    
    # 快速重试机制（2次尝试）
    for attempt in range(2):
        try:
            logger.debug(f"Resume download attempt {attempt + 1}, position: {resume_pos}")
            response = session.get(
                url,
                stream=True,
                timeout=(timeouts['connect_timeout'], timeouts['read_timeout'])
            )
            
            if response.status_code == 206:
                logger.info(f"Resume download successful, status: {response.status_code}")
                return response
            elif response.status_code == 200:
                logger.warning("Server returned 200 instead of 206, treating as fresh download")
                return response
            else:
                response.raise_for_status()
                
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt < 1:
                logger.warning(f"Resume download attempt {attempt + 1} failed: {e}, retrying...")
                time.sleep(CONNECTION_RETRY_DELAY)
            else:
                logger.error(f"Resume download failed after {attempt + 1} attempts: {e}")
                raise
        except Exception as e:
            logger.error(f"Resume download unexpected error: {e}")
            raise
    
    raise requests.exceptions.RequestException("Failed to establish resume connection after retries")


def _download_fresh_enhanced(url: str, timeouts: dict) -> requests.Response:
    """
    增强版的全新下载（优化HTTP协议）
    
    Args:
        url: 文件URL
        timeouts: 超时参数字典
    
    Returns:
        requests.Response: HTTP响应对象
    """
    # 使用优化的session
    session = _create_optimized_session()
    session.headers.update(DOWNLOAD_HEADERS)
    
    # 快速重试机制（2次尝试）
    for attempt in range(2):
        try:
            logger.debug(f"Fresh download attempt {attempt + 1}")
            response = session.get(
                url,
                stream=True,
                timeout=(timeouts['connect_timeout'], timeouts['read_timeout'])
            )
            response.raise_for_status()
            logger.info(f"Fresh download successful, status: {response.status_code}")
            return response
            
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt < 1:
                logger.warning(f"Fresh download attempt {attempt + 1} failed: {e}, retrying...")
                time.sleep(CONNECTION_RETRY_DELAY)
            else:
                logger.error(f"Fresh download failed after {attempt + 1} attempts: {e}")
                raise
        except Exception as e:
            logger.error(f"Fresh download unexpected error: {e}")
            raise
    
    raise requests.exceptions.RequestException("Failed to establish fresh connection after retries")


def _download_file_with_enhanced_stability(
    response: requests.Response, 
    save_path: str, 
    limit: int, 
    url: str, 
    timeouts: dict,
    existing_size: int = 0,
    is_resume: bool = False
) -> None:
    """
    增强稳定性的文件下载（优化版）
    
    Args:
        response: HTTP响应对象
        save_path: 文件保存路径
        limit: 文件大小限制
        url: 文件URL
        timeouts: 超时参数字典
        existing_size: 已存在的文件大小
        is_resume: 是否为断点续传
    """
    downloaded_size = existing_size
    start_time = time.time()
    last_chunk_time = start_time
    last_progress_time = start_time
    stall_count = 0  # 停滞计数器
    
    file_mode = 'ab' if is_resume else 'wb'
    
    try:
        with open(save_path, file_mode) as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                current_time = time.time()
                
                # 检查总体超时（严格90秒限制）
                if current_time - start_time > timeouts['total_timeout']:
                    logger.error(f"Download total timeout: {current_time - start_time:.1f}s > {timeouts['total_timeout']}s")
                    raise CustomException(
                        CustomError.DOWNLOAD_FILE_TIMEOUT, 
                        detail=f"Download timeout, total time {current_time - start_time:.1f}s"
                    )
                
                # 检查单个块的读取超时（网络停滞检测）
                chunk_interval = current_time - last_chunk_time
                if chunk_interval > timeouts['chunk_timeout']:
                    stall_count += 1
                    logger.warning(f"Network stall detected: {chunk_interval:.1f}s, count: {stall_count}")
                    
                    # 连续停滞超过阈值则抛出异常
                    if stall_count >= 3:
                        raise CustomException(
                            CustomError.DOWNLOAD_FILE_FAILED, 
                            detail=f"Network connection unstable, multiple stalls detected"
                        )
                
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    last_chunk_time = current_time
                    
                    # 重置停滞计数器
                    if len(chunk) > 0:
                        stall_count = 0
                    
                    # 检查文件大小是否超过限制
                    if downloaded_size > limit:
                        raise CustomException(
                            CustomError.FILE_SIZE_LIMIT_EXCEEDED, 
                            detail=f"{limit / 1024 / 1024:.2f} MB"
                        )
                    
                    # 更频繁的进度日志（15秒间隔）
                    if current_time - last_progress_time >= 15:
                        progress_percent = (downloaded_size / limit) * 100 if limit > 0 else 0
                        speed_mbps = (downloaded_size - existing_size) / (current_time - start_time) / 1024 / 1024
                        logger.info(
                            f"Download progress: {downloaded_size / 1024 / 1024:.1f}MB "
                            f"({progress_percent:.1f}%), speed: {speed_mbps:.2f}MB/s, URL: {url[:50]}..."
                        )
                        last_progress_time = current_time
                        
    except requests.exceptions.ChunkedEncodingError as e:
        raise CustomException(
            CustomError.DOWNLOAD_FILE_FAILED, 
            detail=f"Data transfer error: {str(e)}"
        )
    except Exception as e:
        if isinstance(e, CustomException):
            raise e
        raise CustomException(
            CustomError.DOWNLOAD_FILE_FAILED, 
            detail=f"Error occurred during download: {str(e)}"
        )


def _classify_download_error(error: Exception) -> str:
    """
    分类下载错误类型
    
    Args:
        error: 异常对象
    
    Returns:
        str: 错误类型 ('network', 'server', 'fatal', 'unknown')
    """
    if isinstance(error, CustomException):
        if error.err == CustomError.FILE_SIZE_LIMIT_EXCEEDED:
            return 'fatal'
        elif error.err == CustomError.DOWNLOAD_FILE_TIMEOUT:
            return 'network'
        else:
            return 'server'
    
    if isinstance(error, (requests.exceptions.ConnectionError, 
                         requests.exceptions.Timeout,
                         requests.exceptions.ChunkedEncodingError)):
        return 'network'
    
    if isinstance(error, requests.exceptions.HTTPError):
        status_code = getattr(error.response, 'status_code', None)
        if status_code in [500, 502, 503, 504]:  # 服务器错误
            return 'server'
        elif status_code in [404, 403, 401]:  # 客户端错误
            return 'fatal'
        else:
            return 'server'
    
    return 'unknown'


def _should_cleanup_on_error(error_category: str, supports_range: bool, consecutive_failures: int) -> bool:
    """
    决定错误后是否清理文件
    
    Args:
        error_category: 错误类型
        supports_range: 是否支持断点续传
        consecutive_failures: 连续失败次数
    
    Returns:
        bool: 是否应该清理文件
    """
    # 致命错误始终清理
    if error_category == 'fatal':
        return True
    
    # 不支持断点续传时清理
    if not supports_range:
        return True
    
    # 连续失败太多次时清理（可能是文件损坏）
    if consecutive_failures >= 3:
        return True
    
    # 网络和服务器错误保留文件
    return False


def _calculate_retry_delay(attempt: int, error_category: str, consecutive_failures: int) -> int:
    """
    计算重试等待时间（优化版，控制总时间在90秒内）
    
    Args:
        attempt: 当前尝试次数
        error_category: 错误类型
        consecutive_failures: 连续失败次数
    
    Returns:
        int: 等待时间（秒）
    """
    # 更短的基础等待时间，确保90秒内完成
    base_delays = [1, 2, 4]  # 递增延迟
    base_delay = base_delays[min(attempt, len(base_delays) - 1)]
    
    # 根据错误类型调整（幅度更小）
    if error_category == 'network':
        # 网络错误需要稍微更长的等待时间
        multiplier = 1.2
    elif error_category == 'server':
        # 服务器错误稍微等待
        multiplier = 1.1
    else:
        multiplier = 1.0
    
    # 连续失败次数调整（幅度更小）
    if consecutive_failures >= 2:
        multiplier *= 1.1
    
    final_delay = min(int(base_delay * multiplier), MAX_RETRY_DELAY)
    return max(final_delay, 1)  # 最少等待1秒