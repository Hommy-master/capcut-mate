# 使用轻量级Python镜像作为基础
FROM python:3.9-slim

# 在构建阶段安装curl
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*  # 清理缓存，减小镜像体积

# 安装UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 设置工作目录
WORKDIR /app

# 创建非root用户并切换
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

# 从CI构建的dist目录复制所有文件
COPY dist/ .

# 安装依赖
RUN uv sync

# 设置适当的权限
RUN chown -R appuser:appgroup /app

# 切换到非root用户
USER appuser

# 暴露应用监听的端口
EXPOSE 60000

# 设置环境变量，优化Python运行
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# 启动命令 - 使用uvicorn运行FastAPI应用
# uv run uvicorn main:app --reload --host 0.0.0.0 --port 60000 --workers 4
CMD ["uv", "run", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "60000", "--workers", "4"]