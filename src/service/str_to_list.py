from src.utils.logger import logger
from exceptions import CustomException, CustomError
from typing import List
import json


def str_to_list(obj: str) -> List[str]:
    """
    字符转列表的业务逻辑
    
    Args:
        obj: 对象内容（JSON字符串）
        
    Returns:
        List[str]: 字符串列表
        
    Raises:
        CustomException: 转换失败
    """
    logger.info(f"str_to_list starting, obj: {obj}")
    
    try:
        # 将输入的字符串作为单个元素返回到列表中
        # 根据需求描述，这里是将整个输入字符串作为一个元素返回
        result = [obj]
        
        logger.info(f"str_to_list completed successfully, result count: {len(result)}")
        return result
    except Exception as e:
        logger.error(f"str_to_list failed: {str(e)}")
        raise CustomException(CustomError.UNKNOWN_ERROR)