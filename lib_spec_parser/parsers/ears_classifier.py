"""EARS classifier: classifies EARS requirement patterns and extracts shall clauses."""

import re
from typing import List, Optional

# EARS pattern definitions (order matters: more specific first)
_PATTERNS = [
    ("event-driven", re.compile(r"(?i)\bwhen\b.+\bshall\b")),
    ("state-driven", re.compile(r"(?i)\bwhile\b.+\bshall\b")),
    ("optional", re.compile(r"(?i)\bwhere\b.+\bshall\b")),
    ("unwanted", re.compile(r"(?i)\bif\b.+\bthen\b.+\bshall\b")),
    ("ubiquitous", re.compile(r"(?i)\bthe\s+\w+\s+shall\b")),
]

_SHALL_PATTERN = re.compile(r"(?i)[^.]*\bshall\b[^.]*\.?")


def classify_ears(text: str) -> Optional[str]:
    """Classify a text fragment as an EARS pattern type.

    Returns:
        "ubiquitous" | "event-driven" | "state-driven" | "optional" | "unwanted" | None
    """
    for name, pattern in _PATTERNS:
        if pattern.search(text):
            return name
    return None


def extract_shall_clauses(text: str) -> List[str]:
    """Extract all 'shall' clauses from text.

    Returns:
        List of sentence strings containing 'shall'.
    """
    clauses = []
    # Split by sentence boundaries and find those with 'shall'
    sentences = re.split(r"(?<=[.!?])\s+|\n", text)
    for sentence in sentences:
        if re.search(r"(?i)\bshall\b", sentence):
            clauses.append(sentence.strip())
    return [c for c in clauses if c]
