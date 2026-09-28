"""
Shared test fixtures and sample payloads.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    """FastAPI test client."""
    return TestClient(app)


# ---------------------------------------------------------------------------
# Sample payloads
# ---------------------------------------------------------------------------

@pytest.fixture()
def cra_source_payload_all_true():
    """All CRA sources contributed."""
    return {
        "aan_equifax_contributed": True,
        "aan_experian_contributed": True,
        "aan_tu_contributed": True,
        "aan_clarity_contributed": True,
        "aan_plaid_contributed": True,
    }


@pytest.fixture()
def cra_source_payload_partial():
    """Only Equifax and TransUnion contributed."""
    return {
        "aan_equifax_contributed": True,
        "aan_experian_contributed": False,
        "aan_tu_contributed": "Yes",
        "aan_clarity_contributed": 0,
        "aan_plaid_contributed": None,
    }


@pytest.fixture()
def app_score_payload():
    """Sample risk model weights and fail reasons."""
    return {
        "model_risk_weight_months_in_ds_program": 0.5,
        "model_fail_reason_months_in_ds_program": "Months in DS program too short",
        "model_risk_weight_num_failed_drafts_ever": 1.2,
        "model_fail_reason_num_failed_drafts_ever": "Too many failed drafts",
        "model_risk_weight_payment_increase_percent": -0.3,
        "model_fail_reason_payment_increase_percent": "Payment increase too high",
        "model_risk_weight_debt_cc_percent": 0.8,
        "model_fail_reason_debt_cc_percent": "Credit card debt too high",
        "model_risk_weight_prior_bankruptcy": 0.0,
        "model_fail_reason_prior_bankruptcy": "Prior bankruptcy on record",
        "model_risk_weight_loan_to_income_ratio": 0.9,
        "model_fail_reason_loan_to_income_ratio": "Loan-to-income ratio too high",
        "model_risk_weight_trades_opened_24_months": 0.5,
        "model_fail_reason_trades_opened_24_months": "Too many trades opened in 24 months",
    }


@pytest.fixture()
def vantage_payload():
    """Sample Vantage score reason codes."""
    return {"input_data": [88, "00095", 29, "00004", 97]}


@pytest.fixture()
def full_adverse_action_payload(
    cra_source_payload_all_true, app_score_payload, vantage_payload
):
    """Full payload for the unified adverse action endpoint."""
    return {
        "aan_source_input": cra_source_payload_all_true,
        "cra_calc_input": app_score_payload,
        "vantage_reasons_input": vantage_payload,
    }
