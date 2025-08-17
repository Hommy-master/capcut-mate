from fastapi import APIRouter

router = APIRouter()

@router.get("/hello", operation_id="say_hello")
def hello():
    """
    打招呼
    """

    return {"message": "Hello, CapCut Mate!"}


@router.get("/", operation_id="capcut_mate")
async def root():
    """
    产品介绍，返回欢迎信息
    """
    return {"message": "Welcome to CapCut Mate API"}
