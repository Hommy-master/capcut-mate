from src.utils.logger import logger
from src.pyJianYingDraft import trange, IntroType, trange
import src.pyJianYingDraft as draft
import os
from src.utils import helper
import config


def add_video_to_draft(draft_folder, draft_id, video_path):
    """
    向剪映草稿中添加本地视频
    
    :param draft_folder: 草稿根目录（如 "C:/JianyingPro Drafts"）
    :param draft_id: 草稿ID（草稿文件夹名称）
    :param video_path: 本地视频文件路径
    :return: 操作状态消息
    """
    try:
        # 1. 验证视频文件存在性
        if not os.path.exists(video_path):
            return f"视频文件不存在: {video_path}"
        
        # 2. 初始化草稿文件夹对象
        draft_folder_obj = draft.Draft_folder(draft_folder)

        logger.info("2. init draft")
        
        # 3. 加载指定草稿
        script = draft_folder_obj.load_template(draft_id)
        # 添加音频、视频和文本轨道
        script.add_track(draft.TrackType.audio).add_track(draft.TrackType.video).add_track(draft.TrackType.text)

        logger.info(f"3. load draft: {draft_id}")
        
        # 4. 添加视频轨道
        video_track = script.get_imported_track(draft.TrackType.video)
        logger.info(f"4. add video track: {video_track}")
        
        # 5. 创建视频素材并添加到草稿
        video_segment = draft.VideoSegment(video_path, trange("0s", "4.2s"))
        video_segment.add_animation(IntroType.斜切)               # 添加一个入场动画"斜切"
        logger.info(f"5. add video segment: {video_segment}")
        
        # 6. 添加视频片段到轨道
        script.add_segment(video_segment)
        
        logger.info(f"6. add video segment to track: {video_segment}")

        # 7. 保存草稿
        script.save()

        logger.info(f"7. save draft: {draft_id}")
        
        return f"视频 '{os.path.basename(video_path)}' 成功添加到草稿 '{draft_id}' 的轨道末尾"
    
    except Exception as e:
        logger.error(f"10. error: {str(e)}")
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
    if not draft_id:
        return "", "无效的草稿URL"

    # 下载视频
    video_path = helper.download("https://assets.jcaigc.cn/min.mp4", ".", "test")

    # 添加视频
    add_video_to_draft(config.DRAFT_DIR, draft_id, video_path)

    return draft_url, "批量添加视频成功"
