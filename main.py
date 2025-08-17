from fastapi import FastAPI
from src.router import router
from src.utils.logger import logger
from src import middlewares

# 0. 创建 FastAPI 应用
app = FastAPI(title="CapCut Mate API", version="1.0")

# 1. 注册路由
app.include_router(router.router, prefix="/openapi", tags=["capcut-mate"])

# 2. 添加中间件
app.middleware("http")(middlewares.init_env_middleware)

# ---------- 打印所有路由 ----------
for r in app.routes:
    # 1. 取 HTTP 方法列表
    methods = getattr(r, "methods", None) or [getattr(r, "method", "WS")]
    # 2. 取路径
    path = r.path
    # 3. 取函数名
    name = r.name
    logger.info("Route: %s %s -> %s", ",".join(sorted(methods)), path, name)

logger.info("CapCut Mate API")

# 3. 启动
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=60000, log_config=None)