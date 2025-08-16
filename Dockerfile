FROM python:3.11-slim

# 使用pip安装uv
RUN pip install --no-cache-dir uv

# 验证uv安装
RUN uv --version

# 设置工作目录
WORKDIR /app

# 创建非root用户并提前配置缓存目录
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 --home /home/appuser appuser && \
    # 创建uv缓存目录并设置权限
    mkdir -p /home/appuser/.cache/uv && \
    chown -R appuser:appgroup /home/appuser/.cache

# 从CI构建的dist目录复制所有文件
COPY dist/ .

# 安装依赖（仍使用root用户确保权限）
RUN uv sync && \
    chown -R appuser:appgroup /app

# 切换到非root用户
USER appuser

# 暴露应用端口
EXPOSE 60000

# 设置环境变量，指定uv缓存目录和用户主目录
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    HOME="/home/appuser" \
    UV_CACHE_DIR="/home/appuser/.cache/uv"

# 启动命令
CMD ["uv", "run", "main.py", "--workers", "4"]
