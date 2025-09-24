from src.utils.logger import logger
from src.utils.video_task_manager import task_manager
from exceptions import CustomException, CustomError
from typing import Tuple


def gen_video(draft_url: str) -> str:
    """
    提交视频生成任务（异步处理）
    
    Args:
        draft_url: 草稿URL
    
    Returns:
        message: 响应消息
    """
    logger.info(f"gen_video called with draft_url: {draft_url}")
    
    try:
        # 提交任务到队列
        task_manager.submit_task(draft_url)
        
        logger.info(f"Video generation task submitted for draft_url: {draft_url}")
        return "视频生成任务已提交，请使用draft_url查询进度"
        
    except ValueError as e:
        logger.error(f"Invalid draft_url: {draft_url}, error: {e}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)
    except Exception as e:
        logger.error(f"Submit video generation task failed: {e}")
        raise CustomException(CustomError.VIDEO_GENERATION_SUBMIT_FAILED)


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
        status_info = task_manager.get_task_status(draft_url)
        
        if status_info is None:
            logger.warning(f"No task found for draft_url: {draft_url}")
            raise CustomException(CustomError.VIDEO_TASK_NOT_FOUND)
        
        logger.info(f"Task status retrieved for draft_url: {draft_url}, status={status_info['status']}")
        return status_info
        
    except CustomException:
        raise
    except Exception as e:
        logger.error(f"Get video generation status failed: {e}")
        raise CustomException(CustomError.VIDEO_STATUS_QUERY_FAILED)
