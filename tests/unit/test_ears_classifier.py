"""Unit tests for ears_classifier module."""

from lib_spec_parser.parsers.ears_classifier import classify_ears, extract_shall_clauses


class TestEarsClassifier:
    def test_ubiquitous_pattern(self):
        text = "The system shall log all user actions."
        result = classify_ears(text)
        assert result == "ubiquitous"

    def test_event_driven_pattern(self):
        text = "When the user submits the form, the system shall validate the input."
        result = classify_ears(text)
        assert result == "event-driven"

    def test_state_driven_pattern(self):
        text = "While the system is processing, the system shall display a loading indicator."
        result = classify_ears(text)
        assert result == "state-driven"

    def test_optional_pattern(self):
        text = "Where the user has enabled dark mode, the system shall use dark colors."
        result = classify_ears(text)
        assert result == "optional"

    def test_unwanted_pattern(self):
        text = "If the network fails, then the system shall display an error message."
        result = classify_ears(text)
        assert result == "unwanted"

    def test_no_ears_pattern(self):
        text = "This is plain text."
        result = classify_ears(text)
        assert result is None

    def test_extract_shall_clauses(self):
        text = "When the user submits, the system shall validate.\nThe system shall log actions."
        clauses = extract_shall_clauses(text)
        assert len(clauses) == 2

    def test_extract_shall_clauses_empty(self):
        text = "No requirements in this text at all."
        clauses = extract_shall_clauses(text)
        assert clauses == []
