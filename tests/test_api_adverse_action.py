"""
Integration tests for POST /v1/adverse-action (unified endpoint).
"""


class TestAdverseActionEndpoint:
    def test_full_payload(self, client, full_adverse_action_payload):
        resp = client.post("/v1/adverse-action", json=full_adverse_action_payload)
        assert resp.status_code == 200
        data = resp.json()

        # Verify all three sections are present
        assert "adverse_action_request_input" in data
        assert "aan_cra_sources" in data
        assert "cra_fail_reasons" in data
        assert "vantage_reasons" in data

        # CRA Sources
        assert data["aan_cra_sources"]["aan_cra_source_1"] == "Equifax"
        assert data["aan_cra_sources"]["aan_cra_source_5_"] == "Plaid"

        # Fail Reasons
        assert data["cra_fail_reasons"]["fail_reason_app_score1"] is not None

        # Vantage
        assert data["vantage_reasons"]["vantage_score_code_1"] == 88

    def test_missing_all_sections(self, client):
        resp = client.post("/v1/adverse-action", json={})
        assert resp.status_code == 200
        data = resp.json()

        # All sections should be present with null/empty values
        assert data["aan_cra_sources"]["aan_cra_source_1"] is None
        assert data["cra_fail_reasons"]["fail_reason_app_score1"] is None
        assert data["vantage_reasons"] == {}

    def test_only_cra_sources(self, client):
        resp = client.post("/v1/adverse-action", json={
            "aan_source_input": {"aan_equifax_contributed": True}
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["aan_cra_sources"]["aan_cra_source_1"] == "Equifax"
        assert data["cra_fail_reasons"]["fail_reason_app_score1"] is None
        assert data["vantage_reasons"] == {}

    def test_only_vantage(self, client):
        resp = client.post("/v1/adverse-action", json={
            "vantage_reasons_input": {"input_data": [88]}
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["aan_cra_sources"]["aan_cra_source_1"] is None
        assert data["vantage_reasons"]["vantage_score_code_1"] == 88

    def test_request_echo(self, client):
        payload = {
            "aan_source_input": {"aan_equifax_contributed": True}
        }
        resp = client.post("/v1/adverse-action", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        # The request should be echoed back
        assert "adverse_action_request_input" in data
        echoed = data["adverse_action_request_input"]
        assert echoed["aan_source_input"]["aan_equifax_contributed"] is True


class TestHealthEndpoint:
    def test_health(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "version" in data
