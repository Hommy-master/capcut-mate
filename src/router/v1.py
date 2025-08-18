from fastapi import APIRouter, Request
import pyJianYingDraft as draft
from src.utils.logger import logger
import uuid

router = APIRouter(prefix="/v1", tags=["v1"])

@router.post("/create_draft")
def create_draft(request: Request, height: int = 1080, width: int = 1920):
    """
    创建剪映草稿 (v1版本)
    """
    # 从请求状态中获取草稿目录
    draft_dir = request.state.draft_dir
    logger.info("current draft dir: %s", draft_dir)

    # 生成一个UUID
    draft_id = uuid.uuid4()
    logger.info("current draft id: %s", draft_id)

    # 初始化草稿文件夹
    draft_folder = draft.DraftFolder(draft_dir)
    # 创建新草稿
    script = draft_folder.create_draft(str(draft_id), width, height)
    # 保存草稿
    script.save()

    return {"message": "草稿创建成功", "draft_id": str(draft_id)}