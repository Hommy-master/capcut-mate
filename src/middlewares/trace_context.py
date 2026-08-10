"""为每个 HTTP 请求注入 W3C trace 上下文并写入 contextvars。"""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.utils import trace_context as tc


class TraceContextMiddleware(BaseHTTPMiddleware):
    """
    最先执行（应注册为最后 add_middleware）：解析/生成 trace_id、span_id，
    在响应中返回 traceparent 与 X-Request-ID。
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        def _get(h: str) -> str | None:
            return request.headers.get(h)

        trace_id, span_id = tc.resolve_trace_from_headers(_get)

        tid_token = tc.trace_id_var.set(trace_id)
        sid_token = tc.span_id_var.set(span_id)
        request.state.trace_id = trace_id
        request.state.span_id = span_id
        try:
            response = await call_next(request)
        finally:
            tc.trace_id_var.reset(tid_token)
            tc.span_id_var.reset(sid_token)

        response.headers["traceparent"] = tc.build_traceparent(trace_id, span_id)
        response.headers["X-Request-ID"] = trace_id
        return response
