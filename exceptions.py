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
    INVALID_IMAGE_INFO = (2009, "无效的图片信息，请检查image_infos字段值是否正确", "Invalid image information, please check if the value of the image_infos field is correct.")
    IMAGE_ADD_FAILED = (2010, "图片添加失败", "Image addition failed")
    INVALID_STICKER_INFO = (2011, "无效的贴纸信息，请检查贴纸参数是否正确", "Invalid sticker information, please check if sticker parameters are correct.")
    STICKER_ADD_FAILED = (2012, "贴纸添加失败", "Sticker addition failed")
    INVALID_KEYFRAME_INFO = (2013, "无效的关键帧信息，请检查keyframes字段值是否正确", "Invalid keyframe information, please check if the value of the keyframes field is correct.")
    KEYFRAME_ADD_FAILED = (2014, "关键帧添加失败", "Keyframe addition failed")
    SEGMENT_NOT_FOUND = (2015, "片段未找到，请检查segment_id是否正确", "Segment not found, please check if the segment_id is correct.")
    INVALID_SEGMENT_TYPE = (2016, "无效的片段类型，该片段不支持关键帧", "Invalid segment type, this segment does not support keyframes.")
    INVALID_KEYFRAME_PROPERTY = (2017, "无效的关键帧属性类型", "Invalid keyframe property type.")
    INVALID_CAPTION_INFO = (2018, "无效的字幕信息，请检查captions字段值是否正确", "Invalid caption information, please check if the value of the captions field is correct.")
    CAPTION_ADD_FAILED = (2019, "字幕添加失败", "Caption addition failed")
    INVALID_EFFECT_INFO = (2020, "无效的特效信息，请检查effect_infos字段值是否正确", "Invalid effect information, please check if the value of the effect_infos field is correct.")
    EFFECT_ADD_FAILED = (2021, "特效添加失败", "Effect addition failed")
    EFFECT_NOT_FOUND = (2022, "特效未找到，请检查特效名称是否正确", "Effect not found, please check if the effect name is correct.")
    INVALID_MASK_INFO = (2023, "无效的遮罩信息，请检查遮罩参数是否正确", "Invalid mask information, please check if mask parameters are correct.")
    MASK_ADD_FAILED = (2024, "遮罩添加失败", "Mask addition failed")
    MASK_NOT_FOUND = (2025, "遮罩类型未找到，请检查遮罩名称是否正确", "Mask type not found, please check if the mask name is correct.")
    INVALID_TEXT_STYLE_INFO = (2026, "无效的文本样式信息，请检查文本或关键词参数", "Invalid text style information, please check text or keyword parameters.")
    TEXT_STYLE_CREATE_FAILED = (2027, "文本样式创建失败", "Text style creation failed")
    MATERIAL_CREATE_FAILED = (2028, "素材创建失败", "Material creation failed")
    TEXT_ANIMATION_GET_FAILED = (2029, "获取文字动画失败", "Get text animation failed")
    VIDEO_GENERATION_SUBMIT_FAILED = (2030, "视频生成任务提交失败", "Video generation task submit failed")
    VIDEO_TASK_NOT_FOUND = (2031, "视频生成任务未找到", "Video generation task not found")
    VIDEO_STATUS_QUERY_FAILED = (2032, "视频任务状态查询失败", "Video task status query failed")
    IMAGE_ANIMATION_GET_FAILED = (2033, "获取图片动画失败", "Get image animation failed")
    AUDIO_DURATION_GET_FAILED = (2034, "获取音频时长失败", "Get audio duration failed")

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
