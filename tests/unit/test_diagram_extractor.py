"""Unit tests for diagram_extractor module."""

from lib_spec_parser.diagram_extractor import extract_diagrams


class TestDiagramExtractor:
    def test_extracts_mermaid(self):
        text = "```mermaid\ngraph TD\n    A --> B\n```\n"
        diagrams = extract_diagrams(text, "spec.md")
        assert len(diagrams) == 1
        assert diagrams[0].source_format == "mermaid"

    def test_mermaid_raw_source(self):
        text = "```mermaid\ngraph TD\n    A --> B\n```\n"
        diagrams = extract_diagrams(text, "spec.md")
        assert "graph TD" in diagrams[0].raw_source

    def test_extracts_plantuml(self):
        text = "```plantuml\n@startuml\nAlice -> Bob\n@enduml\n```\n"
        diagrams = extract_diagrams(text, "spec.md")
        assert len(diagrams) == 1
        assert diagrams[0].source_format == "plantuml"

    def test_extracts_dot(self):
        text = "```dot\ndigraph G { a -> b; }\n```\n"
        diagrams = extract_diagrams(text, "spec.md")
        assert len(diagrams) == 1
        assert diagrams[0].source_format == "dot"

    def test_diagram_id_format(self):
        text = "```mermaid\ngraph TD\n    A --> B\n```\n"
        diagrams = extract_diagrams(text, "path/spec.md")
        assert diagrams[0].diagram_id == "path/spec.md::block0"

    def test_multiple_diagrams(self):
        text = "```mermaid\ngraph LR\n    X --> Y\n```\ntext\n```dot\ndigraph {}\n```\n"
        diagrams = extract_diagrams(text, "spec.md")
        assert len(diagrams) == 2
        assert diagrams[0].diagram_id == "spec.md::block0"
        assert diagrams[1].diagram_id == "spec.md::block1"

    def test_no_diagrams(self):
        text = "No diagrams here."
        diagrams = extract_diagrams(text, "spec.md")
        assert diagrams == []

    def test_case_insensitive_format(self):
        text = "```Mermaid\ngraph TD\n    A --> B\n```\n"
        diagrams = extract_diagrams(text, "spec.md")
        assert len(diagrams) == 1
        assert diagrams[0].source_format == "mermaid"
