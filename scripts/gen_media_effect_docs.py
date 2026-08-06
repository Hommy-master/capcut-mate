# -*- coding: utf-8 -*-
"""Generate transition/animation lists for imgs_infos and video_infos docs."""
from __future__ import annotations

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

OLD_EXAMPLES = {
    '"fade_in"': f'"{EXAMPLE_IN}"',
    '"fade_out"': f'"{EXAMPLE_OUT}"',
    '"bounce"': f'"{EXAMPLE_LOOP}"',
    '"cross_fade"': f'"{EXAMPLE_TRANSITION}"',
    '\\"fade_in\\"': f'\\"{EXAMPLE_IN}\\"',
    '\\"fade_out\\"': f'\\"{EXAMPLE_OUT}\\"',
    '\\"bounce\\"': f'\\"{EXAMPLE_LOOP}\\"',
    '\\"cross_fade\\"': f'\\"{EXAMPLE_TRANSITION}\\"',
}


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
    bad_tr_img = []
    for name in transitions:
        matched = any(
            isinstance(attr, TransitionType) and attr.value.name == name
            for attr in TransitionType
        )
        if not matched:
            bad_tr_img.append(name)
    bad_tr_video = [n for n in transitions if find_transition_type_by_name(n) is None]

    if bad_in or bad_out or bad_loop or bad_tr_img or bad_tr_video:
        raise SystemExit(
            f"unresolvable names: in={bad_in[:5]} out={bad_out[:5]} "
            f"loop={bad_loop[:5]} tr_img={bad_tr_img[:5]} tr_video={bad_tr_video[:5]}"
        )

    for name, kind in [
        (EXAMPLE_IN, "in"),
        (EXAMPLE_OUT, "out"),
        (EXAMPLE_LOOP, "group"),
    ]:
        if map_video_animation_name_to_enum(name, kind) is None:
            raise SystemExit(f"example unresolved: {name}")
    if find_transition_type_by_name(EXAMPLE_TRANSITION) is None:
        raise SystemExit(f"example transition unresolved: {EXAMPLE_TRANSITION}")

    return ins, outs, loops, transitions


def build_zh(*, include_animations: bool, video_api_note: bool = False) -> str:
    ins, outs, loops, transitions = _validate()
    parts = [
        "### 支持的转场与动画名称",
        "",
        "下列名称可直接作为对应字段的值（与剪映端展示名一致）。未匹配到时该效果不会生效。",
        "",
    ]
    if video_api_note:
        parts.extend(
            [
                "说明：`video_infos` 请求参数目前仅包含 `transition`；下列入场/出场/循环动画与图片画面动画同源，可直接用于 `imgs_infos` / `add_images` 等接口的同名字段。",
                "",
            ]
        )
    parts.extend(
        [
            f"#### 转场（transition，共 {len(transitions)} 种）",
            "",
            "```text",
            *transitions,
            "```",
            "",
        ]
    )
    if include_animations:
        parts.extend(
            [
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
    return "\n".join(parts)


def build_en(*, include_animations: bool, video_api_note: bool = False) -> str:
    ins, outs, loops, transitions = _validate()
    parts = [
        "### Supported Transitions and Animations",
        "",
        "Use the names below directly as field values (same as CapCut/Jianying display names). Unmatched names are ignored.",
        "",
    ]
    if video_api_note:
        parts.extend(
            [
                "Note: `video_infos` currently only accepts `transition` in the request. "
                "Intro/outro/loop names below match image/clip animations and can be used with `imgs_infos` / `add_images`.",
                "",
            ]
        )
    parts.extend(
        [
            f"#### Transitions (transition, {len(transitions)} total)",
            "",
            "```text",
            *transitions,
            "```",
            "",
        ]
    )
    if include_animations:
        parts.extend(
            [
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
    return "\n".join(parts)


def inject(path: Path, before_heading: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    wrapped = f"{MARKER_START}\n{block.rstrip()}\n{MARKER_END}\n\n"

    if MARKER_START in text and MARKER_END in text:
        start = text.index(MARKER_START)
        end = text.index(MARKER_END) + len(MARKER_END)
        after = text[end:].lstrip("\n")
        text = text[:start] + wrapped.rstrip("\n") + "\n\n" + after
    else:
        if before_heading not in text:
            raise SystemExit(f"insert marker not found in {path}: {before_heading}")
        text = text.replace(before_heading, wrapped + before_heading, 1)

    for old, new in OLD_EXAMPLES.items():
        text = text.replace(old, new)

    path.write_text(text, encoding="utf-8")


def update_param_hints(path: Path, lang: str, has_animations: bool) -> None:
    text = path.read_text(encoding="utf-8")
    if lang == "zh":
        text = text.replace(
            "| transition | string |❌ | None |转场效果 |",
            "| transition | string |❌ | None |转场名称，须为下方「转场」列表中的值 |",
        )
        text = text.replace(
            "| transition | string |❌ | None |转场效果 |",
            "| transition | string |❌ | None |转场名称，须为下方「转场」列表中的值 |",
        )
        # video_infos table may differ slightly
        text = text.replace(
            "| transition | string |❌ | None |转场效果 |",
            "| transition | string |❌ | None |转场名称，须为下方「转场」列表中的值 |",
        )
        if has_animations:
            text = text.replace(
                "| in_animation | string |❌ | None |入动画效果 |",
                "| in_animation | string |❌ | None |入场动画名称，须为下方「入场动画」列表中的值 |",
            )
            text = text.replace(
                "| out_animation | string |❌ | None |出动画效果 |",
                "| out_animation | string |❌ | None |出场动画名称，须为下方「出场动画」列表中的值 |",
            )
            text = text.replace(
                "| loop_animation | string |❌ | None |循动画效果 |",
                "| loop_animation | string |❌ | None |循环动画名称，须为下方「循环动画」列表中的值 |",
            )
    else:
        text = text.replace(
            "| transition | string |❌ | None | Transition effect |",
            "| transition | string |❌ | None | Transition name from Transitions below |",
        )
        if has_animations:
            text = text.replace(
                "| in_animation | string |❌ | None | Entrance animation effect |",
                "| in_animation | string |❌ | None | Intro animation name from Intro animations below |",
            )
            text = text.replace(
                "| out_animation | string |❌ | None | Exit animation effect |",
                "| out_animation | string |❌ | None | Outro animation name from Outro animations below |",
            )
            text = text.replace(
                "| loop_animation | string |❌ | None | Loop animation effect |",
                "| loop_animation | string |❌ | None | Loop animation name from Loop animations below |",
            )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    docs = ROOT / "docs"

    # imgs_infos: transitions + animations
    inject(docs / "imgs_infos.zh.md", "##响应格式", build_zh(include_animations=True))
    inject(docs / "imgs_infos.md", "## Response Format", build_en(include_animations=True))
    update_param_hints(docs / "imgs_infos.zh.md", "zh", True)
    update_param_hints(docs / "imgs_infos.md", "en", True)

    # video_infos: full lists (transition is the request field; animations listed for the same media catalog)
    inject(
        docs / "video_infos.zh.md",
        "##响应格式",
        build_zh(include_animations=True, video_api_note=True),
    )
    inject(
        docs / "video_infos.md",
        "## Response Format",
        build_en(include_animations=True, video_api_note=True),
    )
    update_param_hints(docs / "video_infos.zh.md", "zh", False)
    update_param_hints(docs / "video_infos.md", "en", False)

    for path, old, new in [
        (
            docs / "video_infos.zh.md",
            "| transition | string |❌ | None |转场效果 |",
            "| transition | string |❌ | None |转场名称，须为下方「转场」列表中的值 |",
        ),
        (
            docs / "video_infos.md",
            "| transition | string |❌ | None | Transition effect |",
            "| transition | string |❌ | None | Transition name from Transitions below |",
        ),
    ]:
        text = path.read_text(encoding="utf-8")
        if old in text:
            path.write_text(text.replace(old, new), encoding="utf-8")

    _, _, _, transitions = _validate()
    print(
        f"updated imgs/video infos docs: "
        f"transitions={len(transitions)}, "
        f"in={len(_sorted_titles(IntroType))}, "
        f"out={len(_sorted_titles(OutroType))}, "
        f"loop={len(_sorted_titles(GroupAnimationType))}"
    )


if __name__ == "__main__":
    main()
