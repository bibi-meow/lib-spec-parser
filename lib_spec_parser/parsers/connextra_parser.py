"""Connextra parser: parses 'As a / I want / So that' user story format."""

import re
from typing import List

_CONNEXTRA_PATTERN = re.compile(
    r"(?i)as\s+a\s+(?P<role>[^,]+),\s*i\s+want\s+(?P<goal>[^,.]+)(?:,?\s*so\s+that\s+(?P<benefit>.+))?",
    re.DOTALL,
)


def parse_connextra(text: str) -> List[dict]:  # type: ignore[type-arg]
    """Parse Connextra user stories from text.

    Returns:
        List of dicts with keys: role, goal, benefit.
    """
    results = []
    for match in _CONNEXTRA_PATTERN.finditer(text):
        results.append(
            {
                "role": match.group("role").strip(),
                "goal": match.group("goal").strip(),
                "benefit": (match.group("benefit") or "").strip(),
            }
        )
    return results
