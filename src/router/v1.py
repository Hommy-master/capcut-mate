from src.schemas.gen_video import GenVideoResponse
from src.schemas.get_draft import GetDraftResponse
from src.schemas.add_videos import AddVideosResponse
from src.schemas.add_audios import AddAudiosResponse
from src.schemas.add_images import AddImagesResponse
from src.schemas.add_sticker import AddStickerResponse
from src.schemas.add_keyframes import AddKeyframesResponse
from src.schemas.add_captions import AddCaptionsResponse
from src.schemas.add_effects import AddEffectsResponse
from src.schemas.add_masks import AddMasksResponse
from src.schemas.add_text_style import AddTextStyleResponse
from src.schemas.get_text_animations import GetTextAnimationsResponse
from src.schemas.get_image_animations import GetImageAnimationsResponse
from src.schemas.easy_create_material import EasyCreateMaterialResponse
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
from src.schemas.add_effects import AddEffectsRequest, AddEffectsResponse
from src.schemas.add_masks import AddMasksRequest, AddMasksResponse
from src.schemas.add_text_style import AddTextStyleRequest, AddTextStyleResponse
from src.schemas.get_text_animations import GetTextAnimationsRequest, GetTextAnimationsResponse
from src.schemas.get_image_animations import GetImageAnimationsRequest, GetImageAnimationsResponse
from src.schemas.easy_create_material import EasyCreateMaterialRequest, EasyCreateMaterialResponse
from src.schemas.save_draft import SaveDraftRequest, SaveDraftResponse
from src.schemas.gen_video import GenVideoRequest, GenVideoResponse
from src.schemas.gen_video_status import GenVideoStatusRequest, GenVideoStatusResponse
from src.schemas.get_draft import GetDraftRequest, GetDraftResponse
from src.schemas.get_audio_duration import GetAudioDurationRequest, GetAudioDurationResponse
from src.schemas.timelines import TimelinesRequest, TimelinesResponse
from src.schemas.audio_timelines import AudioTimelinesRequest, AudioTimelinesResponse
from src.schemas.audio_infos import AudioInfosRequest, AudioInfosResponse
from src.schemas.imgs_infos import ImgsInfosRequest, ImgsInfosResponse
from src.schemas.caption_infos import CaptionInfosRequest, CaptionInfosResponse
from src.schemas.effect_infos import EffectInfosRequest, EffectInfosResponse
from src.schemas.keyframes_infos import KeyframesInfosRequest, KeyframesInfosResponse
from src.schemas.video_infos import VideoInfosRequest, VideoInfosResponse
from src.schemas.search_sticker import SearchStickerRequest, SearchStickerResponse
from src.schemas.get_url import GetUrlRequest, GetUrlResponse
from src.schemas.str_list_to_objs import StrListToObjsRequest, StrListToObjsResponse
from src.schemas.str_to_list import StrToListRequest, StrToListResponse
from src.schemas.objs_to_str_list import ObjsToStrListRequest, ObjsToStrListResponse
from src import service
from typing import Annotated
from src.utils.logger import logger
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
    # 添加日志打印参数值
    logger.info(f"add_captions request params: {acr.model_dump_json()}")

    # 调用service层处理业务逻辑
    draft_url, track_id, text_ids, segment_ids, segment_infos = service.add_captions(
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
        style_text=acr.style_text,
        underline=acr.underline,
        italic=acr.italic,
        bold=acr.bold,
        has_shadow=acr.has_shadow,
        shadow_info=acr.shadow_info
    )

    return AddCaptionsResponse(
        draft_url=draft_url,
        track_id=track_id,
        text_ids=text_ids,
        segment_ids=segment_ids,
        segment_infos=segment_infos
    )

@router.post(path="/add_effects", response_model=AddEffectsResponse)
def add_effects(aer: AddEffectsRequest) -> AddEffectsResponse:
    """
    向剪映草稿添加特效 (v1版本)
    """

    # 调用service层处理业务逻辑
    draft_url, track_id, effect_ids, segment_ids = service.add_effects(
        draft_url=aer.draft_url,
        effect_infos=aer.effect_infos
    )

    return AddEffectsResponse(
        draft_url=draft_url,
        track_id=track_id,
        effect_ids=effect_ids,
        segment_ids=segment_ids
    )

@router.post(path="/add_masks", response_model=AddMasksResponse)
def add_masks(amr: AddMasksRequest) -> AddMasksResponse:
    """
    向剪映草稿添加遮罩 (v1版本)
    """

    # 调用service层处理业务逻辑
    draft_url, masks_added, affected_segments, mask_ids = service.add_masks(
        draft_url=amr.draft_url,
        segment_ids=amr.segment_ids,
        name=amr.name,
        X=amr.X,
        Y=amr.Y,
        width=amr.width,
        height=amr.height,
        feather=amr.feather,
        rotation=amr.rotation,
        invert=amr.invert,
        roundCorner=amr.roundCorner
    )

    return AddMasksResponse(
        draft_url=draft_url,
        masks_added=masks_added,
        affected_segments=affected_segments,
        mask_ids=mask_ids
    )

@router.post(path="/add_text_style", response_model=AddTextStyleResponse)
def add_text_style(atsr: AddTextStyleRequest) -> AddTextStyleResponse:
    """
    为文本创建富文本样式 (v1版本)
    """

    # 调用service层处理业务逻辑
    text_style = service.add_text_style(
        text=atsr.text,
        keyword=atsr.keyword,
        font_size=atsr.font_size,
        keyword_color=atsr.keyword_color,
        keyword_font_size=atsr.keyword_font_size
    )

    return AddTextStyleResponse(
        text_style=text_style
    )

@router.post(path="/easy_create_material", response_model=EasyCreateMaterialResponse)
def easy_create_material(ecmr: EasyCreateMaterialRequest) -> EasyCreateMaterialResponse:
    """
    快速创建素材轨道 (v1版本)
    """

    # 调用service层处理业务逻辑
    draft_url = service.easy_create_material(
        draft_url=ecmr.draft_url,
        audio_url=ecmr.audio_url,
        text=ecmr.text,
        img_url=ecmr.img_url,
        video_url=ecmr.video_url,
        text_color=ecmr.text_color,
        font_size=ecmr.font_size,
        text_transform_y=ecmr.text_transform_y
    )

    return EasyCreateMaterialResponse(
        draft_url=draft_url
    )

@router.post(path="/get_text_animations", response_model=GetTextAnimationsResponse)
def get_text_animations(gtar: GetTextAnimationsRequest) -> GetTextAnimationsResponse:
    """
    获取文字出入场动画 (v1版本)
    """

    # 调用service层处理业务逻辑
    effects = service.get_text_animations(
        mode=gtar.mode,
        type=gtar.type
    )

    # 直接返回对象数组，Pydantic会自动处理序列化
    return GetTextAnimationsResponse(
        effects=effects
    )

@router.post(path="/get_image_animations", response_model=GetImageAnimationsResponse)
def get_image_animations(giar: GetImageAnimationsRequest) -> GetImageAnimationsResponse:
    """
    获取图片出入场动画 (v1版本)
    """

    # 调用service层处理业务逻辑
    effects = service.get_image_animations(
        mode=giar.mode,
        type=giar.type
    )

    # 直接返回对象数组，Pydantic会自动处理序列化
    return GetImageAnimationsResponse(
        effects=effects
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
    message = service.gen_video(
        draft_url=gvr.draft_url,
    )

    return GenVideoResponse(message=message)


@router.post(path="/gen_video_status", response_model=GenVideoStatusResponse)
def gen_video_status(gvsr: GenVideoStatusRequest) -> GenVideoStatusResponse:
    """
    查询视频生成任务状态 (v1版本)
    """

    # 调用service层处理业务逻辑
    status_info = service.gen_video_status(
        draft_url=gvsr.draft_url
    )

    return GenVideoStatusResponse(**status_info)


@router.post(path="/get_audio_duration", response_model=GetAudioDurationResponse)
def get_audio_duration(gadr: GetAudioDurationRequest) -> GetAudioDurationResponse:
    """
    获取音频文件时长 (v1版本)
    """
    
    # 调用service层处理业务逻辑
    duration = service.get_audio_duration(
        mp3_url=gadr.mp3_url
    )
    
    return GetAudioDurationResponse(duration=duration)


@router.post(path="/timelines", response_model=TimelinesResponse)
def timelines(request: TimelinesRequest) -> TimelinesResponse:
    """
    创建时间线 (v1版本)
    """
    logger.info("Received request to calculate timelines")
    
    # 调用service层处理业务逻辑
    timelines, all_timelines = service.timelines(
        duration=request.duration,
        num=request.num,
        start=request.start,
        type=request.type
    )

    return TimelinesResponse(timelines=timelines, all_timelines=all_timelines)


@router.post(path="/audio_timelines", response_model=AudioTimelinesResponse)
def audio_timelines(request: AudioTimelinesRequest) -> AudioTimelinesResponse:
    """
    根据音频文件时长计算时间线 (v1版本)
    """
    logger.info("Received request to calculate audio timelines")
    
    # 调用service层处理业务逻辑
    timelines, all_timelines = service.audio_timelines(
        links=request.links
    )
    
    return AudioTimelinesResponse(timelines=timelines, all_timelines=all_timelines)


@router.post(path="/audio_infos", response_model=AudioInfosResponse)
def audio_infos(request: AudioInfosRequest) -> AudioInfosResponse:
    """
    根据音频URL和时间线生成音频信息 (v1版本)
    """
    logger.info("Received request to generate audio infos")
    
    # 调用service层处理业务逻辑
    infos_json = service.audio_infos(
        mp3_urls=request.mp3_urls,
        timelines=[{"start": t.start, "end": t.end} for t in request.timelines],
        audio_effect=request.audio_effect,
        volume=request.volume
    )
    
    return AudioInfosResponse(infos=infos_json)


@router.post(path="/imgs_infos", response_model=ImgsInfosResponse)
def imgs_infos(request: ImgsInfosRequest) -> ImgsInfosResponse:
    """
    根据图片URL和时间线生成图片信息 (v1版本)
    """
    logger.info("Received request to generate image infos")
    
    # 调用service层处理业务逻辑
    infos_json = service.imgs_infos(
        imgs=request.imgs,
        timelines=[{"start": t.start, "end": t.end} for t in request.timelines],
        height=request.height,
        width=request.width,
        in_animation=request.in_animation,
        in_animation_duration=request.in_animation_duration,
        loop_animation=request.loop_animation,
        loop_animation_duration=request.loop_animation_duration,
        out_animation=request.out_animation,
        out_animation_duration=request.out_animation_duration,
        transition=request.transition,
        transition_duration=request.transition_duration
    )
    
    return ImgsInfosResponse(infos=infos_json)


@router.post(path="/caption_infos", response_model=CaptionInfosResponse)
def caption_infos(request: CaptionInfosRequest) -> CaptionInfosResponse:
    """
    根据文本和时间线生成字幕信息 (v1版本)
    """
    logger.info("Received request to generate caption infos")
    
    # 调用service层处理业务逻辑
    infos_json = service.caption_infos(
        texts=request.texts,
        timelines=[{"start": t.start, "end": t.end} for t in request.timelines],
        font_size=request.font_size,
        keyword_color=request.keyword_color,
        keyword_font_size=request.keyword_font_size,
        keywords=request.keywords,
        in_animation=request.in_animation,
        in_animation_duration=request.in_animation_duration,
        loop_animation=request.loop_animation,
        loop_animation_duration=request.loop_animation_duration,
        out_animation=request.out_animation,
        out_animation_duration=request.out_animation_duration,
        transition=request.transition,
        transition_duration=request.transition_duration
    )
    
    return CaptionInfosResponse(infos=infos_json)


@router.post(path="/effect_infos", response_model=EffectInfosResponse)
def effect_infos(request: EffectInfosRequest) -> EffectInfosResponse:
    """
    根据特效名称和时间线生成特效信息 (v1版本)
    """
    logger.info("Received request to generate effect infos")
    
    # 调用service层处理业务逻辑
    infos_json = service.effect_infos(
        effects=request.effects,
        timelines=[{"start": t.start, "end": t.end} for t in request.timelines]
    )
    
    return EffectInfosResponse(infos=infos_json)


@router.post(path="/keyframes_infos", response_model=KeyframesInfosResponse)
def keyframes_infos(request: KeyframesInfosRequest) -> KeyframesInfosResponse:
    """
    根据关键帧类型、位置比例和值生成关键帧信息 (v1版本)
    """
    logger.info("Received request to generate keyframes infos")
    
    # 调用service层处理业务逻辑
    keyframes_json = service.keyframes_infos(
        ctype=request.ctype,
        offsets=request.offsets,
        values=request.values,
        segment_infos=[{"id": s.id, "start": s.start, "end": s.end} for s in request.segment_infos],
        height=request.height,
        width=request.width
    )
    
    return KeyframesInfosResponse(keyframes_infos=keyframes_json)


@router.post(path="/video_infos", response_model=VideoInfosResponse)
def video_infos(request: VideoInfosRequest) -> VideoInfosResponse:
    """
    根据视频URL和时间线生成视频信息 (v1版本)
    """
    logger.info("Received request to generate video infos")
    
    # 调用service层处理业务逻辑
    infos_json = service.video_infos(
        video_urls=request.video_urls,
        timelines=[{"start": t.start, "end": t.end} for t in request.timelines],
        height=request.height,
        width=request.width,
        mask=request.mask,
        transition=request.transition,
        transition_duration=request.transition_duration,
        volume=request.volume
    )
    
    return VideoInfosResponse(infos=infos_json)


@router.post(path="/search_sticker", response_model=SearchStickerResponse)
def search_sticker(ssr: SearchStickerRequest) -> SearchStickerResponse:
    """
    搜索贴纸 (v1版本)
    """
    
    # 调用service层处理业务逻辑
    data = service.search_sticker(
        keyword=ssr.keyword
    )
    
    return SearchStickerResponse(data=data)


@router.post(path="/get_url", response_model=GetUrlResponse)
def get_url(gur: GetUrlRequest) -> GetUrlResponse:
    """
    提取链接 (v1版本)
    """
    
    # 调用service层处理业务逻辑
    output = service.get_url(
        output=gur.output
    )
    
    return GetUrlResponse(output=output)


@router.post(path="/str_list_to_objs", response_model=StrListToObjsResponse)
def str_list_to_objs(slto: StrListToObjsRequest) -> StrListToObjsResponse:
    """
    字符串列表转化成对象列表 (v1版本)
    """
    
    # 调用service层处理业务逻辑
    infos = service.str_list_to_objs(
        infos=slto.infos
    )
    
    return StrListToObjsResponse(infos=infos)


@router.post(path="/str_to_list", response_model=StrToListResponse)
def str_to_list(stl: StrToListRequest) -> StrToListResponse:
    """
    字符转列表 (v1版本)
    """
    
    # 调用service层处理业务逻辑
    infos = service.str_to_list(
        obj=stl.obj
    )
    
    return StrToListResponse(infos=infos)


@router.post(path="/objs_to_str_list", response_model=ObjsToStrListResponse)
def objs_to_str_list(otl: ObjsToStrListRequest) -> ObjsToStrListResponse:
    """
    对象列表转化成字符串列表 (v1版本)
    """
    
    # 调用service层处理业务逻辑
    infos = service.objs_to_str_list(
        outputs=[obj.dict() for obj in otl.outputs]
    )
    
    return ObjsToStrListResponse(infos=infos)
