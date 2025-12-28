from src.utils.logger import logger
import config
import src.pyJianYingDraft as draft
from src.utils.draft_cache import update_cache
from exceptions import CustomException, CustomError
import datetime
import uuid
import os
import shutil


def generate_unique_draft_id():
    """生成唯一的草稿ID"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    return f"{timestamp}{unique_id}"


def ensure_template_exists():
    """确保默认模板存在于草稿目录中"""
    # 使用绝对路径构建模板源路径
    current_file_dir = os.path.dirname(os.path.abspath(__file__))  # src/service
    src_dir = os.path.dirname(current_file_dir)  # src
    project_root = os.path.dirname(src_dir)  # 项目根目录
    template_source_path = os.path.join(project_root, "template", "default")
    template_target_path = os.path.join(config.DRAFT_DIR, "default")
    
    if not os.path.exists(template_target_path):
        os.makedirs(config.DRAFT_DIR, exist_ok=True)
        shutil.copytree(template_source_path, template_target_path)
    
    return template_target_path


def fix_template_tracks(template_target_path):
    """修复模板中的轨道，确保所有轨道都有name字段"""
    draft_content_path = os.path.join(template_target_path, "draft_content.json")
    if os.path.exists(draft_content_path):
        import json
        with open(draft_content_path, 'r', encoding="utf-8") as f:
            template_data = json.load(f)
        
        # 确保所有轨道都有name字段
        for track in template_data.get("tracks", []):
            if "name" not in track:
                # 使用type作为名称，如果type存在的话
                track_type = track.get("type", "unknown")
                track["name"] = f"{track_type}_track"
        
        # 保存修改后的模板
        with open(draft_content_path, 'w', encoding="utf-8") as f:
            json.dump(template_data, f, ensure_ascii=False, indent=4)


def check_main_track_exists(script):
    """检查是否已存在主轨道"""
    main_track_name = "main_track"
    main_track_exists = main_track_name in script.tracks
    if not main_track_exists:
        for track in script.imported_tracks:
            try:
                if hasattr(track, 'name') and track.name == main_track_name:
                    main_track_exists = True
                    break
            except AttributeError:
                # 如果track没有name属性，跳过
                continue
    return main_track_exists


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
    draft_folder = draft.Draft_folder(config.DRAFT_DIR)

    # 使用默认模板创建剪映草稿
    try:
        # 确保默认模板存在
        template_target_path = ensure_template_exists()
        
        # 生成唯一的草稿ID
        draft_id = generate_unique_draft_id()
        logger.info(f"draft_id: {draft_id}, width: {width}, height: {height}")
        
        # 修复模板中的轨道
        fix_template_tracks(template_target_path)
        
        # 使用default模板来创建新草稿
        script = draft_folder.duplicate_as_template("default", draft_id, allow_replace=True)
        
        # 确保草稿中的ID与文件夹ID一致
        script.content["id"] = draft_id
        
        # 更新草稿的画布尺寸以匹配请求的尺寸
        script.width = width
        script.height = height
        script.content["canvas_config"]["width"] = width
        script.content["canvas_config"]["height"] = height
        
        # 添加空的主轨道（仅当没有主轨道时添加）
        main_track_exists = check_main_track_exists(script)
        if not main_track_exists:
            script.add_track(track_type=draft.TrackType.video, track_name="main_track", relative_index=0)
            logger.info(f"Added empty main track: main_track")
        
        # 保存草稿以确保更改被保存
        script.save()
        
    except Exception as e:
        logger.error(f"create draft failed: {e}")
        raise CustomException(CustomError.DRAFT_CREATE_FAILED)

    # 缓存草稿
    update_cache(draft_id, script)

    logger.info(f"create draft success: {draft_id}")
    return config.DRAFT_URL + "?draft_id=" + draft_id