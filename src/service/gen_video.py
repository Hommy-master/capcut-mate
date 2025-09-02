from src.utils.logger import logger
from src.utils.draft_cache import DRAFT_CACHE
from src.utils import helper
import src.pyJianYingDraft as draft
from src.pyJianYingDraft import ExportResolution, ExportFramerate
import config
import os


def gen_video(draft_url: str) -> (str, str):
    """
    生成视频的业务逻辑
    
    Args:
        draft_url: 草稿URL
    
    Returns:
        video_url: 视频URL
        message: 响应消息，如果成功就返回"视频生成成功"，失败就返回具体错误信息
    """

    # 从URL中提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        return "", "无效的草稿URL"

    # 此前需要将剪映打开，并位于目录页
    ctrl = draft.JianyingController()

    # 然后即可导出指定名称的草稿, 注意导出结束后视频才会被剪切(重命名)至指定位置
    ctrl.export_draft("draft_id", "C:\\workspace\\test.mp4")

    logger.info(f"gen video success: %s", os.path.join(config.DRAFT_DIR, draft_id))
    return draft_url, "视频生成成功"

