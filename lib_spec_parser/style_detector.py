"""Style detector: auto-detects spec style from text content."""

import re

# EARS patterns (checked before plain)
_EARS_PATTERNS = [
    re.compile(r"(?i)\bwhen\b.+\bshall\b"),
    re.compile(r"(?i)\bwhile\b.+\bshall\b"),
    re.compile(r"(?i)\bwhere\b.+\bshall\b"),
    re.compile(r"(?i)\bif\b.+\bthen\b.+\bshall\b"),
    re.compile(r"(?i)\bthe\s+\w+\s+shall\b"),
]

# Gherkin requires Feature: or Scenario: markers, not just step keywords
_GHERKIN_PATTERN = re.compile(r"(?im)^(Feature:|Scenario(?: Outline)?:|Example:)")
_CONNEXTRA_PATTERN = re.compile(r"(?i)\bas\s+a\b.+\bi\s+want\b", re.DOTALL)


def detect_style(text: str) -> str:
    """Auto-detect the spec style of the given text.

    Returns:
        "gherkin" | "ears" | "connextra" | "usdm" | "plain"
    """
    if not text.strip():
        return "plain"

    if _GHERKIN_PATTERN.search(text):
        return "gherkin"

    if _CONNEXTRA_PATTERN.search(text):
        return "connextra"

    for pattern in _EARS_PATTERNS:
        if pattern.search(text):
            return "ears"

    return "plain"
