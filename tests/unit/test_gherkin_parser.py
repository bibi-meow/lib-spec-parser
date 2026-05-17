"""Unit tests: gherkin_parser."""

from __future__ import annotations

from lib_spec_parser.parsers.gherkin_parser import parse_gherkin


def test_single_scenario():
    text = """Feature: Auth
  Scenario: Login
    Given user
    When click
    Then ok
"""
    scenarios = parse_gherkin(text)
    assert len(scenarios) == 1
    assert scenarios[0].name == "Login"
    assert scenarios[0].given == ("user",)
    assert scenarios[0].when == ("click",)
    assert scenarios[0].then == ("ok",)


def test_and_steps_attach_to_previous_type():
    text = """Feature: x
  Scenario: y
    Given a
    And b
    When c
    And d
    Then e
    And f
"""
    scenarios = parse_gherkin(text)
    assert scenarios[0].given == ("a", "b")
    assert scenarios[0].when == ("c", "d")
    assert scenarios[0].then == ("e", "f")


def test_multiple_scenarios():
    text = """Feature: x
  Scenario: A
    Given a
    When b
    Then c
  Scenario: B
    Given d
    When e
    Then f
"""
    scenarios = parse_gherkin(text)
    assert len(scenarios) == 2
    assert scenarios[0].name == "A"
    assert scenarios[1].name == "B"


def test_scenario_outline_examples():
    text = """Feature: x
  Scenario Outline: parameterized
    Given <a>
    When <b>
    Then <c>

    Examples:
      | a | b | c |
      | 1 | 2 | 3 |
      | 4 | 5 | 6 |
"""
    scenarios = parse_gherkin(text)
    assert len(scenarios) == 1
    assert len(scenarios[0].examples) == 2
    ex = scenarios[0].examples[0]
    assert ex == {"a": "1", "b": "2", "c": "3"}


def test_empty_input():
    assert parse_gherkin("") == []
    assert parse_gherkin("just plain text") == []
