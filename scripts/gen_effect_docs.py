# -*- coding: utf-8 -*-
"""Generate effect_title lists and inject them into add_effects docs."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.pyJianYingDraft.metadata import VideoSceneEffectType, VideoCharacterEffectType

MARKER_START = "<!-- EFFECT_LIST_START -->"
MARKER_END = "<!-- EFFECT_LIST_END -->"

EXAMPLE_EFFECT = "录制边框 III"
EXAMPLE_EFFECT_2 = "简约边框"


def _all_effect_names() -> list[str]:
    names = {item.value.name for item in VideoSceneEffectType} | {
        item.value.name for item in VideoCharacterEffectType
    }
    return sorted(names, key=lambda s: (s.casefold(), s))


def _validate(names: list[str]) -> None:
    scene = {item.value.name for item in VideoSceneEffectType}
    char = {item.value.name for item in VideoCharacterEffectType}
    known = scene | char
    bad = [n for n in names if n not in known]
    if bad:
        raise SystemExit(f"unresolvable effects: {bad[:10]}")
    for example in (EXAMPLE_EFFECT, EXAMPLE_EFFECT_2):
        if example not in known:
            raise SystemExit(f"example effect unresolved: {example}")


def build_zh(names: list[str]) -> str:
    scene_count = len({item.value.name for item in VideoSceneEffectType})
    char_count = len({item.value.name for item in VideoCharacterEffectType})
    return "\n".join(
        [
            "### 支持的特效名称（effect_title 可用值）",
            "",
            "下列名称可直接作为 `effect_title` 的值（与剪映特效展示名一致，来自画面特效与人物特效）。未匹配到时添加会失败。",
            "",
            f"当前共 **{len(names)}** 种（画面特效 {scene_count} + 人物特效 {char_count}，去重后）：",
            "",
            "```text",
            *names,
            "```",
            "",
        ]
    )


def build_en(names: list[str]) -> str:
    scene_count = len({item.value.name for item in VideoSceneEffectType})
    char_count = len({item.value.name for item in VideoCharacterEffectType})
    return "\n".join(
        [
            "### Supported Effect Names (`effect_title` values)",
            "",
            "Use the names below directly as `effect_title` (same as CapCut/Jianying display names; from scene effects and character effects). Unmatched names will fail.",
            "",
            f"Total: **{len(names)}** effects ({scene_count} scene + {char_count} character, after dedupe):",
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
        "[中文版](./add_audios.zh.md) | [English](./add_audios.md)",
        "[中文版](./add_effects.zh.md) | [English](./add_effects.md)",
    )
    text = text.replace(
        '- `effect_title`: 特效名称，必须是系统中已存在的特效名称',
        '- `effect_title`: 特效名称，须为下方「支持的特效名称」列表中的值',
    )
    # Replace outdated vague name section with pointer (kept until marker replaces area)
    old_section = """#### 特效名称说明

- **effect_title**: 特效的名称
  - 格式：字符串
  - 示例：`"录制边框 III"`
  - 获取方式：通过剪映特效库或相关API获取
  - 常见特效名称：
    - 边框特效："录制边框 III", "简约边框", "霓虹边框"
    - 滤镜特效："复古滤镜", "黑白滤镜", "暖色调"
    - 动态特效："粒子效果", "光晕效果", "闪烁特效"
    - 转场特效："淡入淡出", "推拉门", "马赛克转场"

"""
    if old_section in text and MARKER_START not in text:
        text = text.replace(old_section, "")
    elif old_section in text:
        text = text.replace(old_section, "")

    text = text.replace('\\"复古滤镜\\"', f'\\"{EXAMPLE_EFFECT_2}\\"')
    text = text.replace('"复古滤镜"', f'"{EXAMPLE_EFFECT_2}"')
    path.write_text(text, encoding="utf-8")


def polish_en(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '- `effect_title`: Effect name, must be an existing effect name in the system',
        '- `effect_title`: Effect name; must be one of the Supported Effect Names below',
    )
    # Prefer real CapCut titles in examples
    text = text.replace("Recording Border III", EXAMPLE_EFFECT)
    text = text.replace("Vintage Filter", EXAMPLE_EFFECT_2)
    text = text.replace('\\"Recording Border III\\"', f'\\"{EXAMPLE_EFFECT}\\"')
    text = text.replace('\\"Vintage Filter\\"', f'\\"{EXAMPLE_EFFECT_2}\\"')
    path.write_text(text, encoding="utf-8")


def main() -> None:
    names = _all_effect_names()
    _validate(names)
    docs = ROOT / "docs"

    zh_path = docs / "add_effects.zh.md"
    en_path = docs / "add_effects.md"

    polish_zh(zh_path)
    polish_en(en_path)

    inject(zh_path, "## 响应格式", build_zh(names))
    inject(en_path, "## Response Format", build_en(names))

    # Re-run polish for example replacements that may sit after inject target
    polish_zh(zh_path)
    polish_en(en_path)

    print(f"updated add_effects docs with {len(names)} effect titles")


if __name__ == "__main__":
    main()
