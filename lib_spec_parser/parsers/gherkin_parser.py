"""Gherkin parser: extracts Feature/Scenario/Steps from BDD-style text."""

import re
from typing import List, Union

from lib_spec_parser.models import Scenario

_SCENARIO_PATTERN = re.compile(r"(?im)^(?:Scenario(?: Outline)?|Example):\s*(.+)$")
_STEP_PATTERN = re.compile(r"(?im)^\s+(Given|When|Then|And|But)\s+(.+)$")

_GHERKIN_KEYWORDS = [
    "Feature:",
    "Scenario:",
    "Scenario Outline:",
    "Examples:",
    "Given",
    "When",
    "Then",
    "And",
    "But",
]


def parse_gherkin(text: str, return_keywords: bool = False) -> Union[List[Scenario], List[str]]:
    """Parse Gherkin text and extract scenarios (or keywords if requested).

    Args:
        text: Raw Gherkin text.
        return_keywords: If True, return list of detected keywords instead of scenarios.

    Returns:
        List of Scenario objects, or list of keyword strings if return_keywords=True.
    """
    if return_keywords:
        found = []
        for kw in _GHERKIN_KEYWORDS:
            if re.search(re.escape(kw), text, re.IGNORECASE):
                found.append(kw)
        return found

    scenarios: list[Scenario] = []
    for match in _SCENARIO_PATTERN.finditer(text):
        name = match.group(1).strip()
        start = match.end()
        # Find next scenario or end of text
        next_match = _SCENARIO_PATTERN.search(text, start)
        end = next_match.start() if next_match else len(text)
        body = text[start:end]

        steps = []
        for step_match in _STEP_PATTERN.finditer(body):
            keyword = step_match.group(1)
            content = step_match.group(2).strip()
            steps.append(f"{keyword} {content}")

        scenarios.append(Scenario(name=name, steps=steps))

    return scenarios
