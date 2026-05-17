"""SpecId extractor — 9 種プレフィックスの正規表現抽出。

Traces: LIB-FR-04
"""

from __future__ import annotations

import re

from .models import SpecId

# Match prefixes US/FR/REQ/NFR/AR/EA/PR/PE/AD followed by hyphen,
# digits, and optional single lowercase suffix letter.
_SPEC_ID_PATTERN = re.compile(r"\b(US|FR|REQ|NFR|AR|EA|PR|PE|AD)-(\d+[a-z]?)\b")


def extract_spec_ids(text: str) -> list[SpecId]:
    """spec 全文から SpecId を網羅抽出する。

    Args:
        text: spec 全文

    Returns:
        List[SpecId]（重複は occurrence 単位で記録）
    """
    results: list[SpecId] = []
    # Pre-compute cumulative char-to-line lookup
    line_starts: list[int] = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            line_starts.append(i + 1)

    for m in _SPEC_ID_PATTERN.finditer(text):
        value = m.group(0)
        id_type = m.group(1)
        # Find 1-based line number for the match start
        pos = m.start()
        # Binary search would be faster but sequential is fine for typical spec sizes
        line_no = 1
        for idx, start in enumerate(line_starts):
            if start > pos:
                line_no = idx
                break
            line_no = idx + 1
        results.append(SpecId(value=value, id_type=id_type, line_number=line_no))
    return results
