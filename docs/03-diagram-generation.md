# lib-spec-parser Diagram Extraction 手法

> input data から diagram を「抽出」するアルゴリズム・実装方針を定義する。
> design doc §7 Step 4 参照。

---

## 本 lib における Step 4 の位置付け

**本 lib は diagram を「生成」しない。テンプレート名は "Diagram Generation" だが、本 lib では "Diagram Extraction"（埋め込み図ブロックの抽出）として読み替える。**

理由: lib-spec-parser.md の役割は「spec の中に何が書かれているか」を取り出すこと（概要欄）。図の生成（input data → 新規 diagram）は他 lib（diagram-parser / scdl-builder 等）の責務であり、本 lib の責務外。

---

## 抽出対象

| diagram 種別 | 抽出元 input | 抽出手法（概要） |
|------------|------------|--------------|
| Mermaid ブロック | spec ファイル（.md / .yaml / .rst） | Markdown コードブロック言語タグ ` ```mermaid ` を正規表現で検出 |
| PlantUML ブロック | spec ファイル（.md / .yaml / .rst） | `@startuml` / `@enduml` マーカー、または ` ```plantuml ` コードブロックを正規表現で検出 |
| ASCII Art ブロック | spec ファイル（.md / .yaml / .rst） | プレーンコードブロック内のテキストにヒューリスティック（罫線/矢印文字密度）を適用 |

**適用条件**: `config.params.extract_diagrams == True` の場合のみ実行（デフォルト True）。False の場合は `SpecContent.embedded_diagrams = []` を返す。

---

## アルゴリズム定義

### Mermaid ブロック抽出アルゴリズム

**決定論性**: D

```
1. input: spec ファイル全文 text: str
2. 正規表現: r'^```mermaid\s*\n(.*?)\n```$' (multiline, dotall)
3. 各マッチに対し:
   a. raw_content := マッチした内側のテキスト
   b. start_line := マッチ開始位置を行番号に変換（fence 直後の行）
   c. end_line := マッチ終了位置を行番号に変換（fence 直前の行）
   d. DiagramRef(diagram_type="mermaid", raw_content=..., start_line=..., end_line=...) を生成
4. 出力: List[DiagramRef] (mermaid のみ)
```

### PlantUML ブロック抽出アルゴリズム

**決定論性**: D

```
1. input: spec ファイル全文 text: str
2. 2 種類のマッチを並列に実施:
   - パターン A: r'@startuml\s*\n(.*?)\n@enduml' (multiline, dotall)
   - パターン B: r'^```plantuml\s*\n(.*?)\n```$' (multiline, dotall)
3. 各マッチに対し DiagramRef(diagram_type="plantuml", ...) を生成
4. 重複検出: パターン A と B が同一範囲をマッチした場合は A を優先（@startuml が公式 marker）
5. 出力: List[DiagramRef] (plantuml のみ)
```

### ASCII Art ブロック抽出アルゴリズム

**決定論性**: H（ヒューリスティック）

```
1. input: spec ファイル全文 text: str
2. プレーンコードブロック（``` で囲まれ、言語タグ無し、または "text" / "ascii"）を全て抽出
3. 各ブロックに対しヒューリスティック判定:
   a. ブロック内テキストに罫線文字（─│┌┐└┘├┤┬┴┼ ─ ━ ║ ═ + - | ▶ ▷ → →）の出現率を計算
   b. 出現率が閾値（例: ≥ 5% / 行）以上、かつ行数 ≥ 3 行 / 幅 ≥ 10 文字なら ASCII Art と判定
4. 判定対象に対し DiagramRef(diagram_type="ascii_art", ...) を生成
5. 出力: List[DiagramRef] (ascii_art のみ)
```

**注**: ASCII Art 判定はヒューリスティックのため誤判定の可能性がある（決定論性 H）。下流 lib（architecture_verifier）がこの DiagramRef を読んだ際に意味解釈に失敗しても、本 lib の責務範囲では「抽出した raw_content」までは完全に保持する。

---

## 統合フロー

```
1. config.params.extract_diagrams が False なら return []
2. mermaid_refs := extract_mermaid(text)
3. plantuml_refs := extract_plantuml(text)
4. ascii_refs := extract_ascii_art(text)
5. all_refs := mermaid_refs + plantuml_refs + ascii_refs
6. start_line でソート（spec ファイル内の出現順）
7. return all_refs
```

---

## Step 3 Diagram Spec との差異（Step 4 発見分）

Step 4 の実装方針検討中に 02-diagram-spec.md との差異が見つかった場合はここに記録し、
`02-diagram-spec.md` を即更新する。

| 発見日 | 差異内容 | 02-diagram-spec.md 更新内容 | Decision Log |
|-------|---------|--------------------------|-------------|
| —     | （現時点で差異なし） | —                         | —           |

**Decision Log**: #4-1（抽出アルゴリズム選択の判断を記録）
