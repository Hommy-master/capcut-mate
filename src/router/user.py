from fastapi import APIRouter, HTTPException, status
from src.schemas.user import User, UserCreate, UserUpdate
from src.service.user import (
    create_user,
    get_user,
    get_users,
    update_user,
    delete_user
)

router = APIRouter()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate):
    """创建新用户"""
    return create_user(user=user)

@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100):
    """获取用户列表"""
    users = get_users(skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int):
    """获取单个用户详情"""
    user = get_user(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
def update_existing_user(user_id: int, user: UserUpdate):
    """更新用户信息"""
    updated_user = update_user(user_id=user_id, user=user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_user(user_id: int):
    """删除用户"""
    success = delete_user(user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None
