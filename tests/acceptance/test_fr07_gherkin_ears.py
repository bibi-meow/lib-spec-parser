"""LIB-FR-07 acceptance tests: Gherkin/EARS extraction.

Traces: LIB-FR-07, US-L-07
"""

from __future__ import annotations

from lib_spec_parser.parsers.ears_classifier import classify_ears
from lib_spec_parser.parsers.gherkin_parser import parse_gherkin


def test_gherkin_given_when_then_counts():
    text = """Feature: Test
  Scenario: Sample
    Given step1
    And step2
    When action
    Then result
"""
    scenarios = parse_gherkin(text)
    assert len(scenarios) == 1
    assert len(scenarios[0].given) == 2
    assert len(scenarios[0].when) == 1
    assert len(scenarios[0].then) == 1


def test_gherkin_scenario_outline_examples():
    text = """Feature: Test
  Scenario Outline: Outlined
    Given <a>
    When <b>
    Then <c>

    Examples:
      | a | b | c |
      | 1 | 2 | 3 |
      | 4 | 5 | 6 |
      | 7 | 8 | 9 |
"""
    scenarios = parse_gherkin(text)
    assert len(scenarios) == 1
    assert len(scenarios[0].examples) == 3
    # Each example should be a dict with the column names as keys
    for ex in scenarios[0].examples:
        assert "a" in ex
        assert "b" in ex
        assert "c" in ex


def test_ears_five_patterns_classified():
    text = """The system shall be available.
When a request arrives, the system shall log it.
While the system is in standby, the system shall conserve power.
Where the user is admin, the system shall allow access.
If an error occurs, then the system shall roll back."""
    clauses = classify_ears(text)
    assert len(clauses) == 5
    patterns = {c["ears_pattern"] for c in clauses}
    # All 5 EARS patterns should be present
    assert patterns == {
        "ubiquitous",
        "event_driven",
        "state_driven",
        "optional",
        "unwanted",
    }


def test_multiple_scenarios_independent():
    text = """Feature: Test
  Scenario: One
    Given a
    When b
    Then c
  Scenario: Two
    Given d
    When e
    Then f
  Scenario: Three
    Given g
    When h
    Then i
"""
    scenarios = parse_gherkin(text)
    assert len(scenarios) == 3
    assert scenarios[0].name == "One"
    assert scenarios[1].name == "Two"
    assert scenarios[2].name == "Three"


def test_gherkin_scenario_name():
    text = """Feature: Auth
  Scenario: Login flow
    Given user
    When click
    Then success
"""
    scenarios = parse_gherkin(text)
    assert scenarios[0].name == "Login flow"
