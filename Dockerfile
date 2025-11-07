FROM python:3.11-slim

# 配置阿里云镜像源（Debian 13 trixie）以加速软件包下载
RUN cp /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/debian.sources.backup 2>/dev/null || true && \
    echo 'Types: deb\n\
URIs: https://mirrors.aliyun.com/debian\n\
Suites: trixie trixie-updates trixie-backports\n\
Components: main contrib non-free non-free-firmware\n\
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg\n\
\n\
Types: deb\n\
URIs: https://mirrors.aliyun.com/debian-security\n\
Suites: trixie-security\n\
Components: main contrib non-free non-free-firmware\n\
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg' > /etc/apt/sources.list.d/debian.sources

# 安装系统依赖：ffmpeg（用于音频处理）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 验证 ffmpeg 安装
RUN ffmpeg -version && ffprobe -version

# 使用pip安装uv
RUN pip install --no-cache-dir uv

# 验证uv安装
RUN uv --version

# 设置工作目录
WORKDIR /app

# 创建非root用户并提前配置缓存目录
RUN mkdir -p /root/.cache/uv

# 从CI构建的dist目录复制所有文件
COPY dist/ .

# 安装依赖（仍使用root用户确保权限）
RUN uv sync

# 暴露应用端口
EXPOSE 60000

# 设置环境变量，指定uv缓存目录和用户主目录
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    HOME="/root" \
    UV_CACHE_DIR="/root/.cache/uv"

# 启动命令
CMD ["uv", "run", "main.py", "--workers", "4"]
