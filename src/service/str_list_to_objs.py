from src.utils.logger import logger
from exceptions import CustomException, CustomError
from typing import List, Dict, Any


def str_list_to_objs(infos: List[str]) -> List[Dict[str, Any]]:
    """
    字符串列表转化成对象列表的业务逻辑
    
    Args:
        infos: 字符串列表
        
    Returns:
        List[Dict[str, Any]]: 对象列表
        
    Raises:
        CustomException: 转换失败
    """
    logger.info(f"str_list_to_objs starting, infos: {infos}")
    
    try:
        # 将字符串列表转换为对象列表
        result = []
        for info in infos:
            result.append({"output": info})
        
        logger.info(f"str_list_to_objs completed successfully, result count: {len(result)}")
        return result
    except Exception as e:
        logger.error(f"str_list_to_objs failed: {str(e)}")
        raise CustomException(CustomError.UNKNOWN_ERROR)