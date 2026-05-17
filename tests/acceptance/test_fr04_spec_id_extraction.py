"""LIB-FR-04 acceptance tests: SpecId extraction.

Traces: LIB-FR-04, US-L-04
"""

from __future__ import annotations

from lib_spec_parser import execute


def _config(extract_ids: bool = True) -> dict:
    return {
        "artifact_type": "spec",
        "executor_lib": "lib_spec_parser",
        "params": {
            "extract_ids": extract_ids,
            "trace_format": "Traces:",
            "spec_style": "auto",
            "extract_diagrams": True,
        },
        "enabled": True,
    }


def test_all_nine_prefixes_extracted():
    md = b"""# Spec
US-01 and FR-003 and REQ-007 and NFR-002 and AR-01 and EA-02 and PR-01 and PE-03 and AD-01
"""
    result = execute(_config(), md, "spec.md")
    spec_ids = result["content"]["spec_ids"]
    assert len(spec_ids) == 9
    types = {s["id_type"] for s in spec_ids}
    assert types == {"US", "FR", "REQ", "NFR", "AR", "EA", "PR", "PE", "AD"}


def test_duplicate_ids_recorded_as_occurrences():
    md = b"""# Spec
US-01 appears here.
And US-01 also here.
And US-01 once more.
"""
    result = execute(_config(), md, "spec.md")
    spec_ids = result["content"]["spec_ids"]
    us01_count = sum(1 for s in spec_ids if s["value"] == "US-01")
    assert us01_count == 3


def test_extract_ids_false_returns_empty():
    md = b"""# Spec
US-01, FR-002
"""
    result = execute(_config(extract_ids=False), md, "spec.md")
    assert result["content"]["spec_ids"] == []


def test_spec_id_values_and_types():
    md = b"""# Spec
The requirement US-01 traces to FR-003.
"""
    result = execute(_config(), md, "spec.md")
    spec_ids = result["content"]["spec_ids"]
    us = [s for s in spec_ids if s["value"] == "US-01"]
    fr = [s for s in spec_ids if s["value"] == "FR-003"]
    assert len(us) == 1
    assert us[0]["id_type"] == "US"
    assert len(fr) == 1
    assert fr[0]["id_type"] == "FR"


def test_spec_id_with_suffix_letter():
    md = b"""# Spec
US-06a is a variant.
"""
    result = execute(_config(), md, "spec.md")
    spec_ids = result["content"]["spec_ids"]
    values = [s["value"] for s in spec_ids]
    assert "US-06a" in values


def test_spec_id_line_number():
    lines = ["# Spec", "", "Some text here.", "US-01 on line 4"]
    md = ("\n".join(lines) + "\n").encode("utf-8")
    result = execute(_config(), md, "spec.md")
    spec_ids = result["content"]["spec_ids"]
    us = [s for s in spec_ids if s["value"] == "US-01"]
    assert len(us) == 1
    assert us[0]["line_number"] == 4
