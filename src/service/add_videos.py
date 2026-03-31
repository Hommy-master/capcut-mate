from src.pyJianYingDraft.video_segment import VideoSegment

import asyncio
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
from src.utils.draft_lock_manager import get_draft_lock_manager


def add_videos(
    draft_url: str, 
    video_infos: str,
    scene_timelines: Optional[List[Dict[str, int]]] = None,
    alpha: float = 1.0, 
    scale_x: float = 1.0, 
    scale_y: float = 1.0, 
    transform_x: int = 0, 
    transform_y: int = 0
) -> Tuple[str, str, List[str], List[str]]:
    """
    添加视频到剪映草稿的业务逻辑（同步版本，兼容旧代码）
    
    Args:
        draft_url: ""  // [必选] 草稿 URL
        video_infos: [ 
            {
                "video_url": "https://example.com/video1.mp4", // [必选] 视频文件的 URL 地址
                "width": 1920, // [可选] 视频宽度，不传则自动获取视频文件尺寸
                "height": 1080, // [可选] 视频高度，不传则自动获取视频文件尺寸
                "start": 0.0, // [必选] 视频在时间轴上的开始时间 (微秒)
                "end": 12000000.0, // [必选] 视频在时间轴上的结束时间 (微秒)
                "duration": 12000000.0, // [可选] 视频总时长 (微秒)，如果不传则默认为 end-start
                "mask": "", // 遮罩类型 [可选]，默认值为 None
                "transition": "", // 转场效果名称 [可选]，默认值为 None
                "transition_duration": 500000.0, // 转场持续时间 (微秒)[可选]，默认值为 500000
                "volume": 1.0, // 音量大小 [0, 10][可选]，默认值为 1.0，10 为最大音量
            } 
        ] // [必选]
        scene_timelines: [ // [可选] 场景时间线数组，用于视频变速，与 video_infos 一一对应
            {
                "start": 0, // [必选] 场景开始时间 (微秒)
                "end": 6000000 // [必选] 场景结束时间 (微秒)
            }
        ]
        // 变速原理：speed = (video.end - video.start) / (scene_timeline.end - scene_timeline.start)
        // 示例：视频时间轴 0-2000000(2 秒)，场景时间线 0-1000000(1 秒)，则视频以 2 倍速播放
        // 如果不提供 scene_timelines 或对应项为 None，视频以正常速度 (1.0 倍) 播放
        alpha: 全局透明度 [0, 1][可选]，默认值为 1.0
        scale_x: X 轴缩放比例 [可选]，默认值为 1.0
        scale_y: Y 轴缩放比例 [可选]，默认值为 1.0
        transform_x: X 轴位置偏移 (像素)[可选]，默认值为 0
        transform_y: Y 轴位置偏移 (像素)[可选]，默认值为 0
    
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
    # 调用内部处理函数（不获取锁，由外层控制）
    return _add_videos_internal(
        draft_url=draft_url,
        video_infos=video_infos,
        scene_timelines=scene_timelines,
        alpha=alpha,
        scale_x=scale_x,
        scale_y=scale_y,
        transform_x=transform_x,
        transform_y=transform_y
    )


async def add_videos_async(
    draft_url: str, 
    video_infos: str,
    scene_timelines: Optional[List[Dict[str, int]]] = None,
    alpha: float = 1.0, 
    scale_x: float = 1.0, 
    scale_y: float = 1.0, 
    transform_x: int = 0, 
    transform_y: int = 0,
    lock_timeout: float = 30.0
) -> Tuple[str, str, List[str], List[str]]:
    """
    添加视频到剪映草稿的异步版本（带并发锁保护）
    
    功能：
    1. 使用 DraftLockManager 防止同一草稿的并发写操作
    2. 支持超时控制，避免无限等待
    3. 自动释放锁，即使发生异常
    
    Args:
        draft_url: 草稿 URL，格式：".../get_draft?draft_id=xxx"
        video_infos: JSON 字符串，包含视频信息列表，详见 add_videos 函数
        scene_timelines: 场景时间线列表，用于视频变速，与 video_infos 一一对应
        alpha: 全局透明度 [0, 1]，默认 1.0
        scale_x: X 轴缩放比例，默认 1.0
        scale_y: Y 轴缩放比例，默认 1.0
        transform_x: X 轴位置偏移（像素），默认 0
        transform_y: Y 轴位置偏移（像素），默认 0
        lock_timeout: 获取锁的超时时间（秒），默认 30 秒
    
    Returns:
        tuple: (draft_url, track_id, video_ids, segment_ids)
    
    Raises:
        CustomException: 视频添加失败或获取锁超时
        asyncio.TimeoutError: 等待锁超时时抛出
    
    Example:
        >>> result = await add_videos_async(
        ...     draft_url="http://.../draft_id=123",
        ...     video_infos='[{"video_url":"...", "start":0, "end":5000000}]'
        ... )
    """
    # 提取草稿 ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if not draft_id:
        raise CustomException(CustomError.INVALID_DRAFT_URL)
    
    # 获取锁管理器
    lock_manager = get_draft_lock_manager()
    
    # 尝试获取锁
    try:
        await lock_manager.acquire_lock(draft_id, timeout=lock_timeout)
        logger.info(f"Lock acquired for draft_id: {draft_id}")
    except asyncio.TimeoutError:
        logger.error(f"Timeout waiting for lock on draft_id: {draft_id}")
        raise CustomException(
            CustomError.VIDEO_ADD_FAILED,
            f"Failed to acquire lock for draft {draft_id} after {lock_timeout}s"
        )
    
    try:
        # 执行实际的添加操作
        result = _add_videos_internal(
            draft_url=draft_url,
            video_infos=video_infos,
            scene_timelines=scene_timelines,
            alpha=alpha,
            scale_x=scale_x,
            scale_y=scale_y,
            transform_x=transform_x,
            transform_y=transform_y
        )
        return result
    finally:
        # 确保释放锁
        await lock_manager.release_lock(draft_id)
        logger.info(f"Lock released for draft_id: {draft_id}")


def _add_videos_internal(
    draft_url: str,
    video_infos: str,
    scene_timelines: Optional[List[Dict[str, int]]] = None,
    alpha: float = 1.0,
    scale_x: float = 1.0,
    scale_y: float = 1.0,
    transform_x: int = 0,
    transform_y: int = 0
) -> Tuple[str, str, List[str], List[str]]:
    """
    添加视频的内部处理函数（无锁，需外层控制并发）
    
    此函数不包含锁机制，必须在已获取锁的情况下调用
    
    Args:
        draft_url: 草稿 URL
        video_infos: 视频信息 JSON 字符串
        scene_timelines: 场景时间线列表
        alpha: 全局透明度
        scale_x: X 轴缩放比例
        scale_y: Y 轴缩放比例
        transform_x: X 轴位置偏移
        transform_y: Y 轴位置偏移
    
    Returns:
        tuple: (draft_url, track_id, video_ids, segment_ids)
    """
    logger.info(f"_add_videos_internal, draft_url: {draft_url}")

    # 1. 提取草稿 ID
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

    # 3.5 保存每个视频的原始时间信息（用于变速后的连续性计算）
    for video in videos:
        video['original_start'] = video['start']
        video['original_end'] = video['end']
    
    # 3.6 处理场景时间线（可选，已是对象数组）
    logger.info(f"Parsed {len(videos)} videos, scene_timelines: {scene_timelines}")

    # 4. 从缓存中获取草稿
    script: ScriptFile = DRAFT_CACHE[draft_id]

    # 5. 添加视频轨道（明确说明不使用主轨道，并设置合适的渲染层级）
    track_name = f"video_track_{helper.gen_unique_id()}"
    # 设置 relative_index=10 确保视频轨道在主视频轨道之上，避免与主轨道冲突
    script.add_track(track_type=draft.TrackType.video, track_name=track_name, relative_index=10)

    # 6. 遍历视频信息，添加视频到草稿中的指定轨道，收集片段 ID
    segment_ids = []
    current_track_end = 0  # 跟踪当前轨道上的实际结束位置（用于处理变速后的连续性）
    for i, video in enumerate(videos):
        # 获取对应的场景时间线（如果有）
        scene_timeline = scene_timelines[i] if scene_timelines and i < len(scene_timelines) else None
        
        # 自动调整视频的 start 时间，确保与前一个视频连续（处理变速后的间隙问题）
        if i > 0 and current_track_end > 0:
            # 使用原始时长计算新的 end
            original_duration = video['original_end'] - video['original_start']
            video['start'] = current_track_end
            video['end'] = video['start'] + original_duration
            logger.info(f"Adjusted video {i} start time to {video['start']} for continuity, original_duration: {original_duration}")
        
        segment_id, actual_duration = add_video_to_draft(script, track_name, draft_video_dir=draft_video_dir, video=video,
                                      scene_timeline=scene_timeline,
                                      alpha=alpha, scale_x=scale_x, scale_y=scale_y, 
                                      transform_x=transform_x, transform_y=transform_y)
        segment_ids.append(segment_id)
        # 更新当前轨道结束位置（使用实际播放时长，而非原始时间轴时长）
        current_track_end = video['start'] + actual_duration
        logger.info(f"Video {i} added, track end position: {current_track_end}, actual_duration: {actual_duration}")
    logger.info(f"segment_ids: {segment_ids}")

    # 7. 保存草稿
    script.save()

    # 8. 获取当前视频轨道 id
    track_id = ""
    for key in script.tracks.keys():
        if script.tracks[key].name == track_name:
            track_id = script.tracks[key].track_id
            break
    logger.info(f"draft_id: {draft_id}, track_id: {track_id}")

    # 9. 获取当前所有视频资源 ID（全局唯一 ID）
    video_ids = [video.material_id for video in script.materials.videos]
    logger.info(f"draft_id: {draft_id}, video_ids: {video_ids}")

    # TODO: 这里还是有点小问题，为什么得到的 video_ids 与 segment_ids 的结果一样
    return draft_url, track_id, video_ids, segment_ids

def add_video_to_draft(
    script: ScriptFile,
    track_name: str,
    draft_video_dir: str,
    video: dict, 
    scene_timeline: Optional[Dict[str, int]] = None,
    alpha: float = 1.0, 
    scale_x: float = 1.0, 
    scale_y: float = 1.0, 
    transform_x: int = 0, 
    transform_y: int = 0
    ) -> Tuple[str, int]:
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
        scene_timeline: 场景时间线字典，包含以下字段：
            start: 场景开始时间(微秒)
            end: 场景结束时间(微秒)
            用于计算视频变速：speed = (video.end - video.start) / (scene_timeline.end - scene_timeline.start)
        alpha: 视频透明度
        scale_x: 横向缩放
        scale_y: 纵向缩放
        transform_x: X轴位置偏移(像素)
        transform_y: Y轴位置偏移(像素)       
    
    Returns:
        segment_id: 片段ID
        actual_duration: 视频在轨道上的实际播放时长(微秒)，考虑变速后的时长
    """
    try:
        # 0. 下载视频
        video_path = download(url=video['video_url'], save_dir=draft_video_dir)

        # 1. 创建视频素材
        video_material = draft.VideoMaterial(video_path)
        
        # 2. 获取视频播放时长（target duration）
        target_duration = video.get('duration', video['end'] - video['start'])
        
        # 获取草稿的宽高用于transform坐标转换
        draft_width = script.width
        draft_height = script.height
        logger.info(f"draft size: {draft_width}x{draft_height}, transform_x: {transform_x}, transform_y: {transform_y}")

        # 4. 创建图像调节设置
        clip_settings = draft.ClipSettings(
            alpha=alpha,
            scale_x=scale_x,
            scale_y=scale_y,
            transform_x=transform_x / draft_width,  #半画布宽单位
            transform_y=transform_y / draft_height  #为半画布高单位
        )
        
        # 5. 计算在时间轴上的显示时长（source duration）
        display_duration = video['end'] - video['start']
        
        # 5.5 计算变速（如果提供了场景时间线）
        speed = 1.0
        actual_duration = display_duration  # 默认实际时长等于显示时长
        if scene_timeline:
            scene_duration = scene_timeline['end'] - scene_timeline['start']
            if scene_duration > 0:
                # speed = 时间轴时长 / 场景时长
                # 例如：时间轴2秒，场景1秒，则speed=2（2倍速）
                speed = display_duration / scene_duration
                actual_duration = scene_duration  # 实际播放时长为场景时长
                logger.info(f"Video speed calculated: {speed}x (display_duration={display_duration}, scene_duration={scene_duration})")
        
        # 6. 创建视频片段
        # 用户传入 volume 范围为 [0, 10]，剪映内部范围为 [0, 10]
        raw_volume = video.get('volume', 1.0)
        video_segment = draft.VideoSegment(
            material=video_material, 
            target_timerange=trange(start=video['start'], duration=display_duration),
            source_timerange=trange(start=0, duration=min(video_material.duration, display_duration)),
            speed=speed,  # 使用计算出的速度
            volume=raw_volume,
            clip_settings=clip_settings
        )
        logger.info(f"video_path: {video_path}, start: {video['start']}, target_duration: {target_duration}, display_duration: {display_duration}, speed: {speed}, raw_volume: {raw_volume}")

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

        # 8. 返回片段ID和实际播放时长（注意：是segment_id而不是material_id）
        return video_segment.segment_id, actual_duration
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
                "width": 1920, // [可选] 视频宽度，不传则自动获取视频文件尺寸
                "height": 1080, // [可选] 视频高度，不传则自动获取视频文件尺寸
                "start": 0.0, // [必选] 视频在时间轴上的开始时间 
                "end": 12000000.0, // [必选] 视频在时间轴上的结束时间 
                "duration": 12000000.0, // [可选] 视频总时长(微秒)，如果不传则默认为end-start
                "mask": "", // 遮罩类型[可选]，默认值为None
                "transition": "", // 转场效果名称[可选]，默认值为None
                "transition_duration": 500000.0, // 转场持续时间(微秒)[可选]，默认值为500000
                "volume": 1.0, // 音量大小[0, 10][可选]，默认值为1.0，10为最大音量
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
        
        # 检查必选字段（移除width和height，因为它们现在是可选的）
        required_fields = ["video_url", "start", "end"]
        missing_fields = [field for field in required_fields if field not in item]
        
        if missing_fields:
            raise CustomException(CustomError.INVALID_VIDEO_INFO, f"the {i}th item is missing required fields: {', '.join(missing_fields)}")
        
        # 如果没有提供duration，则计算为end-start
        duration = item.get("duration", item["end"] - item["start"])
        
        # 创建处理后的对象，设置默认值
        processed_item = {
            "video_url": item["video_url"],
            "width": item.get("width"),  # 可选参数
            "height": item.get("height"),  # 可选参数
            "start": item["start"],
            "end": item["end"],
            "duration": duration,
            "mask": item.get("mask", None),  # 默认值 None
            "transition": item.get("transition", None),  # 默认值 None
            "transition_duration": item.get("transition_duration", 500000),  # 默认值 500000
            "volume": item.get("volume", 1.0)  # 默认值 1.0
        }
        
        # 验证数值范围：用户传入范围 [0, 10]，超范围时给默认值
        if processed_item["volume"] < 0 or processed_item["volume"] > 10:
            logger.warning(f"Volume {processed_item['volume']} out of range [0, 10], using default 1.0")
            processed_item["volume"] = 1.0
        
        if processed_item["transition_duration"] < 0:
            # 转场持续时间必须为非负数，给默认值
            processed_item["transition_duration"] = 500000
        
        result.append(processed_item)
    
    return result
