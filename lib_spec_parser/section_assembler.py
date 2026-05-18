"""Section assembler: splits Markdown content into SpecSection objects."""

import re
from typing import List

from lib_spec_parser.models import Scenario, SpecSection
from lib_spec_parser.parsers.ears_classifier import extract_shall_clauses
from lib_spec_parser.parsers.gherkin_parser import parse_gherkin
from lib_spec_parser.style_detector import detect_style

# Match h2 and h3 headings
_HEADING_PATTERN = re.compile(r"(?m)^(#{2,3})\s+(.+)$")


def assemble_sections(text: str, forced_style: str | None = None) -> List[SpecSection]:
    """Split Markdown text into SpecSection objects at h2/h3 boundaries.

    Args:
        text: Raw markdown text.
        forced_style: Override style detection ("gherkin"|"ears"|"connextra"|"usdm"|"plain"|None).

    Returns:
        List of SpecSection objects.
    """
    sections: list[SpecSection] = []
    headings = list(_HEADING_PATTERN.finditer(text))

    if not headings:
        # No headings — treat whole text as one section if non-empty
        stripped = text.strip()
        if stripped:
            style = forced_style or detect_style(stripped)
            section = _build_section("", style, stripped)
            sections.append(section)
        return sections

    for i, heading_match in enumerate(headings):
        heading_text = heading_match.group(2).strip()
        start = heading_match.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        body = text[start:end].strip()

        style = forced_style or detect_style(body)
        section = _build_section(heading_text, style, body)
        sections.append(section)

    return sections


def _build_section(heading: str, style: str, body: str) -> SpecSection:
    """Build a SpecSection with appropriate sub-data based on style."""
    keywords: list[str] = []
    shall_clauses: list[str] = []
    scenarios: list[Scenario] = []

    if style == "gherkin":
        parsed = parse_gherkin(body)
        scenarios = parsed  # type: ignore[assignment]
        keywords = ["Scenario", "Given", "When", "Then"]
    elif style == "ears":
        shall_clauses = extract_shall_clauses(body)
        keywords = ["shall"]
    elif style == "connextra":
        keywords = ["As a", "I want", "So that"]

    return SpecSection(
        section_id=heading,
        style=style,
        raw_text=body,
        keywords=keywords,
        shall_clauses=shall_clauses,
        scenarios=scenarios,
    )
