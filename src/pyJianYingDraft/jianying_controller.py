"""剪映自动化控制，主要与自动导出有关"""

import time
import shutil
import uiautomation as uia

from enum import Enum
from typing import Optional, Literal, Callable

from . import exceptions
from .exceptions import AutomationError

# 添加logger导入
from src.utils.logger import logger

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

    app: uia.WindowControl
    """剪映窗口"""
    app_status: Literal["home", "edit", "pre_export"]
    """当app_status为pre_export时，app_sub_status表示导出过程中的子状态"""
    app_sub_status: Literal["none", "export_start", "exporting", "export_succeed"]

    def __init__(self):
        """初始化剪映控制器, 此时剪映应该处于目录页"""
        self.get_window()

    def find_and_click_draft(self, draft_name: str) -> None:
        """查找并点击指定名称的草稿
        
        Args:
            draft_name (str): 要查找的草稿名称
            
        Raises:
            DraftNotFound: 未找到指定名称的剪映草稿
        """
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

    def wait_for_export_completion(self, timeout: float) -> None:
        """等待导出完成
        
        Args:
            timeout (float): 超时时间（秒）
            
        Raises:
            AutomationError: 导出超时
        """
        # 等待导出完成
        st = time.time()
        while True:
            self.get_window()
            if self.app_status != "pre_export": break

            succeed_close_btn = self.app.TextControl(searchDepth=2, Compare=ControlFinder.desc_matcher("ExportSucceedCloseBtn"))
            if succeed_close_btn.Exists(0):
                break

            if time.time() - st > timeout:
                raise AutomationError("导出超时, 时限为%d秒" % timeout)

            time.sleep(1)
        time.sleep(2)

    def return_to_home(self) -> None:
        """回到目录页并稍作延迟"""
        self.get_window()
        self.switch_to_home()
        time.sleep(2)

    def move_exported_file(self, original_path: str, output_path: Optional[str]) -> None:
        """移动导出的文件到指定位置
        
        Args:
            original_path (str): 原始导出路径
            output_path (Optional[str]): 目标输出路径，如果为None则不移动
        """
        if output_path is not None:
            shutil.move(original_path, output_path)

    def export_draft(self, draft_name: str, output_path: Optional[str] = None, *,
                     resolution: Optional[ExportResolution] = None,
                     framerate: Optional[ExportFramerate] = None,
                     timeout: float = 1200) -> None:
        """导出指定的剪映草稿, **目前仅支持剪映6及以下版本**

        **注意: 需要确认有导出草稿的权限(不使用VIP功能或已开通VIP), 否则可能陷入死循环**

        Args:
            draft_name (`str`): 要导出的剪映草稿名称
            output_path (`str`, optional): 导出路径, 支持指向文件夹或直接指向文件, 不指定则使用剪映默认路径.
            resolution (`Export_resolution`, optional): 导出分辨率, 默认不改变剪映导出窗口中的设置.
            framerate (`Export_framerate`, optional): 导出帧率, 默认不改变剪映导出窗口中的设置.
            timeout (`float`, optional): 导出超时时间(秒), 默认为20分钟.

        Raises:
            `DraftNotFound`: 未找到指定名称的剪映草稿
            `AutomationError`: 剪映操作失败
        """
        logger.info(f"start export {draft_name} to {output_path}")

        # 初始化准备
        self.get_window()
        self.switch_to_home()

        original_path = None

        for i in range(16):
            # 确保窗口有焦点
            self.__ensure_window_focus()
            if self.app_status == "home":
                logger.info("[%d]app is already in home page", i)
                self.find_and_click_draft(draft_name)
            elif self.app_status == "edit":
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
                    self.wait_for_export_completion(timeout)                    
                elif self.app_sub_status == "export_succeed":
                    logger.info("[%d]app is already in pre_export[export_succeed] page", i)
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
            if self.app_status == "home":
                return
            elif self.app_status == "pre_export":
                if self.app_sub_status == "export_succeed":
                    succeed_close_btn = self.app.TextControl(searchDepth=2, Compare=ControlFinder.desc_matcher("ExportSucceedCloseBtn"))
                    if succeed_close_btn.Exists(0):
                        succeed_close_btn.Click(simulateMove=False)
                        time.sleep(2)
                        self.get_window()
            elif self.app_status == "edit":
                close_btn = self.app.GroupControl(searchDepth=1, ClassName="TitleBarButton", foundIndex=3)
                close_btn.Click(simulateMove=False)
                time.sleep(2)
                self.get_window()
            else:
                raise AutomationError("invalid app status: %s" % self.app_status)
        
        logger.info("can not switch to home page after 32 attempts")

    def get_window(self) -> None:
        """寻找剪映窗口并置顶"""
        if hasattr(self, "app") and self.app.Exists(0):
            self.app.SetTopmost(False)

        self.app = uia.WindowControl(searchDepth=1, Compare=self.__jianying_window_cmp)
        if not self.app.Exists(0):
            raise AutomationError("剪映窗口未找到")

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