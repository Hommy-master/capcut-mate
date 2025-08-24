from fastapi import APIRouter, Request
from src.schemas.create_draft import CreateDraftRequest, CreateDraftResponse
from src.schemas.add_videos import AddVideosRequest, AddVideosResponse
from src import service
from src.constants.base import DRAFT_DIR


router = APIRouter(prefix="/v1", tags=["v1"])

@router.post("/create_draft", response_model=CreateDraftResponse)
def create_draft(request: Request, cdr: CreateDraftRequest):
    """
    创建剪映草稿 (v1版本)
    """
    
    # 调用service层处理业务逻辑
    draft_url = service.create_draft_service(
        width=cdr.width,
        height=cdr.height
    )

    return CreateDraftResponse(message="草稿创建成功", draft_url=draft_url)

@router.post("/add_videos", response_model=AddVideosResponse)
def add_videos(request: Request, avr: AddVideosRequest):
    """
    向剪映草稿添加视频 (v1版本)
    """

    # 调用service层处理业务逻辑
    draft_url = service.add_videos_service(
        draft_url=avr.draft_url,
        video_infos=avr.video_infos,
        alpha=avr.alpha,
        scale_x=avr.scale_x,
        scale_y=avr.scale_y,
        transform_x=avr.transform_x,
        transform_y=avr.transform_y
    )

    return AddVideosResponse(message="视频添加成功", draft_url=draft_url)
