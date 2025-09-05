from src.utils.logger import logger
from src.utils import helper
import config
import os


def get_draft(draft_id: str) -> (str, str):
    """
    获取剪映草稿的业务逻辑
    
    Args:
        draft_url: 草稿URL
    
    Returns:
        files: 文件列表
        message: 响应消息，如果成功，就返回“获取草稿成功”，如果失败，则包含具体的错误信息
    """

    # 从URL中提取草稿ID
    if not draft_id:
        return [], "无效的草稿ID"

    draft_dir = os.path.join(config.DRAFT_DIR, draft_id)
    if not os.path.exists(draft_dir):
        return [], f"草稿目录{draft_dir}不存在"
    
    # 从草稿目录中获取文件列表
    files = helper.get_all_files(draft_dir)

    logger.info(f"get draft success: {draft_id}")
    return files, "获取草稿成功"

