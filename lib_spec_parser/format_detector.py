"""Format detector — .md/.yaml/.rst 拡張子判定。

Traces: LIB-FR-01
"""

from __future__ import annotations

import os

from .errors import ParseError

_EXT_MAP = {
    ".md": "md",
    ".markdown": "md",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".rst": "rst",
}


def detect_format(path: str, text: str) -> str:
    """path の拡張子から file format を判定する。

    Args:
        path: ファイルパス
        text: ファイル内容（現状未使用、将来の content sniff 用）

    Returns:
        "md" | "yaml" | "rst"

    Raises:
        ParseError: 未対応拡張子
    """
    _, ext = os.path.splitext(path.lower())
    if ext in _EXT_MAP:
        return _EXT_MAP[ext]
    raise ParseError(
        f"unsupported file extension: {ext!r} (path={path!r}); "
        f"supported: .md, .markdown, .yaml, .yml, .rst"
    )
