"""
Integration tests for POST /v1/cra-sources endpoint.
"""


class TestCraSourcesEndpoint:
    def test_all_sources_contributed(self, client, cra_source_payload_all_true):
        resp = client.post("/v1/cra-sources", json=cra_source_payload_all_true)
        assert resp.status_code == 200
        data = resp.json()
        assert data["aan_cra_source_1"] == "Equifax"
        assert data["aan_cra_source_2"] == "Experian"
        assert data["aan_cra_source_3"] == "TransUnion"
        assert data["aan_cra_source_4"] == "Clarity"
        assert data["aan_cra_source_5_"] == "Plaid"

    def test_partial_sources(self, client, cra_source_payload_partial):
        resp = client.post("/v1/cra-sources", json=cra_source_payload_partial)
        assert resp.status_code == 200
        data = resp.json()
        assert data["aan_cra_source_1"] == "Equifax"
        assert data["aan_cra_source_2"] == "TransUnion"
        assert data["aan_cra_source_3"] is None

    def test_empty_body(self, client):
        resp = client.post("/v1/cra-sources", json={})
        assert resp.status_code == 200
        data = resp.json()
        assert data["aan_cra_source_1"] is None

    def test_string_flags(self, client):
        resp = client.post("/v1/cra-sources", json={
            "aan_equifax_contributed": "true",
            "aan_plaid_contributed": "on",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["aan_cra_source_1"] == "Equifax"
        assert data["aan_cra_source_2"] == "Plaid"
