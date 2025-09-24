from src.schemas.gen_video import GenVideoResponse
from src.schemas.get_draft import GetDraftResponse
from src.schemas.add_videos import AddVideosResponse
from src.schemas.add_audios import AddAudiosResponse
from src.schemas.save_draft import SaveDraftResponse
from src.schemas.create_draft import CreateDraftResponse
from fastapi import APIRouter, Request, Depends
from src.schemas.create_draft import CreateDraftRequest, CreateDraftResponse
from src.schemas.add_videos import AddVideosRequest, AddVideosResponse
from src.schemas.add_audios import AddAudiosRequest, AddAudiosResponse
from src.schemas.save_draft import SaveDraftRequest, SaveDraftResponse
from src.schemas.gen_video import GenVideoRequest, GenVideoResponse
from src.schemas.get_draft import GetDraftRequest, GetDraftResponse
from src import service
from typing import Annotated
import config


router = APIRouter(prefix="/v1", tags=["v1"])

@router.post(path="/create_draft", response_model=CreateDraftResponse)
def create_draft(cdr: CreateDraftRequest) -> CreateDraftResponse:
    """
    创建剪映草稿 (v1版本)
    """
    
    # 调用service层处理业务逻辑
    draft_url = service.create_draft(
        width=cdr.width,
        height=cdr.height
    )

    return CreateDraftResponse(draft_url=draft_url, tip_url=config.TIP_URL)

@router.post(path="/save_draft", response_model=SaveDraftResponse)
def save_draft(sdr: SaveDraftRequest) -> SaveDraftResponse:
    """
    保存剪映草稿 (v1版本)
    """
    # 调用service层处理业务逻辑
    draft_url = service.save_draft(
        draft_url=sdr.draft_url,
    )

    return SaveDraftResponse(draft_url=draft_url)

@router.post(path="/add_videos", response_model=AddVideosResponse)
def add_videos(avr: AddVideosRequest) -> AddVideosResponse:
    """
    向剪映草稿添加视频 (v1版本)
    """

    # 调用service层处理业务逻辑
    draft_url, track_id, video_ids, segment_ids = service.add_videos(
        draft_url=avr.draft_url,
        video_infos=avr.video_infos,
        alpha=avr.alpha,
        scale_x=avr.scale_x,
        scale_y=avr.scale_y,
        transform_x=avr.transform_x,
        transform_y=avr.transform_y
    )

    return AddVideosResponse(draft_url=draft_url, track_id=track_id, video_ids=video_ids, segment_ids=segment_ids)

@router.post(path="/add_audios", response_model=AddAudiosResponse)
def add_audios(aar: AddAudiosRequest) -> AddAudiosResponse:
    """
    向剪映草稿批量添加音频 (v1版本)
    """

    # 调用service层处理业务逻辑
    draft_url, track_id, audio_ids = service.add_audios(
        draft_url=aar.draft_url,
        audio_infos=aar.audio_infos
    )

    return AddAudiosResponse(draft_url=draft_url, track_id=track_id, audio_ids=audio_ids)

@router.get(path="/get_draft", response_model=GetDraftResponse)
def get_draft(params: Annotated[GetDraftRequest, Depends()]) -> GetDraftResponse:
    """
    获取草稿 - 获取所有文件列表
    """

    # 调用service层处理业务逻辑
    files = service.get_draft(
        draft_id=params.draft_id,
    )

    return GetDraftResponse(files=files)

# 生成视频 - 根据草稿URL，导出视频
@router.post(path="/gen_video", response_model=GenVideoResponse)
def gen_video(request: Request, gvr: GenVideoRequest) -> GenVideoResponse:
    """
    生成视频 - 根据草稿URL，导出视频
    """

    # 调用service层处理业务逻辑
    draft_url, message = service.gen_video(
        draft_url=gvr.draft_url,
    )

    return GenVideoResponse(message=message, video_url=draft_url)

