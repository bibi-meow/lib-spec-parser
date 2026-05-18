# lib-spec-parser User Stories

> Lib-level user stories derived from upstream system US: US-01, US-02, US-05, US-06, US-06a, US-22, US-23.

## Upstream US Coverage

| US ID  | Title                                | Relevance |
|--------|--------------------------------------|-----------|
| US-01  | Parse spec files to normalized form  | Core      |
| US-02  | Extract requirement IDs              | Core      |
| US-05  | Detect embedded diagrams             | Core      |
| US-06  | Split spec into sections             | Core      |
| US-06a | Auto-detect spec style               | Core      |
| US-22  | Extract trace tags                   | Core      |
| US-23  | Support Gherkin and EARS styles      | Core      |

---

## US-L-01: Parse spec files to a normalized artifact

**As a** spec review tool  
**I want** to parse Markdown, YAML, and RST spec files into a NormalizedArtifact  
**So that** downstream tools can process them without format-specific logic

**Acceptance Criteria:**
- [x] execute() returns a NormalizedArtifact for .md, .yaml, and .rst inputs
- [x] artifact_type is always "spec"
- [x] artifact_id.path matches the input path

**Upstream US**: US-01

---

## US-L-02: Extract requirement IDs

**As a** spec review tool  
**I want** to extract requirement IDs (US-XX, FR-NNN, REQ-NNN, etc.) from spec text  
**So that** I can link requirements to other artifacts

**Acceptance Criteria:**
- [x] Extracts IDs with default prefixes: US, FR, NFR, REQ, AR, AD
- [x] Supports configurable prefixes via id_prefixes param
- [x] Can be disabled via extract_ids=False

**Upstream US**: US-02

---

## US-L-03: Extract trace tags

**As a** spec review tool  
**I want** to extract "Traces: FR-01, US-03" patterns from spec text  
**So that** I can build a traceability graph

**Acceptance Criteria:**
- [x] Extracts tags from "Traces: ..." lines
- [x] Supports configurable trace_format param
- [x] Handles multiple comma-separated tags

**Upstream US**: US-22

---

## US-L-04: Split spec into sections

**As a** spec review tool  
**I want** to split Markdown specs at h2/h3 heading boundaries into SpecSection objects  
**So that** each section can be analyzed independently

**Acceptance Criteria:**
- [x] Splits at ## and ### headings
- [x] Each section has section_id, style, raw_text
- [x] Sections without headings are treated as one section

**Upstream US**: US-06

---

## US-L-05: Auto-detect spec style

**As a** spec review tool  
**I want** the lib to auto-detect whether a section is Gherkin, EARS, Connextra, or plain  
**So that** I can apply appropriate parsing logic

**Acceptance Criteria:**
- [x] Detects Gherkin by Feature:/Scenario: markers
- [x] Detects EARS by "shall" patterns
- [x] Detects Connextra by "As a / I want" pattern
- [x] Falls back to "plain" when no pattern matches
- [x] Can be overridden via spec_style param

**Upstream US**: US-06a

---

## US-L-06: Extract embedded diagrams

**As a** spec review tool  
**I want** to detect and extract mermaid/plantuml/dot fenced blocks as DiagramRef  
**So that** diagram_parser can process them separately

**Acceptance Criteria:**
- [x] Detects ```mermaid, ```plantuml, ```dot fences
- [x] DiagramRef contains diagram_id, source_format, raw_source
- [x] diagram_id format: "{path}::block{index}"
- [x] Can be disabled via extract_diagrams=False

**Upstream US**: US-05

---

## US-L-07: Parse Gherkin scenarios and EARS shall clauses

**As a** spec review tool  
**I want** to extract Scenario/steps from Gherkin and "shall" clauses from EARS text  
**So that** I can verify BDD coverage and requirement completeness

**Acceptance Criteria:**
- [x] Gherkin: extracts Scenario objects with name and steps
- [x] EARS: extracts shall_clauses as a list of sentence strings

**Upstream US**: US-23
