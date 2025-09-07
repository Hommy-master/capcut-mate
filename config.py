# 项目常量定义
import os


# 确保路径使用正确的操作系统分隔符
DRAFT_DIR = os.path.join(os.path.dirname(__file__), "output", "draft")
DRAFT_URL = os.getenv("DRAFT_URL", "https://cm.jcaigc.cn/openapi/v1/get_draft")
