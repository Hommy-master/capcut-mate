import uuid
from src.utils.logger import logger
from src.constants.base import DRAFT_DIR
from pyJianYingDraft import DraftFolder


def create_draft_service(width: int, height: int) -> str:
    """
    创建剪映草稿的业务逻辑
    
    Args:
        width: 草稿宽度
        height: 草稿高度
    
    Returns:
        生成的草稿ID
    """
    # 生成一个UUID作为草稿ID
    draft_id = str(uuid.uuid4())
    logger.info(f"draft_id: {draft_id}, width: {width}, height: {height}")

    try:
        # 初始化草稿文件夹
        draft_folder = DraftFolder(DRAFT_DIR)
        # 创建新草稿
        script = draft_folder.create_draft(draft_id, width, height)
        # 保存草稿
        script.save()
        logger.info(f"create draft success: {draft_id}")
        return draft_id
    except Exception as e:
        error_msg = str(e)
        logger.error(f"create draft failed: {error_msg}")
        raise Exception(f"create draft failed: {error_msg}")
