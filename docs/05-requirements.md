# lib-spec-parser Requirements

## Functional Requirements

| FR ID    | Description                                            | Determinism | Test File |
|----------|-------------------------------------------------------|:-----------:|-----------|
| LIB-FR-01 | execute() returns NormalizedArtifact for any spec input | D | test_fr01_parse_normalized.py |
| LIB-FR-02 | Extract TraceTag from "Traces: ..." lines             | D | test_fr02_trace_tags.py |
| LIB-FR-03 | Auto-detect spec style (gherkin/ears/connextra/plain) | D | test_fr03_style_detection.py |
| LIB-FR-04 | Extract SpecId (US-XX, FR-NNN, REQ-NNN, etc.)         | D | test_fr04_spec_id_extraction.py |
| LIB-FR-05 | Split Markdown into sections at h2/h3 boundaries      | D | test_fr05_section_structure.py |
| LIB-FR-06 | Extract diagram fence blocks as DiagramRef            | D | test_fr06_diagram_extraction.py |
| LIB-FR-07 | Extract Gherkin scenarios and EARS shall clauses      | D | test_fr07_gherkin_ears.py |

---

## LIB-FR-01: Parse spec files to NormalizedArtifact

**Input**: `raw_content: bytes`, `path: str`, `config: ParserConfig`
**Output**: `NormalizedArtifact(artifact_id, artifact_type="spec", content)`
**Determinism**: D

```gherkin
Feature: Parse spec files to normalized artifact
  So that downstream tools can process them without format-specific logic

  Scenario: Parse Markdown spec file
    Given a Markdown spec file as bytes
    When execute() is called with path="spec.md"
    Then a NormalizedArtifact is returned with artifact_type="spec"
    And artifact_id.path equals "spec.md"

  Scenario: Parse empty file
    Given an empty bytes input
    When execute() is called
    Then a NormalizedArtifact is returned without error
```

---

## LIB-FR-02: Extract TraceTag from trace lines

**Input**: Text containing "Traces: FR-01, US-03" lines
**Output**: `List[TraceTag]` extracted from matching lines
**Determinism**: D

```gherkin
Feature: Extract trace tags
  Scenario: Single trace tag
    Given a spec with "Traces: FR-01"
    When parsed
    Then trace_tags contains TraceTag(raw="FR-01")

  Scenario: Multiple trace tags
    Given a spec with "Traces: FR-01, US-03"
    When parsed
    Then trace_tags contains FR-01 and US-03
```

---

## LIB-FR-03: Auto-detect spec style

**Input**: Section text
**Output**: `style: str` = "gherkin" | "ears" | "connextra" | "usdm" | "plain"
**Determinism**: D

```gherkin
Feature: Auto-detect spec style
  Scenario: Detect Gherkin
    Given text containing "Feature:" or "Scenario:"
    When detect_style is called
    Then style is "gherkin"

  Scenario: Detect EARS
    Given text containing "the system shall"
    When detect_style is called
    Then style is "ears"
```

---

## LIB-FR-04: Extract SpecId

**Input**: Full spec text
**Output**: `List[SpecId]` with configurable prefixes
**Determinism**: D

```gherkin
Feature: Extract requirement IDs
  Scenario: Default prefixes
    Given text "US-01 and FR-003 are related"
    When parsed with default config
    Then spec_ids contains US-01 and FR-003

  Scenario: Disabled extraction
    Given config with extract_ids=False
    When parsed
    Then spec_ids is empty
```

---

## LIB-FR-05: Section structure

**Input**: Markdown text
**Output**: `List[SpecSection]` split at h2/h3
**Determinism**: D

```gherkin
Feature: Split Markdown into sections
  Scenario: Multiple h2 headings
    Given Markdown with "## Section One" and "## Section Two"
    When parsed
    Then sections contains two entries with matching section_ids
```

---

## LIB-FR-06: Diagram extraction

**Input**: Markdown with fenced blocks
**Output**: `List[DiagramRef]` with diagram_id, source_format, raw_source
**Determinism**: D

```gherkin
Feature: Extract embedded diagram blocks
  Scenario: Mermaid fence
    Given Markdown with ```mermaid ... ```
    When parsed with extract_diagrams=True
    Then embedded_diagrams contains DiagramRef with source_format="mermaid"

  Scenario: Disabled extraction
    Given config with extract_diagrams=False
    When parsed
    Then embedded_diagrams is empty
```

---

## LIB-FR-07: Gherkin and EARS parsing

**Input**: Section text with Gherkin or EARS patterns
**Output**: `scenarios: List[Scenario]` or `shall_clauses: List[str]`
**Determinism**: D

```gherkin
Feature: Parse Gherkin and EARS
  Scenario: Gherkin scenarios
    Given text with "Scenario: Login" and Given/When/Then steps
    When parsed as gherkin
    Then scenarios contains the scenario with its steps

  Scenario: EARS shall clauses
    Given text with "the system shall validate"
    When parsed as ears
    Then shall_clauses contains the matching sentence
```
