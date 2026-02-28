from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile, trange, StickerSegment, ClipSettings
import src.pyJianYingDraft as draft
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
import os
from src.utils import helper
import config
from typing import Tuple


def add_sticker(
    draft_url: str,
    sticker_id: str,
    start: int,
    end: int,
    scale: float = 1.0,
    transform_x: int = 0,
    transform_y: int = 0
) -> Tuple[str, str, str, str, int]:
    """
    添加贴纸到剪映草稿的业务逻辑
    
    Args:
        draft_url: 草稿URL，必选参数
        sticker_id: 贴纸的唯一标识ID，必选参数
        start: 贴纸开始时间（微秒），必选参数
        end: 贴纸结束时间（微秒），必选参数
        scale: 贴纸缩放比例，默认1.0，可选参数。1.0=原始大小，0.5=缩小一半，2.0=放大两倍，建议范围[0.1, 5.0]
        transform_x: X轴位置偏移（像素），默认值0，可选参数。正值向右移动，负值向左移动，以画布中心为原点
        transform_y: Y轴位置偏移（像素），默认值0，可选参数。正值向下移动，负值向上移动，以画布中心为原点
    
    Returns:
        Tuple[str, str, str, str, int]: 返回元组包含以下信息
        - draft_url: 草稿URL
        - sticker_id: 贴纸的唯一标识ID
        - track_id: 轨道ID
        - segment_id: 片段ID
        - duration: 贴纸显示时长（微秒）
    
    Raises:
        CustomException: 贴纸添加失败
    """
    logger.info(f"add_sticker starting, draft_url: {draft_url}, sticker_id: {sticker_id}, start: {start}, end: {end}, scale: {scale}, transform_x: {transform_x}, transform_y: {transform_y}")

    # 1. 验证时间参数
    if end <= start:
        logger.error(f"Invalid time range: end ({end}) must be greater than start ({start})")
        raise CustomException(CustomError.INVALID_STICKER_INFO)
    
    # 计算贴纸显示时长
    duration = end - start
    logger.info(f"Calculated sticker duration: {duration} microseconds")

    # 2. 提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        logger.error(f"Invalid draft_url or draft not found in cache, draft_id: {draft_id}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    # 3. 从缓存中获取草稿
    script: ScriptFile = DRAFT_CACHE[draft_id]
    logger.info(f"Retrieved script from cache, draft_id: {draft_id}")

    # 4. 创建贴纸轨道（如果不存在）
    track_name = f"sticker_track_{helper.gen_unique_id()}"
    try:
        script.add_track(track_type=draft.TrackType.sticker, track_name=track_name)
        logger.info(f"Created sticker track: {track_name}")
    except Exception as e:
        logger.error(f"Failed to create sticker track: {str(e)}")
        raise CustomException(CustomError.STICKER_ADD_FAILED)

    # 5. 创建图像调节设置
    # 获取草稿的宽高用于transform坐标转换
    draft_width = script.width
    draft_height = script.height
    logger.info(f"draft size: {draft_width}x{draft_height}, transform_x: {transform_x}, transform_y: {transform_y}")
    
    clip_settings = ClipSettings(
        scale_x=scale,
        scale_y=scale,
        transform_x=transform_x / draft_width,  # 转换为半画布宽单位
        transform_y=transform_y / draft_height   # 转换为半画布高单位
    )
    logger.info(f"Created clip settings - scale: {scale}, transform_x: {transform_x/draft_width}, transform_y: {transform_y/draft_height}")

    # 6. 创建贴纸片段
    try:
        sticker_segment = StickerSegment(
            resource_id=sticker_id,
            target_timerange=trange(start=start, duration=duration),
            clip_settings=clip_settings
        )
        logger.info(f"Created sticker segment, segment_id: {sticker_segment.segment_id}, resource_id: {sticker_id}")
    except Exception as e:
        logger.error(f"Failed to create sticker segment: {str(e)}")
        raise CustomException(CustomError.STICKER_ADD_FAILED)

    # 7. 向指定轨道添加贴纸片段
    try:
        script.add_segment(sticker_segment, track_name)
        logger.info(f"Added sticker segment to track: {track_name}")
    except Exception as e:
        logger.error(f"Failed to add sticker segment to track: {str(e)}")
        raise CustomException(CustomError.STICKER_ADD_FAILED)

    # 8. 保存草稿
    try:
        script.save()
        logger.info(f"Saved script successfully, draft_id: {draft_id}")
    except Exception as e:
        logger.error(f"Failed to save script: {str(e)}")
        raise CustomException(CustomError.STICKER_ADD_FAILED)

    # 9. 获取轨道ID
    track_id = ""
    for key in script.tracks.keys():
        if script.tracks[key].name == track_name:
            track_id = script.tracks[key].track_id
            break
    
    if not track_id:
        logger.error(f"Failed to retrieve track_id for track: {track_name}")
        raise CustomException(CustomError.STICKER_ADD_FAILED)
    
    logger.info(f"Retrieved track_id: {track_id}")

    # 10. 获取片段ID
    segment_id = sticker_segment.segment_id
    logger.info(f"Final segment_id: {segment_id}")

    logger.info(f"add_sticker completed successfully - draft_id: {draft_id}, track_id: {track_id}, segment_id: {segment_id}, duration: {duration}")
    
    return draft_url, sticker_id, track_id, segment_id, duration