from typing import List, Dict, Any, Tuple
import asyncio

from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile
from src.pyJianYingDraft.video_segment import VideoSegment
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
from src.utils import helper
from src.utils.draft_lock_manager import DraftLockManager
from src.service.add_masks import find_segment_by_id


def add_mask_keyframes(
    draft_url: str,
    keyframes: List[Dict[str, Any]],
) -> Tuple[str, int, List[str]]:
    """向已有蒙版的视频片段添加蒙版关键帧。

    关键帧写入片段 common_keyframes，不修改 materials.masks 的静态 config。
    单位与 add_masks 一致：X/Y/width/height 为像素，feather 为 0-100，rotation 为度。

    Returns:
        draft_url, keyframes_added, affected_segments
    """
    logger.info(
        f"add_mask_keyframes started, draft_url: {draft_url}, "
        f"keyframe count: {len(keyframes) if keyframes else 0}"
    )

    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        logger.error(f"Invalid draft_url or draft not found in cache: {draft_url}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    if not keyframes:
        logger.error("No keyframes provided")
        raise CustomException(CustomError.INVALID_MASK_KEYFRAME_INFO)

    script: ScriptFile = DRAFT_CACHE[draft_id]
    keyframes_added = 0
    affected_segments: List[str] = []

    for i, item in enumerate(keyframes):
        try:
            added = _add_mask_keyframe_item(script, item)
        except CustomException:
            raise
        except ValueError as e:
            logger.error(f"Invalid mask keyframe item {i + 1}: {e}")
            raise CustomException(CustomError.INVALID_MASK_KEYFRAME_INFO, str(e))
        except Exception as e:
            logger.error(f"Failed to add mask keyframe item {i + 1}, error: {str(e)}")
            raise CustomException(CustomError.MASK_KEYFRAME_ADD_FAILED)

        keyframes_added += added
        segment_id = str(item["segment_id"])
        if segment_id not in affected_segments:
            affected_segments.append(segment_id)

    try:
        script.save()
    except Exception as e:
        logger.error(f"Failed to save draft: {str(e)}")
        raise CustomException(CustomError.MASK_KEYFRAME_ADD_FAILED)

    logger.info(
        f"add_mask_keyframes completed, draft_id: {draft_id}, "
        f"keyframes_added: {keyframes_added}, segments: {affected_segments}"
    )
    return draft_url, keyframes_added, affected_segments


async def add_mask_keyframes_async(
    draft_url: str,
    keyframes: List[Dict[str, Any]],
    lock_timeout: float = 30.0,
) -> Tuple[str, int, List[str]]:
    """add_mask_keyframes 的异步版本，带草稿写锁。"""
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if not draft_id:
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    lock_manager = DraftLockManager()
    try:
        await lock_manager.acquire_lock(draft_id, timeout=lock_timeout)
        logger.info(f"Lock acquired for draft_id: {draft_id}")
    except asyncio.TimeoutError:
        logger.error(f"Timeout waiting for lock on draft_id: {draft_id}")
        raise CustomException(
            CustomError.DRAFT_LOCK_TIMEOUT,
            f"Failed to acquire lock for draft {draft_id} within {lock_timeout}s",
        )

    try:
        return add_mask_keyframes(draft_url=draft_url, keyframes=keyframes)
    finally:
        await lock_manager.release_lock(draft_id)
        logger.info(f"Lock released for draft_id: {draft_id}")


def _add_mask_keyframe_item(script: ScriptFile, item: Dict[str, Any]) -> int:
    """处理一条蒙版关键帧，返回实际写入的属性条数。"""
    segment_id = item.get("segment_id")
    if not isinstance(segment_id, str) or not segment_id:
        raise CustomException(CustomError.INVALID_MASK_KEYFRAME_INFO)

    try:
        offset = int(item.get("offset"))
    except (TypeError, ValueError):
        raise CustomException(CustomError.INVALID_MASK_KEYFRAME_INFO)
    if offset < 0:
        raise CustomException(CustomError.INVALID_MASK_KEYFRAME_INFO)

    x = _optional_float(item.get("X"))
    y = _optional_float(item.get("Y"))
    width = _optional_float(item.get("width"))
    height = _optional_float(item.get("height"))
    feather = _optional_float(item.get("feather"))
    rotation = _optional_float(item.get("rotation"))
    if (
        x is None
        and y is None
        and width is None
        and height is None
        and feather is None
        and rotation is None
    ):
        raise CustomException(CustomError.INVALID_MASK_KEYFRAME_INFO)
    if feather is not None and not (0.0 <= feather <= 100.0):
        raise CustomException(CustomError.INVALID_MASK_KEYFRAME_INFO)
    if width is not None and width < 0:
        raise CustomException(CustomError.INVALID_MASK_KEYFRAME_INFO)
    if height is not None and height < 0:
        raise CustomException(CustomError.INVALID_MASK_KEYFRAME_INFO)

    segment = find_segment_by_id(script, segment_id)
    if segment is None:
        logger.error(f"Segment not found: {segment_id}")
        raise CustomException(CustomError.SEGMENT_NOT_FOUND)

    if not isinstance(segment, VideoSegment):
        logger.error(f"Segment {segment_id} is not a video segment, cannot add mask keyframes")
        raise CustomException(CustomError.INVALID_SEGMENT_TYPE)

    if segment.mask is None:
        logger.error(f"Segment {segment_id} has no mask, call add_masks first")
        raise CustomException(CustomError.SEGMENT_MASK_NOT_FOUND)

    time_offset = max(0, min(offset, segment.duration))
    added = segment.add_mask_keyframe(
        time_offset,
        center_x=x,
        center_y=y,
        width=width,
        height=height,
        feather=feather,
        rotation=rotation,
    )
    logger.info(
        f"Added {added} mask keyframe(s) to segment {segment_id} at offset {time_offset}"
    )
    return added


def _optional_float(value: Any) -> Any:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        raise CustomException(CustomError.INVALID_MASK_KEYFRAME_INFO)
