from src.utils.logger import logger
import config
import src.pyJianYingDraft as draft
from src.utils.draft_cache import update_cache
from exceptions import CustomException, CustomError
import datetime
import uuid
import os
import shutil


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

    # 使用默认模板创建剪映草稿
    try:
        # 先确保默认模板存在于草稿目录中
        template_source_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "template", "default")
        template_target_path = os.path.join(config.DRAFT_DIR, "default")
        
        # 如果草稿目录中不存在默认模板，则从template/default复制
        if not os.path.exists(template_target_path):
            os.makedirs(config.DRAFT_DIR, exist_ok=True)
            shutil.copytree(template_source_path, template_target_path)
        
        # 使用default模板来创建新草稿
        script = draft_folder.duplicate_as_template("default", draft_id, allow_replace=True)
        
        # 更新草稿的画布尺寸以匹配请求的尺寸
        script.width = width
        script.height = height
        script.content["canvas_config"]["width"] = width
        script.content["canvas_config"]["height"] = height
        
        # 添加空的主轨道（仅当没有主轨道时添加）
        main_track_name = "main_track"
        # 检查是否已存在主轨道
        if main_track_name not in script.tracks and not any(track.name == main_track_name for track in script.imported_tracks):
            script.add_track(track_type=draft.TrackType.video, track_name=main_track_name, relative_index=0)
            logger.info(f"Added empty main track: {main_track_name}")
        
        # 保存草稿以确保更改被保存
        script.save()
        
    except Exception as e:
        logger.error(f"create draft failed: {e}")
        raise CustomException(CustomError.DRAFT_CREATE_FAILED)

    # 缓存草稿
    update_cache(draft_id, script)

    logger.info(f"create draft success: {draft_id}")
    return config.DRAFT_URL + "?draft_id=" + draft_id