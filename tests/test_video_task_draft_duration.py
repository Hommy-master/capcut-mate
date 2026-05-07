"""云渲染草稿时长校验：低于 3 秒视为空草稿。"""
import json
import os
import tempfile
from datetime import datetime
from unittest.mock import patch

import pytest

from src.utils.video_task_manager import (
    MIN_DRAFT_EXPORT_DURATION_US,
    TaskStatus,
    VideoGenTask,
    VideoGenTaskManager,
)


def _task(draft_id: str = "d_test") -> VideoGenTask:
    return VideoGenTask(
        draft_url=f"http://example/openapi?draft_id={draft_id}",
        draft_id=draft_id,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
    )


@pytest.fixture
def draft_home():
    with tempfile.TemporaryDirectory() as td:
        yield td


class TestCheckDraftDuration:
    def test_below_three_seconds_returns_false(self, draft_home) -> None:
        did = "below_three"
        root = os.path.join(draft_home, did)
        os.makedirs(root, exist_ok=True)
        path = os.path.join(root, "draft_content.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"duration": MIN_DRAFT_EXPORT_DURATION_US - 1}, f)

        with patch("src.utils.video_task_manager.config") as cfg:
            cfg.DRAFT_SAVE_PATH = draft_home
            assert VideoGenTaskManager()._check_draft_duration(_task(did)) is False

    def test_exactly_three_seconds_returns_true(self, draft_home) -> None:
        did = "exact_three"
        root = os.path.join(draft_home, did)
        os.makedirs(root, exist_ok=True)
        path = os.path.join(root, "draft_content.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"duration": MIN_DRAFT_EXPORT_DURATION_US}, f)

        with patch("src.utils.video_task_manager.config") as cfg:
            cfg.DRAFT_SAVE_PATH = draft_home
            assert VideoGenTaskManager()._check_draft_duration(_task(did)) is True

    def test_zero_duration_returns_false(self, draft_home) -> None:
        did = "zero_d"
        root = os.path.join(draft_home, did)
        os.makedirs(root, exist_ok=True)
        path = os.path.join(root, "draft_content.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"duration": 0}, f)

        with patch("src.utils.video_task_manager.config") as cfg:
            cfg.DRAFT_SAVE_PATH = draft_home
            assert VideoGenTaskManager()._check_draft_duration(_task(did)) is False


class TestPhaseDownloadPrepareMessage:
    """时长不通过时，阶段函数返回带 draft_id 的提示文案。"""

    @patch("src.utils.video_task_manager.sys.platform", "win32")
    @patch.object(VideoGenTaskManager, "_download_draft", return_value=True)
    def test_phase_returns_duration_too_short_message(
        self, m_dl, draft_home
    ) -> None:
        did = "phase_short"
        root = os.path.join(draft_home, did)
        os.makedirs(root, exist_ok=True)
        path = os.path.join(root, "draft_content.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"duration": 1000}, f)

        with patch("src.utils.video_task_manager.config") as cfg:
            cfg.DRAFT_SAVE_PATH = draft_home
            cfg.DRAFT_DIR = draft_home
            out = VideoGenTaskManager()._phase_download_and_prepare(_task(did))
            assert (
                out
                == f"草稿中视频时长不大于3秒，请检查草稿内容: {did}"
            )
