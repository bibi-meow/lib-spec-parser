"""Unit tests: diagram_extractor."""

from __future__ import annotations

from lib_spec_parser.diagram_extractor import extract_diagrams


def test_mermaid_block():
    text = "# Spec\n\n```mermaid\nflowchart TD\nA-->B\n```\n"
    diagrams = extract_diagrams(text)
    mermaid = [d for d in diagrams if d.diagram_type == "mermaid"]
    assert len(mermaid) == 1
    assert "flowchart TD" in mermaid[0].raw_content
    assert "A-->B" in mermaid[0].raw_content


def test_plantuml_block():
    text = "# Spec\n\n@startuml\nAlice -> Bob\n@enduml\n"
    diagrams = extract_diagrams(text)
    plantuml = [d for d in diagrams if d.diagram_type == "plantuml"]
    assert len(plantuml) == 1
    assert "Alice -> Bob" in plantuml[0].raw_content


def test_multiple_mermaid_blocks():
    text = """# Spec
```mermaid
A
```
text
```mermaid
B
```
"""
    diagrams = extract_diagrams(text)
    mermaid = [d for d in diagrams if d.diagram_type == "mermaid"]
    assert len(mermaid) == 2


def test_no_diagrams_returns_empty():
    text = "Just text, no diagrams."
    assert extract_diagrams(text) == []


def test_line_numbers_increasing():
    text = """line1
line2
```mermaid
content
```
"""
    diagrams = extract_diagrams(text)
    assert len(diagrams) == 1
    assert diagrams[0].start_line <= diagrams[0].end_line
    assert diagrams[0].start_line >= 1
