from src.utils.logger import logger
from src.utils.unique_id import UniqueIDGenerator
from src.constants import base
from pyJianYingDraft import DraftFolder


def create_draft_service(width: int, height: int) -> str:
    """
    创建剪映草稿的业务逻辑
    
    Args:
        width: 草稿宽度
        height: 草稿高度
    
    Returns:
        生成的草稿URL
    """
    # 生成一个草稿ID
    draft_id = UniqueIDGenerator().generate()
    logger.info(f"draft_id: {draft_id}, width: {width}, height: {height}")

    try:
        # 初始化草稿文件夹
        draft_folder = DraftFolder(base.DRAFT_DIR)
        # 创建新草稿
        script = draft_folder.create_draft(draft_id, width, height)
        # 保存草稿
        script.save()
        logger.info(f"create draft success: {draft_id}")
        return base.DRAFT_URL + "?draft_id=" + draft_id
    except Exception as e:
        error_msg = str(e)
        logger.error(f"create draft failed: {error_msg}")
        raise Exception(f"create draft failed: {error_msg}")
