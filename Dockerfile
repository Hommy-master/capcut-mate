FROM python:3.9-slim

WORKDIR /app

# 接收CI传递的混淆代码目录（默认obfuscated）
ARG OBFUSCATED_CODE=obfuscated

# 安装依赖
COPY pyproject.toml .
RUN pip install --no-cache-dir uv && \
    uv sync --no-dev

# 仅复制CI中混淆后的代码（关键：不处理源码，直接用CI的混淆结果）
COPY $OBFUSCATED_CODE/main.py ./bin/
COPY $OBFUSCATED_CODE/src/ ./bin/src/

# 创建配置和日志目录
RUN mkdir -p /app/etc /app/logs && \
    echo "LOG_LEVEL=info" > /app/etc/config.env && \
    echo "LOG_DIR=/app/logs" >> /app/etc/config.env

# 权限设置
RUN addgroup --system appgroup && \
    adduser --system --group appuser && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 60000
CMD ["uv", "run", "/app/bin/main.py"]
