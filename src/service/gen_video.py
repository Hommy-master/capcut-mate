from src.utils.logger import logger
from src.utils.video_task_manager import task_manager
from src.utils.points import get_user_points
from exceptions import CustomException, CustomError
from typing import Tuple
import config


def gen_video(draft_url: str, apiKey: str = None) -> str:
    """
    提交视频生成任务（异步处理）
    
    Args:
        draft_url: 草稿URL
        apiKey: 可选的API密钥，必须是合法的UUID格式，可以为空
    
    Returns:
        message: 响应消息
    """
    logger.info(f"gen_video called with draft_url: {draft_url}, apiKey provided: {apiKey is not None}")
    
    try:
        if config.ENABLE_APIKEY == "true":
            if apiKey == "": # 开启API密钥验证
                raise CustomException(CustomError.INVALID_APIKEY)

            # 查询用户积分
            user_points = get_user_points(apiKey)
        
            # 检查积分是否足够（需要大于1）
            if user_points <= 1:
                logger.error(f"Insufficient account balance: {user_points} for API key: {apiKey[:8]}***")
                raise CustomException(CustomError.INSUFFICIENT_ACCOUNT_BALANCE)
        
        # 验证草稿URL格式
        validate_draft_url(draft_url)
        
        # 提交任务到队列
        task_manager.submit_task(draft_url)
        
        logger.info(f"Video generation task submitted for draft_url: {draft_url}")
        return "视频生成任务已提交，请使用draft_url查询进度"
        
    except CustomException as e:
        # 如果是自定义异常，直接抛出
        raise e
    except ValueError as e:
        logger.error(f"Invalid draft_url: {draft_url}, error: {e}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)
    except Exception as e:
        logger.error(f"Submit video generation task failed: {e}")
        # 如果get_user_points失败，也抛出系统内部错误
        raise CustomException(CustomError.INTERNAL_SERVER_ERROR)


def validate_draft_url(draft_url: str) -> None:
    """
    验证草稿URL格式是否有效
    
    Args:
        draft_url: 草稿URL
    
    Raises:
        ValueError: 当URL格式无效时
    """
    if not draft_url or not isinstance(draft_url, str):
        raise ValueError("草稿URL不能为空")
    
    draft_id = extract_draft_id_from_url(draft_url)
    if not draft_id:
        raise ValueError("无法从URL中提取draft_id")


def extract_draft_id_from_url(draft_url: str) -> str:
    """
    从草稿URL中提取draft_id
    
    Args:
        draft_url: 草稿URL
        
    Returns:
        draft_id: 草稿ID
    """
    from src.utils import helper
    return helper.get_url_param(draft_url, "draft_id")


def gen_video_status(draft_url: str) -> dict:
    """
    查询视频生成任务状态
    
    Args:
        draft_url: 草稿URL
    
    Returns:
        任务状态信息
    """
    logger.info(f"gen_video_status called with draft_url: {draft_url}")
    
    try:
        # 查询任务状态
        status_info = get_task_status_info(draft_url)
        
        logger.info(f"Task status retrieved for draft_url: {draft_url}, status={status_info['status']}")
        return status_info
        
    except CustomException:
        raise
    except Exception as e:
        logger.error(f"Get video generation status failed: {e}")
        raise CustomException(CustomError.VIDEO_STATUS_QUERY_FAILED)


def get_task_status_info(draft_url: str) -> dict:
    """
    获取任务状态信息
    
    Args:
        draft_url: 草稿URL
        
    Returns:
        任务状态信息
        
    Raises:
        CustomException: 当任务不存在时
    """
    status_info = task_manager.get_task_status(draft_url)
    
    if status_info is None:
        logger.warning(f"No task found for draft_url: {draft_url}")
        raise CustomException(CustomError.VIDEO_TASK_NOT_FOUND)
    
    return status_info
