# 项目常量定义
import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

# 草稿目录 - 使用相对路径和跨平台路径分隔符
DRAFT_DIR = os.path.join(PROJECT_ROOT, "output", "draft")

# 确保路径使用正确的操作系统分隔符
DRAFT_DIR = os.path.normpath(DRAFT_DIR)
