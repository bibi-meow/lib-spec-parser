"""LIB-FR-03 acceptance tests: Style detection.

Traces: LIB-FR-03, US-L-03
"""

from __future__ import annotations

from lib_spec_parser.style_detector import detect


def test_gherkin_style():
    text = """Feature: Login
  Scenario: Successful
    Given user is here
    When user logs in
    Then success
"""
    assert detect(text, "auto") == "gherkin"


def test_ears_event_driven_style():
    text = """When a request arrives, the system shall log the event."""
    assert detect(text, "auto") == "ears"


def test_ears_ubiquitous_style():
    text = """The system shall provide an API."""
    assert detect(text, "auto") == "ears"


def test_connextra_style():
    text = """As a user, I want to log in, so that I can access the dashboard."""
    assert detect(text, "auto") == "connextra"


def test_plain_style():
    text = """This is just some descriptive text without any patterns."""
    assert detect(text, "auto") == "plain"


def test_explicit_gherkin_overrides_content():
    text = """This is just plain text."""
    # Forced to gherkin
    assert detect(text, "gherkin") == "gherkin"


def test_explicit_ears_overrides_content():
    text = """Just plain text."""
    assert detect(text, "ears") == "ears"


def test_explicit_connextra_overrides_content():
    text = """Just plain text."""
    assert detect(text, "connextra") == "connextra"


def test_explicit_plain_overrides_content():
    text = """Feature: Login
  Scenario: x
    Given y
"""
    assert detect(text, "plain") == "plain"
