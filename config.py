# 项目常量定义
import os


# 保存剪映草稿的目录
DRAFT_DIR = os.path.join(os.path.dirname(__file__), "output", "draft")

# 剪映草稿的下载路径
DRAFT_URL = os.getenv("DRAFT_URL", "https://cm.jcaigc.cn/openapi/v1/get_draft")

# 将容器内的文件路径转成一个下载路径，执行替换操作，即将/app/ -> https://cm.jcaigc.cn/
DOWNLOAD_URL = os.getenv("DOWNLOAD_URL", "https://cm.jcaigc.cn/")
