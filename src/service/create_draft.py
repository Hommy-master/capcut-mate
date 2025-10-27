from src.utils.logger import logger
import config
import src.pyJianYingDraft as draft
from src.utils.draft_cache import update_cache
from exceptions import CustomException, CustomError
import datetime
import uuid


def create_draft(width: int, height: int) -> str:
    """
    创建剪映草稿的业务逻辑
    
    Args:
        width: 草稿宽度
        height: 草稿高度
    
    Returns:
        draft_url: 草稿URL

    Raises:
        CustomException: 草稿创建失败
    """
    # 生成一个草稿ID
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    draft_id = f"{timestamp}{unique_id}"
    logger.info(f"draft_id: {draft_id}, width: {width}, height: {height}")

    draft_folder = draft.Draft_folder(config.DRAFT_DIR)

    # 创建剪映草稿
    try:
        script = draft_folder.create_draft(draft_id, width, height, allow_replace=True)        
    except Exception as e:
        logger.error(f"create draft failed: {e}")
        raise CustomException(CustomError.DRAFT_CREATE_FAILED)

    # 缓存草稿
    update_cache(draft_id, script)

    logger.info(f"create draft success: {draft_id}")
    return config.DRAFT_URL + "?draft_id=" + draft_id

