""" 
视频生成异步任务队列管理器
支持任务排队、状态跟踪和结果查询
"""
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Tuple, Any
from dataclasses import dataclass
from src.utils.logger import logger
from src.utils import helper
from src.utils.video_task_store import (
    get_completed_by_draft_id,
    prune_if_needed,
    save_completed_result,
)
import src.pyJianYingDraft as draft
import config
import os
import sys
import subprocess
import json

# 如果是Linux系统，则不导入uiautomation，并避免执行相关代码
try:
    from uiautomation import UIAutomationInitializerInThread  # type: ignore
except ImportError:
    # 在缺少依赖的系统上创建一个占位符
    class UIAutomationInitializerInThread:  # type: ignore
        def __enter__(self):
            pass
        def __exit__(self, *args):
            pass


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"      # 等待中
    PROCESSING = "processing"  # 处理中
    COMPLETED = "completed"   # 已完成
    FAILED = "failed"        # 失败


@dataclass
class VideoGenTask:
    """视频生成任务数据类"""
    draft_url: str
    draft_id: str
    status: TaskStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    video_url: str = ""
    error_message: str = ""
    progress: int = 0  # 进度百分比 0-100
    api_key: Optional[str] = None  # 存储API密钥用于计费
    outfile: str = ""  # 导出目标路径，在下载阶段生成


class VideoGenTaskManager:
    """视频生成任务管理器 - 单例模式

    草稿下载、COS 上传可并发（各自线程池）；剪映 RPA 导出由 export_video_lock 保证全局同一时间仅一个。
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        # 任务存储：{draft_url: VideoGenTask}
        self.tasks: Dict[str, VideoGenTask] = {}
        # 任务队列
        self.task_queue: asyncio.Queue = asyncio.Queue()
        _io_workers = min(32, (os.cpu_count() or 1) + 4)
        self._download_executor = ThreadPoolExecutor(
            max_workers=_io_workers,
            thread_name_prefix="draft_dl",
        )
        self._upload_executor = ThreadPoolExecutor(
            max_workers=_io_workers,
            thread_name_prefix="cos_upload",
        )
        # 导出视频专用锁（确保任何时候只有一个线程执行剪映 RPA 导出）
        self.export_video_lock = threading.Lock()
        # 工作线程
        self.worker_thread: Optional[threading.Thread] = None
        # 停止标志
        self.stop_flag = threading.Event()
        
        logger.info("VideoGenTaskManager initialized")   
    
    def submit_task(self, draft_url: str, api_key: str = None) -> None:
        """
        提交视频生成任务
        
        Args:
            draft_url: 草稿URL
            api_key: API密钥，用于计费
        """
        # 提取草稿ID
        draft_id = helper.get_url_param(draft_url, "draft_id")
        if not draft_id:
            raise ValueError("无效的草稿URL")
        
        # 检查是否已有相同草稿的任务在进行
        if draft_url in self.tasks:
            existing_task = self.tasks[draft_url]
            if existing_task.status in [TaskStatus.PENDING, TaskStatus.PROCESSING]:
                logger.info(f"Task already exists for draft_url: {draft_url}")
                return
        
        # 创建新任务
        task = VideoGenTask(
            draft_url=draft_url,
            draft_id=draft_id,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            api_key=api_key  # 存储API密钥用于计费
        )
        
        # 存储任务
        self.tasks[draft_url] = task
        
        # 添加到队列 - 使用线程安全的方式
        self._add_task_to_queue_sync(task)
        
        # 启动工作线程（如果还没启动）
        self._ensure_worker_running()
        
        logger.info(f"Task submitted for draft_url: {draft_url}")
    
    async def _add_to_queue(self, task: VideoGenTask):
        """将任务添加到队列"""
        await self.task_queue.put(task)
        logger.info(f"Task added to queue: {task.draft_url}")
    
    def _add_task_to_queue_sync(self, task: VideoGenTask):
        """
        同步方式将任务添加到队列
        使用线程安全的方式提交任务
        """
        # 由于队列是asyncio.Queue，我们需要从主线程安全地添加任务
        try:
            # 获取当前事件循环
            loop = asyncio.get_running_loop()
            # 如果当前有运行的事件循环，就创建任务
            if loop.is_running():
                asyncio.run_coroutine_threadsafe(self._add_to_queue(task), loop)
            else:
                # 如果没有运行的事件循环，启动一个
                if not loop.is_closed():
                    loop.create_task(self._add_to_queue(task))
        except RuntimeError:
            # 如果没有事件循环，创建一个新的
            def run_in_new_loop():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    new_loop.run_until_complete(self._add_to_queue(task))
                finally:
                    new_loop.close()
            
            # 在新线程中运行事件循环
            thread = threading.Thread(target=run_in_new_loop, daemon=True)
            thread.start()
    
    def get_task_status(self, draft_url: str) -> Optional[Dict[str, Any]]:
        """
        根据草稿URL获取任务状态
        
        Args:
            draft_url: 草稿URL
            
        Returns:
            任务状态信息，如果不存在返回None
        """
        prune_if_needed()

        task = self.tasks.get(draft_url)
        if task:
            return {
                "draft_url": task.draft_url,
                "status": task.status.value,
                "progress": task.progress,
                "video_url": task.video_url,
                "error_message": task.error_message,
                "created_at": task.created_at.isoformat(),
                "started_at": task.started_at.isoformat() if task.started_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            }

        draft_id = helper.get_url_param(draft_url, "draft_id")
        return get_completed_by_draft_id(draft_id)

    def get_active_render_count(self) -> int:
        """
        当前进行中的云渲染草稿数量：排队(pending) + 渲染中(processing)。
        不含已完成(completed)、失败(failed)。
        """
        active = (TaskStatus.PENDING, TaskStatus.PROCESSING)
        return sum(1 for t in self.tasks.values() if t.status in active)

    def _ensure_worker_running(self):
        """确保工作线程正在运行"""
        if self.worker_thread is None or not self.worker_thread.is_alive():
            self.stop_flag.clear()
            self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
            self.worker_thread.start()
            logger.info("Worker thread started")
    
    def _worker_loop(self):
        """工作线程主循环"""
        logger.info("Worker loop started")
        
        # 在工作线程中创建新的事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self._async_worker_loop())
        finally:
            loop.close()
    
    async def _async_worker_loop(self):
        """异步工作循环"""
        while not self.stop_flag.is_set():
            try:
                # 等待任务（带超时，以便检查停止标志）
                task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)

                t = asyncio.create_task(self._process_task(task))
                t.add_done_callback(self._log_async_task_done)
                
            except asyncio.TimeoutError:
                # 超时，继续循环检查停止标志
                continue
            except Exception as e:
                logger.error(f"Worker loop error: {e}")
                # 短暂休息后继续
                await asyncio.sleep(1)

    def _log_async_task_done(self, fut: asyncio.Task) -> None:
        try:
            fut.result()
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.exception(f"Async task finished with error: {e}")
    
    async def _process_task(self, task: VideoGenTask):
        """
        处理单个视频生成任务：下载、COS 上传可与其他任务并行；导出受 export_video_lock 串行。
        """
        logger.info(f"Processing task: {task.draft_url}")

        task.status = TaskStatus.PROCESSING
        task.started_at = datetime.now()
        task.progress = 10

        loop = asyncio.get_running_loop()

        try:
            prep_error = await loop.run_in_executor(
                self._download_executor,
                self._phase_download_and_prepare,
                task,
            )
            if prep_error:
                task.status = TaskStatus.FAILED
                task.error_message = prep_error
                task.progress = 0
                logger.error(f"Task failed: {task.draft_url}, error: {prep_error}")
                return

            export_error = await loop.run_in_executor(
                None,
                self._phase_export_only,
                task,
            )
            if export_error:
                task.status = TaskStatus.FAILED
                task.error_message = export_error
                task.progress = 0
                logger.error(f"Task failed: {task.draft_url}, error: {export_error}")
                return

            video_url, error_message = await loop.run_in_executor(
                self._upload_executor,
                self._phase_cos_upload_finalize,
                task,
            )

            if video_url:
                task.status = TaskStatus.COMPLETED
                task.video_url = video_url
                task.progress = 100
                logger.info(f"Task completed successfully: {task.draft_url}")
            else:
                task.status = TaskStatus.FAILED
                task.error_message = error_message
                task.progress = 0
                logger.error(f"Task failed: {task.draft_url}, error: {error_message}")

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            task.progress = 0
            logger.exception(f"Task exception: {task.draft_url}, error: {e}")

        finally:
            task.completed_at = datetime.now()
            if task.status in (TaskStatus.COMPLETED, TaskStatus.FAILED):
                try:
                    save_completed_result(
                        draft_id=task.draft_id,
                        draft_url=task.draft_url,
                        status=task.status.value,
                        progress=task.progress,
                        video_url=task.video_url,
                        error_message=task.error_message,
                        created_at=task.created_at,
                        started_at=task.started_at,
                        completed_at=task.completed_at,
                    )
                except Exception as persist_err:
                    logger.exception(
                        "Failed to persist video gen task result: %s", persist_err
                    )
    
    def _check_draft_duration(self, task: VideoGenTask) -> bool:
        """
        检查草稿中的视频时长是否大于0
        
        Args:
            task: 视频生成任务
            
        Returns:
            bool: 时长是否大于0
        """
        try:
            # 构建草稿内容文件路径
            draft_content_path = os.path.join(config.DRAFT_SAVE_PATH, task.draft_id, "draft_content.json")
            
            # 检查文件是否存在
            if not os.path.exists(draft_content_path):
                logger.error(f"草稿内容文件不存在: {draft_content_path}")
                return False
            
            # 读取并解析JSON文件
            with open(draft_content_path, 'r', encoding='utf-8') as f:
                draft_content = json.load(f)
            
            # 获取时长
            duration = draft_content.get("duration", 0)
            
            # 检查时长是否大于0
            if duration <= 0:
                logger.error(f"草稿中视频时长不大于0: {duration}, 草稿ID: {task.draft_id}")
                return False
            
            logger.info(f"草稿视频时长检查通过: {duration} 微秒, 草稿ID: {task.draft_id}")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"解析草稿内容文件失败: {e}, 草稿ID: {task.draft_id}")
            return False
        except Exception as e:
            logger.error(f"检查草稿时长时发生错误: {e}, 草稿ID: {task.draft_id}")
            return False

    def _phase_download_and_prepare(self, task: VideoGenTask) -> str:
        """
        下载草稿并校验时长（可并发执行）。

        Returns:
            错误信息，成功时返回空字符串。
        """
        try:
            task.progress = 20
            task.outfile = os.path.join(config.DRAFT_DIR, f"{helper.gen_unique_id()}.mp4")

            if not sys.platform.startswith("win"):
                return "视频生成功能仅在Windows系统上可用"

            task.progress = 30

            if not self._download_draft(task):
                error_message = f"草稿下载失败: {task.draft_url}"
                logger.error(error_message)
                return error_message

            if not self._check_draft_duration(task):
                error_message = (
                    f"草稿中视频时长不大于0，请检查草稿内容: {task.draft_id}"
                )
                logger.error(error_message)
                return error_message

            task.progress = 40
            return ""
        except Exception as exc:
            logger.exception(
                f"Export draft failed: draft_id={task.draft_id}, error={exc}"
            )
            return f"导出草稿失败: {exc}"

    def _phase_export_only(self, task: VideoGenTask) -> str:
        """
        仅执行剪映导出（在 export_video_lock 内，全局串行）。

        Returns:
            错误信息，成功时返回空字符串。
        """
        try:
            if not self._export_video(task, task.outfile):
                return "导出草稿失败"
            return ""
        except Exception as exc:
            logger.exception(
                f"Export draft failed: draft_id={task.draft_id}, error={exc}"
            )
            return f"导出草稿失败: {exc}"

    def _phase_cos_upload_finalize(self, task: VideoGenTask) -> Tuple[str, str]:
        """
        COS 上传、扣费与清理（可与其它任务的上传并行）。
        """
        try:
            task.progress = 95
            upload_url, upload_failed = self._upload_video_to_cos(task.outfile)
            self._calculate_and_charge(task, task.outfile)
            self._cleanup_files(task.outfile, task.draft_id)
            return self._handle_result(upload_url, upload_failed)
        except Exception as exc:
            logger.exception(
                f"Export draft failed: draft_id={task.draft_id}, error={exc}"
            )
            return "", f"导出草稿失败: {exc}"
    
    def _download_draft(self, task: VideoGenTask) -> bool:
        """
        下载草稿
        
        Args:
            task: 视频生成任务
        
        Returns:
            bool: 下载是否成功
        """
        logger.info(f"Start downloading draft before export: {task.draft_url}")
        from src.utils.draft_downloader import download_draft
        download_success = download_draft(task.draft_url)
        
        if download_success:
            logger.info(f"Draft downloaded successfully: {task.draft_url}")
        else:
            logger.error(f"Failed to download draft: {task.draft_url}")
        
        return download_success
    
    def _export_video(self, task: VideoGenTask, outfile: str) -> bool:
        """
        导出视频
        
        Args:
            task: 视频生成任务
            outfile: 输出文件路径
        
        Returns:
            bool: 导出是否成功
        """
        # 使用专用锁确保任何时候只有一个线程执行导出视频操作
        with self.export_video_lock:
            logger.info(f"Begin to export draft: {task.draft_id} -> {outfile}")
            
            # 更新进度
            task.progress = 50
            
            # 检查JianyingController是否可用
            if draft.JianyingController is None:
                if sys.platform != "win32":
                    error_msg = "剪映自动导出功能仅在Windows平台可用"
                else:
                    error_msg = "缺少Windows依赖，请安装: pip install capcut-mate[windows]"
                logger.error(error_msg)
                raise RuntimeError(error_msg)
            
            with UIAutomationInitializerInThread():
                # 此前需要将剪映打开，并位于目录页
                ctrl = draft.JianyingController()

                # 更新进度
                task.progress = 70

                # 导出指定名称的草稿
                ctrl.export_draft(task.draft_id, outfile)

            # 检查文件是否生成
            if not os.path.exists(outfile):
                # 个别版本剪映不会抛异常，但文件未生成
                logger.error("剪映导出结束但目标文件未生成，请检查磁盘空间或剪映版本")
                return False

            logger.info(f"Export draft success: {outfile}")
            return True
    
    def _upload_video_to_cos(self, outfile: str) -> Tuple[str, bool]:
        """
        上传视频到COS
        
        Args:
            outfile: 输出文件路径
        
        Returns:
            (upload_url, upload_failed): 上传后的URL和是否上传失败
        """
        upload_url = ""
        upload_failed = False
        
        try:
            from src.utils.cos import cos_upload_file
            logger.info(f"Uploading video to COS: {outfile}")
            upload_url = cos_upload_file(outfile, expire_days=config.VIDEO_GEN_RETENTION_DAYS)
            logger.info(f"Video uploaded to COS successfully: {upload_url}")
        except Exception as upload_error:
            logger.error(f"Failed to upload video to COS: {upload_error}")
            upload_failed = True
        
        return upload_url, upload_failed
    
    def _calculate_and_charge(self, task: VideoGenTask, outfile: str) -> None:
        """
        计算并扣除费用（必需执行但不关心结果）
        
        Args:
            task: 视频生成任务
            outfile: 输出文件路径
        
        Returns:
            None: 无返回值
        """
        if config.ENABLE_APIKEY and task.api_key:
            try:
                # 导入获取媒体时长的函数
                from src.utils.media import get_media_duration
                
                # 获取视频时长（返回的是微秒）
                duration_us = get_media_duration(outfile)
                
                if duration_us and duration_us > 0:
                    # 将微秒转换为秒
                    video_duration = duration_us / 1_000_000  # 微秒转秒
                    
                    # 计算费用：0.01积分/秒
                    cost = video_duration * 0.01
                    
                    # 导入扣费函数
                    from src.utils.points import deduct_user_points
                    
                    # 扣除用户积分（必需执行但不关心结果）
                    charge_success = deduct_user_points(
                        api_key=task.api_key,
                        points=cost,
                        desc=f"剪映草稿导出视频，时长{video_duration:.2f}秒，费用{cost:.2f}积分"
                    )
                    
                    if charge_success:
                        logger.info(f"Successfully charged {cost:.2f} points for video duration {video_duration:.2f}s, API key: {task.api_key[:8]}***")
                    else:
                        logger.warning(f"Failed to charge {cost:.2f} points for video duration {video_duration:.2f}s, API key: {task.api_key[:8]}***")
                else:
                    logger.warning(f"Could not determine video duration for charging: {outfile}")
            except Exception as charge_error:
                logger.error(f"Error calculating or charging for video duration: {charge_error}")
    
    def _cleanup_files(self, outfile: str, draft_id: str) -> None:
        """
        清理临时文件
        
        Args:
            outfile: 输出文件路径
            draft_id: 草稿ID
        """
        try:
            # 清理本地视频文件
            if os.path.exists(outfile):
                os.remove(outfile)
                logger.info(f"Cleaned up local video file: {outfile}")
            
            # 清理下载的草稿文件
            import shutil
            draft_path = os.path.join(config.DRAFT_SAVE_PATH, draft_id)
            if os.path.exists(draft_path):
                shutil.rmtree(draft_path)
                logger.info(f"Cleaned up draft directory: {draft_path}")
        except Exception as cleanup_error:
            logger.warning(f"Failed to clean up files: {cleanup_error}")
    
    def _handle_result(self, upload_url: str, upload_failed: bool) -> Tuple[str, str]:
        """
        处理最终结果
        
        Args:
            upload_url: 上传后的URL
            upload_failed: 上传是否失败
        
        Returns:
            (video_url, error_message): 视频URL和错误信息
        """
        # 如果上传失败，返回错误信息；扣费结果不关心
        if upload_failed:
            return "", "视频上传失败"
        
        # 返回上传后的URL，扣费结果不阻塞视频生成
        return upload_url, ""
    
    def stop(self):
        """停止任务管理器"""
        logger.info("Stopping VideoGenTaskManager")
        self.stop_flag.set()
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=5)
        self._download_executor.shutdown(wait=False)
        self._upload_executor.shutdown(wait=False)
        logger.info("VideoGenTaskManager stopped")


# 全局任务管理器实例
task_manager = VideoGenTaskManager()