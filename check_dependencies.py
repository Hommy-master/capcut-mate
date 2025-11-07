#!/usr/bin/env python3
"""
依赖检查脚本
在应用启动前检查必要的系统依赖是否已安装
"""

import subprocess
import sys
import os
from typing import List, Tuple


def check_command_exists(command: str) -> Tuple[bool, str]:
    """
    检查命令是否存在

    Args:
        command: 命令名称

    Returns:
        (是否存在, 版本信息或错误信息)
    """
    try:
        result = subprocess.run(
            [command, '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            # 提取版本信息的第一行
            version_line = result.stdout.split('\n')[0] if result.stdout else "Unknown version"
            return True, version_line
        else:
            return False, f"Command returned error code {result.returncode}"

    except FileNotFoundError:
        return False, f"Command '{command}' not found in PATH"
    except Exception as e:
        return False, f"Error checking command: {str(e)}"


def print_install_instructions():
    """打印安装说明"""
    print("\n" + "="*80)
    print("📦 Missing Dependencies - Installation Instructions")
    print("="*80)
    print("\n🐧 For Debian/Ubuntu:")
    print("  Run the following commands:")
    print("  1. Configure mirror (optional, for faster download in China):")
    print("     sudo cp /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/debian.sources.backup")
    print("     # Then configure Aliyun mirror as shown in your setup")
    print("  2. Install ffmpeg:")
    print("     sudo apt-get update")
    print("     sudo apt-get install -y ffmpeg")
    print("  3. Verify installation:")
    print("     ffmpeg -version")
    print("     ffprobe -version")

    print("\n🐳 For Docker:")
    print("  Rebuild the Docker image - ffmpeg is now included in the Dockerfile")
    print("  docker build -t capcut-mate .")

    print("\n🍎 For macOS:")
    print("  brew install ffmpeg")

    print("\n🪟 For Windows:")
    print("  1. Download ffmpeg from: https://ffmpeg.org/download.html")
    print("  2. Add ffmpeg to PATH")
    print("  3. Restart terminal")

    print("\n" + "="*80 + "\n")


def check_all_dependencies() -> bool:
    """
    检查所有必要的依赖

    Returns:
        所有依赖是否满足
    """
    dependencies = ['ffmpeg', 'ffprobe']
    all_satisfied = True
    missing_deps = []

    print("🔍 Checking system dependencies...")
    print("-" * 80)

    for dep in dependencies:
        exists, info = check_command_exists(dep)

        if exists:
            print(f"✅ {dep}: {info}")
        else:
            print(f"❌ {dep}: NOT FOUND - {info}")
            all_satisfied = False
            missing_deps.append(dep)

    print("-" * 80)

    if not all_satisfied:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing_deps)}")
        print_install_instructions()
        return False
    else:
        print("\n✅ All dependencies satisfied!")
        return True


def main():
    """主函数"""
    print("\n" + "="*80)
    print("🚀 CapCut-Mate Dependency Checker")
    print("="*80 + "\n")

    if not check_all_dependencies():
        print("❌ Dependency check FAILED!")
        print("   Please install missing dependencies and try again.\n")
        sys.exit(1)
    else:
        print("\n✅ Dependency check PASSED!")
        print("   You can now start the application.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
