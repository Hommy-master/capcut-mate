# 环境初始化中间件
from fastapi import Request
import config
import os
from datetime import datetime


# 请求前的准备工作，如：创建草稿目录
async def prepare_middleware(request: Request, call_next):
    # 递归创建目录，如果目录存在，就直接跳过创建
    os.makedirs(config.DRAFT_DIR, exist_ok=True)

    # 继续处理请求
    response = await call_next(request)
    return response