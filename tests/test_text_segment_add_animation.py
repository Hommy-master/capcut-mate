"""TextSegment.add_animation：循环动画修正后的回归与行为测试。

保证入场/出场逻辑不变；循环动画 start 在入场结束后，duration 为单次循环时长（可受中间空隙限制）。
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from src.pyJianYingDraft.text_segment import TextSegment, TextStyle
from src.pyJianYingDraft.time_util import Timerange
from src.pyJianYingDraft.metadata import TextIntro, TextOutro, TextLoopAnim


def _anim(seg: TextSegment, animation_type: str):
    assert seg.animations_instance is not None
    return next(a for a in seg.animations_instance.animations if a.animation_type == animation_type)


# --- 入场 / 出场：与改动前一致 ---


def test_intro_only_start_zero_and_respects_duration():
    seg = TextSegment("t", Timerange(0, 10_000_000), style=TextStyle())
    seg.add_animation(TextIntro.弹入, duration=400_000)
    a = _anim(seg, "in")
    assert a.start == 0
    assert a.duration == 400_000


def test_outro_only_start_is_segment_end_minus_duration():
    seg = TextSegment("t", Timerange(0, 10_000_000), style=TextStyle())
    seg.add_animation(TextOutro.弹弓, duration=600_000)
    a = _anim(seg, "out")
    assert a.start == 10_000_000 - 600_000
    assert a.duration == 600_000


def test_intro_then_outro_both_unchanged():
    seg = TextSegment("t", Timerange(0, 10_000_000), style=TextStyle())
    seg.add_animation(TextIntro.弹入, duration=500_000)
    seg.add_animation(TextOutro.弹弓, duration=500_000)
    tin, tout = _anim(seg, "in"), _anim(seg, "out")
    assert tin.start == 0 and tin.duration == 500_000
    assert tout.start == 9_500_000 and tout.duration == 500_000


def test_intro_duration_still_capped_by_segment_length():
    """公共前缀 min(tim(duration), segment) 对入场仍生效。"""
    seg = TextSegment("t", Timerange(0, 300_000), style=TextStyle())
    seg.add_animation(TextIntro.弹入, duration=500_000)
    assert _anim(seg, "in").duration == 300_000


def test_outro_duration_still_capped_by_segment_length():
    seg = TextSegment("t", Timerange(0, 400_000), style=TextStyle())
    seg.add_animation(TextOutro.弹弓, duration=900_000)
    tout = _anim(seg, "out")
    assert tout.duration == 400_000
    assert tout.start == 0


# --- 循环动画：新语义 ---


def test_loop_only_start_zero_uses_explicit_cycle():
    seg = TextSegment("t", Timerange(0, 8_000_000), style=TextStyle())
    seg.add_animation(TextLoopAnim.旋转, duration=1_200_000)
    lo = _anim(seg, "loop")
    assert lo.start == 0
    assert lo.duration == 1_200_000


def test_loop_only_cycle_limited_by_segment_before_loop_branch():
    """先被全局 min(..., segment) 限制，再在 loop 分支与 available 取 min。"""
    seg = TextSegment("t", Timerange(0, 1_000_000), style=TextStyle())
    seg.add_animation(TextLoopAnim.旋转, duration=3_000_000)
    lo = _anim(seg, "loop")
    assert lo.start == 0
    assert lo.duration == 1_000_000


def test_loop_none_duration_uses_enum_default_microseconds():
    # 旋转 元数据默认 0.5s
    seg = TextSegment("t", Timerange(0, 5_000_000), style=TextStyle())
    seg.add_animation(TextLoopAnim.旋转, duration=None)
    lo = _anim(seg, "loop")
    assert lo.start == 0
    assert lo.duration == 500_000


def test_loop_after_intro_outro_starts_at_intro_end():
    seg = TextSegment("t", Timerange(0, 10_000_000), style=TextStyle())
    seg.add_animation(TextIntro.弹入, duration=500_000)
    seg.add_animation(TextOutro.弹弓, duration=500_000)
    seg.add_animation(TextLoopAnim.旋转, duration=1_000_000)
    tin, tout, lo = _anim(seg, "in"), _anim(seg, "out"), _anim(seg, "loop")
    assert tin.start == 0 and tin.duration == 500_000
    assert tout.start == 9_500_000 and tout.duration == 500_000
    assert lo.start == 500_000
    assert lo.duration == 1_000_000


def test_loop_cycle_capped_by_available_between_in_and_out():
    seg = TextSegment("t", Timerange(0, 2_000_000), style=TextStyle())
    seg.add_animation(TextIntro.弹入, duration=800_000)
    seg.add_animation(TextOutro.弹弓, duration=800_000)
    # 中间仅剩 400_000 μs；请求 3s 单次循环，先被 min(..., 2s) 成 2s，再 cap 到 400_000
    seg.add_animation(TextLoopAnim.旋转, duration=3_000_000)
    lo = _anim(seg, "loop")
    assert lo.start == 800_000
    assert lo.duration == 400_000


def test_loop_accepts_int_duration_microseconds():
    seg = TextSegment("t", Timerange(0, 6_000_000), style=TextStyle())
    seg.add_animation(TextLoopAnim.旋转, duration=900_000)
    assert _anim(seg, "loop").duration == 900_000


def test_add_in_out_loop_order_required_by_contract():
    """与文档一致：先入场、再出场、再循环。"""
    seg = TextSegment("t", Timerange(0, 10_000_000), style=TextStyle())
    seg.add_animation(TextIntro.弹入, duration=100_000)
    seg.add_animation(TextOutro.弹弓, duration=100_000)
    seg.add_animation(TextLoopAnim.旋转, duration=200_000)
    assert len(seg.animations_instance.animations) == 3


def test_add_loop_before_in_raises():
    seg = TextSegment("t", Timerange(0, 5_000_000), style=TextStyle())
    seg.add_animation(TextLoopAnim.旋转, duration=500_000)
    with pytest.raises(ValueError, match="入出场动画"):
        seg.add_animation(TextIntro.弹入, duration=100_000)
