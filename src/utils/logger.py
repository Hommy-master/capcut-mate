from logging.config import dictConfig
from typing import Optional
import logging
import os
import config


LOG_DIR = config.LOG_DIR
LOG_FILE = os.path.join(LOG_DIR, "capcut-mate.log")
LOG_MAX_BYTES = 20 * 1024 * 1024  # 20MB
LOG_BACKUP_COUNT = 10

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


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
            "fmt": "%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(rel_path)s:%(lineno)d | %(message)s",
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

logger = logging.getLogger(__name__)
