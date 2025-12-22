from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile, trange
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

        # 2. 如果没有提供duration，则从音频文件中获取实际时长
        if audio.get('duration') is None:
            # 创建临时AudioMaterial对象来获取音频时长
            temp_material = AudioMaterial(audio_path)
            audio['duration'] = temp_material.duration
            logger.info(f"Auto-detected audio duration: {audio['duration']} microseconds")

        # 3. 计算截取时长
        segment_duration = audio['end'] - audio['start']
        logger.info(f"Audio trimming params - start: {audio['start']} microseconds, end: {audio['end']} microseconds, duration: {segment_duration} microseconds")

        # 5. 创建音频素材并添加到草稿
        # 使用逻辑截取，通过source_timerange设置音频片段的开始和结束时间
        audio_segment = draft.AudioSegment(
            material=audio_path,  # 使用原始音频文件
            source_timerange=trange(start=audio['start'], duration=segment_duration),  # 设置从原始音频的哪个位置开始截取
            target_timerange=trange(start=0, duration=segment_duration),  # 轨道开始时间从0开始
            volume=audio['volume']
        )
        
        # 3. 添加音频效果（如果指定了）
        if audio.get('audio_effect'):
            try:
                # 添加音频效果
                audio_effect = audio['audio_effect']
                effect_type = None
                
                # 查找对应的音频效果类型
                for effect_name, effect_meta in draft.AudioSceneEffectType.__members__.items():
                    if effect_meta.value.name == audio_effect:
                        effect_type = effect_meta
                        break
                
                # 如果找到了对应的效果类型，则添加效果
                if effect_type:
                    # 获取效果的默认参数，转换为0-100范围内的值列表
                    # 注意：add_effect方法需要的是0-100范围内的参数值列表
                    # 而不是直接传递实际值
                    params_list = []
                    for param in effect_type.value.params:
                        # 将实际默认值转换为0-100范围内的值
                        # 例如：如果参数范围是0-1，默认值是1，则转换为100
                        if param.min_value != param.max_value:
                            # 计算参数值在0-100范围内的对应值
                            param_value = ((param.default_value - param.min_value) / (param.max_value - param.min_value)) * 100
                        else:
                            # 如果参数范围是固定值，则使用50作为默认值
                            param_value = 50
                        params_list.append(param_value)
                    
                    # 添加效果
                    audio_segment.add_effect(
                        effect_type=effect_type,
                        params=params_list
                    )
                    logger.info(f"Added audio effect: {audio_effect} with params: {params_list}")
                else:
                    logger.warning(f"Unknown audio effect: {audio_effect}")
            except Exception as e:
                logger.warning(f"Failed to add audio effect '{audio['audio_effect']}': {str(e)}")

        logger.info(f"Created audio segment, material_id: {audio_segment.material_instance.material_id}")
        logger.info(f"Audio segment details - start: {audio['start']}, duration: {segment_duration}, volume: {audio['volume']}")

        # 4. 向指定轨道添加片段
        script.add_segment(audio_segment, track_name)

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
        
        if processed_item["start"] < 0 or processed_item["end"] <= processed_item["start"]:
            logger.error(f"Invalid time range: start={processed_item['start']}, end={processed_item['end']}")
            raise CustomException(CustomError.INVALID_AUDIO_INFO, f"the {i}th item has invalid time range")
        
        # 如果提供了duration且小于等于0，则报错
        if processed_item["duration"] is not None and processed_item["duration"] <= 0:
            logger.error(f"Invalid duration: {processed_item['duration']}")
            raise CustomException(CustomError.INVALID_AUDIO_INFO, f"the {i}th item has invalid duration")
        
        result.append(processed_item)
        logger.debug(f"Processed audio item {i+1}: {processed_item}")
    
    return result