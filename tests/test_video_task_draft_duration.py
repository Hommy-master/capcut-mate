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


_API_KEY = "11111111-1111-1111-1111-111111111111"


def _task_with_key(draft_id: str) -> VideoGenTask:
    task = _task(draft_id)
    task.api_key = _API_KEY
    return task


def _write_draft(draft_home: str, draft_id: str, duration_us: int) -> None:
    root = os.path.join(draft_home, draft_id)
    os.makedirs(root, exist_ok=True)
    with open(os.path.join(root, "draft_content.json"), "w", encoding="utf-8") as f:
        json.dump({"duration": duration_us}, f)


class TestExportBalanceAdmission:
    """导出前按草稿时长预估费用：余额不足时不再白用一次导出。"""

    def test_insufficient_balance_returns_message(self, draft_home) -> None:
        did = "balance_low"
        _write_draft(draft_home, did, 10 * 1_000_000)  # 10 秒 × 0.005 = 0.05 元

        with (
            patch("src.utils.video_task_manager.config") as cfg,
            patch("src.utils.points.get_user_points", return_value=0.01),
        ):
            cfg.DRAFT_SAVE_PATH = draft_home
            cfg.ENABLE_APIKEY = True
            message = VideoGenTaskManager()._ensure_export_balance(_task_with_key(did))

        assert "充值余额不足" in message
        assert "0.05" in message
        assert "https://jcaigc.cn/recharge" in message

    def test_enough_balance_allows_export(self, draft_home) -> None:
        did = "balance_ok"
        _write_draft(draft_home, did, 10 * 1_000_000)

        with (
            patch("src.utils.video_task_manager.config") as cfg,
            patch("src.utils.points.get_user_points", return_value=100.0),
        ):
            cfg.DRAFT_SAVE_PATH = draft_home
            cfg.ENABLE_APIKEY = True
            message = VideoGenTaskManager()._ensure_export_balance(_task_with_key(did))

        assert message == ""

    def test_balance_query_failure_does_not_block_export(self, draft_home) -> None:
        did = "balance_down"
        _write_draft(draft_home, did, 10 * 1_000_000)

        with (
            patch("src.utils.video_task_manager.config") as cfg,
            patch(
                "src.utils.points.get_user_points",
                side_effect=RuntimeError("points api down"),
            ),
        ):
            cfg.DRAFT_SAVE_PATH = draft_home
            cfg.ENABLE_APIKEY = True
            message = VideoGenTaskManager()._ensure_export_balance(_task_with_key(did))

        assert message == ""

    @patch("src.utils.video_task_manager.sys.platform", "win32")
    @patch.object(VideoGenTaskManager, "_ensure_local_draft_ready", return_value="")
    @patch.object(VideoGenTaskManager, "_download_draft", return_value="")
    def test_phase_returns_insufficient_balance_message(
        self, m_dl, m_ready, draft_home
    ) -> None:
        did = "phase_balance"
        _write_draft(draft_home, did, 10 * 1_000_000)

        with (
            patch("src.utils.video_task_manager.config") as cfg,
            patch("src.utils.points.get_user_points", return_value=0.01),
        ):
            cfg.DRAFT_SAVE_PATH = draft_home
            cfg.DRAFT_DIR = draft_home
            cfg.ENABLE_APIKEY = True
            out = VideoGenTaskManager()._phase_download_and_prepare(_task_with_key(did))

        assert out.startswith("充值余额不足")


class TestPhaseDownloadPrepareMessage:
    """时长不通过时，阶段函数返回带 draft_id 的提示文案。"""

    @patch("src.utils.video_task_manager.sys.platform", "win32")
    @patch.object(VideoGenTaskManager, "_ensure_local_draft_ready", return_value="")
    @patch.object(VideoGenTaskManager, "_download_draft", return_value="")
    def test_phase_returns_duration_too_short_message(
        self, m_dl, m_ready, draft_home
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
