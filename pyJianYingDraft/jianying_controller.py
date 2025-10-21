"""剪映自动化控制，主要与自动导出有关"""

import time
import shutil
from process_controller import ProcessController
import uiautomation as uia
import re
import os
from logging.handlers import RotatingFileHandler
import logging # 引入 logging 模块

from enum import Enum
from typing import Optional, Literal, Callable

from . import exceptions
from .exceptions import AutomationError

# --- 配置日志记录器 ---
logger = logging.getLogger('flask_video_generator') # 为您的Flask应用定义一个特定的logger名称
logger.setLevel(logging.INFO) # 设置最低记录级别

# 创建一个格式化器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 创建一个控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 创建一个文件处理器，并设置文件轮换
log_dir = 'logs' # 定义日志文件存放的目录
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file_path = os.path.join(log_dir, 'flask_video_generator.log') # 日志文件名

file_handler = RotatingFileHandler(log_file_path, backupCount=5, encoding='utf-8') # 5MB per file, keep 5 backups
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info("Flask 应用日志系统初始化完成。")

class Export_resolution(Enum):
    """导出分辨率"""
    RES_4K = "4K"
    RES_2K = "2K"
    RES_1080P = "1080P"
    RES_720P = "720P"
    RES_480P = "480P"

class Export_framerate(Enum):
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

class Jianying_controller:
    """剪映控制器"""

    app: uia.WindowControl
    """剪映窗口"""
    app_status: Literal["home", "edit", "pre_export"]
    export_progress: dict = {"status": "idle", "percent": 0.0, "message": "", "start_time": 0}
    """导出进度信息"""

    def __init__(self):
        """初始化剪映控制器, 此时剪映应该处于目录页"""
        logger.info("Initializing Jianying_controller...")
        self.get_window()
        self.export_progress = {"status": "idle", "percent": 0.0, "message": "", "start_time": 0}
        logger.info("Jianying_controller initialized successfully.")

    def get_export_progress(self) -> dict:
        """获取当前导出进度
        
        Returns:
            dict: 包含以下字段的字典
                - status: 当前状态，可能的值有 "idle"(空闲), "exporting"(导出中), "finished"(已完成), "error"(出错)
                - percent: 导出进度百分比，0-100的浮点数
                - message: 进度消息
                - start_time: 开始导出的时间戳
                - elapsed: 已经过的时间(秒)
        """
        if self.export_progress["status"] != "idle":
            self.export_progress["elapsed"] = time.time() - self.export_progress["start_time"]
        return self.export_progress

    def export_draft(self, draft_name: str, output_path: Optional[str] = None, *,
                     resolution: Optional[Export_resolution] = None,
                     framerate: Optional[Export_framerate] = None,
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
        logger.info(f"Starting export for draft: '{draft_name}' to '{output_path or 'default path'}' with resolution: {resolution}, framerate: {framerate}")
        self.export_progress["status"] = "exporting"
        self.export_progress["percent"] = 0.0
        self.export_progress["message"] = "开始导出"
        self.export_progress["start_time"] = time.time()
        self.export_progress["elapsed"] = 0

        logger.info("Attempting to switch to home page.")
        self.get_window()
        self.switch_to_home()
        logger.info("Successfully switched to home page.")

        self.export_progress["status"] = "exporting"
        self.export_progress["percent"] = 5.0
        self.export_progress["message"] = "正在导出"
        self.export_progress["elapsed"] = time.time() - self.export_progress["start_time"]

        logger.info(f"Clicking draft: '{draft_name}'")
        # 点击对应草稿
        draft_name_text = self.app.TextControl(
            searchDepth=2,
            Compare=ControlFinder.desc_matcher(f"HomePageDraftTitle:{draft_name}", exact=True)
        )
        if not draft_name_text.Exists(0):
            error_msg = f"DraftNotFound: No Jianying draft named '{draft_name}' found."
            logger.error(error_msg)
            self.export_progress["status"] = "error"
            self.export_progress["percent"] = 100.0
            self.export_progress["message"] = f"未找到名为{draft_name}的剪映草稿"
            self.export_progress["elapsed"] = time.time() - self.export_progress["start_time"]
            raise exceptions.DraftNotFound(f"未找到名为{draft_name}的剪映草稿")
        draft_btn = draft_name_text.GetParentControl()
        if draft_btn is None:
            error_msg = f"AutomationError: Could not find parent control for draft title '{draft_name}'."
            logger.error(error_msg)
            self.export_progress["status"] = "error"
            self.export_progress["percent"] = 100.0
            self.export_progress["message"] = f"自动化操作失败，无法点击草稿'{draft_name}'"
            self.export_progress["elapsed"] = time.time() - self.export_progress["start_time"]
            raise AutomationError(error_msg)
        
        draft_btn.Click(simulateMove=False)
        logger.info(f"Clicked on draft: '{draft_name}'.")

        self.export_progress["status"] = "exporting"
        self.export_progress["percent"] = 10.0
        self.export_progress["message"] = "正在导出"
        self.export_progress["elapsed"] = time.time() - self.export_progress["start_time"]
        
        logger.info(f"Waiting for edit window for draft: '{draft_name}' (timeout: 180s)")
        # 等待编辑窗口加载，最多等待180秒
        wait_start_time = time.time()
        while time.time() - wait_start_time < 180:
            try:
                self.get_window() # 尝试获取最新的窗口句柄和状态
            except AutomationError as e:
                logger.debug(f"Failed to get window during edit window wait: {e}. Retrying...")
                time.sleep(1)
                continue
            
            # 检查是否出现显卡运行环境提示框，如果出现则点击"暂不启用"
            try:
                disable_btn = self.app.TextControl(searchDepth=3, Compare=ControlFinder.desc_matcher("暂不启用"))
                if disable_btn.Exists(0):
                    disable_btn.Click(simulateMove=False)
                    logger.info("Clicked '暂不启用' for graphics environment prompt.")
                    time.sleep(1)
            except Exception as e:
                logger.debug(f"No '暂不启用' button found or error during click: {e}")
            
            # 检查是否已进入编辑窗口
            time.sleep(1)
            export_btn = self.app.TextControl(searchDepth=2, Compare=ControlFinder.desc_matcher("MainWindowTitleBarExportBtn"))
            if export_btn.Exists(0):
                time.sleep(1)
                break
            time.sleep(1)
        else:
            error_msg = f"AutomationError: Waiting for edit window timed out (180 seconds) for draft '{draft_name}'."
            logger.error(error_msg)
            self.export_progress["status"] = "error"
            self.export_progress["percent"] = 100.0
            self.export_progress["message"] = "编辑超时（180秒）"
            self.export_progress["elapsed"] = time.time() - self.export_progress["start_time"]
            raise AutomationError("等待进入编辑窗口超时（180秒）")
        self.export_progress["status"] = "exporting"
        self.export_progress["percent"] = 15.0
        self.export_progress["message"] = "正在导出"
        self.export_progress["elapsed"] = time.time() - self.export_progress["start_time"]
        
        # 点击导出按钮
        export_btn.Click(simulateMove=False)
        
        logger.info(f"Waiting for export settings window (timeout: 180s) for draft: '{draft_name}'")
        # 等待导出窗口加载，最多等待180秒
        wait_start_time = time.time()
        while time.time() - wait_start_time < 180:
            try:
                self.get_window()
            except:
                time.sleep(1)
                continue
            # 检查是否已进入导出窗口
            export_path_sib = self.app.TextControl(searchDepth=2, Compare=ControlFinder.desc_matcher("ExportPath"))
            if export_path_sib.Exists(0):
                time.sleep(1) # 额外等待确保UI稳定
                break
            time.sleep(1)
        else:
            self.export_progress["status"] = "error"
            self.export_progress["percent"] = 100.0
            self.export_progress["message"] = "导出超时（180秒）"
            self.export_progress["elapsed"] = time.time() - self.export_progress["start_time"]
            raise AutomationError("等待进入导出窗口超时（180秒）")
        self.export_progress["status"] = "exporting"
        self.export_progress["percent"] = 20.0
        self.export_progress["message"] = "正在导出"
        self.export_progress["elapsed"] = time.time() - self.export_progress["start_time"]
        
        # 获取原始导出路径（带后缀名）
        export_path_text = export_path_sib.GetSiblingControl(lambda ctrl: True)
        assert export_path_text is not None
        export_path = export_path_text.GetPropertyValue(30159)

        logger.info(f"Attempting to set resolution: {resolution.value if resolution else 'unchanged'}, framerate: {framerate.value if framerate else 'unchanged'} for '{draft_name}'")
        # 设置分辨率
        if resolution is not None:
            retry_count = 0
            max_retries = 3
            while retry_count < max_retries:
                try:
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
                    break  # 设置成功，跳出循环
                except AutomationError as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        raise  # 重试次数用完，抛出异常
                    time.sleep(1)  # 延迟1秒后重试

        # 设置帧率
        if framerate is not None:
            retry_count = 0
            max_retries = 3
            while retry_count < max_retries:
                try:
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
                    break  # 设置成功，跳出循环
                except AutomationError as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        raise  # 重试次数用完，抛出异常
                    time.sleep(1)  # 延迟1秒后重试

        logger.info(f"Clicking final export button for draft: '{draft_name}'")
        # 点击导出
        export_btn = self.app.TextControl(searchDepth=2, Compare=ControlFinder.desc_matcher("ExportOkBtn", exact=True))
        if not export_btn.Exists(0):
            raise AutomationError("未在导出窗口中找到导出按钮")
        export_btn.Click(simulateMove=False)
        time.sleep(5)

        # 等待导出完成
        st = time.time()
        while True:
            # self.get_window()
            if self.app_status != "pre_export": continue

            # 查找导出成功按钮
            succeed_close_btn = self.app.TextControl(searchDepth=2, Compare=ControlFinder.desc_matcher("ExportSucceedCloseBtn"))
            if succeed_close_btn.Exists(0):
                self.export_progress["status"] = "finished"
                self.export_progress["percent"] = 100
                self.export_progress["message"] = "导出完成"
                self.export_progress["elapsed"] = time.time() - self.export_progress["start_time"]
                succeed_close_btn.Click(simulateMove=False)
                break

            # 查找并更新进度百分比
            try:
                # 尝试查找所有文本控件，寻找包含百分比的文本
                text_controls = self.app.GetChildren()
                for control in text_controls:
                    progress_text = ""
                    # 检查控件名称
                    if hasattr(control, "Name") and control.Name and "%" in control.Name:
                        progress_text = control.Name
                    # 检查控件描述
                    elif hasattr(control, "GetPropertyValue"):
                        desc = control.GetPropertyValue(30159) if hasattr(control, "GetPropertyValue") else ""
                        if desc and isinstance(desc, str) and "%" in desc:
                            progress_text = desc
                    
                    if progress_text:
                        # 提取百分比数字，支持小数点
                        percent_match = re.search(r'(\d+\.?\d*)%', progress_text)
                        print("progress_text is " + progress_text)
                        print("percent_match is ", percent_match)
                        if percent_match:
                            percent = float(percent_match.group(1))  # 使用float而不是int
                            print("percent is ", percent)
                            self.export_progress["percent"] = percent * 0.8 + 20
                            self.export_progress["message"] = "正在导出"
                            self.export_progress["elapsed"] = time.time() - self.export_progress["start_time"]
                        break
            except Exception as e:
                self.export_progress["message"] = f"获取进度时出错: {e}"
                self.export_progress["elapsed"] = time.time() - self.export_progress["start_time"]

            if time.time() - st > timeout:
                self.export_progress["status"] = "error"
                self.export_progress["message"] = f"导出超时{timeout}秒"
                self.export_progress["elapsed"] = time.time() - self.export_progress["start_time"]
                raise AutomationError("导出超时, 时限为%d秒" % timeout)

            time.sleep(1)
        time.sleep(2)

        # 复制导出的文件到指定目录
        if output_path is not None:
            shutil.move(export_path, output_path)

        logger.info(f"导出 {draft_name} 至 {output_path} 完成")

        # 回到目录页
        logger.info("back to home page")
        try:
            self.get_window()
            self.switch_to_home()
        except Exception as e:
            logger.warning(f"back to home 失败: {str(e)}, 杀进程重启")
            ProcessController.kill_jianying()

            if not ProcessController.restart_jianying():
                logger.critical("Failed to restart JianYing application. Aborting.")
                raise Exception("无法重启剪映程序")
            
            time.sleep(2)  # 等待进程启动
            ProcessController.kill_jianying_detector()


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
        return False
