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
            if self.app_status != "pre_export": continue

            succeed_close_btn = self.app.TextControl(searchDepth=2, Compare=ControlFinder.desc_matcher("ExportSucceedCloseBtn"))
            if succeed_close_btn.Exists(0):
                # 尝试点击成功关闭按钮，最多重试5次
                max_click_retries = 5
                click_retry_count = 0
                
                while click_retry_count < max_click_retries:
                    succeed_close_btn.Click(simulateMove=False)
                    
                    # 等待一段时间让点击生效
                    time.sleep(2)
                    
                    # 重新获取窗口状态，检查是否已离开导出成功界面
                    self.get_window()
                    
                    # 如果状态不再是pre_export，说明点击成功，成功关闭了导出界面
                    if self.app_status != "pre_export":
                        logger.info("成功点击导出完成关闭按钮，已离开导出界面")
                        return  # 成功完成导出，退出函数
                    
                    # 如果仍然在导出界面，说明点击可能没有生效，继续重试
                    click_retry_count += 1
                    logger.info(f"导出完成关闭按钮点击未生效，正在进行第 {click_retry_count} 次重试")
                    time.sleep(2)  # 等待后再试
                
                # 如果重试多次后仍然无法关闭导出界面，则抛出异常
                raise AutomationError(f"导出完成关闭按钮点击失败，已重试 {max_click_retries} 次，无法离开导出界面")
                
            if time.time() - st > timeout:
                raise AutomationError("导出超时, 时限为%d秒" % timeout)

            time.sleep(1)

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
        print(f"开始导出 {draft_name} 至 {output_path}")
        # 初始化准备
        self.get_window()
        self.switch_to_home()
        
        # 查找并点击目标草稿
        self.find_and_click_draft(draft_name)
        
        # 点击导出按钮进入导出界面
        self.click_export_button()
        
        # 获取原始导出路径
        original_path = self.get_original_export_path()
        
        # 设置分辨率（如果指定）
        self.set_export_resolution(resolution)
        
        # 设置帧率（如果指定）
        self.set_export_framerate(framerate)
        
        # 点击最终导出按钮
        self.click_final_export_button()
        
        # 等待导出完成
        self.wait_for_export_completion(timeout)
        
        # 返回主页
        self.return_to_home()
        
        # 移动导出文件到指定路径（如果指定）
        self.move_exported_file(original_path, output_path)
        
        print(f"导出 {draft_name} 至 {output_path} 完成")

    def switch_to_home(self) -> None:
        """切换到剪映主页"""
        if self.app_status == "home":
            return
        if self.app_status != "edit":
            raise AutomationError("仅支持从编辑模式切换到主页")
        close_btn = self.app.GroupControl(searchDepth=1, ClassName="TitleBarButton", foundIndex=3)
        close_btn.Click(simulateMove=False)
        time.sleep(2)
        self.get_window()

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

        self.app.SetActive()
        self.app.SetTopmost()

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