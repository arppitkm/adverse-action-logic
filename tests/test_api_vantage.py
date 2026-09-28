"""
Integration tests for POST /v1/vantage-reasons endpoint.
"""


class TestVantageEndpoint:
    def test_basic_lookup(self, client, vantage_payload):
        resp = client.post("/v1/vantage-reasons", json=vantage_payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["vantage_score_code_1"] == 88
        assert data["vantage_score_description_1"] == "Bankruptcy"
        assert data["vantage_score_code_2"] == 95
        assert data["vantage_score_description_2"] == "No negative reason code"

    def test_missing_input_data(self, client):
        resp = client.post("/v1/vantage-reasons", json={})
        assert resp.status_code == 422  # Pydantic validation error

    def test_empty_list(self, client):
        resp = client.post("/v1/vantage-reasons", json={"input_data": []})
        assert resp.status_code == 200
        assert resp.json() == {}

    def test_leading_zeros(self, client):
        resp = client.post("/v1/vantage-reasons", json={
            "input_data": ["00088", "00004"]
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["vantage_score_code_1"] == 88
        assert data["vantage_score_code_2"] == 4

    def test_max_five_enforced(self, client):
        resp = client.post("/v1/vantage-reasons", json={
            "input_data": [88, 95, 29, 4, 97, 85]
        })
        # max_length=5 on the model should cause validation error
        assert resp.status_code == 422
