"""Unit tests: trace_tag_extractor."""

from __future__ import annotations

from lib_spec_parser.trace_tag_extractor import extract_trace_tags


def test_single_traces_line():
    text = "# Spec\nTraces: US-01, FR-02\n"
    tags = extract_trace_tags(text, "Traces:")
    assert len(tags) == 1
    assert tags[0].referenced_ids == ("US-01", "FR-02")
    assert tags[0].line_number == 2


def test_multiple_traces_lines():
    text = "Traces: US-01\nbody\nTraces: FR-01, AR-02\n"
    tags = extract_trace_tags(text, "Traces:")
    assert len(tags) == 2


def test_custom_trace_format():
    text = "Refs: AR-01\nTraces: FR-01\n"
    tags = extract_trace_tags(text, "Refs:")
    assert len(tags) == 1
    assert tags[0].referenced_ids == ("AR-01",)


def test_mixed_separators():
    text = "Traces: FR-01,US-02  AR-03\n"
    tags = extract_trace_tags(text, "Traces:")
    assert tags[0].referenced_ids == ("FR-01", "US-02", "AR-03")


def test_no_traces_returns_empty():
    text = "# Spec\nNo trace tags here.\n"
    tags = extract_trace_tags(text, "Traces:")
    assert tags == []


def test_raw_line_preserved():
    text = "Traces: US-01\n"
    tags = extract_trace_tags(text, "Traces:")
    assert "US-01" in tags[0].raw_line
