from fastapi import APIRouter
import pyJianYingDraft as draft
from src import constants

router = APIRouter()

@router.get("/create_draft")
def create_draft(height: int = 1080, width: int = 1920):
    """
    创建剪映草稿
    """
    # 初始化草稿文件夹
    draft_folder = draft.DraftFolder(constants.DRAFT_DIR)
    # 创建新草稿
    script = draft_folder.create_draft("我的草稿", width, height)
    # 保存草稿
    script.save()

    # 添加音频轨道
    return {"message": "草稿创建成功"}
