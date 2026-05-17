# API Reference

## Quick Start

```python
from lib_spec_parser import execute

with open("my-spec.md", "rb") as f:
    raw = f.read()

artifact = execute(
    config={
        "enabled": True,
        "artifact_type": "spec",
        "params": {
            "trace_format": "Traces:",
            "spec_id_prefixes": ["REQ", "US"],
            "spec_style": "auto",
        },
    },
    raw_content=raw,
    path="my-spec.md",
)
```

---

## `execute()`

Module-level convenience function. Equivalent to `SpecParserExecutor().execute(...)`.

```python
def execute(
    config: dict,
    raw_content: bytes,
    path: str,
) -> dict:
    ...
```

---

## `SpecParserExecutor`

```python
class SpecParserExecutor:
    def execute(
        self,
        config: dict,
        raw_content: bytes,
        path: str,
    ) -> dict:
        """
        Parse a specification file into a NormalizedArtifact.

        Args:
            config: Parser configuration dict with keys:
                - enabled (bool): Must be True; raises ValueError if False
                - artifact_type (str): Must be "spec"
                - params (dict): Optional tuning parameters (see below)
            raw_content: Raw file bytes (UTF-8 encoded)
            path: File path used for format detection (by extension)

        Returns:
            NormalizedArtifact dict (see Output Format)

        Raises:
            ValueError: config["enabled"] is False
            ParseError: UTF-8 decode failure, unsupported extension,
                        or unrecoverable parse error
        """
```

### `params` keys

| Key | Default | Description |
|-----|---------|-------------|
| `trace_format` | `"Traces:"` | Prefix string for trace tags |
| `spec_id_prefixes` | `["US","FR","REQ","NFR","AR","EA","PR","PE","AD"]` | ID prefixes to extract |
| `spec_style` | `"auto"` | Section style: `"auto"` \| `"gherkin"` \| `"ears"` \| `"connextra"` \| `"plain"` |
| `extract_ids` | `true` | Enable/disable SpecId extraction |
| `extract_diagrams` | `true` | Enable/disable diagram block extraction |

---

## Output Format

```json
{
  "artifactId": "spec:path/to/spec.md:abc123",
  "artifactType": "spec",
  "content": {
    "spec_ids": [
      {"value": "REQ-001", "id_type": "REQ", "line_number": 3}
    ],
    "sections": [
      {
        "section_id": "REQ-001",
        "style": "ears",
        "raw_text": "...",
        "keywords": [],
        "shall_clauses": ["The system shall ..."],
        "scenarios": []
      }
    ],
    "trace_tags": [
      {
        "raw_line": "Traces: REQ-001",
        "referenced_ids": ["REQ-001"],
        "line_number": 5
      }
    ],
    "embedded_diagrams": [
      {
        "diagram_type": "mermaid",
        "raw_content": "graph TD ...",
        "start_line": 10,
        "end_line": 14
      }
    ]
  }
}
```

---

## Data Types

### `SpecId`

| Field | Type | Description |
|-------|------|-------------|
| `value` | `str` | Full ID string, e.g. `"US-01"` |
| `id_type` | `str` | Prefix, e.g. `"US"` |
| `line_number` | `int` | 1-based line number |

### `TraceTag`

| Field | Type | Description |
|-------|------|-------------|
| `raw_line` | `str` | Full original line, e.g. `"Traces: FR-01, US-03"` |
| `referenced_ids` | `list[str]` | Extracted IDs, e.g. `["FR-01", "US-03"]` |
| `line_number` | `int` | 1-based line number |

### `SpecSection`

| Field | Type | Description |
|-------|------|-------------|
| `section_id` | `str` | SpecId found in the heading (empty string if none) |
| `style` | `str` | `"gherkin"` \| `"ears"` \| `"connextra"` \| `"plain"` |
| `raw_text` | `str` | Original section text (lossless) |
| `keywords` | `list[str]` | Detected keywords |
| `shall_clauses` | `list[str]` | EARS shall-statements (non-empty when `style="ears"`) |
| `scenarios` | `list[Scenario]` | Gherkin scenarios (non-empty when `style="gherkin"`) |

### `Scenario`

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Scenario title |
| `given` | `list[str]` | Given steps |
| `when` | `list[str]` | When steps |
| `then` | `list[str]` | Then steps |
| `examples` | `list[dict[str, str]]` | Scenario Outline examples rows |

### `DiagramRef`

| Field | Type | Description |
|-------|------|-------------|
| `diagram_type` | `str` | `"mermaid"` \| `"plantuml"` \| `"ascii_art"` |
| `raw_content` | `str` | Original diagram block text |
| `start_line` | `int` | 1-based start line |
| `end_line` | `int` | 1-based end line |

---

## Exceptions

### `ParseError`

Raised when a specification file cannot be parsed. This library uses a **fail-fast** contract: it never returns partial output. If any step fails, `ParseError` is raised immediately.

```python
from lib_spec_parser import ParseError

try:
    artifact = execute(config, raw_content, path)
except ParseError as e:
    print(f"Parse failed: {e}")
```

| Cause | Exception |
|-------|-----------|
| `config["enabled"]` is `False` | `ValueError` |
| Raw bytes are not valid UTF-8 | `ParseError` |
| File extension is not `.md`, `.yaml`/`.yml`, or `.rst` | `ParseError` |
| Unrecoverable parse error in section assembly | `ParseError` |
