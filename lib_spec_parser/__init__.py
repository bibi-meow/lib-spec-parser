"""lib-spec-parser — parses specification files and extracts structured content."""

__version__ = "0.1.0"

from lib_spec_parser.executor import SpecParserExecutor
from lib_spec_parser.models import (
    ArtifactId,
    DiagramRef,
    NormalizedArtifact,
    ParserConfig,
    Scenario,
    SpecContent,
    SpecId,
    SpecSection,
    TraceTag,
)

__all__ = [
    "SpecParserExecutor",
    "NormalizedArtifact",
    "SpecContent",
    "SpecSection",
    "SpecId",
    "TraceTag",
    "DiagramRef",
    "Scenario",
    "ArtifactId",
    "ParserConfig",
]
