from enum import Enum

# 自定义错误码
class CustomError(Enum):
    """错误码枚举类（支持中英文）"""
    
    # ===== 基础错误码 (1000-1999) =====
    SUCCESS = (0, "成功", "Success")
    PARAM_VALIDATION_FAILED = (1001, "参数校验失败", "Parameter validation failed")
    RESOURCE_NOT_FOUND = (1002, "资源不存在", "Resource not found")
    PERMISSION_DENIED = (1003, "权限不足", "Permission denied")
    AUTHENTICATION_FAILED = (1004, "认证失败", "Authentication failed")
    
    # ===== 业务错误码 (2000-2999) =====
    INVALID_DRAFT_URL = (2001, "无效的草稿URL", "Invalid draft URL")
    DRAFT_CREATE_FAILED = (2002, "草稿创建失败", "Draft creation failed")
    INVALID_VIDEO_INFO = (2003, "无效的视频信息，请检查video_infos字段值是否正确", "Invalid video information, please check if the value of the video_infos field is correct.")
    FILE_SIZE_LIMIT_EXCEEDED = (2004, "文件大小超出限制", "File size exceeds the limit")
    DOWNLOAD_FILE_FAILED = (2005, "下载文件失败", "Download file failed")
    VIDEO_ADD_FAILED = (2006, "视频添加失败", "Video addition failed")
    INVALID_AUDIO_INFO = (2007, "无效的音频信息，请检查audio_infos字段值是否正确", "Invalid audio information, please check if the value of the audio_infos field is correct.")
    AUDIO_ADD_FAILED = (2008, "音频添加失败", "Audio addition failed")

    # ===== 系统错误码 (9000-9999) =====
    INTERNAL_SERVER_ERROR = (9998, "系统内部错误", "Internal server error")
    UNKNOWN_ERROR = (9999, "未知异常", "Unknown error")

    def __init__(self, code: int, cn_message: str, en_message: str) -> None:
        self.code = code
        self.cn_message = cn_message
        self.en_message = en_message

    def as_dict(self, detail: str = "", lang: str = 'zh') -> dict:
        """转换为API响应格式，支持中英文"""
        message = self.cn_message if lang == 'zh' else self.en_message
        if detail:
            message += f"({detail})"
        return {"code": self.code, "message": message}


# 自定义异常类
class CustomException(Exception):
    """自定义业务异常类"""
    def __init__(self, err: CustomError, detail: str = "") -> None:
        self.err = err
        self.detail = detail
        super().__init__(err.cn_message)
