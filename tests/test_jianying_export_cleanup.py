"""剪映导出失败恢复逻辑单元测试。"""
from __future__ import annotations

import os
import tempfile
import time
import unittest
from unittest.mock import patch

from src.utils import jianying_export_cleanup as cleanup


class TestJianyingExportCleanup(unittest.TestCase):
    def _make_draft(self, base: str, draft_id: str) -> str:
        draft_dir = os.path.join(base, draft_id)
        os.makedirs(draft_dir, exist_ok=True)
        content_path = os.path.join(draft_dir, cleanup.DRAFT_CONTENT_FILE)
        with open(content_path, "w", encoding="utf-8") as f:
            f.write("{}")
        return draft_dir

    def test_removes_root_meta_info_unconditionally(self) -> None:
        with tempfile.TemporaryDirectory() as base:
            meta_path = os.path.join(base, cleanup.ROOT_META_INFO_FILE)
            with open(meta_path, "w", encoding="utf-8") as f:
                f.write("{}")

            with patch.object(cleanup.config, "DRAFT_SAVE_PATH", base):
                self.assertTrue(cleanup.clear_draft_save_directory())

            self.assertFalse(os.path.exists(meta_path))

    def test_removes_draft_when_draft_content_is_older_than_24h(self) -> None:
        with tempfile.TemporaryDirectory() as base:
            draft_dir = self._make_draft(base, "20250101120000abcdef01")
            old_ts = time.time() - cleanup.DRAFT_CONTENT_MIN_AGE_SECONDS - 60

            with (
                patch.object(cleanup.config, "DRAFT_SAVE_PATH", base),
                patch.object(cleanup.os.path, "getctime", return_value=old_ts),
            ):
                cleanup.clear_draft_save_directory()

            self.assertFalse(os.path.exists(draft_dir))

    def test_keeps_draft_when_draft_content_is_within_24h(self) -> None:
        with tempfile.TemporaryDirectory() as base:
            draft_dir = self._make_draft(base, "20250101120000abcdef01")
            recent_ts = time.time() - 3600

            with (
                patch.object(cleanup.config, "DRAFT_SAVE_PATH", base),
                patch.object(cleanup.os.path, "getctime", return_value=recent_ts),
            ):
                cleanup.clear_draft_save_directory()

            self.assertTrue(os.path.isdir(draft_dir))

    def test_skips_cleanup_when_draft_save_path_missing(self) -> None:
        missing = os.path.join(tempfile.gettempdir(), "capcut_nonexistent_draft_path")
        self.assertFalse(os.path.isdir(missing))

        with patch.object(cleanup.config, "DRAFT_SAVE_PATH", missing):
            self.assertFalse(cleanup.draft_save_path_exists())
            self.assertFalse(cleanup.clear_draft_save_directory())

    def test_skips_cleanup_when_draft_save_path_empty(self) -> None:
        with patch.object(cleanup.config, "DRAFT_SAVE_PATH", ""):
            self.assertFalse(cleanup.draft_save_path_exists())
            self.assertFalse(cleanup.clear_draft_save_directory())

    @patch("src.utils.jianying_export_cleanup.clear_draft_save_directory")
    @patch("src.utils.jianying_export_cleanup.kill_jianying_process")
    def test_recover_skips_clear_when_draft_path_missing(
        self, mock_kill, mock_clear
    ) -> None:
        missing = os.path.join(tempfile.gettempdir(), "capcut_nonexistent_draft_path")
        with patch.object(cleanup.config, "DRAFT_SAVE_PATH", missing):
            cleanup.recover_from_export_failure()

        mock_kill.assert_called_once()
        mock_clear.assert_not_called()

    def test_skips_draft_dir_without_draft_content(self) -> None:
        with tempfile.TemporaryDirectory() as base:
            draft_dir = os.path.join(base, "20250101120000abcdef01")
            os.makedirs(draft_dir)

            with patch.object(cleanup.config, "DRAFT_SAVE_PATH", base):
                cleanup.clear_draft_save_directory()

            self.assertTrue(os.path.isdir(draft_dir))

    @patch("src.utils.jianying_export_cleanup.subprocess.run")
    def test_kill_jianying_process_invokes_taskkill(self, mock_run) -> None:
        mock_run.return_value.returncode = 0
        cleanup.kill_jianying_process()
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertEqual(args[:3], ["taskkill", "/F", "/T"])
        self.assertEqual(args[4], "JianyingPro.exe")

    @patch("src.utils.jianying_export_cleanup.clear_draft_save_directory")
    @patch("src.utils.jianying_export_cleanup.kill_jianying_process")
    @patch("src.utils.jianying_export_cleanup.draft_save_path_exists", return_value=True)
    def test_recover_from_export_failure(self, _exists, mock_kill, mock_clear) -> None:
        cleanup.recover_from_export_failure()
        mock_kill.assert_called_once()
        mock_clear.assert_called_once()


if __name__ == "__main__":
    unittest.main()
