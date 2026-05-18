"""Diagram extractor: detects fenced diagram blocks and returns DiagramRef objects."""

import re
from typing import List

from lib_spec_parser.models import DiagramRef

_SUPPORTED_FORMATS = {"mermaid", "plantuml", "dot"}

# Match fenced code blocks with supported formats (case-insensitive)
_FENCE_PATTERN = re.compile(
    r"```(mermaid|plantuml|dot)\s*\n(.*?)```",
    re.IGNORECASE | re.DOTALL,
)


def extract_diagrams(text: str, path: str) -> List[DiagramRef]:
    """Extract embedded diagram blocks from markdown text.

    Args:
        text: Raw markdown text.
        path: File path used to construct diagram_id.

    Returns:
        List of DiagramRef objects with diagram_id, source_format, raw_source.
    """
    diagrams: list[DiagramRef] = []
    for index, match in enumerate(_FENCE_PATTERN.finditer(text)):
        fmt = match.group(1).lower()
        raw = match.group(2)
        diagrams.append(
            DiagramRef(
                diagram_id=f"{path}::block{index}",
                source_format=fmt,
                raw_source=raw,
            )
        )
    return diagrams
