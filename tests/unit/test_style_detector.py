"""Unit tests for style_detector module."""

from lib_spec_parser.style_detector import detect_style


class TestStyleDetector:
    def test_detects_gherkin(self):
        text = "Feature: Login\n\nScenario: Success\n  Given user is on page\n"
        assert detect_style(text) == "gherkin"

    def test_detects_ears(self):
        text = "When the user submits, the system shall validate.\n"
        assert detect_style(text) == "ears"

    def test_detects_connextra(self):
        text = "As a user, I want to log in, So that I can access my account.\n"
        assert detect_style(text) == "connextra"

    def test_detects_plain(self):
        text = "This is plain specification text without any special format.\n"
        assert detect_style(text) == "plain"

    def test_empty_is_plain(self):
        assert detect_style("") == "plain"

    def test_ears_while_pattern(self):
        text = "While the system is processing, the system shall display loading.\n"
        assert detect_style(text) == "ears"

    def test_ears_ubiquitous_pattern(self):
        text = "The system shall log all actions.\n"
        assert detect_style(text) == "ears"
