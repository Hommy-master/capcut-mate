# 环境初始化中间件
from fastapi import Request, Response
from src.constants.base import DRAFT_DIR
import os
from datetime import datetime


# 请求前的准备工作，如：创建草稿目录
async def prepare_middleware(request: Request, call_next):
    # 递归创建目录
    draft_dir = os.path.join(DRAFT_DIR, datetime.now().strftime("%Y-%m-%d"))
    os.makedirs(draft_dir, exist_ok=True)

    # 将草稿目录传给下一个HTTP Handle
    request.state.draft_dir = draft_dir

    # 继续处理请求
    response = await call_next(request)
    return response






