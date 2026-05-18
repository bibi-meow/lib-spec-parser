"""FR-07: Gherkin scenarios and EARS shall clauses extraction."""

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

Scenario: Failed login
  Given the user is on the login page
  When the user enters invalid credentials
  Then an error message is displayed
"""

EARS_CONTENT = b"""# System Requirements

## REQ-001 Basic Validation

When the user submits the form, the system shall validate the input.

## REQ-002 Loading State

While the system is processing, the system shall display a loading indicator.

## REQ-003 Always On

The system shall log all user actions.
"""


class TestFR07GherkinEARS:
    def test_gherkin_scenarios_extracted(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(spec_style="gherkin"), GHERKIN_CONTENT, "spec.md")
        gherkin_sections = [s for s in result.content.sections if s.style == "gherkin"]
        all_scenarios = []
        for s in gherkin_sections:
            all_scenarios.extend(s.scenarios)
        assert len(all_scenarios) >= 2

    def test_gherkin_steps_extracted(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(spec_style="gherkin"), GHERKIN_CONTENT, "spec.md")
        gherkin_sections = [s for s in result.content.sections if s.style == "gherkin"]
        all_steps = []
        for s in gherkin_sections:
            for scenario in s.scenarios:
                all_steps.extend(scenario.steps)
        assert any("Given" in step for step in all_steps)
        assert any("When" in step for step in all_steps)
        assert any("Then" in step for step in all_steps)

    def test_ears_shall_clauses_extracted(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(spec_style="ears"), EARS_CONTENT, "spec.md")
        ears_sections = [s for s in result.content.sections if s.style == "ears"]
        all_clauses = []
        for s in ears_sections:
            all_clauses.extend(s.shall_clauses)
        assert len(all_clauses) >= 1

    def test_ears_event_driven_pattern(self):
        event_req = b"## REQ-001\n\nWhen the user submits the form, the system shall validate.\n"
        content = event_req
        executor = SpecParserExecutor()
        result = executor.execute(_config(spec_style="ears"), content, "spec.md")
        ears_sections = [s for s in result.content.sections if s.style == "ears"]
        all_clauses = []
        for s in ears_sections:
            all_clauses.extend(s.shall_clauses)
        assert len(all_clauses) >= 1

    def test_gherkin_scenario_name(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(spec_style="gherkin"), GHERKIN_CONTENT, "spec.md")
        gherkin_sections = [s for s in result.content.sections if s.style == "gherkin"]
        names = []
        for s in gherkin_sections:
            names.extend(sc.name for sc in s.scenarios)
        assert any("Successful login" in n for n in names)
