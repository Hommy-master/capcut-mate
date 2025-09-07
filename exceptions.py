from enum import Enum

# 自定义错误码
class CustomError(Enum):
    """错误码枚举类（支持中英文）"""
    
    # ===== 基础错误码 (1000-1999) =====
    SUCCESS = (0, "成功", "success")
    PARAM_VALIDATION_FAILED = (1001, "参数校验失败", "Parameter validation failed")
    RESOURCE_NOT_FOUND = (1002, "资源不存在", "Resource not found")
    PERMISSION_DENIED = (1003, "权限不足", "Permission denied")
    AUTHENTICATION_FAILED = (1004, "认证失败", "Authentication failed")
    
    # ===== 业务错误码 (2000-2999) =====
    INVALID_DRAFT_URL = (2001, "无效的草稿URL", "Invalid draft URL")
    DRAFT_CREATE_FAILED = (2002, "草稿创建失败", "Draft creation failed")
    
    # ===== 系统错误码 (9000-9999) =====
    INTERNAL_SERVER_ERROR = (9998, "系统内部错误", "Internal server error")
    UNKNOWN_ERROR = (9999, "未知异常", "Unknown error")

    def __init__(self, code: int, cn_message: str, en_message: str):
        self.code = code
        self.cn_message = cn_message
        self.en_message = en_message

    def as_dict(self, detail: str = None, language: str = 'zh') -> dict:
        """转换为API响应格式，支持中英文"""
        message = self.cn_message if language == 'zh' else self.en_message
        if detail:
            message += f"({detail})"
        return {"code": self.code, "message": message}


# 自定义异常类
class CustomException(Exception):
    """自定义业务异常类"""
    def __init__(self, err: CustomError, detail: str = None):
        self.err = err
        self.detail = detail
        super().__init__(err.cn_message)
