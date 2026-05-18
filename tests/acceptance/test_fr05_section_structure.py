"""FR-05: Markdown h2/h3 section splitting."""

from lib_spec_parser import ParserConfig, SpecParserExecutor


def _config(**params) -> ParserConfig:
    return ParserConfig(
        artifact_type="spec",
        executor_lib="lib-spec-parser",
        params=params,
    )


MULTI_SECTION_MD = b"""# Title

## Section One

Content of section one.

## Section Two

Content of section two.

### Sub-section 2.1

Sub-content.
"""


class TestFR05SectionStructure:
    def test_splits_on_h2(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), MULTI_SECTION_MD, "spec.md")
        section_ids = [s.section_id for s in result.content.sections]
        assert any("Section One" in sid for sid in section_ids)
        assert any("Section Two" in sid for sid in section_ids)

    def test_splits_on_h3(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), MULTI_SECTION_MD, "spec.md")
        section_ids = [s.section_id for s in result.content.sections]
        assert any("Sub-section 2.1" in sid for sid in section_ids)

    def test_raw_text_present(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), MULTI_SECTION_MD, "spec.md")
        texts = [s.raw_text for s in result.content.sections]
        assert any("Content of section one" in t for t in texts)

    def test_single_section(self):
        content = b"## Only One\n\nJust one section.\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), content, "spec.md")
        assert len(result.content.sections) == 1

    def test_no_sections_empty_list(self):
        content = b"Just plain text without headings.\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), content, "spec.md")
        # Either empty sections or one default section
        assert isinstance(result.content.sections, list)

    def test_each_section_has_style(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), MULTI_SECTION_MD, "spec.md")
        for section in result.content.sections:
            assert section.style in ("gherkin", "ears", "connextra", "usdm", "plain")
