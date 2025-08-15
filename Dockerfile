FROM python:3.9-slim

WORKDIR /app

# 安装uv
RUN pip install --no-cache-dir uv

# 复制项目文件
COPY pyproject.toml .
COPY README.md .
COPY main.py .
COPY src/ src/
COPY tests/ tests/

# 安装依赖
RUN uv sync

# 暴露端口
EXPOSE 60000

# 启动命令
CMD ["uv", "run", "start"]
