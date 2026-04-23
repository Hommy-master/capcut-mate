import json
from unittest.mock import MagicMock, patch

import pytest

from src.service.add_audios import add_audio_to_draft
from src.service.add_images import add_image_to_draft
from src.service.add_videos import add_video_to_draft
from src.pyJianYingDraft.local_materials import VideoMaterial, AudioMaterial
from src.schemas.add_images import AddImagesRequest
from src.schemas.add_videos import AddVideosRequest
from src.schemas.add_audios import AddAudiosRequest
from src.schemas.easy_create_material import EasyCreateMaterialRequest


@pytest.fixture
def draft_ctx():
    script = MagicMock()
    script.width = 1920
    script.height = 1080
    return {
        "draft_id": "draft-test-001",
        "draft_url": "http://localhost/v1/get_draft?draft_id=draft-test-001",
        "script": script,
    }


def test_add_image_to_draft_uses_url_for_material_path(draft_ctx):
    """图片写入草稿时，素材对象中的 path 应为原始 URL。"""
    segment = MagicMock()
    segment.segment_id = "seg-image-1"
    segment.material_instance.material_id = "img-mat-1"
    with patch("src.service.add_images.draft.VideoSegment", return_value=segment) as mock_segment:
        add_image_to_draft(
            script=draft_ctx["script"],
            track_name="image_track_1",
            image={
                "image_url": "https://assets.jcaigc.cn/demo1.png",
                "width": 1024,
                "height": 1024,
                "start": 0,
                "end": 1_000_000,
            },
        )
    material = mock_segment.call_args.kwargs["material"]
    assert material.path == "https://assets.jcaigc.cn/demo1.png"
    assert material.material_type == "photo"


def test_add_video_to_draft_uses_url_for_material_path(draft_ctx):
    """视频写入草稿时，VideoMaterial 入参应为用户原始 URL。"""
    video_material = MagicMock(duration=2_000_000)
    segment = MagicMock(segment_id="seg-video-1")
    with patch("src.service.add_videos.draft.VideoMaterial", return_value=video_material) as mock_material, \
            patch("src.service.add_videos.draft.VideoSegment", return_value=segment):
        add_video_to_draft(
            script=draft_ctx["script"],
            track_name="video_track_1",
            video={
                "video_url": "https://assets.jcaigc.cn/demo1.mp4",
                "start": 0,
                "end": 1_000_000,
                "duration": 1_000_000,
                "volume": 1.0,
            },
        )
    assert mock_material.call_args.args[0] == "https://assets.jcaigc.cn/demo1.mp4"


def test_add_audio_to_draft_uses_url_for_material_path(draft_ctx):
    """音频写入草稿时，素材对象中的 path 应为原始 URL。"""
    segment = MagicMock()
    segment.material_instance.material_id = "audio-mat-1"
    with patch("src.service.add_audios.get_audio_actual_duration", return_value=1_000_000), \
            patch("src.service.add_audios.draft.AudioSegment", return_value=segment) as mock_segment:
        add_audio_to_draft(
            script=draft_ctx["script"],
            track_name="audio_track_1",
            audio={
                "audio_url": "https://assets.jcaigc.cn/demo1.mp3",
                "start": 0,
                "end": 1_000_000,
                "volume": 1.0,
            },
        )
    material = mock_segment.call_args.kwargs["material"]
    assert material.path == "https://assets.jcaigc.cn/demo1.mp3"


def test_video_material_supports_remote_url_metadata():
    """底层 VideoMaterial 应支持 URL + 元数据直写。"""
    material = VideoMaterial(
        "https://assets.jcaigc.cn/demo1.mp4",
        duration=3_000_000,
        width=1280,
        height=720,
        material_type="video",
    )
    assert material.path == "https://assets.jcaigc.cn/demo1.mp4"
    assert material.duration == 3_000_000
    assert material.width == 1280
    assert material.height == 720
    assert material.material_type == "video"


def test_audio_material_supports_remote_url_duration():
    """底层 AudioMaterial 应支持 URL + duration 直写。"""
    material = AudioMaterial("https://assets.jcaigc.cn/demo1.mp3", duration=2_500_000)
    assert material.path == "https://assets.jcaigc.cn/demo1.mp3"
    assert material.duration == 2_500_000


def test_schema_rejects_non_http_image_url():
    """图片 URL 非 http/https 时，应在 schema 阶段失败。"""
    with pytest.raises(Exception):
        AddImagesRequest(
            draft_url="http://localhost/v1/get_draft?draft_id=draft-1",
            image_infos=json.dumps([{
                "image_url": "file:///tmp/demo1.png",
                "width": 100,
                "height": 100,
                "start": 0,
                "end": 1000,
            }]),
        )


def test_schema_rejects_non_http_video_url():
    """视频 URL 非 http/https 时，应在 schema 阶段失败。"""
    with pytest.raises(Exception):
        AddVideosRequest(
            draft_url="http://localhost/v1/get_draft?draft_id=draft-1",
            video_infos=json.dumps([{
                "video_url": "C:/temp/demo1.mp4",
                "start": 0,
                "end": 1000,
            }]),
        )


def test_schema_rejects_non_http_audio_url():
    """音频 URL 非 http/https 时，应在 schema 阶段失败。"""
    with pytest.raises(Exception):
        AddAudiosRequest(
            draft_url="http://localhost/v1/get_draft?draft_id=draft-1",
            audio_infos=json.dumps([{
                "audio_url": "ftp://example.com/demo1.mp3",
                "start": 0,
                "end": 1000,
            }]),
        )


def test_easy_create_material_schema_rejects_non_http_audio_url():
    """easy_create_material 的 audio_url 应在 schema 阶段校验。"""
    with pytest.raises(Exception):
        EasyCreateMaterialRequest(
            draft_url="http://localhost/v1/get_draft?draft_id=draft-1",
            audio_url="file:///tmp/demo1.mp3",
        )


def test_easy_create_material_schema_rejects_non_http_optional_media_url():
    """easy_create_material 的 img_url/video_url 如有值必须为 http/https。"""
    with pytest.raises(Exception):
        EasyCreateMaterialRequest(
            draft_url="http://localhost/v1/get_draft?draft_id=draft-1",
            audio_url="https://assets.jcaigc.cn/test1.mp3",
            img_url="ftp://example.com/demo1.png",
        )
