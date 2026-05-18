"""TraceTag extractor: extracts trace references from 'Traces: ...' lines."""

import re
from typing import List

_ID_PATTERN = re.compile(r"\b[A-Z][A-Z0-9]*-\d+\b")


def extract_trace_tags(text: str, trace_format: str = "Traces:") -> List[str]:
    """Extract trace tags from lines matching the trace format prefix.

    Args:
        text: Raw text to search.
        trace_format: Prefix string that marks a trace line (e.g., "Traces:").

    Returns:
        List of tag strings (e.g., ["FR-01", "US-03"]).
    """
    escaped = re.escape(trace_format)
    line_pattern = re.compile(rf"(?i){escaped}\s*(.+)")

    tags: list[str] = []
    seen: dict[str, None] = {}

    for line_match in line_pattern.finditer(text):
        remainder = line_match.group(1)
        for id_match in _ID_PATTERN.finditer(remainder):
            val = id_match.group(0)
            if val not in seen:
                seen[val] = None
                tags.append(val)

    return tags
