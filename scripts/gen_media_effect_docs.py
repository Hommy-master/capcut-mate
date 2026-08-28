# -*- coding: utf-8 -*-
"""Generate transition/animation lists for add_images / add_videos docs.

Lists belong in add_xxx docs (not xxx_infos). This script also strips any
leftover MEDIA_EFFECT_LIST blocks from imgs_infos / video_infos and leaves
a short pointer to the corresponding add_xxx document.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.pyJianYingDraft.metadata import (
    IntroType,
    OutroType,
    GroupAnimationType,
    TransitionType,
)
from src.service.add_images import map_video_animation_name_to_enum
from src.service.add_videos import find_transition_type_by_name

MARKER_START = "<!-- MEDIA_EFFECT_LIST_START -->"
MARKER_END = "<!-- MEDIA_EFFECT_LIST_END -->"

EXAMPLE_IN = "渐显"
EXAMPLE_OUT = "渐隐"
EXAMPLE_LOOP = "动感摇晃I"
EXAMPLE_TRANSITION = "叠化"


def _sorted_titles(enum_cls) -> list[str]:
    return sorted({item.value.title for item in enum_cls}, key=lambda s: (s.casefold(), s))


def _sorted_transition_names() -> list[str]:
    return sorted({item.value.name for item in TransitionType}, key=lambda s: (s.casefold(), s))


def _validate() -> tuple[list[str], list[str], list[str], list[str]]:
    ins = _sorted_titles(IntroType)
    outs = _sorted_titles(OutroType)
    loops = _sorted_titles(GroupAnimationType)
    transitions = _sorted_transition_names()

    bad_in = [n for n in ins if map_video_animation_name_to_enum(n, "in") is None]
    bad_out = [n for n in outs if map_video_animation_name_to_enum(n, "out") is None]
    bad_loop = [n for n in loops if map_video_animation_name_to_enum(n, "group") is None]
    bad_tr = [n for n in transitions if find_transition_type_by_name(n) is None]
    if bad_in or bad_out or bad_loop or bad_tr:
        raise SystemExit(
            f"unresolvable: in={bad_in[:3]} out={bad_out[:3]} "
            f"loop={bad_loop[:3]} tr={bad_tr[:3]}"
        )
    for name, kind in [(EXAMPLE_IN, "in"), (EXAMPLE_OUT, "out"), (EXAMPLE_LOOP, "group")]:
        if map_video_animation_name_to_enum(name, kind) is None:
            raise SystemExit(f"example unresolved: {name}")
    if find_transition_type_by_name(EXAMPLE_TRANSITION) is None:
        raise SystemExit(f"example transition unresolved: {EXAMPLE_TRANSITION}")
    return ins, outs, loops, transitions


def build_images_zh(ins, outs, loops, transitions) -> str:
    return "\n".join(
        [
            "### 支持的转场与动画名称",
            "",
            "下列名称可直接作为 `image_infos` 中对应字段的值（与剪映端展示名一致）。未匹配到时该效果不会生效。",
            "",
            f"#### 转场（transition，共 {len(transitions)} 种）",
            "",
            "```text",
            *transitions,
            "```",
            "",
            f"#### 入场动画（in_animation，共 {len(ins)} 种）",
            "",
            "```text",
            *ins,
            "```",
            "",
            f"#### 出场动画（out_animation，共 {len(outs)} 种）",
            "",
            "```text",
            *outs,
            "```",
            "",
            f"#### 循环动画（loop_animation，共 {len(loops)} 种）",
            "",
            "```text",
            *loops,
            "```",
            "",
        ]
    )


def build_images_en(ins, outs, loops, transitions) -> str:
    return "\n".join(
        [
            "### Supported Transitions and Animations",
            "",
            "Use the names below directly as `image_infos` field values (same as CapCut/Jianying display names). Unmatched names are ignored.",
            "",
            f"#### Transitions (transition, {len(transitions)} total)",
            "",
            "```text",
            *transitions,
            "```",
            "",
            f"#### Intro animations (in_animation, {len(ins)} total)",
            "",
            "```text",
            *ins,
            "```",
            "",
            f"#### Outro animations (out_animation, {len(outs)} total)",
            "",
            "```text",
            *outs,
            "```",
            "",
            f"#### Loop animations (loop_animation, {len(loops)} total)",
            "",
            "```text",
            *loops,
            "```",
            "",
        ]
    )


def build_videos_zh(transitions) -> str:
    return "\n".join(
        [
            "### 支持的转场名称（transition 可用值）",
            "",
            "下列名称可直接作为 `video_infos` 中 `transition` 的值（与剪映端展示名一致）。未匹配到时该转场不会生效。",
            "",
            f"当前共 **{len(transitions)}** 种转场：",
            "",
            "```text",
            *transitions,
            "```",
            "",
        ]
    )


def build_videos_en(transitions) -> str:
    return "\n".join(
        [
            "### Supported Transition Names (`transition` values)",
            "",
            "Use the names below directly as `video_infos.transition` (same as CapCut/Jianying display names). Unmatched names are ignored.",
            "",
            f"Total: **{len(transitions)}** transitions:",
            "",
            "```text",
            *transitions,
            "```",
            "",
        ]
    )


def inject(path: Path, before: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    wrapped = f"{MARKER_START}\n{block.rstrip()}\n{MARKER_END}\n\n"

    if MARKER_START in text and MARKER_END in text:
        start = text.index(MARKER_START)
        end = text.index(MARKER_END) + len(MARKER_END)
        after = text[end:].lstrip("\n")
        text = text[:start] + wrapped.rstrip("\n") + "\n\n" + after
    else:
        if before not in text:
            raise SystemExit(f"insert marker not found in {path}: {before}")
        text = text.replace(before, wrapped + before, 1)

    path.write_text(text, encoding="utf-8")


def strip_list_keep_pointer(path: Path, pointer: str) -> None:
    """Remove MEDIA_EFFECT_LIST from infos docs and insert a short pointer."""
    text = path.read_text(encoding="utf-8")
    if MARKER_START in text and MARKER_END in text:
        start = text.index(MARKER_START)
        end = text.index(MARKER_END) + len(MARKER_END)
        after = text[end:].lstrip("\n")
        text = text[:start] + pointer.rstrip() + "\n\n" + after
        path.write_text(text, encoding="utf-8")


def update_add_images_hints(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8")
    if lang == "zh":
        text = text.replace(
            "| in_animation | string | ❌ | - | 入场动画名称（可选） |",
            "| in_animation | string | ❌ | - | 入场动画名称，须为下方「入场动画」列表中的值 |",
        )
        text = text.replace(
            "| out_animation | string | ❌ | - | 出场动画名称（可选） |",
            "| out_animation | string | ❌ | - | 出场动画名称，须为下方「出场动画」列表中的值 |",
        )
        text = text.replace(
            "| loop_animation | string | ❌ | - | 循环动画名称（可选） |",
            "| loop_animation | string | ❌ | - | 循环动画名称，须为下方「循环动画」列表中的值 |",
        )
        text = text.replace(
            "| transition | string | ❌ | - | 转场效果名称（可选） |",
            "| transition | string | ❌ | - | 转场名称，须为下方「转场」列表中的值 |",
        )
    else:
        text = text.replace(
            "| in_animation | string | ❌ | - | Intro animation name (optional) |",
            "| in_animation | string | ❌ | - | Intro animation name from Intro animations below |",
        )
        text = text.replace(
            "| out_animation | string | ❌ | - | Outro animation name (optional) |",
            "| out_animation | string | ❌ | - | Outro animation name from Outro animations below |",
        )
        text = text.replace(
            "| loop_animation | string | ❌ | - | Loop animation name (optional) |",
            "| loop_animation | string | ❌ | - | Loop animation name from Loop animations below |",
        )
        text = text.replace(
            "| transition | string | ❌ | - | Transition effect name (optional) |",
            "| transition | string | ❌ | - | Transition name from Transitions below |",
        )
    path.write_text(text, encoding="utf-8")


def update_add_videos_hints(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8")
    if lang == "zh":
        text = text.replace(
            "| transition | string | ❌ | - | 转场效果名称 |",
            "| transition | string | ❌ | - | 转场名称，须为下方「支持的转场名称」列表中的值 |",
        )
        # Replace invalid transition examples
        text = text.replace('\\"淡入淡出\\"', f'\\"{EXAMPLE_TRANSITION}\\"')
        text = text.replace('"淡入淡出"', f'"{EXAMPLE_TRANSITION}"')
        # Shorten vague transition section if present
        text = re.sub(
            r"#### 转场效果\n\n- \*\*transition\*\*: 转场效果名称\n- \*\*transition_duration\*\*: 转场持续时间\n"
            r"  - 最小值：100,000微秒（0\.1秒）\n"
            r"  - 最大值：2,500,000微秒（2\.5秒）\n"
            r"  - 推荐值：500,000微秒（0\.5秒）\n",
            "#### 转场效果\n\n"
            "- **transition**: 转场名称，须为下方「支持的转场名称」列表中的值\n"
            "- **transition_duration**: 转场持续时间\n"
            "  - 最小值：100,000微秒（0.1秒）\n"
            "  - 最大值：2,500,000微秒（2.5秒）\n"
            "  - 推荐值：500,000微秒（0.5秒）\n",
            text,
            count=1,
        )
    else:
        text = text.replace(
            "| transition | string | ❌ | - | Transition effect name |",
            "| transition | string | ❌ | - | Transition name from Supported Transition Names below |",
        )
        text = text.replace('\\"fade\\"', f'\\"{EXAMPLE_TRANSITION}\\"')
        text = text.replace('"fade"', f'"{EXAMPLE_TRANSITION}"')
        text = text.replace('\\"淡入淡出\\"', f'\\"{EXAMPLE_TRANSITION}\\"')
        text = text.replace('"淡入淡出"', f'"{EXAMPLE_TRANSITION}"')
    path.write_text(text, encoding="utf-8")


def update_infos_examples(path: Path) -> None:
    """Keep infos docs examples valid, without embedding full lists."""
    text = path.read_text(encoding="utf-8")
    text = text.replace('\\"淡入淡出\\"', f'\\"{EXAMPLE_TRANSITION}\\"')
    text = text.replace('"淡入淡出"', f'"{EXAMPLE_TRANSITION}"')
    text = text.replace('\\"fade\\"', f'\\"{EXAMPLE_TRANSITION}\\"')
    text = text.replace('"fade"', f'"{EXAMPLE_TRANSITION}"')
    text = text.replace('\\"cross_fade\\"', f'\\"{EXAMPLE_TRANSITION}\\"')
    text = text.replace('"cross_fade"', f'"{EXAMPLE_TRANSITION}"')
    text = text.replace('\\"fade_in\\"', f'\\"{EXAMPLE_IN}\\"')
    text = text.replace('"fade_in"', f'"{EXAMPLE_IN}"')
    text = text.replace('\\"fade_out\\"', f'\\"{EXAMPLE_OUT}\\"')
    text = text.replace('"fade_out"', f'"{EXAMPLE_OUT}"')
    text = text.replace('\\"bounce\\"', f'\\"{EXAMPLE_LOOP}\\"')
    text = text.replace('"bounce"', f'"{EXAMPLE_LOOP}"')
    path.write_text(text, encoding="utf-8")


def main() -> None:
    docs = ROOT / "docs"
    ins, outs, loops, transitions = _validate()

    # --- add_images ---
    inject(docs / "add_images.zh.md", "## 响应格式", build_images_zh(ins, outs, loops, transitions))
    inject(docs / "add_images.md", "## Response Format", build_images_en(ins, outs, loops, transitions))
    update_add_images_hints(docs / "add_images.zh.md", "zh")
    update_add_images_hints(docs / "add_images.md", "en")

    # --- add_videos ---
    inject(docs / "add_videos.zh.md", "## 响应格式", build_videos_zh(transitions))
    # EN may use "## Response Format" after transition section
    inject(docs / "add_videos.md", "## Response Format", build_videos_en(transitions))
    update_add_videos_hints(docs / "add_videos.zh.md", "zh")
    update_add_videos_hints(docs / "add_videos.md", "en")

    # --- strip from infos docs, leave pointers ---
    strip_list_keep_pointer(
        docs / "imgs_infos.zh.md",
        "### 可用转场与动画名称\n\n"
        "转场、入场/出场/循环动画的完整可用值清单，请参见 "
        "[添加图片（add_images）](./add_images.zh.md) 文档中的「支持的转场与动画名称」。",
    )
    strip_list_keep_pointer(
        docs / "imgs_infos.md",
        "### Available Transitions and Animations\n\n"
        "For the full lists of valid `transition` / `in_animation` / `out_animation` / `loop_animation` values, "
        "see [add_images](./add_images.md) → Supported Transitions and Animations.",
    )
    strip_list_keep_pointer(
        docs / "video_infos.zh.md",
        "### 可用转场名称\n\n"
        "转场完整可用值清单，请参见 [添加视频（add_videos）](./add_videos.zh.md) 文档中的「支持的转场名称」。"
        "画面入场/出场/循环动画请参见 [添加图片（add_images）](./add_images.zh.md)。",
    )
    strip_list_keep_pointer(
        docs / "video_infos.md",
        "### Available Transition Names\n\n"
        "For the full list of valid `transition` values, see [add_videos](./add_videos.md) → Supported Transition Names. "
        "For intro/outro/loop clip animations, see [add_images](./add_images.md).",
    )

    for name in ("imgs_infos.zh.md", "imgs_infos.md", "video_infos.zh.md", "video_infos.md"):
        update_infos_examples(docs / name)

    # Restore infos param hints that previously pointed to "下方列表"
    for path, replacements in [
        (
            docs / "imgs_infos.zh.md",
            [
                (
                    "| in_animation | string |❌ | None |入场动画名称，须为下方「入场动画」列表中的值 |",
                    "| in_animation | string |❌ | None |入场动画名称，可用值见 [add_images](./add_images.zh.md) |",
                ),
                (
                    "| out_animation | string |❌ | None |出场动画名称，须为下方「出场动画」列表中的值 |",
                    "| out_animation | string |❌ | None |出场动画名称，可用值见 [add_images](./add_images.zh.md) |",
                ),
                (
                    "| loop_animation | string |❌ | None |循环动画名称，须为下方「循环动画」列表中的值 |",
                    "| loop_animation | string |❌ | None |循环动画名称，可用值见 [add_images](./add_images.zh.md) |",
                ),
                (
                    "| transition | string |❌ | None |转场名称，须为下方「转场」列表中的值 |",
                    "| transition | string |❌ | None |转场名称，可用值见 [add_images](./add_images.zh.md) / [add_videos](./add_videos.zh.md) |",
                ),
            ],
        ),
        (
            docs / "imgs_infos.md",
            [
                (
                    "| in_animation | string |❌ | None | Intro animation name from Intro animations below |",
                    "| in_animation | string |❌ | None | Intro animation name; see [add_images](./add_images.md) |",
                ),
                (
                    "| out_animation | string |❌ | None | Outro animation name from Outro animations below |",
                    "| out_animation | string |❌ | None | Outro animation name; see [add_images](./add_images.md) |",
                ),
                (
                    "| loop_animation | string |❌ | None | Loop animation name from Loop animations below |",
                    "| loop_animation | string |❌ | None | Loop animation name; see [add_images](./add_images.md) |",
                ),
                (
                    "| transition | string |❌ | None | Transition name from Transitions below |",
                    "| transition | string |❌ | None | Transition name; see [add_images](./add_images.md) / [add_videos](./add_videos.md) |",
                ),
            ],
        ),
        (
            docs / "video_infos.zh.md",
            [
                (
                    "| transition | string |❌ | None |转场名称，须为下方「转场」列表中的值 |",
                    "| transition | string |❌ | None |转场名称，可用值见 [add_videos](./add_videos.zh.md) |",
                ),
            ],
        ),
        (
            docs / "video_infos.md",
            [
                (
                    "| transition | string |❌ | None | Transition name from Transitions below |",
                    "| transition | string |❌ | None | Transition name; see [add_videos](./add_videos.md) |",
                ),
            ],
        ),
    ]:
        text = path.read_text(encoding="utf-8")
        for old, new in replacements:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")

    print(
        "moved media effect lists to add_images/add_videos; "
        f"transitions={len(transitions)}, in={len(ins)}, out={len(outs)}, loop={len(loops)}"
    )


if __name__ == "__main__":
    main()
