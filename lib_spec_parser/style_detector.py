"""Style detector — gherkin / ears / connextra / plain.

Traces: LIB-FR-03
Determinism: D (正規表現マッチング順序で決定論的解決)
"""

from __future__ import annotations

import re

_GHERKIN_KEYWORDS = re.compile(
    r"\b(Feature:|Scenario(?:\s+Outline)?:|Given\b|When\b|Then\b)",
    re.MULTILINE,
)

# EARS: shall 文 + EARS keyword (When/While/Where/If) or ubiquitous "The system shall"
_EARS_PATTERN = re.compile(
    r"(\bThe\s+system\s+shall\b|"
    r"\bWhen\b[^.\n]*?\bshall\b|"
    r"\bWhile\b[^.\n]*?\bshall\b|"
    r"\bWhere\b[^.\n]*?\bshall\b|"
    r"\bIf\b[^.\n]*?\bthen\b[^.\n]*?\bshall\b)",
    re.IGNORECASE,
)

_CONNEXTRA_PATTERN = re.compile(
    r"\bAs\s+a[n]?\s+.+?,\s*I\s+want\s+.+?,\s*so\s+that\s+.+",
    re.IGNORECASE | re.DOTALL,
)


def detect(text: str, configured_style: str = "auto") -> str:
    """style を判定する。

    Args:
        text: section / spec テキスト
        configured_style: "auto" | "gherkin" | "ears" | "connextra" | "plain"

    Returns:
        "gherkin" | "ears" | "connextra" | "plain"
        (configured_style != "auto" の場合はそのまま返す)
    """
    if configured_style != "auto":
        return configured_style

    # Priority order (per 07-spec.md determinism note):
    # Gherkin → EARS → Connextra → Plain
    if _has_gherkin(text):
        return "gherkin"
    if _EARS_PATTERN.search(text):
        return "ears"
    if _CONNEXTRA_PATTERN.search(text):
        return "connextra"
    return "plain"


def _has_gherkin(text: str) -> bool:
    """Gherkin pattern detection — require ≥ 2 distinct keyword categories
    to avoid misclassifying isolated "Given a request" style sentences.
    """
    found_kinds: set[str] = set()
    for m in _GHERKIN_KEYWORDS.finditer(text):
        kw = m.group(1).rstrip(":")
        if kw.startswith("Scenario"):
            found_kinds.add("Scenario")
        else:
            found_kinds.add(kw)
        if len(found_kinds) >= 2:
            return True
    return False
