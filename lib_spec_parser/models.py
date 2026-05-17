"""lib-spec-parser data model.

Traces: 全 LIB-FR（型基盤）
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SpecId:
    """要件 ID（例: US-01, FR-003）。

    Traces: LIB-FR-04
    """

    value: str  # 例: "US-01"
    id_type: str  # "US"|"FR"|"REQ"|"NFR"|"AR"|"EA"|"PR"|"PE"|"AD"
    line_number: int  # 1-based


@dataclass(frozen=True)
class TraceTag:
    """`Traces:` タグに列挙された参照 ID。

    Traces: LIB-FR-02

    Note:
        frozen=True のため referenced_ids は tuple とする。
    """

    raw_line: str
    referenced_ids: tuple[str, ...]
    line_number: int  # 1-based


@dataclass(frozen=True)
class Scenario:
    """Gherkin シナリオ 1 件。

    Traces: LIB-FR-07
    """

    name: str
    given: tuple[str, ...]
    when: tuple[str, ...]
    then: tuple[str, ...]
    examples: tuple[dict[str, str], ...]


@dataclass(frozen=True)
class SpecSection:
    """spec ファイルの 1 節。

    Traces: LIB-FR-05
    """

    section_id: str  # 節の SpecId（なければ ""）
    style: str  # "gherkin"|"ears"|"connextra"|"plain"
    raw_text: str  # 原文（情報損失なし）
    keywords: tuple[str, ...]
    shall_clauses: tuple[str, ...]  # EARS のみ非空
    scenarios: tuple[Scenario, ...]  # Gherkin のみ非空


@dataclass(frozen=True)
class DiagramRef:
    """埋め込み図ブロックへの参照。

    Traces: LIB-FR-06
    """

    diagram_type: str  # "mermaid"|"plantuml"|"ascii_art"
    raw_content: str
    start_line: int  # 1-based
    end_line: int  # 1-based


@dataclass
class SpecContent:
    """NormalizedArtifact.content (artifactType="spec" 用)。

    Traces: LIB-FR-01, LIB-FR-02, LIB-FR-04, LIB-FR-05, LIB-FR-06
    """

    spec_ids: list[SpecId] = field(default_factory=list)
    sections: list[SpecSection] = field(default_factory=list)
    trace_tags: list[TraceTag] = field(default_factory=list)
    embedded_diagrams: list[DiagramRef] = field(default_factory=list)
