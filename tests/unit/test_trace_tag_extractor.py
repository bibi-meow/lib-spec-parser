"""Unit tests for trace_tag_extractor module."""

from lib_spec_parser.trace_tag_extractor import extract_trace_tags


class TestTraceTagExtractor:
    def test_single_tag(self):
        text = "Traces: FR-01"
        tags = extract_trace_tags(text)
        assert "FR-01" in tags

    def test_multiple_tags(self):
        text = "Traces: FR-01, US-03"
        tags = extract_trace_tags(text)
        assert "FR-01" in tags
        assert "US-03" in tags

    def test_custom_format(self):
        text = "Links: FR-02"
        tags = extract_trace_tags(text, trace_format="Links:")
        assert "FR-02" in tags

    def test_no_traces(self):
        text = "No traces in this text."
        assert extract_trace_tags(text) == []

    def test_traces_with_spaces(self):
        text = "Traces: REQ-001, REQ-002, US-05"
        tags = extract_trace_tags(text)
        assert len(tags) == 3

    def test_multiline_traces(self):
        text = "Some text.\nTraces: FR-01\nMore text."
        tags = extract_trace_tags(text)
        assert "FR-01" in tags
