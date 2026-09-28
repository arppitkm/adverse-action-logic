"""
Unit tests for app.core.cra_calculations module.
"""

import pytest

from app.core.cra_calculations import _to_float, build_app_score_fail_reasons


# ---------------------------------------------------------------------------
# _to_float
# ---------------------------------------------------------------------------

class TestToFloat:
    @pytest.mark.parametrize(
        "value, expected",
        [
            (1.5, 1.5),
            (0, 0.0),
            ("3.14", 3.14),
            ("-1.0", -1.0),
            ("0", 0.0),
            (None, None),
            ("abc", None),
            ("", None),
        ],
    )
    def test_various_values(self, value, expected):
        assert _to_float(value) == expected


# ---------------------------------------------------------------------------
# build_app_score_fail_reasons
# ---------------------------------------------------------------------------

class TestBuildAppScoreFailReasons:
    def test_basic_ranking(self):
        """Positive weights sorted descending; only top 4 returned."""
        payload = {
            "model_risk_weight_months_in_ds_program": 0.5,
            "model_fail_reason_months_in_ds_program": "reason_months",
            "model_risk_weight_num_failed_drafts_ever": 1.2,
            "model_fail_reason_num_failed_drafts_ever": "reason_drafts",
            "model_risk_weight_debt_cc_percent": 0.8,
            "model_fail_reason_debt_cc_percent": "reason_cc",
            "model_risk_weight_loan_to_income_ratio": 0.9,
            "model_fail_reason_loan_to_income_ratio": "reason_lti",
        }
        result = build_app_score_fail_reasons(payload)

        assert result["fail_reason_app_score1"] == "reason_drafts"    # 1.2
        assert result["fail_reason_app_score2"] == "reason_lti"       # 0.9
        assert result["fail_reason_app_score3"] == "reason_cc"        # 0.8
        assert result["fail_reason_app_score4"] == "reason_months"    # 0.5

    def test_negative_and_zero_weights_excluded(self):
        """Zero and negative weights should not appear in results."""
        payload = {
            "model_risk_weight_months_in_ds_program": 0.0,
            "model_fail_reason_months_in_ds_program": "should not appear",
            "model_risk_weight_payment_increase_percent": -0.5,
            "model_fail_reason_payment_increase_percent": "should not appear",
            "model_risk_weight_num_failed_drafts_ever": 1.0,
            "model_fail_reason_num_failed_drafts_ever": "only this one",
        }
        result = build_app_score_fail_reasons(payload)

        assert result["fail_reason_app_score1"] == "only this one"
        assert result["fail_reason_app_score2"] is None
        assert result["fail_reason_app_score3"] is None
        assert result["fail_reason_app_score4"] is None

    def test_tie_breaking_by_table_order(self):
        """When weights are equal, earlier entry in RISK_VAR_SPECS wins."""
        payload = {
            "model_risk_weight_months_in_ds_program": 1.0,
            "model_fail_reason_months_in_ds_program": "first_in_table",
            "model_risk_weight_num_failed_drafts_ever": 1.0,
            "model_fail_reason_num_failed_drafts_ever": "second_in_table",
        }
        result = build_app_score_fail_reasons(payload)

        assert result["fail_reason_app_score1"] == "first_in_table"
        assert result["fail_reason_app_score2"] == "second_in_table"

    def test_empty_payload(self):
        """Empty payload produces all-None results."""
        result = build_app_score_fail_reasons({})
        for i in range(1, 5):
            assert result[f"fail_reason_app_score{i}"] is None

    def test_max_four_reasons(self):
        """Even with more than 4 positive weights, only top 4 returned."""
        payload = {}
        from app.core.cra_calculations import RISK_VAR_SPECS

        # Set all 15 specs to positive weights
        for idx, spec in enumerate(RISK_VAR_SPECS):
            payload[spec.weight_field] = float(idx + 1)
            payload[spec.fail_reason_field] = f"reason_{idx}"

        result = build_app_score_fail_reasons(payload)

        # Should only have 4 keys
        assert result["fail_reason_app_score1"] is not None
        assert result["fail_reason_app_score2"] is not None
        assert result["fail_reason_app_score3"] is not None
        assert result["fail_reason_app_score4"] is not None
        assert len(result) == 4

    def test_string_weights(self):
        """String values that can be parsed to float should work."""
        payload = {
            "model_risk_weight_months_in_ds_program": "0.7",
            "model_fail_reason_months_in_ds_program": "reason_from_string",
        }
        result = build_app_score_fail_reasons(payload)
        assert result["fail_reason_app_score1"] == "reason_from_string"

    def test_non_numeric_weight_skipped(self):
        """Non-numeric weight values should be skipped (not cause errors)."""
        payload = {
            "model_risk_weight_months_in_ds_program": "not_a_number",
            "model_fail_reason_months_in_ds_program": "should not appear",
        }
        result = build_app_score_fail_reasons(payload)
        assert result["fail_reason_app_score1"] is None
