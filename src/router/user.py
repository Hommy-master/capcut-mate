from fastapi import APIRouter, HTTPException, status
from src.schemas.user import User, UserCreate, UserUpdate
from src.service.user import (
    get_user
)

router = APIRouter()

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int):
    """获取单个用户详情"""
    user = get_user(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

