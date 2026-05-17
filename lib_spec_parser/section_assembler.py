"""Section assembler — Markdown 見出し境界で節分割し SpecSection を組み立てる.

Traces: LIB-FR-05
Determinism: D
"""

from __future__ import annotations

import re

from .models import SpecSection
from .parsers.ears_classifier import classify_ears
from .parsers.gherkin_parser import parse_gherkin
from .spec_id_extractor import extract_spec_ids
from .style_detector import detect as detect_style

# Markdown headings: lines starting with one or more '#'
_HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)

# Extract a SpecId-like token from a heading line for section_id
_SECTION_ID_PATTERN = re.compile(r"\b(US|FR|REQ|NFR|AR|EA|PR|PE|AD)-(\d+[a-z]?)\b")

# Mermaid fenced block — captured to extract Gherkin payload from a ```gherkin ... ``` block
_GHERKIN_FENCE_PATTERN = re.compile(
    r"```gherkin[ \t]*\n(.*?)```",
    re.DOTALL,
)


def _section_id_from_heading(heading_text: str) -> str:
    m = _SECTION_ID_PATTERN.search(heading_text)
    return m.group(0) if m else ""


def _extract_gherkin_payload(section_text: str) -> str:
    """Return the concatenated Gherkin payload(s) from fenced blocks in the section.

    If no fenced block, returns the section text itself (so plain Gherkin still parses).
    """
    parts: list[str] = []
    for m in _GHERKIN_FENCE_PATTERN.finditer(section_text):
        parts.append(m.group(1))
    if parts:
        return "\n".join(parts)
    return section_text


def assemble_sections(text: str, default_style: str = "auto") -> list[SpecSection]:
    """Markdown 見出し境界で節を分割し SpecSection リストを返す。

    Args:
        text: spec 全文
        default_style: 全節に適用する固定 style（"auto" 時は section ごとに自動判定）

    Returns:
        List[SpecSection]
    """
    # Find heading positions
    headings = list(_HEADING_PATTERN.finditer(text))

    sections: list[SpecSection] = []

    if not headings:
        # Entire text is one anonymous section
        if text.strip():
            sections.append(_make_section("", text, default_style))
        return sections

    # Pre-amble before first heading (only emitted if non-empty)
    first_start = headings[0].start()
    preamble = text[:first_start]
    if preamble.strip():
        sections.append(_make_section("", preamble, default_style))

    for i, h in enumerate(headings):
        heading_line = h.group(0)
        heading_text = h.group(2)
        section_id = _section_id_from_heading(heading_text)
        body_start = h.end()
        body_end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        # Include the heading line itself in raw_text so the section is faithful
        raw_text = heading_line + "\n" + text[body_start:body_end]
        sections.append(_make_section(section_id, raw_text, default_style))

    return sections


def _make_section(
    section_id: str,
    raw_text: str,
    default_style: str,
) -> SpecSection:
    style = detect_style(raw_text, default_style)
    shall_clauses: tuple[str, ...] = ()
    scenarios: tuple = ()
    keywords: tuple[str, ...] = ()

    if style == "gherkin":
        payload = _extract_gherkin_payload(raw_text)
        scenarios = tuple(parse_gherkin(payload))
        keywords = ("Feature", "Scenario", "Given", "When", "Then")
    elif style == "ears":
        ears_entries = classify_ears(raw_text)
        shall_clauses = tuple(e["text"] for e in ears_entries)
        keywords = tuple(sorted({e["ears_pattern"] for e in ears_entries}))
    elif style == "connextra":
        keywords = ("As", "I want", "so that")
    else:
        # plain
        keywords = ()

    # Capture any spec id references as keywords for plain too (optional)
    ids = extract_spec_ids(raw_text)
    if ids and not keywords:
        keywords = tuple(sorted({i.value for i in ids}))

    return SpecSection(
        section_id=section_id,
        style=style,
        raw_text=raw_text,
        keywords=keywords,
        shall_clauses=shall_clauses,
        scenarios=scenarios,
    )
