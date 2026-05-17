"""Connextra parser — "As a X, I want Y, so that Z" 分解.

Traces: LIB-FR-01
Determinism: D
"""

from __future__ import annotations

import re

_CONNEXTRA_PATTERN = re.compile(
    r"As\s+a[n]?\s+(?P<role>.+?)\s*,\s*I\s+want\s+(?P<want>.+?)\s*,\s*so\s+that\s+(?P<benefit>.+?)(?:\.\s*$|\n|$)",
    re.IGNORECASE | re.DOTALL,
)


def parse_connextra(text: str) -> dict[str, str] | None:
    """Connextra テキストを 3 フィールドに分解する。

    Args:
        text: section テキスト

    Returns:
        dict(role=..., want=..., benefit=...) or None (パターン不一致時)
    """
    m = _CONNEXTRA_PATTERN.search(text)
    if not m:
        return None
    return {
        "role": m.group("role").strip(),
        "want": m.group("want").strip(),
        "benefit": m.group("benefit").strip().rstrip("."),
    }
