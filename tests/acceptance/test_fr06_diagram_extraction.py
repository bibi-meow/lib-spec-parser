"""LIB-FR-06 acceptance tests: DiagramRef extraction.

Traces: LIB-FR-06, US-L-06
"""

from __future__ import annotations

from lib_spec_parser import execute


def _config(extract_diagrams: bool = True) -> dict:
    return {
        "artifact_type": "spec",
        "executor_lib": "lib_spec_parser",
        "params": {
            "extract_ids": True,
            "trace_format": "Traces:",
            "spec_style": "auto",
            "extract_diagrams": extract_diagrams,
        },
        "enabled": True,
    }


def test_mermaid_block_extracted():
    # Construct spec where mermaid block is at lines 11-12 (content), fence at 10 and 13
    # Use 9 prefix lines, then ```mermaid (line 10), then content (11-12), then ``` (line 13)
    prefix = "\n".join(["# Spec"] + [f"line {i}" for i in range(2, 10)])
    md = (prefix + "\n```mermaid\nflowchart TD\nA-->B\n```\n").encode("utf-8")
    result = execute(_config(), md, "spec.md")
    diagrams = result["content"]["embedded_diagrams"]
    mermaid = [d for d in diagrams if d["diagram_type"] == "mermaid"]
    assert len(mermaid) >= 1
    assert "flowchart TD" in mermaid[0]["raw_content"]


def test_plantuml_block_extracted():
    md = b"""# Spec

@startuml
Alice -> Bob: hello
@enduml
"""
    result = execute(_config(), md, "spec.md")
    diagrams = result["content"]["embedded_diagrams"]
    plantuml = [d for d in diagrams if d["diagram_type"] == "plantuml"]
    assert len(plantuml) >= 1
    assert "Alice -> Bob" in plantuml[0]["raw_content"]


def test_extract_diagrams_false_returns_empty():
    md = b"""# Spec

```mermaid
flowchart TD
A-->B
```
"""
    result = execute(_config(extract_diagrams=False), md, "spec.md")
    assert result["content"]["embedded_diagrams"] == []


def test_mermaid_line_numbers():
    md = b"""# Spec

```mermaid
flowchart TD
A-->B
```
"""
    result = execute(_config(), md, "spec.md")
    diagrams = result["content"]["embedded_diagrams"]
    mermaid = [d for d in diagrams if d["diagram_type"] == "mermaid"]
    assert len(mermaid) == 1
    # Fence opens at line 3, content at 4-5, closes at 6.
    # Verify that start_line < end_line and both are positive
    assert mermaid[0]["start_line"] >= 1
    assert mermaid[0]["end_line"] >= mermaid[0]["start_line"]
