from fastapi import FastAPI
from src.router import router
from logging.config import dictConfig
import logging
import os


app = FastAPI(
    title="CapCut Mate API", 
    version="1.0"
)

class RelativePathFormatter(logging.Formatter):
    def __init__(self, *args, project_root: str = None, **kwargs):
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
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["default"], "level": "INFO", "propagate": False},
    },
}

dictConfig(LOGGING_CONFIG)

if __name__ == "__main__":
    import uvicorn
    app.include_router(router.router, prefix="/openapi", tags=["capcut-mate"])
    uvicorn.run(app, host="0.0.0.0", port=60000, log_config=None)  # 禁用 uvicorn 默认日志
