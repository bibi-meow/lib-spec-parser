# lib-spec-parser Requirements

> cicd の lib-spec-parser.md から lib-level の機能要求（FR）を導出する。
> design doc §7 Step 5 参照。
> **Gherkin 形式で受入テスト（AT）を記述すること。**

---

## 対応 cicd lib 設計

| 設計ドキュメント | パス |
|---------------|------|
| lib-spec-parser.md | `cicd/doc/sys/lib/.../lib-spec-parser.md` |
| Verification Engine BC Tactical | `cicd/doc/sys/business-process/bc-verification-engine.md` §6（NormalizedArtifact / SpecContent / ParserConfig 定義） |
| sys.1-userstory.md | `cicd/doc/sys/user-stories/sys.1-userstory.md` §5 US-01/02/05/06/06a/22/23 |

---

## 機能要求一覧

| FR ID | 説明 | 対応 US-L | 決定論性 | Decision Log |
|-------|------|----------|---------|-------------|
| LIB-FR-01 | MD/YAML/RST → NormalizedArtifact 生成 | US-L-01 | D | #6-1 |
| LIB-FR-02 | `Traces:` タグの正確抽出 | US-L-02 | D | #6-2 |
| LIB-FR-03 | SpecSection style 自動判定（gherkin/ears/connextra/plain） | US-L-03 | D | #6-3 |
| LIB-FR-04 | SpecId 網羅抽出（US/FR/REQ/NFR/AR/EA/PR/PE/AD） | US-L-04 | D | #6-4 |
| LIB-FR-05 | SpecSection の構造化（全フィールド） | US-L-05 | D | #6-5 |
| LIB-FR-06 | embedded_diagrams 抽出（Mermaid/PlantUML/ASCII Art） | US-L-06 | D (mermaid/plantuml) / H (ascii_art) | #6-6 |
| LIB-FR-07 | Gherkin Scenario / EARS shall_clauses の完全抽出 | US-L-07 | D | #6-7 |

## 非機能要求一覧

| NFR ID | 説明 | 検証手法 |
|--------|------|--------|
| LIB-NFR-01 | 1 MB の Markdown ファイルを 2 秒以内に parse できること | pytest-benchmark で測定 |
| LIB-NFR-02 | pyright strict モードで型エラーがないこと | `pyright --strict lib_spec_parser/` で確認 |
| LIB-NFR-03 | 全 FR の受入テストが pytest で green であること | `pytest tests/ -v` |

---

## LIB-FR-01: Markdown spec ファイルの正規化

**概要**: spec ファイル（MD/YAML/RST）を読み込み、`NormalizedArtifact(artifactType="spec", content=SpecContent(...))` に変換する。

**入力**: `raw_content: bytes`, `path: str`, `config: ParserConfig`
**出力**: `NormalizedArtifact`
**決定論性**: D

### Gherkin 受入テスト

```gherkin
Feature: Markdown spec ファイルの正規化
  spec ファイルを NormalizedArtifact へ変換する

  Scenario: Gherkin スタイルの Markdown spec を parse する
    Given spec ファイル "feature.md" に Gherkin シナリオが含まれている
    And config.params.spec_style == "auto"
    When execute(config, raw_content, "feature.md") を呼び出す
    Then NormalizedArtifact.artifactType == "spec"
    And NormalizedArtifact.content.sections[0].style == "gherkin"
    And NormalizedArtifact.content.sections[0].scenarios が 1 件以上存在する

  Scenario: 不正な UTF-8 バイト列が入力された場合
    Given raw_content が不正な UTF-8 バイト列 (0xFF, 0xFE)
    When execute(config, raw_content, "broken.md") を呼び出す
    Then ParseError が raise される
```

**AT ファイル**: `tests/test_execute.py`
**Decision Log**: #6-1

---

## LIB-FR-02: Traces タグの正確抽出

**概要**: spec ファイル内の `Traces: <ID>, <ID>, ...` 行を全件抽出し `List[TraceTag]` として返す。

**入力**: spec 全文 `text: str`, `trace_format: str` (default `"Traces:"`)
**出力**: `List[TraceTag]`（各エントリは `raw_line` / `referenced_ids` / `line_number` を持つ）
**決定論性**: D

### Gherkin 受入テスト

```gherkin
Feature: Traces タグの正確抽出
  spec ファイル内の Traces: タグから参照 ID を構造化抽出する

  Scenario: 標準形式の Traces タグを抽出する
    Given spec ファイルに L42 に "Traces: FR-01, US-03" が含まれている
    When execute() を呼び出す
    Then SpecContent.trace_tags に 1 件のエントリがあり
    And entry.referenced_ids == ["FR-01", "US-03"]
    And entry.line_number == 42

  Scenario: trace_format をカスタマイズした場合
    Given config.params.trace_format == "Refs:"
    And spec に "Refs: AR-01" と "Traces: FR-01" の両方が存在
    When execute() を呼び出す
    Then SpecContent.trace_tags には Refs: のみが抽出され Traces: は含まれない

  Scenario: 区切りが空白とカンマ混在の場合
    Given spec に "Traces: FR-01,US-02  AR-03" の行が含まれる
    When execute() を呼び出す
    Then trace_tags[0].referenced_ids == ["FR-01", "US-02", "AR-03"]
```

**AT ファイル**: `tests/test_trace_tag_extractor.py`
**Decision Log**: #6-2

---

## LIB-FR-03: SpecSection style 自動判定

**概要**: 各 SpecSection に対して style（"gherkin" / "ears" / "connextra" / "plain"）を自動判定する。`config.params.spec_style` で明示固定も可。

**入力**: section の `raw_text: str`, `spec_style: str` (default `"auto"`)
**出力**: `style: str`
**決定論性**: D

### Gherkin 受入テスト

```gherkin
Feature: SpecSection style 自動判定
  各セクションの記述スタイルを 4 種類に分類する

  Scenario: Gherkin スタイルを判定する
    Given セクションに "Feature:" + "Scenario:" + "Given/When/Then" が含まれる
    When style_detector.detect(text, spec_style="auto") を呼び出す
    Then 戻り値 == "gherkin"

  Scenario: EARS スタイル（Event-driven）を判定する
    Given セクションに "When <trigger>, the <system> shall <response>" の文がある
    When style_detector.detect(text, "auto") を呼び出す
    Then 戻り値 == "ears"

  Scenario: Connextra スタイルを判定する
    Given セクションに "As a user, I want X, so that Y" が含まれる
    When style_detector.detect(text, "auto") を呼び出す
    Then 戻り値 == "connextra"

  Scenario: いずれにも該当しない節は plain
    Given セクションが単なる自然言語の記述のみ
    When style_detector.detect(text, "auto") を呼び出す
    Then 戻り値 == "plain"

  Scenario: 明示固定モード
    Given config.params.spec_style == "gherkin"
    And セクションは plain な自然言語
    When style_detector.detect(text, "gherkin") を呼び出す
    Then 戻り値 == "gherkin" (内容に依らず固定)
```

**AT ファイル**: `tests/test_style_detector.py`
**Decision Log**: #6-3

---

## LIB-FR-04: SpecId 網羅抽出

**概要**: spec ファイル全文から SpecId（プレフィックス `US/FR/REQ/NFR/AR/EA/PR/PE/AD`）を正規表現で網羅抽出する。

**入力**: spec 全文 `text: str`, `extract_ids: bool` (default `True`)
**出力**: `List[SpecId]`
**決定論性**: D

### Gherkin 受入テスト

```gherkin
Feature: SpecId 網羅抽出
  spec ファイル内の SpecId を 9 種類のプレフィックスで網羅抽出する

  Scenario: 全プレフィックスの ID を抽出する
    Given spec 全文に US-01 / FR-003 / REQ-007 / NFR-002 / AR-01 / EA-02 / PR-01 / PE-03 / AD-01 が含まれる
    When execute() を呼び出す
    Then SpecContent.spec_ids には 9 件のエントリが存在し
    And 各エントリの id_type が "US"|"FR"|"REQ"|"NFR"|"AR"|"EA"|"PR"|"PE"|"AD" のいずれかと一致する

  Scenario: 同一 ID が複数箇所に出現
    Given spec に "US-01" が 3 箇所に登場
    When execute() を呼び出す
    Then SpecContent.spec_ids には "US-01" が 3 件 occurrence として記録される

  Scenario: extract_ids が False の場合
    Given config.params.extract_ids == False
    When execute() を呼び出す
    Then SpecContent.spec_ids == []
```

**AT ファイル**: `tests/test_spec_id_extractor.py`
**Decision Log**: #6-4

---

## LIB-FR-05: SpecSection の構造化（全フィールド）

**概要**: spec ファイルを節（section）単位に分解し、SpecSection（section_id / style / raw_text / keywords / shall_clauses / scenarios）に構造化する。

**入力**: spec 全文 `text: str`, `style`（FR-03 出力）
**出力**: `List[SpecSection]`
**決定論性**: D

### Gherkin 受入テスト

```gherkin
Feature: SpecSection の構造化
  spec ファイルを節単位で構造化し diff 可能形式を提供する

  Scenario: Markdown 見出しごとに節分割
    Given spec ファイルが "## US-01" と "## US-02" の 2 見出しを含む
    When execute() を呼び出す
    Then SpecContent.sections.len == 2
    And sections[0].section_id == "US-01"
    And sections[1].section_id == "US-02"

  Scenario: EARS スタイルの節の shall_clauses
    Given 節が "The system shall ..." 文を 3 つ含む
    When execute() を呼び出す
    Then sections[0].style == "ears"
    And sections[0].shall_clauses.len == 3

  Scenario: Gherkin スタイルの節の scenarios
    Given 節が "Scenario: A" と "Scenario: B" の 2 シナリオを含む
    When execute() を呼び出す
    Then sections[0].style == "gherkin"
    And sections[0].scenarios.len == 2
    And sections[0].scenarios[0].name == "A"

  Scenario: raw_text の情報損失なし
    Given 節の原文が 100 行のテキスト
    When execute() を呼び出す
    Then sections[0].raw_text にその 100 行が情報損失なく保持される
```

**AT ファイル**: `tests/test_section_assembler.py`
**Decision Log**: #6-5

---

## LIB-FR-06: embedded_diagrams 抽出

**概要**: spec ファイルに埋め込まれた Mermaid / PlantUML / ASCII Art の図ブロックを抽出し `List[DiagramRef]` を返す。

**入力**: spec 全文 `text: str`, `extract_diagrams: bool` (default `True`)
**出力**: `List[DiagramRef]`
**決定論性**: D (mermaid / plantuml) / H (ascii_art)

### Gherkin 受入テスト

```gherkin
Feature: embedded_diagrams 抽出
  spec 内に埋め込まれた図ブロックを抽出する

  Scenario: Mermaid コードブロックの抽出
    Given spec ファイルに ```mermaid\nflowchart TD\nA-->B\n``` が L10-L12 に存在
    When execute() を呼び出す
    Then SpecContent.embedded_diagrams[0].diagram_type == "mermaid"
    And embedded_diagrams[0].start_line == 11
    And embedded_diagrams[0].end_line == 12
    And embedded_diagrams[0].raw_content に "flowchart TD" が含まれる

  Scenario: PlantUML @startuml ブロックの抽出
    Given spec ファイルに "@startuml ... @enduml" が含まれる
    When execute() を呼び出す
    Then embedded_diagrams のいずれかの diagram_type == "plantuml"

  Scenario: extract_diagrams が False の場合
    Given config.params.extract_diagrams == False
    When execute() を呼び出す
    Then SpecContent.embedded_diagrams == []
```

**AT ファイル**: `tests/test_diagram_extractor.py`
**Decision Log**: #6-6

---

## LIB-FR-07: Gherkin Scenario / EARS shall_clauses の完全抽出

**概要**: Gherkin の Given-When-Then 構造と EARS 5 パターンの shall 文を 1 件も漏らさず抽出する。

**入力**: section の `raw_text: str`, `style: str`
**出力**: `Scenario` リスト（Gherkin 時）または `shall_clauses` リスト（EARS 時）
**決定論性**: D

### Gherkin 受入テスト

```gherkin
Feature: Gherkin/EARS 完全抽出
  論理層検証に必要な仕様文要素を抽出する

  Scenario: Gherkin の Given-When-Then を抽出する
    Given Scenario ブロックに Given 2 行 / When 1 行 / Then 1 行
    When gherkin_parser.parse(text) を呼び出す
    Then scenarios[0].given.len == 2
    And scenarios[0].when.len == 1
    And scenarios[0].then.len == 1

  Scenario: Scenario Outline + Examples の展開
    Given "Scenario Outline:" + "Examples:" テーブル 3 行
    When gherkin_parser.parse(text) を呼び出す
    Then scenarios[0].examples.len == 3
    And 各 example が dict 形式で Examples テーブルの列名をキーとして持つ

  Scenario: EARS 5 パターンを分類する
    Given spec に Ubiquitous / Event-driven / State-driven / Optional / Unwanted の各パターン文がある
    When ears_classifier.classify(text) を呼び出す
    Then 戻り値 SpecSection.shall_clauses に 5 件の文が含まれ
    And 各文に ears_pattern ラベルが付与されている

  Scenario: Scenario が複数ある節
    Given 節に Scenario が 3 件含まれる
    When gherkin_parser.parse(text) を呼び出す
    Then scenarios.len == 3 (独立 Scenario オブジェクト)
```

**AT ファイル**: `tests/test_gherkin_parser.py`, `tests/test_ears_classifier.py`
**Decision Log**: #6-7

---
