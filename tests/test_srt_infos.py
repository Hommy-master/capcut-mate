"""SRT 解析与 srt_infos 服务测试"""
import json
import pytest

from src.utils.srt import parse_srt


SAMPLE_SRT = """1
00:00:00,000 --> 00:00:02,000
你好，世界

2
00:00:02,500 --> 00:00:05,000
这是第二行字幕
跨两行的文本

3
00:00:05,000 --> 00:00:08,200
最后一句
"""


def test_parse_srt_basic():
    entries = parse_srt(SAMPLE_SRT)
    assert len(entries) == 3

    # 第 1 条：0 ~ 2,000,000 微秒
    assert entries[0]["start"] == 0
    assert entries[0]["end"] == 2_000_000
    assert entries[0]["text"] == "你好，世界"

    # 第 2 条：多行文本合并，2,500,000 ~ 5,000,000 微秒
    assert entries[1]["start"] == 2_500_000
    assert entries[1]["end"] == 5_000_000
    assert entries[1]["text"] == "这是第二行字幕\n跨两行的文本"

    # 第 3 条
    assert entries[2]["start"] == 5_000_000
    assert entries[2]["end"] == 8_200_000


def test_parse_srt_with_bom_and_crlf():
    """带 BOM + Windows 换行符 + 点号毫秒分隔符"""
    content = "﻿1\r\n00:00:01.000 --> 00:00:03.500\r\nhello\r\n"
    entries = parse_srt(content)
    assert len(entries) == 1
    assert entries[0]["start"] == 1_000_000
    assert entries[0]["end"] == 3_500_000
    assert entries[0]["text"] == "hello"


def test_parse_srt_sorts_by_start():
    """乱序条目应按开始时间升序排列"""
    content = (
        "1\n00:00:05,000 --> 00:00:06,000\nsecond\n\n"
        "2\n00:00:01,000 --> 00:00:02,000\nfirst\n"
    )
    entries = parse_srt(content)
    assert [e["text"] for e in entries] == ["first", "second"]


def test_parse_srt_empty_raises():
    with pytest.raises(ValueError):
        parse_srt("这不是一个合法的 SRT 文件，没有任何时间轴")


def test_parse_srt_skips_empty_text_block():
    """有时间轴但无文本的块应被跳过"""
    content = (
        "1\n00:00:01,000 --> 00:00:02,000\n\n\n"
        "2\n00:00:03,000 --> 00:00:04,000\nvalid\n"
    )
    entries = parse_srt(content)
    assert len(entries) == 1
    assert entries[0]["text"] == "valid"
