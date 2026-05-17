"""LIB-FR-05 acceptance tests: SpecSection structuring.

Traces: LIB-FR-05, US-L-05
"""

from __future__ import annotations

from lib_spec_parser import execute


def _config() -> dict:
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


def test_markdown_heading_splits_sections():
    md = b"""## US-01

Some content for US-01.

## US-02

Some content for US-02.
"""
    result = execute(_config(), md, "spec.md")
    sections = result["content"]["sections"]
    # at least two sections, identifying US-01 and US-02
    section_ids = [s["section_id"] for s in sections]
    assert "US-01" in section_ids
    assert "US-02" in section_ids


def test_ears_section_shall_clauses():
    md = b"""## REQ-001

The system shall do X.
The system shall do Y.
The system shall do Z.
"""
    result = execute(_config(), md, "spec.md")
    sections = result["content"]["sections"]
    # find the REQ-001 section
    ears_section = next((s for s in sections if s["section_id"] == "REQ-001"), None)
    assert ears_section is not None
    assert ears_section["style"] == "ears"
    assert len(ears_section["shall_clauses"]) == 3


def test_gherkin_section_scenarios():
    md = b"""## FEAT-01

```gherkin
Feature: Test
  Scenario: A
    Given a
    When b
    Then c
  Scenario: B
    Given d
    When e
    Then f
```
"""
    result = execute(_config(), md, "spec.md")
    sections = result["content"]["sections"]
    gherkin_sections = [s for s in sections if s["style"] == "gherkin"]
    assert len(gherkin_sections) >= 1
    scenarios = gherkin_sections[0]["scenarios"]
    assert len(scenarios) == 2
    names = [s["name"] for s in scenarios]
    assert "A" in names
    assert "B" in names


def test_raw_text_is_preserved():
    body_lines = [f"Body line {i}" for i in range(1, 11)]
    md = ("## US-01\n\n" + "\n".join(body_lines) + "\n").encode("utf-8")
    result = execute(_config(), md, "spec.md")
    sections = result["content"]["sections"]
    us01 = next((s for s in sections if s["section_id"] == "US-01"), None)
    assert us01 is not None
    # all body lines should be retained in raw_text
    for line in body_lines:
        assert line in us01["raw_text"]


def test_section_has_all_required_fields():
    md = b"""## US-01

Plain content.
"""
    result = execute(_config(), md, "spec.md")
    sections = result["content"]["sections"]
    assert len(sections) >= 1
    s = sections[0]
    for field in (
        "section_id",
        "style",
        "raw_text",
        "keywords",
        "shall_clauses",
        "scenarios",
    ):
        assert field in s
