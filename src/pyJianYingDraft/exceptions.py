"""自定义异常类"""

class TrackNotFound(NameError):
    """未找到满足条件的轨道"""
class AmbiguousTrack(ValueError):
    """找到多个满足条件的轨道"""
class SegmentOverlap(ValueError):
    """新片段与已有的轨道片段重叠"""

class MaterialNotFound(NameError):
    """未找到满足条件的素材"""
class AmbiguousMaterial(ValueError):
    """找到多个满足条件的素材"""

class ExtensionFailed(ValueError):
    """替换素材时延伸片段失败"""

class DraftNotFound(NameError):
    """未找到草稿"""
class AutomationError(Exception):
    """自动化操作失败"""
class ExportTimeout(Exception):
    """导出超时"""

# 剪映显示导出成功、但源文件不存在时的错误标记；供 video_task_manager 归类为可重试
EXPORT_OUTPUT_MISSING_ERROR_MARKER = "export output missing"

class ExportOutputMissingError(AutomationError):
    """剪映显示导出成功，但导出文件不存在。"""
