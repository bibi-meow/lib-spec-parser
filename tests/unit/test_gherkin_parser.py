"""Unit tests for gherkin_parser module."""

from lib_spec_parser.parsers.gherkin_parser import parse_gherkin

GHERKIN_TEXT = """Feature: Login

Scenario: Successful login
  Given the user is on the login page
  When the user enters valid credentials
  Then the user is redirected to the dashboard

Scenario: Failed login
  Given the user is on the login page
  When the user enters invalid credentials
  Then an error message is displayed
"""


class TestGherkinParser:
    def test_extracts_two_scenarios(self):
        scenarios = parse_gherkin(GHERKIN_TEXT)
        assert len(scenarios) == 2

    def test_scenario_names(self):
        scenarios = parse_gherkin(GHERKIN_TEXT)
        names = [s.name for s in scenarios]
        assert "Successful login" in names
        assert "Failed login" in names

    def test_scenario_steps(self):
        scenarios = parse_gherkin(GHERKIN_TEXT)
        first = next(s for s in scenarios if s.name == "Successful login")
        assert len(first.steps) == 3

    def test_step_content(self):
        scenarios = parse_gherkin(GHERKIN_TEXT)
        first = next(s for s in scenarios if s.name == "Successful login")
        assert any("Given" in step for step in first.steps)

    def test_no_scenarios_returns_empty(self):
        text = "Just plain text."
        scenarios = parse_gherkin(text)
        assert scenarios == []

    def test_keywords_detected(self):
        keywords = parse_gherkin(GHERKIN_TEXT, return_keywords=True)
        # Returns list of keywords found
        assert isinstance(keywords, list)
