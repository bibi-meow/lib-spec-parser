"""Data models for lib-spec-parser."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class SpecId:
    value: str  # "US-01", "FR-003" etc.


@dataclass
class TraceTag:
    raw: str  # "FR-01" etc.


@dataclass
class DiagramRef:
    """Reference to an embedded diagram block in the spec.

    GraphModel is not included (diagram_parser responsibility).
    """

    diagram_id: str  # "{path}::block{index}"
    source_format: str  # "mermaid" | "plantuml" | "dot" | "ascii"
    raw_source: str  # raw text inside the fence


@dataclass
class Scenario:
    name: str
    steps: List[str] = field(default_factory=list)


@dataclass
class SpecSection:
    section_id: str = ""
    style: str = "plain"  # "gherkin"|"ears"|"connextra"|"usdm"|"plain"
    raw_text: str = ""
    keywords: List[str] = field(default_factory=list)
    shall_clauses: List[str] = field(default_factory=list)  # EARS only
    scenarios: List[Scenario] = field(default_factory=list)  # Gherkin only


@dataclass
class ArtifactId:
    path: str


@dataclass
class SpecContent:
    spec_ids: List[SpecId] = field(default_factory=list)
    sections: List[SpecSection] = field(default_factory=list)
    trace_tags: List[TraceTag] = field(default_factory=list)
    embedded_diagrams: List[DiagramRef] = field(default_factory=list)


@dataclass
class NormalizedArtifact:
    artifact_id: ArtifactId
    artifact_type: str  # "spec"
    content: SpecContent


@dataclass
class ParserConfig:
    artifact_type: str
    executor_lib: str
    params: dict = field(default_factory=dict)
    enabled: bool = True
