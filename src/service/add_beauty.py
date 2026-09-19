from typing import List, Dict, Any, Tuple, Optional
import asyncio

from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile
from src.pyJianYingDraft.metadata.beauty_meta import find_beauty_type, build_figure_algorithm_path
from src.pyJianYingDraft.video_segment import VideoSegment, FigureEffect
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
from src.utils import helper
from src.utils.draft_lock_manager import DraftLockManager
from src.service.add_masks import find_segment_by_id

BEAUTY_SLIDER_NAMES = ("匀肤", "丰盈", "磨皮", "祛法令纹", "亮眼", "祛黑眼圈", "美白", "白牙")


def add_beauty(
    draft_url: str,
    segment_ids: List[str],
    beauty_infos: Optional[List[Dict[str, Any]]] = None,
    *,
    匀肤: float = 0,
    丰盈: float = 0,
    磨皮: float = 0,
    祛法令纹: float = 0,
    亮眼: float = 0,
    祛黑眼圈: float = 0,
    美白: float = 0,
    白牙: float = 0,
    肤色: str = "",
    肤色强度: float = 60,
) -> Tuple[str, List[str], List[str]]:
    """向指定视频片段添加美颜。

    美颜写入 materials.effects（type=figure），并挂到片段 extra_material_refs。
    同一片段已有同名滑杆时只更新强度。任意滑杆都会补一条 makeup-root。
    具名参数默认不生效（滑杆为 0、肤色为空）；非默认值会与 beauty_infos 合并写入。

    Returns:
        draft_url, affected_segments, figure_ids
    """
    beauty_infos = _merge_beauty_infos(
        beauty_infos,
        {
            "匀肤": 匀肤,
            "丰盈": 丰盈,
            "磨皮": 磨皮,
            "祛法令纹": 祛法令纹,
            "亮眼": 亮眼,
            "祛黑眼圈": 祛黑眼圈,
            "美白": 美白,
            "白牙": 白牙,
            "肤色": 肤色,
            "肤色强度": 肤色强度,
        },
    )
    logger.info(
        f"add_beauty started, draft_url: {draft_url}, "
        f"segment_ids: {segment_ids}, beauty count: {len(beauty_infos)}"
    )

    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        logger.error(f"Invalid draft_url or draft not found in cache: {draft_url}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    if not segment_ids:
        logger.error("No segment_ids provided")
        raise CustomException(CustomError.INVALID_BEAUTY_INFO)

    if not beauty_infos:
        logger.error("No beauty_infos provided")
        raise CustomException(CustomError.INVALID_BEAUTY_INFO)

    script: ScriptFile = DRAFT_CACHE[draft_id]
    affected_segments: List[str] = []
    figure_ids: List[str] = []

    for i, segment_id in enumerate(segment_ids):
        try:
            logger.info(f"Processing segment {i + 1}/{len(segment_ids)}, segment_id: {segment_id}")
            ids = add_beauty_to_segment(script, segment_id, beauty_infos)
            affected_segments.append(segment_id)
            figure_ids.extend(ids)
        except CustomException:
            raise
        except Exception as e:
            logger.error(
                f"Failed to add beauty to segment {segment_id}, error: {str(e)}"
            )
            raise CustomException(CustomError.BEAUTY_ADD_FAILED)

    script.save()
    logger.info(
        f"add_beauty completed, draft_id: {draft_id}, "
        f"segments: {len(affected_segments)}, figures: {len(figure_ids)}"
    )
    return draft_url, affected_segments, figure_ids


async def add_beauty_async(
    draft_url: str,
    segment_ids: List[str],
    beauty_infos: Optional[List[Dict[str, Any]]] = None,
    lock_timeout: float = 30.0,
    **named_beauty: Any,
) -> Tuple[str, List[str], List[str]]:
    """add_beauty 的异步版本，带草稿写锁。"""
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
        return add_beauty(
            draft_url=draft_url,
            segment_ids=segment_ids,
            beauty_infos=beauty_infos,
            **named_beauty,
        )
    finally:
        await lock_manager.release_lock(draft_id)
        logger.info(f"Lock released for draft_id: {draft_id}")


def _merge_beauty_infos(
    beauty_infos: Optional[List[Dict[str, Any]]],
    named: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """把具名美颜参数合并进 beauty_infos。滑杆为 0、肤色为空时跳过。"""
    items: List[Dict[str, Any]] = list(beauty_infos or [])
    for name in BEAUTY_SLIDER_NAMES:
        value = named.get(name, 0)
        if value:
            items.append({"name": name, "intensity": value})
    skin = str(named.get("肤色") or "").strip()
    if skin:
        items.append({"name": skin, "intensity": named.get("肤色强度", 60)})
    return items


def add_beauty_to_segment(
    script: ScriptFile,
    segment_id: str,
    beauty_infos: List[Dict[str, Any]],
) -> List[str]:
    """向一个视频片段写入美颜，并登记到 materials.effects。"""
    segment = find_segment_by_id(script, segment_id)
    if segment is None:
        logger.error(f"Segment not found: {segment_id}")
        raise CustomException(CustomError.SEGMENT_NOT_FOUND)

    if not isinstance(segment, VideoSegment):
        logger.error(f"Segment {segment_id} is not a video segment, cannot add beauty")
        raise CustomException(CustomError.INVALID_SEGMENT_TYPE)

    video_material_id = segment.material_instance.material_id
    algorithm_path = build_figure_algorithm_path(
        script.materials.ensure_figure_placeholder(),
        video_material_id,
    )

    figure_ids: List[str] = []
    for info in beauty_infos:
        name = info.get("name")
        if not isinstance(name, str) or not name:
            raise CustomException(CustomError.INVALID_BEAUTY_INFO)

        beauty_type = find_beauty_type(name)
        if beauty_type is None:
            logger.error(f"Beauty type not found: {name}")
            raise CustomException(CustomError.BEAUTY_NOT_FOUND)

        try:
            intensity = float(info.get("intensity", 0))
        except (TypeError, ValueError):
            raise CustomException(CustomError.INVALID_BEAUTY_INFO)
        if not 0.0 <= intensity <= 100.0:
            raise CustomException(CustomError.INVALID_BEAUTY_INFO)

        path = algorithm_path if beauty_type.value.needs_algorithm_path else ""
        figure = segment.add_beauty(beauty_type, intensity, algorithm_artifact_path=path)
        _register_figure(script, figure)
        figure_ids.append(figure.global_id)
        logger.info(f"Applied beauty {name}={intensity} to segment {segment_id}, figure_id: {figure.global_id}")

    root = segment.ensure_makeup_root(algorithm_path)
    _register_figure(script, root)
    figure_ids.append(root.global_id)
    return figure_ids


def _register_figure(script: ScriptFile, figure: FigureEffect) -> None:
    """片段已在轨道上时，补登记美颜素材。避免与 add_segment 重复追加。"""
    if figure not in script.materials:
        script.materials.figures.append(figure)
