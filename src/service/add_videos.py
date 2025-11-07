from src.pyJianYingDraft.video_segment import VideoSegment


from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile, trange, IntroType
import src.pyJianYingDraft as draft
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
import os
from src.utils import helper
import config
import json
from typing import List, Dict, Any, Tuple, Optional
from src.utils.enum_mapper import (
    map_mask_type, map_transition_type, map_filter_type,
    map_video_intro_type, map_video_outro_type, map_video_group_animation_type
)


def add_videos(
    draft_url: str,
    video_infos: str,
    alpha: float = 1.0,
    scale_x: float = 1.0,
    scale_y: float = 1.0,
    transform_x: int = 0,
    transform_y: int = 0
) -> Tuple[str, str, List[str], List[str]]:
    """
    添加视频到剪映草稿的业务逻辑
    文档：https://jy-api.fyshark.com/docs/API_ADD_VIDEOS.md

    Args:
        draft_url: ""  // [必选] 草稿URL
        video_infos: [
            {
                "video_url": "https://example.com/video1.mp4", // [必选] 视频文件的URL地址
                "width": 1920, // [必选] 视频宽度
                "height": 1080, // [必选] 视频高度
                "start": 0.0, // [必选] 视频在时间轴上的开始时间 (微秒)
                "end": 12000000.0, // [必选] 视频在时间轴上的结束时间 (微秒)
                "duration": 12000000.0, // [必选] 视频总时长(微秒)
                "mask": "", // 遮罩类型[可选]，默认值为None
                "mask_config": {}, // 遮罩配置[可选]
                "transition": "", // 转场效果名称[可选]，默认值为None
                "transition_duration": 500000.0, // 转场持续时间(微秒)[可选]，默认值为500000
                "volume": 1.0, // 音量大小[0, 1][可选]，默认值为1.0
                "filter": "", // 滤镜类型[可选]
                "filter_intensity": 100.0, // 滤镜强度[0, 100][可选]
                "in_animation": "", // 入场动画[可选]
                "out_animation": "", // 出场动画[可选]
                "group_animation": "", // 组合动画[可选]
                "animation_duration": null, // 动画时长(微秒)[可选]
                "background_fill_type": "", // 背景填充类型[可选]，blur或color
                "background_blur": 0.0625, // 背景模糊程度[可选]
                "background_color": "#00000000" // 背景颜色[可选]
            }
        ] // [必选]
        alpha: 全局透明度[0, 1][可选]，默认值为1.0
        scale_x: X轴缩放比例[可选]，默认值为1.0
        scale_y: Y轴缩放比例[可选]，默认值为1.0
        transform_x: X轴位置偏移(像素)[可选]，默认值为0
        transform_y: Y轴位置偏移(像素)[可选]，默认值为0

    Returns:
        "draft_url": "https://ts.fyshark.com/#/cozeToJianyin?drafId=...",
        "track_id": "video-track-uuid",
        "video_ids": ["video1-uuid", "video2-uuid", "video3-uuid"],
        "segment_ids": ["segment1-uuid", "segment2-uuid", "segment3-uuid"],
        "videos_count": 3, [未用]
        "total_duration": 15000000 [未用]

    Raises:
        CustomException: 视频批量添加失败
    """
    logger.info(f"add_videos, draft_url: {draft_url}, video_infos: {video_infos}, alpha: {alpha}, scale_x: {scale_x}, scale_y: {scale_y}, transform_x: {transform_x}, transform_y: {transform_y}")

    # 1. 提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    # 2. 创建保存视频资源的目录
    draft_dir = os.path.join(config.DRAFT_DIR, draft_id)
    draft_video_dir = os.path.join(draft_dir, "assets", "videos")
    os.makedirs(name=draft_video_dir, exist_ok=True)

    # 3. 解析视频信息
    videos = parse_video_data(json_str=video_infos)
    if len(videos) == 0:
        logger.info(f"No video info, draft_id: {draft_id}")
        raise CustomException(CustomError.INVALID_VIDEO_INFO)

    # 4. 从缓存中获取草稿
    script: ScriptFile = DRAFT_CACHE[draft_id]

    # 5. 添加视频轨道
    track_name = f"video_track_{helper.gen_unique_id()}"
    script.add_track(track_type=draft.TrackType.video, track_name=track_name)

    # 6. 遍历视频信息，添加视频到草稿中的指定轨道，收集片段ID
    segment_ids = []
    for video in videos:
        segment_id = add_video_to_draft(
            script, track_name,
            draft_video_dir=draft_video_dir,
            video=video,
            alpha=alpha,
            scale_x=scale_x,
            scale_y=scale_y,
            transform_x=transform_x,
            transform_y=transform_y
        )
        segment_ids.append(segment_id)
    logger.info(f"segment_ids: {segment_ids}")

    # 7. 保存草稿
    script.save()

    # 获取当前视频轨道id
    track_id = ""
    for key in script.tracks.keys():
        if script.tracks[key].name == track_name:
            track_id = script.tracks[key].track_id
            break
    logger.info(f"draft_id: {draft_id}, track_id: {track_id}")

    # 获取当前所有视频资源ID（全局唯一ID）
    # 注意：这里获取的是本次添加的视频的 material_id
    # segment_ids 是片段实例ID，video_ids 是素材ID
    # 由于每次添加都会创建新的素材实例，所以实际上 material_id 等同于 segment 中引用的 material_id
    video_ids = segment_ids  # 在当前实现中，每个片段对应一个素材实例，所以它们是相同的
    logger.info(f"draft_id: {draft_id}, video_ids: {video_ids}")

    return draft_url, track_id, video_ids, segment_ids

def add_video_to_draft(
    script: ScriptFile,
    track_name: str,
    draft_video_dir: str,
    video: dict,
    alpha: float = 1.0,
    scale_x: float = 1.0,
    scale_y: float = 1.0,
    transform_x: int = 0,
    transform_y: int = 0
    ) -> str:
    """
    向剪映草稿中添加视频

    Args:
        script: 草稿文件对象
        track_name: 视频轨道名称
        draft_video_dir: 视频资源目录
        video:
            video_url: 视频URL
            width: 视频宽度,
            height: 视频高度,
            start: 开始时间,
            end: 结束时间,
            duration: 视频总时长,
            mask: 遮罩类型
            mask_config: 遮罩配置（可选）
            transition: 转场
            transition_duration: 转场时长
            volume: 音量
            filter: 滤镜类型（可选）
            filter_intensity: 滤镜强度（可选）
            in_animation: 入场动画（可选）
            out_animation: 出场动画（可选）
            group_animation: 组合动画（可选）
            animation_duration: 动画时长（可选）
            background_fill_type: 背景填充类型（可选，blur或color）
            background_blur: 背景模糊程度（可选）
            background_color: 背景颜色（可选）
        alpha: 视频透明度
        scale_x: 横向缩放
        scale_y: 纵向缩放
        transform_x: X轴位置偏移(像素)
        transform_y: Y轴位置偏移(像素)

    Returns:
        material_id: 素材ID
    """
    try:
        # 0. 下载视频
        video_path = helper.download(url=video['video_url'], save_dir=draft_video_dir)

        # 1. 创建图像调节设置
        clip_settings = draft.ClipSettings(
            alpha=alpha,
            scale_x=scale_x,
            scale_y=scale_y,
            transform_x=transform_x / (video['width'] / 2) if video['width'] > 0 else 0,
            transform_y=transform_y / (video['height'] / 2) if video['height'] > 0 else 0
        )

        # 2. 创建视频素材并添加到草稿
        duration = video['end'] - video['start']
        video_segment = draft.VideoSegment(
            material=video_path,
            target_timerange=trange(start=video['start'], duration=duration),
            volume=video['volume'],
            clip_settings=clip_settings
        )
        logger.info(f"material_id: {video_segment.material_instance.material_id}")
        logger.info(f"video_path: {video_path}, start: {video['start']}, duration: {duration}, volume: {video['volume']}")

        # 3. 添加遮罩
        if video.get('mask'):
            try:
                mask_type = map_mask_type(video['mask'])
                if mask_type:
                    mask_config = video.get('mask_config', {})
                    video_segment.add_mask(
                        mask_type,
                        center_x=mask_config.get('center_x', 0.0),
                        center_y=mask_config.get('center_y', 0.0),
                        size=mask_config.get('size', 0.5),
                        rotation=mask_config.get('rotation', 0.0),
                        feather=mask_config.get('feather', 0.0),
                        invert=mask_config.get('invert', False),
                        rect_width=mask_config.get('rect_width'),
                        round_corner=mask_config.get('round_corner')
                    )
                    logger.info(f"Added mask: {video['mask']}")
                else:
                    logger.warning(f"Mask type not found: {video['mask']}")
            except Exception as e:
                logger.warning(f"Failed to add mask '{video['mask']}': {str(e)}")

        # 4. 添加转场
        if video.get('transition'):
            try:
                transition_type = map_transition_type(video['transition'])
                if transition_type:
                    video_segment.add_transition(
                        transition_type,
                        duration=video.get('transition_duration')
                    )
                    logger.info(f"Added transition: {video['transition']}, duration: {video.get('transition_duration')}")
                else:
                    logger.warning(f"Transition type not found: {video['transition']}")
            except Exception as e:
                logger.warning(f"Failed to add transition '{video['transition']}': {str(e)}")

        # 5. 添加滤镜
        if video.get('filter'):
            try:
                filter_type = map_filter_type(video['filter'])
                if filter_type:
                    intensity = video.get('filter_intensity', 100.0)
                    video_segment.add_filter(filter_type, intensity)
                    logger.info(f"Added filter: {video['filter']}, intensity: {intensity}")
                else:
                    logger.warning(f"Filter type not found: {video['filter']}")
            except Exception as e:
                logger.warning(f"Failed to add filter '{video['filter']}': {str(e)}")

        # 6. 添加入场动画
        if video.get('in_animation'):
            try:
                intro_type = map_video_intro_type(video['in_animation'])
                if intro_type:
                    video_segment.add_animation(
                        intro_type,
                        duration=video.get('animation_duration')
                    )
                    logger.info(f"Added in_animation: {video['in_animation']}")
                else:
                    logger.warning(f"Intro animation type not found: {video['in_animation']}")
            except Exception as e:
                logger.warning(f"Failed to add in_animation '{video['in_animation']}': {str(e)}")

        # 7. 添加出场动画
        if video.get('out_animation'):
            try:
                outro_type = map_video_outro_type(video['out_animation'])
                if outro_type:
                    video_segment.add_animation(
                        outro_type,
                        duration=video.get('animation_duration')
                    )
                    logger.info(f"Added out_animation: {video['out_animation']}")
                else:
                    logger.warning(f"Outro animation type not found: {video['out_animation']}")
            except Exception as e:
                logger.warning(f"Failed to add out_animation '{video['out_animation']}': {str(e)}")

        # 8. 添加组合动画
        if video.get('group_animation'):
            try:
                group_type = map_video_group_animation_type(video['group_animation'])
                if group_type:
                    video_segment.add_animation(
                        group_type,
                        duration=video.get('animation_duration')
                    )
                    logger.info(f"Added group_animation: {video['group_animation']}")
                else:
                    logger.warning(f"Group animation type not found: {video['group_animation']}")
            except Exception as e:
                logger.warning(f"Failed to add group_animation '{video['group_animation']}': {str(e)}")

        # 9. 添加背景填充
        if video.get('background_fill_type'):
            try:
                fill_type = video['background_fill_type']
                blur = video.get('background_blur', 0.0625)
                color = video.get('background_color', '#00000000')
                video_segment.add_background_filling(fill_type, blur, color)
                logger.info(f"Added background filling: type={fill_type}, blur={blur}, color={color}")
            except Exception as e:
                logger.warning(f"Failed to add background filling: {str(e)}")

        # 10. 向指定轨道添加片段
        script.add_segment(video_segment, track_name)

        return video_segment.material_instance.material_id
    except CustomException:
        logger.error(f"Add video to draft failed, draft_video_dir: {draft_video_dir}, video: {video}")
        raise
    except Exception as e:
        logger.error(f"Add video to draft failed, error: {str(e)}")
        raise CustomException(err=CustomError.VIDEO_ADD_FAILED)

def parse_video_data(json_str: str) -> List[Dict[str, Any]]:
    """
    解析视频数据的JSON字符串，处理可选字段的默认值

    Args:
        json_str: 包含视频数据的JSON字符串，格式如下：
        [
            {
                "video_url": "https://example.com/video1.mp4", // [必选] 视频文件的URL地址
                "width": 1920, // [必选] 视频宽度
                "height": 1080, // [必选] 视频高度
                "start": 0.0, // [必选] 视频在时间轴上的开始时间
                "end": 12000000.0, // [必选] 视频在时间轴上的结束时间
                "duration": 12000000.0, // [必选] 视频总时长(微秒)
                "mask": "", // 遮罩类型[可选]，默认值为None
                "mask_config": {}, // 遮罩配置[可选]
                "transition": "", // 转场效果名称[可选]，默认值为None
                "transition_duration": 500000.0, // 转场持续时间(微秒)[可选]，默认值为500000
                "volume": 1.0, // 音量大小[0, 1][可选]，默认值为1.0
                "filter": "", // 滤镜类型[可选]
                "filter_intensity": 100.0, // 滤镜强度[0, 100][可选]
                "in_animation": "", // 入场动画[可选]
                "out_animation": "", // 出场动画[可选]
                "group_animation": "", // 组合动画[可选]
                "animation_duration": null, // 动画时长(微秒)[可选]
                "background_fill_type": "", // 背景填充类型[可选]，blur或color
                "background_blur": 0.0625, // 背景模糊程度[可选]
                "background_color": "#00000000" // 背景颜色[可选]
            }
        ]

    Returns:
        包含视频对象的数组，每个对象都处理了默认值

    Raises:
        json.JSONDecodeError: 当JSON格式错误时抛出
        KeyError: 当缺少必选字段时抛出
    """
    try:
        # 解析JSON字符串
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise CustomException(CustomError.INVALID_VIDEO_INFO, f"JSON parse error: {e.msg}")

    # 确保输入是列表
    if not isinstance(data, list):
        raise CustomException(CustomError.INVALID_VIDEO_INFO, "video_infos should be a list")

    result = []

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise CustomException(CustomError.INVALID_VIDEO_INFO, f"the {i}th item should be a dict")

        # 检查必选字段
        required_fields = ["video_url", "width", "height", "start", "end", "duration"]
        missing_fields = [field for field in required_fields if field not in item]

        if missing_fields:
            raise CustomException(CustomError.INVALID_VIDEO_INFO, f"the {i}th item is missing required fields: {', '.join(missing_fields)}")

        # 创建处理后的对象，设置默认值
        processed_item = {
            "video_url": item["video_url"],
            "width": item["width"],
            "height": item["height"],
            "start": item["start"],
            "end": item["end"],
            "duration": item["duration"],
            "mask": item.get("mask", None),  # 默认值 None
            "mask_config": item.get("mask_config", {}),  # 遮罩配置
            "transition": item.get("transition", None),  # 默认值 None
            "transition_duration": item.get("transition_duration", 500000),  # 默认值 500000
            "volume": item.get("volume", 1.0),  # 默认值 1.0
            "filter": item.get("filter", None),  # 滤镜类型
            "filter_intensity": item.get("filter_intensity", 100.0),  # 滤镜强度
            "in_animation": item.get("in_animation", None),  # 入场动画
            "out_animation": item.get("out_animation", None),  # 出场动画
            "group_animation": item.get("group_animation", None),  # 组合动画
            "animation_duration": item.get("animation_duration", None),  # 动画时长
            "background_fill_type": item.get("background_fill_type", None),  # 背景填充类型
            "background_blur": item.get("background_blur", 0.0625),  # 背景模糊
            "background_color": item.get("background_color", "#00000000")  # 背景颜色
        }

        # 验证数值范围
        if processed_item["volume"] < 0 or processed_item["volume"] > 1:
            # 音量值必须在[0, 1]范围内，给默认值
            processed_item["volume"] = 1.0

        if processed_item["transition_duration"] < 0:
            # 转场持续时间必须为非负数，给默认值
            processed_item["transition_duration"] = 500000

        result.append(processed_item)

    return result
