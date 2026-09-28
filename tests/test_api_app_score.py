"""
Integration tests for POST /v1/app-score-fail-reasons endpoint.
"""


class TestAppScoreEndpoint:
    def test_ranked_fail_reasons(self, client, app_score_payload):
        resp = client.post("/v1/app-score-fail-reasons", json=app_score_payload)
        assert resp.status_code == 200
        data = resp.json()

        # Expected ranking: 1.2, 0.9, 0.8, 0.5 (two at 0.5 — tie-break by table order)
        assert data["fail_reason_app_score1"] == "Too many failed drafts"
        assert data["fail_reason_app_score2"] == "Loan-to-income ratio too high"
        assert data["fail_reason_app_score3"] == "Credit card debt too high"
        # 0.5 for months_in_ds_program (idx 0) beats 0.5 for trades_opened_24_months (idx 8)
        assert data["fail_reason_app_score4"] == "Months in DS program too short"

    def test_empty_payload(self, client):
        resp = client.post("/v1/app-score-fail-reasons", json={})
        assert resp.status_code == 200
        data = resp.json()
        assert data["fail_reason_app_score1"] is None

    def test_only_negative_weights(self, client):
        resp = client.post("/v1/app-score-fail-reasons", json={
            "model_risk_weight_months_in_ds_program": -0.5,
            "model_fail_reason_months_in_ds_program": "should not appear",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["fail_reason_app_score1"] is None
