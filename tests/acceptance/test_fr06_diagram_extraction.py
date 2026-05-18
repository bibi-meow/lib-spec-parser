"""FR-06: Diagram fence block extraction as DiagramRef."""

from lib_spec_parser import ParserConfig, SpecParserExecutor


def _config(**params) -> ParserConfig:
    return ParserConfig(
        artifact_type="spec",
        executor_lib="lib-spec-parser",
        params=params,
    )


MERMAID_CONTENT = b"""## Architecture

```mermaid
graph TD
    A --> B
    B --> C
```

Some text after.
"""

PLANTUML_CONTENT = b"""## Sequence

```plantuml
@startuml
Alice -> Bob: Hello
@enduml
```
"""

MULTI_DIAGRAM_CONTENT = b"""## Section

```mermaid
graph LR
    X --> Y
```

Middle text.

```dot
digraph G {
    a -> b;
}
```
"""


class TestFR06DiagramExtraction:
    def test_extracts_mermaid_diagram(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), MERMAID_CONTENT, "spec.md")
        diagrams = result.content.embedded_diagrams
        assert len(diagrams) == 1
        assert diagrams[0].source_format == "mermaid"

    def test_mermaid_raw_source(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), MERMAID_CONTENT, "spec.md")
        assert "graph TD" in result.content.embedded_diagrams[0].raw_source

    def test_extracts_plantuml_diagram(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), PLANTUML_CONTENT, "spec.md")
        diagrams = result.content.embedded_diagrams
        assert len(diagrams) == 1
        assert diagrams[0].source_format == "plantuml"

    def test_diagram_id_format(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), MERMAID_CONTENT, "path/spec.md")
        assert result.content.embedded_diagrams[0].diagram_id == "path/spec.md::block0"

    def test_multiple_diagrams_indexed(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), MULTI_DIAGRAM_CONTENT, "spec.md")
        assert len(result.content.embedded_diagrams) == 2
        assert result.content.embedded_diagrams[0].diagram_id == "spec.md::block0"
        assert result.content.embedded_diagrams[1].diagram_id == "spec.md::block1"

    def test_extract_diagrams_false_skips(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(extract_diagrams=False), MERMAID_CONTENT, "spec.md")
        assert result.content.embedded_diagrams == []

    def test_dot_diagram_extracted(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), MULTI_DIAGRAM_CONTENT, "spec.md")
        formats = [d.source_format for d in result.content.embedded_diagrams]
        assert "dot" in formats

    def test_no_diagrams_empty_list(self):
        content = b"## Section\n\nNo diagrams here.\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), content, "spec.md")
        assert result.content.embedded_diagrams == []
