import os
import asyncio
from fastapi import FastAPI, Request
from src.middlewares import init_env_middleware
from src.customException.setttings import DRAFT_DIR

# 创建测试应用
app = FastAPI()

# 注册中间件
app.middleware("http")(init_env_middleware)

# 测试路由
@app.get("/")
async def test(request: Request):
    return {
        "message": "测试成功",
        "draft_dir": os.environ.get("DRAFT_DIR"),
        "today_draft_dir": os.environ.get("TODAY_DRAFT_DIR"),
        "dir_exists": os.path.exists(DRAFT_DIR)
    }

# 运行测试
if __name__ == "__main__":
    import uvicorn
    print("启动测试服务器...")
    print(f"草稿目录: {DRAFT_DIR}")
    uvicorn.run(app, host="0.0.0.0", port=8000)