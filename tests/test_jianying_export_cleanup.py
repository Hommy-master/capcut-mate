"""剪映导出失败恢复逻辑单元测试。"""
from __future__ import annotations

import os
import tempfile
import unittest
from unittest.mock import patch

from src.utils import jianying_export_cleanup as cleanup


class TestJianyingExportCleanup(unittest.TestCase):
    def test_clear_draft_save_directory_removes_all_entries(self) -> None:
        with tempfile.TemporaryDirectory() as base:
            draft_a = os.path.join(base, "20250101120000abcdef01")
            os.makedirs(draft_a)
            with open(os.path.join(base, "root_meta_info.json"), "w", encoding="utf-8") as f:
                f.write("{}")

            with patch.object(cleanup.config, "DRAFT_SAVE_PATH", base):
                cleanup.clear_draft_save_directory()

            self.assertEqual(os.listdir(base), [])

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
    def test_recover_from_export_failure(self, mock_kill, mock_clear) -> None:
        cleanup.recover_from_export_failure()
        mock_kill.assert_called_once()
        mock_clear.assert_called_once()

if __name__ == "__main__":
    unittest.main()
