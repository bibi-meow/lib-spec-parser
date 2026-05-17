"""Unit tests: ears_classifier."""

from __future__ import annotations

from lib_spec_parser.parsers.ears_classifier import classify_ears


def test_ubiquitous():
    text = "The system shall log all events."
    clauses = classify_ears(text)
    assert len(clauses) == 1
    assert clauses[0]["ears_pattern"] == "ubiquitous"


def test_event_driven():
    text = "When a request arrives, the system shall log it."
    clauses = classify_ears(text)
    assert len(clauses) == 1
    assert clauses[0]["ears_pattern"] == "event_driven"


def test_state_driven():
    text = "While idle, the system shall conserve power."
    clauses = classify_ears(text)
    assert len(clauses) == 1
    assert clauses[0]["ears_pattern"] == "state_driven"


def test_optional():
    text = "Where admin mode is active, the system shall allow access."
    clauses = classify_ears(text)
    assert len(clauses) == 1
    assert clauses[0]["ears_pattern"] == "optional"


def test_unwanted():
    text = "If an error occurs, then the system shall roll back."
    clauses = classify_ears(text)
    assert len(clauses) == 1
    assert clauses[0]["ears_pattern"] == "unwanted"


def test_all_five_patterns_in_one_text():
    text = """The system shall be available.
When a request arrives, the system shall log it.
While the system is in standby, the system shall conserve power.
Where the user is admin, the system shall allow access.
If an error occurs, then the system shall roll back."""
    clauses = classify_ears(text)
    assert len(clauses) == 5
    patterns = {c["ears_pattern"] for c in clauses}
    assert patterns == {
        "ubiquitous",
        "event_driven",
        "state_driven",
        "optional",
        "unwanted",
    }


def test_no_match_returns_empty():
    text = "There is no requirement here."
    assert classify_ears(text) == []
