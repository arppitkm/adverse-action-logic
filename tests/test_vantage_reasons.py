"""
Unit tests for app.core.vantage_reasons module.
"""

import pytest

from app.core.vantage_reasons import (
    VANTAGE_REASON_MAP,
    _parse_vantage_code,
    get_vantage_reasons,
)


# ---------------------------------------------------------------------------
# _parse_vantage_code
# ---------------------------------------------------------------------------

class TestParseVantageCode:
    @pytest.mark.parametrize(
        "code, expected",
        [
            (90, 90),
            (4, 4),
            ("90", 90),
            ("00090", 90),
            ("00012", 12),
            ("  88  ", 88),
            (None, None),
            ("", None),
            ("   ", None),
            ("abc", None),
            (88.0, 88),
        ],
    )
    def test_various_inputs(self, code, expected):
        assert _parse_vantage_code(code) == expected


# ---------------------------------------------------------------------------
# get_vantage_reasons
# ---------------------------------------------------------------------------

class TestGetVantageReasons:
    def test_basic_lookup(self):
        result = get_vantage_reasons([88, 95])
        assert result["vantage_score_code_1"] == 88
        assert result["vantage_score_description_1"] == "Bankruptcy"
        assert result["vantage_score_code_2"] == 95
        assert result["vantage_score_description_2"] == "No negative reason code"

    def test_leading_zeros(self):
        result = get_vantage_reasons(["00090", "00004"])
        assert result["vantage_score_code_1"] == 90
        assert result["vantage_score_description_1"] == (
            "No open revolving accounts in your credit file"
        )
        assert result["vantage_score_code_2"] == 4
        assert result["vantage_score_description_2"] == (
            "Balances on accts too high compared to credit limits and loan amounts"
        )

    def test_unknown_code(self):
        result = get_vantage_reasons([999])
        assert result["vantage_score_code_1"] == 999
        assert result["vantage_score_description_1"] == "Unknown Code: 999"

    def test_invalid_code_produces_none(self):
        result = get_vantage_reasons(["abc"])
        assert result["vantage_score_code_1"] is None
        assert result["vantage_score_description_1"] is None

    def test_max_five_items(self):
        codes = [88, 95, 29, 4, 97, 85, 86]  # 7 items
        result = get_vantage_reasons(codes)
        # Should only have 5 pairs (10 keys)
        assert "vantage_score_code_5" in result
        assert "vantage_score_code_6" not in result

    def test_empty_list(self):
        result = get_vantage_reasons([])
        assert result == {}

    def test_preserves_input_order(self):
        result = get_vantage_reasons([97, 4, 88])
        assert result["vantage_score_code_1"] == 97
        assert result["vantage_score_code_2"] == 4
        assert result["vantage_score_code_3"] == 88

    def test_all_codes_in_map_are_valid(self):
        """Verify every code in VANTAGE_REASON_MAP resolves correctly."""
        for code, desc in VANTAGE_REASON_MAP.items():
            result = get_vantage_reasons([code])
            assert result["vantage_score_code_1"] == code
            assert result["vantage_score_description_1"] == desc
