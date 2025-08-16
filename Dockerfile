FROM python:3.11-slim

# 安装基础工具
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 提前创建非特权用户和缓存目录
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 --home /home/appuser appuser && \
    mkdir -p /home/appuser/.cache/uv && \
    chown -R appuser:appgroup /home/appuser

# 把 uv 装到全局（root 即可）
RUN pip install --no-cache-dir uv

WORKDIR /app

# 先复制锁文件，用 --link-mode=copy 避免软链到 /root
COPY --chown=appuser:appgroup pyproject.toml uv.lock ./
USER appuser
ENV UV_CACHE_DIR=/home/appuser/.cache/uv
RUN uv venv --link-mode=copy .venv && \
    uv sync --frozen

# 再复制剩余源码
USER root          # root 有权限 COPY
COPY --chown=appuser:appgroup dist/ ./
USER appuser       # 最后切回非 root

EXPOSE 60000
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# 启动命令
CMD ["uv", "run", "main.py", "--workers", "4"]
