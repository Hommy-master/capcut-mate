from src.pyJianYingDraft.video_segment import VideoSegment


from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile, trange, IntroType
import src.pyJianYingDraft as draft
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
import os
from src.utils import helper
from src.utils.download import download
import config
import json
from typing import List, Dict, Any, Tuple, Optional


def add_videos(
    draft_url: str, 
    video_infos: str,
    alpha: float = 1.0, 
    scale_x: float = 1.0, 
    scale_y: float = 1.0, 
    transform_x: int = 0, 
    transform_y: int = 0
) -> Tuple[str, str, List[str], List[str]]:
    """
    添加视频到剪映草稿的业务逻辑
    
    Args:
        draft_url: ""  // [必选] 草稿URL
        video_infos: [ 
            {
                "video_url": "https://example.com/video1.mp4", // [必选] 视频文件的URL地址
                "width": 1920, // [必选] 视频宽度 
                "height": 1080, // [必选] 视频高度 
                "start": 0.0, // [必选] 视频在时间轴上的开始时间 (微秒)
                "end": 12000000.0, // [必选] 视频在时间轴上的结束时间 (微秒)
                "duration": 12000000.0, // [可选] 视频总时长(微秒)，如果不传则默认为end-start
                "mask": "", // 遮罩类型[可选]，默认值为None
                "transition": "", // 转场效果名称[可选]，默认值为None
                "transition_duration": 500000.0, // 转场持续时间(微秒)[可选]，默认值为500000
                "volume": 1.0, // 音量大小[0, 1][可选]，默认值为1.0
            } 
        ] // [必选]
        alpha: 全局透明度[0, 1][可选]，默认值为1.0
        scale_x: X轴缩放比例[可选]，默认值为1.0
        scale_y: Y轴缩放比例[可选]，默认值为1.0
        transform_x: X轴位置偏移(像素)[可选]，默认值为0
        transform_y: Y轴位置偏移(像素)[可选]，默认值为0
    
    Returns:
        "draft_url": "https://capcut-mate.jcaigc.cn/openapi/capcut-mate/v1/get_draft?draft_id=...",
        "track_id": "video-track-uuid",
        "video_ids": ["video1-uuid", "video2-uuid", "video3-uuid"],
        "segment_ids": ["segment1-uuid", "segment2-uuid", "segment3-uuid"],
        "videos_count": 3, [未用]
        "total_duration": 15000000 [未用]

    Raises:
        CustomException: 视频批量添加失败
    """
    logger.info(f"add_videos, draft_url: {draft_url}, video_infos: {video_infos}, alpha: {alpha}, scale_x: {scale_x}, scale_y: {scale_y}, transform_x: {transform_x}, transform_y: {transform_y}")

    # 1. 提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    # 2. 创建保存视频资源的目录
    draft_dir = os.path.join(config.DRAFT_DIR, draft_id)
    draft_video_dir = os.path.join(draft_dir, "assets", "videos")
    os.makedirs(name=draft_video_dir, exist_ok=True)

    # 3. 解析视频信息
    videos = parse_video_data(json_str=video_infos)
    if len(videos) == 0:
        logger.info(f"No video info, draft_id: {draft_id}")
        raise CustomException(CustomError.INVALID_VIDEO_INFO)

    # 4. 从缓存中获取草稿
    script: ScriptFile = DRAFT_CACHE[draft_id]

    # 5. 添加视频轨道（明确说明不使用主轨道，并设置合适的渲染层级）
    track_name = f"video_track_{helper.gen_unique_id()}"
    # 设置 relative_index=10 确保视频轨道在主视频轨道之上，避免与主轨道冲突
    script.add_track(track_type=draft.TrackType.video, track_name=track_name, relative_index=10)

    # 6. 遍历视频信息，添加视频到草稿中的指定轨道，收集片段ID
    segment_ids = []
    for video in videos:
        segment_id = add_video_to_draft(script, track_name, draft_video_dir=draft_video_dir, video=video,
                                      alpha=alpha, scale_x=scale_x, scale_y=scale_y, 
                                      transform_x=transform_x, transform_y=transform_y)
        segment_ids.append(segment_id)
    logger.info(f"segment_ids: {segment_ids}")

    # 7. 保存草稿
    script.save()

    # 8. 获取当前视频轨道id
    track_id = ""
    for key in script.tracks.keys():
        if script.tracks[key].name == track_name:
            track_id = script.tracks[key].track_id
            break
    logger.info(f"draft_id: {draft_id}, track_id: {track_id}")

    # 9. 获取当前所有视频资源ID（全局唯一ID）
    video_ids = [video.material_id for video in script.materials.videos]
    logger.info(f"draft_id: {draft_id}, video_ids: {video_ids}")

    # TODO: 这里还是有点小问题，为什么得到的video_ids与segment_ids的结果一样
    return draft_url, track_id, video_ids, segment_ids

def add_video_to_draft(
    script: ScriptFile,
    track_name: str,
    draft_video_dir: str,
    video: dict, 
    alpha: float = 1.0, 
    scale_x: float = 1.0, 
    scale_y: float = 1.0, 
    transform_x: int = 0, 
    transform_y: int = 0
    ) -> str:
    """
    向剪映草稿中添加视频
    
    Args:
        script: 草稿文件对象
        track_name: 视频轨道名称
        draft_video_dir: 视频资源目录
        video: 视频信息字典，包含以下字段：
            video_url: 视频URL
            width: 视频宽度(像素)
            height: 视频高度(像素)
            start: 视频在时间轴上的开始时间(微秒)
            end: 视频在时间轴上的结束时间(微秒)
            duration: 视频总时长(微秒)，可选，默认为end-start
            mask: 遮罩类型(可选)
            transition: 转场效果(可选)
            transition_duration: 转场持续时间(可选)
            volume: 音量大小(可选)
        alpha: 视频透明度
        scale_x: 横向缩放
        scale_y: 纵向缩放
        transform_x: X轴位置偏移(像素)
        transform_y: Y轴位置偏移(像素)       
    
    Returns:
        segment_id: 片段ID
    """
    try:
        # 0. 下载视频
        video_path = download(url=video['video_url'], save_dir=draft_video_dir)

        # 1. 获取视频播放时长（target duration）
        target_duration = video.get('duration', video['end'] - video['start'])

        # 2. 创建图像调节设置
        clip_settings = draft.ClipSettings(
            alpha=alpha,
            scale_x=scale_x,
            scale_y=scale_y,
            transform_x=transform_x / video['width'],  # 转换为半画布宽单位
            transform_y=transform_y / video['height']  # 转换为半画布高单位
        )
        
        # 3. 计算在时间轴上的显示时长（source duration）
        display_duration = video['end'] - video['start']
        
        # 4. 创建视频素材
        video_material = draft.VideoMaterial(video_path)
        
        # 5. 创建视频片段
        video_segment = draft.VideoSegment(
            material=video_material, 
            target_timerange=trange(start=video['start'], duration=display_duration),
            source_timerange=trange(start=0, duration=min(video_material.duration, display_duration)),
            speed=1.0,  # 保持原始速度
            volume=video.get('volume', 1.0),
            clip_settings=clip_settings
        )
        logger.info(f"video_path: {video_path}, start: {video['start']}, target_duration: {target_duration}, display_duration: {display_duration}, volume: {video.get('volume', 1.0)}")

        # 6. 添加转场效果（如果指定了）
        transition_name = video.get('transition')
        if transition_name:
            transition_type = find_transition_type_by_name(transition_name)
            if transition_type:
                transition_duration = video.get('transition_duration', 500000)  # 默认500ms
                try:
                    video_segment.add_transition(transition_type, duration=transition_duration)
                    logger.info(f"Added transition '{transition_name}' with duration {transition_duration}us")
                except Exception as e:
                    logger.warning(f"Failed to add transition '{transition_name}': {str(e)}")
            else:
                logger.warning(f"Transition type not found for name: {transition_name}")

        # 7. 向指定轨道添加片段
        script.add_segment(video_segment, track_name)

        # 8. 返回片段ID（注意：是segment_id而不是material_id）
        return video_segment.segment_id
    except CustomException:
        logger.info(f"Add video to draft failed, draft_video_dir: {draft_video_dir}, video: {video}")
        raise
    except Exception as e:
        logger.error(f"Add video to draft failed, error: {str(e)}")
        raise CustomException(err=CustomError.VIDEO_ADD_FAILED)


def find_transition_type_by_name(transition_name: str) -> Optional[draft.TransitionType]:
    """
    根据转场名称查找对应的转场类型
    
    Args:
        transition_name: 转场名称
    
    Returns:
        对应的转场类型枚举，如果未找到则返回None
    """
    if not transition_name:
        return None
        
    try:
        return draft.TransitionType.from_name(transition_name)
    except ValueError:
        logger.warning(f"Transition type not found for name: {transition_name}")
        return None


def parse_video_data(json_str: str) -> List[Dict[str, Any]]:
    """
    解析视频数据的JSON字符串，处理可选字段的默认值
    
    Args:
        json_str: 包含视频数据的JSON字符串，格式如下：
        [ 
            {
                "video_url": "https://example.com/video1.mp4", // [必选] 视频文件的URL地址
                "width": 1920, // [必选] 视频宽度 
                "height": 1080, // [必选] 视频高度 
                "start": 0.0, // [必选] 视频在时间轴上的开始时间 
                "end": 12000000.0, // [必选] 视频在时间轴上的结束时间 
                "duration": 12000000.0, // [可选] 视频总时长(微秒)，如果不传则默认为end-start
                "mask": "", // 遮罩类型[可选]，默认值为None
                "transition": "", // 转场效果名称[可选]，默认值为None
                "transition_duration": 500000.0, // 转场持续时间(微秒)[可选]，默认值为500000
                "volume": 1.0, // 音量大小[0, 1][可选]，默认值为1.0
            } 
        ]
        
    Returns:
        包含视频对象的数组，每个对象都处理了默认值
        
    Raises:
        json.JSONDecodeError: 当JSON格式错误时抛出
        KeyError: 当缺少必选字段时抛出
    """
    try:
        # 解析JSON字符串
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise CustomException(CustomError.INVALID_VIDEO_INFO, f"JSON parse error: {e.msg}")
    
    # 确保输入是列表
    if not isinstance(data, list):
        raise CustomException(CustomError.INVALID_VIDEO_INFO, "video_infos should be a list")
    
    result = []
    
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise CustomException(CustomError.INVALID_VIDEO_INFO, f"the {i}th item should be a dict")
        
        # 检查必选字段
        required_fields = ["video_url", "width", "height", "start", "end"]
        missing_fields = [field for field in required_fields if field not in item]
        
        if missing_fields:
            raise CustomException(CustomError.INVALID_VIDEO_INFO, f"the {i}th item is missing required fields: {', '.join(missing_fields)}")
        
        # 如果没有提供duration，则计算为end-start
        duration = item.get("duration", item["end"] - item["start"])
        
        # 创建处理后的对象，设置默认值
        processed_item = {
            "video_url": item["video_url"],
            "width": item["width"],
            "height": item["height"],
            "start": item["start"],
            "end": item["end"],
            "duration": duration,
            "mask": item.get("mask", None),  # 默认值 None
            "transition": item.get("transition", None),  # 默认值 None
            "transition_duration": item.get("transition_duration", 500000),  # 默认值 500000
            "volume": item.get("volume", 1.0)  # 默认值 1.0
        }
        
        # 验证数值范围
        if processed_item["volume"] < 0 or processed_item["volume"] > 1:
            # 音量值必须在[0, 1]范围内，给默认值
            processed_item["volume"] = 1.0
        
        if processed_item["transition_duration"] < 0:
            # 转场持续时间必须为非负数，给默认值
            processed_item["transition_duration"] = 500000
        
        result.append(processed_item)
    
    return result
