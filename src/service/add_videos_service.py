from src.utils.logger import logger
from src.constants.base import DRAFT_DIR
from pyJianYingDraft import trange, DraftFolder, Track_type
from urllib.parse import urlparse, parse_qs
import os
import pyJianYingDraft as draft


def extract_draft_id(url):
    """
    从URL中提取draft_id参数值
    :param url: 包含查询参数的完整URL字符串
    :return: draft_id的值（字符串），若不存在则返回None
    """
    # 解析URL获取查询参数字符串
    parsed_url = urlparse(url)
    query_string = parsed_url.query
    
    # 将查询字符串解析为字典
    query_params = parse_qs(query_string)
    
    # 提取draft_id参数（注意值以列表形式存储）
    draft_id_list = query_params.get('draft_id', [])
    
    # 返回第一个值（通常参数唯一）
    return draft_id_list[0] if draft_id_list else None

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
        
        # 3. 加载指定草稿
        script = draft_folder_obj.load_template(draft_id)
        
        # 4. 添加视频轨道（如果不存在）
        video_tracks = script.get_tracks(Track_type.video)
        if not video_tracks:
            video_track = script.add_track(Track_type.video)
        else:
            video_track = video_tracks[0]  # 使用第一个视频轨道
        
        # 5. 创建视频素材并添加到草稿
        video_material = draft.Video_material(video_path)
        script.add_material(video_material)
        
        # 6. 计算轨道当前总时长（用于确定新视频位置）
        current_duration = script.duration if hasattr(script, 'duration') else 0
        
        # 7. 创建视频片段（添加到轨道末尾）
        video_segment = draft.Video_segment(
            material=video_material,
            target_timerange=trange(current_duration, video_material.duration),
            source_timerange=trange(0, video_material.duration),
            speed=1.0,
            clip_settings=draft.Clip_settings(
                scale=1.0,          # 缩放比例（1.0为原始大小）
                alpha=1.0           # 透明度（1.0为完全不透明）
            )
        )
        
        # 8. 添加视频片段到轨道
        script.add_segment(video_segment, track=video_track)
        
        # 9. 保存草稿
        script.save()
        
        return f"视频 '{os.path.basename(video_path)}' 成功添加到草稿 '{draft_id}' 的轨道末尾"
    
    except Exception as e:
        return f"操作失败: {str(e)}"

def add_videos_service(
    draft_url: str, 
    video_infos: str,
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

    logger.info(f"add_videos_service: {draft_url}, {video_infos}, {alpha}, {scale_x}, {scale_y}, {transform_x}, {transform_y}")

    # 提取草稿ID
    draft_id = extract_draft_id(draft_url)
    if not draft_id:
        raise ValueError("URL中未包含有效draft_id参数")

    # 初始化草稿文件夹
    draft_folder = DraftFolder(DRAFT_DIR)
    try:
        if draft_folder.has_draft(draft_id):
            script = draft_folder.load_template(draft_id)
            logger.info(f"成功加载草稿: {draft_url}")
        else:
            raise ValueError(f"草稿不存在: {draft_url}")
    except Exception as e:
        logger.error(f"初始化草稿失败: {str(e)}")
        raise

    # 添加视频
    try:
        # 添加视频轨道
        video_track = script.add_track(Track_type.Video)


        script.add_material(video_infos, track_id)
    except Exception as e:
        logger.error(f"添加视频失败: {str(e)}")
        raise
    
    return draft_url
