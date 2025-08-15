# 第一阶段：构建阶段（代码混淆）
FROM python:3.9-slim as builder

# 设置工作目录
WORKDIR /build

# 安装代码混淆工具
RUN pip install --no-cache-dir uv pyminifier

# 复制项目文件
COPY pyproject.toml .
COPY main.py .
COPY src/ ./src/

# 安装项目依赖（仅构建阶段需要）
RUN uv sync

# 创建混淆后代码的目录结构
RUN mkdir -p /build/obfuscated/bin /build/obfuscated/etc /build/obfuscated/logs

# 使用pyminifier进行代码混淆
# 混淆主程序（保留入口点可识别性）
RUN pyminifier --obfuscate --destdir /build/obfuscated/bin main.py

# 混淆src目录下的所有模块
RUN find src -name "*.py" -exec sh -c ' \
    for file do \
        mkdir -p /build/obfuscated/bin/$(dirname "$file"); \
        pyminifier --obfuscate --destdir /build/obfuscated/bin/$(dirname "$file") "$file"; \
    done \
' sh {} +

# 复制并简化配置文件
RUN echo "LOG_LEVEL=info" > /build/obfuscated/etc/config.env && \
    echo "PORT=60000" >> /build/obfuscated/etc/config.env && \
    echo "LOG_DIR=/app/logs" >> /build/obfuscated/etc/config.env

# 第二阶段：运行阶段
FROM python:3.9-slim

# 创建非root用户
RUN addgroup --system appgroup && \
    adduser --system --group appuser

# 设置工作目录
WORKDIR /app

# 创建目录结构
RUN mkdir -p /app/bin /app/etc /app/logs && \
    chown -R appuser:appgroup /app

# 安装运行时依赖
COPY pyproject.toml .
RUN pip install --no-cache-dir uv && \
    uv sync --no-dev && \
    rm -rf /root/.cache

# 从构建阶段复制混淆后的代码和配置
COPY --from=builder /build/obfuscated/bin/ /app/bin/
COPY --from=builder /build/obfuscated/etc/ /app/etc/

# 设置权限
RUN chown -R appuser:appgroup /app && \
    chmod 500 /app/bin/*.py /app/bin/src/**/*.py && \
    chmod 755 /app/bin /app/logs /app/etc

# 切换到非root用户
USER appuser

# 暴露端口
EXPOSE 60000

# 设置环境变量
ENV CONFIG_PATH=/app/etc/config.env \
    LOG_DIR=/app/logs

# 启动命令
CMD ["uv", "run", "/app/bin/main.py"]
