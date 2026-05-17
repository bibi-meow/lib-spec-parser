"""Gherkin parser — Given/When/Then + Scenario Outline + Examples.

Traces: LIB-FR-01, LIB-FR-07
Determinism: D (state machine)
"""

from __future__ import annotations

from ..models import Scenario


def _new_state() -> dict:
    return {
        "name": "",
        "given": [],
        "when": [],
        "then": [],
        "examples": [],
        "is_outline": False,
        "in_examples": False,
        "examples_header": None,
    }


def _flush(current: dict, scenarios: list[Scenario]) -> None:
    if not current["name"] and not (current["given"] or current["when"] or current["then"]):
        return
    scenarios.append(
        Scenario(
            name=current["name"],
            given=tuple(current["given"]),
            when=tuple(current["when"]),
            then=tuple(current["then"]),
            examples=tuple(current["examples"]),
        )
    )


def _parse_table_row(line: str) -> list[str]:
    # Strip leading/trailing pipes and split
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [cell.strip() for cell in s.split("|")]


def parse_gherkin(text: str) -> list[Scenario]:
    """Gherkin テキストから Scenario リストを抽出する。

    Args:
        text: Gherkin 形式テキスト（``` mermaid 等の fence は呼び出し側で除去済み想定）

    Returns:
        Scenario の出現順リスト
    """
    scenarios: list[Scenario] = []
    current: dict | None = None
    last_step_type: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        # Skip Feature lines
        if line.startswith("Feature:"):
            continue

        # Scenario or Scenario Outline header
        if line.startswith("Scenario Outline:") or line.startswith("Scenario:"):
            if current is not None:
                _flush(current, scenarios)
            current = _new_state()
            current["is_outline"] = line.startswith("Scenario Outline:")
            # split on first ':'
            current["name"] = line.split(":", 1)[1].strip()
            last_step_type = None
            continue

        if current is None:
            # Lines before any Scenario header are ignored.
            continue

        # Examples block
        if line.startswith("Examples:"):
            current["in_examples"] = True
            current["examples_header"] = None
            last_step_type = None
            continue

        if current["in_examples"]:
            if line.startswith("|"):
                row = _parse_table_row(line)
                if current["examples_header"] is None:
                    current["examples_header"] = row
                else:
                    header = current["examples_header"]
                    if len(row) == len(header):
                        current["examples"].append(dict(zip(header, row)))
                continue
            else:
                # Examples block ended
                current["in_examples"] = False

        # Step lines
        if line.startswith("Given "):
            current["given"].append(line[len("Given ") :])
            last_step_type = "given"
        elif line.startswith("When "):
            current["when"].append(line[len("When ") :])
            last_step_type = "when"
        elif line.startswith("Then "):
            current["then"].append(line[len("Then ") :])
            last_step_type = "then"
        elif line.startswith("And ") or line.startswith("But "):
            if last_step_type is not None:
                current[last_step_type].append(line[len("And ") :])
        # ignore other lines (e.g., comments, blank, narrative)

    if current is not None:
        _flush(current, scenarios)

    return scenarios
