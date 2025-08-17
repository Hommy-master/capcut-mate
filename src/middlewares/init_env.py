# 环境初始化中间件
from fastapi import Request, Response
from src.constants.base import DRAFT_DIR
import os
import datetime


# 初始化环境变量中间件
async def init_env_middleware(request: Request, call_next):
    # 递归创建目录
    today_dir = os.path.join(DRAFT_DIR, datetime.now().strftime("%Y-%m-%d"))
    os.makedirs(today_dir, exist_ok=True)
    # 设置环境变量
    os.environ["DRAFT_DIR"] = DRAFT_DIR
    os.environ["TODAY_DRAFT_DIR"] = today_dir

    # 继续处理请求
    response = await call_next(request)
    return response






