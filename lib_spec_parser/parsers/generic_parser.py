"""Generic parser: plain text spec processing."""

from typing import List


def parse_generic(text: str) -> List[str]:
    """Extract meaningful lines from plain text spec.

    Returns:
        List of non-empty lines.
    """
    return [line.strip() for line in text.splitlines() if line.strip()]
