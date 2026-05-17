# Architecture Overview

## Purpose

`lib-spec-parser` reads specification files (Markdown / YAML / RST) and converts them into a structured `NormalizedArtifact` dict containing four extracted fields:

- `spec_ids` — requirement IDs (e.g. `REQ-001`, `US-02`)
- `sections` — document sections with detected style and parsed content
- `trace_tags` — traceability tag lines (e.g. `Traces: REQ-001`)
- `embedded_diagrams` — Mermaid / PlantUML diagram blocks

All processing is deterministic (regex-based). No LLM calls are made.

---

## Module Map

```
lib_spec_parser/
├── __init__.py             # Public API: execute() + SpecParserExecutor
├── executor.py             # Orchestration: input validation → decode → parse → assemble
├── format_detector.py      # Extension-based format detection (.md / .yaml / .rst)
├── style_detector.py       # Content-based style detection (gherkin / ears / connextra / plain)
├── section_assembler.py    # Split on Markdown headings → List[SpecSection]
├── spec_id_extractor.py    # Regex extraction of requirement IDs
├── trace_tag_extractor.py  # Extraction of "Traces:" tag lines
├── diagram_extractor.py    # Mermaid / PlantUML block extraction
├── models.py               # Frozen dataclass type definitions
├── errors.py               # ParseError exception
└── parsers/
    ├── gherkin_parser.py   # State-machine Gherkin parser → List[Scenario]
    ├── ears_classifier.py  # EARS 5-pattern classifier → shall_clauses
    ├── connextra_parser.py # As/I want/So that decomposition
    └── generic_parser.py   # Plain text (no-op; extraction handled by other modules)
```

| Module | Responsibility | Deterministic |
|--------|---------------|---------------|
| `executor.py` | Full pipeline orchestration | ✅ |
| `format_detector.py` | `.md` / `.yaml` / `.rst` detection | ✅ |
| `style_detector.py` | Gherkin → EARS → Connextra → Plain priority | ✅ |
| `parsers/gherkin_parser.py` | Given/When/Then + Scenario Outline | ✅ |
| `parsers/ears_classifier.py` | 5 EARS pattern regex classification | ✅ |
| `parsers/connextra_parser.py` | As/I want/So that regex decomposition | ✅ |
| `section_assembler.py` | Heading-boundary section splitting | ✅ |
| `diagram_extractor.py` | Mermaid/PlantUML: ✅ / ASCII Art: heuristic | ⚠️ partial |
| `spec_id_extractor.py` | 9-prefix regex with word boundary | ✅ |
| `trace_tag_extractor.py` | Configurable prefix regex | ✅ |

---

## Data Flow

```
[raw_content: bytes]  [path: str]  [config: dict]
         │                 │              │
         └─────────────────┴──────────────┘
                           │
                     [executor]
                     │        │
               UTF-8 decode   input validation
                     │
               [format_detector] → "md" | "yaml" | "rst"
                     │
               [style_detector]  → "gherkin" | "ears" | "connextra" | "plain"
                     │
          ┌──────────┼──────────┬──────────┐
          ▼          ▼          ▼          ▼
    [gherkin_  [ears_     [connextra_  [generic_
     parser]   classifier]  parser]    parser]
          └──────────┴──────────┴──────────┘
                           │
                  [section_assembler] → List[SpecSection]
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
  [spec_id_extractor] [trace_tag_    [diagram_extractor]
                       extractor]
          │                │                │
    List[SpecId]    List[TraceTag]   List[DiagramRef]
          └────────────────┴────────────────┘
                           │
                    [SpecContent]
                           │
                  [NormalizedArtifact dict]
```

---

## Error Handling

This library follows a **fail-fast** contract: partial output is never returned.

| Condition | Raised By | Exception |
|-----------|-----------|-----------|
| `config["enabled"]` is `False` | `executor` | `ValueError` |
| Non-UTF-8 bytes | `executor` | `ParseError` |
| Unsupported extension | `format_detector` | `ParseError` |
| Unrecoverable section assembly failure | `section_assembler` | `ParseError` |

---

## Style Detection Priority

When `spec_style="auto"` (default), style is detected in this order:

1. **Gherkin** — `Feature:` / `Scenario:` + ≥2 Given/When/Then keywords
2. **EARS** — `shall` keyword + EARS pattern keywords (When/While/Where/If)
3. **Connextra** — `As a[n]? ..., I want ..., so that ...` pattern
4. **Plain** — none of the above
