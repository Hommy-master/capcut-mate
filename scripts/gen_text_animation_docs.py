# -*- coding: utf-8 -*-
"""Generate text animation lists and inject them into add_captions docs."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.pyJianYingDraft.metadata import TextIntro, TextOutro, TextLoopAnim
from src.service.add_captions import map_animation_name_to_enum

MARKER_START = "<!-- ANIMATION_LIST_START -->"
MARKER_END = "<!-- ANIMATION_LIST_END -->"

ZH_INSERT_BEFORE = "## 完整参数请求示例（含注释）"
EN_INSERT_BEFORE = "## Fully Annotated Request Example"


def _titles(enum_cls) -> list[str]:
    return sorted({item.value.title for item in enum_cls}, key=lambda s: (s.casefold(), s))


def _validate(names: list[str], anim_type: str) -> None:
    bad = [n for n in names if map_animation_name_to_enum(n, anim_type) is None]
    if bad:
        raise SystemExit(f"unresolvable {anim_type} animations: {bad}")


def build_lists() -> tuple[str, str]:
    in_names = _titles(TextIntro)
    out_names = _titles(TextOutro)
    loop_names = _titles(TextLoopAnim)
    _validate(in_names, "in")
    _validate(out_names, "out")
    _validate(loop_names, "loop")

    zh = "\n".join(
        [
            "### 支持的文字动画（in / out / loop）",
            "",
            "下列名称可直接作为字段 in_animation、out_animation、loop_animation 的值（与 get_text_animations 返回的 name、以及剪映动画标题一致）。未匹配到时该动画不会生效。",
            "",
            f"#### 入场动画（in_animation，共 {len(in_names)} 种）",
            "",
            "```text",
            *in_names,
            "```",
            "",
            f"#### 出场动画（out_animation，共 {len(out_names)} 种）",
            "",
            "```text",
            *out_names,
            "```",
            "",
            f"#### 循环动画（loop_animation，共 {len(loop_names)} 种）",
            "",
            "```text",
            *loop_names,
            "```",
            "",
        ]
    )

    en = "\n".join(
        [
            "### Supported Text Animations (in / out / loop)",
            "",
            "Use the names below directly as in_animation, out_animation, or loop_animation (same as CapCut/Jianying titles and get_text_animations.name). Unmatched names are ignored.",
            "",
            f"#### Intro animations (in_animation, {len(in_names)} total)",
            "",
            "```text",
            *in_names,
            "```",
            "",
            f"#### Outro animations (out_animation, {len(out_names)} total)",
            "",
            "```text",
            *out_names,
            "```",
            "",
            f"#### Loop animations (loop_animation, {len(loop_names)} total)",
            "",
            "```text",
            *loop_names,
            "```",
            "",
        ]
    )
    return zh, en


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

    # Point animation field descriptions to the list section
    text = text.replace(
        "| in_animation | string | ❌ | `null` | 入场动画名称，需与 `get_text_animations` 返回的名称一致，如 `\"向上滑动\"` |",
        "| in_animation | string | ❌ | `null` | 入场动画名称，须为下方「入场动画」列表中的值，如 `\"向上滑动\"` |",
    )
    text = text.replace(
        "| out_animation | string | ❌ | `null` | 出场动画名称，如 `\"向下滑动\"` |",
        "| out_animation | string | ❌ | `null` | 出场动画名称，须为下方「出场动画」列表中的值，如 `\"向下滑动\"` |",
    )
    text = text.replace(
        "| loop_animation | string | ❌ | `null` | 循环动画名称，如 `\"弹幕滚动\"` |",
        "| loop_animation | string | ❌ | `null` | 循环动画名称，须为下方「循环动画」列表中的值，如 `\"弹幕滚动\"` |",
    )
    text = text.replace(
        "| in_animation | string | ❌ | `null` | Intro animation name from `get_text_animations`, e.g. `\"向上滑动\"` |",
        "| in_animation | string | ❌ | `null` | Intro animation name from Intro animations below, e.g. `\"向上滑动\"` |",
    )
    text = text.replace(
        "| out_animation | string | ❌ | `null` | Outro animation name, e.g. `\"向下滑动\"` |",
        "| out_animation | string | ❌ | `null` | Outro animation name from Outro animations below, e.g. `\"向下滑动\"` |",
    )
    text = text.replace(
        "| loop_animation | string | ❌ | `null` | Loop animation name, e.g. `\"弹幕滚动\"` |",
        "| loop_animation | string | ❌ | `null` | Loop animation name from Loop animations below, e.g. `\"弹幕滚动\"` |",
    )

    path.write_text(text, encoding="utf-8")


def main() -> None:
    zh, en = build_lists()
    docs = ROOT / "docs"
    inject(docs / "add_captions.zh.md", ZH_INSERT_BEFORE, zh)
    inject(docs / "add_captions.md", EN_INSERT_BEFORE, en)
    print(
        "updated animation docs: "
        f"in={zh.count(chr(10)) and len(_titles(TextIntro))}, "
        f"out={len(_titles(TextOutro))}, loop={len(_titles(TextLoopAnim))}"
    )


if __name__ == "__main__":
    main()
