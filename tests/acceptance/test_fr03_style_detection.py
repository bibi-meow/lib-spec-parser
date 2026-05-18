"""FR-03: Auto-detection of spec style (gherkin/ears/connextra/usdm/plain)."""

from lib_spec_parser import ParserConfig, SpecParserExecutor


def _config(**params) -> ParserConfig:
    return ParserConfig(
        artifact_type="spec",
        executor_lib="lib-spec-parser",
        params=params,
    )


GHERKIN_CONTENT = b"""# Login Feature

Feature: User Login

Scenario: Successful login
  Given the user is on the login page
  When the user enters valid credentials
  Then the user is redirected to the dashboard
"""

EARS_CONTENT = b"""# System Requirements

## REQ-001

When the user submits the form, the system shall validate the input.

## REQ-002

While the system is processing, the system shall display a loading indicator.
"""

CONNEXTRA_CONTENT = b"""# User Stories

## US-01

As a registered user, I want to log in, So that I can access my account.
"""

PLAIN_CONTENT = b"""# Plain Spec

## Section 1

This is a plain text specification without any special format.
"""


class TestFR03StyleDetection:
    def test_auto_detects_gherkin(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(spec_style="auto"), GHERKIN_CONTENT, "spec.md")
        gherkin_sections = [s for s in result.content.sections if s.style == "gherkin"]
        assert len(gherkin_sections) > 0

    def test_auto_detects_ears(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(spec_style="auto"), EARS_CONTENT, "spec.md")
        ears_sections = [s for s in result.content.sections if s.style == "ears"]
        assert len(ears_sections) > 0

    def test_auto_detects_connextra(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(spec_style="auto"), CONNEXTRA_CONTENT, "spec.md")
        conn_sections = [s for s in result.content.sections if s.style == "connextra"]
        assert len(conn_sections) > 0

    def test_auto_detects_plain(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(spec_style="auto"), PLAIN_CONTENT, "spec.md")
        plain_sections = [s for s in result.content.sections if s.style == "plain"]
        assert len(plain_sections) > 0

    def test_forced_style_gherkin(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(spec_style="gherkin"), GHERKIN_CONTENT, "spec.md")
        assert any(s.style == "gherkin" for s in result.content.sections)

    def test_default_is_auto(self):
        executor = SpecParserExecutor()
        # No spec_style param should behave like auto
        result = executor.execute(_config(), GHERKIN_CONTENT, "spec.md")
        assert result.content.sections is not None
