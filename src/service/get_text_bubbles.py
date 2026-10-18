"""
气泡(剪映「气泡」文字效果)标识符解析的业务逻辑处理模块

气泡与花字、文字模板在剪映数据模型里是三种不同的东西: 气泡是``type="text_shape"``
的素材, 挂在文本片段的``extra_material_refs``上, 只负责文字底下的装饰底板, 不改动
文字本身的填充/描边/阴影。

与花字/文字模板的关键差异: 气泡的``effect_id``与``resource_id``**不是同一个值**,
例如剪映草稿中形如``effect_id="716434"``、``resource_id="6821385652727190024"``,
两者都需给出。因此清单里两者分别记录, 也支持``"716434:6821385652727190024"``
这种显式 ID 对写法来使用清单外的气泡。

气泡素材的其余字段(本机缓存 path、request_id 等)取决于创建者本机的剪映缓存,
本服务侧无从得知, 由剪映按 effect_id/resource_id 自行拉取; 若需要精确复刻某个
气泡, 可在配置项的 "material" 字段中原样覆写这些字段。

清单目前只收录``气泡1``草稿实证过的 1 个气泡; 需要更多时按同样的字段格式增补
(``id`` 为 resource_id, ``effect_id`` 单独给出, 两者缺一不可)。
"""
import json
import os
from typing import List, Dict, Any, Optional
from src.utils.logger import logger
from config import PROJECT_ROOT

# 气泡配置文件路径（固定路径，无需外部配置）
_BUBBLE_CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "bubble.json")


# 进程启动时加载气泡数据到内存
_BUBBLE_DATA: List[Dict[str, Any]] = []
_BUBBLE_MAP_BY_NAME: Dict[str, Dict[str, Any]] = {}
_BUBBLE_MAP_BY_RESOURCE_ID: Dict[str, Dict[str, Any]] = {}
_BUBBLE_MAP_BY_EFFECT_ID: Dict[str, Dict[str, Any]] = {}


def _normalize_bubble(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """将配置项标准化为 resolve_text_bubble 的返回格式

    ``id`` 是气泡的``resource_id``(与花字/文字模板清单里 id 兼作 effect_id 的约定
    不同); ``effect_id`` 单独给出。两者缺一不可, 缺失则视为无效配置项——只填一个
    剪映定位不到该气泡资源。
    """
    resource_id = str(item.get("id", "") or "").strip()
    effect_id = str(item.get("effect_id", "") or "").strip()
    if not resource_id or not effect_id:
        return None

    extra_material = item.get("material")
    return {
        "effect_id": effect_id,
        "resource_id": resource_id,
        "name": item.get("title", "") or "",
        "category_id": str(item.get("category_id", "") or ""),
        "category_name": item.get("category_name", "") or "",
        "extra_material": dict(extra_material) if isinstance(extra_material, dict) else {},
    }


def _load_bubble_data() -> None:
    """在进程启动时加载气泡数据到内存

    配置文件缺失或损坏时退化为空表并告警, 不影响显式 ID 对的调用方式。
    气泡名称存在重复时, 名称查找固定取配置中靠前的一条, 需要精确定位请传
    resource_id 或显式 ID 对。
    """
    global _BUBBLE_DATA, _BUBBLE_MAP_BY_NAME, _BUBBLE_MAP_BY_RESOURCE_ID, _BUBBLE_MAP_BY_EFFECT_ID

    try:
        with open(_BUBBLE_CONFIG_PATH, "r", encoding="utf-8") as f:
            _BUBBLE_DATA = json.load(f)

        if not isinstance(_BUBBLE_DATA, list):
            raise ValueError("气泡配置应为数组")

        duplicate_names = 0
        invalid_items = 0
        for item in _BUBBLE_DATA:
            if not isinstance(item, dict):
                continue
            bubble_data = _normalize_bubble(item)
            if bubble_data is None:
                invalid_items += 1
                logger.warning(f"气泡配置项缺少 id 或 effect_id, 已忽略: {item}")
                continue

            title = bubble_data["name"]
            if title:
                # 重名取靠前的一条, 保证结果稳定且与配置顺序一致
                if title in _BUBBLE_MAP_BY_NAME:
                    duplicate_names += 1
                else:
                    _BUBBLE_MAP_BY_NAME[title] = bubble_data
            _BUBBLE_MAP_BY_RESOURCE_ID[bubble_data["resource_id"]] = bubble_data
            # effect_id 是短数字(如 716434), 可能被多个气泡复用, 冲突时保留先出现的
            _BUBBLE_MAP_BY_EFFECT_ID.setdefault(bubble_data["effect_id"], bubble_data)

        logger.info(
            f"成功加载 {len(_BUBBLE_DATA)} 个气泡到内存"
            f"（{len(_BUBBLE_MAP_BY_NAME)} 个不重名气泡"
            f"{f'，{duplicate_names} 条重名已忽略' if duplicate_names else ''}"
            f"{f'，{invalid_items} 条无效配置已忽略' if invalid_items else ''}）"
        )

    except FileNotFoundError:
        logger.warning(
            f"气泡配置文件不存在: {_BUBBLE_CONFIG_PATH}，"
            f"仅支持传入 \"effect_id:resource_id\" 显式 ID 对"
        )
        _BUBBLE_DATA = []
        _BUBBLE_MAP_BY_NAME = {}
        _BUBBLE_MAP_BY_RESOURCE_ID = {}
        _BUBBLE_MAP_BY_EFFECT_ID = {}
    except Exception as e:
        logger.error(f"加载气泡数据失败: {str(e)}")
        _BUBBLE_DATA = []
        _BUBBLE_MAP_BY_NAME = {}
        _BUBBLE_MAP_BY_RESOURCE_ID = {}
        _BUBBLE_MAP_BY_EFFECT_ID = {}


# 模块导入时自动加载数据
_load_bubble_data()


def _parse_explicit_pair(identifier: str) -> Optional[Dict[str, Any]]:
    """解析 ``"effect_id:resource_id"`` 显式 ID 对

    仅接受恰好一个冒号且两侧均非空的写法; 其余(含名称里带冒号的)一律视为不匹配,
    交由调用方回退为空表查找失败。
    """
    if identifier.count(":") != 1:
        return None

    effect_id, resource_id = (part.strip() for part in identifier.split(":"))
    if not effect_id or not resource_id:
        return None

    return {
        "effect_id": effect_id,
        "resource_id": resource_id,
        "name": "",
        "category_id": "",
        "category_name": "",
        "extra_material": {},
    }


def resolve_text_bubble(bubble_identifier: str) -> Optional[Dict[str, Any]]:
    """
    解析气泡标识符，返回对应的气泡信息

    Args:
        bubble_identifier: 可取值:
            1. 气泡名称（中文名称，如 "背景装饰54"）
            2. resource_id（清单中的 ``id``，19 位云资源 id）
            3. effect_id（清单中的短数字 id，如 "716434"）
            4. 显式 ID 对 ``"effect_id:resource_id"``，用于清单外的任意气泡
        名称存在重名时固定命中配置中靠前的一条，需要精确定位请传 resource_id
        或显式 ID 对。

    Returns:
        气泡信息字典，包含 effect_id、resource_id、name、category_id、
        category_name 以及可选的 extra_material；未找到则返回 None
    """
    logger.debug(f"Resolving text bubble: {bubble_identifier}")

    if not isinstance(bubble_identifier, str) or not bubble_identifier.strip():
        logger.warning(f"Invalid text bubble identifier: {bubble_identifier!r}")
        return None

    identifier = bubble_identifier.strip()

    # 1. 优先走清单: 名称 / resource_id / effect_id 三种精确命中
    if identifier in _BUBBLE_MAP_BY_NAME:
        return _BUBBLE_MAP_BY_NAME[identifier]
    if identifier in _BUBBLE_MAP_BY_RESOURCE_ID:
        return _BUBBLE_MAP_BY_RESOURCE_ID[identifier]
    if identifier in _BUBBLE_MAP_BY_EFFECT_ID:
        return _BUBBLE_MAP_BY_EFFECT_ID[identifier]

    # 2. 清单未命中时, 尝试显式 ID 对（清单外的任意气泡）
    explicit_pair = _parse_explicit_pair(identifier)
    if explicit_pair is not None:
        return explicit_pair

    # 3. 未找到。气泡的 effect_id 与 resource_id 不同, 只给一个数字无法补全另一个,
    #    故不做「纯数字直接透传」, 由调用方回退为普通字幕
    logger.warning(
        f"Text bubble not found: {identifier}，"
        f"清单外的气泡请传入 \"effect_id:resource_id\" 显式 ID 对"
    )
    return None
