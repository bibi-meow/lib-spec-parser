"""Generic parser — plain テキスト (SpecId / TraceTag 抽出のみ別モジュールに委譲).

Traces: LIB-FR-01
Determinism: D
"""

from __future__ import annotations


def parse_generic(text: str) -> str:
    """plain テキストの処理。

    Generic parser is a no-op pass-through for raw text; SpecId and TraceTag
    extraction live in dedicated modules. Returns the input text unchanged so
    callers can use it as raw_text for SpecSection assembly.
    """
    return text
