from fastapi import FastAPI
from src.router import user as user_router

app = FastAPI(title="CapCut Mate API", version="1.0")

# 注册路由
app.include_router(user_router.router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to CapCut Mate API"}
