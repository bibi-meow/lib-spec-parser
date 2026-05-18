# lib-spec-parser Diagram Spec

## Scope Declaration

lib-spec-parser **does not parse or generate diagram graph models**.

This lib detects embedded diagram fence blocks in spec files and returns them as `DiagramRef`
objects containing only `raw_source`. The actual graph model parsing is the responsibility of
`lib-diagram-parser`.

### What this lib does

- Detects fenced code blocks with formats: `mermaid`, `plantuml`, `dot`
- Returns `DiagramRef(diagram_id, source_format, raw_source)` — raw text only
- Does NOT produce node/edge graph structures

### What this lib does NOT do

- Parse Mermaid/PlantUML/DOT syntax
- Produce `GraphModel` or node/edge representations
- Validate diagram syntax

**Decision Log**: #1-2
