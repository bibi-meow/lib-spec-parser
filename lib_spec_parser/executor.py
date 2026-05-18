"""SpecParserExecutor: main entry point for lib-spec-parser."""

from lib_spec_parser.diagram_extractor import extract_diagrams
from lib_spec_parser.format_detector import detect_format
from lib_spec_parser.models import (
    ArtifactId,
    NormalizedArtifact,
    ParserConfig,
    SpecContent,
    SpecId,
    TraceTag,
)
from lib_spec_parser.section_assembler import assemble_sections
from lib_spec_parser.spec_id_extractor import extract_spec_ids
from lib_spec_parser.trace_tag_extractor import extract_trace_tags


class SpecParserExecutor:
    """Parses specification files and returns NormalizedArtifact objects.

    Supported formats: Markdown (.md), YAML (.yaml/.yml), RST (.rst).
    """

    def execute(
        self,
        config: ParserConfig,
        raw_content: bytes,
        path: str,
    ) -> NormalizedArtifact:
        """Parse a spec file and return a NormalizedArtifact.

        Steps:
            1. Detect file format from extension.
            2. Decode bytes to UTF-8 text.
            3. Determine spec_style (auto or forced).
            4. Assemble sections.
            5. Extract SpecIds (if extract_ids=True).
            6. Extract TraceTags.
            7. Extract DiagramRefs (if extract_diagrams=True).
            8. Build and return NormalizedArtifact.

        Args:
            config: ParserConfig with params controlling extraction.
            raw_content: Raw bytes of the spec file.
            path: File path (used for artifact_id and diagram IDs).

        Returns:
            NormalizedArtifact with artifact_type="spec".
        """
        params = config.params or {}

        # Step 1: detect format (informational; we handle all as text for now)
        _fmt = detect_format(path)

        # Step 2: decode
        text = raw_content.decode("utf-8", errors="replace") if raw_content else ""

        # Step 3: determine style
        spec_style = params.get("spec_style", "auto")
        forced_style = None if spec_style == "auto" else spec_style

        # Step 4: assemble sections
        sections = assemble_sections(text, forced_style=forced_style)

        # Step 5: extract SpecIds
        extract_ids = params.get("extract_ids", True)
        spec_ids = []
        if extract_ids:
            prefixes = params.get("id_prefixes", None)
            raw_ids = extract_spec_ids(text, prefixes=prefixes)
            spec_ids = [SpecId(value=sid) for sid in raw_ids]

        # Step 6: extract TraceTags
        trace_format = params.get("trace_format", "Traces:")
        raw_tags = extract_trace_tags(text, trace_format=trace_format)
        trace_tags = [TraceTag(raw=tag) for tag in raw_tags]

        # Step 7: extract DiagramRefs
        extract_diag = params.get("extract_diagrams", True)
        embedded_diagrams = []
        if extract_diag:
            embedded_diagrams = extract_diagrams(text, path)

        # Step 8: build artifact
        content = SpecContent(
            spec_ids=spec_ids,
            sections=sections,
            trace_tags=trace_tags,
            embedded_diagrams=embedded_diagrams,
        )

        return NormalizedArtifact(
            artifact_id=ArtifactId(path=path),
            artifact_type="spec",
            content=content,
        )
