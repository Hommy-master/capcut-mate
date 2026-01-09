from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile, trange, AudioSceneEffectType, VideoSceneEffectType, VideoCharacterEffectType
import src.pyJianYingDraft as draft
from src.pyJianYingDraft.local_materials import AudioMaterial
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
import os
from src.utils import helper
from src.utils.download import download
import config
import json
from typing import List, Dict, Any, Tuple


def add_audios(
    draft_url: str, 
    audio_infos: str
) -> Tuple[str, str, List[str]]:
    """
    添加音频到剪映草稿的业务逻辑
    
    Args:
        draft_url: 草稿URL，必选参数
        audio_infos: 音频信息JSON字符串，格式如下：
        [
            {
                "audio_url": "https://example.com/audio.mp3", // [必选] 音频文件URL
                "duration": 23184000, // [可选] 音频总时长(微秒)，如果不提供将自动获取
                "end": 23184000, // [必选] 音频片段结束时间(微秒)
                "start": 0, // [必选] 音频片段开始时间(微秒)
                "volume": 1.0, // [可选] 音频音量[0.0, 2.0]，默认值为1.0
                "audio_effect": "reverb" // [可选] 音频效果名称，默认值为None
            }
        ]
        
    Returns:
        draft_url: 草稿URL
        track_id: 音频轨道ID（非主轨道）
        audio_ids: 音频ID列表

    Raises:
        CustomException: 音频批量添加失败
    """
    logger.info(f"add_audios, draft_url: {draft_url}, audio_infos: {audio_infos}")

    # 1. 提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        logger.error(f"Invalid draft URL or draft not found in cache, draft_id: {draft_id}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    # 2. 创建保存音频资源的目录
    draft_dir = os.path.join(config.DRAFT_DIR, draft_id)
    draft_audio_dir = os.path.join(draft_dir, "assets", "audios")
    os.makedirs(name=draft_audio_dir, exist_ok=True)
    logger.info(f"Created audio directory: {draft_audio_dir}")

    # 3. 解析音频信息
    audios = parse_audio_data(json_str=audio_infos)
    if len(audios) == 0:
        logger.error(f"No audio info provided, draft_id: {draft_id}")
        raise CustomException(CustomError.INVALID_AUDIO_INFO)
    logger.info(f"Parsed {len(audios)} audio items")

    # 4. 从缓存中获取草稿
    script: ScriptFile = DRAFT_CACHE[draft_id]

    # 5. 添加音频轨道（明确说明不使用主轨道，并设置合适的渲染层级）
    track_name = f"audio_track_{helper.gen_unique_id()}"
    # 设置 relative_index=10 确保音频轨道在主音频轨道之上，避免与主轨道冲突
    script.add_track(track_type=draft.TrackType.audio, track_name=track_name, relative_index=10)
    logger.info(f"Added audio track (non-main track): {track_name}")

    # 6. 遍历音频信息，添加音频到草稿中的指定轨道，收集音频ID
    audio_ids = []
    for i, audio in enumerate(audios):
        try:
            audio_id = add_audio_to_draft(script, track_name, draft_audio_dir=draft_audio_dir, audio=audio)
            audio_ids.append(audio_id)
            logger.info(f"Added audio {i+1}/{len(audios)}, audio_id: {audio_id}")
        except Exception as e:
            logger.error(f"Failed to add audio {i+1}/{len(audios)}, error: {str(e)}")
            raise

    # 7. 保存草稿
    script.save()
    logger.info(f"Draft saved successfully")

    # 8. 获取当前音频轨道ID
    track_id = ""
    for key in script.tracks.keys():
        if script.tracks[key].name == track_name:
            track_id = script.tracks[key].track_id
            break
    logger.info(f"Audio track created, draft_id: {draft_id}, track_id: {track_id}")

    return draft_url, track_id, audio_ids


def find_audio_effect_type(audio_effect: str):
    """
    根据音频效果名称查找对应的效果类型
    
    Args:
        audio_effect: 音频效果名称
    
    Returns:
        effect_type: 对应的效果类型对象，如果未找到则返回None
    """
    effect_type = None
    
    # 查找对应的音频效果类型
    for effect_name, effect_meta in AudioSceneEffectType.__members__.items():
        if effect_meta.value.name == audio_effect:
            effect_type = effect_meta
            break
    
    # 如果没找到，则尝试在VideoSceneEffectType中查找
    if effect_type is None:
        for effect_name, effect_meta in VideoSceneEffectType.__members__.items():
            if effect_meta.value.name == audio_effect:
                effect_type = effect_meta
                break
    
    # 如果没找到，则尝试在VideoCharacterEffectType中查找
    if effect_type is None:
        for effect_name, effect_meta in VideoCharacterEffectType.__members__.items():
            if effect_meta.value.name == audio_effect:
                effect_type = effect_meta
                break
    
    return effect_type


def convert_params_to_range(effect_type) -> list:
    """
    将效果参数转换为0-100范围内的值列表
    
    Args:
        effect_type: 效果类型对象
    
    Returns:
        params_list: 转换后的参数值列表
    """
    params_list = []
    for param in effect_type.value.params:
        # 将实际默认值转换为0-100范围内的值
        if param.min_value != param.max_value:
            # 计算参数值在0-100范围内的对应值
            param_value = ((param.default_value - param.min_value) / (param.max_value - param.min_value)) * 100
        else:
            # 如果参数范围是固定值，则使用50作为默认值
            param_value = 50
        params_list.append(param_value)
    
    return params_list


def add_audio_effect(audio_segment, audio_effect: str):
    """
    为音频片段添加音频效果
    
    Args:
        audio_segment: 音频片段对象
        audio_effect: 音频效果名称
    """
    effect_type = find_audio_effect_type(audio_effect)
    
    # 如果找到了对应的效果类型，则添加效果
    if effect_type:
        params_list = convert_params_to_range(effect_type)
        
        # 添加效果
        audio_segment.add_effect(
            effect_type=effect_type,
            params=params_list
        )
        logger.info(f"Added audio effect: {audio_effect} with params: {params_list}")
    else:
        logger.warning(f"Unknown audio effect: {audio_effect}")


def add_audio_to_draft(
    script: ScriptFile,
    track_name: str,
    draft_audio_dir: str,
    audio: dict
) -> str:
    """
    向剪映草稿中添加单个音频
    
    Args:
        script: 草稿文件对象
        track_name: 音频轨道名称
        draft_audio_dir: 音频资源目录
        audio: 音频信息字典，包含以下字段：
            audio_url: 音频URL
            duration: 音频总时长(微秒)，可选字段
            start: 开始时间(微秒)
            end: 结束时间(微秒)
            volume: 音量[0.0, 2.0]
            audio_effect: 音频效果名称(可选)
    
    Returns:
        material_id: 音频素材ID
    
    Raises:
        CustomException: 添加音频失败
    """
    try:
        # 1. 下载音频文件
        audio_path = download(url=audio['audio_url'], save_dir=draft_audio_dir)
        logger.info(f"Downloaded audio from {audio['audio_url']} to {audio_path}")

        # 2. 获取音频的实际时长
        temp_material = AudioMaterial(audio_path)
        actual_duration = temp_material.duration
        logger.info(f"Actual audio duration: {actual_duration} microseconds")
        
        # 3. 如果没有提供duration，则使用实际检测到的时长
        if audio.get('duration') is None:
            audio['duration'] = actual_duration
            logger.info(f"Using detected audio duration: {actual_duration} microseconds")
        
        # 4. 根据音频实际时长和指定时长进行智能调整
        start_time = audio['start']
        requested_end_time = audio['end']
        requested_duration = requested_end_time - start_time
        
        # 检查并修正开始时间，确保不小于0
        if start_time < 0:
            logger.warning(f"Start time {start_time} is negative, setting to 0")
            start_time = 0
            
        # 根据实际音频时长和请求的时长进行智能处理
        if actual_duration < requested_duration:
            # 情况1: 音频实际长度不够（小于end - start）时，使用音频实际时长
            logger.warning(f"Audio actual duration {actual_duration} is less than requested duration {requested_duration}, using actual duration")
            # 使用音频实际时长，但保持起始时间不变
            segment_duration = actual_duration
            end_time = start_time + segment_duration
        else:
            # 情况2: 音频实际时长足够时，使用指定的end作为结束时间（但不超过音频实际时长）
            calculated_end_time = min(requested_end_time, start_time + actual_duration)
            segment_duration = calculated_end_time - start_time
            end_time = calculated_end_time
        
        # 确保片段至少有最小持续时间，避免0持续时间导致的问题
        if segment_duration <= 0:
            logger.warning(f"Segment duration is zero or negative ({segment_duration}), setting to minimum duration")
            # 设置最小持续时间，比如100微秒，这样可以避免重叠问题
            segment_duration = 100
            end_time = start_time + segment_duration
        
        # 更新音频对象中的时间参数
        audio['start'] = start_time
        audio['end'] = end_time
        
        # 5. 计算片段持续时间
        logger.info(f"Adjusted audio segment: start={start_time}, end={end_time}, duration={segment_duration}, requested_duration={requested_duration}")
        
        # 6. 创建音频素材并添加到草稿
        audio_segment = draft.AudioSegment(
            material=audio_path,
            target_timerange=trange(start=start_time, duration=segment_duration),
            volume=audio['volume']
        )
        
        # 7. 添加音频效果（如果指定了）
        if audio.get('audio_effect'):
            add_audio_effect(audio_segment, audio['audio_effect'])

        logger.info(f"Created audio segment, material_id: {audio_segment.material_instance.material_id}")
        logger.info(f"Audio segment details - start: {start_time}, duration: {segment_duration}, volume: {audio['volume']}")

        # 8. 向指定轨道添加片段
        try:
            script.add_segment(audio_segment, track_name)
        except Exception as e:
            # 如果添加片段时出现重叠错误，尝试调整片段位置
            if "overlaps" in str(e) or "overlap" in str(e).lower():
                logger.warning(f"Segment overlap detected: {str(e)}, attempting to adjust")
                # 稍微调整片段的开始时间，避免重叠
                # 逐步增加偏移量，直到不再重叠
                offset = 100
                max_attempts = 10
                attempts = 0
                
                while attempts < max_attempts:
                    try:
                        adjusted_start = start_time + offset
                        logger.info(f"Attempt {attempts + 1}: Adjusting segment start time from {start_time} to {adjusted_start}")
                        
                        # 重新创建片段，使用调整后的时间
                        audio_segment = draft.AudioSegment(
                            material=audio_path,
                            target_timerange=trange(start=adjusted_start, duration=segment_duration),
                            volume=audio['volume']
                        )
                        
                        # 再次尝试添加片段
                        script.add_segment(audio_segment, track_name)
                        logger.info(f"Successfully added adjusted segment with start time {adjusted_start}")
                        break  # 成功添加，跳出循环
                    except Exception as retry_e:
                        if "overlaps" in str(retry_e) or "overlap" in str(retry_e).lower():
                            attempts += 1
                            offset += 100  # 增加偏移量
                            logger.info(f"Still overlapping, increasing offset to {offset}")
                        else:
                            # 如果不是重叠错误，重新抛出异常
                            raise
                
                if attempts >= max_attempts:
                    logger.error(f"Failed to add segment after {max_attempts} attempts, giving up")
                    raise
            else:
                # 如果不是重叠错误，重新抛出异常
                raise

        return audio_segment.material_instance.material_id
        
    except CustomException:
        logger.error(f"Add audio to draft failed, draft_audio_dir: {draft_audio_dir}, audio: {audio}")
        raise
    except Exception as e:
        logger.error(f"Add audio to draft failed, error: {str(e)}")
        raise CustomException(err=CustomError.AUDIO_ADD_FAILED)


def parse_audio_data(json_str: str) -> List[Dict[str, Any]]:
    """
    解析音频数据的JSON字符串，处理可选字段的默认值
    
    Args:
        json_str: 包含音频数据的JSON字符串，格式如下：
        [
            {
                "audio_url": "https://example.com/audio.mp3", // [必选] 音频文件URL
                "duration": 23184000, // [可选] 音频总时长(微秒)，如果不提供将自动获取
                "end": 23184000, // [必选] 音频片段结束时间(微秒)
                "start": 0, // [必选] 音频片段开始时间(微秒)
                "volume": 1.0, // [可选] 音频音量[0.0, 2.0]，默认值为1.0
                "audio_effect": "reverb" // [可选] 音频效果名称，默认值为None
            }
        ]
        
    Returns:
        包含音频对象的数组，每个对象都处理了默认值
        
    Raises:
        CustomException: 当JSON格式错误或缺少必选字段时抛出
    """
    try:
        # 解析JSON字符串
        data = json.loads(json_str)
        logger.info(f"Successfully parsed JSON with {len(data) if isinstance(data, list) else 1} items")
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e.msg}")
        raise CustomException(CustomError.INVALID_AUDIO_INFO, f"JSON parse error: {e.msg}")
    
    # 确保输入是列表
    if not isinstance(data, list):
        logger.error("Audio infos should be a list")
        raise CustomException(CustomError.INVALID_AUDIO_INFO, "audio_infos should be a list")
    
    result = []
    
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            logger.error(f"The {i}th item should be a dict")
            raise CustomException(CustomError.INVALID_AUDIO_INFO, f"the {i}th item should be a dict")
        
        # 检查必选字段
        required_fields = ["audio_url", "start", "end"]
        missing_fields = [field for field in required_fields if field not in item]
        
        if missing_fields:
            logger.error(f"The {i}th item is missing required fields: {', '.join(missing_fields)}")
            raise CustomException(CustomError.INVALID_AUDIO_INFO, f"the {i}th item is missing required fields: {', '.join(missing_fields)}")
        
        # 创建处理后的对象，设置默认值
        processed_item = {
            "audio_url": item["audio_url"],
            "duration": item.get("duration"),  # duration变为可选字段
            "start": item["start"],
            "end": item["end"],
            "volume": item.get("volume", 1.0),  # 默认音量 1.0
            "audio_effect": item.get("audio_effect", None)  # 默认无音频效果
        }
        
        # 验证数值范围
        if processed_item["volume"] < 0.0 or processed_item["volume"] > 2.0:
            logger.warning(f"Volume value {processed_item['volume']} out of range [0.0, 2.0], using default 1.0")
            processed_item["volume"] = 1.0
        
        # 不在此处严格验证时间范围，留待后续处理中进行容错调整
        # 如果开始时间大于结束时间或等于结束时间，我们将在 add_audio_to_draft 函数中进行智能调整
        
        # 如果提供了duration且小于等于0，则报错
        if processed_item["duration"] is not None and processed_item["duration"] <= 0:
            logger.error(f"Invalid duration: {processed_item['duration']}")
            raise CustomException(CustomError.INVALID_AUDIO_INFO, f"the {i}th item has invalid duration")
        
        result.append(processed_item)
        logger.debug(f"Processed audio item {i+1}: {processed_item}")
    
    return result