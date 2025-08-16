# 使用轻量级Python镜像作为基础
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 创建非root用户并切换
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

# 从CI构建的dist目录复制所有文件（混淆后的代码、依赖和运行时）
COPY dist/ .

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
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "60000", "--workers", "4"]