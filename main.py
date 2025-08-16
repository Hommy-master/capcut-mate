from fastapi import FastAPI
from src.router import router
from src.utils.logger import logger

app = FastAPI(
    title="CapCut Mate API", 
    version="1.0"
)

if __name__ == "__main__":
    # 设置路由
    app.include_router(router.router, prefix="/openapi", tags=["capcut-mate"])
   
    logger.info("CapCut Mate API started")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=60000, log_config=None)  # 禁用 uvicorn 默认日志
