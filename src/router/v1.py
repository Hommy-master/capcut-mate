from email import message
from fastapi import APIRouter, Request
from src.schemas.create_draft import CreateDraftRequest, CreateDraftResponse
from src.schemas.add_videos import AddVideosRequest, AddVideosResponse
from src.schemas.save_draft import SaveDraftRequest, SaveDraftResponse
from src.schemas.gen_video import GenVideoRequest, GenVideoResponse
from src import service


router = APIRouter(prefix="/v1", tags=["v1"])

@router.post("/create_draft", response_model=CreateDraftResponse)
def create_draft(request: Request, cdr: CreateDraftRequest):
    """
    创建剪映草稿 (v1版本)
    """
    
    # 调用service层处理业务逻辑
    draft_url, message = service.create_draft(
        width=cdr.width,
        height=cdr.height
    )

    return CreateDraftResponse(message=message, draft_url=draft_url)

@router.post("/save_draft", response_model=SaveDraftResponse)
def save_draft(request: Request, sdr: SaveDraftRequest):
    """
    保存剪映草稿 (v1版本)
    """
    # 调用service层处理业务逻辑
    draft_url, message = service.save_draft(
        draft_url=sdr.draft_url,
    )

    return SaveDraftResponse(message=message, draft_url=draft_url)

@router.post("/add_videos", response_model=AddVideosResponse)
def add_videos(request: Request, avr: AddVideosRequest):
    """
    向剪映草稿添加视频 (v1版本)
    """

    # 调用service层处理业务逻辑
    draft_url, message = service.add_videos(
        draft_url=avr.draft_url,
        video_infos=avr.video_infos,
        alpha=avr.alpha,
        scale_x=avr.scale_x,
        scale_y=avr.scale_y,
        transform_x=avr.transform_x,
        transform_y=avr.transform_y
    )

    return AddVideosResponse(message=message, draft_url=draft_url)

# 生成视频 - 根据草稿URL，导出视频
@router.post("/gen_video", response_model=GenVideoResponse)
def gen_video(request: Request, gvr: GenVideoRequest):
    """
    生成视频 - 根据草稿URL，导出视频
    """

    # 调用service层处理业务逻辑
    draft_url, message = service.gen_video(
        draft_url=gvr.draft_url,
    )

    return GenVideoResponse(message=message, video_url=draft_url)

