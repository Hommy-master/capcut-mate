from dataclasses import dataclass, replace
from typing import List, Dict, Any, Tuple, Optional
import asyncio

from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile
from src.pyJianYingDraft.metadata.beauty_meta import (
    ALL_FACES,
    BEAUTY_CATALOG,
    BEAUTY_GROUPS,
    GROUP_BODY,
    GROUP_MAKEUP,
    GROUP_SHAPE,
    GROUP_SKIN,
    BeautyMeta,
    build_figure_algorithm_path,
    find_beauty_type,
    find_skin_tone,
)
from src.pyJianYingDraft.video_segment import VideoSegment, FigureEffect
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
from src.utils import helper
from src.utils.draft_lock_manager import DraftLockManager
from src.service.add_masks import find_segment_by_id

# 非滑杆字段（预设选择 / 预设参数），由 _extra_ops 单独处理
_EXTRA_FIELDS: Dict[str, Tuple[str, ...]] = {
    GROUP_SKIN: ("skin_tone", "temperature", "intensity"),
    GROUP_MAKEUP: ("look", "intensity", "face_id"),
}


@dataclass(frozen=True)
class _BeautyOp:
    """一条已解析完成、可直接写入草稿的美化操作。"""

    meta: BeautyMeta
    intensity: float = 0.0
    """剪映滑杆原值 0~100。"""
    cold_warm: float = 0.0
    """肤色冷暖原值 0~99，仅肤色使用。"""


def add_beauty(
    draft_url: str,
    segment_ids: List[str],
    *,
    skin: Optional[Dict[str, Any]] = None,
    shape: Optional[Dict[str, Any]] = None,
    makeup: Optional[Dict[str, Any]] = None,
    body: Optional[Dict[str, Any]] = None,
) -> Tuple[str, List[str], List[str]]:
    """向指定视频片段添加美颜 / 美型 / 美妆 / 美体。

    每个非 0 滑杆写入 materials.effects（type=figure），并挂到片段 extra_material_refs；
    同一片段已有同素材时只原地更新强度（保留素材 id）；任意滑杆都会补一条 makeup-root。
    滑杆为 0 表示不写入（与剪映「关闭」= 素材缺失一致）。

    Returns:
        draft_url, affected_segments, figure_ids
    """
    # 先收集并校验全部参数，再改动草稿，避免多片段时前面片段被写坏
    ops = _collect_ops(skin=skin, shape=shape, makeup=makeup, body=body)
    logger.info(
        f"add_beauty started, draft_url: {draft_url}, "
        f"segment_ids: {segment_ids}, beauty op count: {len(ops)}"
    )

    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        logger.error(f"Invalid draft_url or draft not found in cache: {draft_url}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    if not segment_ids:
        logger.error("No segment_ids provided")
        raise CustomException(CustomError.INVALID_BEAUTY_INFO)

    if not ops:
        logger.error("No effective beauty params provided")
        raise CustomException(CustomError.INVALID_BEAUTY_INFO, "no effective beauty parameters provided")

    script: ScriptFile = DRAFT_CACHE[draft_id]
    affected_segments: List[str] = []
    figure_ids: List[str] = []

    for i, segment_id in enumerate(segment_ids):
        try:
            logger.info(f"Processing segment {i + 1}/{len(segment_ids)}, segment_id: {segment_id}")
            ids = add_beauty_to_segment(script, segment_id, ops)
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
    *,
    skin: Optional[Dict[str, Any]] = None,
    shape: Optional[Dict[str, Any]] = None,
    makeup: Optional[Dict[str, Any]] = None,
    body: Optional[Dict[str, Any]] = None,
    lock_timeout: float = 30.0,
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
            skin=skin,
            shape=shape,
            makeup=makeup,
            body=body,
        )
    finally:
        await lock_manager.release_lock(draft_id)
        logger.info(f"Lock released for draft_id: {draft_id}")


def _read_value(data: Dict[str, Any], name: str, *, default: float = 0.0, maximum: float = 100.0) -> float:
    """读取一个滑杆数值并校验范围；缺省时返回 default。"""
    value = data.get(name, default)
    if value is None:
        return default
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise CustomException(CustomError.INVALID_BEAUTY_INFO, f"{name}: {data.get(name)!r}")
    if not 0.0 <= value <= maximum:
        raise CustomException(CustomError.INVALID_BEAUTY_INFO, f"{name}: {value}")
    return value


def _read_face_id(data: Dict[str, Any]) -> str:
    """读取妆容作用的人脸：默认全部人脸（-1），也接受 0、1、2… 这样的人脸序号。"""
    value = str(data.get("face_id", ALL_FACES) or ALL_FACES).strip()
    if value != ALL_FACES and not value.isdigit():
        raise CustomException(
            CustomError.INVALID_BEAUTY_INFO,
            f"face_id: {data.get('face_id')!r}, expected {ALL_FACES} (all faces) or a non-negative face index",
        )
    return value


def _reject_unknown_keys(group: str, data: Dict[str, Any]) -> None:
    """拒绝目录之外的键（HTTP 层已由 schema 的 extra=forbid 拦截，这里兜底直接调用）。"""
    known = set(BEAUTY_CATALOG[group]) | set(_EXTRA_FIELDS.get(group, ()))
    unknown = [key for key in data if key not in known]
    if unknown:
        raise CustomException(CustomError.BEAUTY_NOT_FOUND, f"unknown beauty parameters: {', '.join(unknown)}")


def _collect_ops(
    *,
    skin: Optional[Dict[str, Any]] = None,
    shape: Optional[Dict[str, Any]] = None,
    makeup: Optional[Dict[str, Any]] = None,
    body: Optional[Dict[str, Any]] = None,
) -> List[_BeautyOp]:
    """按分组顺序把请求转换为待写入操作。滑杆为 0 跳过；预留字段非 0 报 2044。"""
    groups = {
        GROUP_SKIN: dict(skin or {}),
        GROUP_SHAPE: dict(shape or {}),
        GROUP_MAKEUP: dict(makeup or {}),
        GROUP_BODY: dict(body or {}),
    }
    ops: List[_BeautyOp] = []
    for group in BEAUTY_GROUPS:
        data = groups[group]
        if not data:
            continue
        _reject_unknown_keys(group, data)

        for meta in BEAUTY_CATALOG[group].values():
            value = _read_value(data, meta.name)
            if not value:
                continue
            if not meta.supported:
                raise CustomException(
                    CustomError.BEAUTY_NOT_FOUND,
                    f"{meta.name} is not supported yet (no matching material in the draft), pass 0",
                )
            ops.append(_BeautyOp(meta, intensity=value))

        ops.extend(_extra_ops(group, data))
    return ops


def _extra_ops(group: str, data: Dict[str, Any]) -> List[_BeautyOp]:
    """处理肤色 / 美妆套装这类预设选择字段。预设值沿用剪映预设名，为中文。"""
    if group == GROUP_SKIN:
        preset = str(data.get("skin_tone") or "").strip()
        if not preset:
            return []
        meta = find_skin_tone(preset)
        if meta is None:
            raise CustomException(
                CustomError.BEAUTY_NOT_FOUND,
                f"unsupported skin_tone preset: {preset}, expected 冷白 / 暖白",
            )
        return [_BeautyOp(
            meta,
            intensity=_read_value(data, "intensity", default=60.0),
            cold_warm=_read_value(data, "temperature", default=0.0, maximum=meta.cold_warm_divisor),
        )]

    if group == GROUP_MAKEUP:
        preset = str(data.get("look") or "").strip()
        if not preset:
            return []
        meta = find_beauty_type(GROUP_MAKEUP, preset)
        if meta is None:
            raise CustomException(
                CustomError.BEAUTY_NOT_FOUND,
                f"unknown makeup look: {preset}, expected 淡人妆 / 氧气感",
            )
        return [_BeautyOp(
            replace(meta, face_id=_read_face_id(data)),
            intensity=_read_value(data, "intensity", default=80.0),
        )]

    return []


def add_beauty_to_segment(
    script: ScriptFile,
    segment_id: str,
    ops: List[_BeautyOp],
) -> List[str]:
    """向一个视频片段写入美化素材，并登记到 materials.effects。"""
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
    for op in ops:
        figure = segment.add_beauty(
            op.meta,
            op.intensity,
            cold_warm=op.cold_warm,
            algorithm_artifact_path=algorithm_path,
        )
        _register_figure(script, figure)
        figure_ids.append(figure.global_id)
        logger.info(
            f"Applied beauty {op.meta.name}={op.intensity} to segment {segment_id}, "
            f"figure_id: {figure.global_id}"
        )

    root = segment.ensure_makeup_root(algorithm_path)
    _register_figure(script, root)
    figure_ids.append(root.global_id)
    return figure_ids


def _register_figure(script: ScriptFile, figure: FigureEffect) -> None:
    """片段已在轨道上时，补登记美颜素材。避免与 add_segment 重复追加。"""
    if figure not in script.materials:
        script.materials.figures.append(figure)
