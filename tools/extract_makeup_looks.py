"""从剪映素材面板缓存导出美妆「套装」清单，生成 makeup_looks_generated.py。

数据源是剪映客户端的素材面板缓存 rp.db（http_cache 表里 get_panel_info 的响应）：
分类 category_key=taozhuang 即美妆面板的「套装」列表，条目的 third_resource_id
就是草稿 materials.effects[].resource_id 里写的值（已与参考草稿逐条核对）。

用法：
    python tools/extract_makeup_looks.py                    # 自动搜索本机剪映/CapCut 缓存
    python tools/extract_makeup_looks.py --db ~/x/rp.db     # 指定缓存库（可重复）
    python tools/extract_makeup_looks.py --json panel.json  # 用离线保存的面板响应
    python tools/extract_makeup_looks.py --out src/.../makeup_looks_generated.py

面板数据只在剪映里打开过「美妆」面板后才会落到本机缓存，否则请先打开一次。
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

# 生成目标（相对仓库根目录）
DEFAULT_OUT = "src/pyJianYingDraft/metadata/makeup_looks_generated.py"

# 面板里「套装」分类的 key，其余 key（kouhong 口红、yanying 眼影…）是单品
LOOK_CATEGORY_KEY = "taozhuang"

# 默认缓存位置：只取国内版剪映（CapCut 国际版是同一套结构但套装名为英文，
# 需要时用 --db 显式指定其 rp.db）
DEFAULT_DB_PATTERNS = [
    "~/Movies/JianyingPro/User Data/Cache/ressdk_db/*/rp.db",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "JianyingPro/User Data/Cache/ressdk_db/*/rp.db"),
]


def _iter_panel_payloads(db_paths: Iterable[str]) -> Iterable[Dict[str, Any]]:
    """从 rp.db 的 http_cache 表里按时间顺序取出可解析的面板响应。"""
    for db_path in db_paths:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        try:
            rows = conn.execute(
                "select response_body from http_cache where url like '%get_panel_info%' order by timestamp"
            ).fetchall()
        finally:
            conn.close()
        for (body,) in rows:
            if not body:
                continue
            try:
                yield json.loads(body)
            except (TypeError, ValueError):
                continue


def _extract_looks(payloads: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """从面板响应里挑出「套装」分类，返回 {名称: 条目}。

    缓存里可能有多份快照（剪映会缓存历史响应）：遇到完整快照（has_more=False）就整体替换，
    分页响应则合并进来，这样最终以最新一份完整清单为准，已经下架的套装不会残留。
    """
    looks: Dict[str, Dict[str, Any]] = {}
    conflicts: Dict[str, set] = {}
    for payload in payloads:
        data = payload.get("data")
        if not isinstance(data, dict):
            continue
        categories = data.get("categories") or []
        resources = data.get("category_resources") or {}
        for category in categories:
            if category.get("category_key") != LOOK_CATEGORY_KEY:
                continue
            bucket = resources.get(str(category.get("category_id"))) or {}
            if not bucket.get("has_more"):
                looks = {} if bucket.get("effect_item_list") else looks
            for item in bucket.get("effect_item_list") or []:
                attr = item.get("common_attr") or {}
                name = (attr.get("title") or "").strip()
                resource_id = attr.get("third_resource_id_str") or attr.get("third_resource_id")
                if not name or not resource_id:
                    continue
                extra = {}
                if attr.get("extra"):
                    try:
                        extra = json.loads(attr["extra"])
                    except (TypeError, ValueError):
                        extra = {}
                if name in looks and looks[name]["resource_id"] != str(resource_id):
                    conflicts.setdefault(name, set()).update({looks[name]["resource_id"], str(resource_id)})
                looks[name] = {
                    "resource_id": str(resource_id),
                    "effect_id": str(attr.get("effect_id") or attr.get("id") or ""),
                    "name": name,
                    "is_vip": bool(extra.get("is_vip")),
                }
    for name, ids in conflicts.items():
        print(f"注意：{name} 在缓存里出现过多个 resource_id {sorted(ids)}，已取最新快照的值", file=sys.stderr)
    return looks


def _render(looks: Dict[str, Dict[str, Any]]) -> str:
    """渲染生成文件内容，条目按名称排序，保证可重复生成。"""
    lines: List[str] = [
        '"""由 tools/extract_makeup_looks.py 生成，请勿手工修改。',
        "",
        "数据来源：剪映素材面板缓存（get_panel_info，category_key=taozhuang，美妆「套装」）。",
        "resource_id：写入草稿 materials.effects[].resource_id 的值（面板响应的 third_resource_id）；",
        "effect_id：面板条目 id；is_vip：是否会员素材。",
        '"""',
        "",
        "MAKEUP_LOOK_MAP = {",
    ]
    for name in sorted(looks):
        item = looks[name]
        lines.append(
            f'    "{name}": {{"resource_id": "{item["resource_id"]}", '
            f'"effect_id": "{item["effect_id"]}", "name": "{name}", '
            f'"is_vip": {item["is_vip"]}}},'
        )
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def _resolve_dbs(raw_paths: List[str]) -> List[str]:
    """展开命令行给的路径（支持 glob），未给时搜索各平台默认缓存位置。"""
    patterns = raw_paths or DEFAULT_DB_PATTERNS
    found: List[str] = []
    for pattern in patterns:
        expanded = os.path.expanduser(pattern)
        found.extend(sorted(glob.glob(expanded)))
    return [p for p in found if os.path.isfile(p)]


def main() -> int:
    parser = argparse.ArgumentParser(description="导出剪映美妆「套装」清单")
    parser.add_argument("--db", action="append", default=[], help="rp.db 路径（可重复，支持 glob）")
    parser.add_argument("--json", action="append", default=[], help="离线保存的面板响应 JSON（可重复）")
    parser.add_argument("--out", default=DEFAULT_OUT, help=f"输出文件（默认 {DEFAULT_OUT}）")
    parser.add_argument("--print", dest="print_only", action="store_true", help="只打印，不写文件")
    args = parser.parse_args()

    payloads: List[Dict[str, Any]] = []
    if args.json:
        for path in args.json:
            payloads.append(json.loads(Path(path).read_text(encoding="utf-8")))
    dbs = _resolve_dbs(args.db)
    if not args.json and not dbs:
        print("未找到剪映面板缓存，请先在剪映里打开一次「美妆」面板，或用 --db / --json 指定数据源", file=sys.stderr)
        return 2
    payloads.extend(_iter_panel_payloads(dbs))

    looks = _extract_looks(payloads)
    if not looks:
        print("面板缓存里没有「套装」数据（先在剪映里打开一次美妆面板再试）", file=sys.stderr)
        return 1

    content = _render(looks)
    if args.print_only:
        print(content)
        return 0

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"已写入 {out_path}：{len(looks)} 个套装（{sum(1 for v in looks.values() if v['is_vip'])} 个会员素材）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
