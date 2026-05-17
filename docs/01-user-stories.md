# lib-spec-parser User Stories

> cicd の sys.1-userstory.md の対応 US から lib-level US を導出する。
> design doc §7 Step 2 参照。

## 対応 cicd US

| cicd US ID | タイトル | 本 lib の関連性 |
|-----------|---------|--------------|
| US-01 | Spec→Code 意味的一致の自動検証 | 関連 — spec 側の構造抽出（spec_ids / sections / trace_tags）が下流 spec_code_verifier の前提 |
| US-02 | コード変更時の spec 影響特定 | 関連 — spec_ids と trace_tags の網羅抽出が change_impact_analyzer の入力 |
| US-05 | spec 間の論理的矛盾検出 | 関連 — SpecSection 単位の構造化（style 判定）が contradiction_detector の入力 |
| US-06 | テスト網羅性の指摘（advisory） | 関連 — spec_ids と trace_tags が spec_test_verifier のカバレッジ判定の前提 |
| US-06a | spec 差分点の自動抽出 | 関連 — sections の構造化が diff 可能形式を提供（change_impact_analyzer） |
| US-22 | Spec-Code 両端一致レビュー | 関連 — spec→code 方向だけでなく code→spec 方向の参照基盤として NormalizedArtifact を完全提供 |
| US-23 | 論理的一致 PR 保証 | 関連 — Gherkin scenarios / EARS shall_clauses 抽出が論理層検証（bisimulation / LLM）への入力 |

正規ドキュメント引用根拠:
- `cicd/doc/sys/user-stories/sys.1-userstory.md` §5.1 US-01/02/05/06/06a, §5.5 US-22/23
- `cicd/doc/sys/lib/.../lib-spec-parser.md` の "対応 US" 欄

---

## US-L-01: spec ファイルの正規化と NormalizedArtifact 生成

**As a** Verification Engine BC（SD-02 Artifact Processing）
**I want** Markdown / YAML / RST 形式の spec ファイルを `NormalizedArtifact(artifactType="spec", content=SpecContent(...))` に正規化する
**So that** SD-01 Strategy 群が spec 内部構造（spec_ids / sections / trace_tags / embedded_diagrams）に依存することなく一律のオブジェクトとして spec ↔ code 一致検証を実行できる

**Acceptance Criteria:**
- [ ] Given `.md` / `.yaml` / `.rst` ファイルの raw_content（bytes） / When `execute(config, raw_content, path)` を呼び出す / Then `NormalizedArtifact.artifactType == "spec"` かつ `content` が `SpecContent` を満たす
- [ ] Given UTF-8 でデコード不能なバイト列 / When `execute()` を呼び出す / Then `ParseError` が raise される
- [ ] Given `config.enabled == False` / When `execute()` を呼び出す / Then `ValueError` が raise される
- [ ] Given Gherkin スタイルの Markdown spec / When `execute()` を呼び出す / Then `SpecContent.sections[*].style == "gherkin"` が含まれる

**cicd US 参照**: US-01
**Decision Log**: #2-1

---

## US-L-02: Traces タグの正確抽出

**As a** Verification Engine BC（SD-02 Artifact Processing）
**I want** spec ファイル内の `Traces: <ID>, <ID>, ...` 形式のタグを 1 件も漏らさず構造化抽出する
**So that** 下流 lib（change_impact_analyzer / trace_mapper）が spec ↔ code の trace 関係を正確に追跡でき、コード変更時に影響する spec 要件が自動特定される

**Acceptance Criteria:**
- [ ] Given spec に `Traces: FR-01, US-03` の行が含まれる / When `execute()` を呼び出す / Then `SpecContent.trace_tags` に 1 件以上のエントリが含まれ `referenced_ids == ["FR-01", "US-03"]` を満たす
- [ ] Given Traces タグが複数行に存在 / When `execute()` を呼び出す / Then 各行の `line_number` が原文の行番号を正確に保持する
- [ ] Given `config.params.trace_format` が `"Refs:"` に変更されている / When `execute()` を呼び出す / Then `Refs:` 形式のタグのみが抽出される
- [ ] Given Traces タグの ID 区切りが空白・カンマ混在 / When 抽出 / Then 全 ID が正規化された形式で `referenced_ids` に格納される

**cicd US 参照**: US-02
**Decision Log**: #2-2

---

## US-L-03: SpecSection スタイルの自動判定

**As a** Verification Engine BC（SD-02 Artifact Processing）
**I want** 各 SpecSection に対して記述スタイル（gherkin / ears / connextra / plain）を自動判定する
**So that** contradiction_detector が style 別に異なる照合アルゴリズム（Gherkin scenario 同士の整合性 / EARS shall 文の論理矛盾検出 など）を選択でき、論理的矛盾検出の精度が上がる

**Acceptance Criteria:**
- [ ] Given `Feature:` + `Scenario:` + `Given/When/Then` を含むセクション / When `execute()` を呼び出す / Then `SpecSection.style == "gherkin"`
- [ ] Given `shall` を含む 5 パターン（Ubiquitous/Event-driven/State-driven/Optional/Unwanted）のいずれかにマッチする文 / When 判定 / Then `SpecSection.style == "ears"`
- [ ] Given `As a ..., I want ..., so that ...` 形式 / When 判定 / Then `SpecSection.style == "connextra"`
- [ ] Given 上記のいずれにも該当しない節 / When 判定 / Then `SpecSection.style == "plain"`
- [ ] Given `config.params.spec_style == "gherkin"` で明示固定 / When 判定 / Then 内容に依らず `style == "gherkin"` で固定される

**cicd US 参照**: US-05
**Decision Log**: #2-3

---

## US-L-04: spec_ids と trace_tags の網羅抽出

**As a** Verification Engine BC（SD-02 Artifact Processing）
**I want** spec ファイル内の SpecId（US-XX / FR-NNN / REQ-NNN / NFR-NNN / AR / EA / PR / PE / AD）と TraceTag を 1 件も漏らさず抽出する
**So that** spec_test_verifier がテストカバレッジを判定するときに「テストが trace タグで参照していない spec_id」を正確に列挙でき、テスト網羅性の指摘が advisory として有効に機能する

**Acceptance Criteria:**
- [ ] Given spec 全文に `US-01 / FR-003 / REQ-007 / NFR-002 / AR-01 / EA-02 / PR-01 / PE-03 / AD-01` の各形式 ID が含まれる / When `execute()` を呼び出す / Then `SpecContent.spec_ids` に全 ID が `id_type` 付きで含まれる
- [ ] Given 同一 ID が複数箇所に出現 / When 抽出 / Then duplicate を含め全 occurrence が記録される（または unique 化＋ occurrence map のいずれかが decision として明示される）
- [ ] Given `config.params.extract_ids == False` / When `execute()` を呼び出す / Then `SpecContent.spec_ids == []`

**cicd US 参照**: US-06
**Decision Log**: #2-4

---

## US-L-05: SpecSection の構造化（diff 可能形式）

**As a** Verification Engine BC（SD-02 Artifact Processing）
**I want** spec ファイルを節（section）単位に分解し、各節を `section_id` / `style` / `raw_text` / `keywords` / `shall_clauses` / `scenarios` のフィールドで構造化する
**So that** change_impact_analyzer が前回 baseline と今回 spec の SpecSection 単位で diff を取れて、追加/削除/変更された spec ID と関連コードへの修正提案が可能になる

**Acceptance Criteria:**
- [ ] Given spec が複数の Markdown 見出し（`## US-01`, `## US-02`）を含む / When `execute()` を呼び出す / Then `SpecContent.sections` に各見出しごとに 1 件以上のエントリが生成され `section_id` が SpecId と一致する
- [ ] Given EARS スタイルの節 / When `execute()` を呼び出す / Then `SpecSection.shall_clauses` に各 shall 文が原文のまま格納される
- [ ] Given Gherkin スタイルの節 / When `execute()` を呼び出す / Then `SpecSection.scenarios` に `name / given / when / then` を持つ `Scenario` オブジェクトが格納される
- [ ] Given 各 SpecSection の `raw_text` / When 確認 / Then 該当節の原文テキストが情報損失なく保持される

**cicd US 参照**: US-06a
**Decision Log**: #2-5

---

## US-L-06: NormalizedArtifact の完全提供（spec → code / code → spec 両方向）

**As a** Verification Engine BC（SD-02 Artifact Processing）
**I want** SpecContent の 4 フィールド（spec_ids / sections / trace_tags / embedded_diagrams）を例外なく全て提供し、抽出失敗時は ParseError を raise する（partial output で fallback しない）
**So that** spec_code_verifier が spec→code と code→spec の両方向で参照可能な完全な NormalizedArtifact を受け取り、両端一致レビュー（spec→code: 実装漏れ検出 / code→spec: undocumented 検出）の精度が保証される

**Acceptance Criteria:**
- [ ] Given 正常な spec ファイル / When `execute()` を呼び出す / Then 戻り値の `SpecContent` の 4 フィールド全てが initialize 済み（空 list でも構わないが `None` ではない）
- [ ] Given parse 途中で復元不能なエラー（不正な UTF-8 / 未対応フォーマット） / When `execute()` を呼び出す / Then `ParseError` が raise され、部分的な `SpecContent` を返さない
- [ ] Given config に複数 params 設定 / When 全て enabled の場合 / Then 全フィールドが populate される

**cicd US 参照**: US-22
**Decision Log**: #2-6

---

## US-L-07: Gherkin Scenario / EARS shall_clauses の完全抽出

**As a** Verification Engine BC（SD-02 Artifact Processing）
**I want** Gherkin の Given-When-Then 構造と EARS の 5 パターン shall 文を 1 件も取りこぼさず抽出する
**So that** logical_consistency_prover（US-23）が Layer M（AST + bisimulation）で論理層検証を行うときに、spec の前提・結論・制約の完全な集合に対して証明を実行でき、PR 境界で論理的一致性が保証される

**Acceptance Criteria:**
- [ ] Given Gherkin `Scenario:` ブロック / When `execute()` を呼び出す / Then `Scenario.given / when / then` がそれぞれ list として全行を保持する
- [ ] Given Gherkin `Scenario Outline:` + `Examples:` テーブル / When `execute()` を呼び出す / Then `Scenario.examples` に Examples テーブルの全行が dict として展開される
- [ ] Given EARS の 5 パターンを含む spec / When `execute()` を呼び出す / Then `SpecSection.shall_clauses` に 5 パターン全ての shall 文が ears_pattern ラベル付きで含まれる
- [ ] Given Scenario が複数ある節 / When 抽出 / Then 全 Scenario が独立した `Scenario` オブジェクトとして列挙される

**cicd US 参照**: US-23
**Decision Log**: #2-7

---
