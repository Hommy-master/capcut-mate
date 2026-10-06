# 对象存储 object key 构建
import datetime
import os
import re
import uuid

import config

# 文件名主干保留的最大长度（对象存储 key 上限 1024 字节，这里取值更保守）
_MAX_STEM_LENGTH = 80
# 扩展名保留的最大长度
_MAX_EXTENSION_LENGTH = 16
# 只保留字母、数字、下划线（含中文等 Unicode 文字）、点和连字符，其余字符统一替换为 _
_UNSAFE_FILENAME_CHARS = re.compile(r"[^\w.\-]+")


def build_storage_object_key(filename: str, now: datetime.datetime | None = None) -> str:
    """
    构建对象存储 key：[配置前缀/]yyyy-MM-dd/文件名

    Args:
        filename: 对象文件名（不含路径）
        now: 用于日期分目录的时间；默认当前时间
    """
    if now is None:
        now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    prefix = (config.STORAGE_UPLOAD_PREFIX or "").strip().strip("/")
    if prefix:
        return f"{prefix}/{current_date}/{filename}"
    return f"{current_date}/{filename}"


def sanitize_object_filename(filename: str) -> str:
    """
    净化上传文件名：去掉路径、替换不安全字符，只保留「主干 + 扩展名」。

    Args:
        filename: 客户端原始文件名（可能带路径或特殊字符）

    Returns:
        str: 可安全写入 object key 的文件名

    Raises:
        ValueError: 净化后没有可用字符时
    """
    # 兼容 Windows 风格路径：先统一分隔符，再取最后一段，避免 ../ 等路径穿越
    name = (filename or "").replace("\\", "/").rsplit("/", 1)[-1].strip()
    name = _UNSAFE_FILENAME_CHARS.sub("_", name).strip("._")
    if not name:
        raise ValueError(f"invalid file name: {filename!r}")

    stem, extension = os.path.splitext(name)
    stem = stem[:_MAX_STEM_LENGTH].strip("._")
    if not stem:
        raise ValueError(f"invalid file name: {filename!r}")
    return f"{stem}{extension[:_MAX_EXTENSION_LENGTH].lower()}"


def build_upload_object_key(filename: str, now: datetime.datetime | None = None) -> str:
    """
    构建客户端上传用的 object key：[配置前缀/]yyyy-MM-dd/唯一前缀_文件名

    唯一前缀用于避免同名文件在同一天互相覆盖（build_storage_object_key 本身不含唯一性）。

    Args:
        filename: 客户端原始文件名
        now: 用于日期分目录的时间；默认当前时间

    Raises:
        ValueError: 文件名非法时（见 sanitize_object_filename）
    """
    unique_prefix = uuid.uuid4().hex[:16]
    return build_storage_object_key(f"{unique_prefix}_{sanitize_object_filename(filename)}", now=now)
