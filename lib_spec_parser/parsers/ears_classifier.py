"""EARS classifier — 5 パターンの shall 文分類.

Traces: LIB-FR-07
Determinism: D
"""

from __future__ import annotations

import re

# Pattern order matters: more-specific patterns must be tested before the
# ubiquitous catch-all so a "When ..., the system shall ..." sentence is
# classified as event_driven (not ubiquitous).
#
# Patterns key off the leading keyword (When/While/Where/If) and the presence
# of "shall" later in the sentence.
_EARS_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "event_driven",
        re.compile(r"^\s*When\b[^.\n]*?\bshall\b[^.\n]*\.?", re.IGNORECASE | re.MULTILINE),
    ),
    (
        "state_driven",
        re.compile(r"^\s*While\b[^.\n]*?\bshall\b[^.\n]*\.?", re.IGNORECASE | re.MULTILINE),
    ),
    (
        "optional",
        re.compile(r"^\s*Where\b[^.\n]*?\bshall\b[^.\n]*\.?", re.IGNORECASE | re.MULTILINE),
    ),
    (
        "unwanted",
        re.compile(
            r"^\s*If\b[^.\n]*?\bthen\b[^.\n]*?\bshall\b[^.\n]*\.?",
            re.IGNORECASE | re.MULTILINE,
        ),
    ),
    (
        "ubiquitous",
        re.compile(r"^\s*The\s+system\s+shall\b[^.\n]*\.?", re.IGNORECASE | re.MULTILINE),
    ),
]


def classify_ears(text: str) -> list[dict]:
    """EARS 5 パターンの shall 文を分類抽出する。

    Args:
        text: spec テキスト

    Returns:
        List[dict(text, ears_pattern, line_number)]
        - text: マッチした shall 文
        - ears_pattern: "ubiquitous"|"event_driven"|"state_driven"|"optional"|"unwanted"
        - line_number: 1-based 行番号
    """
    # Track which (start, end) ranges have already been claimed to avoid double-classification.
    claimed: list[tuple[int, int]] = []
    raw_results: list[tuple[int, dict]] = []  # (start_pos, entry)

    for pattern_name, regex in _EARS_PATTERNS:
        for m in regex.finditer(text):
            start, end = m.start(), m.end()
            # Skip if overlaps with already-claimed range
            overlap = False
            for s, e in claimed:
                if not (end <= s or start >= e):
                    overlap = True
                    break
            if overlap:
                continue
            claimed.append((start, end))
            line_no = text.count("\n", 0, start) + 1
            raw_results.append(
                (
                    start,
                    {
                        "text": m.group(0).strip(),
                        "ears_pattern": pattern_name,
                        "line_number": line_no,
                    },
                )
            )

    # Sort by document order
    raw_results.sort(key=lambda x: x[0])
    return [entry for _, entry in raw_results]
