# 环境初始化中间件
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import config
import os


class PrepareMiddleware(BaseHTTPMiddleware):
    """请求前的准备工作中间件
    功能：
    1. 创建临时目录
    2. 创建输出目录
    """

    async def dispatch(self, request: Request, call_next):
        # 递归创建目录，如果目录存在，就直接跳过创建
        os.makedirs(config.DRAFT_DIR, exist_ok=True)
        os.makedirs(config.TEMP_DIR, exist_ok=True)

        # 继续处理请求
        response = await call_next(request)
        return response