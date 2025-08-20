from fastapi import APIRouter, Request, Depends
from src.schemas.draft import CreateDraftRequest, CreateDraftResponse
from src.service.draft_service import create_draft_service

router = APIRouter(prefix="/v1", tags=["v1"])

@router.post("/create_draft", response_model=CreateDraftResponse)
def create_draft(request: Request, draft_request: CreateDraftRequest):
    """
    创建剪映草稿 (v1版本)
    """
    # 从请求状态中获取草稿目录
    draft_dir = request.state.draft_dir

    # 调用service层处理业务逻辑
    draft_id = create_draft_service(
        draft_dir=draft_dir,
        width=draft_request.width,
        height=draft_request.height
    )

    return CreateDraftResponse(message="草稿创建成功", draft_id=draft_id)