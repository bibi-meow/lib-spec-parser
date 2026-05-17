"""LIB-FR-01 acceptance tests: MD → NormalizedArtifact generation.

Traces: LIB-FR-01, US-L-01, US-L-06
"""

from __future__ import annotations

import pytest

from lib_spec_parser import execute
from lib_spec_parser.errors import ParseError


def _default_config() -> dict:
    return {
        "artifact_type": "spec",
        "executor_lib": "lib_spec_parser",
        "params": {
            "extract_ids": True,
            "trace_format": "Traces:",
            "spec_style": "auto",
            "extract_diagrams": True,
        },
        "enabled": True,
    }


def test_parse_markdown_gherkin_artifact_type_is_spec():
    md = b"""## US-01

```gherkin
Feature: Authentication
  Scenario: Successful login
    Given the user is on the login screen
    When the user enters a valid password
    Then the user is redirected to the dashboard
```

Traces: US-01, FR-003
"""
    result = execute(_default_config(), md, "spec.md")
    assert result["artifactType"] == "spec"


def test_parse_markdown_gherkin_section_style():
    md = b"""## US-01

```gherkin
Feature: Authentication
  Scenario: Successful login
    Given the user is on the login screen
    When the user enters a valid password
    Then the user is redirected to the dashboard
```
"""
    result = execute(_default_config(), md, "spec.md")
    sections = result["content"]["sections"]
    assert len(sections) >= 1
    # Find at least one gherkin section
    gherkin_sections = [s for s in sections if s["style"] == "gherkin"]
    assert len(gherkin_sections) >= 1
    assert len(gherkin_sections[0]["scenarios"]) >= 1


def test_parse_markdown_trace_tags():
    md = b"""# Spec
Traces: US-01, FR-003
"""
    result = execute(_default_config(), md, "spec.md")
    trace_tags = result["content"]["trace_tags"]
    assert len(trace_tags) == 1
    assert trace_tags[0]["referenced_ids"] == ["US-01", "FR-003"]


def test_invalid_utf8_raises_parse_error():
    bad_bytes = b"\xff\xfe\x00invalid"
    with pytest.raises(ParseError):
        execute(_default_config(), bad_bytes, "broken.md")


def test_unsupported_extension_raises_parse_error():
    with pytest.raises(ParseError):
        execute(_default_config(), b"hello", "spec.txt")


def test_config_disabled_raises_value_error():
    cfg = _default_config()
    cfg["enabled"] = False
    with pytest.raises(ValueError):
        execute(cfg, b"x", "x.md")


def test_normalized_artifact_has_all_four_fields():
    md = b"# Spec\n\nNothing here.\n"
    result = execute(_default_config(), md, "spec.md")
    content = result["content"]
    assert "spec_ids" in content
    assert "sections" in content
    assert "trace_tags" in content
    assert "embedded_diagrams" in content
    # All must be lists (populated)
    assert isinstance(content["spec_ids"], list)
    assert isinstance(content["sections"], list)
    assert isinstance(content["trace_tags"], list)
    assert isinstance(content["embedded_diagrams"], list)


def test_artifact_id_is_deterministic():
    md = b"# Spec\n"
    r1 = execute(_default_config(), md, "path/to/spec.md")
    r2 = execute(_default_config(), md, "path/to/spec.md")
    assert r1["artifactId"] == r2["artifactId"]
