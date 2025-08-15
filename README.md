# CapCut Mate API

## 项目简介
CapCut Mate API 是一个基于 FastAPI 构建的剪映小助手

## 功能特点
- 用户管理：创建、查询、更新和删除用户
- 数据验证：使用 Pydantic 进行请求数据验证
- 安全认证：密码加密存储
- RESTful API 设计：符合标准的 API 设计规范
- 自动生成文档：FastAPI 自动生成交互式 API 文档

## 技术栈
- Python 3.11+
- FastAPI：高性能的 Web 框架
- Pydantic：数据验证和模型定义
- Passlib：密码加密
- Uvicorn：ASGI 服务器
- uv：Python 包管理器和项目管理工具

## 快速开始

### 前提条件
- Python 3.11 或更高版本
- uv：Python 包管理器和项目管理工具
  安装方法: `pip install uv` 或访问 [uv 官方网站](https://github.com/astral-sh/uv) 获取最新安装指南

### 安装步骤
1. 克隆项目
```bash
git clone git@github.com:Hommy-master/capcut-mate.git
cd capcut-mate
```

2. 安装依赖
```bash
uv sync
uv add passlib[bcrypt]
uv add email-validator
```

3. 启动服务器
```bash
uvicorn main:app --reload
```

4. 访问 API 文档
启动服务器后，访问以下地址查看自动生成的交互式 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 许可证
本项目采用 MIT 许可证，详情请见 LICENSE 文件。
