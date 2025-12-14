from src.utils.logger import logger
from exceptions import CustomException, CustomError
import re


def get_url(output: str) -> str:
    """
    提取链接的业务逻辑
    
    Args:
        output: 提取内容
        
    Returns:
        str: 提取结果
        
    Raises:
        CustomException: 提取失败
    """
    logger.info(f"get_url starting, output: {output}")
    
    try:
        # 直接返回输入的内容，不做任何处理
        # 根据需求描述，这个接口的作用是"用于多值返回变成单值返回"
        # 在实际应用中，这里可能会有一些处理逻辑
        result = output
        
        logger.info(f"get_url completed successfully, result: {result}")
        return result
    except Exception as e:
        logger.error(f"get_url failed: {str(e)}")
        raise CustomException(CustomError.UNKNOWN_ERROR)