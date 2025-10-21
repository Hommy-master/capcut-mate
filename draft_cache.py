from collections import OrderedDict
import pyJianYingDraft as draft
from typing import Dict

# Modify global variable, use OrderedDict to implement LRU cache, limit the maximum number to 10000
DRAFT_CACHE: Dict[str, 'draft.Script_file'] = OrderedDict()  # Use Dict for type hinting
MAX_CACHE_SIZE = 10000

def update_cache(key: str, value: draft.Script_file) -> None:
    """Update LRU cache"""
    if key in DRAFT_CACHE:
        # If the key exists, delete the old item
        DRAFT_CACHE.pop(key)
    elif len(DRAFT_CACHE) >= MAX_CACHE_SIZE:
        print(f"{key}, Cache is full, deleting the least recently used item")
        # If the cache is full, delete the least recently used item (the first item)
        DRAFT_CACHE.popitem(last=False)
    # Add new item to the end (most recently used)
    DRAFT_CACHE[key] = value