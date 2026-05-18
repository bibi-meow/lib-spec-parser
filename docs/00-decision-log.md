# lib-spec-parser Decision Log

> Key design decisions recorded for traceability.

---

## Decision #1-1: No external dependencies

- **What**: Whether to use external parsing libraries (e.g., mistune, python-markdown)
- **Options considered**: A) Use mistune for Markdown parsing / B) stdlib + regex only
- **Decision**: B — stdlib + regex only
- **Rationale**: Minimizes dependency surface; spec parsing requirements are well-bounded and
  achievable with regex. Avoids version conflicts in downstream pip installs.
- **Determinism**: D (deterministic)
- **Reviewable by**: Check `pyproject.toml` dependencies = []
- **Traces from**: US-01, US-02
- **Traces to**: 04-oss-selection.md

---

## Decision #1-2: DiagramRef contains raw_source only (no GraphModel)

- **What**: Whether diagram_parser should produce a parsed graph model
- **Options considered**: A) Parse diagram AST / B) Return raw_source only
- **Decision**: B — raw_source only; GraphModel is diagram_parser's responsibility
- **Rationale**: Single-responsibility principle. lib-spec-parser detects diagram fences;
  lib-diagram-parser converts them to graph models. Clean contract boundary.
- **Determinism**: D
- **Reviewable by**: DiagramRef dataclass in models.py has no graph fields
- **Traces from**: US-05
- **Traces to**: 02-diagram-spec.md

---

## Decision #1-3: Section splitting at h2/h3 only

- **What**: Which heading levels to use as section boundaries
- **Options considered**: A) h1-h6 all / B) h2-h3 only / C) configurable
- **Decision**: B — h2 and h3 as boundaries
- **Rationale**: h1 is typically the document title; h4+ are too granular for spec sections.
  h2/h3 matches common spec document conventions.
- **Determinism**: D
- **Reviewable by**: section_assembler.py regex `#{2,3}`
- **Traces from**: US-06
- **Traces to**: 06-architecture.md

---

## Decision #1-4: Style detection priority order

- **What**: When multiple styles could match, which takes precedence
- **Options considered**: A) Gherkin > Connextra > EARS > plain / B) EARS > Gherkin > Connextra > plain
- **Decision**: A — Gherkin first (requires Feature:/Scenario: markers), then Connextra, then EARS
- **Rationale**: Gherkin has the most distinctive markers (Feature:/Scenario:). EARS uses common
  words (when/while/shall) that could appear in non-EARS text. Requiring explicit markers for
  Gherkin reduces false positives.
- **Determinism**: D
- **Reviewable by**: style_detector.py detection order
- **Traces from**: US-06a
- **Traces to**: style_detector.py
