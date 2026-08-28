from logging.config import dictConfig
from typing import Optional
import logging
import os
import sys
import config


LOG_DIR = config.LOG_DIR
LOG_FILE = os.path.join(LOG_DIR, "capcut-mate.log")
LOG_MAX_BYTES = 20 * 1024 * 1024  # 20MB
LOG_BACKUP_COUNT = 10

_ENABLE_EXTENDED_FLAGS = 0x0080
_ENABLE_QUICK_EDIT_MODE = 0x0040


def disable_quick_edit() -> None:
    """Turn off console QuickEdit mode on Windows so selecting text in cmd.exe
    does not freeze the process while it writes to stdout."""
    if sys.platform != "win32":
        return

    import ctypes

    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-10)  # STD_INPUT_HANDLE
    mode = ctypes.c_uint32()
    if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
        return

    mode.value &= ~_ENABLE_QUICK_EDIT_MODE
    mode.value |= _ENABLE_EXTENDED_FLAGS
    kernel32.SetConsoleMode(handle, mode.value)


disable_quick_edit()

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


class SkipGenVideoStatusAccessLogFilter(logging.Filter):
    """Drop uvicorn access lines for gen_video_status (high-frequency polling floods the console)."""

    _PATH_FRAGMENT = "/gen_video_status"

    def filter(self, record: logging.LogRecord) -> bool:
        return self._PATH_FRAGMENT not in record.getMessage()


class RelativePathFormatter(logging.Formatter):
    def __init__(self, *args, project_root: Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        # 把项目根目录传进来
        self.project_root = project_root or os.getcwd()

    def format(self, record: logging.LogRecord) -> str:
        record.rel_path = os.path.relpath(record.pathname, self.project_root)
        return super().format(record)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": RelativePathFormatter,
            "fmt": "%(asctime)s.%(msecs)03d | %(levelname)s | %(trace_id)s | %(name)s | %(rel_path)s:%(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE,
            "maxBytes": LOG_MAX_BYTES,
            "backupCount": LOG_BACKUP_COUNT,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default", "file"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"handlers": ["default", "file"], "level": "INFO", "propagate": False},
        "uvicorn.access": {"handlers": ["default", "file"], "level": "INFO", "propagate": False},
        "src.utils.logger": {"handlers": ["default", "file"], "level": "INFO", "propagate": False}
    },
}

dictConfig(LOGGING_CONFIG)


def _install_trace_context_filters() -> None:
    """dictConfig 之后注册，避免字符串解析 Filter 时在包未加载完的情况下循环导入。"""
    from src.utils.trace_context import TraceContextFilter

    filt = TraceContextFilter()
    for log_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "src.utils.logger"):
        for h in logging.getLogger(log_name).handlers:
            h.addFilter(filt)


_install_trace_context_filters()

logging.getLogger("uvicorn.access").addFilter(SkipGenVideoStatusAccessLogFilter())

logger = logging.getLogger(__name__)
