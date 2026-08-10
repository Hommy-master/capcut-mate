"""Unit tests for draft directory cleanup (oldest first, protected / locked / cached skips)."""
from __future__ import annotations

import os

from src.utils import draft_cleanup as dc


def _mkdir(p: str, name: str) -> str:
    path = os.path.join(p, name)
    os.makedirs(path, exist_ok=True)
    return path


def test_is_draft_directory_name_accepts_standard_id() -> None:
    assert dc.is_draft_directory_name("20200101000000aaaaaaaa") is True
    assert dc.is_draft_directory_name("20200101000000abcdef12") is True


def test_is_draft_directory_name_rejects_invalid() -> None:
    assert dc.is_draft_directory_name("20200101000000aaaaaaa") is False
    assert dc.is_draft_directory_name("20200101000000aaaaaaaag") is False
    assert dc.is_draft_directory_name("draft") is False
    assert dc.is_draft_directory_name("") is False


def test_list_sorted_draft_ids_ignores_files_and_bad_names(tmp_path) -> None:
    base = str(tmp_path)
    _mkdir(base, "20200201000000bbbbbbbb")
    _mkdir(base, "20200101000000aaaaaaaa")
    open(os.path.join(base, "x.mp4"), "wb").close()
    _mkdir(base, "not_a_valid_draft_id")
    got = dc.list_sorted_draft_ids(base)
    assert got == ["20200101000000aaaaaaaa", "20200201000000bbbbbbbb"]


def test_select_drafts_for_deletion_oldest_first_until_quota(tmp_path) -> None:
    ordered = [
        "20200101000000aaaaaaaa",
        "20200201000000bbbbbbbb",
        "20200301000000cccccccc",
    ]
    assert dc.select_drafts_for_deletion(ordered, max_keep=3, skip_ids=set()) == []
    assert dc.select_drafts_for_deletion(ordered, max_keep=2, skip_ids=set()) == [
        "20200101000000aaaaaaaa"
    ]
    assert dc.select_drafts_for_deletion(ordered, max_keep=1, skip_ids=set()) == [
        "20200101000000aaaaaaaa",
        "20200201000000bbbbbbbb",
    ]
    assert dc.select_drafts_for_deletion(ordered, max_keep=0, skip_ids=set()) == ordered


def test_select_drafts_for_deletion_skips_protected_uses_next_oldest() -> None:
    ordered = [
        "20200101000000aaaaaaaa",
        "20200201000000bbbbbbbb",
        "20200301000000cccccccc",
    ]
    skip = {"20200101000000aaaaaaaa"}
    assert dc.select_drafts_for_deletion(ordered, max_keep=1, skip_ids=skip) == [
        "20200201000000bbbbbbbb",
        "20200301000000cccccccc",
    ]


def test_run_one_draft_cleanup_deletes_oldest_unskipped_only(tmp_path) -> None:
    base = str(tmp_path)
    old = "20200101000000aaaaaaaa"
    mid = "20200201000000bbbbbbbb"
    new = "20200301000000cccccccc"
    for d in (old, mid, new):
        _mkdir(base, d)
    deleted = dc.run_one_draft_cleanup(
        draft_dir=base,
        max_keep=1,
        protected_ids=[],
        locked_ids=[],
        cached_ids=[],
    )
    assert set(deleted) == {old, mid}
    assert os.path.isdir(os.path.join(base, new))
    assert not os.path.exists(os.path.join(base, old))
    assert not os.path.exists(os.path.join(base, mid))


def test_run_one_draft_cleanup_never_removes_protected_ids(tmp_path) -> None:
    base = str(tmp_path)
    for pid in dc.DRAFT_CLEANUP_PROTECTED_DRAFT_IDS:
        _mkdir(base, pid)
    extra = "20990101000000eeeeeeee"
    _mkdir(base, extra)
    deleted = dc.run_one_draft_cleanup(
        draft_dir=base,
        max_keep=0,
        protected_ids=dc.DRAFT_CLEANUP_PROTECTED_DRAFT_IDS,
        locked_ids=[],
        cached_ids=[],
    )
    assert extra in deleted
    for pid in dc.DRAFT_CLEANUP_PROTECTED_DRAFT_IDS:
        assert pid not in deleted
        assert os.path.isdir(os.path.join(base, pid))


def test_run_one_draft_cleanup_skips_locked_ids(tmp_path) -> None:
    base = str(tmp_path)
    a, b, c = (
        "20200101000000aaaaaaaa",
        "20200201000000bbbbbbbb",
        "20200301000000cccccccc",
    )
    for d in (a, b, c):
        _mkdir(base, d)
    deleted = dc.run_one_draft_cleanup(
        draft_dir=base,
        max_keep=1,
        protected_ids=[],
        locked_ids=[a],
        cached_ids=[],
    )
    assert a not in deleted
    assert set(deleted) == {b, c}
    assert os.path.isdir(os.path.join(base, a))


def test_run_one_draft_cleanup_skips_cached_ids(tmp_path) -> None:
    base = str(tmp_path)
    a, b = "20200101000000aaaaaaaa", "20200201000000bbbbbbbb"
    for d in (a, b):
        _mkdir(base, d)
    deleted = dc.run_one_draft_cleanup(
        draft_dir=base,
        max_keep=1,
        protected_ids=[],
        locked_ids=[],
        cached_ids=[a],
    )
    assert a not in deleted
    assert deleted == [b]


def test_list_sorted_draft_ids_missing_dir_returns_empty(tmp_path) -> None:
    missing = os.path.join(str(tmp_path), "nope")
    assert dc.list_sorted_draft_ids(missing) == []
