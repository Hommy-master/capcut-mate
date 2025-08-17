from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from src.router import router
from src.utils.logger import logger

app = FastAPI(title="CapCut Mate API", version="1.0")

# 1. 注册路由
app.include_router(router.router, prefix="/openapi", tags=["capcut-mate"])

# 2. 创建 MCP 实例
mcp = FastApiMCP(app)

# 3. 同时暴露两种端点（可选其一，也可两个都要）
mcp.mount_http() # 👈 推荐
mcp.mount_sse()  # 如果客户端只支持 SSE

# ---------- 打印所有路由 ----------
for r in app.routes:
    # 1. 取 HTTP 方法列表
    methods = getattr(r, "methods", None) or [getattr(r, "method", "WS")]
    # 2. 取路径
    path = r.path
    # 3. 取函数名
    name = r.name
    logger.info("Route: %s %s -> %s", ",".join(sorted(methods)), path, name)

logger.info("CapCut Mate API & MCP mounted")

# 4. 启动
if __name__ == "__main__":
    """
    参数：
    proxy_headers=True,
    forwarded_allow_ips="*",
    作用：解决反向代理后，后端在 http⇄https 之间死循环
    """
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=60000,
        log_config=None
    )