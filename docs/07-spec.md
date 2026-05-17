# lib-spec-parser API Spec

> lib の公開 API を定義する。dataclass で型を明示し、pseudocode でアルゴリズムを示す。
> design doc §7 Step 7 参照。
> **API signature は 06-architecture.md の DFD と一致させること。**

---

## 公開 API 一覧

| 関数 / クラス | 入力型 | 出力型 | 決定論性 |
|-------------|-------|-------|---------|
| `SpecParserExecutor.execute` | `ParserConfig`, `bytes`, `str` | `NormalizedArtifact` | D |

---

## 型定義

```python
# 05-requirements.md の LIB-FR-NN と対応させる

from __future__ import annotations
from dataclasses import dataclass, field

# ──────────────────────────────────────────────────
# Inner value types
# ──────────────────────────────────────────────────

@dataclass(frozen=True)
class SpecId:
    """要件 ID（例: US-01, FR-003）。
    
    Traces: LIB-FR-04
    """
    value: str         # 例: "US-01"
    id_type: str       # "US"|"FR"|"REQ"|"NFR"|"AR"|"EA"|"PR"|"PE"|"AD"
    line_number: int   # 出現行（1-based）


@dataclass(frozen=True)
class TraceTag:
    """Traces: タグに列挙された参照 ID。
    
    Traces: LIB-FR-02
    """
    raw_line: str               # 例: "Traces: FR-01, US-03" 全文
    referenced_ids: list[str]   # 例: ["FR-01", "US-03"]
    line_number: int            # 出現行（1-based）


@dataclass(frozen=True)
class Scenario:
    """Gherkin シナリオ 1 件。
    
    Traces: LIB-FR-07
    """
    name: str                       # "Scenario:" 後の文字列
    given: list[str]                # Given 行のリスト
    when: list[str]                 # When 行のリスト
    then: list[str]                 # Then 行のリスト
    examples: list[dict[str, str]]  # Scenario Outline の Examples 表（列名→値）


@dataclass(frozen=True)
class SpecSection:
    """spec ファイルの 1 節。
    
    Traces: LIB-FR-05
    """
    section_id: str             # 節の SpecId（なければ ""）
    style: str                  # "gherkin"|"ears"|"connextra"|"plain"
    raw_text: str               # 節の原文テキスト（情報損失なし）
    keywords: list[str]         # 検出キーワード
    shall_clauses: list[str]    # EARS パターンの shall 文（style="ears" のみ非空）
    scenarios: list[Scenario]   # Gherkin シナリオ（style="gherkin" のみ非空）


@dataclass(frozen=True)
class DiagramRef:
    """埋め込み図ブロックへの参照。
    
    Traces: LIB-FR-06
    """
    diagram_type: str    # "mermaid"|"plantuml"|"ascii_art"
    raw_content: str     # 図ブロックの原文
    start_line: int      # 開始行（1-based）
    end_line: int        # 終了行（1-based）


@dataclass(frozen=True)
class SpecContent:
    """NormalizedArtifact の content フィールド（artifactType="spec" 用）。
    
    Traces: LIB-FR-01, LIB-FR-02, LIB-FR-04, LIB-FR-05, LIB-FR-06
    """
    spec_ids: list[SpecId]              = field(default_factory=list)
    sections: list[SpecSection]         = field(default_factory=list)
    trace_tags: list[TraceTag]          = field(default_factory=list)
    embedded_diagrams: list[DiagramRef] = field(default_factory=list)


# ──────────────────────────────────────────────────
# 外部契約型（bc-verification-engine.md §6 で定義済 — 参照のみ）
# ──────────────────────────────────────────────────

# from cicd.verification_engine.models import (
#     ParserConfig,        # artifact_type / executor_lib / params / enabled
#     NormalizedArtifact,  # artifactId / artifactType / content
# )

# ──────────────────────────────────────────────────
# 例外型
# ──────────────────────────────────────────────────

class ParseError(Exception):
    """spec ファイルの parse に失敗したことを示す。
    
    fail-fast 契約（US-L-06）に基づき、partial output ではなく
    本例外で即座に失敗を伝達する。
    """
    pass
```

---

## API signature

```python
class SpecParserExecutor:
    """ParserExecutorPort の実装。
    
    bc-verification-engine.md §6 で定義された ParserExecutorPort interface
    を実装する単一クラス。本 lib のエントリポイント。
    """

    def execute(
        self,
        config: "ParserConfig",
        raw_content: bytes,
        path: str,
    ) -> "NormalizedArtifact":
        """
        spec ファイルを NormalizedArtifact へ変換する。

        Args:
            config: ParserConfig
                - artifact_type: 期待値 "spec"
                - params.extract_ids: bool (default True)
                - params.trace_format: str (default "Traces:")
                - params.spec_style: str (default "auto") — "gherkin"|"ears"|"connextra"|"auto"
                - params.extract_diagrams: bool (default True)
                - enabled: bool
            raw_content: spec ファイルの生バイト（UTF-8 想定）
            path: VCS 上のファイルパス（拡張子でフォーマット補助判定）

        Returns:
            NormalizedArtifact(
                artifactType="spec",
                content=SpecContent(
                    spec_ids=...,
                    sections=...,
                    trace_tags=...,
                    embedded_diagrams=...,
                )
            )
            — SpecContent の 4 フィールドは全て populate される（None ではない）

        Raises:
            ValueError: config.enabled == False
            ParseError:
                - raw_content が UTF-8 デコード不能
                - path の拡張子が未対応（"md"/"yaml"/"rst" 以外）
                - lark-parser / PyYAML / docutils が文法エラーを raise
                - section_assembler で復元不能な不整合検出

        Traces: LIB-FR-01, LIB-FR-02, LIB-FR-03, LIB-FR-04, LIB-FR-05, LIB-FR-06, LIB-FR-07
        Decision Log: #8-1
        """
        ...
```

---

## Pseudocode

```
function execute(config, raw_content, path):
  # ─── 1. 入力検証 ─────────────────────────────────────
  if not config.enabled:
    raise ValueError("ParserConfig is disabled")
  if config.artifact_type != "spec":
    raise ValueError(f"unexpected artifact_type: {config.artifact_type}")

  # ─── 2. デコード ─────────────────────────────────────
  try:
    text = raw_content.decode("utf-8")
  except UnicodeDecodeError as e:
    raise ParseError(f"UTF-8 decode failed: {e}") from e

  # ─── 3. フォーマット検出 ──────────────────────────────
  file_format = format_detector.detect(path, text)
  # file_format ∈ {"md", "yaml", "rst"}  — 他は ParseError

  # ─── 4. スタイル判定 ─────────────────────────────────
  configured_style = config.params.get("spec_style", "auto")
  style = style_detector.detect(text, configured_style)
  # style ∈ {"gherkin", "ears", "connextra", "plain"}

  # ─── 5. パース振り分け（style ベース） ───────────────
  if style == "gherkin":
    raw_sections = gherkin_parser.parse(text, file_format)
  elif style == "ears":
    raw_sections = ears_classifier.classify(text, file_format)
  elif style == "connextra":
    raw_sections = connextra_parser.parse(text, file_format)
  elif style == "plain":
    raw_sections = generic_parser.parse(text, file_format)
  else:
    raise ParseError(f"unknown style: {style}")
  # ※ style == "auto" は style_detector が解決済（"auto" は戻り値に来ない）

  # ─── 6. SpecSection 組立 ────────────────────────────
  sections: list[SpecSection] = section_assembler.assemble(text, raw_sections, file_format)
  #   ── Determinism: D — 見出し境界 + parser 出力の決定論的マージ

  # ─── 7. SpecId 抽出 ─────────────────────────────────
  extract_ids = config.params.get("extract_ids", True)
  spec_ids: list[SpecId] = (
    spec_id_extractor.extract(text) if extract_ids else []
  )

  # ─── 8. TraceTag 抽出 ───────────────────────────────
  trace_format = config.params.get("trace_format", "Traces:")
  trace_tags: list[TraceTag] = trace_tag_extractor.extract(text, trace_format)

  # ─── 9. DiagramRef 抽出 ─────────────────────────────
  extract_diagrams = config.params.get("extract_diagrams", True)
  embedded_diagrams: list[DiagramRef] = (
    diagram_extractor.extract(text) if extract_diagrams else []
  )

  # ─── 10. SpecContent 組立 ───────────────────────────
  spec_content = SpecContent(
    spec_ids=spec_ids,
    sections=sections,
    trace_tags=trace_tags,
    embedded_diagrams=embedded_diagrams,
  )

  # ─── 11. NormalizedArtifact 生成 ────────────────────
  artifact_id = make_artifact_id(path)  # decision: path をベースに ID を生成（決定論的）
  return NormalizedArtifact(
    artifactId=artifact_id,
    artifactType="spec",
    content=spec_content,
  )
```

### 決定論性ノート

- 全工程が決定論的（D）。LLM 呼び出しは一切なし
- `style == "auto"` の解決は `style_detector` 内で正規表現マッチング順序により決定論的に解決される（Gherkin → EARS → Connextra → Plain の順で最初にマッチしたものを採用）
- ASCII Art の diagram_extractor のみヒューリスティック判定（H）— Mermaid/PlantUML は決定論的

**Decision Log**: #8-1（API 設計の判断を記録）

---

<!-- 実装開始（Step 9）前にこの spec が 06-architecture.md と一致していることを確認すること -->
<!-- 差異があれば先に 06-architecture.md を更新する -->
