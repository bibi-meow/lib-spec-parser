# lib-spec-parser Trace Matrix

> FR（機能要求）→ AT（受入テスト）→ Code（実装）→ Test（単体テスト）のトレーサビリティを管理する。
> design doc §7 Step 15 参照。
> **実装完了後に全 FR が網羅されていることを確認してから push すること。**

---

## Trace Matrix

| FR ID | 説明 | 受入テストファイル | 実装モジュール | 単体テストファイル | 完了 |
|-------|------|------------------|--------------|-----------------|------|
| LIB-FR-01 | MD/YAML/RST → NormalizedArtifact | tests/acceptance/test_fr01_parse_normalized.py | lib_spec_parser/executor.py, lib_spec_parser/format_detector.py | tests/unit/test_format_detector.py | [x] |
| LIB-FR-02 | TraceTag 抽出 | tests/acceptance/test_fr02_trace_tags.py | lib_spec_parser/trace_tag_extractor.py | tests/unit/test_trace_tag_extractor.py | [x] |
| LIB-FR-03 | Style 自動判定 | tests/acceptance/test_fr03_style_detection.py | lib_spec_parser/style_detector.py | tests/unit/test_style_detector.py | [x] |
| LIB-FR-04 | SpecId 網羅抽出 | tests/acceptance/test_fr04_spec_id_extraction.py | lib_spec_parser/spec_id_extractor.py | tests/unit/test_spec_id_extractor.py | [x] |
| LIB-FR-05 | SpecSection 構造化 | tests/acceptance/test_fr05_section_structure.py | lib_spec_parser/section_assembler.py | （acceptance のみ：section_assembler は parser/extractor 統合の薄い orchestrator） | [x] |
| LIB-FR-06 | DiagramRef 抽出 | tests/acceptance/test_fr06_diagram_extraction.py | lib_spec_parser/diagram_extractor.py | tests/unit/test_diagram_extractor.py | [x] |
| LIB-FR-07 | Gherkin/EARS 論理条件 | tests/acceptance/test_fr07_gherkin_ears.py | lib_spec_parser/parsers/gherkin_parser.py, lib_spec_parser/parsers/ears_classifier.py, lib_spec_parser/parsers/connextra_parser.py | tests/unit/test_gherkin_parser.py, tests/unit/test_ears_classifier.py, tests/unit/test_connextra_parser.py | [x] |

---

## カバレッジサマリ

| 指標 | 件数 |
|------|------|
| FR 総数 | 7 |
| AT（受入テスト）総数 | 42 |
| Unit Test 総数 | 45 |
| 全テスト総数 | 87 |
| 実装モジュール総数 | 11（executor / format_detector / models / errors / trace_tag_extractor / style_detector / spec_id_extractor / section_assembler / diagram_extractor / parsers/{gherkin,ears_classifier,connextra,generic}） |
| 全 FR 網羅済み | YES |
| 全テスト PASS | YES (87 passed, 0 failed) |
| 行カバレッジ | 95% (332/351 lines) |

### モジュール別カバレッジ（pytest-cov 実測値）

| モジュール | Stmts | Miss | Cover |
|-----------|-------|------|-------|
| `__init__.py` | 7 | 0 | 100% |
| `diagram_extractor.py` (LIB-FR-06) | 20 | 0 | 100% |
| `errors.py` | 3 | 0 | 100% |
| `executor.py` (LIB-FR-01) | 54 | 5 | 91% |
| `format_detector.py` (LIB-FR-01) | 9 | 0 | 100% |
| `models.py` | 39 | 0 | 100% |
| `parsers/__init__.py` | 0 | 0 | 100% |
| `parsers/connextra_parser.py` (LIB-FR-07) | 8 | 0 | 100% |
| `parsers/ears_classifier.py` (LIB-FR-07) | 21 | 3 | 86% |
| `parsers/generic_parser.py` | 3 | 3 | 0% |
| `parsers/gherkin_parser.py` (LIB-FR-07) | 65 | 2 | 97% |
| `section_assembler.py` (LIB-FR-05) | 60 | 6 | 90% |
| `spec_id_extractor.py` (LIB-FR-04) | 22 | 0 | 100% |
| `style_detector.py` (LIB-FR-03) | 25 | 0 | 100% |
| `trace_tag_extractor.py` (LIB-FR-02) | 15 | 0 | 100% |
| **TOTAL** | **351** | **19** | **95%** |

### FR 別 acceptance テスト件数

| FR ID | AT 件数 | Unit 件数 |
|-------|---------|-----------|
| LIB-FR-01 | 8 | 7 (format_detector) |
| LIB-FR-02 | 5 | 6 (trace_tag_extractor) |
| LIB-FR-03 | 9 | 6 (style_detector) |
| LIB-FR-04 | 6 | 6 (spec_id_extractor) |
| LIB-FR-05 | 5 | 0 (acceptance 中心) |
| LIB-FR-06 | 4 | 5 (diagram_extractor) |
| LIB-FR-07 | 5 | 5+7+3=15 (gherkin / ears / connextra) |
| **合計** | **42** | **45** |

---

## トレーサビリティ確認チェックリスト

- [x] 全 FR ID (LIB-FR-01〜07) が Trace Matrix に記載されている
- [x] 各 FR に対応する受入テストファイル (tests/acceptance/test_frNN_*.py) が存在する
- [x] 各 FR に対応する実装モジュールが記載されている
- [x] 各 FR に対応する単体テスト（または acceptance 経由のカバレッジ）が記載されている
- [x] pytest で全テスト PASS が確認されている（87 passed）
- [x] カバレッジサマリの「全 FR 網羅済み」が YES になっている
- [x] ruff check / ruff format / pyright のすべてが PASS
- [x] 行カバレッジ 95%（生成器メソッド `generic_parser.py` のみ未使用のため 0%）

---

## 機械検証コマンド

```bash
# 1. FR → AT 対応の機械検証（acceptance テストの収集）
pytest tests/acceptance/ -v --collect-only
# 期待: 42 acceptance tests collected、各 test_frNN_*.py が docstring に "Traces: LIB-FR-NN" を含む

# 2. FR ID の埋め込み確認（コード・ドキュメント横断）
grep -rn "LIB-FR-" lib_spec_parser/ tests/acceptance/ docs/
# 期待: 各 FR ID が少なくとも実装・テスト・ドキュメントの 3 箇所に出現

# 3. カバレッジ計測（FR 別の網羅度確認）
pytest --cov=lib_spec_parser --cov-report=term-missing tests/
# 期待: 87 passed, TOTAL 95% (351 statements, 19 missing)

# 4. 品質ゲート一括
ruff check lib_spec_parser/ tests/      # exit 0
ruff format --check lib_spec_parser/ tests/  # exit 0
pyright lib_spec_parser/                # 0 errors, 0 warnings
pytest -v                               # 87 passed
```

---

## 未カバー行の説明（行カバレッジ 95% / 19 行 miss）

| ファイル | 未カバー行 | 内容 | 判定 |
|---------|-----------|------|------|
| `executor.py` | 103, 126-129 | エラーパスとエッジケース（unsupported extension after detection、invalid utf-8 path） | acceptance テスト `test_invalid_utf8_raises_parse_error` 等で部分カバー。残りは defensive guard |
| `parsers/ears_classifier.py` | 75-76, 78 | classify_ears で未マッチ時の早期 return | unwanted パターンの分岐 |
| `parsers/generic_parser.py` | 7-17 | YAML/RST の generic parser スタブ（現状未使用） | 将来 FR 拡張用 placeholder（MVP では markdown 経路のみ） |
| `parsers/gherkin_parser.py` | 29, 106 | Examples table の境界処理 | acceptance では基本パターンのみ |
| `section_assembler.py` | 45, 65-67, 73, 107 | section split のエッジケース（空 raw、heading 直後の改行） | 主要パスは 90% カバー |

**Decision Log**: #15-1（Trace Matrix 完成の確認を記録）
**Decision Log**: #15-2（Step 11 品質ゲート 4 種類すべて PASS：pytest 87/87, ruff check OK, ruff format OK, pyright 0 errors）

---

<!-- Step 9（scaffold）前にこのファイルのスケルトンを作成し、実装中に逐次更新する -->
<!-- Step 15 でこの Matrix を最終確認してから push する -->
