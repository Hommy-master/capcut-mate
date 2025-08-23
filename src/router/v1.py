from fastapi import APIRouter, Request
from src.schemas.create_draft import CreateDraftRequest, CreateDraftResponse
from src.schemas.add_videos import AddVideosRequest, AddVideosResponse
from src.service.create_draft_service import create_draft_service
from src.service.add_videos_service import add_videos_service

router = APIRouter(prefix="/v1", tags=["v1"])

@router.post("/create_draft", response_model=CreateDraftResponse)
def create_draft(request: Request, cdr: CreateDraftRequest):
    """
    创建剪映草稿 (v1版本)
    """
    
    # 调用service层处理业务逻辑
    draft_id = create_draft_service(
        width=cdr.width,
        height=cdr.height
    )

    return CreateDraftResponse(message="草稿创建成功", draft_id=draft_id)

import json
from fastapi import HTTPException

@router.post("/add_videos", response_model=AddVideosResponse)
def add_videos(request: Request, avr: AddVideosRequest):
    """
    向剪映草稿添加视频 (v1版本)
    """

    # 将JSON字符串转换为字典
    try:
        video_infos = json.loads(avr.video_infos) if avr.video_infos else {}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="video_infos格式不正确，应为有效的JSON字符串")

    # 调用service层处理业务逻辑
    result = add_videos_service(
        draft_url=avr.draft_url,
        video_infos=video_infos,
        alpha=avr.alpha,
        scale_x=avr.scale_x,
        scale_y=avr.scale_y,
        transform_x=avr.transform_x,
        transform_y=avr.transform_y
    )

    # 假设result是包含draft_url的字典
    return AddVideosResponse(message="视频添加成功", draft_url=result.get("data", {}).get("draft_url", ""))
