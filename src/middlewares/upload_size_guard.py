# 上传请求体前置拦截中间件
# Starlette 在进入路由前就会把整个 multipart 请求体写入磁盘（文件部分 >1MB 落盘，且无总量上限），
# 端点内的体积校验太晚；这里按 Content-Length 提前拒绝。
# 仅对携带真实 Content-Length 的客户端有效，分块传输编码/伪造请求头由 service 内的流式上限兜底。
from typing import Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from exceptions import CustomError, CustomException
from src.service.upload_file import MAX_UPLOAD_BODY_BYTES, MAX_UPLOAD_SIZE_BYTES

# 上传接口路径后缀（路由前缀为 /openapi/capcut-mate）
UPLOAD_PATH_SUFFIX = "/v1/upload_file"


def _exceeds_body_limit(method: str, path: str, content_length: Optional[str]) -> bool:
    """判断是否为超限的上传请求（无/非法 Content-Length 时不拦截，交给 service 流式校验）。"""
    if method != "POST" or not path.endswith(UPLOAD_PATH_SUFFIX):
        return False
    if not content_length or not content_length.isdigit():
        return False
    return int(content_length) > MAX_UPLOAD_BODY_BYTES


class UploadSizeGuardMiddleware(BaseHTTPMiddleware):
    """上传请求体大小前置拦截：超过上限直接返回 2004，不读取请求体。"""

    async def dispatch(self, request: Request, call_next):
        if _exceeds_body_limit(request.method, request.url.path, request.headers.get("content-length")):
            raise CustomException(
                CustomError.FILE_SIZE_LIMIT_EXCEEDED,
                detail=f"{MAX_UPLOAD_SIZE_BYTES / 1024 / 1024:.2f} MB"
            )

        return await call_next(request)
