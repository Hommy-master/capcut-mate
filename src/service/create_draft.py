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
    基于模板创建剪映草稿的业务逻辑
    
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

    # 使用模板创建草稿
    try:
        # 复制模板到新草稿目录
        template_path = os.path.join(config.TEMPLATE_DIR, "default")
        draft_path = os.path.join(config.DRAFT_DIR, draft_id)
        if os.path.exists(draft_path): shutil.rmtree(draft_path)
        shutil.copytree(template_path, draft_path)
        
        # 在创建草稿时，确保两个文件都存在且内容相同
        draft_info_path = os.path.join(draft_path, "draft_info.json")
        draft_content_path = os.path.join(draft_path, "draft_content.json")
        
        # 加载模板草稿，然后修改配置
        script = draft.ScriptFile.load_template(draft_info_path)
        # 启用双文件兼容模式，这样保存时会自动同步两个文件
        script.dual_file_compatibility = True
        script.width, script.height = width, height
        script.content["canvas_config"]["width"], script.content["canvas_config"]["height"] = width, height
        
        # 保存修改后的草稿（会自动同步到两个文件）
        script.save_path = draft_content_path
        script.save()
        
        # 添加空的主轨道（仅当没有主轨道时添加）
        main_track_name = "main_track"
        script.add_track(track_type=draft.TrackType.video, track_name=main_track_name, relative_index=0)
        logger.info(f"Added empty main track: {main_track_name}")
        
        script.save()
        
    except Exception as e:
        logger.error(f"create draft failed: {e}")
        raise CustomException(CustomError.DRAFT_CREATE_FAILED)

    # 缓存草稿并返回URL
    update_cache(draft_id, script)
    logger.info(f"create draft success: {draft_id}")
    return config.DRAFT_URL + "?draft_id=" + draft_id