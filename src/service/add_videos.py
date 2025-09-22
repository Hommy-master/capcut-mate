from src.utils.logger import logger
from src.pyJianYingDraft import trange, IntroType, trange
import src.pyJianYingDraft as draft
from src.utils.draft_cache import DRAFT_CACHE
from exceptions import CustomException, CustomError
import os
from src.utils import helper
import config
import hashlib
import json


def add_video_to_draft(draft_id, video_path) -> str:
    """
    向剪映草稿中添加本地视频
    
    Args:
        draft_id: 草稿ID（草稿文件夹名称）
        video_path: 本地视频文件路径
    
    Returns:
        draft_url: 草稿URL
        message: 响应消息，如果成功就返回"添加视频成功"，失败就返回具体错误信息
    """

    try:
        # 1. 从缓存中获取草稿
        script = DRAFT_CACHE[draft_id]

        # 2. 添加视频轨道
        script.add_track(draft.TrackType.video)
        logger.info(f"2. add video track: {draft_id}")
        
        # 3. 创建视频素材并添加到草稿
        video_segment = draft.VideoSegment(video_path, trange("0s", "4.2s"))
        video_segment.add_animation(IntroType.斜切)               # 添加一个入场动画"斜切"
        logger.info(f"3. add video segment: {video_segment}")
        
        # 4. 添加视频片段到轨道
        script.add_segment(video_segment)
        
        logger.info(f"4. add video segment to track: {video_segment}")

        # 5. 保存草稿
        script.save()

        logger.info(f"5. save draft: {draft_id}")
        
        return f"视频 '{os.path.basename(video_path)}' 成功添加到草稿 '{draft_id}' 的轨道末尾"
    except Exception as e:
        logger.error(f"add video to draft failed, error: {str(e)}")
        return f"操作失败: {str(e)}"

def add_videos(
    draft_url: str, 
    video_infos: str,
    alpha: float = 1.0, 
    scale_x: float = 1.0, 
    scale_y: float = 1.0, 
    transform_x: int = 0, 
    transform_y: int = 0
) -> (str, str):
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
                "start": 0, // [必选] 视频在时间轴上的开始时间 
                "end": 12000000, // [必选] 视频在时间轴上的结束时间 
                "duration": 12000000, // [必选] 视频总时长(微秒)
                "mask": "", // 遮罩类型[可选]，默认值为None
                "transition": "", // 转场效果名称[可选]，默认值为None
                "transition_duration": 500000, // 转场持续时间(微秒)[可选]，默认值为500000
                "volume": 1.0, // 音量大小[0, 1][可选]，默认值为1.0
            } 
        ] // [必选]
        alpha: 全局透明度[0, 1][可选]，默认值为1.0
        scale_x: X轴缩放比例[可选]，默认值为1.0
        scale_y: Y轴缩放比例[可选]，默认值为1.0
        transform_x: X轴位置偏移(像素)[可选]，默认值为0
        transform_y: Y轴位置偏移(像素)[可选]，默认值为0
    
    Returns:
        "code": 0,
        "message": "视频批量添加成功",
        "draft_url": "https://ts.fyshark.com/#/cozeToJianyin?drafId=...",
        "track_id": "video-track-uuid",
        "video_ids": ["video1-uuid", "video2-uuid", "video3-uuid"],
        "segment_ids": ["segment1-uuid", "segment2-uuid", "segment3-uuid"],
        "videos_count": 3,
        "total_duration": 15000000

    Raises:
        CustomException: 视频批量添加失败
    """

    logger.debug(f"add_videos_service: {draft_url}, {video_infos}, {alpha}, {scale_x}, {scale_y}, {transform_x}, {transform_y}")

    # 提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if (not draft_id) or (draft_id not in DRAFT_CACHE):
        raise CustomException(CustomError.INVALID_DRAFT_URL)

    # 创建保存视频资源的目录
    draft_dir = os.path.join(config.DRAFT_DIR, draft_id)
    draft_video_dir = os.path.join(draft_dir, "assets", "videos")
    os.makedirs(draft_video_dir, exist_ok=True)

    # 根据视频URL生成视频的文件名
    video_url = "https://assets.jcaigc.cn/min.mp4"
    video_filename = hashlib.md5(video_url.encode('utf-8')).hexdigest()

    # 下载视频
    video_path = helper.download(video_url, draft_video_dir, video_filename)

    # 添加视频
    message = add_video_to_draft(draft_id, video_path)

    return draft_url, message

def parse_video_infos(video_infos_str: str) -> list:
    """
    解析包含视频信息的JSON字符串，验证必选字段并为可选字段提供默认值
    
    Args:
        video_infos_str: JSON字符串，json字符串的值为数组，示例如下：
        [ 
            {
                "video_url": "https://example.com/video1.mp4", // [必选] 视频文件的URL地址
                "width": 1920, // [必选] 视频宽度 
                "height": 1080, // [必选] 视频高度 
                "start": 0, // [必选] 视频在时间轴上的开始时间 
                "end": 12000000, // [必选] 视频在时间轴上的结束时间 
                "duration": 12000000, // [必选] 视频总时长(微秒)
                "mask": "", // 遮罩类型[可选]，默认值为None
                "transition": "", // 转场效果名称[可选]，默认值为None
                "transition_duration": 500000, // 转场持续时间(微秒)[可选]，默认值为500000
                "volume": 1.0, // 音量大小[0, 1][可选]，默认值为1.0
            } 
        ]
        
    Returns:
        list: 解析后的video_infos列表
        
    Raises:
        CustomException: 视频信息解析失败
    """
    try:
        # 解析JSON字符串
        video_infos = json.loads(video_infos_str)
    except json.JSONDecodeError as e:
        logger.info(f"parse video_infos_str failed, error: {e}")
        raise CustomException(CustomError.INVALID_VIDEO_INFO)
    
    # 检查video_infos是否为一个列表
    if not isinstance(video_infos, list):
        logger.info(f"video_infos is not list, video_infos_str: {video_infos_str}")
        raise CustomException(CustomError.INVALID_VIDEO_INFO)
    
    required_fields = ['video_url', 'width', 'height', 'start', 'end', 'duration']
    
    for i, video_info in enumerate(video_infos):
        if not isinstance(video_info, dict):
            logger.info(f"video_info is not dict, video_info: {video_info}")
            raise CustomException(CustomError.INVALID_VIDEO_INFO)
        
        # 检查必选字段
        for field in required_fields:
            if field not in video_info:
                logger.info(f"invalid video_info, missing field: {field}, i: {i}, video_info: {video_info}")
                raise CustomException(CustomError.INVALID_VIDEO_INFO)
        
        # 设置可选字段的默认值
        video_info.setdefault('mask', None)
        video_info.setdefault('transition', None)
        video_info.setdefault('transition_duration', 500000)
        video_info.setdefault('volume', 1.0)
        
        # 验证数值类型和范围
        if not isinstance(video_info['width'], (int, float)) or video_info['width'] <= 0:
            raise TypeError(f"视频信息 {i} 的width必须是正数")
        
        if not isinstance(video_info['height'], (int, float)) or video_info['height'] <= 0:
            raise TypeError(f"视频信息 {i} 的height必须是正数")
        
        if not isinstance(video_info['volume'], (int, float)) or not 0 <= video_info['volume'] <= 1:
            raise TypeError(f"视频信息 {i} 的volume必须在0到1之间")
    
    return video_infos

import json

def parse_video_infos(video_infos_str):
    """
    解析包含视频信息的JSON数组字符串，验证必选字段并为可选字段提供默认值
    
    Args:
        video_infos_str (str): 包含视频信息数组的JSON字符串
        
    Returns:
        list: 解析后的视频信息对象数组
        
    Raises:
        ValueError: 当JSON格式无效或缺少必选字段时
        KeyError: 当缺少必选字段时
        TypeError: 当字段类型不正确时
    """
    try:
        # 解析JSON字符串
        video_infos = json.loads(video_infos_str)
    except json.JSONDecodeError as e:
        raise ValueError("无效的JSON格式") from e
    
    if not isinstance(video_infos, list):
        raise TypeError("输入应该是视频信息数组")
    
    required_fields = ['video_url', 'width', 'height', 'start', 'end', 'duration']
    
    for i, video_info in enumerate(video_infos):
        if not isinstance(video_info, dict):
            raise TypeError(f"索引 {i} 处的元素应该是字典类型")
        
        # 检查必选字段
        for field in required_fields:
            if field not in video_info:
                raise KeyError(f"视频信息 {i} 中缺少必选字段: {field}")
        
        # 设置可选字段的默认值
        video_info.setdefault('mask', None)
        video_info.setdefault('transition', None)
        video_info.setdefault('transition_duration', 500000)
        video_info.setdefault('volume', 1.0)
        
        # 验证数值类型和范围
        if not isinstance(video_info['width'], (int, float)) or video_info['width'] <= 0:
            raise TypeError(f"视频信息 {i} 的width必须是正数")
        
        if not isinstance(video_info['height'], (int, float)) or video_info['height'] <= 0:
            raise TypeError(f"视频信息 {i} 的height必须是正数")
        
        if not isinstance(video_info['volume'], (int, float)) or not 0 <= video_info['volume'] <= 1:
            raise TypeError(f"视频信息 {i} 的volume必须在0到1之间")
    
    return video_infos

# 使用示例
if __name__ == "__main__":
    sample_json = """
    [
        {
            "video_url": "https://example.com/video1.mp4",
            "width": 1920,
            "height": 1080,
            "start": 0,
            "end": 12000000,
            "duration": 12000000,
            "mask": "circle",
            "transition": "fade",
            "transition_duration": 500000,
            "volume": 0.8
        }
    ]
    """
    
    try:
        result = parse_video_infos(sample_json)
        print("解析成功:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"解析错误: {e}")