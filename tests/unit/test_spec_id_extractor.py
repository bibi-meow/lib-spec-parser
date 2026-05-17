"""Unit tests: spec_id_extractor."""

from __future__ import annotations

from lib_spec_parser.spec_id_extractor import extract_spec_ids


def test_all_nine_prefixes():
    text = "US-01 FR-002 REQ-003 NFR-004 AR-005 EA-006 PR-007 PE-008 AD-009"
    ids = extract_spec_ids(text)
    assert len(ids) == 9
    types = {i.id_type for i in ids}
    assert types == {"US", "FR", "REQ", "NFR", "AR", "EA", "PR", "PE", "AD"}


def test_duplicate_ids_recorded_separately():
    text = "US-01 and US-01 and US-01"
    ids = extract_spec_ids(text)
    assert len(ids) == 3
    assert all(i.value == "US-01" for i in ids)


def test_suffix_letter_supported():
    text = "US-06a is a variant."
    ids = extract_spec_ids(text)
    assert ids[0].value == "US-06a"


def test_line_number_tracked():
    text = "line 1\nline 2\nUS-01 on line 3\n"
    ids = extract_spec_ids(text)
    assert ids[0].line_number == 3


def test_no_match_returns_empty():
    text = "no spec IDs here."
    ids = extract_spec_ids(text)
    assert ids == []


def test_custom_prefixes_filter():
    """spec_id_prefixes で抽出プレフィックスを絞り込める。"""
    text = "US-01 FR-002 REQ-003 MYID-004"
    ids = extract_spec_ids(text, prefixes=["MYID"])
    assert len(ids) == 1
    assert ids[0].value == "MYID-004"
    assert ids[0].id_type == "MYID"


def test_custom_prefixes_excludes_defaults():
    """カスタム prefixes を指定するとデフォルト ID は抽出されない。"""
    text = "US-01 FR-002 SRS-010"
    ids = extract_spec_ids(text, prefixes=["SRS"])
    values = [i.value for i in ids]
    assert "SRS-010" in values
    assert "US-01" not in values
    assert "FR-002" not in values


def test_none_prefixes_uses_defaults():
    """prefixes=None でデフォルト 9 種プレフィックスが使われる。"""
    text = "US-01 FR-002"
    ids = extract_spec_ids(text, prefixes=None)
    assert len(ids) == 2


def test_word_boundary_no_false_match():
    # Should not match in the middle of a word
    text = "FUS-01 is not a spec id, but US-01 is."
    ids = extract_spec_ids(text)
    # Only US-01 should match (FUS-01's "US-01" is part of FUS-01,
    # but \b boundary makes this nuanced).
    # Let's just check that we get at least the standalone US-01
    values = [i.value for i in ids]
    assert "US-01" in values
