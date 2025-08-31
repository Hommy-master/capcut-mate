from src.utils.logger import logger
import src.pyJianYingDraft as draft
from src.utils.draft_cache import DRAFT_CACHE
from src.utils import helper
import config
import os


def save_draft(draft_url: str) -> (str, str):
    """
    保存剪映草稿的业务逻辑
    
    Args:
        draft_url: 草稿URL
    
    Returns:
        draft_url: 草稿URL
        message: 响应消息，如果成功就返回"草稿保存成功"，失败就返回具体错误信息
    """

    # 从URL中提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        return "", "无效的草稿URL"

    # 从缓存中获取草稿
    script = DRAFT_CACHE[draft_id]

    # 保存草稿
    script.save()

    logger.info(f"save draft success: %s", os.path.join(config.DRAFT_DIR, draft_id))
    return draft_url, "草稿保存成功"

