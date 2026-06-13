# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Modified by Hommy <taohongmin@sina.cn> on 2026-06-12
"""剪映自动化控制，主要与自动导出有关"""

import ctypes
import os
import time
import shutil
import sys

# 平台检查和依赖导入
if sys.platform != "win32":
    raise ImportError("JianyingController is only available on Windows platform")

try:
    import uiautomation as uia
except ImportError as e:
    raise ImportError(f"Missing required Windows dependencies: {e}. Please install with: pip install capcut-mate[windows]")

try:
    import pyautogui  # pyright: ignore[reportMissingModuleSource]
except ImportError as e:
    raise ImportError(f"Missing required Windows dependencies: {e}. Please install with: pip install pyautogui[windows]")

from enum import Enum
from typing import Optional, Literal, Callable

from . import exceptions
from .exceptions import AutomationError

# 添加logger导入
from src.utils.logger import logger

# Windows UI Automation COM 错误（EVENT_E_ALL_SUBSCRIBERS_FAILED）
COM_UIA_ERROR_HRESULT = -2147220991
COM_UIA_ERROR_MARKER = "事件无法调用任何订户"
UIA_CLICK_MAX_RETRIES = 4
UIA_CLICK_RETRY_INTERVAL = 1.0


def is_com_uia_error(exc: BaseException) -> bool:
    if isinstance(exc, ctypes.COMError):
        args = getattr(exc, "args", ())
        if args and args[0] == COM_UIA_ERROR_HRESULT:
            return True
        if len(args) >= 2 and COM_UIA_ERROR_MARKER in str(args[1]):
            return True
    text = str(exc)
    return str(COM_UIA_ERROR_HRESULT) in text or COM_UIA_ERROR_MARKER in text


class ExportResolution(Enum):
    """导出分辨率"""
    RES_8K = "8K"
    RES_4K = "4K"
    RES_2K = "2K"
    RES_1080P = "1080P"
    RES_720P = "720P"
    RES_480P = "480P"

class ExportFramerate(Enum):
    """导出帧率"""
    FR_24 = "24fps"
    FR_25 = "25fps"
    FR_30 = "30fps"
    FR_50 = "50fps"
    FR_60 = "60fps"

class ControlFinder:
    """控件查找器，封装部分与控件查找相关的逻辑"""

    @staticmethod
    def desc_matcher(target_desc: str, depth: int = 2, exact: bool = False) -> Callable[[uia.Control, int], bool]:
        """根据full_description查找控件的匹配器"""
        target_desc = target_desc.lower()
        def matcher(control: uia.Control, _depth: int) -> bool:
            if _depth != depth:
                return False
            full_desc: str = control.GetPropertyValue(30159).lower()
            return (target_desc == full_desc) if exact else (target_desc in full_desc)
        return matcher

    @staticmethod
    def class_name_matcher(class_name: str, depth: int = 1, exact: bool = False) -> Callable[[uia.Control, int], bool]:
        """根据ClassName查找控件的匹配器"""
        class_name = class_name.lower()
        def matcher(control: uia.Control, _depth: int) -> bool:
            if _depth != depth:
                return False
            curr_class_name: str = control.ClassName.lower()
            return (class_name == curr_class_name) if exact else (class_name in curr_class_name)
        return matcher

class JianyingController:
    """剪映控制器"""

    # 窗口查找重试：剪映启动较慢、RDP 刚连上、或 UI 树尚未就绪时，瞬时 Exists(0) 易失败
    WINDOW_FIND_MAX_RETRIES = 12
    WINDOW_FIND_RETRY_INTERVAL = 1.0

    app: uia.WindowControl
    """剪映窗口"""
    app_status: Literal["home", "edit", "pre_export"]
    """当app_status为pre_export时，app_sub_status表示导出过程中的子状态"""
    app_sub_status: Literal["none", "export_start", "exporting", "export_succeed"]

    def __init__(self):
        """初始化剪映控制器, 此时剪映应该处于目录页"""
        self.get_window()

    def _safe_click(
        self,
        get_control: Callable[[], uia.Control],
        operation: str,
        *,
        exists_timeout: float = 1.0,
        max_retries: int = UIA_CLICK_MAX_RETRIES,
        retry_interval: float = UIA_CLICK_RETRY_INTERVAL,
    ) -> None:
        """带 COM 重试的控件点击；每次尝试重新查找控件，失效时刷新窗口。"""
        last_exc: Optional[BaseException] = None
        for attempt in range(1, max_retries + 1):
            try:
                control = get_control()
                if not control.Exists(exists_timeout, 0.5):
                    raise AutomationError(f"{operation}: control not found")
                control.Click(simulateMove=False)
                return
            except Exception as exc:
                last_exc = exc
                if not is_com_uia_error(exc) or attempt >= max_retries:
                    logger.error(
                        "UIA click failed: operation=%s attempt=%d/%d error=%r",
                        operation,
                        attempt,
                        max_retries,
                        exc,
                        exc_info=not is_com_uia_error(exc),
                    )
                    raise
                logger.warning(
                    "UIA COM error on click, retrying: operation=%s attempt=%d/%d",
                    operation,
                    attempt,
                    max_retries,
                )
                time.sleep(retry_interval)
                self.get_window()
        if last_exc is not None:
            raise last_exc

    def _find_export_succeed_close_btn(self) -> Optional[uia.Control]:
        """在当前窗口或「导出」子窗口中查找导出成功关闭按钮。"""
        btn = self.app.TextControl(
            searchDepth=3,
            Compare=ControlFinder.desc_matcher("ExportSucceedCloseBtn"),
        )
        if btn.Exists(0.5):
            return btn

        export_window = self.app.WindowControl(searchDepth=2, Name="导出")
        if export_window.Exists(0.5):
            btn = export_window.TextControl(
                searchDepth=2,
                Compare=ControlFinder.desc_matcher("ExportSucceedCloseBtn"),
            )
            if btn.Exists(0.5):
                return btn
        return None

    def _require_export_succeed_close_btn(self) -> uia.Control:
        btn = self._find_export_succeed_close_btn()
        if btn is None:
            raise AutomationError("export succeed close button not found")
        return btn

    def _dismiss_export_success_dialog(self) -> bool:
        """关闭导出成功弹窗；返回是否找到并点击了关闭按钮。"""
        if self._find_export_succeed_close_btn() is None:
            return False
        logger.info("Dismissing export success dialog")
        self._safe_click(
            self._require_export_succeed_close_btn,
            "dismiss_export_success_dialog",
        )
        time.sleep(2)
        self.get_window()
        return True

    def find_and_click_draft(
        self,
        draft_name: str,
        max_retries: int = 6,
        retry_interval: float = 5.0,
        draft_dir: Optional[str] = None,
    ) -> None:
        """查找并点击指定名称的草稿
        
        Args:
            draft_name (str): 要查找的草稿名称
            max_retries (int): 最大重试次数，默认6次
            retry_interval (float): 重试间隔时间(秒)，默认5秒
            draft_dir (str, optional): 剪映本地草稿目录；未找到时会触发 robocopy 扫描以刷新列表
            
        Raises:
            DraftNotFound: 未找到指定名称的剪映草稿
        """
        last_exception = None
        for attempt in range(max_retries):
            try:
                # 点击对应草稿
                draft_name_text = self.app.TextControl(
                    searchDepth=2,
                    Compare=ControlFinder.desc_matcher(f"HomePageDraftTitle:{draft_name}", exact=True)
                )
                if not draft_name_text.Exists(0):
                    raise exceptions.DraftNotFound(f"未找到名为{draft_name}的剪映草稿")
                draft_btn = draft_name_text.GetParentControl()
                assert draft_btn is not None
                draft_btn.Click(simulateMove=False)
                time.sleep(10)
                self.get_window()
                return  # 成功则返回
            except exceptions.DraftNotFound as e:
                last_exception = e
                if attempt < max_retries - 1:
                    logger.info(
                        "Draft not found (name=%s), retry %d/%d",
                        draft_name,
                        attempt + 1,
                        max_retries,
                    )
                    if draft_dir and os.path.isdir(draft_dir):
                        from src.utils.draft_downloader import trigger_directory_scan_with_robocopy
                        logger.info(
                            "Triggering robocopy directory scan before retry: %s",
                            draft_dir,
                        )
                        trigger_directory_scan_with_robocopy(draft_dir)
                    time.sleep(retry_interval)
        
        # 所有重试都失败，抛出异常
        raise last_exception

    def click_export_button(self) -> None:
        """点击编辑页面的导出按钮
        
        Raises:
            AutomationError: 未找到导出按钮
        """
        export_btn = self.app.TextControl(searchDepth=2, Compare=ControlFinder.desc_matcher("MainWindowTitleBarExportBtn"))
        if not export_btn.Exists(0):
            raise AutomationError("未在编辑窗口中找到导出按钮")
        export_btn.Click(simulateMove=False)
        time.sleep(10)
        self.get_window()

    def get_original_export_path(self) -> str:
        """获取原始导出路径
        
        Returns:
            str: 原始导出路径
            
        Raises:
            AutomationError: 未找到导出路径框
        """
        # 获取原始导出路径（带后缀名）
        export_path_sib = self.app.TextControl(searchDepth=2, Compare=ControlFinder.desc_matcher("ExportPath"))
        if not export_path_sib.Exists(0):
            raise AutomationError("未找到导出路径框")
        export_path_text = export_path_sib.GetSiblingControl(lambda ctrl: True)
        assert export_path_text is not None
        export_path = export_path_text.GetPropertyValue(30159)
        return export_path

    def set_export_resolution(self, resolution: Optional[ExportResolution]) -> None:
        """设置导出分辨率
        
        Args:
            resolution (Optional[ExportResolution]): 导出分辨率，如果为None则不设置
            
        Raises:
            AutomationError: 未找到相关控件
        """
        if resolution is not None:
            setting_group = self.app.GroupControl(searchDepth=1,
                                          Compare=ControlFinder.class_name_matcher("PanelSettingsGroup_QMLTYPE"))
            if not setting_group.Exists(0):
                raise AutomationError("未找到导出设置组")
            resolution_btn = setting_group.TextControl(searchDepth=2, Compare=ControlFinder.desc_matcher("ExportSharpnessInput"))
            if not resolution_btn.Exists(0.5):
                raise AutomationError("未找到导出分辨率下拉框")
            resolution_btn.Click(simulateMove=False)
            time.sleep(0.5)
            resolution_item = self.app.TextControl(
                searchDepth=2, Compare=ControlFinder.desc_matcher(resolution.value)
            )
            if not resolution_item.Exists(0.5):
                raise AutomationError(f"未找到{resolution.value}分辨率选项")
            resolution_item.Click(simulateMove=False)
            time.sleep(0.5)

    def set_export_framerate(self, framerate: Optional[ExportFramerate]) -> None:
        """设置导出帧率
        
        Args:
            framerate (Optional[ExportFramerate]): 导出帧率，如果为None则不设置
            
        Raises:
            AutomationError: 未找到相关控件
        """
        if framerate is not None:
            setting_group = self.app.GroupControl(searchDepth=1,
                                          Compare=ControlFinder.class_name_matcher("PanelSettingsGroup_QMLTYPE"))
            if not setting_group.Exists(0):
                raise AutomationError("未找到导出设置组")
            framerate_btn = setting_group.TextControl(searchDepth=2, Compare=ControlFinder.desc_matcher("FrameRateInput"))
            if not framerate_btn.Exists(0.5):
                raise AutomationError("未找到导出帧率下拉框")
            framerate_btn.Click(simulateMove=False)
            time.sleep(0.5)
            framerate_item = self.app.TextControl(
                searchDepth=2, Compare=ControlFinder.desc_matcher(framerate.value)
            )
            if not framerate_item.Exists(0.5):
                raise AutomationError(f"未找到{framerate.value}帧率选项")
            framerate_item.Click(simulateMove=False)
            time.sleep(0.5)

    def click_final_export_button(self) -> None:
        """点击导出窗口的最终导出按钮
        
        Raises:
            AutomationError: 未找到导出按钮
        """
        export_btn = self.app.TextControl(searchDepth=2, Compare=ControlFinder.desc_matcher("ExportOkBtn", exact=True))
        if not export_btn.Exists(0):
            raise AutomationError("未在导出窗口中找到导出按钮")
        export_btn.Click(simulateMove=False)
        time.sleep(5)

    def __ensure_window_focus(self) -> None:
        """在点击前确保窗口有焦点"""
        # 1. 确保窗口激活
        self.app.SetActive()
        time.sleep(1)
        
        # 2. 确保窗口置顶
        self.app.SetTopmost()
        time.sleep(1)
        
        # 3. 强制获取焦点
        try:
            self.app.SetFocus()
        except:
            pass  # 某些情况下可能失败，但继续执行
        time.sleep(1)

    def wait_for_export_completion(self, timeout: float) -> bool:
        """等待导出完成
        
        Args:
            timeout (float): 超时时间（秒）
            
        Returns:
            bool: 是否已关闭导出成功弹窗（表示导出已完成）
            
        Raises:
            AutomationError: 导出超时
        """
        # 点击继续导出按钮次数
        continue_export_click_count = 0
        export_succeeded = False

        # 等待导出完成
        st = time.time()
        while True:
            self.get_window()
            if self.app_status != "pre_export":
                break

            if self._find_export_succeed_close_btn() is not None:
                logger.info("Export finished, closing success dialog")
                self._safe_click(
                    self._require_export_succeed_close_btn,
                    "wait_for_export_completion.close_success",
                )
                time.sleep(2)
                export_succeeded = True
                break

            if time.time() - st > timeout:
                raise AutomationError("导出超时, 时限为%d秒" % timeout)

            # 导出过程中，如果出现异常弹窗，则点击继续导出按钮
            if continue_export_click_count < 20:
                print("pyautogui.size(): ", pyautogui.size(), ", click index: ", continue_export_click_count)
                pyautogui.click(x=996, y=597, button="left")
                continue_export_click_count += 1

            time.sleep(1)
        time.sleep(2)
        return export_succeeded

    def return_to_home(self) -> None:
        """回到目录页并稍作延迟"""
        self.get_window()
        self._dismiss_export_success_dialog()
        self.switch_to_home()
        time.sleep(2)

    def move_exported_file(self, original_path: str, output_path: Optional[str]) -> None:
        """移动导出的文件到指定位置
        
        Args:
            original_path (str): 原始导出路径
            output_path (Optional[str]): 目标输出路径，如果为None则不移动
        """
        logger.info(f"move {original_path} to {output_path}")
        if output_path is not None:
            shutil.move(original_path, output_path)

    def export_draft(self, draft_name: str, output_path: Optional[str] = None, *,
                     resolution: Optional[ExportResolution] = None,
                     framerate: Optional[ExportFramerate] = None,
                     timeout: float = 300,
                     draft_dir: Optional[str] = None) -> None:
        """导出指定的剪映草稿, **目前仅支持剪映6及以下版本**

        **注意: 需要确认有导出草稿的权限(不使用VIP功能或已开通VIP), 否则可能陷入死循环**

        Args:
            draft_name (`str`): 要导出的剪映草稿名称
            output_path (`str`, optional): 导出路径, 支持指向文件夹或直接指向文件, 不指定则使用剪映默认路径.
            resolution (`Export_resolution`, optional): 导出分辨率, 默认不改变剪映导出窗口中的设置.
            framerate (`Export_framerate`, optional): 导出帧率, 默认不改变剪映导出窗口中的设置.
            timeout (`float`, optional): 导出超时时间(秒), 默认为5分钟.
            draft_dir (`str`, optional): 剪映本地草稿目录；未在首页找到草稿时会 robocopy 触发扫描后重试.

        Raises:
            `DraftNotFound`: 未找到指定名称的剪映草稿
            `AutomationError`: 剪映操作失败
        """
        logger.info(f"start export {draft_name} to {output_path}")

        # 初始化准备
        self.get_window()
        self.switch_to_home()

        original_path = None
        export_completed = False

        for i in range(16):
            # 确保窗口有焦点
            self.__ensure_window_focus()
            if self.app_status == "home":
                logger.info("[%d]app is already in home page", i)
                self.find_and_click_draft(draft_name, draft_dir=draft_dir)
            elif self.app_status == "edit":
                if export_completed or (
                    original_path and os.path.isfile(original_path)
                ):
                    logger.info(
                        "[%d]export already finished, skip re-export and return home",
                        i,
                    )
                    self.return_to_home()
                    break
                logger.info("[%d]app is already in edit page", i)
                # 点击导出按钮进入导出界面
                self.click_export_button()
            elif self.app_status == "pre_export":                
                if self.app_sub_status == "export_start":
                    logger.info("[%d]app is already in pre_export[export_start] page", i)
                    # 获取原始导出路径
                    original_path = self.get_original_export_path()
                    # 设置分辨率（如果指定）
                    self.set_export_resolution(resolution)                    
                    # 设置帧率（如果指定）
                    self.set_export_framerate(framerate)                    
                    # 点击最终导出按钮
                    self.click_final_export_button()
                    # 获取窗口状态
                    self.get_window()
                elif self.app_sub_status == "exporting":
                    logger.info("[%d]app is already in pre_export[exporting] page", i)
                    if self.wait_for_export_completion(timeout):
                        export_completed = True
                        self.return_to_home()
                        break
                    self.get_window()
                    if original_path and os.path.isfile(original_path):
                        logger.info(
                            "[%d]export output file exists after wait, treating as success",
                            i,
                        )
                        export_completed = True
                        self.return_to_home()
                        break
                elif self.app_sub_status == "export_succeed":
                    logger.info("[%d]app is already in pre_export[export_succeed] page", i)
                    export_completed = True
                    self.return_to_home()
                    break
                else:
                    raise AutomationError("[%d]app is in unknown sub-status: %s" % (i, self.app_sub_status))
            else:
                raise AutomationError("[%d]app is in unknown status: %s" % (i, self.app_status))
        
        # 移动导出文件到指定路径（如果指定）
        self.move_exported_file(original_path, output_path)
        
        logger.info(f"export {draft_name} to {output_path} completed")

    def switch_to_home(self) -> None:
        """切换到剪映主页"""
        for i in range(8):
            self.get_window()
            if self.app_status == "home":
                return

            if self._dismiss_export_success_dialog():
                continue

            if self.app_status == "pre_export":
                # 导出弹窗未识别为 export_succeed 时，仍尝试关闭成功页或按 ESC 退出
                if self.app_sub_status in ("export_succeed", "exporting", "export_start"):
                    if self._find_export_succeed_close_btn() is not None:
                        self._safe_click(
                            self._require_export_succeed_close_btn,
                            f"switch_to_home.pre_export_close[{i}]",
                        )
                        time.sleep(2)
                        continue
                logger.warning(
                    "switch_to_home: stuck in pre_export sub_status=%s, attempt=%d",
                    self.app_sub_status,
                    i,
                )
                time.sleep(1)
                continue

            if self.app_status == "edit":
                close_btn = self.app.GroupControl(
                    searchDepth=1,
                    ClassName="TitleBarButton",
                    foundIndex=3,
                )
                if not close_btn.Exists(1, 0.5):
                    logger.warning(
                        "switch_to_home: edit close button missing, attempt=%d",
                        i,
                    )
                    time.sleep(1)
                    continue
                self._safe_click(
                    lambda: self.app.GroupControl(
                        searchDepth=1,
                        ClassName="TitleBarButton",
                        foundIndex=3,
                    ),
                    f"switch_to_home.edit_close[{i}]",
                )
                time.sleep(2)
                continue

            raise AutomationError("invalid app status: %s" % self.app_status)

        logger.warning("Cannot switch to home page after %d attempts", 8)

    def get_window(
        self,
        max_retries: Optional[int] = None,
        retry_interval: Optional[float] = None,
    ) -> None:
        """寻找剪映窗口并置顶；未找到时按间隔重试以提高容错。"""
        if max_retries is None:
            max_retries = self.WINDOW_FIND_MAX_RETRIES
        if retry_interval is None:
            retry_interval = self.WINDOW_FIND_RETRY_INTERVAL

        if hasattr(self, "app") and self.app.Exists(0):
            self.app.SetTopmost(False)

        for attempt in range(max_retries):
            self.app = uia.WindowControl(searchDepth=1, Compare=self.__jianying_window_cmp)
            if self.app.Exists(0):
                if attempt > 0:
                    logger.info(
                        "Jianying main window matched on attempt %d/%d",
                        attempt + 1,
                        max_retries,
                    )
                break
            if attempt < max_retries - 1:
                logger.warning(
                    "Jianying main window not found, retrying in %.1fs (%d/%d)",
                    retry_interval,
                    attempt + 1,
                    max_retries,
                )
                time.sleep(retry_interval)
        else:
            raise AutomationError(
                "Jianying window not found after %d attempts (%.1fs interval); "
                "ensure Jianying Pro is open on the home or edit screen."
                % (max_retries, retry_interval)
            )

        # 寻找可能存在的导出窗口
        export_window = self.app.WindowControl(searchDepth=1, Name="导出")
        if export_window.Exists(0):
            self.app = export_window
            self.app_status = "pre_export"

        # 初始化导出子状态
        self.init_export_sub_status()

        logger.info("app_status: %s, app_sub_status: %s", self.app_status, self.app_sub_status)

        self.app.SetActive()
        self.app.SetTopmost()

    # 初始化导出子状态
    def init_export_sub_status(self) -> None:
        if self.app_status == "pre_export":
            # 0. 初始化默认值为导出中
            self.app_sub_status = "exporting"
            
            # 1. 检查窗口是否停留在导出开始页面
            export_ok_btn = self.app.TextControl(searchDepth=2, Compare=ControlFinder.desc_matcher("ExportOkBtn", exact=True))
            if export_ok_btn.Exists(0):
                self.app_sub_status = "export_start"
                return

            # 2. 检查窗口是否停留在导出完成页面
            succeed_close_btn = self.app.TextControl(searchDepth=2, Compare=ControlFinder.desc_matcher("ExportSucceedCloseBtn"))
            if succeed_close_btn.Exists(0):
                self.app_sub_status = "export_succeed"
                return
        else:
            self.app_sub_status = "none"

    def __jianying_window_cmp(self, control: uia.WindowControl, depth: int) -> bool:
        if control.Name != "剪映专业版":
            return False
        if "HomePage".lower() in control.ClassName.lower():
            self.app_status = "home"
            return True
        if "MainWindow".lower() in control.ClassName.lower():
            self.app_status = "edit"
            return True

        logger.info(f"ClassName: {control.ClassName.lower()}, Name: {control.Name.lower()}")
        return False