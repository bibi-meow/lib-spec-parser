"""Unit tests: format_detector."""

from __future__ import annotations

import pytest

from lib_spec_parser.errors import ParseError
from lib_spec_parser.format_detector import detect_format


def test_detect_md_extension():
    assert detect_format("spec.md", "# hi") == "md"


def test_detect_markdown_extension():
    assert detect_format("spec.markdown", "# hi") == "md"


def test_detect_yaml_extension():
    assert detect_format("spec.yaml", "a: 1") == "yaml"


def test_detect_yml_extension():
    assert detect_format("spec.yml", "a: 1") == "yaml"


def test_detect_rst_extension():
    assert detect_format("spec.rst", "Title\n=====") == "rst"


def test_unsupported_extension_raises():
    with pytest.raises(ParseError):
        detect_format("spec.txt", "hello")


def test_no_extension_raises():
    with pytest.raises(ParseError):
        detect_format("README", "hello")
