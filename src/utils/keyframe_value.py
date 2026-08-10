"""关键帧属性值的归一化工具（与 pyJianYingDraft / keyframes_infos 约定一致）。"""

POSITION_X = "KFTypePositionX"
POSITION_Y = "KFTypePositionY"

# |value| <= 1 视为已归一化（剪映半画布单位）；> 1 视为像素位移（与 transform_x 一致）
_NORMALIZED_POSITION_MAX = 1.0


def normalize_keyframe_value(
    ctype: str,
    value: float,
    width: int | None = None,
    height: int | None = None,
    *,
    assume_pixel: bool = False,
) -> float:
    """
    将关键帧属性值转换为剪映草稿内部单位。

    位置类关键帧（KFTypePositionX/Y）在剪映中为「UI 显示像素值 / 画布宽(高)」，
    与 add_videos/add_images 中 transform_x / draft_width 的换算一致。

    Args:
        assume_pixel: True 时只要提供了 width/height 就按像素换算（keyframes_infos）；
            False 时仅当 |value| > 1 时按像素换算（add_keyframes，兼容已归一化的 -1~1）。
    """
    if ctype == POSITION_X and width is not None and width > 0:
        if assume_pixel or abs(value) > _NORMALIZED_POSITION_MAX:
            return value / width
    elif ctype == POSITION_Y and height is not None and height > 0:
        if assume_pixel or abs(value) > _NORMALIZED_POSITION_MAX:
            return value / height
    return value
