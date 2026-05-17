# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-05-18

### Added

- `SpecParserExecutor.execute()` — parse Markdown/YAML/RST spec files into `NormalizedArtifact`
- `execute()` — module-level convenience function
- Format detection: `.md` / `.yaml` / `.yml` / `.rst`
- Style detection: Gherkin / EARS / Connextra / Plain (auto mode)
- `spec_id_extractor` — extract requirement IDs with 9 default prefixes (US/FR/REQ/NFR/AR/EA/PR/PE/AD)
- `trace_tag_extractor` — extract configurable `Traces:` tag lines
- `diagram_extractor` — extract Mermaid and PlantUML blocks
- `section_assembler` — split Markdown on headings into `SpecSection` list
- Gherkin parser: Given/When/Then, Scenario Outline + Examples
- EARS classifier: 5 patterns (Ubiquitous/Event-driven/State-driven/Optional/Unwanted)
- Connextra parser: As/I want/So that decomposition
- `ParseError` exception with fail-fast contract
- 87 tests (unit + acceptance) covering all 7 functional requirements
- CI: ruff + pyright + pytest (Python 3.11 / 3.12)
