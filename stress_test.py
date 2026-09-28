"""
Locust stress test for MRS_30 Adverse Action Logic microservice.

Run:
    1. Start the API server:   uvicorn app.main:app --port 8000
    2. Start Locust:           locust -f stress_test.py --host=http://localhost:8000
    3. Open dashboard:         http://localhost:8089
       Set users, spawn rate, and click Start.

Or run headless (no browser):
    locust -f stress_test.py --host=http://localhost:8000 \
        --users 100 --spawn-rate 10 --run-time 60s --headless
"""

from locust import HttpUser, between, task


# ---------------------------------------------------------------------------
# Sample payloads
# ---------------------------------------------------------------------------

CRA_SOURCE_PAYLOAD = {
    "aan_equifax_contributed": True,
    "aan_experian_contributed": True,
    "aan_tu_contributed": False,
    "aan_clarity_contributed": "Yes",
    "aan_plaid_contributed": 1,
}

APP_SCORE_PAYLOAD = {
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

VANTAGE_PAYLOAD = {
    "input_data": [88, "00095", 29, "00004", 97],
}

FULL_ADVERSE_ACTION_PAYLOAD = {
    "aan_source_input": CRA_SOURCE_PAYLOAD,
    "cra_calc_input": APP_SCORE_PAYLOAD,
    "vantage_reasons_input": VANTAGE_PAYLOAD,
}


# ---------------------------------------------------------------------------
# Locust user
# ---------------------------------------------------------------------------

class AdverseActionUser(HttpUser):
    """
    Simulates a client calling the MRS_30 microservice.

    Traffic distribution roughly reflects expected real-world usage:
    - Unified endpoint gets the most traffic (50%)
    - Individual endpoints split the rest
    - Health check is occasional
    """

    # Wait 0.5–2 seconds between tasks (simulates real spacing)
    wait_time = between(0.5, 2)

    @task(5)
    def unified_adverse_action(self):
        """POST /v1/adverse-action — the primary endpoint."""
        self.client.post("/v1/adverse-action", json=FULL_ADVERSE_ACTION_PAYLOAD)

    @task(2)
    def cra_sources(self):
        """POST /v1/cra-sources"""
        self.client.post("/v1/cra-sources", json=CRA_SOURCE_PAYLOAD)

    @task(2)
    def app_score_fail_reasons(self):
        """POST /v1/app-score-fail-reasons"""
        self.client.post("/v1/app-score-fail-reasons", json=APP_SCORE_PAYLOAD)

    @task(2)
    def vantage_reasons(self):
        """POST /v1/vantage-reasons"""
        self.client.post("/v1/vantage-reasons", json=VANTAGE_PAYLOAD)

    @task(1)
    def health_check(self):
        """GET /health"""
        self.client.get("/health")
