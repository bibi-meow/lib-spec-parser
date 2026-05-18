# lib-spec-parser

Parses specification files (Markdown, YAML, RST) and extracts structured content for automated
review tools.

## Features

- Extracts requirement IDs (e.g., `US-01`, `FR-003`, `REQ-007`) with configurable prefix lists
- Extracts trace tags from `Traces: FR-01, US-03` patterns (configurable prefix)
- Detects specification styles automatically:
  - **Gherkin BDD** — Feature/Scenario/Given/When/Then
  - **EARS** — "the system shall", "when X, the system shall Y"
  - **Connextra** — "As a / I want / So that"
  - **Plain text** — fallback for unstructured specs
- Splits Markdown documents into sections at `##` and `###` headings
- Extracts embedded diagram code blocks (Mermaid, PlantUML, DOT) as raw source references

## Installation

```bash
pip install git+https://github.com/bibi-meow/lib-spec-parser.git
```

## Quick Start

```python
from lib_spec_parser import SpecParserExecutor, ParserConfig

executor = SpecParserExecutor()
config = ParserConfig(
    artifact_type="spec",
    executor_lib="lib-spec-parser",
    params={
        "extract_ids": True,
        "trace_format": "Traces:",
        "spec_style": "auto",       # or "gherkin", "ears", "connextra", "plain"
        "extract_diagrams": True,
    },
)

with open("requirements.md", "rb") as f:
    raw = f.read()

artifact = executor.execute(config, raw, "requirements.md")

# Requirement IDs
for sid in artifact.content.spec_ids:
    print(sid.value)   # "US-01", "FR-003", ...

# Trace tags
for tag in artifact.content.trace_tags:
    print(tag.raw)     # "FR-01", "US-03", ...

# Sections with style
for section in artifact.content.sections:
    print(section.section_id, section.style)  # "Login Feature", "gherkin"

# Embedded diagrams (raw source only)
for diag in artifact.content.embedded_diagrams:
    print(diag.diagram_id, diag.source_format)  # "spec.md::block0", "mermaid"
    print(diag.raw_source)
```

## Configuration

| Parameter        | Type           | Default      | Description |
|------------------|----------------|:------------:|-------------|
| `extract_ids`    | `bool`         | `True`       | Extract requirement IDs |
| `id_prefixes`    | `list[str]`    | `["US","FR","NFR","REQ","AR","AD"]` | ID prefix list |
| `trace_format`   | `str`          | `"Traces:"`  | Trace tag line prefix |
| `spec_style`     | `str`          | `"auto"`     | Force style or auto-detect |
| `extract_diagrams` | `bool`      | `True`       | Extract diagram fence blocks |

## Output Types

```python
NormalizedArtifact
  artifact_id.path       : str            # input file path
  artifact_type          : str            # always "spec"
  content.spec_ids       : List[SpecId]   # extracted IDs
  content.trace_tags     : List[TraceTag] # trace references
  content.sections       : List[SpecSection]
  content.embedded_diagrams : List[DiagramRef]
```

## Requirements

- Python 3.11+
- No external dependencies (standard library only)

## License

MIT
