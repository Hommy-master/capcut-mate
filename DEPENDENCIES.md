# 系统依赖说明

## 概述

CapCut-Mate 需要以下系统依赖才能正常运行：

- **FFmpeg** - 用于音频处理（`get_audio_duration` 端点需要）

## 快速安装

### 方式 1：使用自动安装脚本（推荐）

```bash
# 赋予执行权限
chmod +x install_ffmpeg.sh

# 运行安装脚本
./install_ffmpeg.sh
```

### 方式 2：手动安装

#### Debian/Ubuntu

```bash
# 1. 备份原始源（可选）
sudo cp /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/debian.sources.backup

# 2. 配置阿里云镜像源（可选，加速下载）
sudo bash -c 'cat > /etc/apt/sources.list.d/debian.sources << '\''EOF'\''
Types: deb
URIs: https://mirrors.aliyun.com/debian
Suites: trixie trixie-updates trixie-backports
Components: main contrib non-free non-free-firmware
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg

Types: deb
URIs: https://mirrors.aliyun.com/debian-security
Suites: trixie-security
Components: main contrib non-free non-free-firmware
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
EOF'

# 3. 更新并安装 ffmpeg
sudo apt-get update
sudo apt-get install -y ffmpeg

# 4. 验证安装
ffmpeg -version
ffprobe -version
```

#### macOS

```bash
# 使用 Homebrew 安装
brew install ffmpeg

# 验证安装
ffmpeg -version
ffprobe -version
```

#### Windows

1. 从 [FFmpeg 官网](https://ffmpeg.org/download.html) 下载 Windows 版本
2. 解压到目标目录（如 `C:\ffmpeg`）
3. 将 `C:\ffmpeg\bin` 添加到系统 PATH
4. 重启终端并验证：`ffmpeg -version`

### 方式 3：Docker（无需手动安装）

使用 Docker 运行项目时，ffmpeg 已包含在镜像中，无需额外安装：

```bash
# 构建镜像
docker build -t capcut-mate .

# 运行容器
docker run -p 60000:60000 capcut-mate
```

## 检查依赖

在启动应用前，可以运行依赖检查脚本：

```bash
# 运行依赖检查
python check_dependencies.py
```

输出示例：

```
================================================================================
🚀 CapCut-Mate Dependency Checker
================================================================================

🔍 Checking system dependencies...
--------------------------------------------------------------------------------
✅ ffmpeg: ffmpeg version 6.0
✅ ffprobe: ffprobe version 6.0
--------------------------------------------------------------------------------

✅ All dependencies satisfied!
   You can now start the application.
```

## 常见问题

### Q1: 为什么需要 FFmpeg？

**A:** `get_audio_duration` 端点使用 `ffprobe`（FFmpeg 的一部分）来分析音频文件并获取时长信息。

### Q2: 不安装 FFmpeg 能运行项目吗？

**A:** 可以运行项目，但调用 `get_audio_duration` 端点时会返回错误。其他功能不受影响。

### Q3: Docker 镜像已经包含 FFmpeg 了吗？

**A:** 是的！更新后的 Dockerfile 已经包含了 ffmpeg 的安装步骤，使用 Docker 部署无需额外配置。

### Q4: 如何验证 FFmpeg 是否安装成功？

**A:** 运行以下命令：

```bash
ffmpeg -version
ffprobe -version
```

如果显示版本信息则安装成功。

### Q5: 安装脚本配置了阿里云镜像源，会影响其他软件吗？

**A:** 阿里云镜像源只是更换了软件包下载源，不会影响已安装软件的功能，只是让后续软件包下载更快（特别是在中国大陆）。

## 相关文件

- `Dockerfile` - Docker 镜像构建文件（已包含 ffmpeg 安装）
- `check_dependencies.py` - 依赖检查脚本
- `install_ffmpeg.sh` - FFmpeg 自动安装脚本
- `src/service/get_audio_duration.py` - 使用 ffprobe 的服务代码

## 技术细节

### FFmpeg 在项目中的使用

```python
# src/service/get_audio_duration.py

# 使用 ffprobe 分析音频文件
cmd = [
    'ffprobe',
    '-i', audio_file_path,
    '-v', 'quiet',
    '-print_format', 'json',
    '-show_format',
    '-show_streams'
]

result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
```

### 错误处理

如果 ffprobe 不可用，会返回友好的错误消息：

```json
{
  "error": "FFprobe tool not available. Please install ffmpeg: Debian/Ubuntu: 'sudo apt-get install -y ffmpeg' | macOS: 'brew install ffmpeg' | Docker: Rebuild image with updated Dockerfile"
}
```

## 更新日志

- **2025-01** - 添加 FFmpeg 到 Dockerfile，解决每次运行都需手动安装的问题
- **2025-01** - 创建自动安装脚本和依赖检查工具
- **2025-01** - 改进错误提示，提供详细的安装说明
