FROM python:3.11-slim

RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

RUN pip install --no-cache-dir uv

WORKDIR /app

# 一次性复制源码 + 锁文件（root copy，再 chown）
COPY --chown=appuser:appgroup dist/* .

USER appuser
ENV UV_CACHE_DIR=/tmp/uv-cache
RUN uv venv --link-mode=copy .venv && \
    uv sync --frozen

EXPOSE 60000
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# 启动命令
CMD ["uv", "run", "main.py", "--workers", "4"]
