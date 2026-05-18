# lib-spec-parser OSS Selection

## Decision: No External Dependencies

lib-spec-parser uses **Python standard library only** (regex, dataclasses, os.path).

### Evaluation

| Candidate | Functionality | Maintenance | License | Notes |
|-----------|:------------:|:-----------:|:-------:|-------|
| mistune   | 4 | 4 | BSD | Overkill; AST not needed |
| python-markdown | 3 | 5 | BSD | Extension-heavy; too much for our use case |
| **stdlib regex** | 5 | 5 | N/A | Sufficient for all extraction tasks |

**Decision**: stdlib only — no `[project] dependencies` entries required.

**Rationale**: Spec parsing requirements (ID extraction, fence detection, style detection) are
well-bounded regex problems. Adding a parsing library would increase install footprint with no
functional benefit.

**Decision Log**: #1-1
