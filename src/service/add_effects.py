import json
from typing import List, Dict, Any, Tuple, Optional, Union

from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile, TrackType, EffectSegment, Timerange
from src.pyJianYingDraft.metadata import VideoSceneEffectType, VideoCharacterEffectType
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
from src.utils import helper


def add_effects(
    draft_url: str,
    effect_infos: str
) -> Tuple[str, str, List[str], List[str]]:
    """
    添加特效到剪映草稿的业务逻辑

    Args:
        draft_url: 草稿URL
        effect_infos: 特效信息列表的JSON字符串，格式如下：
            [
                {
                    "effect_title": "录制边框 III",  # 特效名称/标题，必选参数
                    "start": 0,  # 特效开始时间（微秒），必选参数
                    "end": 5000000,  # 特效结束时间（微秒），必选参数
                    "params": [50, 80, 100]  # 特效参数列表，可选参数，取值范围[0, 100]
                }
            ]

    Returns:
        draft_url: 草稿URL
        track_id: 特效轨道ID
        effect_ids: 特效ID列表
        segment_ids: 特效片段ID列表

    Raises:
        CustomException: 特效添加失败
    """
    logger.info(f"add_effects started, draft_url: {draft_url}, effects count: {len(json.loads(effect_infos) if effect_infos else [])}")

    # 1. 提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        logger.error(f"Invalid draft_url or draft not found in cache: {draft_url}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    # 2. 解析特效信息
    effect_items = parse_effects_data(json_str=effect_infos)
    if len(effect_items) == 0:
        logger.info(f"No effect info provided, draft_id: {draft_id}")
        raise CustomException(CustomError.INVALID_EFFECT_INFO)

    logger.info(f"Parsed {len(effect_items)} effect items")

    # 3. 从缓存中获取草稿
    script: ScriptFile = DRAFT_CACHE[draft_id]

    # 4. 添加特效轨道
    track_name = f"effect_track_{helper.gen_unique_id()}"
    script.add_track(track_type=TrackType.effect, track_name=track_name)
    logger.info(f"Added effect track: {track_name}")

    # 5. 遍历特效信息，添加特效到草稿中的指定轨道，收集片段ID
    segment_ids = []
    effect_ids = []
    for i, effect in enumerate(effect_items):
        try:
            logger.info(f"Processing effect {i+1}/{len(effect_items)}, title: {effect['effect_title']}")

            segment_id, effect_id = add_effect_to_draft(
                script, track_name, effect=effect
            )
            segment_ids.append(segment_id)
            effect_ids.append(effect_id)
            logger.info(f"Added effect {i+1}/{len(effect_items)}, segment_id: {segment_id}")
        except Exception as e:
            logger.error(f"Failed to add effect {i+1}/{len(effect_items)}, error: {str(e)}")
            raise

    # 6. 保存草稿
    script.save()
    logger.info(f"Draft saved successfully")

    # 7. 获取当前特效轨道ID
    track_id = ""
    for key in script.tracks.keys():
        if script.tracks[key].name == track_name:
            track_id = script.tracks[key].track_id
            break
    logger.info(f"Effect track created, draft_id: {draft_id}, track_id: {track_id}")

    logger.info(f"add_effects completed successfully - draft_id: {draft_id}, track_id: {track_id}, effects_added: {len(effect_items)}")

    return draft_url, track_id, effect_ids, segment_ids


def add_effect_to_draft(
    script: ScriptFile,
    track_name: str,
    effect: dict
) -> Tuple[str, str]:
    """
    向剪映草稿中添加单个特效

    Args:
        script: 草稿文件对象
        track_name: 特效轨道名称
        effect: 特效信息字典，包含以下字段：
            effect_title: 特效名称/标题
            start: 特效开始时间（微秒）
            end: 特效结束时间（微秒）
            params: 特效参数列表（可选），取值范围[0, 100]

    Returns:
        segment_id: 片段ID
        effect_id: 特效ID（material_id）

    Raises:
        CustomException: 添加特效失败
    """
    try:
        # 1. 查找特效类型
        effect_type = find_effect_type_by_name(effect['effect_title'])
        if effect_type is None:
            logger.error(f"Effect type not found for title: {effect['effect_title']}")
            raise CustomException(CustomError.EFFECT_NOT_FOUND)

        # 2. 创建时间范围
        effect_duration = effect['end'] - effect['start']
        timerange = Timerange(start=effect['start'], duration=effect_duration)

        # 3. 获取特效参数
        params = effect.get('params', None)
        if params is not None:
            # 验证参数数量
            effect_meta = effect_type.value
            if hasattr(effect_meta, 'params') and len(params) > len(effect_meta.params):
                logger.warning(f"Too many parameters provided for effect '{effect['effect_title']}': provided {len(params)}, expected max {len(effect_meta.params)}")
                params = params[:len(effect_meta.params)]  # 截断多余的参数

            # 验证参数值范围（0-100）
            validated_params = []
            for i, param in enumerate(params):
                if param is None:
                    validated_params.append(None)
                elif not isinstance(param, (int, float)):
                    logger.warning(f"Invalid parameter type at index {i}: {type(param)}, using None")
                    validated_params.append(None)
                elif param < 0 or param > 100:
                    logger.warning(f"Parameter value out of range [0, 100] at index {i}: {param}, clamping")
                    validated_params.append(max(0, min(100, param)))
                else:
                    validated_params.append(float(param))

            params = validated_params
            logger.info(f"Using effect parameters: {params}")

        # 4. 创建特效片段
        effect_segment = EffectSegment(
            effect_type=effect_type,
            target_timerange=timerange,
            params=params
        )

        logger.info(f"Created effect segment, effect_id: {effect_segment.effect_inst.global_id}")
        logger.info(f"Effect segment details - start: {effect['start']}, duration: {effect_duration}, title: {effect['effect_title']}, params: {params}")

        # 5. 向指定轨道添加片段
        script.add_segment(effect_segment, track_name)

        return effect_segment.segment_id, effect_segment.effect_inst.global_id

    except CustomException:
        logger.error(f"Add effect to draft failed, effect: {effect}")
        raise
    except Exception as e:
        logger.error(f"Add effect to draft failed, error: {str(e)}")
        raise CustomException(CustomError.EFFECT_ADD_FAILED)


def find_effect_type_by_name(effect_title: str) -> Optional[Union[VideoSceneEffectType, VideoCharacterEffectType]]:
    """
    根据特效名称查找对应的特效类型

    Args:
        effect_title: 特效名称/标题

    Returns:
        对应的特效类型枚举，如果未找到则返回None
    """
    logger.info(f"Searching for effect type with title: {effect_title}")

    # 搜索VideoSceneEffectType中的特效
    for effect_type in VideoSceneEffectType:
        if effect_type.value.name == effect_title:
            logger.info(f"Found scene effect: {effect_title}")
            return effect_type

    # 搜索VideoCharacterEffectType中的特效
    for effect_type in VideoCharacterEffectType:
        if effect_type.value.name == effect_title:
            logger.info(f"Found character effect: {effect_title}")
            return effect_type

    logger.warning(f"Effect type not found for title: {effect_title}")
    return None


def parse_effects_data(json_str: str) -> List[Dict[str, Any]]:
    """
    解析特效数据的JSON字符串，验证必选字段和数值范围

    Args:
        json_str: 包含特效数据的JSON字符串，格式如下：
        [
            {
                "effect_title": "录制边框 III",  # [必选] 特效名称/标题
                "start": 0,  # [必选] 特效开始时间（微秒）
                "end": 5000000,  # [必选] 特效结束时间（微秒）
                "params": [50, 80, 100]  # [可选] 特效参数列表，取值范围[0, 100]
            }
        ]

    Returns:
        包含特效对象的数组，每个对象都验证过格式和范围

    Raises:
        CustomException: 当JSON格式错误或缺少必选字段时抛出
    """
    try:
        # 解析JSON字符串
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e.msg}")
        raise CustomException(CustomError.INVALID_EFFECT_INFO, f"JSON parse error: {e.msg}")

    # 确保输入是列表
    if not isinstance(data, list):
        logger.error("effect_infos should be a list")
        raise CustomException(CustomError.INVALID_EFFECT_INFO, "effect_infos should be a list")

    result = []

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            logger.error(f"the {i}th item should be a dict")
            raise CustomException(CustomError.INVALID_EFFECT_INFO, f"the {i}th item should be a dict")

        # 检查必选字段
        required_fields = ["effect_title", "start", "end"]
        missing_fields = [field for field in required_fields if field not in item]

        if missing_fields:
            logger.error(f"the {i}th item is missing required fields: {', '.join(missing_fields)}")
            raise CustomException(CustomError.INVALID_EFFECT_INFO, f"the {i}th item is missing required fields: {', '.join(missing_fields)}")

        # 创建处理后的对象
        processed_item = {
            "effect_title": str(item["effect_title"]),
            "start": item["start"],
            "end": item["end"],
            "params": item.get("params", None)  # 添加参数支持
        }

        # 验证数值类型和范围
        if not isinstance(processed_item["start"], (int, float)) or processed_item["start"] < 0:
            logger.error(f"the {i}th item has invalid start time: {processed_item['start']}")
            raise CustomException(CustomError.INVALID_EFFECT_INFO, f"the {i}th item has invalid start time")

        if not isinstance(processed_item["end"], (int, float)) or processed_item["end"] <= processed_item["start"]:
            logger.error(f"the {i}th item has invalid end time: {processed_item['end']}")
            raise CustomException(CustomError.INVALID_EFFECT_INFO, f"the {i}th item has invalid end time")

        # 验证特效名称
        if len(processed_item["effect_title"].strip()) == 0:
            logger.error(f"the {i}th item has invalid effect_title: {processed_item['effect_title']}")
            raise CustomException(CustomError.INVALID_EFFECT_INFO, f"the {i}th item has invalid effect_title")

        # 验证参数列表
        if processed_item["params"] is not None:
            if not isinstance(processed_item["params"], list):
                logger.warning(f"the {i}th item has invalid params type (should be list), ignoring params")
                processed_item["params"] = None
            else:
                # 验证参数列表不为空
                if len(processed_item["params"]) == 0:
                    processed_item["params"] = None
                else:
                    logger.info(f"Effect {i} has {len(processed_item['params'])} parameters")

        # 将时间转换为整数（微秒）
        processed_item["start"] = int(processed_item["start"])
        processed_item["end"] = int(processed_item["end"])

        result.append(processed_item)

    logger.info(f"Successfully parsed {len(result)} effect items")
    return result
