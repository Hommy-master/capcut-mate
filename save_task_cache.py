from collections import OrderedDict
import threading
from typing import Dict, Any

# Using OrderedDict to implement LRU cache, limiting the maximum number to 1000
DRAFT_TASKS: Dict[str, dict] = OrderedDict()  # Using Dict for type hinting
MAX_TASKS_CACHE_SIZE = 1000


def update_tasks_cache(task_id: str, task_status: dict) -> None:
    """Update task status LRU cache
    
    :param task_id: Task ID
    :param task_status: Task status information dictionary
    """

    if task_id in DRAFT_TASKS:
        # If the key exists, delete the old item
        DRAFT_TASKS.pop(task_id)
    elif len(DRAFT_TASKS) >= MAX_TASKS_CACHE_SIZE:
        # If the cache is full, delete the least recently used item (the first item)
        DRAFT_TASKS.popitem(last=False)
    # Add new item to the end (most recently used)
    DRAFT_TASKS[task_id] = task_status

def update_task_field(task_id: str, field: str, value: Any) -> None:
    """Update a single field in the task status
    
    :param task_id: Task ID
    :param field: Field name to update
    :param value: New value for the field
    """
    if task_id in DRAFT_TASKS:
        # Copy the current status, modify the specified field, then update the cache
        task_status = DRAFT_TASKS[task_id].copy()
        task_status[field] = value
        # Delete the old item and add the updated item
        DRAFT_TASKS.pop(task_id)
        DRAFT_TASKS[task_id] = task_status
    else:
        # If the task doesn't exist, create a default status and set the specified field
        task_status = {
            "status": "initialized",
            "message": "Task initialized",
            "progress": 0,
            "completed_files": 0,
            "total_files": 0,
            "draft_url": ""
        }
        task_status[field] = value
        # If the cache is full, delete the least recently used item
        if len(DRAFT_TASKS) >= MAX_TASKS_CACHE_SIZE:
            DRAFT_TASKS.popitem(last=False)
        # Add new item
        DRAFT_TASKS[task_id] = task_status

def update_task_fields(task_id: str, **fields) -> None:
    """Update multiple fields in the task status
    
    :param task_id: Task ID
    :param fields: Fields to update and their values, provided as keyword arguments
    """
    if task_id in DRAFT_TASKS:
        # Copy the current status, modify the specified fields, then update the cache
        task_status = DRAFT_TASKS[task_id].copy()
        for field, value in fields.items():
            task_status[field] = value
        # Delete the old item and add the updated item
        DRAFT_TASKS.pop(task_id)
        DRAFT_TASKS[task_id] = task_status
    else:
        # If the task doesn't exist, create a default status and set the specified fields
        task_status = {
            "status": "initialized",
            "message": "Task initialized",
            "progress": 0,
            "completed_files": 0,
            "total_files": 0,
            "draft_url": ""
        }
        for field, value in fields.items():
            task_status[field] = value
        # If the cache is full, delete the least recently used item
        if len(DRAFT_TASKS) >= MAX_TASKS_CACHE_SIZE:
            DRAFT_TASKS.popitem(last=False)
        # Add new item
        DRAFT_TASKS[task_id] = task_status

def increment_task_field(task_id: str, field: str, increment: int = 1) -> None:
    """Increment a numeric field in the task status
    
    :param task_id: Task ID
    :param field: Field name to increment
    :param increment: Value to increment by, default is 1
    """
    if task_id in DRAFT_TASKS:
        # Copy the current status, increment the specified field, then update the cache
        task_status = DRAFT_TASKS[task_id].copy()
        if field in task_status and isinstance(task_status[field], (int, float)):
            task_status[field] += increment
        else:
            task_status[field] = increment
        # Delete the old item and add the updated item
        DRAFT_TASKS.pop(task_id)
        DRAFT_TASKS[task_id] = task_status

def get_task_status(task_id: str) -> dict:
    """Get task status
    
    :param task_id: Task ID
    :return: Task status information dictionary
    """
    task_status = DRAFT_TASKS.get(task_id, {
        "status": "not_found",
        "message": "Task does not exist",
        "progress": 0,
        "completed_files": 0,
        "total_files": 0,
        "draft_url": ""
    })
    
    # If the task is found, update its position in the LRU cache
    if task_id in DRAFT_TASKS:
        # First delete, then add to the end, implementing LRU update
        update_tasks_cache(task_id, task_status)
        
    return task_status

def create_task(task_id: str) -> None:
    """Create a new task and initialize its status
    
    :param task_id: Task ID
    """
    task_status = {
        "status": "initialized",
        "message": "Task initialized",
        "progress": 0,
        "completed_files": 0,
        "total_files": 0,
        "draft_url": ""
    }
    update_tasks_cache(task_id, task_status)