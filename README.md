# lib-spec-parser

様々なフォーマット（Markdown / YAML / RST）の仕様書ファイルを、ツールが扱いやすい共通フォーマット（`NormalizedArtifact`）に変換する Python ライブラリです。

## インストール

```bash
pip install "git+https://github.com/bibi-meow/lib-spec-parser.git"
```

## 使い方

```python
from lib_spec_parser import execute

with open("my-spec.md", "rb") as f:
    raw = f.read()

artifact = execute(
    config={
        "enabled": True,
        "artifact_type": "spec",
        "params": {
            "trace_format": "Traces:",              # トレースタグのプレフィックス
            "spec_id_prefixes": ["REQ", "US"],      # 抽出する ID プレフィックス
            "spec_style": "auto",                   # auto | gherkin | ears | connextra | plain
        },
    },
    raw_content=raw,
    path="my-spec.md",
)

# セクション単位で構造化された結果
for section in artifact["content"]["sections"]:
    print(section["section_id"], section["style"])

# トレースタグ（例: "Traces: REQ-001"）
for tag in artifact["content"]["trace_tags"]:
    print(tag["referenced_ids"])

# 認識した ID 一覧（例: "REQ-001", "US-02"）
for spec_id in artifact["content"]["spec_ids"]:
    print(spec_id["value"])
```

## 設定オプション

| パラメータ | デフォルト | 説明 |
|---|---|---|
| `trace_format` | `"Traces:"` | トレースタグのプレフィックス文字列 |
| `spec_id_prefixes` | `["US","FR","REQ","NFR","AR","EA","PR","PE","AD"]` | ID として抽出するプレフィックス一覧（プロジェクトに合わせて変更可） |
| `spec_style` | `"auto"` | セクションのスタイル固定。`"auto"` の場合は内容から自動判定 |
| `extract_ids` | `true` | ID 抽出の有効 / 無効 |
| `extract_diagrams` | `true` | Mermaid / PlantUML ブロック抽出の有効 / 無効 |

## 出力フォーマット

```json
{
  "artifactId": "spec:path/to/spec.md:abc123",
  "artifactType": "spec",
  "content": {
    "spec_ids": [
      {"value": "REQ-001", "id_type": "REQ", "line_number": 3}
    ],
    "sections": [
      {
        "section_id": "REQ-001",
        "style": "ears",
        "raw_text": "...",
        "keywords": [],
        "shall_clauses": ["The system shall ..."],
        "scenarios": []
      }
    ],
    "trace_tags": [
      {"raw_line": "Traces: REQ-001", "referenced_ids": ["REQ-001"], "line_number": 5}
    ],
    "embedded_diagrams": [
      {"diagram_type": "mermaid", "raw_content": "graph TD ...", "start_line": 10, "end_line": 14}
    ]
  }
}
```

## 開発

```bash
git clone https://github.com/bibi-meow/lib-spec-parser.git
cd lib-spec-parser
pip install -e ".[dev]"
pytest
```

## 品質ゲート

```bash
pytest                    # 87 tests
ruff check .              # no errors
ruff format --check .     # no changes
pyright lib_spec_parser/  # 0 errors
```

## ライセンス

MIT
