import json
import os
from typing import Optional
from urllib.parse import urlparse
import asyncio

from src.utils.logger import logger
from src.pyJianYingDraft import ScriptFile, TrackType, trange, TextSegment, TextStyle, ClipSettings
import src.pyJianYingDraft as draft
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
from src.utils import helper
import config
from src.utils.draft_lock_manager import DraftLockManager


def easy_create_material(
    draft_url: str,
    audio_url: str,
    text: Optional[str] = None,
    img_url: Optional[str] = None,
    video_url: Optional[str] = None,
    text_color: str = "#ffffff",
    font_size: int = 15,
    text_transform_y: int = 0
) -> str:
    """
    在现有草稿中添加多种类型的素材内容，包括音频、视频、图片和文字
    
    Args:
        draft_url: 目标草稿的完整URL，必选参数
        audio_url: 音频文件URL，必选参数，不能为空或"null"
        text: 要添加的文字内容，可选参数，默认为None
        img_url: 图片文件URL，可选参数，默认为None
        video_url: 视频文件URL，可选参数，默认为None
        text_color: 文字颜色（十六进制格式），默认值："#ffffff"
        font_size: 字体大小，默认值：15
        text_transform_y: 文字Y轴位置偏移，默认值：0
    
    Returns:
        draft_url: 草稿URL
    
    Raises:
        CustomException: 素材创建失败
    """
    logger.info(f"easy_create_material started, draft_url: {draft_url}, audio_url: {audio_url}")
    logger.info(f"Materials to add - text: {text is not None}, img_url: {img_url is not None}, video_url: {video_url is not None}")

    # 1. 提取草稿ID并验证
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        logger.error(f"Invalid draft_url or draft not found in cache: {draft_url}")
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    # 2. 验证音频URL（必选参数）
    if not audio_url or audio_url.lower() == "null" or audio_url.strip() == "":
        logger.error("Audio URL is required and cannot be empty or null")
        raise CustomException(CustomError.MATERIAL_CREATE_FAILED)

    # 3. 从缓存中获取草稿
    script: ScriptFile = DRAFT_CACHE[draft_id]
    logger.info(f"Retrieved script from cache, draft_id: {draft_id}")

    try:
        # 4. 添加音频（必须的）
        audio_added = add_audio_material(script, draft_id, audio_url)
        logger.info(f"Audio material added: {audio_added}")

        # 5. 添加视频（如果提供）
        if video_url and video_url.strip() and video_url.lower() != "null":
            video_added = add_video_material(script, draft_id, video_url)
            logger.info(f"Video material added: {video_added}")

        # 6. 添加图片（如果提供）
        if img_url and img_url.strip() and img_url.lower() != "null":
            image_added = add_image_material(script, draft_id, img_url)
            logger.info(f"Image material added: {image_added}")

        # 7. 添加文字（如果提供）
        if text and text.strip():
            text_added = add_text_material(script, text, text_color, font_size, text_transform_y)
            logger.info(f"Text material added: {text_added}")

        # 8. 保存草稿
        script.save()
        logger.info(f"Draft saved successfully")

        logger.info(f"easy_create_material completed successfully - draft_id: {draft_id}")
        return draft_url
        
    except Exception as e:
        logger.error(f"Failed to create materials: {str(e)}")
        raise CustomException(CustomError.MATERIAL_CREATE_FAILED)


async def easy_create_material_async(
    draft_url: str,
    audio_url: str,
    text: Optional[str] = None,
    img_url: Optional[str] = None,
    video_url: Optional[str] = None,
    text_color: str = "#ffffff",
    font_size: int = 15,
    text_transform_y: int = 0,
    lock_timeout: float = 30.0
) -> str:
    """
    在现有草稿中添加多种类型的素材内容的异步版本（带并发锁保护）
    
    功能：
    1. 使用 DraftLockManager 防止同一草稿的并发写操作
    2. 支持超时控制，避免无限等待
    3. 自动释放锁，即使发生异常
    
    Args:
        draft_url: 目标草稿的完整 URL，必选参数
        audio_url: 音频文件 URL，必选参数，不能为空或"null"
        text: 要添加的文字内容，可选参数，默认为 None
        img_url: 图片文件 URL，可选参数，默认为 None
        video_url: 视频文件 URL，可选参数，默认为 None
        text_color: 文字颜色（十六进制格式），默认值："#ffffff"
        font_size: 字体大小，默认值：15
        text_transform_y: 文字 Y 轴位置偏移，默认值：0
        lock_timeout: 获取锁的超时时间（秒），默认 30 秒
    
    Returns:
        draft_url: 草稿 URL
    
    Raises:
        CustomException: 素材创建失败或获取锁超时
        asyncio.TimeoutError: 等待锁超时时抛出
    
    Example:
        >>> result = await easy_create_material_async(
        ...     draft_url="http://.../draft_id=123",
        ...     audio_url="https://.../audio.mp3",
        ...     text="Hello"
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
        return easy_create_material(
            draft_url=draft_url,
            audio_url=audio_url,
            text=text,
            img_url=img_url,
            video_url=video_url,
            text_color=text_color,
            font_size=font_size,
            text_transform_y=text_transform_y
        )
    finally:
        # 释放锁
        await lock_manager.release_lock(draft_id)
        logger.info(f"Lock released for draft_id: {draft_id}")


def add_video_material(script: ScriptFile, draft_id: str, video_url: str) -> bool:
    """
    添加视频素材到草稿（固定5秒时长）
    
    与add_videos接口保持一致的处理方式：
    1. 创建规范的视频资源目录
    2. 使用parse_video_data解析视频信息
    3. 调用add_video_to_draft添加视频
    
    Args:
        script: 草稿文件对象
        draft_id: 草稿ID
        video_url: 视频文件URL
    
    Returns:
        是否成功添加
    """
    try:
        logger.info(f"Adding video material: {video_url}")
        
        # 1. 创建视频资源目录（与add_videos保持一致）
        draft_dir = os.path.join(config.DRAFT_DIR, draft_id)
        draft_video_dir = os.path.join(draft_dir, "assets", "videos")
        os.makedirs(name=draft_video_dir, exist_ok=True)
        logger.info(f"Created video directory: {draft_video_dir}")
        
        # 2. 构造视频信息JSON（固定5秒时长）
        video_infos = json.dumps([{
            "video_url": video_url,
            "width": 1920,
            "height": 1080,
            "start": 0,
            "end": 5000000,  # 5秒（5 * 1000000微秒）
            "duration": 5000000,
            "volume": 1.0
        }])
        
        # 3. 解析视频信息
        from src.service.add_videos import parse_video_data, add_video_to_draft
        video_items = parse_video_data(video_infos)
        if not video_items:
            logger.error("No video items parsed")
            return False
        
        # 4. 添加视频轨道
        track_name = f"video_track_{helper.gen_unique_id()}"
        script.add_track(track_type=TrackType.video, track_name=track_name, relative_index=10)
        logger.info(f"Added video track: {track_name}")
        
        # 5. 添加视频到轨道（传递正确的视频资源目录）
        add_video_to_draft(script, track_name, draft_video_dir, video_items[0])
        
        return True
    except Exception as e:
        logger.error(f"Failed to add video material: {str(e)}")
        return False


def add_image_material(script: ScriptFile, draft_id: str, img_url: str) -> bool:
    """
    添加图片素材到草稿
    
    与add_images接口保持一致的处理方式：
    1. 创建规范的图片资源目录
    2. 使用parse_image_data解析图片信息
    3. 调用add_image_to_draft添加图片
    
    Args:
        script: 草稿文件对象
        draft_id: 草稿ID
        img_url: 图片文件URL
    
    Returns:
        是否成功添加
    """
    try:
        logger.info(f"Adding image material: {img_url}")
        
        # 1. 创建图片资源目录（与add_images保持一致）
        draft_dir = os.path.join(config.DRAFT_DIR, draft_id)
        draft_image_dir = os.path.join(draft_dir, "assets", "images")
        os.makedirs(name=draft_image_dir, exist_ok=True)
        logger.info(f"Created image directory: {draft_image_dir}")
        
        # 2. 构造图片信息JSON（默认尺寸和3秒显示时长）
        image_infos = json.dumps([{
            "image_url": img_url,
            "width": 1024,
            "height": 1024,
            "start": 0,
            "end": 3000000,  # 3秒（3 * 1000000微秒）
        }])
        
        # 3. 解析图片信息
        from src.service.add_images import parse_image_data, add_image_to_draft
        image_items = parse_image_data(image_infos)
        if not image_items:
            logger.error("No image items parsed")
            return False
        
        # 4. 添加图片轨道
        track_name = f"image_track_{helper.gen_unique_id()}"
        script.add_track(track_type=TrackType.video, track_name=track_name, relative_index=10)
        logger.info(f"Added image track: {track_name}")
        
        # 5. 添加图片到轨道（传递正确的图片资源目录）
        add_image_to_draft(script, track_name, draft_image_dir, image_items[0])
        
        return True
    except Exception as e:
        logger.error(f"Failed to add image material: {str(e)}")
        return False


def add_audio_material(script: ScriptFile, draft_id: str, audio_url: str) -> bool:
    """
    添加音频素材到草稿（固定5秒时长）
    
    与add_audios接口保持一致的处理方式：
    1. 创建规范的音频资源目录
    2. 使用parse_audio_data解析音频信息
    3. 调用add_audio_to_draft添加音频
    
    Args:
        script: 草稿文件对象
        draft_id: 草稿ID
        audio_url: 音频文件URL
    
    Returns:
        是否成功添加
    """
    try:
        logger.info(f"Adding audio material: {audio_url}")
        
        # 1. 创建音频资源目录（与add_audios保持一致）
        draft_dir = os.path.join(config.DRAFT_DIR, draft_id)
        draft_audio_dir = os.path.join(draft_dir, "assets", "audios")
        os.makedirs(name=draft_audio_dir, exist_ok=True)
        logger.info(f"Created audio directory: {draft_audio_dir}")
        
        # 2. 构造音频信息JSON（固定5秒时长）
        audio_infos = json.dumps([{
            "audio_url": audio_url,
            "start": 0,
            "end": 5000000,  # 5秒（5 * 1000000微秒）
            "volume": 1.0
        }])
        
        # 3. 解析音频信息
        from src.service.add_audios import parse_audio_data, add_audio_to_draft
        audio_items = parse_audio_data(audio_infos)
        if not audio_items:
            logger.error("No audio items parsed")
            return False
        
        # 4. 添加音频轨道
        track_name = f"audio_track_{helper.gen_unique_id()}"
        script.add_track(track_type=TrackType.audio, track_name=track_name, relative_index=10)
        logger.info(f"Added audio track: {track_name}")
        
        # 5. 添加音频到轨道（传递正确的音频资源目录）
        add_audio_to_draft(script, track_name, draft_audio_dir, audio_items[0])
        
        return True
    except Exception as e:
        logger.error(f"Failed to add audio material: {str(e)}")
        return False


def add_text_material(
    script: ScriptFile, 
    text: str, 
    text_color: str = "#ffffff", 
    font_size: int = 15, 
    text_transform_y: int = 0
) -> bool:
    """
    添加文字素材到草稿
    
    Args:
        script: 草稿文件对象
        text: 文字内容
        text_color: 文字颜色
        font_size: 字体大小
        text_transform_y: Y轴位置偏移
    
    Returns:
        是否成功添加
    """
    try:
        logger.info(f"Adding text material: {text[:20]}...")
        
        # 创建文字轨道
        track_name = f"text_track_{helper.gen_unique_id()}"
        script.add_track(track_type=TrackType.text, track_name=track_name)
        
        # 创建图像调节设置
        # 获取草稿的高用于transform坐标转换
        draft_height = script.height
        logger.info(f"draft height: {draft_height}, text_transform_y: {text_transform_y}")
        
        clip_settings = ClipSettings(
            transform_y=text_transform_y / draft_height  # 转换为半画布高单位
        )
        
        # 创建文本样式
        rgb_color = hex_to_rgb(text_color)
        text_style = TextStyle(
            align=1,  # 1为居中对齐
            color=(rgb_color[0], rgb_color[1], rgb_color[2]),
            size=font_size
        )
        
        # 创建文本片段（默认5秒显示时长）
        text_segment = TextSegment(
            text=text,
            timerange=trange(start=0, duration=5000000),  # 5秒
            style=text_style,
            clip_settings=clip_settings
        )
        
        # 向轨道添加文本片段
        script.add_segment(text_segment, track_name)
        
        logger.info(f"Text segment created and added, text: {text}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to add text material: {str(e)}")
        return False


def hex_to_rgb(hex_color: str) -> list:
    """
    将十六进制颜色转换为RGB数组
    
    Args:
        hex_color: 十六进制颜色，如 "#ffffff"
    
    Returns:
        RGB数组，值范围为0-1
    """
    # 移除 # 前缀
    hex_color = hex_color.lstrip('#')
    
    # 确保是6位十六进制
    if len(hex_color) != 6:
        logger.warning(f"Invalid hex color: {hex_color}, using default white")
        hex_color = "ffffff"  # 默认白色
    
    try:
        # 转换为RGB
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        
        return [r, g, b]
    except ValueError:
        logger.warning(f"Failed to parse hex color: {hex_color}, using default white")
        return [1.0, 1.0, 1.0]  # 默认白色


def validate_url(url: str) -> bool:
    """
    验证URL格式是否正确
    
    Args:
        url: 待验证的URL
    
    Returns:
        URL是否有效
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False