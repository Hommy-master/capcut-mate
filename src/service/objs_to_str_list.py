from src.utils.logger import logger
from exceptions import CustomException, CustomError
from typing import List, Dict, Any


def objs_to_str_list(outputs: List[Dict[str, Any]]) -> List[str]:
    """
    对象列表转化成字符串列表的业务逻辑
    
    Args:
        outputs: 数据对象列表
        
    Returns:
        List[str]: 字符串列表
        
    Raises:
        CustomException: 转换失败
    """
    logger.info(f"objs_to_str_list starting, outputs count: {len(outputs)}")
    
    try:
        # 将对象列表中的output字段提取出来组成字符串列表
        result = []
        for obj in outputs:
            result.append(obj.get("output", ""))
        
        logger.info(f"objs_to_str_list completed successfully, result count: {len(result)}")
        return result
    except Exception as e:
        logger.error(f"objs_to_str_list failed: {str(e)}")
        raise CustomException(CustomError.UNKNOWN_ERROR)