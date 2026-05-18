"""Unit tests for spec_id_extractor module."""

from lib_spec_parser.spec_id_extractor import extract_spec_ids


class TestSpecIdExtractor:
    def test_extracts_us_ids(self):
        text = "US-01 requirement"
        ids = extract_spec_ids(text)
        assert "US-01" in ids

    def test_extracts_fr_ids(self):
        text = "FR-003 must be implemented"
        ids = extract_spec_ids(text)
        assert "FR-003" in ids

    def test_extracts_req_ids(self):
        text = "REQ-007: system requirement"
        ids = extract_spec_ids(text)
        assert "REQ-007" in ids

    def test_extracts_nfr_ids(self):
        text = "NFR-01 performance"
        ids = extract_spec_ids(text)
        assert "NFR-01" in ids

    def test_extracts_ar_ids(self):
        text = "AR-01 architecture"
        ids = extract_spec_ids(text)
        assert "AR-01" in ids

    def test_extracts_ad_ids(self):
        text = "AD-02 decision"
        ids = extract_spec_ids(text)
        assert "AD-02" in ids

    def test_no_partial_match(self):
        # Should not match embedded IDs in words
        text = "USER-01 is not valid"
        ids = extract_spec_ids(text)
        assert "USER-01" not in ids

    def test_multiple_ids(self):
        text = "US-01 and FR-002 and REQ-003"
        ids = extract_spec_ids(text)
        assert len(ids) == 3

    def test_custom_prefixes(self):
        text = "CUSTOM-01 is a requirement"
        ids = extract_spec_ids(text, prefixes=["CUSTOM"])
        assert "CUSTOM-01" in ids

    def test_empty_text(self):
        assert extract_spec_ids("") == []
