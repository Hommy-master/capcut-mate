from src.utils.logger import logger
from src.pyJianYingDraft import trange, IntroType, trange
import src.pyJianYingDraft as draft
from src.utils.draft_cache import DRAFT_CACHE
import os
from src.utils import helper
import config
import hashlib


def add_video_to_draft(draft_id, video_path) -> str:
    """
    向剪映草稿中添加本地视频
    
    Args:
        draft_id: 草稿ID（草稿文件夹名称）
        video_path: 本地视频文件路径
    
    Returns:
        draft_url: 草稿URL
        message: 响应消息，如果成功就返回"添加视频成功"，失败就返回具体错误信息
    """

    try:
        # 1. 从缓存中获取草稿
        script = DRAFT_CACHE[draft_id]

        # 2. 添加视频轨道
        script.add_track(draft.TrackType.video)
        logger.info(f"2. add video track: {draft_id}")
        
        # 3. 创建视频素材并添加到草稿
        video_segment = draft.VideoSegment(video_path, trange("0s", "4.2s"))
        video_segment.add_animation(IntroType.斜切)               # 添加一个入场动画"斜切"
        logger.info(f"3. add video segment: {video_segment}")
        
        # 4. 添加视频片段到轨道
        script.add_segment(video_segment)
        
        logger.info(f"4. add video segment to track: {video_segment}")

        # 5. 保存草稿
        script.save()

        logger.info(f"5. save draft: {draft_id}")
        
        return f"视频 '{os.path.basename(video_path)}' 成功添加到草稿 '{draft_id}' 的轨道末尾"
    except Exception as e:
        logger.error(f"add video to draft failed, error: {str(e)}")
        return f"操作失败: {str(e)}"

def add_videos(
    draft_url: str, 
    video_infos: str,
    alpha: float = 1.0, 
    scale_x: float = 1.0, 
    scale_y: float = 1.0, 
    transform_x: int = 0, 
    transform_y: int = 0
) -> (str, str):
    """
    添加视频到剪映草稿的业务逻辑
    文档：https://jy-api.fyshark.com/docs/API_ADD_VIDEOS.md
    
    Args:
        draft_url: ""  // [必选] 草稿URL
        video_infos: [ 
            {
                "video_url": "https://example.com/video1.mp4", // [必选] 视频文件的URL地址
                "width": 1920, // [必选] 视频宽度 
                "height": 1080, // [必选] 视频高度 
                "start": 0, // [必选] 视频在时间轴上的开始时间 
                "end": 12000000, // [必选] 视频在时间轴上的结束时间 
                "duration": 12000000, // [必选] 视频总时长(微秒)
                "mask": "", // 遮罩类型
                "transition": "", // 转场效果名称
                "transition_duration": 500000, // 转场持续时间(微秒)
                "volume": 1.0, // 音量大小[0, 1]
            } 
        ] // [必选]
        alpha: 全局透明度[0, 1]
        scale_x: X轴缩放比例
        scale_y: Y轴缩放比例
        transform_x: X轴位置偏移(像素)
        transform_y: Y轴位置偏移(像素)
    
    Returns:
        "message": "视频批量添加成功",
        "draft_url": "https://ts.fyshark.com/#/cozeToJianyin?drafId=...",
        "track_id": "video-track-uuid",
        "video_ids": ["video1-uuid", "video2-uuid", "video3-uuid"],
        "segment_ids": ["segment1-uuid", "segment2-uuid", "segment3-uuid"],
        "videos_count": 3,
        "total_duration": 15000000
    """

    logger.info(f"add_videos_service: {draft_url}, {video_infos}, {alpha}, {scale_x}, {scale_y}, {transform_x}, {transform_y}")

    # 提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        return "", "无效的草稿URL"

    # 创建保存视频资源的目录
    draft_dir = os.path.join(config.DRAFT_DIR, draft_id)
    draft_video_dir = os.path.join(draft_dir, "assets", "videos")
    os.makedirs(draft_video_dir, exist_ok=True)

    # 根据视频URL生成视频的文件名
    video_url = "https://assets.jcaigc.cn/min.mp4"
    video_filename = hashlib.md5(video_url.encode('utf-8')).hexdigest()

    # 下载视频
    video_path = helper.download(video_url, draft_video_dir, video_filename)

    # 添加视频
    message = add_video_to_draft(draft_id, video_path)

    return draft_url, message
