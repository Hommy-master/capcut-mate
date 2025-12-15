from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile, trange
import src.pyJianYingDraft as draft
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
from src.schemas.add_images import SegmentInfo
import os
from src.utils import helper
from src.utils.download import download
import config
import json
from typing import List, Dict, Any, Tuple


def add_images(
    draft_url: str, 
    image_infos: str,
    alpha: float = 1.0, 
    scale_x: float = 1.0, 
    scale_y: float = 1.0, 
    transform_x: int = 0, 
    transform_y: int = 0
) -> Tuple[str, str, List[str], List[str], List[SegmentInfo]]:
    """
    添加图片到剪映草稿的业务逻辑
    
    Args:
        draft_url: 草稿URL，必选参数
        image_infos: 图片信息JSON字符串，格式如下：
        [
            {
                "image_url": "https://s.coze.cn/t/XpufYwc2_u4/", // [必选] 图片文件URL
                "width": 1024, // [必选] 图片宽度(像素)
                "height": 1024, // [必选] 图片高度(像素)
                "start": 0, // [必选] 显示开始时间(微秒)
                "end": 1000000, // [必选] 显示结束时间(微秒)
                "in_animation": "", // [可选] 入场动画类型
                "out_animation": "", // [可选] 出场动画类型
                "loop_animation": "", // [可选] 循环动画类型
                "in_animation_duration": "", // [可选] 入场动画时长(微秒)
                "out_animation_duration": "", // [可选] 出场动画时长(微秒)
                "loop_animation_duration": "", // [可选] 循环动画时长(微秒)
                "transition": "", // [可选] 转场效果类型
                "transition_duration": 500000 // [可选] 转场效果时长(微秒，范围100000-2500000)
            }
        ]
        alpha: 全局透明度[0, 1]，默认值为1.0
        scale_x: X轴缩放比例，默认值为1.0
        scale_y: Y轴缩放比例，默认值为1.0
        transform_x: X轴位置偏移(像素)，默认值为0
        transform_y: Y轴位置偏移(像素)，默认值为0
    
    Returns:
        draft_url: 草稿URL
        track_id: 图片轨道ID（非主轨道）
        image_ids: 图片ID列表
        segment_ids: 片段ID列表
        segment_infos: 片段信息列表，包含每个片段的ID、开始时间和结束时间

    Raises:
        CustomException: 图片批量添加失败
    """
    logger.info(f"add_images started, draft_url: {draft_url}, alpha: {alpha}, scale_x: {scale_x}, scale_y: {scale_y}, transform_x: {transform_x}, transform_y: {transform_y}")

    # 1. 提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        logger.error(f"Invalid draft URL or draft not found in cache, draft_id: {draft_id}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    # 2. 创建保存图片资源的目录
    draft_dir = os.path.join(config.DRAFT_DIR, draft_id)
    draft_image_dir = os.path.join(draft_dir, "assets", "images")
    os.makedirs(name=draft_image_dir, exist_ok=True)
    logger.info(f"Created image directory: {draft_image_dir}")

    # 3. 解析图片信息
    images = parse_image_data(json_str=image_infos)
    if len(images) == 0:
        logger.error(f"No image info provided, draft_id: {draft_id}")
        raise CustomException(CustomError.INVALID_IMAGE_INFO)
    logger.info(f"Parsed {len(images)} image items")

    # 4. 从缓存中获取草稿
    script: ScriptFile = DRAFT_CACHE[draft_id]

    # 5. 添加图片轨道（明确说明不使用主轨道，并设置合适的渲染层级）
    track_name = f"image_track_{helper.gen_unique_id()}"
    # 设置 relative_index=10 确保图片轨道在主视频轨道之上，避免与主轨道冲突
    script.add_track(track_type=draft.TrackType.video, track_name=track_name, relative_index=10)
    logger.info(f"Added image track (non-main track): {track_name}")

    # 6. 遍历图片信息，添加图片到草稿中的指定轨道，收集片段ID和信息
    segment_ids = []
    segment_infos = []
    for i, image in enumerate(images):
        try:
            segment_id, segment_info = add_image_to_draft(
                script, track_name, 
                draft_image_dir=draft_image_dir, 
                image=image,
                alpha=alpha,
                scale_x=scale_x,
                scale_y=scale_y,
                transform_x=transform_x,
                transform_y=transform_y
            )
            segment_ids.append(segment_id)
            segment_infos.append(segment_info)
            logger.info(f"Added image {i+1}/{len(images)}, segment_id: {segment_id}")
        except Exception as e:
            logger.error(f"Failed to add image {i+1}/{len(images)}, error: {str(e)}")
            raise

    # 7. 保存草稿
    script.save()
    logger.info(f"Draft saved successfully")

    # 8. 获取当前图片轨道ID
    track_id = ""
    for key in script.tracks.keys():
        if script.tracks[key].name == track_name:
            track_id = script.tracks[key].track_id
            break
    logger.info(f"Image track created, draft_id: {draft_id}, track_id: {track_id}")

    # 9. 获取当前所有图片资源ID（明确说明这些是图片资源，不与主轨道冲突）
    image_ids = [video.material_id for video in script.materials.videos if video.material_type == "photo"]
    logger.info(f"Image track completed, draft_id: {draft_id}, image_ids: {image_ids}")

    return draft_url, track_id, image_ids, segment_ids, segment_infos


def add_image_to_draft(
    script: ScriptFile,
    track_name: str,
    draft_image_dir: str,
    image: dict,
    alpha: float = 1.0, 
    scale_x: float = 1.0, 
    scale_y: float = 1.0, 
    transform_x: int = 0, 
    transform_y: int = 0
) -> Tuple[str, SegmentInfo]:
    """
    向剪映草稿中添加单个图片
    
    Args:
        script: 草稿文件对象
        track_name: 视频轨道名称
        draft_image_dir: 图片资源目录
        image: 图片信息字典，包含以下字段：
            image_url: 图片URL
            width: 图片宽度(像素)
            height: 图片高度(像素)
            start: 显示开始时间(微秒)
            end: 显示结束时间(微秒)
            in_animation: 入场动画类型(可选)
            out_animation: 出场动画类型(可选)
            loop_animation: 循环动画类型(可选)
            in_animation_duration: 入场动画时长(微秒，可选)
            out_animation_duration: 出场动画时长(微秒，可选)
            loop_animation_duration: 循环动画时长(微秒，可选)
            transition: 转场效果类型(可选)
            transition_duration: 转场效果时长(微秒，可选)
        alpha: 图片透明度
        scale_x: 横向缩放
        scale_y: 纵向缩放
        transform_x: X轴位置偏移(像素)
        transform_y: Y轴位置偏移(像素)
    
    Returns:
        segment_id: 片段ID
        segment_info: 片段信息字典，包含id、start、end
    
    Raises:
        CustomException: 添加图片失败
    """
    try:
        # 1. 下载图片文件
        image_path = download(url=image['image_url'], save_dir=draft_image_dir)
        logger.info(f"Downloaded image from {image['image_url']} to {image_path}")

        # 2. 创建图片素材并添加到草稿
        segment_duration = image['end'] - image['start']
        
        # 创建图像调节设置
        clip_settings = draft.ClipSettings(
            alpha=alpha,
            scale_x=scale_x,
            scale_y=scale_y,
            transform_x=transform_x / image['width'],  # 转换为半画布宽单位
            transform_y=transform_y / image['height']  # 转换为半画布高单位
        )
        
        # 创建视频片段（图片使用VideoSegment）
        video_segment = draft.VideoSegment(
            material=image_path,
            target_timerange=trange(start=image['start'], duration=segment_duration),
            clip_settings=clip_settings
        )
        
        # 3. 添加动画效果（如果指定了）
        # 注意：由于动画相关的枚举类型较复杂，这里先预留接口
        if image.get('in_animation'):
            try:
                logger.info(f"In animation '{image['in_animation']}' specified but not implemented yet")
                # 这里可以根据需要添加具体的入场动画
                # 例如：video_segment.add_animation(IntroType.XXX, duration=image.get('in_animation_duration'))
            except Exception as e:
                logger.warning(f"Failed to add in animation '{image['in_animation']}': {str(e)}")
        
        if image.get('out_animation'):
            try:
                logger.info(f"Out animation '{image['out_animation']}' specified but not implemented yet")
                # 这里可以根据需要添加具体的出场动画
                # 例如：video_segment.add_animation(OutroType.XXX, duration=image.get('out_animation_duration'))
            except Exception as e:
                logger.warning(f"Failed to add out animation '{image['out_animation']}': {str(e)}")
        
        if image.get('loop_animation'):
            try:
                logger.info(f"Loop animation '{image['loop_animation']}' specified but not implemented yet")
                # 循环动画可能需要特殊处理
            except Exception as e:
                logger.warning(f"Failed to add loop animation '{image['loop_animation']}': {str(e)}")
        
        # 4. 添加转场效果（如果指定了）
        if image.get('transition'):
            try:
                logger.info(f"Transition '{image['transition']}' specified but not implemented yet")
                # 例如：video_segment.add_transition(TransitionType.XXX, duration=image.get('transition_duration'))
            except Exception as e:
                logger.warning(f"Failed to add transition '{image['transition']}': {str(e)}")

        logger.info(f"Created image segment, material_id: {video_segment.material_instance.material_id}")
        logger.info(f"Image segment details - start: {image['start']}, duration: {segment_duration}, size: {image['width']}x{image['height']}")

        # 5. 向指定轨道添加片段
        script.add_segment(video_segment, track_name)

        # 6. 构造片段信息
        segment_info = SegmentInfo(
            id=video_segment.segment_id,
            start=image['start'],
            end=image['end']
        )

        return video_segment.segment_id, segment_info
        
    except CustomException:
        logger.error(f"Add image to draft failed, draft_image_dir: {draft_image_dir}, image: {image}")
        raise
    except Exception as e:
        logger.error(f"Add image to draft failed, error: {str(e)}")
        raise CustomException(err=CustomError.IMAGE_ADD_FAILED)


def parse_image_data(json_str: str) -> List[Dict[str, Any]]:
    """
    解析图片数据的JSON字符串，处理可选字段的默认值
    
    Args:
        json_str: 包含图片数据的JSON字符串，格式如下：
        [
            {
                "image_url": "https://s.coze.cn/t/XpufYwc2_u4/", // [必选] 图片文件URL
                "width": 1024, // [必选] 图片宽度(像素)
                "height": 1024, // [必选] 图片高度(像素)
                "start": 0, // [必选] 显示开始时间(微秒)
                "end": 1000000, // [必选] 显示结束时间(微秒)
                "in_animation": "", // [可选] 入场动画类型
                "out_animation": "", // [可选] 出场动画类型
                "loop_animation": "", // [可选] 循环动画类型
                "in_animation_duration": "", // [可选] 入场动画时长(微秒)
                "out_animation_duration": "", // [可选] 出场动画时长(微秒)
                "loop_animation_duration": "", // [可选] 循环动画时长(微秒)
                "transition": "", // [可选] 转场效果类型
                "transition_duration": 500000 // [可选] 转场效果时长(微秒，范围100000-2500000)
            }
        ]
        
    Returns:
        包含图片对象的数组，每个对象都处理了默认值
        
    Raises:
        CustomException: 当JSON格式错误或缺少必选字段时抛出
    """
    try:
        # 解析JSON字符串
        data = json.loads(json_str)
        logger.info(f"Successfully parsed JSON with {len(data) if isinstance(data, list) else 1} items")
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e.msg}")
        raise CustomException(CustomError.INVALID_IMAGE_INFO, f"JSON parse error: {e.msg}")
    
    # 确保输入是列表
    if not isinstance(data, list):
        logger.error("Image infos should be a list")
        raise CustomException(CustomError.INVALID_IMAGE_INFO, "image_infos should be a list")
    
    result = []
    
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            logger.error(f"The {i}th item should be a dict")
            raise CustomException(CustomError.INVALID_IMAGE_INFO, f"the {i}th item should be a dict")
        
        # 检查必选字段
        required_fields = ["image_url", "width", "height", "start", "end"]
        missing_fields = [field for field in required_fields if field not in item]
        
        if missing_fields:
            logger.error(f"The {i}th item is missing required fields: {', '.join(missing_fields)}")
            raise CustomException(CustomError.INVALID_IMAGE_INFO, f"the {i}th item is missing required fields: {', '.join(missing_fields)}")
        
        # 创建处理后的对象，设置默认值
        processed_item = {
            "image_url": item["image_url"],
            "width": item["width"],
            "height": item["height"],
            "start": item["start"],
            "end": item["end"],
            "in_animation": item.get("in_animation", None),  # 默认无入场动画
            "out_animation": item.get("out_animation", None),  # 默认无出场动画
            "loop_animation": item.get("loop_animation", None),  # 默认无循环动画
            "in_animation_duration": item.get("in_animation_duration", None),  # 默认无入场动画时长
            "out_animation_duration": item.get("out_animation_duration", None),  # 默认无出场动画时长
            "loop_animation_duration": item.get("loop_animation_duration", None),  # 默认无循环动画时长
            "transition": item.get("transition", None),  # 默认无转场
            "transition_duration": item.get("transition_duration", 500000)  # 默认转场时长500000微秒
        }
        
        # 验证数值范围
        if processed_item["width"] <= 0 or processed_item["height"] <= 0:
            logger.error(f"Invalid image dimensions: width={processed_item['width']}, height={processed_item['height']}")
            raise CustomException(CustomError.INVALID_IMAGE_INFO, f"the {i}th item has invalid image dimensions")
        
        if processed_item["start"] < 0 or processed_item["end"] <= processed_item["start"]:
            logger.error(f"Invalid time range: start={processed_item['start']}, end={processed_item['end']}")
            raise CustomException(CustomError.INVALID_IMAGE_INFO, f"the {i}th item has invalid time range")
        
        # 验证转场时长范围
        if processed_item["transition_duration"] < 100000 or processed_item["transition_duration"] > 2500000:
            logger.warning(f"Transition duration {processed_item['transition_duration']} out of range [100000, 2500000], using default 500000")
            processed_item["transition_duration"] = 500000
        
        result.append(processed_item)
        logger.debug(f"Processed image item {i+1}: {processed_item}")
    
    return result