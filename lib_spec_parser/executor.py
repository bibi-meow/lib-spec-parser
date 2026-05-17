"""SpecParserExecutor — ParserExecutorPort 実装.

Traces: LIB-FR-01〜07
Determinism: D
"""

from __future__ import annotations

import hashlib
from typing import Any

from .diagram_extractor import extract_diagrams
from .errors import ParseError
from .format_detector import detect_format
from .models import SpecContent
from .section_assembler import assemble_sections
from .spec_id_extractor import extract_spec_ids
from .trace_tag_extractor import extract_trace_tags


def _spec_id_to_dict(s) -> dict[str, Any]:
    return {"value": s.value, "id_type": s.id_type, "line_number": s.line_number}


def _trace_tag_to_dict(t) -> dict[str, Any]:
    return {
        "raw_line": t.raw_line,
        "referenced_ids": list(t.referenced_ids),
        "line_number": t.line_number,
    }


def _scenario_to_dict(s) -> dict[str, Any]:
    return {
        "name": s.name,
        "given": list(s.given),
        "when": list(s.when),
        "then": list(s.then),
        "examples": [dict(e) for e in s.examples],
    }


def _section_to_dict(s) -> dict[str, Any]:
    return {
        "section_id": s.section_id,
        "style": s.style,
        "raw_text": s.raw_text,
        "keywords": list(s.keywords),
        "shall_clauses": list(s.shall_clauses),
        "scenarios": [_scenario_to_dict(sc) for sc in s.scenarios],
    }


def _diagram_to_dict(d) -> dict[str, Any]:
    return {
        "diagram_type": d.diagram_type,
        "raw_content": d.raw_content,
        "start_line": d.start_line,
        "end_line": d.end_line,
    }


def _spec_content_to_dict(c: SpecContent) -> dict[str, Any]:
    return {
        "spec_ids": [_spec_id_to_dict(s) for s in c.spec_ids],
        "sections": [_section_to_dict(s) for s in c.sections],
        "trace_tags": [_trace_tag_to_dict(t) for t in c.trace_tags],
        "embedded_diagrams": [_diagram_to_dict(d) for d in c.embedded_diagrams],
    }


def _make_artifact_id(path: str) -> str:
    """path から決定論的に artifactId を生成する。"""
    h = hashlib.sha1(path.encode("utf-8")).hexdigest()[:12]
    return f"spec:{path}:{h}"


class SpecParserExecutor:
    """ParserExecutorPort の実装。

    SpecParser は config (dict) / raw_content (bytes) / path (str) を受け取り、
    NormalizedArtifact (dict) を返す。bc-verification-engine.md §6 で定義された
    共有契約型はこの lib では直接 import せず dict / TypedDict 形式で交換する。
    """

    def execute(
        self,
        config: dict[str, Any],
        raw_content: bytes,
        path: str,
    ) -> dict[str, Any]:
        """spec ファイルを NormalizedArtifact (dict) へ変換する。

        Raises:
            ValueError: config.enabled == False or artifact_type mismatch
            ParseError: UTF-8 decode 失敗 / 未対応拡張子 / parser 内部失敗
        """
        # 1. 入力検証
        if not config.get("enabled", True):
            raise ValueError("ParserConfig is disabled (enabled=False)")
        artifact_type = config.get("artifact_type", "spec")
        if artifact_type != "spec":
            raise ValueError(f"unexpected artifact_type: {artifact_type!r}")

        params = config.get("params", {}) or {}

        # 2. デコード
        try:
            text = raw_content.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ParseError(f"UTF-8 decode failed: {e}") from e

        # 3. フォーマット検出（未対応なら ParseError raise）
        file_format = detect_format(path, text)
        # file_format is kept for future content-type specific handling;
        # currently the same Markdown-based assembler covers md/rst, and yaml
        # is accepted as plain text pass-through to spec_id / trace_tag extraction.
        _ = file_format

        # 4. configured style
        configured_style = params.get("spec_style", "auto")

        # 5/6. SpecSection 組立 (Markdown 見出し境界 + parser 振り分け)
        try:
            sections = assemble_sections(text, default_style=configured_style)
        except Exception as e:  # noqa: BLE001 — wrap into ParseError per fail-fast contract
            if isinstance(e, ParseError):
                raise
            raise ParseError(f"section_assembler failed: {e}") from e

        # 7. SpecId 抽出
        extract_ids_flag = params.get("extract_ids", True)
        spec_ids = extract_spec_ids(text) if extract_ids_flag else []

        # 8. TraceTag 抽出
        trace_format = params.get("trace_format", "Traces:")
        trace_tags = extract_trace_tags(text, trace_format)

        # 9. DiagramRef 抽出
        extract_diagrams_flag = params.get("extract_diagrams", True)
        diagrams = extract_diagrams(text) if extract_diagrams_flag else []

        # 10. SpecContent 組立
        content = SpecContent(
            spec_ids=spec_ids,
            sections=sections,
            trace_tags=trace_tags,
            embedded_diagrams=diagrams,
        )

        # 11. NormalizedArtifact (dict) 生成
        return {
            "artifactId": _make_artifact_id(path),
            "artifactType": "spec",
            "content": _spec_content_to_dict(content),
        }
