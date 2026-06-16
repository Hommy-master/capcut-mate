# 对象存储 object key 构建
import datetime

import config


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
