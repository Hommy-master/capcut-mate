import json
from typing import List, Dict, Any, Tuple, Optional
import asyncio

from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile, TrackType, FilterSegment, Timerange
from src.pyJianYingDraft.metadata import FilterType
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
from src.utils import helper
from src.utils.draft_lock_manager import DraftLockManager


def add_filters(
    draft_url: str,
    filter_infos: str
) -> Tuple[str, str, List[str], List[str]]:
    """
    添加滤镜到剪映草稿的业务逻辑
    
    Args:
        draft_url: 草稿URL
        filter_infos: 滤镜信息列表的JSON字符串，格式如下：
            [
                {
                    "filter_title": "复古",  # 滤镜名称/标题，必选参数
                    "start": 0,  # 滤镜开始时间（微秒），必选参数
                    "end": 5000000,  # 滤镜结束时间（微秒），必选参数
                    "intensity": 100  # 滤镜强度(0-100)，可选参数，默认100
                }
            ]
    
    Returns:
        draft_url: 草稿URL
        track_id: 滤镜轨道ID
        filter_ids: 滤镜ID列表
        segment_ids: 滤镜片段ID列表
    
    Raises:
        CustomException: 滤镜添加失败
    """
    logger.info(f"add_filters started, draft_url: {draft_url}, filters count: {len(json.loads(filter_infos) if filter_infos else [])}")

    # 1. 提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        logger.error(f"Invalid draft_url or draft not found in cache: {draft_url}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    # 2. 解析滤镜信息
    filter_items = parse_filters_data(json_str=filter_infos)
    if len(filter_items) == 0:
        logger.info(f"No filter info provided, draft_id: {draft_id}")
        raise CustomException(CustomError.INVALID_FILTER_INFO)

    logger.info(f"Parsed {len(filter_items)} filter items")

    # 3. 从缓存中获取草稿
    script: ScriptFile = DRAFT_CACHE[draft_id]

    # 4. 添加滤镜轨道
    track_name = f"filter_track_{helper.gen_unique_id()}"
    script.add_track(track_type=TrackType.filter, track_name=track_name)
    logger.info(f"Added filter track: {track_name}")

    # 5. 遍历滤镜信息，添加滤镜到草稿中的指定轨道，收集片段ID
    segment_ids = []
    filter_ids = []
    for i, filter_item in enumerate(filter_items):
        try:
            logger.info(f"Processing filter {i+1}/{len(filter_items)}, title: {filter_item['filter_title']}")
            
            segment_id, filter_id = add_filter_to_draft(
                script, track_name, filter_item=filter_item
            )
            segment_ids.append(segment_id)
            filter_ids.append(filter_id)
            logger.info(f"Added filter {i+1}/{len(filter_items)}, segment_id: {segment_id}")
        except Exception as e:
            logger.error(f"Failed to add filter {i+1}/{len(filter_items)}, error: {str(e)}")
            raise

    # 6. 保存草稿
    script.save()
    logger.info("Draft saved successfully")

    # 7. 获取当前滤镜轨道ID
    track_id = ""
    for key in script.tracks.keys():
        if script.tracks[key].name == track_name:
            track_id = script.tracks[key].track_id
            break
    logger.info(f"Filter track created, draft_id: {draft_id}, track_id: {track_id}")

    logger.info(f"add_filters completed successfully - draft_id: {draft_id}, track_id: {track_id}, filters_added: {len(filter_items)}")
    
    return draft_url, track_id, filter_ids, segment_ids


async def add_filters_async(
    draft_url: str,
    filter_infos: str,
    lock_timeout: float = 30.0
) -> Tuple[str, str, List[str], List[str]]:
    """
    添加滤镜到剪映草稿的异步版本（带并发锁保护）
    
    功能：
    1. 使用 DraftLockManager 防止同一草稿的并发写操作
    2. 支持超时控制，避免无限等待
    3. 自动释放锁，即使发生异常
    
    Args:
        draft_url: 草稿 URL，格式：".../get_draft?draft_id=xxx"
        filter_infos: JSON 字符串，包含滤镜信息列表，详见 add_filters 函数
        lock_timeout: 获取锁的超时时间（秒），默认 30 秒
    
    Returns:
        tuple: (draft_url, track_id, filter_ids, segment_ids)
    
    Raises:
        CustomException: 滤镜添加失败或获取锁超时
        asyncio.TimeoutError: 等待锁超时时抛出
    
    Example:
        >>> result = await add_filters_async(
        ...     draft_url="http://.../draft_id=123",
        ...     filter_infos='[{"filter_title":"复古", "start":0, "end":5000000}]'
        ... )
    """
    # 提取草稿 ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if not draft_id:
        raise CustomException(CustomError.INVALID_DRAFT_URL)
    
    # 获取锁管理器
    lock_manager = DraftLockManager()
    
    # 尝试获取锁
    try:
        await lock_manager.acquire_lock(draft_id, timeout=lock_timeout)
        logger.info(f"Lock acquired for draft_id: {draft_id}")
    except asyncio.TimeoutError:
        logger.error(f"Timeout waiting for lock on draft_id: {draft_id}")
        raise CustomException(
            CustomError.DRAFT_LOCK_TIMEOUT,
            f"Failed to acquire lock for draft {draft_id} within {lock_timeout}s"
        )
    
    try:
        # 调用内部处理函数（不获取锁，由外层控制）
        return add_filters(
            draft_url=draft_url,
            filter_infos=filter_infos
        )
    finally:
        # 释放锁
        await lock_manager.release_lock(draft_id)
        logger.info(f"Lock released for draft_id: {draft_id}")


def add_filter_to_draft(
    script: ScriptFile,
    track_name: str,
    filter_item: dict
) -> Tuple[str, str]:
    """
    向剪映草稿中添加单个滤镜
    
    Args:
        script: 草稿文件对象
        track_name: 滤镜轨道名称
        filter_item: 滤镜信息字典，包含以下字段：
            filter_title: 滤镜名称/标题
            start: 滤镜开始时间（微秒）
            end: 滤镜结束时间（微秒）
            intensity: 滤镜强度(0-100)，可选，默认100
    
    Returns:
        segment_id: 片段ID
        filter_id: 滤镜ID（material_id）
    
    Raises:
        CustomException: 添加滤镜失败
    """
    try:
        # 1. 查找滤镜类型
        filter_type = find_filter_type_by_name(filter_item['filter_title'])
        if filter_type is None:
            logger.error(f"Filter type not found for title: {filter_item['filter_title']}")
            raise CustomException(CustomError.FILTER_NOT_FOUND)
        
        # 2. 创建时间范围
        filter_duration = filter_item['end'] - filter_item['start']
        timerange = Timerange(start=filter_item['start'], duration=filter_duration)
        
        # 3. 获取滤镜强度（默认100）
        intensity = filter_item.get('intensity', 100.0)
        
        # 4. 创建滤镜片段
        filter_segment = FilterSegment(
            meta=filter_type,
            target_timerange=timerange,
            intensity=intensity / 100.0  # 转换为0-1范围
        )
        
        logger.info(f"Created filter segment, filter_id: {filter_segment.material.global_id}")
        logger.info(f"Filter segment details - start: {filter_item['start']}, duration: {filter_duration}, title: {filter_item['filter_title']}, intensity: {intensity}")

        # 5. 向指定轨道添加片段
        script.add_segment(filter_segment, track_name)

        return filter_segment.segment_id, filter_segment.material.global_id
        
    except CustomException:
        logger.error(f"Add filter to draft failed, filter: {filter_item}")
        raise
    except Exception as e:
        logger.error(f"Add filter to draft failed, error: {str(e)}")
        raise CustomException(CustomError.FILTER_ADD_FAILED)


def find_filter_type_by_name(filter_title: str) -> Optional[FilterType]:
    """
    根据滤镜名称查找对应的滤镜类型
    
    Args:
        filter_title: 滤镜名称/标题
    
    Returns:
        对应的滤镜类型枚举，如果未找到则返回None
    """
    logger.info(f"Searching for filter type with title: {filter_title}")
    
    # 搜索FilterType中的滤镜
    for filter_type in FilterType:
        if filter_type.value.name == filter_title:
            logger.info(f"Found filter: {filter_title}")
            return filter_type
    
    logger.warning(f"Filter type not found for title: {filter_title}")
    return None


def parse_filters_data(json_str: str) -> List[Dict[str, Any]]:
    """
    解析滤镜数据的JSON字符串，验证必选字段和数值范围
    
    Args:
        json_str: 包含滤镜数据的JSON字符串，格式如下：
        [
            {
                "filter_title": "复古",  # [必选] 滤镜名称/标题
                "start": 0,  # [必选] 滤镜开始时间（微秒）
                "end": 5000000,  # [必选] 滤镜结束时间（微秒）
                "intensity": 100  # [可选] 滤镜强度(0-100)，默认100
            }
        ]
    
    Returns:
        包含滤镜对象的数组，每个对象都验证过格式和范围
    
    Raises:
        CustomException: 当JSON格式错误或缺少必选字段时抛出
    """
    try:
        # 解析JSON字符串
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e.msg}")
        raise CustomException(CustomError.INVALID_FILTER_INFO, f"JSON parse error: {e.msg}")
    
    # 确保输入是列表
    if not isinstance(data, list):
        logger.error("filter_infos should be a list")
        raise CustomException(CustomError.INVALID_FILTER_INFO, "filter_infos should be a list")
    
    result = []
    
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            logger.error(f"the {i}th item should be a dict")
            raise CustomException(CustomError.INVALID_FILTER_INFO, f"the {i}th item should be a dict")
        
        # 检查必选字段
        required_fields = ["filter_title", "start", "end"]
        missing_fields = [field for field in required_fields if field not in item]
        
        if missing_fields:
            logger.error(f"the {i}th item is missing required fields: {', '.join(missing_fields)}")
            raise CustomException(CustomError.INVALID_FILTER_INFO, f"the {i}th item is missing required fields: {', '.join(missing_fields)}")
        
        # 创建处理后的对象
        processed_item = {
            "filter_title": str(item["filter_title"]),
            "start": item["start"],
            "end": item["end"],
            "intensity": item.get("intensity", 100.0)  # 默认强度为100
        }
        
        # 验证数值类型和范围
        if not isinstance(processed_item["start"], (int, float)) or processed_item["start"] < 0:
            logger.error(f"the {i}th item has invalid start time: {processed_item['start']}")
            raise CustomException(CustomError.INVALID_FILTER_INFO, f"the {i}th item has invalid start time")
        
        if not isinstance(processed_item["end"], (int, float)) or processed_item["end"] <= processed_item["start"]:
            logger.error(f"the {i}th item has invalid end time: {processed_item['end']}")
            raise CustomException(CustomError.INVALID_FILTER_INFO, f"the {i}th item has invalid end time")
        
        # 验证滤镜名称
        if len(processed_item["filter_title"].strip()) == 0:
            logger.error(f"the {i}th item has invalid filter_title: {processed_item['filter_title']}")
            raise CustomException(CustomError.INVALID_FILTER_INFO, f"the {i}th item has invalid filter_title")
        
        # 验证强度范围
        if not isinstance(processed_item["intensity"], (int, float)) or processed_item["intensity"] < 0 or processed_item["intensity"] > 100:
            logger.error(f"the {i}th item has invalid intensity: {processed_item['intensity']}")
            raise CustomException(CustomError.INVALID_FILTER_INFO, f"the {i}th item has invalid intensity (must be 0-100)")
        
        # 将时间转换为整数（微秒）
        processed_item["start"] = int(processed_item["start"])
        processed_item["end"] = int(processed_item["end"])
        processed_item["intensity"] = float(processed_item["intensity"])
        
        result.append(processed_item)
    
    logger.info(f"Successfully parsed {len(result)} filter items")
    return result
