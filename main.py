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
mcp.mount_http()   # 👈 推荐
mcp.mount_sse()  # 如果客户端只支持 SSE

logger.info("CapCut Mate API & MCP mounted")

# 4. 启动
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=60000, log_config=None)