#!/bin/bash

##############################################################################
# FFmpeg 安装脚本
# 用于在本地开发环境快速安装 ffmpeg
##############################################################################

set -e  # 遇到错误立即退出

echo "=================================================="
echo "🎬 FFmpeg Installation Script for CapCut-Mate"
echo "=================================================="
echo ""

# 检测操作系统
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/debian_version ]; then
            echo "debian"
        elif [ -f /etc/redhat-release ]; then
            echo "redhat"
        else
            echo "linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
echo "🔍 Detected OS: $OS"
echo ""

# 检查 ffmpeg 是否已安装
check_ffmpeg() {
    if command -v ffmpeg &> /dev/null && command -v ffprobe &> /dev/null; then
        echo "✅ FFmpeg is already installed!"
        ffmpeg -version | head -n 1
        ffprobe -version | head -n 1
        return 0
    else
        echo "❌ FFmpeg not found"
        return 1
    fi
}

# 安装 ffmpeg (Debian/Ubuntu)
install_debian() {
    echo "📦 Installing ffmpeg on Debian/Ubuntu..."
    echo ""

    # 1. 备份原始源
    echo "⏳ Backing up original sources..."
    sudo cp /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/debian.sources.backup 2>/dev/null || true

    # 2. 配置阿里云镜像源(Debian 13 trixie)
    echo "⏳ Configuring Aliyun mirror for faster download..."
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
    echo "⏳ Updating package list..."
    sudo apt-get update

    echo "⏳ Installing ffmpeg..."
    sudo apt-get install -y ffmpeg

    echo "✅ Installation completed!"
}

# 安装 ffmpeg (macOS)
install_macos() {
    echo "📦 Installing ffmpeg on macOS..."
    echo ""

    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi

    echo "⏳ Installing ffmpeg via Homebrew..."
    brew install ffmpeg

    echo "✅ Installation completed!"
}

# 主逻辑
main() {
    # 先检查是否已安装
    if check_ffmpeg; then
        echo ""
        echo "=================================================="
        echo "✅ No action needed - FFmpeg is ready to use!"
        echo "=================================================="
        exit 0
    fi

    echo ""

    # 根据操作系统安装
    case $OS in
        debian)
            install_debian
            ;;
        macos)
            install_macos
            ;;
        *)
            echo "❌ Unsupported OS: $OS"
            echo ""
            echo "Please install ffmpeg manually:"
            echo "  - Debian/Ubuntu: sudo apt-get install -y ffmpeg"
            echo "  - macOS: brew install ffmpeg"
            echo "  - Windows: Download from https://ffmpeg.org/download.html"
            exit 1
            ;;
    esac

    echo ""
    echo "🔍 Verifying installation..."

    # 验证安装
    if check_ffmpeg; then
        echo ""
        echo "=================================================="
        echo "🎉 Success! FFmpeg is now installed and ready!"
        echo "=================================================="
        exit 0
    else
        echo ""
        echo "=================================================="
        echo "❌ Installation failed or ffmpeg not in PATH"
        echo "=================================================="
        exit 1
    fi
}

# 运行主逻辑
main
