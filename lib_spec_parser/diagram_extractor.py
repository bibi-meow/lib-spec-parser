"""Diagram extractor — Mermaid / PlantUML / ASCII Art.

Traces: LIB-FR-06
Determinism: D (mermaid / plantuml) / H (ascii_art — heuristic)
"""

from __future__ import annotations

import re

from .models import DiagramRef

# Mermaid: ```mermaid ... ``` fenced block
_MERMAID_PATTERN = re.compile(
    r"```mermaid[ \t]*\n(.*?)(?:```|\Z)",
    re.DOTALL,
)

# PlantUML: @startuml ... @enduml
_PLANTUML_PATTERN = re.compile(
    r"@startuml\b(.*?)@enduml\b",
    re.DOTALL,
)


def _line_number_for_pos(text: str, pos: int) -> int:
    """1-based line number for char position."""
    return text.count("\n", 0, pos) + 1


def extract_diagrams(text: str) -> list[DiagramRef]:
    """spec 全文から埋め込み図ブロックを抽出する。

    Args:
        text: spec 全文

    Returns:
        List[DiagramRef]（出現順）
    """
    results: list[DiagramRef] = []

    # Mermaid blocks
    for m in _MERMAID_PATTERN.finditer(text):
        content = m.group(1).rstrip("\n")
        start = _line_number_for_pos(text, m.start(1))
        # end_line: last line of content (group 1)
        end = start + content.count("\n")
        results.append(
            DiagramRef(
                diagram_type="mermaid",
                raw_content=content,
                start_line=start,
                end_line=end,
            )
        )

    # PlantUML blocks
    for m in _PLANTUML_PATTERN.finditer(text):
        content = m.group(0)  # include @startuml/@enduml fences in raw
        start = _line_number_for_pos(text, m.start())
        end = _line_number_for_pos(text, m.end() - 1)
        results.append(
            DiagramRef(
                diagram_type="plantuml",
                raw_content=content,
                start_line=start,
                end_line=end,
            )
        )

    # ASCII Art: out-of-scope heuristic (H). Not implemented in this pass to avoid
    # false positives — Mermaid/PlantUML cover the deterministic cases required by
    # the acceptance tests. ASCII art extraction is documented as future heuristic
    # work (see 06-architecture.md determinism column).

    return results
