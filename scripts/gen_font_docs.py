# -*- coding: utf-8 -*-
"""Generate font lists and inject them into add_captions docs."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.pyJianYingDraft import FontType
from src.service.add_captions import FONT_ALIAS_MAP, resolve_font_type

EXAMPLE_FONT = "得意黑"
OLD_EXAMPLE_FONT = "思源黑体"

ZH_MARKER_START = "<!-- FONT_LIST_START -->"
ZH_MARKER_END = "<!-- FONT_LIST_END -->"
EN_MARKER_START = "<!-- FONT_LIST_START -->"
EN_MARKER_END = "<!-- FONT_LIST_END -->"

ZH_INSERT_BEFORE = "## 完整参数请求示例（含注释）"
EN_INSERT_BEFORE = "## Fully Annotated Request Example"


def build_lists() -> tuple[str, str]:
    names = sorted({f.value.name for f in FontType}, key=lambda s: (s.casefold(), s))
    bad = [n for n in names if resolve_font_type(n) is None]
    if bad:
        raise SystemExit(f"unresolvable fonts: {bad}")
    if resolve_font_type(EXAMPLE_FONT) is None:
        raise SystemExit(f"example font unresolved: {EXAMPLE_FONT}")

    alias_lines = []
    for key, enum_name in FONT_ALIAS_MAP.items():
        font_type = getattr(FontType, enum_name, None)
        display = font_type.value.name if font_type else enum_name
        alias_lines.append(f"- `{key}` → `{display}`")

    zh = "\n".join(
        [
            "### 支持的字体（font 可用值）",
            "",
            "`font` 可直接填写下列**展示名**（与剪映字体名一致）。也支持对应的枚举名，以及下方别名。未匹配到时将回退默认字体。",
            "",
            f"当前共 **{len(names)}** 种字体：",
            "",
            "```",
            *names,
            "```",
            "",
            "#### 字体别名",
            "",
            "下列别名也可作为 `font` 的值：",
            "",
            *alias_lines,
            "",
        ]
    )

    en = "\n".join(
        [
            "### Supported Fonts (`font` values)",
            "",
            "You can set `font` to any of the following **display names** (same as CapCut/Jianying font names). Enum names and the aliases below are also accepted. If unresolved, the default font is used.",
            "",
            f"Total: **{len(names)}** fonts:",
            "",
            "```",
            *names,
            "```",
            "",
            "#### Font aliases",
            "",
            "These aliases are also valid `font` values:",
            "",
            *alias_lines,
            "",
        ]
    )
    return zh, en


def inject(path: Path, before: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    wrapped = f"{ZH_MARKER_START}\n{block.rstrip()}\n{ZH_MARKER_END}\n\n"

    if ZH_MARKER_START in text and ZH_MARKER_END in text:
        start = text.index(ZH_MARKER_START)
        end = text.index(ZH_MARKER_END) + len(ZH_MARKER_END)
        # keep trailing newlines after end marker
        after = text[end:]
        after = after.lstrip("\n")
        text = text[:start] + wrapped.rstrip("\n") + "\n\n" + after
    else:
        if before not in text:
            raise SystemExit(f"insert marker not found in {path}: {before}")
        text = text.replace(before, wrapped + before, 1)

    text = text.replace(OLD_EXAMPLE_FONT, EXAMPLE_FONT)
    # Point font param description to the list section
    text = text.replace(
        "| font | string | ❌ | `null` | 字体名称（枚举名、展示名或别名）；`null` 使用默认字体 |",
        "| font | string | ❌ | `null` | 字体名称，须为下方「支持的字体」中的展示名（也支持枚举名/别名）；`null` 使用默认字体 |",
    )
    text = text.replace(
        "| font | string | ❌ | `null` | Font name (enum/display/alias); `null` uses default |",
        "| font | string | ❌ | `null` | Font name from Supported Fonts below (enum/display/alias also ok); `null` uses default |",
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    zh, en = build_lists()
    docs = ROOT / "docs"
    inject(docs / "add_captions.zh.md", ZH_INSERT_BEFORE, zh)
    inject(docs / "add_captions.md", EN_INSERT_BEFORE, en)

    # cleanup temp fragments if present
    for name in ("_font_list_zh.md", "_font_list_en.md"):
        p = docs / name
        if p.exists():
            p.unlink()

    print(f"updated docs with {zh.count(chr(10)) - 10} font lines; example font -> {EXAMPLE_FONT}")


if __name__ == "__main__":
    main()
