"""各素材接口 parse 函数对 start/end 小数时间的兼容性测试。"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from exceptions import CustomException, CustomError
from src.schemas.add_captions import AddCaptionsResponse, SegmentInfo as CaptionSegmentInfo
from src.schemas.add_images import AddImagesResponse, SegmentInfo as ImageSegmentInfo
from src.schemas.add_videos import AddVideosResponse, SegmentInfo as VideoSegmentInfo
from src.service.add_audios import parse_audio_data
from src.service.add_captions import parse_captions_data
from src.service.add_filters import parse_filters_data
from src.service.add_images import parse_image_data
from src.service.add_videos import parse_video_data


def _sample_item(service: str, start, end) -> dict:
    if service == "captions":
        return {"start": start, "end": end, "text": "测试字幕"}
    if service == "filters":
        return {"filter_title": "复古", "start": start, "end": end, "intensity": 80}
    if service == "images":
        return {"image_url": "https://example.com/image.jpg", "start": start, "end": end}
    if service == "audios":
        return {"audio_url": "https://example.com/audio.mp3", "start": start, "end": end}
    if service == "videos":
        return {"video_url": "https://example.com/video.mp4", "start": start, "end": end}
    raise ValueError(f"unknown service: {service}")


PARSERS = {
    "captions": (parse_captions_data, CustomError.INVALID_CAPTION_INFO),
    "filters": (parse_filters_data, CustomError.INVALID_FILTER_INFO),
    "images": (parse_image_data, CustomError.INVALID_IMAGE_INFO),
    "audios": (parse_audio_data, CustomError.INVALID_AUDIO_INFO),
    "videos": (parse_video_data, CustomError.INVALID_VIDEO_INFO),
}


@pytest.mark.parametrize("service", PARSERS.keys())
def test_integer_start_end_unchanged(service):
    """回归：整数 start/end 行为与改动前一致。"""
    parse_fn, _ = PARSERS[service]
    item = _sample_item(service, 0, 5_000_000)
    result = parse_fn(json.dumps([item]))

    assert len(result) == 1
    assert result[0]["start"] == 0
    assert result[0]["end"] == 5_000_000
    assert isinstance(result[0]["start"], int)
    assert isinstance(result[0]["end"], int)


@pytest.mark.parametrize("service", PARSERS.keys())
def test_float_start_end_converted_to_int(service):
    """小数 start/end 应截断为整数并正常解析。"""
    parse_fn, _ = PARSERS[service]
    item = _sample_item(service, 0.5, 5_000_000.9)
    result = parse_fn(json.dumps([item]))

    assert result[0]["start"] == 0
    assert result[0]["end"] == 5_000_000


@pytest.mark.parametrize("service", PARSERS.keys())
def test_invalid_range_after_int_truncation(service):
    """转换后 end <= start 应报错。"""
    parse_fn, error = PARSERS[service]
    item = _sample_item(service, 1000.1, 1000.9)

    with pytest.raises(CustomException) as exc_info:
        parse_fn(json.dumps([item]))

    assert exc_info.value.err == error


@pytest.mark.parametrize("service", PARSERS.keys())
def test_negative_start_raises(service):
    parse_fn, error = PARSERS[service]
    item = _sample_item(service, -1, 5_000_000)

    with pytest.raises(CustomException) as exc_info:
        parse_fn(json.dumps([item]))

    assert exc_info.value.err == error


@pytest.mark.parametrize("service", PARSERS.keys())
def test_end_lte_start_raises(service):
    parse_fn, error = PARSERS[service]
    item = _sample_item(service, 5_000_000, 5_000_000)

    with pytest.raises(CustomException) as exc_info:
        parse_fn(json.dumps([item]))

    assert exc_info.value.err == error


def test_captions_multiple_items_with_optional_fields():
    """回归：多字幕及可选字段解析不受影响。"""
    items = [
        {
            "start": 0,
            "end": 3_000_000,
            "text": "第一句",
            "keyword": "第一",
            "keyword_font_size": 20,
        },
        {
            "start": 3_000_000.2,
            "end": 6_000_000.8,
            "text": "第二句",
        },
    ]
    result = parse_captions_data(json.dumps(items))

    assert len(result) == 2
    assert result[0]["keyword_font_size"] == 20
    assert result[1]["start"] == 3_000_000
    assert result[1]["end"] == 6_000_000


def test_filters_intensity_preserved():
    """回归：滤镜强度等字段在 time 转换后仍保留。"""
    result = parse_filters_data(json.dumps([
        {"filter_title": "复古", "start": 0.1, "end": 2_000_000.9, "intensity": 60.5},
    ]))

    assert result[0]["start"] == 0
    assert result[0]["end"] == 2_000_000
    assert result[0]["intensity"] == 60.5


def test_images_optional_dimensions_preserved():
    """回归：图片 width/height 可选字段不受影响。"""
    result = parse_image_data(json.dumps([
        {
            "image_url": "https://example.com/a.png",
            "width": 1920,
            "height": 1080,
            "start": 0.5,
            "end": 1_000_000.5,
            "transition_duration": 500000,
        },
    ]))

    assert result[0]["width"] == 1920
    assert result[0]["height"] == 1080
    assert result[0]["start"] == 0
    assert result[0]["end"] == 1_000_000


def test_audios_volume_default_preserved():
    """回归：音频 volume 默认值逻辑不受影响。"""
    result = parse_audio_data(json.dumps([
        {"audio_url": "https://example.com/a.mp3", "start": 0, "end": 5_000_000},
    ]))

    assert result[0]["volume"] == 1.0
    assert result[0]["start"] == 0
    assert result[0]["end"] == 5_000_000


def test_videos_duration_regression():
    """回归：video duration 显式传入 / 默认 end-start 逻辑不变。"""
    videos = parse_video_data(json.dumps([
        {
            "video_url": "https://example.com/v1.mp4",
            "start": 0,
            "end": 3_000_000,
            "duration": 6_000_000,
        },
        {
            "video_url": "https://example.com/v2.mp4",
            "start": 3_000_000,
            "end": 5_000_000,
        },
    ]))

    assert videos[0]["duration"] == 6_000_000
    assert videos[0]["end"] - videos[0]["start"] == 3_000_000
    assert videos[1]["duration"] == 2_000_000


def test_videos_float_duration_converted():
    result = parse_video_data(json.dumps([
        {
            "video_url": "https://example.com/v.mp4",
            "start": 0.5,
            "end": 3_000_000.9,
            "duration": 6_000_000.7,
        },
    ]))

    assert result[0]["start"] == 0
    assert result[0]["end"] == 3_000_000
    assert result[0]["duration"] == 6_000_000


@pytest.mark.parametrize(
    "response_builder",
    [
        lambda start, end: AddCaptionsResponse(
            draft_url="x",
            track_id="t",
            text_ids=[],
            segment_ids=[],
            segment_infos=[CaptionSegmentInfo(id="1", start=start, end=end)],
        ),
        lambda start, end: AddImagesResponse(
            draft_url="x",
            track_id="t",
            image_ids=[],
            segment_ids=[],
            segment_infos=[ImageSegmentInfo(id="1", start=start, end=end)],
        ),
        lambda start, end: AddVideosResponse(
            draft_url="x",
            track_id="t",
            video_ids=[],
            segment_ids=[],
            segment_infos=[VideoSegmentInfo(id="1", start=start, end=end)],
        ),
    ],
    ids=["captions", "images", "videos"],
)
def test_parsed_times_pass_response_validation(response_builder):
    """回归：解析后的整数时间可通过 Pydantic 响应模型校验。"""
    response = response_builder(0, 5_000_000)
    assert response.segment_infos[0].start == 0
    assert response.segment_infos[0].end == 5_000_000
