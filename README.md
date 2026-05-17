# lib-spec-parser

spec ファイル（Markdown/YAML/RST）を構造化された `NormalizedArtifact` へ正規化する Python pip パッケージ。

spec-reviewer パイプラインの Parser lib として、PR に含まれる spec ファイルを解析し、Verification Engine が直接参照できる形式に変換します。

## 機能

- **BDD/Gherkin** 解析（Given-When-Then、Scenario Outline + Examples）
- **EARS** 分類（5 パターン: Ubiquitous/Event-driven/State-driven/Optional/Unwanted）
- **Connextra User Story** 解析（As a / I want / So that）
- **SpecId 抽出**（US-XX, FR-NNN, REQ-NNN 等）
- **TraceTag 抽出**（`Traces:` タグ）
- **埋め込み図抽出**（Mermaid/PlantUML ブロック）

## インストール

```bash
pip install "git+https://github.com/bibi-meow/lib-spec-parser.git"
```

## 使い方

```python
from lib_spec_parser import execute

result = execute(
    config={},  # ParserConfig dict
    raw_content=b"## US-01\n\nTraces: FR-001\n",
    path="spec.md",
)

print(result["content"]["spec_ids"])    # [{"value": "US-01", "id_type": "US"}]
print(result["content"]["trace_tags"])  # [{"referenced_ids": ["FR-001"], ...}]
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
pytest               # 87 tests green
ruff check .         # no errors
ruff format --check .  # no changes
pyright lib_spec_parser/  # 0 errors
```

## ライセンス

MIT
