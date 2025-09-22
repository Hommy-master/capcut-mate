from fastapi import FastAPI
from src.router import v1_router
from src.utils.logger import logger
from src.middlewares import PrepareMiddleware, ResponseMiddleware


# 0. 创建 FastAPI 应用
app = FastAPI(title="CapCut Mate API", version="1.0")

# 1. 注册路由
app.include_router(v1_router, prefix="/openapi", tags=["capcut-mate"])

# 2. 添加中间件
app.add_middleware(PrepareMiddleware)
# 注册统一响应处理中间件（注意顺序，应该在其他中间件之后注册）
app.add_middleware(ResponseMiddleware)

# 3. 打印所有路由
for r in app.routes:
    # 1. 取 HTTP 方法列表
    methods = getattr(r, "methods", None) or [getattr(r, "method", "WS")]
    # 2. 取路径
    path = r.path
    # 3. 取函数名
    name = r.name
    logger.info("Route: %s %s -> %s", ",".join(sorted(methods)), path, name)

logger.info("CapCut Mate API")

# 5. 启动
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=60000, log_config=None, log_level="info")