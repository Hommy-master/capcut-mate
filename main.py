from fastapi import FastAPI
from src.router import router

app = FastAPI(
    title="CapCut Mate API", 
    version="1.0"
)

# 注册路由
app.include_router(router.router, prefix="/openapi", tags=["capcut-mate"])