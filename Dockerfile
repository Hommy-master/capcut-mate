# 使用轻量级Python镜像作为基础
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 创建非root用户并切换
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

# 复制CI处理后的依赖和混淆代码
COPY --chown=appuser:appgroup dist/ /app/

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# 暴露端口
EXPOSE 60000

# 切换到非root用户
USER appuser

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "60000", "--workers", "4"]
    