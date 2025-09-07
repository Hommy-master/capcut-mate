from enum import Enum

# 自定义错误码
class CustomError(Enum):
    """错误码枚举类（符合Python 3.4+标准）"""
    
    # ===== 基础错误码 (1000-1999) =====
    SUCCESS = (0, "成功")
    PARAM_VALIDATION_FAILED = (1001, "参数校验失败")
    RESOURCE_NOT_FOUND = (1002, "资源不存在")
    PERMISSION_DENIED = (1003, "权限不足")
    AUTHENTICATION_FAILED = (1004, "认证失败")
    
    # ===== 业务错误码 (2000-2999) =====
    INVALID_DRAFT_URL = (2001, "无效的草稿URL")
    DRAFT_CREATE_FAILED = (2002, "草稿创建失败")
    
    # ===== 系统错误码 (9000-9999) =====
    INTERNAL_SERVER_ERROR = (9998, "系统内部错误")
    UNKNOWN_ERROR = (9999, "未知异常")

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def as_dict(self, detail: str = None) -> dict:
        """转换为API响应格式"""
        return {"code": self.code, "message": self.message + f"({detail})"} if detail else {"code": self.code, "message": self.message}


# 自定义异常类
class CustomException(Exception):
    """自定义业务异常类"""
    def __init__(self, err: CustomError, detail: str = None):
        self.err = err
        self.detail = detail
        super().__init__(err.message)
