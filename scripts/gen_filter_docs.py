# -*- coding: utf-8 -*-
"""Generate filter_title lists and inject them into add_filters docs."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.pyJianYingDraft.metadata.filter_meta import FilterType

MARKER_START = "<!-- FILTER_LIST_START -->"
MARKER_END = "<!-- FILTER_LIST_END -->"

# Valid FilterType.value.name examples (docs previously used 复古/黑白/电影感 which do not exist)
EXAMPLE_1 = "1980"
EXAMPLE_2 = "森山"
EXAMPLE_3 = "City Walk"


def _all_filter_names() -> list[str]:
    return sorted({item.value.name for item in FilterType}, key=lambda s: (s.casefold(), s))


def _validate(names: list[str]) -> None:
    known = set(names)
    for example in (EXAMPLE_1, EXAMPLE_2, EXAMPLE_3):
        if example not in known:
            raise SystemExit(f"example filter unresolved: {example}")


def build_zh(names: list[str]) -> str:
    return "\n".join(
        [
            "### 支持的滤镜名称（filter_title 可用值）",
            "",
            "下列名称可直接作为 `filter_title` 的值（与剪映滤镜展示名一致）。未匹配到时添加会失败。",
            "",
            f"当前共 **{len(names)}** 种滤镜：",
            "",
            "```text",
            *names,
            "```",
            "",
        ]
    )


def build_en(names: list[str]) -> str:
    return "\n".join(
        [
            "### Supported Filter Names (`filter_title` values)",
            "",
            "Use the names below directly as `filter_title` (same as CapCut/Jianying display names). Unmatched names will fail.",
            "",
            f"Total: **{len(names)}** filters:",
            "",
            "```text",
            *names,
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


def polish_zh(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '- `filter_title`: 滤镜名称，必须是系统中已存在的滤镜名称',
        '- `filter_title`: 滤镜名称，须为下方「支持的滤镜名称」列表中的值',
    )

    old_section = """#### 滤镜名称说明

- **filter_title**: 滤镜的名称
  - 格式：字符串
  - 示例：`"复古"`、`"黑白"`、`"电影感"`
  - 获取方式：通过剪映滤镜库或相关API获取
  - 常见滤镜名称：
    - 复古风格："复古", "1980", "VHS III"
    - 黑白风格："黑白", "森山"
    - 电影风格："电影感", "好莱坞III"
    - 其他风格："City Walk", "Lofi II"

"""
    text = text.replace(old_section, "")

    # Replace invalid example titles with real ones
    replacements = {
        "复古": EXAMPLE_1,
        "黑白": EXAMPLE_2,
        "电影感": EXAMPLE_3,
    }
    # Only replace quoted titles to avoid accidentally changing prose like “复古风格”
    for old, new in replacements.items():
        text = text.replace(f'\\"{old}\\"', f'\\"{new}\\"')
        text = text.replace(f'"{old}"', f'"{new}"')
        text = text.replace(f'「{old}」', f'「{new}」')

    path.write_text(text, encoding="utf-8")


def polish_en(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '- `filter_title`: Filter name, must be an existing filter name in the system',
        '- `filter_title`: Filter name; must be one of the Supported Filter Names below',
    )
    # Keep Chinese CapCut titles in examples (API values)
    replacements = {
        "复古": EXAMPLE_1,
        "黑白": EXAMPLE_2,
        "电影感": EXAMPLE_3,
    }
    for old, new in replacements.items():
        text = text.replace(f'\\"{old}\\"', f'\\"{new}\\"')
        text = text.replace(f'"{old}"', f'"{new}"')

    path.write_text(text, encoding="utf-8")


def main() -> None:
    names = _all_filter_names()
    _validate(names)
    docs = ROOT / "docs"
    zh_path = docs / "add_filters.zh.md"
    en_path = docs / "add_filters.md"

    polish_zh(zh_path)
    polish_en(en_path)
    inject(zh_path, "## 响应格式", build_zh(names))
    inject(en_path, "## Response Format", build_en(names))
    polish_zh(zh_path)
    polish_en(en_path)

    print(f"updated add_filters docs with {len(names)} filter titles")


if __name__ == "__main__":
    main()
