from fastapi import FastAPI
from src.router import v1_router
from src.utils.draft_downloader import download_draft
from src.utils.logger import logger
from src.middlewares import PrepareMiddleware, ResponseMiddleware, TraceContextMiddleware


# 1. 创建 FastAPI 应用
app: FastAPI = FastAPI(title="CapCut Mate API", version="1.0")

# 2. 注册路由
app.include_router(router=v1_router, prefix="/openapi/capcut-mate", tags=["capcut-mate"])

# 3. 添加中间件（最后注册的 TraceContextMiddleware 最先处理请求，用于 W3C trace_id）
app.add_middleware(middleware_class=PrepareMiddleware)
app.add_middleware(middleware_class=ResponseMiddleware)
app.add_middleware(middleware_class=TraceContextMiddleware)

# 4. 打印所有路由
for r in app.routes:
    # 1. 取 HTTP 方法列表
    methods = getattr(r, "methods", None) or [getattr(r, "method", "WS")]
    # 2. 安全地取路径
    path = getattr(r, "path", "<unknown>")
    # 3. 安全地取函数名
    name = getattr(r, "name", "<unnamed>")
    logger.info("Route: %s %s -> %s", ",".join(sorted(methods)), path, name)

logger.info("CapCut Mate API")

# 5. 启动
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=30000, log_config=None, log_level="info")