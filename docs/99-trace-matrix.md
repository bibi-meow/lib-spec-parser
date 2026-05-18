# lib-spec-parser Trace Matrix

> FR → acceptance test → implementation → unit test traceability.

---

## Trace Matrix

| FR ID | Description | Acceptance Test | Implementation | Unit Test | Done |
|-------|-------------|-----------------|----------------|-----------|:----:|
| LIB-FR-01 | execute() returns NormalizedArtifact | tests/acceptance/test_fr01_parse_normalized.py | lib_spec_parser/executor.py | — | [x] |
| LIB-FR-02 | Extract TraceTag from "Traces:" lines | tests/acceptance/test_fr02_trace_tags.py | lib_spec_parser/trace_tag_extractor.py | tests/unit/test_trace_tag_extractor.py | [x] |
| LIB-FR-03 | Auto-detect spec style | tests/acceptance/test_fr03_style_detection.py | lib_spec_parser/style_detector.py | tests/unit/test_style_detector.py | [x] |
| LIB-FR-04 | Extract SpecId (US-XX, FR-NNN, etc.) | tests/acceptance/test_fr04_spec_id_extraction.py | lib_spec_parser/spec_id_extractor.py | tests/unit/test_spec_id_extractor.py | [x] |
| LIB-FR-05 | Split Markdown into sections at h2/h3 | tests/acceptance/test_fr05_section_structure.py | lib_spec_parser/section_assembler.py | — | [x] |
| LIB-FR-06 | Extract diagram fence blocks as DiagramRef | tests/acceptance/test_fr06_diagram_extraction.py | lib_spec_parser/diagram_extractor.py | tests/unit/test_diagram_extractor.py | [x] |
| LIB-FR-07 | Extract Gherkin scenarios and EARS shall clauses | tests/acceptance/test_fr07_gherkin_ears.py | lib_spec_parser/parsers/gherkin_parser.py, ears_classifier.py | tests/unit/test_gherkin_parser.py, test_ears_classifier.py | [x] |

---

## Coverage Summary

| Metric | Count |
|--------|------:|
| FR total | 7 |
| Acceptance test files | 7 |
| Acceptance test cases | 40 |
| Unit test files | 7 |
| Unit test cases | 57 |
| Total tests | 97 |
| All FR covered | YES |

---

## Traceability Checklist

- [x] All FR IDs in Trace Matrix
- [x] Each FR has at least 1 acceptance test scenario
- [x] Each acceptance test file path is recorded
- [x] Each FR has a corresponding implementation file
- [x] Each FR has corresponding unit tests
- [x] pytest: 97 tests PASS
- [x] All FRs covered: YES

**Decision Log**: #1-1 through #1-4
