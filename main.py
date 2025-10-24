from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn

import pyJianYingDraft as draft
from pyJianYingDraft.metadata.animation_meta import Intro_type, Outro_type, Group_animation_type
from pyJianYingDraft.metadata.capcut_animation_meta import CapCut_Intro_type, CapCut_Outro_type, CapCut_Group_animation_type
from pyJianYingDraft.metadata.transition_meta import Transition_type
from pyJianYingDraft.metadata.capcut_transition_meta import CapCut_Transition_type
from pyJianYingDraft.metadata.mask_meta import Mask_type
from pyJianYingDraft.metadata.capcut_mask_meta import CapCut_Mask_type
from pyJianYingDraft.metadata.audio_effect_meta import Tone_effect_type, Audio_scene_effect_type, Speech_to_song_type
from pyJianYingDraft.metadata.capcut_audio_effect_meta import CapCut_Voice_filters_effect_type, CapCut_Voice_characters_effect_type, CapCut_Speech_to_song_effect_type
from pyJianYingDraft.metadata.font_meta import Font_type
from pyJianYingDraft.metadata.animation_meta import Text_intro, Text_outro, Text_loop_anim
from pyJianYingDraft.metadata.capcut_text_animation_meta import CapCut_Text_intro, CapCut_Text_outro, CapCut_Text_loop_anim
from pyJianYingDraft.metadata.video_effect_meta import Video_scene_effect_type, Video_character_effect_type
from pyJianYingDraft.metadata.capcut_effect_meta import CapCut_Video_scene_effect_type, CapCut_Video_character_effect_type

from add_audio_track import add_audio_track
from add_video_track import add_video_track
from add_text_impl import add_text_impl
from add_subtitle_impl import add_subtitle_impl
from add_image_impl import add_image_impl
from add_video_keyframe_impl import add_video_keyframe_impl
from save_draft_impl import save_draft_impl, query_task_status, query_script_impl
from add_effect_impl import add_effect_impl
from add_sticker_impl import add_sticker_impl
from create_draft import create_draft
from util import generate_draft_url as utilgenerate_draft_url, hex_to_rgb
from pyJianYingDraft.text_segment import TextStyleRange, Text_style, Text_border
from settings.local import IS_CAPCUT_ENV, DRAFT_DOMAIN, PREVIEW_ROUTER, PORT

# 请求模型定义在 schemas 中
from schemas import (
    AddVideoRequest, AddAudioRequest, CreateDraftRequest, AddSubtitleRequest,
    AddTextRequest, AddImageRequest, AddVideoKeyframeRequest, AddEffectRequest,
    QueryScriptRequest, SaveDraftRequest, QueryDraftStatusRequest,
    GenerateDraftURLRequest, AddStickerRequest
)

# 创建 FastAPI 应用
app = FastAPI(
    title="CapCut Mate API",
    description="剪映辅助工具 API - 支持视频、音频、文字、图片等素材编辑",
    version="2.0.0",
    docs_url="/apidocs",
    redoc_url="/redoc"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Pydantic 模型定义 ====================
# 统一响应模型
class StandardResponse(BaseModel):
    success: bool = Field(description="请求是否成功")
    output: Any = Field(default="", description="返回数据")
    error: str = Field(default="", description="错误信息")

# ==================== API 路由 ====================

@app.post("/add_video", response_model=StandardResponse, tags=["媒体素材"])
async def add_video_endpoint(request: AddVideoRequest):
    """添加视频到草稿"""
    try:
        draft_result = add_video_track(
            draft_folder=request.draft_folder, video_url=request.video_url, width=request.width,
            height=request.height, start=request.start, end=request.end, target_start=request.target_start,
            draft_id=request.draft_id, transform_y=request.transform_y, scale_x=request.scale_x,
            scale_y=request.scale_y, transform_x=request.transform_x, speed=request.speed,
            track_name=request.track_name, relative_index=request.relative_index, duration=request.duration,
            transition=request.transition, transition_duration=request.transition_duration, volume=request.volume,
            mask_type=request.mask_type, mask_center_x=request.mask_center_x, mask_center_y=request.mask_center_y,
            mask_size=request.mask_size, mask_rotation=request.mask_rotation, mask_feather=request.mask_feather,
            mask_invert=request.mask_invert, mask_rect_width=request.mask_rect_width,
            mask_round_corner=request.mask_round_corner, background_blur=request.background_blur
        )
        return StandardResponse(success=True, output=draft_result)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred while processing video: {str(e)}.")

@app.post("/add_audio", response_model=StandardResponse, tags=["媒体素材"])
async def add_audio_endpoint(request: AddAudioRequest):
    """添加音频到草稿"""
    try:
        sound_effects = [(request.effect_type, request.effect_params)] if request.effect_type else None
        draft_result = add_audio_track(
            draft_folder=request.draft_folder, audio_url=request.audio_url, start=request.start,
            end=request.end, target_start=request.target_start, draft_id=request.draft_id,
            volume=request.volume, track_name=request.track_name, speed=request.speed,
            sound_effects=sound_effects, width=request.width, height=request.height, duration=request.duration
        )
        return StandardResponse(success=True, output=draft_result)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred while processing audio: {str(e)}.")

@app.post("/create_draft", response_model=StandardResponse, tags=["草稿管理"])
async def create_draft_endpoint(request: CreateDraftRequest):
    """创建新草稿"""
    try:
        script, draft_id = create_draft(width=request.width, height=request.height)
        return StandardResponse(success=True, output={"draft_id": draft_id, "draft_url": utilgenerate_draft_url(draft_id)})
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred while creating draft: {str(e)}.")

@app.post("/add_subtitle", response_model=StandardResponse, tags=["媒体素材"])
async def add_subtitle_endpoint(request: AddSubtitleRequest):
    """添加字幕到草稿"""
    try:
        draft_result = add_subtitle_impl(
            srt_path=request.srt, draft_id=request.draft_id, track_name=request.track_name,  # type: ignore
            time_offset=request.time_offset, font=request.font, font_size=request.font_size,
            bold=request.bold, italic=request.italic, underline=request.underline,
            font_color=request.font_color, vertical=request.vertical, alpha=request.alpha,
            border_alpha=request.border_alpha, border_color=request.border_color,
            border_width=request.border_width, background_color=request.background_color,
            background_style=request.background_style, background_alpha=request.background_alpha,
            transform_x=request.transform_x, transform_y=request.transform_y,
            scale_x=request.scale_x, scale_y=request.scale_y, rotation=request.rotation,
            width=request.width, height=request.height
        )
        return StandardResponse(success=True, output=draft_result)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred while processing subtitle: {str(e)}.")

@app.post("/add_text", response_model=StandardResponse, tags=["媒体素材"])
async def add_text_endpoint(request: AddTextRequest):
    """添加文字到草稿"""
    try:
        font_color = request.color if request.color else request.font_color
        font_size = request.size if request.size else request.font_size
        font_alpha = request.alpha if request.alpha is not None else request.font_alpha

        text_styles = None
        if request.text_styles:
            text_styles = []
            for style_data in request.text_styles:
                style_dict = style_data.style or {}
                style = Text_style(
                    size=style_dict.get('size', font_size), bold=style_dict.get('bold', False),
                    italic=style_dict.get('italic', False), underline=style_dict.get('underline', False),
                    color=hex_to_rgb(style_dict.get('color', font_color)), alpha=style_dict.get('alpha', font_alpha),
                    align=style_dict.get('align', 1), vertical=style_dict.get('vertical', request.vertical),
                    letter_spacing=style_dict.get('letter_spacing', 0), line_spacing=style_dict.get('line_spacing', 0)
                )
                border = None
                border_dict = style_data.border or {}
                if border_dict.get('width', 0) > 0:
                    border = Text_border(
                        alpha=border_dict.get('alpha', request.border_alpha),
                        color=hex_to_rgb(border_dict.get('color', request.border_color)),
                        width=border_dict.get('width', request.border_width)
                    )
                style_range = TextStyleRange(
                    start=style_data.start, end=style_data.end, style=style,
                    border=border, font_str=style_data.font or request.font
                )
                text_styles.append(style_range)

        draft_result = add_text_impl(
            text=request.text, start=request.start, end=request.end, draft_id=request.draft_id,
            transform_y=request.transform_y, transform_x=request.transform_x, font=request.font,
            font_color=font_color, font_size=font_size, track_name=request.track_name,
            vertical=request.vertical, font_alpha=font_alpha, border_alpha=request.border_alpha,
            border_color=request.border_color, border_width=request.border_width,
            background_color=request.background_color, background_style=request.background_style,
            background_alpha=request.background_alpha, background_round_radius=request.background_round_radius,
            background_height=request.background_height, background_width=request.background_width,
            background_horizontal_offset=request.background_horizontal_offset,
            background_vertical_offset=request.background_vertical_offset,
            shadow_enabled=request.shadow_enabled, shadow_alpha=request.shadow_alpha,
            shadow_angle=request.shadow_angle, shadow_color=request.shadow_color,
            shadow_distance=request.shadow_distance, shadow_smoothing=request.shadow_smoothing,
            bubble_effect_id=request.bubble_effect_id, bubble_resource_id=request.bubble_resource_id,
            effect_effect_id=request.effect_effect_id, intro_animation=request.intro_animation,
            intro_duration=request.intro_duration, outro_animation=request.outro_animation,
            outro_duration=request.outro_duration, width=request.width, height=request.height,
            fixed_width=request.fixed_width, fixed_height=request.fixed_height, text_styles=text_styles
        )
        return StandardResponse(success=True, output=draft_result)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred while processing text: {str(e)}.")

@app.post("/add_image", response_model=StandardResponse, tags=["媒体素材"])
async def add_image_endpoint(request: AddImageRequest):
    """添加图片到草稿"""
    try:
        draft_result = add_image_impl(
            draft_folder=request.draft_folder, image_url=request.image_url, width=request.width,
            height=request.height, start=request.start, end=request.end, draft_id=request.draft_id,
            transform_y=request.transform_y, scale_x=request.scale_x, scale_y=request.scale_y,
            transform_x=request.transform_x, track_name=request.track_name, relative_index=request.relative_index,
            animation=request.animation, animation_duration=request.animation_duration,
            intro_animation=request.intro_animation, intro_animation_duration=request.intro_animation_duration,
            outro_animation=request.outro_animation, outro_animation_duration=request.outro_animation_duration,
            combo_animation=request.combo_animation, combo_animation_duration=request.combo_animation_duration,
            transition=request.transition, transition_duration=request.transition_duration,
            mask_type=request.mask_type, mask_center_x=request.mask_center_x, mask_center_y=request.mask_center_y,
            mask_size=request.mask_size, mask_rotation=request.mask_rotation, mask_feather=request.mask_feather,
            mask_invert=request.mask_invert, mask_rect_width=request.mask_rect_width,
            mask_round_corner=request.mask_round_corner, background_blur=request.background_blur
        )
        return StandardResponse(success=True, output=draft_result)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred while processing image: {str(e)}.")

@app.post("/add_video_keyframe", response_model=StandardResponse, tags=["特效和动画"])
async def add_video_keyframe_endpoint(request: AddVideoKeyframeRequest):
    """添加视频关键帧"""
    try:
        draft_result = add_video_keyframe_impl(
            draft_id=request.draft_id, track_name=request.track_name, property_type=request.property_type,
            time=request.time, value=request.value, property_types=request.property_types,
            times=request.times, values=request.values
        )
        return StandardResponse(success=True, output=draft_result)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred while adding keyframe: {str(e)}.")

@app.post("/add_effect", response_model=StandardResponse, tags=["特效和动画"])
async def add_effect_endpoint(request: AddEffectRequest):
    """添加特效"""
    try:
        # 验证 effect_category 参数
        if request.effect_category not in ["scene", "character"]:
            return StandardResponse(success=False, error="effect_category must be 'scene' or 'character'")
        
        draft_result = add_effect_impl(
            effect_type=request.effect_type, effect_category=request.effect_category,  # type: ignore
            start=request.start, end=request.end, draft_id=request.draft_id, 
            track_name=request.track_name, params=request.params, 
            width=request.width, height=request.height
        )
        return StandardResponse(success=True, output=draft_result)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred while adding effect: {str(e)}.")

@app.post("/query_script", response_model=StandardResponse, tags=["草稿管理"])
async def query_script_endpoint(request: QueryScriptRequest):
    """查询草稿脚本"""
    try:
        script = query_script_impl(draft_id=request.draft_id, force_update=request.force_update)
        if script is None:
            return StandardResponse(success=False, error=f"Draft {request.draft_id} does not exist in cache.")
        return StandardResponse(success=True, output=script.dumps())
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred while querying script: {str(e)}.")

@app.post("/save_draft", response_model=StandardResponse, tags=["草稿管理"])
async def save_draft_endpoint(request: SaveDraftRequest):
    """保存草稿"""
    try:
        draft_result = save_draft_impl(request.draft_id, request.draft_folder)  # type: ignore
        return StandardResponse(success=True, output=draft_result)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred while saving draft: {str(e)}.")

@app.post("/query_draft_status", response_model=StandardResponse, tags=["任务查询"])
async def query_draft_status_endpoint(request: QueryDraftStatusRequest):
    """查询草稿保存状态"""
    try:
        task_status = query_task_status(request.task_id)
        if task_status["status"] == "not_found":
            return StandardResponse(success=False, error=f"Task with ID {request.task_id} not found.")
        return StandardResponse(success=True, output=task_status)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred while querying task status: {str(e)}.")

@app.post("/generate_draft_url", response_model=StandardResponse, tags=["草稿管理"])
async def generate_draft_url_endpoint(request: GenerateDraftURLRequest):
    """生成草稿预览 URL"""
    try:
        draft_result = {"draft_url": f"{DRAFT_DOMAIN}{PREVIEW_ROUTER}?={request.draft_id}"}
        return StandardResponse(success=True, output=draft_result)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred while generating draft URL: {str(e)}.")

@app.post("/add_sticker", response_model=StandardResponse, tags=["媒体素材"])
async def add_sticker_endpoint(request: AddStickerRequest):
    """添加贴纸"""
    try:
        draft_result = add_sticker_impl(
            resource_id=request.sticker_id, start=request.start, end=request.end,
            draft_id=request.draft_id, transform_y=request.transform_y, transform_x=request.transform_x,  # type: ignore
            alpha=request.alpha, flip_horizontal=request.flip_horizontal, flip_vertical=request.flip_vertical,
            rotation=request.rotation, scale_x=request.scale_x, scale_y=request.scale_y,
            track_name=request.track_name, relative_index=request.relative_index,
            width=request.width, height=request.height
        )
        return StandardResponse(success=True, output=draft_result)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred while adding sticker: {str(e)}.")

# ==================== 资源查询接口 ====================

@app.get("/get_intro_animation_types", response_model=StandardResponse, tags=["资源查询"])
async def get_intro_animation_types():
    """获取入场动画类型列表"""
    try:
        animation_types = []
        enum_type = CapCut_Intro_type if IS_CAPCUT_ENV else Intro_type
        for name, member in enum_type.__members__.items():
            animation_types.append({"name": name})
        return StandardResponse(success=True, output=animation_types)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred: {str(e)}")

@app.get("/get_outro_animation_types", response_model=StandardResponse, tags=["资源查询"])
async def get_outro_animation_types():
    """获取出场动画类型列表"""
    try:
        animation_types = []
        enum_type = CapCut_Outro_type if IS_CAPCUT_ENV else Outro_type
        for name, member in enum_type.__members__.items():
            animation_types.append({"name": name})
        return StandardResponse(success=True, output=animation_types)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred: {str(e)}")

@app.get("/get_combo_animation_types", response_model=StandardResponse, tags=["资源查询"])
async def get_combo_animation_types():
    """获取组合动画类型列表"""
    try:
        animation_types = []
        enum_type = CapCut_Group_animation_type if IS_CAPCUT_ENV else Group_animation_type
        for name, member in enum_type.__members__.items():
            animation_types.append({"name": name})
        return StandardResponse(success=True, output=animation_types)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred: {str(e)}")

@app.get("/get_transition_types", response_model=StandardResponse, tags=["资源查询"])
async def get_transition_types():
    """获取转场类型列表"""
    try:
        transition_types = []
        enum_type = CapCut_Transition_type if IS_CAPCUT_ENV else Transition_type
        for name, member in enum_type.__members__.items():
            transition_types.append({"name": name})
        return StandardResponse(success=True, output=transition_types)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred: {str(e)}")

@app.get("/get_mask_types", response_model=StandardResponse, tags=["资源查询"])
async def get_mask_types():
    """获取蒙版类型列表"""
    try:
        mask_types = []
        enum_type = CapCut_Mask_type if IS_CAPCUT_ENV else Mask_type
        for name, member in enum_type.__members__.items():
            mask_types.append({"name": name})
        return StandardResponse(success=True, output=mask_types)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred: {str(e)}")

@app.get("/get_audio_effect_types", response_model=StandardResponse, tags=["资源查询"])
async def get_audio_effect_types():
    """获取音效类型列表"""
    try:
        effect_types = []
        if IS_CAPCUT_ENV:
            for name, member in CapCut_Voice_filters_effect_type.__members__.items():
                effect_types.append({"name": name, "type": "voice_filter"})
            for name, member in CapCut_Voice_characters_effect_type.__members__.items():
                effect_types.append({"name": name, "type": "voice_character"})
        else:
            for name, member in Tone_effect_type.__members__.items():
                effect_types.append({"name": name, "type": "tone"})
            for name, member in Audio_scene_effect_type.__members__.items():
                effect_types.append({"name": name, "type": "scene"})
        return StandardResponse(success=True, output=effect_types)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred: {str(e)}")

@app.get("/get_font_types", response_model=StandardResponse, tags=["资源查询"])
async def get_font_types():
    """获取字体类型列表"""
    try:
        font_types = [{"name": name} for name, member in Font_type.__members__.items()]
        return StandardResponse(success=True, output=font_types)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred: {str(e)}")

@app.get("/get_text_intro_types", response_model=StandardResponse, tags=["资源查询"])
async def get_text_intro_types():
    """获取文字入场动画类型列表"""
    try:
        animation_types = []
        enum_type = CapCut_Text_intro if IS_CAPCUT_ENV else Text_intro
        for name, member in enum_type.__members__.items():
            animation_types.append({"name": name})
        return StandardResponse(success=True, output=animation_types)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred: {str(e)}")

@app.get("/get_text_outro_types", response_model=StandardResponse, tags=["资源查询"])
async def get_text_outro_types():
    """获取文字出场动画类型列表"""
    try:
        animation_types = []
        enum_type = CapCut_Text_outro if IS_CAPCUT_ENV else Text_outro
        for name, member in enum_type.__members__.items():
            animation_types.append({"name": name})
        return StandardResponse(success=True, output=animation_types)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred: {str(e)}")

@app.get("/get_text_loop_anim_types", response_model=StandardResponse, tags=["资源查询"])
async def get_text_loop_anim_types():
    """获取文字循环动画类型列表"""
    try:
        animation_types = []
        enum_type = CapCut_Text_loop_anim if IS_CAPCUT_ENV else Text_loop_anim
        for name, member in enum_type.__members__.items():
            animation_types.append({"name": name})
        return StandardResponse(success=True, output=animation_types)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred: {str(e)}")

@app.get("/get_video_scene_effect_types", response_model=StandardResponse, tags=["资源查询"])
async def get_video_scene_effect_types():
    """获取场景特效类型列表"""
    try:
        effect_types = []
        enum_type = CapCut_Video_scene_effect_type if IS_CAPCUT_ENV else Video_scene_effect_type
        for name, member in enum_type.__members__.items():
            effect_types.append({"name": name})
        return StandardResponse(success=True, output=effect_types)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred: {str(e)}")

@app.get("/get_video_character_effect_types", response_model=StandardResponse, tags=["资源查询"])
async def get_video_character_effect_types():
    """获取人物特效类型列表"""
    try:
        effect_types = []
        enum_type = CapCut_Video_character_effect_type if IS_CAPCUT_ENV else Video_character_effect_type
        for name, member in enum_type.__members__.items():
            effect_types.append({"name": name})
        return StandardResponse(success=True, output=effect_types)
    except Exception as e:
        return StandardResponse(success=False, error=f"Error occurred: {str(e)}")

# ==================== 启动事件 ====================

@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    print("\n" + "=" * 80)
    print("📋 已注册的路由信息 / Registered Routes:")
    print("=" * 80)
    
    routes_info = []
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            methods = ','.join(sorted(route.methods - {'HEAD', 'OPTIONS'})) if route.methods else 'N/A'
            routes_info.append({
                'endpoint': route.name,
                'methods': methods,
                'path': route.path
            })
    
    routes_info.sort(key=lambda x: x['path'])
    
    print(f"\n{'序号':<6} {'方法':<12} {'路径':<40} {'端点'}")
    print("-" * 80)
    
    for idx, route in enumerate(routes_info, 1):
        print(f"{idx:<6} {route['methods']:<12} {route['path']:<40} {route['endpoint']}")
    
    print("\n" + "=" * 80)
    print(f"✅ 总计: {len(routes_info)} 个路由")
    print(f"🚀 服务启动于: http://0.0.0.0:{PORT}")
    print(f"📖 API 文档: http://0.0.0.0:{PORT}/apidocs")
    print("=" * 80 + "\n")

# ==================== 主程序入口 ====================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=False,
        log_level="info"
    )
