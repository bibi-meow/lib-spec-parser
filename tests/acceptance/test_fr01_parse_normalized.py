"""FR-01: execute() returns NormalizedArtifact."""

from lib_spec_parser import NormalizedArtifact, ParserConfig, SpecParserExecutor

SIMPLE_MD = b"""# My Spec

## FR-001 Login Feature

The system shall allow users to log in.
"""


def _config(**params) -> ParserConfig:
    return ParserConfig(
        artifact_type="spec",
        executor_lib="lib-spec-parser",
        params=params,
    )


class TestFR01ParseNormalized:
    def test_returns_normalized_artifact(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), SIMPLE_MD, "spec.md")
        assert isinstance(result, NormalizedArtifact)

    def test_artifact_type_is_spec(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), SIMPLE_MD, "spec.md")
        assert result.artifact_type == "spec"

    def test_artifact_id_path(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), SIMPLE_MD, "path/to/spec.md")
        assert result.artifact_id.path == "path/to/spec.md"

    def test_content_has_sections(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), SIMPLE_MD, "spec.md")
        assert result.content.sections is not None

    def test_yaml_input_parsed(self):
        yaml_content = b"spec_id: US-01\ndescription: Login feature\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), yaml_content, "spec.yaml")
        assert isinstance(result, NormalizedArtifact)

    def test_rst_input_parsed(self):
        rst_content = b"Login Feature\n=============\n\nUS-01: The system shall allow login.\n"
        executor = SpecParserExecutor()
        result = executor.execute(_config(), rst_content, "spec.rst")
        assert isinstance(result, NormalizedArtifact)

    def test_empty_content_returns_artifact(self):
        executor = SpecParserExecutor()
        result = executor.execute(_config(), b"", "empty.md")
        assert isinstance(result, NormalizedArtifact)
        assert result.artifact_type == "spec"
