# lib-spec-parser API Spec

## Public API

| Class / Function     | Input                                | Output              | Determinism |
|---------------------|--------------------------------------|---------------------|:-----------:|
| `SpecParserExecutor.execute()` | `ParserConfig`, `bytes`, `str` | `NormalizedArtifact` | D |

---

## Data Types

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class SpecId:
    value: str          # e.g. "US-01", "FR-003"

@dataclass
class TraceTag:
    raw: str            # e.g. "FR-01"

@dataclass
class DiagramRef:
    diagram_id: str     # "{path}::block{index}"
    source_format: str  # "mermaid" | "plantuml" | "dot"
    raw_source: str     # fence content (no graph model)

@dataclass
class Scenario:
    name: str
    steps: List[str]    # ["Given ...", "When ...", "Then ..."]

@dataclass
class SpecSection:
    section_id: str     # heading text
    style: str          # "gherkin"|"ears"|"connextra"|"usdm"|"plain"
    raw_text: str
    keywords: List[str]
    shall_clauses: List[str]   # EARS only
    scenarios: List[Scenario]  # Gherkin only

@dataclass
class ArtifactId:
    path: str

@dataclass
class SpecContent:
    spec_ids: List[SpecId]
    sections: List[SpecSection]
    trace_tags: List[TraceTag]
    embedded_diagrams: List[DiagramRef]

@dataclass
class NormalizedArtifact:
    artifact_id: ArtifactId
    artifact_type: str  # always "spec"
    content: SpecContent

@dataclass
class ParserConfig:
    artifact_type: str
    executor_lib: str
    params: dict        # See params reference below
    enabled: bool = True
```

---

## ParserConfig.params Reference

| Key               | Type           | Default      | Description |
|-------------------|----------------|:------------:|-------------|
| `extract_ids`     | `bool`         | `True`       | Whether to extract SpecIds |
| `trace_format`    | `str`          | `"Traces:"`  | Line prefix for trace tags |
| `spec_style`      | `str \| None`  | `"auto"`     | Force style or auto-detect |
| `extract_diagrams`| `bool`         | `True`       | Whether to extract DiagramRefs |
| `id_prefixes`     | `List[str]`    | `["US","FR","NFR","REQ","AR","AD"]` | SpecId prefix list |

---

## API Signature

```python
class SpecParserExecutor:
    def execute(
        self,
        config: ParserConfig,
        raw_content: bytes,
        path: str,
    ) -> NormalizedArtifact:
        """Parse a spec file and return a NormalizedArtifact.

        Args:
            config: ParserConfig controlling extraction behavior.
            raw_content: Raw bytes of the spec file (UTF-8).
            path: File path used for artifact_id and diagram IDs.

        Returns:
            NormalizedArtifact with artifact_type="spec".

        Traces: LIB-FR-01, LIB-FR-02, LIB-FR-03, LIB-FR-04,
                LIB-FR-05, LIB-FR-06, LIB-FR-07
        """
```

---

## Pseudocode

```
execute(config, raw_content, path):
  1. format_detector.detect_format(path) → file_format
  2. raw_content.decode("utf-8", errors="replace") → text
  3. params.spec_style == "auto" → detect_style(text)
                                    else use forced style
  4. assemble_sections(text, forced_style) → List[SpecSection]
     For each section:
       if style == "gherkin": parse_gherkin(body) → scenarios
       if style == "ears":    extract_shall_clauses(body) → shall_clauses
  5. if extract_ids: extract_spec_ids(text, prefixes) → List[str] → List[SpecId]
  6. extract_trace_tags(text, trace_format) → List[str] → List[TraceTag]
  7. if extract_diagrams: extract_diagrams(text, path) → List[DiagramRef]
  8. return NormalizedArtifact(
       artifact_id=ArtifactId(path),
       artifact_type="spec",
       content=SpecContent(spec_ids, sections, trace_tags, embedded_diagrams)
     )
```

**Decision Log**: #1-1, #1-2, #1-3, #1-4
