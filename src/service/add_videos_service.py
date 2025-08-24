from ast import Str
from numbers import Number
import uuid
from src.utils.logger import logger
from src.constants.base import DRAFT_DIR
from pyJianYingDraft import DraftFolder, VideoMaterial, VideoSegment, Track_type
from pyJianYingDraft import trange, Clip_settings, Transition_type, KeyframeProperty

def add_videos_service(
    draft_url: str, 
    video_infos: list,
    alpha: float = 1.0, 
    scale_x: float = 1.0, 
    scale_y: float = 1.0, 
    transform_x: int = 0, 
    transform_y: int = 0
) -> str:
    """
    添加视频到剪映草稿的业务逻辑
    文档：https://jy-api.fyshark.com/docs/API_ADD_VIDEOS.md
    
    Args:
        draft_url: 草稿URL
        video_infos: [ 
            {
                "video_url": "https://example.com/video1.mp4", // 视频文件的URL地址
                "width": 1920, // 视频宽度 
                "height": 1080, // 视频高度 
                "start": 0, // 视频在时间轴上的开始时间 
                "end": 12000000, // 视频在时间轴上的结束时间 
                "duration": 12000000, // 视频总时长(微秒)
                "mask": "", // 遮罩类型
                "transition": "", // 转场效果名称
                "transition_duration": 500000, // 转场持续时间(微秒)
                "volume": 1.0, // 音量大小[0, 1]
            } 
        ]
        alpha: 全局透明度[0, 1]
        scale_x: X轴缩放比例
        scale_y: Y轴缩放比例
        transform_x: X轴位置偏移(像素)
        transform_y: Y轴位置偏移(像素)
    
    Returns:
        {
            "status": "success",
            "message": "视频批量添加成功",
            "data": {
                "draft_url": "https://ts.fyshark.com/#/cozeToJianyin?drafId=...",
                "track_id": "video-track-uuid",
                "video_ids": ["video1-uuid", "video2-uuid", "video3-uuid"],
                "segment_ids": ["segment1-uuid", "segment2-uuid", "segment3-uuid"],
                "videos_count": 3,
                "total_duration": 15000000
            }
        }
    """

    # 初始化草稿文件夹
    draft_folder = DraftFolder(DRAFT_DIR)
    try:
        if draft_folder.has_draft(draft_url):
            script = Script(draft_folder.load_template(draft_url))
            logger.info(f"成功加载草稿: {draft_url}")
        else:
            # 如果草稿不存在，可以选择创建新草稿或抛出异常
            raise ValueError(f"草稿不存在: {draft_url}")
    except Exception as e:
        logger.error(f"初始化草稿失败: {str(e)}")
        raise
    
    return draft_url
