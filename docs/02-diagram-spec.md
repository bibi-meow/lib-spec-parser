# lib-spec-parser Diagram Spec

> 本 lib が生成・参照する diagram の仕様。必ず正規ドキュメントを Read して引用すること。
> **学習データ推定禁止**: LLM の記憶から推定するのではなく正規仕様を Read して根拠を残す。
> design doc §7 Step 3 参照。

---

## 本 lib の diagram 取扱い方針

**本 lib は diagram を「生成」しない。spec ファイルに埋め込まれた図ブロックを「抽出」する Parser である。**

- 入力: spec ファイル（Markdown / YAML / RST）の raw_content
- 出力: 図ブロックへの参照（`SpecContent.embedded_diagrams: List[DiagramRef]`）
- 抽出した DiagramRef は下流の `architecture_verifier` が論理アーキ比較（US-31/US-33）で参照する

---

## 本 lib が扱う diagram

| diagram 種別 | 用途 | 正規仕様ドキュメント |
|------------|------|------------------|
| Mermaid ブロック | spec 内の論理アーキテクチャ図（flowchart / sequenceDiagram / classDiagram 等） | `cicd/doc/sys/business-process/bc-verification-engine.md` §6 SpecContent.embedded_diagrams |
| PlantUML ブロック | spec 内の構造図 / 振る舞い図（`@startuml..@enduml` で囲まれたもの） | 同上 |
| ASCII Art ブロック | spec 内の簡易図（コードブロック内の罫線/矢印で構成されたテキスト） | 同上 |

> 注: SpecContent.embedded_diagrams は `architecture_verifier`（lib-spec-parser.md 依存 lib 欄）が論理アーキ比較で参照する内部フィールドである。本 lib は抽出責務のみを持ち、図の意味解釈は行わない。

---

## ノード型（DiagramRef のフィールド定義）

**本 lib は「図ブロックへの参照」を抽出するため、ノード型は単一の `DiagramRef` のみ**。図ブロック内の個別ノード（Mermaid の flowchart 要素など）はパースしない（責務外）。

| ノード型 ID | 名称 | 属性 | 正規仕様引用（章節 + 抜粋） |
|-----------|------|------|--------------------------|
| NT-01 | `DiagramRef` | `diagram_type`, `raw_content`, `start_line`, `end_line` | bc-verification-engine.md §6 "embedded_diagrams : List[DiagramRef] ← spec 内埋め込み図（arch 比較用）" + §6 "ArchitectureStrategy（SD-01）が実行時に SpecContent.embedded_diagrams（論理アーキ）と CodeContent.call_graph（物理アーキ）から導出する" |

### NT-01 `DiagramRef` フィールド定義

| フィールド名 | 型 | 説明 | 抽出ソース |
|------------|-----|------|----------|
| `diagram_type` | `str` | `"mermaid"` / `"plantuml"` / `"ascii_art"` のいずれか | コードブロック言語タグ または `@startuml` マーカー |
| `raw_content` | `str` | 図ブロックの原文テキスト（情報損失なく保持） | ブロック内テキスト |
| `start_line` | `int` | spec ファイル内の開始行番号（1-based） | コードブロック開始 fence の次行 |
| `end_line` | `int` | spec ファイル内の終了行番号（1-based） | コードブロック終了 fence の前行 |

---

## エッジ型

**該当なし**。本 lib は図ブロックを「抽出」するのみで、図内部の構造（ノード間エッジ）は解釈しない。図内部のセマンティクスは `architecture_verifier` lib の責務。

| エッジ型 ID | 名称 | 方向 | ラベル | 正規仕様引用 |
|-----------|------|------|-------|------------|
| — | （該当なし） | — | — | — |

---

## スキーマ定義

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class DiagramRef:
    """spec ファイルに埋め込まれた図ブロックへの参照。
    
    本 lib は図ブロックの「抽出」のみを行う。図の意味解釈
    （ノード抽出 / エッジ解析）は architecture_verifier lib の責務。
    """
    diagram_type: str    # "mermaid" | "plantuml" | "ascii_art"
    raw_content: str     # 図ブロックの原文（情報損失なし）
    start_line: int      # 1-based 開始行
    end_line: int        # 1-based 終了行
```

---

## 正規ドキュメント引用根拠

| ドキュメント名 | URL / パス | 参照章節 | 引用目的 |
|-------------|----------|---------|---------|
| Verification Engine BC Tactical | `cicd/doc/sys/business-process/bc-verification-engine.md` | §6 NormalizedArtifact — SD-02 → SD-01 間の内部契約型 | SpecContent.embedded_diagrams が List[DiagramRef] として定義されている根拠 |
| Verification Engine BC Tactical | 同上 | §6 アーキモデル（論理 / 物理）の導出 | "ArchitectureStrategy（SD-01）が実行時に SpecContent.embedded_diagrams（論理アーキ）と CodeContent.call_graph（物理アーキ）から導出する。NormalizedArtifact に ArchContent variant は存在しない。" — 本 lib は抽出のみ、解釈は SD-01 Strategy の責務であることを示す |
| lib-spec-parser SOT | `cicd/doc/sys/lib/.../lib-spec-parser.md` | 概要 + 依存 lib | 「埋め込み図（embedded_diagrams）の 4 種を抽出し」「architecture_verifier — 論理アーキ比較（US-31/US-33。embedded_diagrams を使用）」 |

**Decision Log**: #3-1（引用根拠の判断を記録）

---

<!-- Step 4 Diagram Generation 時にズレが発見されたら本ファイルを更新する（フィードバックループ）-->
<!-- 更新時は Decision Log #4-N にズレ内容と修正を記録する -->
