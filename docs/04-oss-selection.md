# lib-spec-parser OSS 選定

> System Architecture に組み込む OSS を評価マトリクスで選定する。
> design doc §7 Step 5 参照。

---

## 選定対象

| 機能 | 必要理由 |
|------|---------|
| Markdown parsing | spec ファイル `.md` から見出し構造 / コードブロックを抽出する必要 |
| Gherkin parsing | §1.1 BDD/Gherkin / §1.4 ATDD / §1.5 Scenario Outline の Given-When-Then 構文を AST に変換する必要 |
| YAML parsing | spec ファイル `.yaml` から構造化 spec を読み込む必要 |
| RST parsing | spec ファイル `.rst` のセクション / Directive を抽出する必要 |
| Regex-based 共通処理 | EARS 5 パターン分類 / Connextra 3 フィールド分解 / SpecId 抽出 / Traces タグ抽出 |

---

## 選定基準

| 基準 | 重み | 説明 |
|------|------|------|
| 機能性 | 0.4 | 仕様文書のスタイル網羅性 / AST 構造の有用性 / カバレッジ |
| 性能 | 0.3 | 1 MB ファイルでの parse 速度（NFR 2 秒以内） |
| 保守性 | 0.2 | 最終更新 / star 数 / コミュニティ |
| ライセンス | 0.1 | BSD / MIT / Apache 互換 |

評価値は 1（不適合）〜 5（最適）の 5 段階。

---

## 評価マトリクス: Markdown parsing

参照: `cicd/doc/sys/verification/catalogs/variants-catalog.md`（OSS 実装一覧）

| 候補 | 機能性 (0.4) | 性能 (0.3) | 保守性 (0.2) | ライセンス (0.1) | 合計スコア |
|------|:-----------:|:--------:|:-----------:|:-------------:|:---------:|
| **mistletoe** | 4 | 4 | 4 | 5 (MIT) | 4.1 |
| markdown-it-py | 4 | 4 | 5 | 5 (MIT) | 4.3 |
| marko | 4 | 3 | 3 | 5 (MIT) | 3.6 |
| 正規表現 (`re` 標準) | 3 | 5 | 5 (Python 標準) | 5 (PSF) | 4.0 |

### 決定

**採用**: `mistletoe`
**採用バージョン**: `^1.3.0`
**理由**:
- AST ベースで Markdown を木構造として扱える（コードブロック・見出しの抽出が容易）
- 純 Python 実装で他依存ゼロ（軽量）
- MIT ライセンス
- markdown-it-py との比較で機能性は同等、mistletoe の方がコード base が小さく依存問題が少ない（spec-reviewer の core 依存として有利）

**補助**: SpecId / Traces タグ / EARS / Connextra の抽出は **Python 標準 `re`** モジュールで決定論的に処理する（追加 OSS 不要）。

**Decision Log**: #5-1

---

## 評価マトリクス: Gherkin parsing

参照: `variants-catalog.md` §2.3 §1.1/§1.4/§1.5 の OSS 実装欄

| 候補 | 機能性 (0.4) | 性能 (0.3) | 保守性 (0.2) | ライセンス (0.1) | 合計スコア |
|------|:-----------:|:--------:|:-----------:|:-------------:|:---------:|
| **lark-parser** (カスタム文法) | 5 | 4 | 4 | 5 (MIT) | 4.5 |
| behave (Feature parser として lib 利用) | 3 | 3 | 4 | 5 (BSD-2-Clause) | 3.4 |
| pytest-bdd (parser 部分のみ抽出) | 3 | 3 | 4 | 5 (MIT) | 3.4 |
| 正規表現 (`re` 標準) | 2 | 5 | 5 | 5 (PSF) | 3.3 |

### 決定

**採用**: `lark-parser`
**採用バージョン**: `^1.1.0`
**理由**:
- Gherkin 6 文法（Feature / Scenario / Scenario Outline / Examples / Background / 多言語キーワード）を EBNF で定義可能、AST 構築が決定論的
- behave / pytest-bdd は CLI / test runner 統合に最適化されており、lib として「ファイルを AST に変換するだけ」の用途では過剰依存
- 正規表現単独では Scenario Outline + Examples の表構造をパースするのが困難（保守性低）
- MIT ライセンス、Python 3.11 対応、コミュニティ活発（PyPI 月間 DL > 5M）

**Decision Log**: #5-1

---

## 評価マトリクス: YAML parsing

| 候補 | 機能性 (0.4) | 性能 (0.3) | 保守性 (0.2) | ライセンス (0.1) | 合計スコア |
|------|:-----------:|:--------:|:-----------:|:-------------:|:---------:|
| **PyYAML** | 5 | 4 | 5 | 5 (MIT) | 4.7 |
| ruamel.yaml | 5 | 3 | 4 | 5 (MIT) | 4.2 |
| oyaml | 3 | 3 | 2 | 5 (MIT) | 2.8 |

### 決定

**採用**: `PyYAML`
**採用バージョン**: `^6.0`
**理由**:
- YAML 1.2 仕様準拠、Python エコシステムでデファクト
- C 実装（libyaml バインディング）で性能良好
- ruamel.yaml は round-trip 編集機能が強みだが、本 lib は read-only 用途のため不要

**Decision Log**: #5-1

---

## 評価マトリクス: RST parsing

| 候補 | 機能性 (0.4) | 性能 (0.3) | 保守性 (0.2) | ライセンス (0.1) | 合計スコア |
|------|:-----------:|:--------:|:-----------:|:-------------:|:---------:|
| **docutils** | 5 | 3 | 5 | 5 (BSD-2-Clause / Public Domain) | 4.3 |
| sphinx (parser 部分) | 5 | 3 | 5 | 5 (BSD-2-Clause) | 4.3 |
| 正規表現 (`re` 標準) | 2 | 5 | 5 | 5 (PSF) | 3.3 |

### 決定

**採用**: `docutils`
**採用バージョン**: `^0.21.0`
**理由**:
- RST 公式 reference 実装
- AST（doctree）として RST 文書全体を扱える
- sphinx は docutils の拡張であり、RST core parsing のみ必要な本 lib では docutils 単体で十分

**Decision Log**: #5-1

---

## 推奨構成サマリ

| 機能 | 採用 OSS | バージョン | ライセンス |
|------|---------|-----------|----------|
| Markdown parsing | mistletoe | ^1.3.0 | MIT |
| Gherkin parsing | lark-parser | ^1.1.0 | MIT |
| YAML parsing | PyYAML | ^6.0 | MIT |
| RST parsing | docutils | ^0.21.0 | BSD-2-Clause / Public Domain |
| EARS / Connextra / SpecId / Traces 抽出 | Python 標準 `re` | 3.11 同梱 | PSF |
| 状態機械（Gherkin 階層追跡） | Python 標準（自作 FSM） | 3.11 同梱 | PSF |

ライセンス互換性: 全て MIT/BSD/PSF 系で商用利用・再配布可。Apache 2.0 と互換。

**Decision Log**: #5-1（OSS 選定全体の判断を記録）

---
