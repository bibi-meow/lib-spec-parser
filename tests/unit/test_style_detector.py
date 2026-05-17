"""Unit tests: style_detector."""

from __future__ import annotations

from lib_spec_parser.style_detector import detect


def test_gherkin_detection():
    text = "Feature: x\n  Scenario: y\n    Given a\n    When b\n    Then c\n"
    assert detect(text, "auto") == "gherkin"


def test_ears_detection():
    text = "When a request arrives, the system shall log it."
    assert detect(text, "auto") == "ears"


def test_connextra_detection():
    text = "As a user, I want to login, so that I can access content."
    assert detect(text, "auto") == "connextra"


def test_plain_detection():
    text = "Plain description with no patterns."
    assert detect(text, "auto") == "plain"


def test_explicit_style_returns_as_is():
    text = "anything"
    assert detect(text, "gherkin") == "gherkin"
    assert detect(text, "ears") == "ears"
    assert detect(text, "connextra") == "connextra"
    assert detect(text, "plain") == "plain"


def test_priority_gherkin_over_ears():
    # When both gherkin and ears patterns present, gherkin wins (per spec order)
    text = """Feature: x
  Scenario: y
    Given a
    When b
    Then c
The system shall do something.
"""
    assert detect(text, "auto") == "gherkin"
