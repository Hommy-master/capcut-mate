import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.service.add_captions import resolve_font_type
from src.pyJianYingDraft import FontType


def test_resolve_font_type_by_alias_zhixianghei():
    """支持通过“志向黑”别名解析字体。"""
    assert resolve_font_type("志向黑") == FontType.励字志向黑简_特粗


def test_resolve_font_type_by_display_name():
    """支持通过字体展示名解析。"""
    assert resolve_font_type("励字志向黑简 特粗") == FontType.励字志向黑简_特粗


def test_resolve_font_type_by_enum_name():
    """支持通过 FontType 枚举字段名解析。"""
    assert resolve_font_type("励字志向黑简_特粗") == FontType.励字志向黑简_特粗


def test_resolve_font_type_with_unknown_name():
    """未知字体名称应回退为默认字体（返回 None）。"""
    assert resolve_font_type("不存在的字体名称") is None
