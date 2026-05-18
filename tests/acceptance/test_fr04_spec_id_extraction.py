"""FR-04: SpecId extraction for US-XX, FR-NNN, REQ-NNN, etc."""

from lib_spec_parser import ParserConfig, SpecParserExecutor


def _config(**params) -> ParserConfig:
    return ParserConfig(
        artifact_type="spec",
        executor_lib="lib-spec-parser",
        params=params,
    )


class TestFR04SpecIdExtraction:
    def test_extracts_us_id(self):
        content = b"## US-01 Login\n\nUser should be able to log in.\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), content, "spec.md")
        ids = [s.value for s in result.content.spec_ids]
        assert "US-01" in ids

    def test_extracts_fr_id(self):
        content = b"FR-003 must be implemented.\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), content, "spec.md")
        ids = [s.value for s in result.content.spec_ids]
        assert "FR-003" in ids

    def test_extracts_req_id(self):
        content = b"REQ-007: The system shall respond within 200ms.\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), content, "spec.md")
        ids = [s.value for s in result.content.spec_ids]
        assert "REQ-007" in ids

    def test_extracts_nfr_id(self):
        content = b"NFR-01: Performance requirement.\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), content, "spec.md")
        ids = [s.value for s in result.content.spec_ids]
        assert "NFR-01" in ids

    def test_extracts_multiple_ids(self):
        content = b"US-01 and FR-002 and REQ-003 are related.\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), content, "spec.md")
        ids = [s.value for s in result.content.spec_ids]
        assert "US-01" in ids
        assert "FR-002" in ids
        assert "REQ-003" in ids

    def test_no_ids_returns_empty(self):
        content = b"No IDs in this text.\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), content, "spec.md")
        assert result.content.spec_ids == []

    def test_extract_ids_false_skips_extraction(self):
        content = b"US-01 and FR-002.\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(extract_ids=False), content, "spec.md")
        assert result.content.spec_ids == []

    def test_custom_prefixes(self):
        content = b"AR-01 and AD-02 are architecture decisions.\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), content, "spec.md")
        ids = [s.value for s in result.content.spec_ids]
        assert "AR-01" in ids
        assert "AD-02" in ids
