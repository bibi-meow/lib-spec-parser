"""Unit tests: connextra_parser."""

from __future__ import annotations

from lib_spec_parser.parsers.connextra_parser import parse_connextra


def test_full_connextra():
    text = "As a user, I want to log in, so that I can access content."
    result = parse_connextra(text)
    assert result is not None
    assert "user" in result["role"]
    assert "log in" in result["want"]
    assert "access content" in result["benefit"]


def test_no_connextra_returns_none():
    text = "Just a description."
    assert parse_connextra(text) is None


def test_partial_connextra_returns_none():
    text = "As a user, I want to do things."
    # Missing "so that" — return None per spec
    result = parse_connextra(text)
    assert result is None
