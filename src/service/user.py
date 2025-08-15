from datetime import datetime
from passlib.context import CryptContext
from src.schemas.user import UserCreate, UserUpdate, UserInDB, User

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 内存存储
fake_db = {}

def get_user(user_id: int):
    """获取用户"""
    db_user = fake_db.get(user_id)
    if db_user:
        return User(** db_user.model_dump())
    return None
