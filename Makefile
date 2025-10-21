# Makefile for CapCut Mate

.PHONY: help install install-mcp sync run-api run-mcp test clean format lint

help:  ## 显示帮助信息
	@echo "可用命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## 安装基础依赖
	uv sync

install-mcp:  ## 安装包含 MCP 支持的依赖
	uv sync --extra mcp

sync:  ## 同步并更新所有依赖
	uv sync --upgrade

run-api:  ## 运行 HTTP API 服务器
	uv run capcut_server.py

run-mcp:  ## 运行 MCP 服务器
	uv run mcp_server.py

test:  ## 运行测试
	uv run pytest tests/

clean:  ## 清理缓存和临时文件
	rm -rf __pycache__ .pytest_cache .uv
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete

format:  ## 格式化代码
	uv run black .
	uv run isort .

lint:  ## 检查代码质量
	uv run flake8 .

dev:  ## 开发模式 - 安装所有依赖
	uv sync --all-extras
