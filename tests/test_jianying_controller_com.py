"""JianyingController 对 UI Automation COM 瞬时错误的容错。"""
import sys
from unittest.mock import MagicMock, PropertyMock, patch

# jianying_controller 在导入时会加载 Windows 专用依赖，测试环境用 mock 占位
sys.modules.setdefault("uiautomation", MagicMock())
sys.modules.setdefault("pyautogui", MagicMock())

import _ctypes
import pytest

from src.pyJianYingDraft.jianying_controller import (
    COM_UIA_ERROR_HRESULT,
    COM_UIA_ERROR_MARKER,
    JianyingController,
    is_com_uia_error,
)


class TestIsComUiaError:
    def test_recognizes_com_error_by_hresult(self) -> None:
        exc = _ctypes.COMError(COM_UIA_ERROR_HRESULT, COM_UIA_ERROR_MARKER, None)
        assert is_com_uia_error(exc) is True

    def test_recognizes_com_error_by_message_string(self) -> None:
        exc = Exception(
            f"({COM_UIA_ERROR_HRESULT}, '{COM_UIA_ERROR_MARKER}', (None, None, None, 0, None))"
        )
        assert is_com_uia_error(exc) is True

    def test_ignores_unrelated_errors(self) -> None:
        assert is_com_uia_error(Exception("导出超时")) is False


class TestJianyingWindowCmp:
    def test_returns_false_when_class_name_com_error(self) -> None:
        ctrl = JianyingController.__new__(JianyingController)
        control = MagicMock()
        type(control).Name = PropertyMock(return_value="剪映专业版")
        type(control).ClassName = PropertyMock(
            side_effect=_ctypes.COMError(
                COM_UIA_ERROR_HRESULT, COM_UIA_ERROR_MARKER, None
            )
        )

        assert ctrl._JianyingController__jianying_window_cmp(control, 1) is False

    def test_returns_false_when_name_com_error(self) -> None:
        ctrl = JianyingController.__new__(JianyingController)
        control = MagicMock()
        type(control).Name = PropertyMock(
            side_effect=_ctypes.COMError(
                COM_UIA_ERROR_HRESULT, COM_UIA_ERROR_MARKER, None
            )
        )

        assert ctrl._JianyingController__jianying_window_cmp(control, 1) is False

    def test_matches_home_page_window(self) -> None:
        ctrl = JianyingController.__new__(JianyingController)
        control = MagicMock()
        type(control).Name = PropertyMock(return_value="剪映专业版")
        type(control).ClassName = PropertyMock(return_value="HomePageWindow")

        assert ctrl._JianyingController__jianying_window_cmp(control, 1) is True
        assert ctrl.app_status == "home"


class TestExistsWithComRetry:
    def test_retries_then_succeeds(self) -> None:
        ctrl = JianyingController.__new__(JianyingController)
        control = MagicMock()
        control.Exists.side_effect = [
            _ctypes.COMError(COM_UIA_ERROR_HRESULT, COM_UIA_ERROR_MARKER, None),
            True,
        ]

        with patch(
            "src.pyJianYingDraft.jianying_controller.time.sleep"
        ) as m_sleep:
            assert (
                ctrl._exists_with_com_retry(control, "test", timeout=0) is True
            )

        assert control.Exists.call_count == 2
        m_sleep.assert_called_once()

    def test_returns_false_when_raise_on_exhausted_false(self) -> None:
        ctrl = JianyingController.__new__(JianyingController)
        control = MagicMock()
        control.Exists.side_effect = _ctypes.COMError(
            COM_UIA_ERROR_HRESULT, COM_UIA_ERROR_MARKER, None
        )

        with patch("src.pyJianYingDraft.jianying_controller.time.sleep"):
            assert (
                ctrl._exists_with_com_retry(
                    control,
                    "test",
                    timeout=0,
                    max_retries=2,
                    raise_on_exhausted=False,
                )
                is False
            )

        assert control.Exists.call_count == 2
