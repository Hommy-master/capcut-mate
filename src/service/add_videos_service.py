from numbers import Number
import uuid
from src.utils.logger import logger
from pyJianYingDraft import DraftFolder, VideoMaterial, VideoSegment, Script, Track_type
from pyJianYingDraft import trange, Clip_settings, Transition_type, KeyframeProperty, SEC

def add_videos_service(
    draft_url: str, 
    video_infos: list,
    alpha: Number = 1.0, 
    scale_x: Number = 1.0, 
    scale_y: Number = 1.0, 
    transform_x: Number = 0, 
    transform_y: Number = 0
) -> dict:
    """
    添加视频到剪映草稿的业务逻辑
    文档：https://jy-api.fyshark.com/docs/API_ADD_VIDEOS.md
    
    Args:
        draft_dir: 草稿保存目录
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
    draft_folder = DraftFolder(draft_dir)
    if draft_folder.has_draft(draft_url):
        script = Script(draft_folder.load_template(draft_url))

    # 获取视频轨道（默认使用第一个视频轨道）
    video_track = script.get_tracks(Track_type.video)[0]
    track_id = video_track.name  # 轨道唯一标识
    # 初始化返回数据
    video_ids = []
    segment_ids = []
    total_duration = 0
    # 遍历添加所有视频
    for idx, video_info in enumerate(video_infos):
        # 1. 创建视频素材对象
        video_material = draft.VideoMaterial(video_info["video_url"])
        script.add_material(video_material)
        video_ids.append(str(uuid.uuid4()))  # 生成视频唯一ID
        
        # 2. 创建视频片段
        start = video_info["start"]
        duration = video_info["duration"]
        video_segment = draft.VideoSegment(
            video_material,
            trange(start, duration),
            clip_settings=Clip_settings(
                alpha=alpha,
                scale_x=scale_x,
                scale_y=scale_y,
                transform_x=transform_x,
                transform_y=transform_y
            )
        )
        
        # 3. 添加音量关键帧
        video_segment.add_keyframe(KeyframeProperty.volume, 0, video_info["volume"])
        
        # 4. 添加转场效果（首片段不添加）
        if idx > 0 and video_info["transition_duration"] > 0:
            prev_segment = script.get_segments(video_track)[-1]
            prev_segment.add_transition(
                Transition_type.溶解,  # 默认转场类型
                duration=video_info["transition_duration"]
            )
        
        # 5. 添加到轨道
        script.add_segment(video_segment, track=video_track)
        segment_ids.append(video_segment.segment_id)
        
        # 更新总时长
        total_duration = max(total_duration, start + duration)
    
    # 保存草稿文件
    script.save()
    
    # 返回结构化结果
    return {
        "status": "success",
        "message": "视频批量添加成功",
        "data": {
            "draft_url": draft_url,
            "track_id": track_id,
            "video_ids": video_ids,
            "segment_ids": segment_ids,
            "videos_count": len(video_infos),
            "total_duration": total_duration
        }
    }