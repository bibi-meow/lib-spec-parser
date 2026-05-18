# lib-spec-parser Architecture

## Purpose

Parse Markdown, YAML, and RST specification files into `NormalizedArtifact` objects containing
structured content: requirement IDs, trace tags, sections with style classification, and diagram
references.

## Input / Output

| Kind   | Type                  | Description                              |
|--------|-----------------------|------------------------------------------|
| Input  | `bytes`               | Raw spec file content                    |
| Input  | `str`                 | File path (used for artifact_id)         |
| Input  | `ParserConfig`        | Extraction parameters                    |
| Output | `NormalizedArtifact`  | Structured spec content                  |

---

## Module Structure

```
lib_spec_parser/
  __init__.py            — Public API exports
  models.py              — Dataclass definitions
  executor.py            — SpecParserExecutor (main entry point)
  format_detector.py     — .md/.yaml/.rst detection from extension
  style_detector.py      — Auto-detect gherkin/ears/connextra/plain
  spec_id_extractor.py   — Regex-based ID extraction (US-XX, FR-NNN, etc.)
  trace_tag_extractor.py — "Traces: ..." line parser
  section_assembler.py   — Markdown h2/h3 → SpecSection builder
  diagram_extractor.py   — Fence block detector → DiagramRef
  parsers/
    __init__.py
    gherkin_parser.py    — Scenario/step extraction
    ears_classifier.py   — EARS pattern classification + shall clause extraction
    connextra_parser.py  — "As a / I want" parser
    generic_parser.py    — Plain text line extractor
```

| Module              | Responsibility                              | Determinism |
|---------------------|---------------------------------------------|:-----------:|
| executor.py         | Orchestrate all extraction steps            | D |
| format_detector.py  | Map file extension to format string         | D |
| style_detector.py   | Classify spec style from text content       | D |
| spec_id_extractor.py| Extract requirement IDs via configurable regex | D |
| trace_tag_extractor.py| Extract trace tags from "Traces:" lines   | D |
| section_assembler.py| Split Markdown at h2/h3 boundaries         | D |
| diagram_extractor.py| Detect fenced diagram blocks               | D |
| gherkin_parser.py   | Parse Scenario/Given/When/Then             | D |
| ears_classifier.py  | Classify EARS pattern; extract shall clauses | D |

---

## DFD (Data Flow)

```
raw_content (bytes) ──▶ format_detector ──▶ detected_format
                                                    │
raw_content ──▶ UTF-8 decode ──▶ text ──────────────┤
                                                    ▼
                               style_detector ──▶ style
                                                    │
                               section_assembler ──▶ List[SpecSection]
                                    │ (per section: gherkin_parser / ears_classifier)
                                    ▼
text ──▶ spec_id_extractor ──▶ List[SpecId]
text ──▶ trace_tag_extractor ──▶ List[TraceTag]
text ──▶ diagram_extractor ──▶ List[DiagramRef]
                                    │
                                    ▼
                            NormalizedArtifact
```

---

## Error Handling

| Error Condition        | Module          | Strategy                                    |
|-----------------------|-----------------|---------------------------------------------|
| Non-UTF-8 bytes       | executor.py     | decode with errors="replace" (no exception) |
| Unknown file extension | format_detector | Default to "markdown"                       |
| Empty input           | executor.py     | Return NormalizedArtifact with empty lists  |

---

## Dependencies

None — Python standard library only (re, os.path, dataclasses).

**Decision Log**: #1-1, #1-2, #1-3
