FROM python:3.11-slim

# 使用pip安装uv
RUN pip install --no-cache-dir uv

# 验证uv安装
RUN uv --version

# 设置工作目录
WORKDIR /app

# 创建非root用户并提前配置缓存目录
RUN mkdir -p /root/.cache/uv /app/bin/

# 从CI构建的dist目录复制所有文件
COPY dist/ .
COPY tools/ffprobe /app/bin/ffprobe

# 安装依赖（仍使用root用户确保权限）
RUN uv sync

# 添加权限
RUN chmod 0755 /app/bin/*

# 暴露应用端口
EXPOSE 30000

# 设置环境变量，指定uv缓存目录和用户主目录
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:/app/bin:$PATH" \
    HOME="/root" \
    UV_CACHE_DIR="/root/.cache/uv"

# 启动命令
CMD ["uv", "run", "main.py", "--workers", "4"]
