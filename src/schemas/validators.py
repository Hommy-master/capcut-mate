# 可复用的 Pydantic 校验函数
import uuid
from typing import Optional


def validate_api_key_uuid(value: Optional[str]) -> Optional[str]:
    """
    校验 apiKey 格式：空值归一为 None，非 UUID 时抛出 ValueError。

    Args:
        value: 请求传入的 apiKey

    Returns:
        Optional[str]: 归一化后的 apiKey

    Raises:
        ValueError: apiKey 不是合法 UUID
    """
    if value is None or value == "":
        return None
    try:
        uuid.UUID(value)
    except ValueError:
        raise ValueError(
            "API密钥格式不正确，必须是合法的UUID；请登录官网 https://jcaigc.cn 获取 apiKey"
        )
    return value
