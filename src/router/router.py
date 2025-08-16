from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
def hello():
    return {"message": "Hello, CapCut Mate!"}


@router.get("/")
async def root():
    return {"message": "Welcome to CapCut Mate API"}
