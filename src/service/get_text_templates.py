"""
文字模板(剪映「文字模板」)标识符解析的业务逻辑处理模块

模板清单维护在 config/text_template.json，字段为 id/title/is_vip/category_id/
category_name。模板素材本机缓存相关的字段(path/resources/装饰贴纸等)无法在本
服务侧得知，由剪映按 effect_id/resource_id 自行拉取；若需要精确复刻某个模板，
可在配置项的 "material" 字段中原样覆写这些字段。

注意 id 即剪映的 effect_id/resource_id，两者同值；is_vip 仅作筛选标记，未购买
的 VIP 模板在剪映侧可能无法渲染。
"""
import json
import os
from typing import List, Dict, Any, Optional
from src.utils.logger import logger
from config import PROJECT_ROOT

# 文字模板配置文件路径（固定路径，无需外部配置）
_TEXT_TEMPLATE_CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "text_template.json")


# 进程启动时加载文字模板数据到内存
_TEXT_TEMPLATE_DATA: List[Dict[str, Any]] = []
_TEXT_TEMPLATE_MAP_BY_NAME: Dict[str, Dict[str, Any]] = {}
_TEXT_TEMPLATE_MAP_BY_ID: Dict[str, Dict[str, Any]] = {}


def _normalize_text_template(item: Dict[str, Any]) -> Dict[str, Any]:
    """将配置项标准化为 resolve_text_template 的返回格式"""
    resource_id = str(item.get("id", "") or "")
    extra_material = item.get("material")
    return {
        "effect_id": resource_id,
        "resource_id": resource_id,
        "name": item.get("title", "") or "",
        "category_id": str(item.get("category_id", "") or ""),
        "category_name": item.get("category_name", "") or "",
        "extra_material": dict(extra_material) if isinstance(extra_material, dict) else {},
    }


def _load_text_template_data() -> None:
    """在进程启动时加载文字模板数据到内存

    配置文件缺失或损坏时退化为空表并告警，不影响纯 effect_id 的调用方式。
    模板名称存在重复（如多个「我的水印」），名称查找固定取配置中靠前的一条，
    需要精确定位时请传 effect_id。
    """
    global _TEXT_TEMPLATE_DATA, _TEXT_TEMPLATE_MAP_BY_NAME, _TEXT_TEMPLATE_MAP_BY_ID

    try:
        with open(_TEXT_TEMPLATE_CONFIG_PATH, "r", encoding="utf-8") as f:
            _TEXT_TEMPLATE_DATA = json.load(f)

        if not isinstance(_TEXT_TEMPLATE_DATA, list):
            raise ValueError("文字模板配置应为数组")

        duplicate_names = 0
        for item in _TEXT_TEMPLATE_DATA:
            if not isinstance(item, dict):
                continue
            template_data = _normalize_text_template(item)
            title = template_data["name"]
            resource_id = template_data["resource_id"]

            if title:
                # 重名取靠前的一条，保证结果稳定且与配置顺序一致
                if title in _TEXT_TEMPLATE_MAP_BY_NAME:
                    duplicate_names += 1
                else:
                    _TEXT_TEMPLATE_MAP_BY_NAME[title] = template_data
            if resource_id:
                _TEXT_TEMPLATE_MAP_BY_ID[resource_id] = template_data

        logger.info(
            f"成功加载 {len(_TEXT_TEMPLATE_DATA)} 个文字模板到内存"
            f"（{len(_TEXT_TEMPLATE_MAP_BY_NAME)} 个不重名模板"
            f"{f'，{duplicate_names} 条重名已忽略' if duplicate_names else ''}）"
        )

    except FileNotFoundError:
        logger.warning(
            f"文字模板配置文件不存在: {_TEXT_TEMPLATE_CONFIG_PATH}，"
            f"仅支持直接传入 effect_id"
        )
        _TEXT_TEMPLATE_DATA = []
        _TEXT_TEMPLATE_MAP_BY_NAME = {}
        _TEXT_TEMPLATE_MAP_BY_ID = {}
    except Exception as e:
        logger.error(f"加载文字模板数据失败: {str(e)}")
        _TEXT_TEMPLATE_DATA = []
        _TEXT_TEMPLATE_MAP_BY_NAME = {}
        _TEXT_TEMPLATE_MAP_BY_ID = {}


# 模块导入时自动加载数据
_load_text_template_data()


def resolve_text_template(template_identifier: str) -> Optional[Dict[str, Any]]:
    """
    解析文字模板标识符，返回对应的模板信息

    Args:
        template_identifier: 可以是 effect_id（数字字符串）或模板名称（中文名称）。
            名称存在重名时固定命中配置中靠前的一条，需要精确定位请传 effect_id。

    Returns:
        文字模板信息字典，包含 effect_id、resource_id、name、category_id、
        category_name 以及可选的 extra_material；未找到则返回 None
    """
    logger.debug(f"Resolving text template: {template_identifier}")

    if not isinstance(template_identifier, str) or not template_identifier:
        logger.warning(f"Invalid text template identifier: {template_identifier!r}")
        return None

    # 1. 尝试作为中文名称查找
    if template_identifier in _TEXT_TEMPLATE_MAP_BY_NAME:
        return _TEXT_TEMPLATE_MAP_BY_NAME[template_identifier]

    # 2. 尝试作为 effect_id 查找
    if template_identifier in _TEXT_TEMPLATE_MAP_BY_ID:
        return _TEXT_TEMPLATE_MAP_BY_ID[template_identifier]

    # 3. 如果是纯数字但不在映射表中，直接使用（可能是新的 effect_id）
    if template_identifier.isdigit():
        return {
            "effect_id": template_identifier,
            "resource_id": template_identifier,
            "name": "",
            "category_id": "",
            "category_name": "",
            "extra_material": {},
        }

    # 4. 未找到
    logger.warning(f"Text template not found: {template_identifier}")
    return None
