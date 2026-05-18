"""FR-02: TraceTag extraction from 'Traces: ...' patterns."""

from lib_spec_parser import ParserConfig, SpecParserExecutor


def _config(**params) -> ParserConfig:
    return ParserConfig(
        artifact_type="spec",
        executor_lib="lib-spec-parser",
        params=params,
    )


class TestFR02TraceTags:
    def test_single_trace_tag(self):
        content = b"## Section\n\nTraces: FR-01\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), content, "spec.md")
        tags = [t.raw for t in result.content.trace_tags]
        assert "FR-01" in tags

    def test_multiple_trace_tags(self):
        content = b"## Section\n\nTraces: FR-01, US-03\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), content, "spec.md")
        tags = [t.raw for t in result.content.trace_tags]
        assert "FR-01" in tags
        assert "US-03" in tags

    def test_custom_trace_format(self):
        content = b"## Section\n\nLinks: FR-02\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(trace_format="Links:"), content, "spec.md")
        tags = [t.raw for t in result.content.trace_tags]
        assert "FR-02" in tags

    def test_no_trace_tags(self):
        content = b"## Section\n\nNo traces here.\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), content, "spec.md")
        assert result.content.trace_tags == []

    def test_trace_tags_with_spaces(self):
        content = b"Traces: REQ-001, REQ-002, US-05\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), content, "spec.md")
        tags = [t.raw for t in result.content.trace_tags]
        assert "REQ-001" in tags
        assert "REQ-002" in tags
        assert "US-05" in tags
