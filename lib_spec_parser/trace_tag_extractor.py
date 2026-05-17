"""Trace tag extractor.

Traces: LIB-FR-02
"""

from __future__ import annotations

import re

from .models import TraceTag

# Allow comma and/or whitespace as separators between IDs in the tag body.
_ID_SPLITTER = re.compile(r"[,\s]+")


def extract_trace_tags(text: str, trace_format: str = "Traces:") -> list[TraceTag]:
    """Trace tag を全件抽出する。

    Args:
        text: spec 全文
        trace_format: tag のプレフィックス文字列（例: "Traces:" or "Refs:"）

    Returns:
        List[TraceTag]（出現順）
    """
    # Escape any regex-special chars in the user-provided prefix.
    prefix_escaped = re.escape(trace_format)
    # Match the prefix at start of a line (allowing leading whitespace).
    # Capture everything after the prefix on the same line as the body.
    pattern = re.compile(rf"^\s*{prefix_escaped}\s*(.+)$", re.MULTILINE)

    results: list[TraceTag] = []
    for m in pattern.finditer(text):
        body = m.group(1).strip()
        # Split on commas and/or whitespace; drop empties.
        ids = tuple(s for s in _ID_SPLITTER.split(body) if s)
        # 1-based line number for start of match
        line_number = text.count("\n", 0, m.start()) + 1
        # raw_line — full matched line text (without the trailing newline)
        raw_line = m.group(0).rstrip("\r\n")
        results.append(
            TraceTag(
                raw_line=raw_line,
                referenced_ids=ids,
                line_number=line_number,
            )
        )
    return results
