from fastapi import FastAPI
from src.router import v1_router
from src.utils.logger import logger
from src import middlewares
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request, status
from src.constants.errcode import ErrCode


# 0. 创建 FastAPI 应用
app = FastAPI(title="CapCut Mate API", version="1.0")

# 1. 注册路由
app.include_router(v1_router, prefix="/openapi", tags=["capcut-mate"])

# 2. 添加中间件
app.middleware("http")(middlewares.prepare_middleware)

# 3. 异常处理：参数校验错误
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """自定义参数校验错误处理器"""
    # 1. 拼接完整错误信息
    error_messages = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        error_type = error["type"]
        error_msg = error["msg"]
        # 组合字段+错误类型+详情信息
        error_messages.append(f"{field} ({error_type}): {error_msg}")
    
    # 2. 构建统一响应结构
    full_message = "; ".join(error_messages)  # 用分号分隔多个错误
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ErrCode.PARAM_VALIDATION_FAILED.as_dict(full_message)
    )

# 异常处理：其它异常
@app.exception_handler(Exception)
async def handle_errors(request, exc):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ErrCode.INTERNAL_SERVER_ERROR.as_dict()
    )

# 4. 打印所有路由
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