from collections import OrderedDict
import src.pyJianYingDraft as draft
from typing import Dict

# Modify global variable, use OrderedDict to implement LRU cache, limit the maximum number to 10000
DRAFT_CACHE: Dict[str, 'draft.ScriptFile'] = OrderedDict()  # Use Dict for type hinting
MAX_CACHE_SIZE = 10000

def update_cache(key: str, value: draft.ScriptFile) -> None:
    """Update LRU cache"""
    if key in DRAFT_CACHE:
        # 如果当前key已经存在，就删除旧的
        DRAFT_CACHE.pop(key)
    elif len(DRAFT_CACHE) >= MAX_CACHE_SIZE:
        print(f"{key}, Cache is full, deleting the least recently used item")
        # 如果缓存已满，就删除最近最少使用的项（即第一个项）
        DRAFT_CACHE.popitem()
    # 添加到缓存的末尾（最近使用的）
    DRAFT_CACHE[key] = value