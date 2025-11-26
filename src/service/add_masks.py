from typing import List, Dict, Any, Tuple, Optional
from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile, MaskType
from src.pyJianYingDraft.video_segment import VideoSegment
from src.pyJianYingDraft.segment import VisualSegment
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
from src.utils import helper


def add_masks(
    draft_url: str,
    segment_ids: List[str],
    name: str = "线性",
    X: int = 0,
    Y: int = 0,
    width: int = 512,
    height: int = 512,
    feather: int = 0,
    rotation: int = 0,
    invert: bool = False,
    roundCorner: int = 0
) -> Tuple[str, int, List[str], List[str]]:
    """
    向现有草稿中的指定片段添加遮罩效果的业务逻辑
    
    Args:
        draft_url: 草稿URL，必选参数
        segment_ids: 要应用遮罩的片段ID数组，必选参数
        name: 遮罩类型名称，默认值："线性"。支持："线性", "镜面", "圆形", "矩形", "爱心", "星形"
        X: 遮罩中心X坐标（像素），默认值：0
        Y: 遮罩中心Y坐标（像素），默认值：0
        width: 遮罩宽度（像素），默认值：512
        height: 遮罩高度（像素），默认值：512
        feather: 羽化程度（0-100），默认值：0
        rotation: 旋转角度（度），默认值：0
        invert: 是否反转遮罩，默认值：false
        roundCorner: 圆角半径（0-100），默认值：0
    
    Returns:
        Tuple[str, int, List[str], List[str]]: 返回元组包含以下信息
        - draft_url: 草稿URL
        - masks_added: 成功添加的遮罩数量
        - affected_segments: 受影响的片段ID列表
        - mask_ids: 遮罩ID列表
    
    Raises:
        CustomException: 遮罩添加失败
    """
    logger.info(f"add_masks started, draft_url: {draft_url}, segment_ids: {segment_ids}, mask_name: {name}")

    # 1. 提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        logger.error(f"Invalid draft_url or draft not found in cache: {draft_url}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    # 2. 验证片段ID列表
    if not segment_ids or len(segment_ids) == 0:
        logger.error("No segment_ids provided")
        raise CustomException(CustomError.INVALID_MASK_INFO)

    logger.info(f"Processing {len(segment_ids)} segments for mask addition")

    # 3. 从缓存中获取草稿
    script: ScriptFile = DRAFT_CACHE[draft_id]

    # 4. 查找遮罩类型
    mask_type = find_mask_type_by_name(name)
    if mask_type is None:
        logger.error(f"Mask type not found for name: {name}")
        raise CustomException(CustomError.MASK_NOT_FOUND)

    # 5. 遍历片段ID，为每个片段添加遮罩
    masks_added = 0
    affected_segments: List[str] = []
    mask_ids: List[str] = []

    for i, segment_id in enumerate(segment_ids):
        try:
            logger.info(f"Processing segment {i+1}/{len(segment_ids)}, segment_id: {segment_id}")
            
            mask_id = add_mask_to_segment(
                script=script,
                segment_id=segment_id,
                mask_type=mask_type,
                center_x=X,
                center_y=Y,
                width=width,
                height=height,
                feather=feather,
                rotation=rotation,
                invert=invert,
                round_corner=roundCorner
            )
            
            masks_added += 1
            affected_segments.append(segment_id)
            mask_ids.append(mask_id)
            logger.info(f"Added mask to segment {i+1}/{len(segment_ids)}, mask_id: {mask_id}")
            
        except Exception as e:
            logger.error(f"Failed to add mask to segment {i+1}/{len(segment_ids)}, segment_id: {segment_id}, error: {str(e)}")
            raise

    # 6. 保存草稿
    script.save()
    logger.info(f"Draft saved successfully")

    logger.info(f"add_masks completed successfully - draft_id: {draft_id}, masks_added: {masks_added}")
    
    return draft_url, masks_added, affected_segments, mask_ids


def add_mask_to_segment(
    script: ScriptFile,
    segment_id: str,
    mask_type: MaskType,
    center_x: int = 0,
    center_y: int = 0,
    width: int = 512,
    height: int = 512,
    feather: int = 0,
    rotation: int = 0,
    invert: bool = False,
    round_corner: int = 0
) -> str:
    """
    向指定片段添加遮罩
    
    Args:
        script: 草稿文件对象
        segment_id: 目标片段ID
        mask_type: 遮罩类型
        center_x: 遮罩中心X坐标（像素）
        center_y: 遮罩中心Y坐标（像素） 
        width: 遮罩宽度（像素）
        height: 遮罩高度（像素）
        feather: 羽化程度（0-100）
        rotation: 旋转角度（度）
        invert: 是否反转遮罩
        round_corner: 圆角半径（0-100）
    
    Returns:
        mask_id: 遮罩ID
    
    Raises:
        CustomException: 添加遮罩失败
    """
    try:
        # 1. 查找片段
        segment = find_segment_by_id(script, segment_id)
        if segment is None:
            logger.error(f"Segment not found: {segment_id}")
            raise CustomException(CustomError.SEGMENT_NOT_FOUND)
        
        # 2. 验证片段类型（只有VideoSegment支持遮罩）
        if not isinstance(segment, VideoSegment):
            logger.error(f"Segment {segment_id} is not a video segment, cannot add mask")
            raise CustomException(CustomError.INVALID_SEGMENT_TYPE)
        
        # 3. 检查片段是否已有遮罩
        if segment.mask is not None:
            logger.info(f"Segment {segment_id} already has a mask, returning existing mask id")
            # 如果片段已经有遮罩，直接返回现有的遮罩ID而不是抛出异常
            return segment.mask.global_id
        
        # 4. 计算遮罩尺寸参数
        # 根据 add_mask 方法的要求，size 是主要尺寸（以占素材高度的比例表示）
        material_width, material_height = segment.material_size
        size = height / material_height  # 高度比例
        rect_width = width / material_width if mask_type == MaskType.矩形 else None
        
        logger.info(f"Adding mask to segment {segment_id}: type={mask_type.value.name}, center=({center_x}, {center_y}), size={size}")
        logger.info(f"Mask details - width: {width}, height: {height}, feather: {feather}, rotation: {rotation}, invert: {invert}, round_corner: {round_corner}")

        # 5. 添加遮罩到片段
        if mask_type == MaskType.矩形:
            # 矩形遮罩可以使用所有参数
            segment.add_mask(
                mask_type=mask_type,
                center_x=float(center_x),
                center_y=float(center_y), 
                size=size,
                rotation=float(rotation),
                feather=float(feather),
                invert=invert,
                rect_width=rect_width,
                round_corner=float(round_corner)
            )
        else:
            # 非矩形遮罩不能使用 rect_width 和 round_corner 参数
            segment.add_mask(
                mask_type=mask_type,
                center_x=float(center_x),
                center_y=float(center_y), 
                size=size,
                rotation=float(rotation),
                feather=float(feather),
                invert=invert
            )

        mask_id = segment.mask.global_id if segment.mask is not None else ""
        if not mask_id:
            logger.error(f"Failed to create mask for segment {segment_id}")
            raise CustomException(CustomError.MASK_ADD_FAILED)
        
        logger.info(f"Successfully added mask to segment {segment_id}, mask_id: {mask_id}")
        
        return mask_id
        
    except CustomException:
        logger.error(f"Add mask to segment failed, segment_id: {segment_id}")
        raise
    except Exception as e:
        logger.error(f"Add mask to segment failed, error: {str(e)}")
        raise CustomException(CustomError.MASK_ADD_FAILED)


def find_segment_by_id(script: ScriptFile, segment_id: str) -> Optional[VisualSegment]:
    """
    通过segment_id在草稿中查找对应的片段
    
    Args:
        script: 草稿文件对象
        segment_id: 片段ID
    
    Returns:
        找到的片段对象，如果未找到则返回None
    """
    logger.info(f"Searching for segment with id: {segment_id}")
    
    # 遍历所有轨道
    for track_name, track in script.tracks.items():
        logger.info(f"Searching in track: {track_name}, segments count: {len(track.segments)}")
        
        # 遍历轨道中的所有片段
        for segment in track.segments:
            if segment.segment_id == segment_id:
                logger.info(f"Found segment {segment_id} in track {track_name}")
                return segment
    
    logger.warning(f"Segment {segment_id} not found in any track")
    return None


def find_mask_type_by_name(mask_name: str) -> Optional[MaskType]:
    """
    根据遮罩名称查找对应的遮罩类型
    
    Args:
        mask_name: 遮罩名称
    
    Returns:
        对应的遮罩类型枚举，如果未找到则返回None
    """
    logger.info(f"Searching for mask type with name: {mask_name}")
    
    # 搜索MaskType中的遮罩
    for mask_type in MaskType:
        if mask_type.value.name == mask_name:
            logger.info(f"Found mask type: {mask_name}")
            return mask_type
    
    logger.warning(f"Mask type not found for name: {mask_name}")
    return None