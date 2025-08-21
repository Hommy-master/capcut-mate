from numbers import Number
import uuid
from src.utils.logger import logger
import pyJianYingDraft as draft


def add_videos_service(draft_dir: str, draft_id: str, video_infos: dict, alpha: Number, scale_x: Number, scale_y: Number, transform_x: Number, transform_y: Number) -> str:
    """
    添加视频到剪映草稿的业务逻辑
    文档：https://jy-api.fyshark.com/docs/API_ADD_VIDEOS.md
    
    Args:
        draft_dir: 草稿保存目录
        draft_id: 草稿ID
        video_infos: [ 
            {
                "video_url": "https://example.com/video1.mp4", 
                "duration": 12000000, // 视频时长，以秒*1000000为单位 
                "width": 1920, // 视频宽度 
                "height": 1080, // 视频高度 
                "start": 0, // 视频在时间轴上的开始时间 
                "end": 12000000, // 视频在时间轴上的结束时间 
                "alpha": 1.0, // 视频透明度 
                "scale_x": 1.0, // 视频缩放比例X 
                "scale_y": 1.0, // 视频缩放比例Y 
                "transform_x": 0, // 视频变换X 
                "transform_y": 0 // 视频变换Y 
            } 
        ]
    
    Returns:
        生成的草稿ID
    """
    # 生成一个UUID作为草稿ID
    draft_id = uuid.uuid4()
    logger.info(f"draft_id: {draft_id}, draft_dir: {draft_dir}, width: {width}, height: {height}")

    try:
        # 初始化草稿文件夹
        draft_folder = draft.DraftFolder(draft_dir)
        # 创建新草稿
        script = draft_folder.create_draft(str(draft_id), width, height)
        # 保存草稿
        script.save()
        logger.info(f"create draft success: {draft_id}")
        return str(draft_id)
    except Exception as e:
        logger.error(f"create draft failed: {str(e)}")
        raise Exception(f"create draft failed: {str(e)}")
