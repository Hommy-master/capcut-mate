"""视频美颜（figure）元数据。

强度在剪映界面是 0~100，写入草稿时为 0~1。
美白、磨皮把强度写在顶层 value；白牙写在 adjust_params。
"""

from dataclasses import dataclass
from enum import Enum
from typing import Literal, Optional


@dataclass(frozen=True)
class BeautyMeta:
    """单个美颜滑杆的资源定义。"""

    name: str
    resource_id: str
    sub_type: str
    """figure 的 sub_type：美白为 none，磨皮/白牙为 auto_beauty。"""
    intensity_mode: Literal["value", "adjust_param"]
    """强度落点：value 写顶层 value；adjust_param 写 adjust_params。"""
    needs_algorithm_path: bool
    material_type: str = "figure"
    category_id: str = "auto-beauty2"
    adjust_param_name: str = "1"


class BeautyType(Enum):
    """已从剪映草稿核对过的美颜滑杆。"""

    美白 = BeautyMeta(
        "美白",
        "6998408303826965006",
        "none",
        "value",
        False,
    )
    磨皮 = BeautyMeta(
        "磨皮",
        "6976822940608238093",
        "auto_beauty",
        "value",
        True,
    )
    白牙 = BeautyMeta(
        "白牙",
        "6998408263892996639",
        "auto_beauty",
        "adjust_param",
        True,
    )


MAKEUP_ROOT = BeautyMeta(
    "makeup-root",
    "7273096354098844221",
    "auto_beauty",
    "value",
    True,
    material_type="makeup_root",
    category_id="",
)
"""美颜伴随素材。任意滑杆生效时每个片段补一条，强度固定为 0。"""


def find_beauty_type(name: str) -> Optional[BeautyType]:
    """按剪映显示名查找美颜类型。"""
    for item in BeautyType:
        if item.value.name == name:
            return item
    return None


def build_figure_algorithm_path(placeholder_id: str, video_material_id: str) -> str:
    """磨皮、白牙、makeup-root 共用的算法产物路径。

    后缀是视频素材 id，不是随机目录。同一草稿的 placeholder 保持不变。
    """
    return (
        f"##_draftpath_placeholder_{placeholder_id}_##"
        f"/video/figure_algorithm/{video_material_id}"
    )
