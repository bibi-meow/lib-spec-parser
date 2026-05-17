# lib-spec-parser System Architecture

> lib のアーキテクチャを定義する。モジュール構成・DFD・エラー処理を明確にする。
> design doc §7 Step 6 参照。
> **lib は caller を意識しない独立設計とすること（strategy-pattern-lib-impl.md 参照）。**

---

## 目的

spec ファイル（Markdown / YAML / RST）を読み込み、Verification Engine BC の SD-01 Strategy 群が参照できる `NormalizedArtifact(artifactType="spec")` に正規化する。spec_ids / sections / trace_tags / embedded_diagrams の 4 フィールドを下流 lib（spec_code_verifier / contradiction_detector / spec_test_verifier / change_impact_analyzer / architecture_verifier）に提供する。

## 入力 / 出力

| 種別 | 型 | 説明 |
|------|-----|------|
| 入力 | `ParserConfig` | artifact_type / executor_lib / params (extract_ids, trace_format, spec_style, extract_diagrams) / enabled |
| 入力 | `raw_content: bytes` | spec ファイルの生バイト列（UTF-8 想定） |
| 入力 | `path: str` | VCS 上のファイルパス（拡張子でフォーマット補助判定） |
| 出力 | `NormalizedArtifact` | artifactType="spec" + content=SpecContent(...)（4 フィールド全 populate） |

---

## モジュール構成

```
lib_spec_parser/
├── __init__.py             # パッケージ公開 API: SpecParserExecutor.execute()
├── executor.py             # SpecParserExecutor — ParserExecutorPort の実装本体
├── format_detector.py      # .md/.yaml/.rst 拡張子 + コンテンツ解析でフォーマット判定
├── style_detector.py       # テキスト内容からスタイル判定（gherkin/ears/connextra/plain/auto）
├── parsers/
│   ├── __init__.py
│   ├── gherkin_parser.py   # Given-When-Then + Scenario Outline → List[SpecSection]（lark-parser 使用）
│   ├── ears_classifier.py  # 5 パターン正規表現 → SpecSection(style="ears", shall_clauses)
│   ├── connextra_parser.py # As/I want/So that → SpecSection(style="connextra")
│   └── generic_parser.py   # plain テキスト → SpecId + TraceTag 抽出のみ
├── section_assembler.py    # parser 出力を List[SpecSection] に組立
├── diagram_extractor.py    # Mermaid/PlantUML/ASCII Art ブロック → List[DiagramRef]
├── spec_id_extractor.py    # 正規表現で SpecId 一覧抽出
├── trace_tag_extractor.py  # "Traces:" タグ抽出
├── models.py               # SpecId, TraceTag, SpecSection, Scenario, DiagramRef, SpecContent 型定義
├── errors.py               # ParseError 例外型定義
└── tests/
    ├── test_executor.py
    ├── test_format_detector.py
    ├── test_style_detector.py
    ├── test_gherkin_parser.py
    ├── test_ears_classifier.py
    ├── test_connextra_parser.py
    ├── test_generic_parser.py
    ├── test_section_assembler.py
    ├── test_diagram_extractor.py
    ├── test_spec_id_extractor.py
    └── test_trace_tag_extractor.py
```

| モジュール | 責務 | 決定論性 |
|-----------|------|---------|
| `executor.py` | 全工程のオーケストレーション（入力検証 → デコード → format/style 判定 → parser 振り分け → 組立 → 戻り値生成） | D |
| `format_detector.py` | 拡張子 + content sniff でフォーマット (`md`/`yaml`/`rst`) 判定 | D |
| `style_detector.py` | テキスト内容からスタイル判定（正規表現マッチング） | D |
| `parsers/gherkin_parser.py` | Gherkin AST 生成（lark-parser のカスタム文法） | D |
| `parsers/ears_classifier.py` | 5 パターン正規表現分類 | D |
| `parsers/connextra_parser.py` | As/I want/So that 正規表現分解 | D |
| `parsers/generic_parser.py` | plain テキスト処理（SpecId + TraceTag のみ抽出） | D |
| `section_assembler.py` | 見出し境界で section 分割し parser 出力を組立 | D |
| `diagram_extractor.py` | コードブロック抽出 + ヒューリスティック判定 | D (mermaid/plantuml) / H (ascii_art) |
| `spec_id_extractor.py` | 9 種類のプレフィックス正規表現で SpecId 一覧抽出 | D |
| `trace_tag_extractor.py` | `Traces:` 行を正規表現で抽出 | D |
| `models.py` | dataclass 型定義のみ（ロジックなし） | D |
| `errors.py` | 例外型定義のみ | D |

---

## DFD (Data Flow Diagram)

```
[raw_content: bytes, path: str, config: ParserConfig]
                 │
                 ▼
         [executor: 入力検証 (config.enabled)]
                 │
                 ▼
         [executor: UTF-8 デコード → text: str]
                 │
                 ▼
         [format_detector] ─────────▶ file_format ("md"/"yaml"/"rst")
                 │
                 ▼
         [style_detector] ──────────▶ style ("gherkin"/"ears"/"connextra"/"plain")
                 │
        ┌────────┼────────┬─────────┬─────────┐
        ▼        ▼        ▼         ▼         ▼
  [gherkin_  [ears_   [connextra_  [generic_  (style により振り分け)
   parser]   classi-   parser]      parser]
              fier]
        │        │        │         │
        └────────┴────────┴─────────┘
                 │
                 ▼
         [section_assembler] ─────▶ sections: List[SpecSection]
                 │
                 ▼
         (parallel)
         ┌─────────────────┬─────────────────┬───────────────────┐
         ▼                 ▼                 ▼                   ▼
  [spec_id_extractor] [trace_tag_     [diagram_extractor]   (no-op if extract_*=False)
                       extractor]
         │                 │                 │
         ▼                 ▼                 ▼
   List[SpecId]      List[TraceTag]    List[DiagramRef]
         │                 │                 │
         └─────────────────┴─────────────────┘
                          │
                          ▼
              [executor: SpecContent 組立]
                          │
                          ▼
              [executor: NormalizedArtifact 生成]
                          │
                          ▼
              [NormalizedArtifact(artifactType="spec", content=SpecContent)]
```

| プロセス | 入力 DF | 出力 DF | 決定論性 |
|---------|---------|---------|---------|
| 入力検証 | `config` | validated config | D |
| UTF-8 デコード | `raw_content: bytes` | `text: str` | D |
| format_detector | `path, text` | `file_format` | D |
| style_detector | `text, config.params.spec_style` | `style` | D |
| gherkin_parser | `text` (style=gherkin) | `List[SpecSection]` | D |
| ears_classifier | `text` (style=ears) | `List[SpecSection]` | D |
| connextra_parser | `text` (style=connextra) | `List[SpecSection]` | D |
| generic_parser | `text` (style=plain) | `List[SpecSection]` | D |
| section_assembler | parser 出力 | `List[SpecSection]` | D |
| spec_id_extractor | `text` | `List[SpecId]` | D |
| trace_tag_extractor | `text, trace_format` | `List[TraceTag]` | D |
| diagram_extractor | `text` | `List[DiagramRef]` | D / H |
| SpecContent 組立 | 各 list | `SpecContent` | D |

---

## モジュール ↔ FR 対応表

| モジュール | 対応 FR | 対応 US-L |
|-----------|--------|----------|
| `executor.py` | LIB-FR-01 | US-L-01, US-L-06 |
| `format_detector.py` | LIB-FR-01 | US-L-01 |
| `style_detector.py` | LIB-FR-03 | US-L-03 |
| `parsers/gherkin_parser.py` | LIB-FR-01, LIB-FR-07 | US-L-01, US-L-07 |
| `parsers/ears_classifier.py` | LIB-FR-01, LIB-FR-07 | US-L-01, US-L-07 |
| `parsers/connextra_parser.py` | LIB-FR-01 | US-L-01 |
| `parsers/generic_parser.py` | LIB-FR-01 | US-L-01 |
| `spec_id_extractor.py` | LIB-FR-04 | US-L-04 |
| `trace_tag_extractor.py` | LIB-FR-02 | US-L-02 |
| `diagram_extractor.py` | LIB-FR-06 | US-L-06 |
| `section_assembler.py` | LIB-FR-05 | US-L-05 |
| `models.py` | 全 FR（型基盤） | 全 US-L |
| `errors.py` | LIB-FR-01, LIB-FR-06（fail-fast 契約） | US-L-06 |

---

## エラー処理

| エラー条件 | 発生モジュール | 処理方針 | 例外型 |
|-----------|-------------|---------|-------|
| `config.enabled == False` | executor | `ValueError` を raise | `ValueError` |
| UTF-8 デコード失敗 | executor | エラー詳細を含む `ParseError` を raise | `ParseError` |
| 未対応フォーマット（path 拡張子が `md`/`yaml`/`rst` 以外） | format_detector | `ParseError` を raise | `ParseError` |
| Gherkin 文法エラー（lark-parser が raise） | gherkin_parser | エラー詳細を `ParseError` で wrap して raise | `ParseError` |
| YAML 構文エラー（PyYAML が raise） | format_detector / generic_parser | `ParseError` で wrap して raise | `ParseError` |
| RST 構文エラー（docutils が raise） | format_detector / generic_parser | `ParseError` で wrap して raise | `ParseError` |
| section_assembler で部分的に失敗 | section_assembler | `ParseError` を raise（partial output 禁止 — US-L-06） | `ParseError` |

> **fail-fast 契約**: US-L-06（NormalizedArtifact 完全提供）に従い、本 lib は partial output を返さない。途中で復元不能なエラーが発生したら必ず `ParseError` を raise する。

---

## 依存 OSS

| OSS | バージョン | 用途 | ライセンス |
|-----|-----------|------|---------|
| mistletoe | ^1.3.0 | Markdown AST parsing | MIT |
| lark-parser | ^1.1.0 | Gherkin AST parsing（カスタム EBNF 文法） | MIT |
| PyYAML | ^6.0 | YAML parsing | MIT |
| docutils | ^0.21.0 | RST parsing | BSD-2-Clause / Public Domain |

Python 標準 `re` モジュールで EARS / Connextra / SpecId / Traces を処理（追加 OSS 不要）。

**Decision Log**: #7-1（アーキテクチャ選択の判断を記録）

---

<!-- Step 7 Spec 記述時に DFD との差異が見つかった場合は本ファイルを更新する -->
