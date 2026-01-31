from typing import Dict, Any, Optional
from exceptions import CustomException, CustomError
from src.utils.logger import logger
import requests

# 常量定义
POINTS_API_BASE_URL = "https://jcaigc.cn/openapi/v1/user/points"
API_HEADERS = {
    'User-Agent': 'CapcutMate/1.0',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

def get_user_points(api_key: str) -> float:
    """
    根据API Key获取用户积分
    
    Args:
        api_key: 用户的API Key
    
    Returns:
        float: 用户当前积分
    
    Raises:
        CustomException: 当获取积分失败时
    """
    try:
        # 调用获取积分API
        params = {'apiKey': api_key}
        result = _call_user_api('GET', '', params=params)
        
        # 检查响应码并处理结果
        code = result.get('code', -1)
        
        if code == 0:
            points = _extract_points_from_response(result)
            logger.info(f"Successfully retrieved user points: {points} for API key: {api_key[:8]}***")
            return points
        elif code == 10007:  # API Key无效
            logger.error(f"Invalid API key, result: {result}, code: {code}")
            raise CustomException(CustomError.INVALID_APIKEY, detail=f"{api_key}")
        else:
            logger.error(f"Failed to get user points: {result}, code: {code}")
            raise CustomException(CustomError.UNKNOWN_ERROR, detail=f"Unknown error occurred while getting user points: {result}, code: {code}")
            
    except CustomException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting user points for API key {api_key[:8]}***: {str(e)}")
        raise CustomException(CustomError.UNKNOWN_ERROR, detail=f"Unknown error occurred while getting user points: {str(e)}")


def deduct_user_points(api_key: str, points: float, desc: str) -> bool:
    """
    根据API Key减少用户积分
    
    Args:
        api_key: 用户的API Key
        points: 要减少的积分数量（必须为正数）
        desc: 减少积分的原因描述
    
    Returns:
        bool: True表示扣减成功，False表示失败
    Raises:
        CustomException: 仅当apiKey无效时抛出异常
    """
    try:
        # 调用扣减积分API
        json_data = {
            'apiKey': api_key,
            'points': float(points),
            'desc': desc.strip()
        }
        
        result = _call_user_api('POST', '/deduct', json_data=json_data)
        code = result.get('code', -1)
        
        if code == 0:
            logger.info(f"Successfully deducted {points} points for API key {api_key[:8]}***, reason: {desc}")
            return True
        elif code == 10007:  # API Key无效
            logger.error(f"Invalid API key for deduct points: {result}, code: {code}")
            raise CustomException(CustomError.INVALID_APIKEY, detail=f"{api_key}")
        else:
            logger.error(f"Failed to deduct points: {result}, code: {code}")
            return False
    except CustomException as e:
        logger.warning(f"Deduct points failed, API key: {api_key[:8]}***, error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error deducting points for API key {api_key[:8]}***: {str(e)}")
        return False


def _extract_points_from_response(result: Dict[str, Any]) -> float:
    """
    从响应中提取积分数据
    
    Args:
        result: API响应数据
    
    Returns:
        float: 积分值
    
    Raises:
        CustomException: 积分数据格式错误时
    """
    try:
        points = result.get('data', {}).get('points', 0.0)
        return float(points)
    except (ValueError, TypeError):
        logger.error(f"Invalid points format in API response, result: {result}")
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR, detail="Points format error")


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

def _call_user_api(method: str, endpoint: str, params: Optional[dict] = None, json_data: Optional[dict] = None, timeout: int = DEFAULT_API_TIMEOUT) -> Dict[str, Any]:
    """
    调用用户积分相关API的通用方法
    
    Args:
        method: HTTP方法 ('GET' 或 'POST')
        endpoint: API端点路径
        params: 查询参数（用于GET请求）
        json_data: JSON数据（用于POST请求）
        timeout: 请求超时时间（秒）
    
    Returns:
        Dict[str, Any]: API响应的JSON数据
    
    Raises:
        CustomException: 当API调用失败或返回错误时
    """
    url = f"{POINTS_API_BASE_URL}{endpoint}"
    
    try:
        logger.info(f"Calling user API: {method} {url}")
        
        # 根据方法类型发送请求
        if method.upper() == 'GET':
            response = requests.get(url, params=params, headers=API_HEADERS, timeout=timeout)
        elif method.upper() == 'POST':
            response = requests.post(url, json=json_data, headers=API_HEADERS, timeout=timeout)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        
        # 解析JSON响应
        return _parse_api_response(response)
        
    except requests.exceptions.Timeout:
        logger.error(f"User API timeout: {method} {url}")
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR, detail="User API call timeout")
    except requests.exceptions.ConnectionError:
        logger.error(f"User API connection error: {method} {url}")
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR, detail="Unable to connect to user API service")
    except requests.exceptions.RequestException as e:
        logger.error(f"User API request failed: {method} {url}, error: {str(e)}")
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR, detail=f"User API request failed: {str(e)}")
    except CustomException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in user API call: {method} {url}, error: {str(e)}")
        raise CustomException(CustomError.UNKNOWN_ERROR, detail=f"Unknown error occurred while calling user API: {str(e)}")
