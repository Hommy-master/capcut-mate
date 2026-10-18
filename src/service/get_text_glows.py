"""
发光(剪映「发光」文字效果)标识符解析的业务逻辑处理模块

发光与气泡、花字、文字模板在剪映数据模型里是四种不同的东西: 发光是``type="bloom"``
的素材, 挂在文本片段的``extra_material_refs``上, 只负责文字边缘的一层辉光, 不改动
文字本身的填充/描边/阴影。

与气泡一样, 发光的``effect_id``与``resource_id``**不是同一个值**, 例如剪映草稿中形如
``effect_id="9762443"``、``resource_id="7202576698775179837"``, 两者都需给出。
因此清单里两者分别记录, 也支持``"9762443:7202576698775179837"``这种显式 ID 对写法
来使用清单外的发光。

与气泡的差异: 发光素材还携带``bloom_params``(颜色/强度/范围/方向), 各预设的取值不同,
故清单里按预设记录该字段; 清单外的显式 ID 对无从得知其取值, 用
``DEFAULT_BLOOM_PARAMS``兜底。

清单目前只收录``发光``草稿实证过的 2 个预设(外发光/轮廓光); 需要更多时按同样的字段
格式增补(``id`` 为 resource_id, ``effect_id`` 单独给出, 两者缺一不可)。
"""
import json
import os
from typing import List, Dict, Any, Optional
from src.utils.logger import logger
from src.pyJianYingDraft.text_segment import DEFAULT_BLOOM_PARAMS
from config import PROJECT_ROOT

# 发光配置文件路径（固定路径，无需外部配置）
_GLOW_CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "glow.json")


# 进程启动时加载发光数据到内存
_GLOW_DATA: List[Dict[str, Any]] = []
_GLOW_MAP_BY_NAME: Dict[str, Dict[str, Any]] = {}
_GLOW_MAP_BY_RESOURCE_ID: Dict[str, Dict[str, Any]] = {}
_GLOW_MAP_BY_EFFECT_ID: Dict[str, Dict[str, Any]] = {}


def _normalize_glow(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """将配置项标准化为 resolve_text_glow 的返回格式

    ``id`` 是发光的``resource_id``(与花字/文字模板清单里 id 兼作 effect_id 的约定
    不同); ``effect_id`` 单独给出。两者缺一不可, 缺失则视为无效配置项——只填一个
    剪映定位不到该发光资源。
    """
    resource_id = str(item.get("id", "") or "").strip()
    effect_id = str(item.get("effect_id", "") or "").strip()
    if not resource_id or not effect_id:
        return None

    bloom_params = item.get("bloom_params")
    extra_material = item.get("material")
    return {
        "effect_id": effect_id,
        "resource_id": resource_id,
        "name": item.get("title", "") or "",
        "panel_id": str(item.get("panel_id", "") or "") or "text_glow",
        "bloom_params": dict(bloom_params) if isinstance(bloom_params, dict) else dict(DEFAULT_BLOOM_PARAMS),
        "extra_material": dict(extra_material) if isinstance(extra_material, dict) else {},
    }


def _load_glow_data() -> None:
    """在进程启动时加载发光数据到内存

    配置文件缺失或损坏时退化为空表并告警, 不影响显式 ID 对的调用方式。
    发光名称存在重复时, 名称查找固定取配置中靠前的一条, 需要精确定位请传
    resource_id 或显式 ID 对。
    """
    global _GLOW_DATA, _GLOW_MAP_BY_NAME, _GLOW_MAP_BY_RESOURCE_ID, _GLOW_MAP_BY_EFFECT_ID

    try:
        with open(_GLOW_CONFIG_PATH, "r", encoding="utf-8") as f:
            _GLOW_DATA = json.load(f)

        if not isinstance(_GLOW_DATA, list):
            raise ValueError("发光配置应为数组")

        duplicate_names = 0
        invalid_items = 0
        for item in _GLOW_DATA:
            if not isinstance(item, dict):
                continue
            glow_data = _normalize_glow(item)
            if glow_data is None:
                invalid_items += 1
                logger.warning(f"发光配置项缺少 id 或 effect_id, 已忽略: {item}")
                continue

            title = glow_data["name"]
            if title:
                # 重名取靠前的一条, 保证结果稳定且与配置顺序一致
                if title in _GLOW_MAP_BY_NAME:
                    duplicate_names += 1
                else:
                    _GLOW_MAP_BY_NAME[title] = glow_data
            _GLOW_MAP_BY_RESOURCE_ID[glow_data["resource_id"]] = glow_data
            # effect_id 是短数字(如 9762443), 可能被多个发光复用, 冲突时保留先出现的
            _GLOW_MAP_BY_EFFECT_ID.setdefault(glow_data["effect_id"], glow_data)

        logger.info(
            f"成功加载 {len(_GLOW_DATA)} 个发光到内存"
            f"（{len(_GLOW_MAP_BY_NAME)} 个不重名发光"
            f"{f'，{duplicate_names} 条重名已忽略' if duplicate_names else ''}"
            f"{f'，{invalid_items} 条无效配置已忽略' if invalid_items else ''}）"
        )

    except FileNotFoundError:
        logger.warning(
            f"发光配置文件不存在: {_GLOW_CONFIG_PATH}，"
            f"仅支持传入 \"effect_id:resource_id\" 显式 ID 对"
        )
        _GLOW_DATA = []
        _GLOW_MAP_BY_NAME = {}
        _GLOW_MAP_BY_RESOURCE_ID = {}
        _GLOW_MAP_BY_EFFECT_ID = {}
    except Exception as e:
        logger.error(f"加载发光数据失败: {str(e)}")
        _GLOW_DATA = []
        _GLOW_MAP_BY_NAME = {}
        _GLOW_MAP_BY_RESOURCE_ID = {}
        _GLOW_MAP_BY_EFFECT_ID = {}


# 模块导入时自动加载数据
_load_glow_data()


def _parse_explicit_pair(identifier: str) -> Optional[Dict[str, Any]]:
    """解析 ``"effect_id:resource_id"`` 显式 ID 对

    仅接受恰好一个冒号且两侧均非空的写法; 其余(含名称里带冒号的)一律视为不匹配,
    交由调用方回退为空表查找失败。清单外的发光没有实证的 bloom_params, 用默认值兜底。
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
        "panel_id": "text_glow",
        "bloom_params": dict(DEFAULT_BLOOM_PARAMS),
        "extra_material": {},
    }


def resolve_text_glow(glow_identifier: str) -> Optional[Dict[str, Any]]:
    """
    解析发光标识符，返回对应的发光信息

    Args:
        glow_identifier: 可取值:
            1. 发光名称（中文名称，如 "外发光"）
            2. resource_id（清单中的 ``id``，19 位云资源 id）
            3. effect_id（清单中的短数字 id，如 "9762443"）
            4. 显式 ID 对 ``"effect_id:resource_id"``，用于清单外的任意发光
        名称存在重名时固定命中配置中靠前的一条，需要精确定位请传 resource_id
        或显式 ID 对。

    Returns:
        发光信息字典，包含 effect_id、resource_id、name、panel_id、
        bloom_params 以及可选的 extra_material；未找到则返回 None
    """
    logger.debug(f"Resolving text glow: {glow_identifier}")

    if not isinstance(glow_identifier, str) or not glow_identifier.strip():
        logger.warning(f"Invalid text glow identifier: {glow_identifier!r}")
        return None

    identifier = glow_identifier.strip()

    # 1. 优先走清单: 名称 / resource_id / effect_id 三种精确命中
    if identifier in _GLOW_MAP_BY_NAME:
        return _GLOW_MAP_BY_NAME[identifier]
    if identifier in _GLOW_MAP_BY_RESOURCE_ID:
        return _GLOW_MAP_BY_RESOURCE_ID[identifier]
    if identifier in _GLOW_MAP_BY_EFFECT_ID:
        return _GLOW_MAP_BY_EFFECT_ID[identifier]

    # 2. 清单未命中时, 尝试显式 ID 对（清单外的任意发光）
    explicit_pair = _parse_explicit_pair(identifier)
    if explicit_pair is not None:
        # 清单外的发光没有实证的 bloom_params, 落到默认值。剪映不会按 resource_id
        # 重新推导颜色/强度/范围(它们只存在于 bloom_params 里), 故如实告警。
        logger.warning(
            f"未收录的发光 {identifier}，bloom_params 使用默认值"
            f"（外发光的实证取值）；如需精确复刻请加入 config/glow.json"
        )
        return explicit_pair

    # 3. 未找到。发光的 effect_id 与 resource_id 不同, 只给一个数字无法补全另一个,
    #    故不做「纯数字直接透传」, 由调用方回退为普通字幕
    logger.warning(
        f"Text glow not found: {identifier}，"
        f"清单外的发光请传入 \"effect_id:resource_id\" 显式 ID 对"
    )
    return None
