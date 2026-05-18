"""Unit tests for format_detector module."""

from lib_spec_parser.format_detector import detect_format


class TestFormatDetector:
    def test_md_extension(self):
        assert detect_format("spec.md") == "markdown"

    def test_yaml_extension(self):
        assert detect_format("spec.yaml") == "yaml"

    def test_yml_extension(self):
        assert detect_format("spec.yml") == "yaml"

    def test_rst_extension(self):
        assert detect_format("spec.rst") == "rst"

    def test_unknown_extension_defaults_markdown(self):
        assert detect_format("spec.txt") == "markdown"

    def test_path_with_directories(self):
        assert detect_format("path/to/spec.md") == "markdown"

    def test_uppercase_extension(self):
        assert detect_format("SPEC.MD") == "markdown"
