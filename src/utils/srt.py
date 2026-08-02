"""SRT 字幕文件解析工具

将标准 SRT 字幕文件解析为字幕条目列表，时间统一转换为微秒（μs），
方便与项目内 caption_infos / add_captions 等接口的时间单位保持一致。
"""
import re
from typing import List, Dict
from src.utils.logger import logger


# SRT 时间轴行正则：00:00:01,000 --> 00:00:04,074
# 毫秒分隔符兼容逗号(,)和点(.)，时分秒位数做一定容错
_TIMECODE_PATTERN = re.compile(
    r"(\d{1,2}):(\d{1,2}):(\d{1,2})[,.](\d{1,3})\s*-->\s*"
    r"(\d{1,2}):(\d{1,2}):(\d{1,2})[,.](\d{1,3})"
)


def _timecode_to_microseconds(hours: str, minutes: str, seconds: str, millis: str) -> int:
    """将 SRT 时间分量转换为微秒。

    Args:
        hours: 小时
        minutes: 分钟
        seconds: 秒
        millis: 毫秒（可能不足 3 位，需右补零）

    Returns:
        int: 对应的微秒值
    """
    # 毫秒可能是 1~3 位（如 "5" 表示 500ms，"05" 表示 50ms），右补零到 3 位
    millis_padded = millis.ljust(3, "0")
    total_ms = (
        int(hours) * 3600 * 1000
        + int(minutes) * 60 * 1000
        + int(seconds) * 1000
        + int(millis_padded)
    )
    return total_ms * 1000


def parse_srt(content: str) -> List[Dict]:
    """解析 SRT 字幕文本为字幕条目列表。

    支持：
    - UTF-8 BOM、\\r\\n / \\n 换行
    - 毫秒分隔符为逗号或点
    - 单条字幕多行文本（合并为以 \\n 连接的一段文本）
    - 缺失序号行的非标准 SRT

    Args:
        content: SRT 文件文本内容

    Returns:
        List[Dict]: 字幕条目列表，每项为 {"start": int, "end": int, "text": str}，
                    start/end 单位为微秒，按 start 升序排列

    Raises:
        ValueError: 未解析到任何有效字幕条目时抛出
    """
    # 去除 BOM，统一换行符
    text = content.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n")

    # 以空行切分为字幕块
    blocks = re.split(r"\n\s*\n", text)

    entries: List[Dict] = []
    for block in blocks:
        lines = [line for line in block.split("\n") if line.strip() != ""]
        if not lines:
            continue

        # 在块内定位时间轴行（标准 SRT 第一行为序号，第二行为时间轴；做容错处理）
        timecode_index = -1
        match = None
        for idx, line in enumerate(lines):
            m = _TIMECODE_PATTERN.search(line)
            if m:
                timecode_index = idx
                match = m
                break

        # 没有时间轴行的块直接跳过（可能是文件头注释等）
        if match is None:
            logger.warning(f"Skip SRT block without timecode: {lines[0][:50]}")
            continue

        start_us = _timecode_to_microseconds(match.group(1), match.group(2), match.group(3), match.group(4))
        end_us = _timecode_to_microseconds(match.group(5), match.group(6), match.group(7), match.group(8))

        # 时间轴行之后的内容为字幕文本，多行合并
        text_lines = lines[timecode_index + 1:]
        caption_text = "\n".join(text_lines).strip()

        # 文本为空的条目跳过
        if caption_text == "":
            continue

        entries.append({"start": start_us, "end": end_us, "text": caption_text})

    if not entries:
        raise ValueError("No valid subtitle entries parsed from SRT content")

    # 按开始时间升序排列，保证时间线有序
    entries.sort(key=lambda e: e["start"])

    logger.info(f"Parsed {len(entries)} subtitle entries from SRT content")
    return entries
