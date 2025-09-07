from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import CustomError, CustomException
from src.utils.logger import logger
import json


async def response_middleware(request: Request, call_next):
    """统一响应处理中间件
    功能：
    1. 统一处理业务正常响应，添加code和message字段
    2. 统一处理异常，返回标准错误格式
    """
    try:
        # 获取语言偏好（默认中文）
        lang = request.headers.get('Accept-Language', 'zh').split(',')[0].split('-')[0]
        if lang not in ['zh', 'en']:
            lang = 'zh'
        
        # 调用下一个处理函数
        response = await call_next(request)
        
        # 检查是否为JSON响应
        if response.headers.get('content-type') == 'application/json':
            # 读取响应内容
            body = [section async for section in response.body_iterator]
            if body:
                body_str = b''.join(body).decode()
                try:
                    # 解析JSON响应
                    data = json.loads(body_str)
                    
                    # 检查响应是否已经包含code和message
                    if 'code' not in data or 'message' not in data:
                        # 包装成统一响应格式（平铺业务数据）
                        unified_response = {
                            'code': CustomError.SUCCESS.code,
                            'message': CustomError.SUCCESS.as_dict(language=lang)['message'],
                            **data
                        }
                        
                        # 创建新的JSON响应
                        return JSONResponse(
                            status_code=response.status_code,
                            content=unified_response
                        )
                except json.JSONDecodeError:
                    logger.warning(f"JSON decode error: {body_str}")
            
        return response
        
    except CustomException as e:
        # 处理自定义业务异常
        logger.error(f"Custom exception: {e.err.code} - {e.err.message}" + (f" ({e.detail})" if e.detail else ""))
        return JSONResponse(
            status_code=200,
            content=e.err.as_dict(e.detail, language=lang)
        )
    except Exception as e:
        # 处理其他未捕获的异常
        logger.error(f"Internal server error: {str(e)}")
        return JSONResponse(
            status_code=200,
            content=CustomError.INTERNAL_SERVER_ERROR.as_dict(str(e), language=lang)
        )