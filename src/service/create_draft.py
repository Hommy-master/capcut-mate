from src.utils.logger import logger
import config
import src.pyJianYingDraft as draft
from src.utils.draft_cache import update_cache
from exceptions import CustomException, CustomError
import datetime
import uuid
import json
import os


def update_draft_meta_info(draft_id: str):
    """
    更新draft_meta_info.json文件中的draft_fold_path字段
    
    Args:
        draft_id: 草稿ID
    """
    draft_path = os.path.join(config.DRAFT_DIR, draft_id)
    meta_info_path = os.path.join(draft_path, "draft_meta_info.json")
    
    # 读取现有的draft_meta_info.json文件
    with open(meta_info_path, 'r', encoding='utf-8') as f:
        meta_info = json.load(f)
    
    # 设置draft_fold_path为草稿文件夹的完整路径
    meta_info["draft_fold_path"] = draft_path
    
    # 写回文件
    with open(meta_info_path, 'w', encoding='utf-8') as f:
        json.dump(meta_info, f, ensure_ascii=False, indent=4)


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
        
        # 添加空的主轨道（仅当没有主轨道时添加）
        main_track_name = "main_track"
        script.add_track(track_type=draft.TrackType.video, track_name=main_track_name, relative_index=0)
        logger.info(f"Added empty main track: {main_track_name}")
        
        # 保存草稿以确保主轨道被创建
        script.save()
        
        # 更新draft_meta_info.json中的draft_fold_path字段
        update_draft_meta_info(draft_id)
        
    except Exception as e:
        logger.error(f"create draft failed: {e}")
        raise CustomException(CustomError.DRAFT_CREATE_FAILED)

    # 缓存草稿
    update_cache(draft_id, script)

    logger.info(f"create draft success: {draft_id}")
    return config.DRAFT_URL + "?draft_id=" + draft_id