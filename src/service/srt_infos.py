from src.utils.logger import logger
from src.utils.download import download, cleanup_temp_file
from src.utils.srt import parse_srt
from src.service.caption_infos import caption_infos
from exceptions import CustomException, CustomError
import config
from typing import List, Optional


def _read_srt_file(file_path: str) -> str:
    """读取 SRT 文件内容，兼容常见编码。

    SRT 文件常见编码为 UTF-8（含 BOM）、GBK 等，依次尝试解码。

    Args:
        file_path: 本地 SRT 文件路径

    Returns:
        str: 文件文本内容

    Raises:
        CustomException: 所有编码均无法解码时抛出
    """
    with open(file_path, "rb") as f:
        raw = f.read()

    for encoding in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue

    logger.error(f"Failed to decode SRT file with all candidate encodings: {file_path}")
    raise CustomException(CustomError.INVALID_CAPTION_INFO, detail="Unable to decode SRT file content")


def srt_infos(
    srt_url: str,
    font_size: Optional[int] = None,
    keyword_color: Optional[str] = None,
    keyword_border_color: Optional[str] = None,
    keyword_font_size: Optional[int] = None,
    keywords: Optional[List[str]] = None,
    in_animation: Optional[str] = None,
    in_animation_duration: Optional[int] = None,
    loop_animation: Optional[str] = None,
    loop_animation_duration: Optional[int] = None,
    out_animation: Optional[str] = None,
    out_animation_duration: Optional[int] = None,
    transition: Optional[str] = None,
    transition_duration: Optional[int] = None,
) -> tuple[str, int]:
    """下载并解析 SRT 文件，生成字幕信息 JSON 字符串。

    解析出的文本与时间线复用 caption_infos 生成最终 JSON，保证与
    add_captions 的入参格式完全一致。

    Args:
        srt_url: SRT 文件 URL
        font_size: 字体大小（可选）
        keyword_color: 关键词颜色（可选）
        keyword_border_color: 关键词边框颜色（可选）
        keyword_font_size: 关键词字体大小（可选）
        keywords: 重点词列表（可选）
        in_animation: 入场动画名称（可选）
        in_animation_duration: 入场动画时长（可选）
        loop_animation: 组合动画名称（可选）
        loop_animation_duration: 循环动画单次循环时长（可选）
        out_animation: 出场动画名称（可选）
        out_animation_duration: 出场动画时长（可选）
        transition: 转场名称（可选）
        transition_duration: 转场时长（可选）

    Returns:
        tuple[str, int]: (字幕信息 JSON 字符串, 字幕条目数量)

    Raises:
        CustomException: 下载失败或 SRT 内容无效时抛出
    """
    logger.info(f"srt_infos called with srt_url: {srt_url}")

    temp_file_path = None
    try:
        # 1. 下载 SRT 文件到临时目录
        temp_file_path = download(srt_url, config.TEMP_DIR)

        # 2. 读取并解析 SRT 内容
        srt_content = _read_srt_file(temp_file_path)
        try:
            entries = parse_srt(srt_content)
        except ValueError as e:
            logger.error(f"Invalid SRT content: {e}")
            raise CustomException(CustomError.INVALID_CAPTION_INFO, detail=str(e))

        # 3. 拆分为文本列表和时间线列表
        texts = [entry["text"] for entry in entries]
        timelines = [{"start": entry["start"], "end": entry["end"]} for entry in entries]

        # 4. 复用 caption_infos 生成字幕信息 JSON，保证格式统一
        infos_json = caption_infos(
            texts=texts,
            timelines=timelines,
            font_size=font_size,
            keyword_color=keyword_color,
            keyword_border_color=keyword_border_color,
            keyword_font_size=keyword_font_size,
            keywords=keywords,
            in_animation=in_animation,
            in_animation_duration=in_animation_duration,
            loop_animation=loop_animation,
            loop_animation_duration=loop_animation_duration,
            out_animation=out_animation,
            out_animation_duration=out_animation_duration,
            transition=transition,
            transition_duration=transition_duration,
        )

        logger.info(f"srt_infos generated {len(entries)} caption items")
        return infos_json, len(entries)

    except CustomException:
        # CustomException 直接重新抛出，保持原有的错误信息
        raise
    except Exception as e:
        logger.error(f"srt_infos failed with unexpected error: {str(e)}")
        raise CustomException(CustomError.INVALID_CAPTION_INFO, detail=f"Unexpected error: {str(e)}")
    finally:
        # 清理临时文件
        cleanup_temp_file(temp_file_path)
