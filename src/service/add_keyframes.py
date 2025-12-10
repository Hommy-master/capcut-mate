import json
from typing import List, Dict, Any, Tuple, Optional

from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile
from src.pyJianYingDraft.keyframe import KeyframeProperty
from src.pyJianYingDraft.segment import VisualSegment
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
from src.utils import helper


def add_keyframes(
    draft_url: str,
    keyframes: str
) -> Tuple[str, int, List[str]]:
    """
    添加关键帧到剪映草稿的业务逻辑
    
    Args:
        draft_url: 草稿URL
        keyframes: 关键帧信息列表的JSON字符串，格式如下：
            [
                {
                    "segment_id": "d62994b4-25fe-422a-a123-87ef05038558",  # 目标片段的唯一标识ID
                    "property": "KFTypePositionX",  # 动画属性类型
                    "offset": 0.5,  # 关键帧在片段中的时间偏移（0-1范围）
                    "value": -0.1  # 属性在该时间点的值
                }
            ]
    
    Returns:
        draft_url: 草稿URL
        keyframes_added: 添加的关键帧数量
        affected_segments: 受影响的片段ID列表
    
    Raises:
        CustomException: 关键帧添加失败
    """
    logger.info(f"add_keyframes started, draft_url: {draft_url}, keyframes: {keyframes}")

    # 1. 提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        logger.error(f"Invalid draft_url or draft not found in cache: {draft_url}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    # 2. 解析关键帧信息
    keyframe_items = parse_keyframes_data(json_str=keyframes)
    if len(keyframe_items) == 0:
        logger.info(f"No keyframe info provided, draft_id: {draft_id}")
        raise CustomException(CustomError.INVALID_KEYFRAME_INFO)

    logger.info(f"Parsed {len(keyframe_items)} keyframe items")

    # 3. 从缓存中获取草稿
    script: ScriptFile = DRAFT_CACHE[draft_id]

    # 4. 处理每个关键帧
    keyframes_added = 0
    affected_segments: List[str] = []
    failed_keyframes = 0  # 记录失败的关键帧数量
    
    for i, keyframe_item in enumerate(keyframe_items):
        try:
            logger.info(f"Processing keyframe {i+1}/{len(keyframe_items)}, segment_id: {keyframe_item['segment_id']}, property: {keyframe_item['property']}")
            
            # 查找片段
            segment = find_segment_by_id(script, keyframe_item['segment_id'])
            if segment is None:
                logger.error(f"Segment not found: {keyframe_item['segment_id']}, skipping this keyframe")
                failed_keyframes += 1
                continue  # 继续处理下一个关键帧，而不是抛出异常
            
            # 验证片段类型
            if not isinstance(segment, VisualSegment):
                logger.error(f"Segment {keyframe_item['segment_id']} is not a visual segment, cannot add keyframes, skipping this keyframe")
                failed_keyframes += 1
                continue  # 继续处理下一个关键帧
            
            # 验证动画属性类型
            try:
                property_enum = KeyframeProperty(keyframe_item['property'])
            except ValueError:
                logger.error(f"Invalid property type: {keyframe_item['property']}, skipping this keyframe")
                failed_keyframes += 1
                continue  # 继续处理下一个关键帧
            
            # 计算时间偏移（将相对位置转换为微秒）
            segment_duration = segment.duration
            time_offset = int(keyframe_item['offset'] * segment_duration)
            
            logger.info(f"Adding keyframe to segment {keyframe_item['segment_id']}: property={property_enum.value}, time_offset={time_offset}, value={keyframe_item['value']}")
            
            # 添加关键帧
            segment.add_keyframe(property_enum, time_offset, keyframe_item['value'])
            
            keyframes_added += 1
            if keyframe_item['segment_id'] not in affected_segments:
                affected_segments.append(keyframe_item['segment_id'])
                
            logger.info(f"Successfully added keyframe {i+1}, total added: {keyframes_added}")
            
        except Exception as e:
            logger.error(f"Failed to add keyframe {i+1}, error: {str(e)}, skipping this keyframe")
            failed_keyframes += 1
            # 继续处理下一个关键帧，而不是抛出异常
    
    # 5. 保存草稿
    try:
        script.save()
        logger.info(f"Draft saved successfully, keyframes_added: {keyframes_added}, failed_keyframes: {failed_keyframes}")
    except Exception as e:
        logger.error(f"Failed to save draft: {str(e)}")
        raise CustomException(CustomError.KEYFRAME_ADD_FAILED)
    
    logger.info(f"add_keyframes completed - draft_id: {draft_id}, keyframes_added: {keyframes_added}, affected_segments: {affected_segments}, failed_keyframes: {failed_keyframes}")
    
    return draft_url, keyframes_added, affected_segments


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


def parse_keyframes_data(json_str: str) -> List[Dict[str, Any]]:
    """
    解析关键帧数据的JSON字符串，验证必选字段和数值范围
    
    Args:
        json_str: 包含关键帧数据的JSON字符串，格式如下：
        [
            {
                "segment_id": "d62994b4-25fe-422a-a123-87ef05038558",  # [必选] 目标片段的唯一标识ID
                "property": "KFTypePositionX",  # [必选] 动画属性类型
                "offset": 0.5,  # [必选] 关键帧在片段中的时间偏移（0-1范围）
                "value": -0.1  # [必选] 属性在该时间点的值
            }
        ]
    
    Returns:
        包含关键帧对象的数组，每个对象都验证过格式和范围
    
    Raises:
        CustomException: 当JSON格式错误或缺少必选字段时抛出
    """
    try:
        # 解析JSON字符串
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e.msg}")
        raise CustomException(CustomError.INVALID_KEYFRAME_INFO, f"JSON parse error: {e.msg}")
    
    # 确保输入是列表
    if not isinstance(data, list):
        logger.error("keyframes should be a list")
        raise CustomException(CustomError.INVALID_KEYFRAME_INFO, "keyframes should be a list")
    
    result = []
    
    # 支持的动画属性类型
    supported_properties = {
        "KFTypePositionX", "KFTypePositionY", "KFTypeScaleX", 
        "KFTypeScaleY", "KFTypeRotation", "KFTypeAlpha"
    }
    
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            logger.error(f"the {i}th item should be a dict")
            raise CustomException(CustomError.INVALID_KEYFRAME_INFO, f"the {i}th item should be a dict")
        
        # 检查必选字段
        required_fields = ["segment_id", "property", "offset", "value"]
        missing_fields = [field for field in required_fields if field not in item]
        
        if missing_fields:
            logger.error(f"the {i}th item is missing required fields: {', '.join(missing_fields)}")
            raise CustomException(CustomError.INVALID_KEYFRAME_INFO, f"the {i}th item is missing required fields: {', '.join(missing_fields)}")
        
        # 验证动画属性类型
        if item["property"] not in supported_properties:
            logger.error(f"the {i}th item has unsupported property type: {item['property']}")
            raise CustomException(CustomError.INVALID_KEYFRAME_INFO, f"the {i}th item has unsupported property type: {item['property']}")
        
        # 验证offset范围（0-1）
        if not isinstance(item["offset"], (int, float)) or item["offset"] < 0.0 or item["offset"] > 1.0:
            logger.error(f"the {i}th item has invalid offset value: {item['offset']}, must be between 0.0 and 1.0")
            raise CustomException(CustomError.INVALID_KEYFRAME_INFO, f"the {i}th item has invalid offset value: {item['offset']}")
        
        # 验证value是数字类型
        if not isinstance(item["value"], (int, float)):
            logger.error(f"the {i}th item has invalid value type: {type(item['value'])}, must be a number")
            raise CustomException(CustomError.INVALID_KEYFRAME_INFO, f"the {i}th item has invalid value type: {type(item['value'])}")
        
        # 创建处理后的对象
        processed_item = {
            "segment_id": str(item["segment_id"]),
            "property": item["property"],
            "offset": float(item["offset"]),
            "value": float(item["value"])
        }
        
        result.append(processed_item)
    
    logger.info(f"Successfully parsed {len(result)} keyframe items")
    return result