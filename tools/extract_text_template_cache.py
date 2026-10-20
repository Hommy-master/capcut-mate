"""从本机剪映缓存补全 config/text_template.json 的 resources/animation 字段

剪映缓存结构：
  artistEffect/<模板effect_id>/<资源hash>/extra.json
  artistEffect/<模板effect_id>/<资源hash>/content.json

字段对应关系：
  extra.json 的 depend_resource_list -> 草稿模板素材的 resources
    type           -> panel
    source         -> source_platform（缓存 source 1 对应 1，其余对应 0）
    资源 path 一律留空，由剪映按 resource_id 拉取
  content.json 文本子节点的 anims 中 anim_type == "in" -> 草稿的入场动画
    anim_resource_id -> resource_id
    anim_start_time  -> start（秒转微秒）
    duration         -> duration（秒转微秒）

content.json 有两种结构，均需支持：
  ScriptTemplate：顶层 children
  TextTemplate：root.children
"""
import argparse
import json
import os
import sys

DEFAULT_CACHE_DIR = os.path.expanduser(
    "~/Movies/JianyingPro/User Data/Cache/artistEffect"
)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "text_template.json")


def _children(content):
    """兼容 ScriptTemplate(顶层 children) 与 TextTemplate(root.children)"""
    if isinstance(content.get("children"), list):
        return content["children"]
    root = content.get("root")
    if isinstance(root, dict) and isinstance(root.get("children"), list):
        return root["children"]
    return []


def _pick_cache_dir(cache_root, template_id):
    """同一模板存在多份缓存时，取修改时间最新且含 extra.json 的一份"""
    template_dir = os.path.join(cache_root, template_id)
    if not os.path.isdir(template_dir):
        return None
    candidates = [
        os.path.join(template_dir, name)
        for name in os.listdir(template_dir)
        if os.path.isfile(os.path.join(template_dir, name, "extra.json"))
    ]
    return max(candidates, key=os.path.getmtime) if candidates else None


def _extract(cache_root, template_id):
    """提取单个模板的 resources 与 animation，缓存缺失时返回 None"""
    cache_dir = _pick_cache_dir(cache_root, template_id)
    if cache_dir is None:
        return None

    with open(os.path.join(cache_dir, "extra.json"), encoding="utf-8") as f:
        extra = json.load(f)
    content_path = os.path.join(cache_dir, "content.json")
    if not os.path.isfile(content_path):
        return None
    with open(content_path, encoding="utf-8") as f:
        content = json.load(f)

    resources = []
    for depend in extra.get("depend_resource_list") or []:
        resource_id = str(depend.get("resource_id", "") or "")
        if not resource_id:
            continue
        resources.append({
            "panel": str(depend.get("type", "") or ""),
            "path": "",
            "resource_id": resource_id,
            # 剪映缓存里 source=1 的资源对应草稿的 source_platform=1（artistEffect），
            # source=2 或旧格式缺省值对应 0（effect）
            "source_platform": 1 if depend.get("source") == 1 else 0,
        })

    animation = None
    for child in _children(content):
        if child.get("type") != "text":
            continue
        for anim in child.get("anims") or []:
            if anim.get("anim_type") != "in" or not anim.get("anim_resource_id"):
                continue
            animation = {
                "type": "in",
                "start": int(round(float(anim.get("anim_start_time", 0) or 0) * 1_000_000)),
                "duration": int(round(float(anim.get("duration", 0) or 0) * 1_000_000)),
                "resource_id": str(anim["anim_resource_id"]),
                "path": "",
            }
            break
        if animation is not None:
            break

    return {"resources": resources, "animation": animation}


def _dump_config(entries):
    """保持配置一行一个模板对象的原有格式"""
    lines = ["["]
    for index, entry in enumerate(entries):
        suffix = "," if index < len(entries) - 1 else ""
        lines.append(json.dumps(entry, ensure_ascii=False) + suffix)
    lines.append("]")
    return "\n".join(lines) + "\n"


def _merge_entry(entry, extracted):
    """只补写提取到的字段，不删除配置里已有的其它数据"""
    if extracted["resources"]:
        entry["resources"] = extracted["resources"]
    if extracted["animation"]:
        entry["animation"] = extracted["animation"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR,
                        help="剪映 artistEffect 缓存目录")
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH,
                        help="text_template.json 路径")
    parser.add_argument("--write", action="store_true",
                        help="写回配置；不加此参数时只打印统计")
    args = parser.parse_args()

    if not os.path.isdir(args.cache_dir):
        print(f"缓存目录不存在: {args.cache_dir}", file=sys.stderr)
        return 1

    with open(args.config, encoding="utf-8") as f:
        entries = json.load(f)

    cached = resources_count = animation_count = 0
    for entry in entries:
        template_id = str(entry.get("id", "") or "")
        extracted = _extract(args.cache_dir, template_id)
        if extracted is None:
            continue
        cached += 1
        if extracted["resources"]:
            resources_count += 1
        if extracted["animation"]:
            animation_count += 1
        _merge_entry(entry, extracted)

    print(f"配置模板数: {len(entries)}")
    print(f"命中缓存: {cached}")
    print(f"可写入 resources: {resources_count}")
    print(f"可写入 animation: {animation_count}")

    if args.write:
        with open(args.config, "w", encoding="utf-8") as f:
            f.write(_dump_config(entries))
        print(f"已写入: {args.config}")
    else:
        print("未写入（加 --write 生效）")

    return 0


if __name__ == "__main__":
    sys.exit(main())
