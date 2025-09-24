from src.schemas.gen_video import GenVideoResponse
from src.schemas.get_draft import GetDraftResponse
from src.schemas.add_videos import AddVideosResponse
from src.schemas.add_audios import AddAudiosResponse
from src.schemas.add_images import AddImagesResponse
from src.schemas.add_sticker import AddStickerResponse
from src.schemas.add_keyframes import AddKeyframesResponse
from src.schemas.add_captions import AddCaptionsResponse
from src.schemas.save_draft import SaveDraftResponse
from src.schemas.create_draft import CreateDraftResponse
from fastapi import APIRouter, Request, Depends
from src.schemas.create_draft import CreateDraftRequest, CreateDraftResponse
from src.schemas.add_videos import AddVideosRequest, AddVideosResponse
from src.schemas.add_audios import AddAudiosRequest, AddAudiosResponse
from src.schemas.add_images import AddImagesRequest, AddImagesResponse
from src.schemas.add_sticker import AddStickerRequest, AddStickerResponse
from src.schemas.add_keyframes import AddKeyframesRequest, AddKeyframesResponse
from src.schemas.add_captions import AddCaptionsRequest, AddCaptionsResponse
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

@router.post(path="/add_images", response_model=AddImagesResponse)
def add_images(air: AddImagesRequest) -> AddImagesResponse:
    """
    向剪映草稿批量添加图片 (v1版本)
    """

    # 调用service层处理业务逻辑
    draft_url, track_id, image_ids, segment_ids, segment_infos = service.add_images(
        draft_url=air.draft_url,
        image_infos=air.image_infos,
        alpha=air.alpha,
        scale_x=air.scale_x,
        scale_y=air.scale_y,
        transform_x=air.transform_x,
        transform_y=air.transform_y
    )

    return AddImagesResponse(
        draft_url=draft_url, 
        track_id=track_id, 
        image_ids=image_ids, 
        segment_ids=segment_ids, 
        segment_infos=segment_infos
    )

@router.post(path="/add_sticker", response_model=AddStickerResponse)
def add_sticker(asr: AddStickerRequest) -> AddStickerResponse:
    """
    向剪映草稿添加贴纸 (v1版本)
    """

    # 调用service层处理业务逻辑
    draft_url, sticker_id, track_id, segment_id, duration = service.add_sticker(
        draft_url=asr.draft_url,
        sticker_id=asr.sticker_id,
        start=asr.start,
        end=asr.end,
        scale=asr.scale,
        transform_x=asr.transform_x,
        transform_y=asr.transform_y
    )

    return AddStickerResponse(
        draft_url=draft_url,
        sticker_id=sticker_id,
        track_id=track_id,
        segment_id=segment_id,
        duration=duration
    )

@router.post(path="/add_keyframes", response_model=AddKeyframesResponse)
def add_keyframes(akr: AddKeyframesRequest) -> AddKeyframesResponse:
    """
    向剪映草稿添加关键帧 (v1版本)
    """

    # 调用service层处理业务逻辑
    draft_url, keyframes_added, affected_segments = service.add_keyframes(
        draft_url=akr.draft_url,
        keyframes=akr.keyframes
    )

    return AddKeyframesResponse(
        draft_url=draft_url,
        keyframes_added=keyframes_added,
        affected_segments=affected_segments
    )

@router.post(path="/add_captions", response_model=AddCaptionsResponse)
def add_captions(acr: AddCaptionsRequest) -> AddCaptionsResponse:
    """
    向剪映草稿批量添加字幕 (v1版本)
    """

    # 调用service层处理业务逻辑
    draft_url, track_id, text_ids, segment_ids = service.add_captions(
        draft_url=acr.draft_url,
        captions=acr.captions,
        text_color=acr.text_color,
        border_color=acr.border_color,
        alignment=acr.alignment,
        alpha=acr.alpha,
        font=acr.font,
        font_size=acr.font_size,
        letter_spacing=acr.letter_spacing,
        line_spacing=acr.line_spacing,
        scale_x=acr.scale_x,
        scale_y=acr.scale_y,
        transform_x=acr.transform_x,
        transform_y=acr.transform_y,
        style_text=acr.style_text
    )

    return AddCaptionsResponse(
        draft_url=draft_url,
        track_id=track_id,
        text_ids=text_ids,
        segment_ids=segment_ids
    )

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

