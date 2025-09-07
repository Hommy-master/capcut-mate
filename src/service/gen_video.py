from src.utils.logger import logger
from src.utils import helper
import src.pyJianYingDraft as draft
import config
import os
import sys

# 如果是Linux系统，则不导入uiautomation，并避免执行相关代码
if sys.platform.startswith('win'):
    from uiautomation import UIAutomationInitializerInThread
else:
    # 可以在这里定义一个假的UIAutomationInitializerInThread类或设置一个标记
    # 或者直接跳过，并在使用的地方做判断
    UIAutomationInitializerInThread = None
    # 或者使用其他替代方案（如果有的话）或者只是pass


def gen_video(draft_url: str) -> (str, str):
    """
    生成视频的业务逻辑
    
    Args:
        draft_url: 草稿URL
    
    Returns:
        video_url: 视频URL
        message: 响应消息，如果成功就返回"视频生成成功"，失败就返回具体错误信息
    """

    # 从URL中提取草稿ID
    draft_id = helper.get_url_param(draft_url, "draft_id")
    if not draft_id:
        return "", "无效的草稿URL"

    # 生成输出文件路径
    outfile = os.path.join(config.DRAFT_DIR, f"{helper.gen_unique_id()}.mp4")

    try:
        with UIAutomationInitializerInThread():
            logger.info("begin to export draft: %s -> %s", draft_id, outfile)

            # 此前需要将剪映打开，并位于目录页
            ctrl = draft.JianyingController()

            # 然后即可导出指定名称的草稿, 注意导出结束后视频才会被剪切(重命名)至指定位置
            ctrl.export_draft(draft_id, outfile)
        if not os.path.exists(outfile):
            # 个别版本剪映不会抛异常，但文件未生成
            raise RuntimeError("剪映导出结束但目标文件未生成，请检查磁盘空间或剪映版本")
    except Exception as exc:  # 捕获 COM/剪映/磁盘等所有异常
        logger.exception("export draft failed: draft_id=%s, error=%s", draft_id, exc)
        return "", f"导出草稿失败: {exc}"

    logger.info(f"export draft success: %s", outfile)
    return outfile, "视频生成成功"
