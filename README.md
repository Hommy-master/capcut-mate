# CapCut Mate API

## 项目简介
CapCut Mate API 是一个基于 FastAPI 构建的剪映自动化助手，提供丰富的API接口来创建和编辑剪映草稿。支持创建草稿、添加视频/音频/图片/字幕/特效等素材、保存草稿及云端渲染等功能，可作为扣子插件一键部署使用。

## 功能特点
- 🎬 草稿管理：创建草稿、获取草稿、保存草稿
- 🎥 素材添加：添加视频、音频、图片、贴纸、字幕、特效、遮罩等
- 🔧 高级功能：关键帧控制、文字样式、动画效果等
- 📤 视频导出：云端渲染生成最终视频
- 🛡️ 数据验证：使用 Pydantic 进行请求数据验证
- 📖 RESTful API：符合标准的 API 设计规范
- 📚 自动文档：FastAPI 自动生成交互式 API 文档

## 技术栈
- Python 3.11+
- FastAPI：高性能的 Web 框架
- Pydantic：数据验证和模型定义
- Passlib：密码加密（如果使用用户认证）
- Uvicorn：ASGI 服务器
- uv：Python 包管理器和项目管理工具

## 快速开始

### 前提条件
- Python 3.11+
- uv：Python 包管理器和项目管理工具

安装方法:
#### Windows
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Linux/macOS
```bash
sh -c "$(curl -LsSf https://astral.sh/uv/install.sh)"
```

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

4. 访问API文档
启动后访问 http://localhost:30000/docs 查看自动生成的交互式API文档

### 容器部署
```bash
docker pull gogoshine/capcut-mate:latest
docker run -p 30000:30000 gogoshine/capcut-mate:latest
```

或者使用 docker-compose:
```bash
docker-compose up -d
```

## API 使用示例

### 创建草稿
```bash
curl -X POST "http://localhost:30000/openapi/capcut-mate/v1/create_draft" \
-H "Content-Type: application/json" \
-d '{"width": 1080, "height": 1920}'
```

### 添加视频
```bash
curl -X POST "http://localhost:30000/openapi/capcut-mate/v1/add_videos" \
-H "Content-Type: application/json" \
-d '{
  "draft_url": "http://localhost:30000/openapi/capcut-mate/v1/get_draft?draft_id=20251126212753cab03392",
  "video_infos": [
    {
      "url": "https://example.com/video.mp4",
      "start": 0,
      "end": 1000000
    }
  ]
}'
```

## API 文档
- 本地访问: http://localhost:30000/docs
- ReDoc 版本: http://localhost:30000/redoc

## 开源社区问题交流群
- 微信群：

  <img src="./assets/wechat-q.jpg" width="344" height="498" alt="剪映小助手">

## 商业合作
- 微信：

  <img src="./assets/wechat.jpg" width="220" height="220" alt="技术支持微信">

- 邮箱：taohongmin51@gmail.com

⭐ 如果你觉得这个项目对你有帮助，欢迎点个 Star 支持一下！你的支持是我持续维护和改进项目的最大动力 😊