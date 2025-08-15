from datetime import datetime
from passlib.context import CryptContext
from src.schemas.user import UserCreate, UserUpdate, UserInDB, User

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 内存存储
fake_db = {}
current_id = 1

def get_password_hash(password):
    """加密密码"""
    return pwd_context.hash(password)

def create_user(user: UserCreate):
    """创建用户"""
    global current_id
    hashed_password = get_password_hash(user.password)
    now = datetime.utcnow()
    
    db_user = UserInDB(
        id=current_id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        created_at=now,
        updated_at=now
    )
    
    fake_db[current_id] = db_user
    current_id += 1
    return User(**db_user.model_dump())

def get_user(user_id: int):
    """获取用户"""
    db_user = fake_db.get(user_id)
    if db_user:
        return User(** db_user.model_dump())
    return None

def get_users(skip: int = 0, limit: int = 100):
    """获取用户列表"""
    user_list = list(fake_db.values())[skip : skip + limit]
    return [User(**user.model_dump()) for user in user_list]

def update_user(user_id: int, user: UserUpdate):
    """更新用户"""
    db_user = fake_db.get(user_id)
    if not db_user:
        return None
    
    update_data = user.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    update_data["updated_at"] = datetime.utcnow()
    updated_user = db_user.model_copy(update=update_data)
    fake_db[user_id] = updated_user
    
    return User(** updated_user.model_dump())

def delete_user(user_id: int):
    """删除用户"""
    if user_id in fake_db:
        del fake_db[user_id]
        return True
    return False
