"""lib-spec-parser — spec-reviewer pip package.

Public API:
    execute(config, raw_content, path) -> dict   (NormalizedArtifact-as-dict)
    SpecParserExecutor                            (ParserExecutorPort impl)
"""

from __future__ import annotations

from typing import Any

from .executor import SpecParserExecutor

__version__ = "0.1.0"

__all__ = ["execute", "SpecParserExecutor", "__version__"]


def execute(config: dict[str, Any], raw_content: bytes, path: str) -> dict[str, Any]:
    """Top-level convenience wrapper around `SpecParserExecutor.execute()`.

    Args:
        config: ParserConfig as dict.
        raw_content: spec file bytes (UTF-8 expected).
        path: VCS path (used for extension-based format detection).

    Returns:
        NormalizedArtifact as dict: {artifactId, artifactType, content}.
    """
    return SpecParserExecutor().execute(config, raw_content, path)
