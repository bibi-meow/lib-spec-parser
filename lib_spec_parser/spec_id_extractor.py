"""SpecId extractor: extracts requirement IDs from text using configurable prefixes."""

import re
from typing import List

_DEFAULT_PREFIXES = ["US", "FR", "NFR", "REQ", "AR", "AD"]


def _build_pattern(prefixes: List[str]) -> re.Pattern:  # type: ignore[type-arg]
    prefix_group = "|".join(re.escape(p) for p in prefixes)
    return re.compile(rf"\b({prefix_group})-\d+\b")


def extract_spec_ids(text: str, prefixes: List[str] | None = None) -> List[str]:
    """Extract requirement IDs from text.

    Args:
        text: Raw text to search.
        prefixes: List of ID prefixes to match. Defaults to US, FR, NFR, REQ, AR, AD.

    Returns:
        List of unique ID strings in order of first occurrence.
    """
    if prefixes is None:
        prefixes = _DEFAULT_PREFIXES

    pattern = _build_pattern(prefixes)
    # Use finditer to get full matches (findall returns captured group only)
    seen: dict[str, None] = {}
    results = []
    for m in pattern.finditer(text):
        val = m.group(0)
        if val not in seen:
            seen[val] = None
            results.append(val)
    return results
