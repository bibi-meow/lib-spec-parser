# lib-spec-parser Decision Log

> 全工程の意思決定を時系列で記録する。第三者がトレース可能にする目的。
> design doc §7 Step 0 参照。

---

## 決定 #0-1（Step 0: PoC 対象 lib の選択）

- **What**: Plan C PoC の実装対象 lib として lib-spec-parser を選択
- **Options considered**: lib-spec-parser / lib-code-parser / lib-test-parser（3 共有 Parser lib）
- **Decision**: lib-spec-parser
- **Rationale**: 対応 US が 7 件（US-01/02/05/06/06a/22/23）と最多。spec-reviewer の入口となる基盤 lib であり、他 lib（spec-code-verifier / contradiction-detector 等）が依存する。PoC の「プロセス実動確認」として最もインパクトが大きい。
- **Determinism**: D（SOT: lib-spec-parser.md の "対応 US" 欄から選択）
- **Reviewable by**: lib-index.md §A の依存グラフと lib-spec-parser.md の依存 lib 欄で検証可能
- **Traces from**: libcreator/CLAUDE.md §主ミッション, libcreator/tasklist.md Plan C
- **Traces to**: Step 2 User Story の scope, Step 6 Requirements の FR 数

---

## 決定 #0-2（Step 0: プロセス設計問題の発見と対処方針）

- **What**: lib-impl-process.md Step 0 が docs/ を先行作成するが、init-lib-repo.sh が REPO_DIR 存在を即 exit 1 する矛盾の対処
- **Options considered**: A) init-lib-repo.sh を修正して pyproject.toml 存在のみで拒否 / B) Step 9 を先に実行してから docs を上書き / C) docs/ を staging ディレクトリに書いて Step 9 後に移動
- **Decision**: A) init-lib-repo.sh を修正 — `pyproject.toml` が存在する場合のみ exit 1（既存 docs/ は許容）
- **Rationale**: lib-impl-process.md は「docs/01〜07 が揃った後に scaffold を実行する」と明記（Step 9 comment）。Process の意図を尊重し、script 側を修正するのが最も整合的。T5 テスト（既存 repo への上書き拒否）は pyproject.toml チェックでも等価に成立する。
- **Determinism**: D（修正後の動作は決定論的）
- **Reviewable by**: test_init_lib_repo.sh T5 が修正後も PASS することで検証可能
- **Traces from**: init-lib-repo.sh 既存チェック実装 + lib-impl-process.md Step 0/Step 9
- **Traces to**: Step 9 での init-lib-repo.sh 実行が成功すること

---

## 決定 #2-1（Step 2: US-L-01 — spec ファイル正規化と NormalizedArtifact 生成）

- **What**: cicd US-01（Spec→Code 意味的一致の自動検証）に対応する lib-level US を「MD/YAML/RST → NormalizedArtifact 生成」として定義
- **Options considered**: A) US-01 を split せず lib 全体の責務として表現 / B) フォーマット別に複数 US-L に分割（MD用 / YAML用 / RST用）
- **Decision**: A) フォーマット別に分割せず 1 つの US-L-01 にまとめる
- **Rationale**: lib-spec-parser.md の「spec ファイル（Markdown / YAML / RST）を読み込み、構造化された SpecContent へ正規化する」という単一責任に対応。フォーマット差は内部実装（format_detector）の責務であり US-L 粒度では不要
- **Determinism**: D（SOT: lib-spec-parser.md "概要" 節 + sys.1-userstory.md §5.1 US-01 から導出）
- **Reviewable by**: 01-user-stories.md US-L-01 Acceptance Criteria が SpecContent 4 フィールドの正規化を網羅していること
- **Traces from**: sys.1-userstory.md §5.1 US-01 / lib-spec-parser.md "対応 US" US-01
- **Traces to**: LIB-FR-01 (Step 6), execute() API signature (Step 8)

---

## 決定 #2-2（Step 2: US-L-02 — Traces タグの正確抽出）

- **What**: cicd US-02（コード変更時の spec 影響特定）に対応する lib-level US を「Traces タグの正確抽出」として定義
- **Options considered**: A) 「変更影響特定」を lib-spec-parser の責務に含める / B) 「Traces タグ抽出」のみを責務とし、影響特定は下流 lib（change_impact_analyzer）に委譲
- **Decision**: B) Traces タグ抽出のみ
- **Rationale**: lib-spec-parser.md の依存 lib 欄に「change_impact_analyzer — spec 差分・変更影響分析（US-06a, US-02）」と記載。spec-parser は「spec の中に何が書かれているか」を取り出すのが責務で、影響特定は下流 lib の責務
- **Determinism**: D（lib-spec-parser.md "依存 lib（下流）" から境界が明確）
- **Reviewable by**: US-L-02 AC が trace_format 設定変更・複数行・区切り混在をカバーしていること
- **Traces from**: lib-spec-parser.md "依存 lib（下流）" の change_impact_analyzer の責務境界
- **Traces to**: LIB-FR-02, trace_tag_extractor module (Step 7)

---

## 決定 #2-3（Step 2: US-L-03 — SpecSection スタイル自動判定）

- **What**: cicd US-05（spec 間の論理的矛盾検出）に対応する lib-level US を「style 自動判定」として定義
- **Options considered**: A) 矛盾検出ロジックを lib 内に含める / B) style 判定のみを lib の責務とし、矛盾検出は contradiction_detector に委譲
- **Decision**: B) style 判定のみ
- **Rationale**: lib-spec-parser.md "依存 lib（下流）" で「contradiction_detector — spec 間矛盾検出（US-05）」と記載。spec-parser は style 分類器を提供し、矛盾検出は下流 lib の責務
- **Determinism**: D（5 パターン正規表現分類器は決定論的）
- **Reviewable by**: US-L-03 AC が 4 style + auto / 明示固定 を網羅していること
- **Traces from**: lib-spec-parser.md "採用する検証手法" §1.1, §2.1, §2.4
- **Traces to**: LIB-FR-03, style_detector module (Step 7)

---

## 決定 #2-4（Step 2: US-L-04 — spec_ids と trace_tags 網羅抽出）

- **What**: cicd US-06（テスト網羅性 advisory）に対応する lib-level US を「spec_ids + trace_tags の網羅抽出」として定義
- **Options considered**: A) テストカバレッジ判定を lib 内に含める / B) spec_ids/trace_tags 抽出のみとし、カバレッジ判定は spec_test_verifier に委譲
- **Decision**: B) 抽出のみ
- **Rationale**: lib-spec-parser.md "依存 lib（下流）" で「spec_test_verifier — spec↔test 整合性（US-06）」と記載。カバレッジ判定の前提として spec_ids / trace_tags の完全な抽出が必要
- **Determinism**: D（SpecId プレフィックス正規表現 + Traces 正規表現）
- **Reviewable by**: US-L-04 AC が 9 種類のプレフィックス（US/FR/NFR/AR/EA/PR/PE/AD/REQ）+ extract_ids 設定をカバー
- **Traces from**: cicd CLAUDE.md "SPEC-ID システム" 有効プレフィックス（US/FR/NFR/AR/EA/PR/PE/AD）
- **Traces to**: LIB-FR-04, spec_id_extractor module (Step 7)

---

## 決定 #2-5（Step 2: US-L-05 — SpecSection 構造化）

- **What**: cicd US-06a（spec 差分点の自動抽出）に対応する lib-level US を「SpecSection 単位の構造化（diff 可能形式）」として定義
- **Options considered**: A) 差分抽出ロジックまで lib に含める / B) 構造化のみとし、diff は change_impact_analyzer に委譲
- **Decision**: B) 構造化のみ
- **Rationale**: lib-spec-parser.md "依存 lib（下流）" で「change_impact_analyzer — spec 差分・変更影響分析（US-06a, US-02）」と記載。diff 可能な構造（section_id / style / raw_text / keywords / shall_clauses / scenarios）を提供することで下流が差分を計算可能
- **Determinism**: D（dataclass フィールド構成が決定論的）
- **Reviewable by**: US-L-05 AC が SpecSection 6 フィールド全てを網羅していること
- **Traces from**: bc-verification-engine.md §6 SpecContent 定義
- **Traces to**: LIB-FR-05, section_assembler module (Step 7)

---

## 決定 #2-6（Step 2: US-L-06 — NormalizedArtifact 完全提供）

- **What**: cicd US-22（Spec-Code 両端一致レビュー）に対応する lib-level US を「NormalizedArtifact の完全提供（partial output 禁止）」として定義
- **Options considered**: A) 部分的に parse 失敗してもそこまでの結果を返す / B) parse 失敗時は ParseError raise（all-or-nothing）
- **Decision**: B) all-or-nothing
- **Rationale**: US-22 は spec→code / code→spec の双方向検証を要件とする。partial output を許すと下流の双方向検証で「どのフィールドが信頼できるか」が判定不能になる。fail-fast で完全性を保証する
- **Determinism**: D（all-or-nothing は決定論的契約）
- **Reviewable by**: US-L-06 AC で SpecContent 4 フィールド全 populate と ParseError 動作が定義されている
- **Traces from**: sys.1-userstory.md §5.5 US-22 "双方向それぞれの precision / recall を分離レポート"
- **Traces to**: LIB-FR-06, execute() error contract (Step 8)

---

## 決定 #2-7（Step 2: US-L-07 — Gherkin/EARS 完全抽出）

- **What**: cicd US-23（論理的一致 PR 保証）に対応する lib-level US を「Gherkin Scenario と EARS shall_clauses の完全抽出」として定義
- **Options considered**: A) Gherkin/EARS 以外も論理層検証対象として抽出 / B) Gherkin scenarios + EARS shall_clauses に限定
- **Decision**: B) Gherkin + EARS に限定
- **Rationale**: lib-spec-parser.md "採用する検証手法" 軸 5 評価で §1.1 Gherkin ○ / §2.1 EARS △ が論理層検証の入力として明示。connextra △ は user story 粒度で論理証明には粒度が粗い。Gherkin/EARS が論理層検証の主入力
- **Determinism**: D（軸 5 評価が決定論的判断根拠）
- **Reviewable by**: US-L-07 AC が Gherkin Scenario Outline + Examples + EARS 5 パターン全てを網羅
- **Traces from**: lib-spec-parser.md "採用する検証手法" §1.1 (軸5: ○) + §2.1 (軸5: △) / variants-catalog.md §2 表
- **Traces to**: LIB-FR-07, gherkin_parser / ears_classifier modules (Step 7)

---

## 決定 #3-1（Step 3: 本 lib が扱う diagram の責務範囲）

- **What**: 本 lib は diagram を「生成」せず、spec ファイルに埋め込まれた図ブロックを「抽出」するのみと定義
- **Options considered**: A) 図の意味解釈（ノード/エッジ）まで lib に含める / B) 図ブロックの抽出（DiagramRef）のみとし、解釈は architecture_verifier に委譲
- **Decision**: B) 抽出のみ
- **Rationale**: bc-verification-engine.md §6 "ArchitectureStrategy（SD-01）が実行時に SpecContent.embedded_diagrams（論理アーキ）と CodeContent.call_graph（物理アーキ）から導出する" — 図の意味解釈は SD-01 Strategy（architecture_verifier）の責務であり SD-02 Parser の責務外
- **Determinism**: D（責務境界が SOT で明示済）
- **Reviewable by**: 02-diagram-spec.md で DiagramRef 4 フィールド（diagram_type / raw_content / start_line / end_line）が抽出責務に限定されていること
- **Traces from**: bc-verification-engine.md §6 NormalizedArtifact 定義 + アーキモデル導出ノート
- **Traces to**: Step 4 抽出アルゴリズム / LIB-FR-06 / diagram_extractor module

---

## 決定 #4-1（Step 4: 図ブロック抽出アルゴリズム選択）

- **What**: Mermaid / PlantUML / ASCII Art の 3 種類を抽出アルゴリズム別に分離（同一 lib 内で 3 つの抽出器を持つ）
- **Options considered**: A) 単一の正規表現で全種類を一括抽出 / B) 種別ごとに専用アルゴリズム / C) 汎用コードブロック抽出器 + 種別判定器
- **Decision**: B) 種別ごとに専用アルゴリズム（mermaid / plantuml / ascii_art の 3 関数）
- **Rationale**: Mermaid は ` ```mermaid ` fence、PlantUML は `@startuml`/`@enduml` または ` ```plantuml ` fence、ASCII Art は罫線文字密度ヒューリスティック — 検出ロジックが本質的に異なる。単一正規表現にすると ASCII Art のヒューリスティック判定が混入し決定論性が失われる
- **Determinism**: Mermaid/PlantUML は D、ASCII Art は H
- **Reviewable by**: 03-diagram-generation.md で 3 アルゴリズムが分離され決定論性ラベルが付与されていること
- **Traces from**: 02-diagram-spec.md §本 lib が扱う diagram（3 種類）
- **Traces to**: LIB-FR-06, diagram_extractor module 内の 3 関数

---

## 決定 #5-1（Step 5: OSS 選定）

- **What**: 各 parsing 機能ごとに採用 OSS を確定
  - Markdown: mistletoe
  - Gherkin: lark-parser（カスタム EBNF 文法）
  - YAML: PyYAML
  - RST: docutils
  - EARS/Connextra/SpecId/Traces: Python 標準 `re`
- **Options considered**: 各機能で 3-4 候補を機能性/性能/保守性/ライセンスの 4 軸で評価（04-oss-selection.md 参照）
- **Decision**: 上記の組合せ（全 MIT/BSD/PSF ライセンス）
- **Rationale**:
  - **mistletoe**: AST ベース、依存ゼロ、軽量（markdown-it-py より code base が小さい）
  - **lark-parser**: Gherkin EBNF 文法を表現可能、behave/pytest-bdd は CLI/runner 統合で本 lib 用途には過剰
  - **PyYAML**: YAML 1.2 デファクト、libyaml バインディングで性能良好
  - **docutils**: RST 公式 reference 実装
  - **re**: 正規表現で十分（EARS 5 パターン / Connextra 3 フィールド / SpecId 9 種プレフィックスは全て正規表現で表現可能）
- **Determinism**: 全 D
- **Reviewable by**: 04-oss-selection.md の評価マトリクス（4 軸スコア + 合計）が選定根拠を示している
- **Traces from**: variants-catalog.md §1.1/§1.4/§1.5/§2.1/§2.4 の OSS 実装欄
- **Traces to**: 06-architecture.md "依存 OSS" 節 / `pyproject.toml`（Step 9 で生成予定）

---

## 決定 #6-1（Step 6: LIB-FR-01 — MD/YAML/RST → NormalizedArtifact）

- **What**: US-L-01 を LIB-FR-01 として「MD/YAML/RST → NormalizedArtifact 生成」と定義
- **Determinism**: D
- **Rationale**: US-L-01 は parse 処理全体の責務をカバーするため、FR-01 は execute() 全体の正常系契約として定義する
- **Reviewable by**: 05-requirements.md LIB-FR-01 の Gherkin 受入テストが正常系と異常系（不正 UTF-8）をカバー
- **Traces from**: US-L-01
- **Traces to**: executor.py / 全 parser module

---

## 決定 #6-2（Step 6: LIB-FR-02 — Traces タグ抽出）

- **What**: US-L-02 を LIB-FR-02 として「Traces タグの正確抽出」と定義
- **Determinism**: D（正規表現で実装可能）
- **Rationale**: trace_format パラメータでカスタマイズ可能とし、コンマ/空白混在の区切りに耐性を持つ抽出ロジックを契約に含める
- **Reviewable by**: 05-requirements.md LIB-FR-02 の Gherkin 受入テストが標準形式 / カスタム trace_format / 区切り混在をカバー
- **Traces from**: US-L-02
- **Traces to**: trace_tag_extractor.py

---

## 決定 #6-3（Step 6: LIB-FR-03 — style 自動判定）

- **What**: US-L-03 を LIB-FR-03 として「style 自動判定（gherkin/ears/connextra/plain + 明示固定モード）」と定義
- **Determinism**: D（正規表現マッチング順序で決定論的に解決）
- **Rationale**: spec_style = "auto" の解決順序を「Gherkin → EARS → Connextra → Plain」と決定論的に固定する。複数 style が同一節に混在する場合、最初にマッチしたもののみ採用（曖昧性ゼロ）
- **Reviewable by**: 05-requirements.md LIB-FR-03 の 4 style 検出 + 明示固定モードの受入テスト
- **Traces from**: US-L-03 / lib-spec-parser.md "採用する検証手法" §1.1 §2.1 §2.4
- **Traces to**: style_detector.py

---

## 決定 #6-4（Step 6: LIB-FR-04 — SpecId 網羅抽出）

- **What**: US-L-04 を LIB-FR-04 として「9 種類のプレフィックス（US/FR/REQ/NFR/AR/EA/PR/PE/AD）を網羅抽出」と定義
- **Options considered**: A) duplicate を許容して全 occurrence を記録 / B) unique 化（SpecId.value で deduplicate）
- **Decision**: A) duplicate 許容 + `line_number` フィールドで occurrence を区別可能にする
- **Rationale**: 下流 lib（spec_test_verifier / change_impact_analyzer）が「どの行で参照されているか」を必要とする可能性が高い。本 lib は raw 情報を完全保持し、unique 化は下流の責務
- **Determinism**: D
- **Reviewable by**: 05-requirements.md LIB-FR-04 の 9 プレフィックス検出 + 重複 occurrence 保持の受入テスト
- **Traces from**: US-L-04 / cicd CLAUDE.md "SPEC-ID システム" 有効プレフィックス
- **Traces to**: spec_id_extractor.py / models.py SpecId.line_number フィールド

---

## 決定 #6-5（Step 6: LIB-FR-05 — SpecSection 構造化）

- **What**: US-L-05 を LIB-FR-05 として「SpecSection 6 フィールド（section_id / style / raw_text / keywords / shall_clauses / scenarios）を全 populate」と定義
- **Determinism**: D
- **Rationale**: change_impact_analyzer が SpecSection 単位で diff を取れるよう、style に応じて非該当フィールドは空 list とする（None ではなく）。`raw_text` は情報損失なく保持
- **Reviewable by**: 05-requirements.md LIB-FR-05 の Markdown 見出し分割 / EARS shall_clauses / Gherkin scenarios / raw_text 保持の受入テスト
- **Traces from**: US-L-05 / bc-verification-engine.md §6 SpecSection 定義
- **Traces to**: section_assembler.py / models.py SpecSection

---

## 決定 #6-6（Step 6: LIB-FR-06 — embedded_diagrams 抽出）

- **What**: US-L-06 を LIB-FR-06 として「Mermaid/PlantUML/ASCII Art の 3 種類を embedded_diagrams フィールドに格納」と定義
- **Determinism**: D（Mermaid, PlantUML）+ H（ASCII Art ヒューリスティック判定）
- **Rationale**: Mermaid/PlantUML は fence 文字列で決定論的に検出可能。ASCII Art は罫線文字密度のヒューリスティックを使うが、誤判定があっても raw_content は完全保持されるため下流での再判定が可能
- **Reviewable by**: 05-requirements.md LIB-FR-06 の Mermaid / PlantUML / extract_diagrams=False の受入テスト
- **Traces from**: US-L-06 / Step 3 02-diagram-spec.md
- **Traces to**: diagram_extractor.py

---

## 決定 #6-7（Step 6: LIB-FR-07 — Gherkin/EARS 完全抽出）

- **What**: US-L-07 を LIB-FR-07 として「Gherkin Scenario / EARS shall_clauses の完全抽出」と定義
- **Determinism**: D
- **Rationale**: lark-parser のカスタム EBNF 文法で Gherkin AST を完全に構築、EARS は 5 パターン正規表現で完全分類。論理層検証（US-23）の入力として spec の前提・結論・制約の完全な集合を提供する
- **Reviewable by**: 05-requirements.md LIB-FR-07 の Given-When-Then / Scenario Outline + Examples / EARS 5 パターン / 複数 Scenario の受入テスト
- **Traces from**: US-L-07 / variants-catalog.md §1.1 §1.5 §2.1
- **Traces to**: parsers/gherkin_parser.py / parsers/ears_classifier.py

---

## 決定 #7-1（Step 7: モジュール分割）

- **What**: 13 モジュール構成（executor / format_detector / style_detector / 4 parser / section_assembler / 3 extractor / models / errors）を採用
- **Options considered**: A) 単一ファイルに全機能を集約 / B) 機能ごとに分離（採用案）/ C) parser を 1 ファイルに統合
- **Decision**: B) 機能ごとに分離
- **Rationale**:
  - **Single Responsibility**: 各モジュールが 1 FR に対応（モジュール ↔ FR 対応表で 1:1 検証可能）
  - **テスト容易性**: 各モジュールが独立してテスト可能（1 モジュール 1 test ファイル）
  - **style ごとの拡張性**: 新 style 追加時に parsers/ 配下に新ファイルを追加するだけ（OCP）
  - **executor が薄い**: オーケストレーションのみで、各モジュールを単純に呼び出す構成
- **Determinism**: D（構造的判断）
- **Reviewable by**: 06-architecture.md のモジュール ↔ FR 対応表で全 FR が少なくとも 1 モジュールに対応
- **Traces from**: 05-requirements.md LIB-FR-01〜07
- **Traces to**: 07-spec.md API signature / Step 9 scaffold（pyproject.toml + src layout）

---

## 決定 #8-1（Step 8: execute() を SpecParserExecutor クラスのメソッドにする）

- **What**: 公開 API を関数 (`execute(...)`) ではなくクラス (`SpecParserExecutor.execute(...)`) として提供
- **Options considered**: A) module-level 関数 `execute()` / B) class instance method `SpecParserExecutor.execute()`
- **Decision**: B) class instance method
- **Rationale**: bc-verification-engine.md §6 ParserExecutorPort は interface（Protocol）として定義されており、実装側は class で提供するのが Hexagonal Architecture / Port-Adapter パターンの慣例。テスト時の mock 注入 / 将来の状態保持（caching 等）にも対応しやすい
- **Determinism**: D
- **Reviewable by**: 07-spec.md API signature が `class SpecParserExecutor: def execute(self, ...)` 形式であること
- **Traces from**: bc-verification-engine.md §6 ParserExecutorPort interface
- **Traces to**: executor.py の実装

---

## 決定 #8-2（Step 8: ParseError 単一例外型の採用）

- **What**: parse 失敗を表現する例外型として `ParseError` の単一クラスを採用（細分化しない）
- **Options considered**: A) 単一 ParseError / B) 階層化（DecodeError / FormatError / SyntaxError 等を ParseError のサブクラスに）
- **Decision**: A) 単一 ParseError
- **Rationale**: 下流 lib（SD-02 Application Service）にとっては「parse 成功 / 失敗」の 2 値で十分。エラー詳細は `str(exception)` のメッセージで伝達。階層化は早期最適化（YAGNI）
- **Determinism**: D
- **Reviewable by**: 07-spec.md errors.py に ParseError のみ定義されている / 06-architecture.md エラー処理表で全エラー条件が ParseError または ValueError に集約
- **Traces from**: 06-architecture.md エラー処理表
- **Traces to**: errors.py

---

## 決定 #8-3（Step 8: SpecContent dataclass を frozen に）

- **What**: SpecContent / SpecSection / SpecId / TraceTag / DiagramRef / Scenario を全て `@dataclass(frozen=True)` で定義
- **Options considered**: A) mutable dataclass / B) frozen dataclass
- **Decision**: B) frozen
- **Rationale**: NormalizedArtifact は SD-02 → SD-01 間の内部契約型で、複数 Strategy が並列に参照する可能性がある。frozen にすることで accidental mutation を防ぎ、参照透過性を保証
- **Determinism**: D
- **Reviewable by**: 07-spec.md 型定義で全 dataclass が `frozen=True`
- **Traces from**: bc-verification-engine.md §6 内部契約型の immutability 慣例
- **Traces to**: models.py

---

## 決定 #8-4（Step 8: artifactId の生成方法）

- **What**: `artifactId` は path から決定論的に生成する（例: hash(path)）
- **Options considered**: A) path をそのまま使用 / B) hash(path) で短縮 / C) caller から渡してもらう
- **Decision**: A) または B) を実装段階で決定（path-based、決定論的であれば可）
- **Rationale**: bc-verification-engine.md §6 ArtifactRef.path が VCS 上のファイルパスとして定義されているため、path から決定論的に artifactId を生成すれば同じ PR に対する繰り返し parse で同じ ID が得られる（冪等性）。caller から渡す方式 (C) は parser の独立性を損なう
- **Determinism**: D
- **Reviewable by**: 07-spec.md pseudocode で artifact_id = make_artifact_id(path) が明示されている / 同一 path で execute() を 2 回呼び出して artifact_id が一致するテスト
- **Traces from**: bc-verification-engine.md §6 ArtifactRef.path
- **Traces to**: executor.py の make_artifact_id 関数

---

## 決定 #8-5（Step 8: style="auto" の解決順序）

- **What**: `config.params.spec_style == "auto"` のときの style 解決順序を「Gherkin → EARS → Connextra → Plain」の順序で最初にマッチしたものを採用
- **Options considered**: A) 全 parser を試して「最も多くのセクションを抽出できたもの」を選ぶ / B) 固定順序で最初のマッチを採用 / C) ユーザに常に明示指定を要求（auto 廃止）
- **Decision**: B) 固定順序（Gherkin → EARS → Connextra → Plain）
- **Rationale**:
  - A) は非決定論性が混入するリスク（タイブレーク条件次第で挙動が変わる）
  - C) は ParserConfig のデフォルト値 `spec_style="auto"` と矛盾
  - B) は決定論的で実装/レビューが容易。Gherkin が最も構造的特徴が強い（Feature/Scenario/Given/When/Then の語彙）ため誤検出率が低く、最初に判定するのが合理的
- **Determinism**: D
- **Reviewable by**: 07-spec.md pseudocode で順序が明示 / style_detector.py のテストで順序検証
- **Traces from**: 05-requirements.md LIB-FR-03 / 決定 #6-3
- **Traces to**: style_detector.py

---

## 決定 #16-1（Post-review: spec_id_prefixes を config から受け取るよう変更）

- **What**: `spec_id_extractor.extract_spec_ids()` の ID プレフィックスを設定ファイルから変更可能にする
- **Options considered**: A) デフォルト 9 種固定のまま維持 / B) config.params.spec_id_prefixes で上書き可能にする
- **Decision**: B) configurable — `params.spec_id_prefixes: list[str] | None`（None = デフォルト 9 種）
- **Rationale**: US-XX / FR-NNN 等はこのプロジェクト固有の ID 形式であり、他プロジェクト（例: MISRA-ID, SRS-NNN 等）では異なるプレフィックスを使う。pip ライブラリとして汎用性を確保するため configurable にする。
- **Determinism**: D（正規表現を prefixes リストから決定論的に生成）
- **Reviewable by**: tests/unit/test_spec_id_extractor.py の test_custom_prefixes_* 3 件で検証可能
- **Traces from**: ユーザーフィードバック「specidのルールは決め打ちできないよね？」（2026-05-18）
- **Traces to**: executor.py params.get("spec_id_prefixes"), spec_id_extractor.extract_spec_ids(prefixes=...)

---

<!-- 各工程で判断が生じるたびに ## 決定 #N-M エントリを追記する -->
<!-- N = 工程番号（0-15）、M = その工程内の連番 -->
