# CapCut Mate API

## 项目简介
CapCut Mate API 是一个基于 FastAPI 构建的剪映小助手

## 功能特点
- 用户管理：创建草稿、添加视频、保存草稿、云端渲染
- 数据验证：使用 Pydantic 进行请求数据验证
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
- Python 3.11
- uv：Python 包管理器和项目管理工具
  安装方法: 
  - windows
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  - linux
  sh -c "$(curl -LsSf https://astral.sh/uv/install.sh)"

### 安装步骤
1. 克隆项目
```bash
git clone git@github.com:Hommy-master/capcut-mate.git
cd capcut-mate
```

2. 安装依赖
```bash
# 安装依赖
uv sync
```

3. 启动服务器
```bash
uv run main.py
```

4. 容器部署
```bash
docker pull gogoshine/capcut-mate:latest
```

## 开源社区问题交流群
- 微信群：

  ![剪映小助手](./assets/wechat-q.jpg)

## 商业合作
- 微信：

  ![微信](./assets/wechat.png)

- 邮箱：taohongmin51@gmail.com
