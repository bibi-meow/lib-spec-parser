"""LIB-FR-02 acceptance tests: Traces tag extraction.

Traces: LIB-FR-02, US-L-02
"""

from __future__ import annotations

from lib_spec_parser import execute


def _config(trace_format: str = "Traces:") -> dict:
    return {
        "artifact_type": "spec",
        "executor_lib": "lib_spec_parser",
        "params": {
            "extract_ids": True,
            "trace_format": trace_format,
            "spec_style": "auto",
            "extract_diagrams": True,
        },
        "enabled": True,
    }


def test_standard_traces_tag_extraction():
    # Construct content where "Traces:" appears at line 42
    lines = ["# Spec"] + [f"line {i}" for i in range(2, 42)] + ["Traces: FR-01, US-03"]
    md = ("\n".join(lines) + "\n").encode("utf-8")
    result = execute(_config(), md, "spec.md")
    trace_tags = result["content"]["trace_tags"]
    assert len(trace_tags) == 1
    assert trace_tags[0]["referenced_ids"] == ["FR-01", "US-03"]
    assert trace_tags[0]["line_number"] == 42


def test_custom_trace_format_only_matches_custom():
    md = b"""# Spec
Refs: AR-01
Traces: FR-01
"""
    result = execute(_config(trace_format="Refs:"), md, "spec.md")
    trace_tags = result["content"]["trace_tags"]
    # Only "Refs:" tags are extracted
    assert len(trace_tags) == 1
    assert trace_tags[0]["referenced_ids"] == ["AR-01"]


def test_mixed_separators_comma_and_whitespace():
    md = b"""# Spec
Traces: FR-01,US-02  AR-03
"""
    result = execute(_config(), md, "spec.md")
    trace_tags = result["content"]["trace_tags"]
    assert len(trace_tags) == 1
    assert trace_tags[0]["referenced_ids"] == ["FR-01", "US-02", "AR-03"]


def test_multiple_traces_tags_extracted():
    md = b"""# Spec
Traces: US-01
Some text
Traces: FR-02, AR-03
"""
    result = execute(_config(), md, "spec.md")
    trace_tags = result["content"]["trace_tags"]
    assert len(trace_tags) == 2
    assert trace_tags[0]["referenced_ids"] == ["US-01"]
    assert trace_tags[1]["referenced_ids"] == ["FR-02", "AR-03"]


def test_raw_line_preserved():
    md = b"""# Spec
Traces: US-01, FR-003
"""
    result = execute(_config(), md, "spec.md")
    trace_tags = result["content"]["trace_tags"]
    assert "US-01" in trace_tags[0]["raw_line"]
    assert "FR-003" in trace_tags[0]["raw_line"]
