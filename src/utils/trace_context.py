"""
分布式追踪上下文（W3C Trace Context + 常见 Request-ID）。

- 入站：优先解析 `traceparent`（W3C），否则 `X-Request-ID` / `X-Trace-Id`；
- 出站响应：`traceparent`、`X-Request-ID`（与 trace-id 对齐）；
- 运行态：`contextvars` 供任意代码通过 `get_trace_id()` 读取，并由 Logging Filter 写入每条日志。
"""
from __future__ import annotations

import contextvars
import hashlib
import logging
import secrets
import uuid
from typing import Optional, Tuple

# --- W3C Trace Context: https://www.w3.org/TR/trace-context/

TRACEPARENT_HEADER = "traceparent"
REQUEST_ID_HEADERS = ("x-request-id", "x-trace-id")

trace_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "trace_id", default=None
)
span_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "span_id", default=None
)


def get_trace_id() -> Optional[str]:
    return trace_id_var.get()


def get_span_id() -> Optional[str]:
    return span_id_var.get()


def _gen_trace_id() -> str:
    return uuid.uuid4().hex


def _gen_span_id() -> str:
    return secrets.token_hex(8)


def parse_traceparent(value: str) -> Optional[Tuple[str, str]]:
    """
    解析 traceparent，成功返回 (trace_id, parent_span_id)，均为小写十六进制字符串。
    trace-id 全 0 视为无效。
    """
    parts = value.strip().split("-")
    if len(parts) != 4:
        return None
    _ver, tid, pid, _flags = parts
    if len(tid) != 32 or len(pid) != 16:
        return None
    tid_l, pid_l = tid.lower(), pid.lower()
    hex32 = set("0123456789abcdef")
    if not all(c in hex32 for c in tid_l) or not all(c in hex32 for c in pid_l):
        return None
    if tid_l == "0" * 32:
        return None
    return tid_l, pid_l


def build_traceparent(trace_id: str, span_id: str, sampled: bool = True) -> str:
    """组装标准 traceparent（version 00）。"""
    flags = "01" if sampled else "00"
    return f"00-{trace_id}-{span_id}-{flags}"


def _normalize_custom_request_id(raw: str) -> str:
    """将客户端 Request-ID 规范为 32 位 hex trace-id；无法解析则稳定哈希到 32 hex。"""
    s = raw.strip()
    if not s:
        return _gen_trace_id()
    no_dash = s.replace("-", "").lower()
    hexset = set("0123456789abcdef")
    if len(no_dash) == 32 and all(c in hexset for c in no_dash):
        return no_dash
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:32]


def resolve_trace_from_headers(header_getter) -> Tuple[str, str]:
    """
    从请求头解析或生成 (trace_id, span_id)。
    header_getter: 与 Starlette Headers 兼容，如 headers.get(name)。
    """
    tp = header_getter(TRACEPARENT_HEADER)
    if tp:
        parsed = parse_traceparent(tp)
        if parsed:
            tid, _parent = parsed
            return tid, _gen_span_id()

    for name in REQUEST_ID_HEADERS:
        v = header_getter(name)
        if v and str(v).strip():
            return _normalize_custom_request_id(str(v)), _gen_span_id()

    return _gen_trace_id(), _gen_span_id()


class TraceContextFilter(logging.Filter):
    """为 LogRecord 增加 trace_id 字段，供 Formatter 使用。"""

    def filter(self, record: logging.LogRecord) -> bool:
        tid = get_trace_id()
        record.trace_id = tid if tid else "-"
        return True
