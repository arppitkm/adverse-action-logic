"""
Unit tests for app.core.cra_source module.
"""

import json

import pytest

from app.core.cra_source import (
    _coerce_payload,
    _is_true,
    populate_aan_cra_sources,
)


# ---------------------------------------------------------------------------
# _is_true
# ---------------------------------------------------------------------------

class TestIsTrue:
    @pytest.mark.parametrize(
        "value, expected",
        [
            (True, True),
            (False, False),
            (1, True),
            (0, False),
            (-1, True),
            (1.0, True),
            (0.0, False),
            ("1", True),
            ("y", True),
            ("yes", True),
            ("YES", True),
            ("true", True),
            ("True", True),
            ("t", True),
            ("on", True),
            ("0", False),
            ("no", False),
            ("false", False),
            ("", False),
            ("  ", False),
            (None, False),
        ],
    )
    def test_various_values(self, value, expected):
        assert _is_true(value) is expected


# ---------------------------------------------------------------------------
# _coerce_payload
# ---------------------------------------------------------------------------

class TestCoercePayload:
    def test_none(self):
        assert _coerce_payload(None) == {}

    def test_empty_dict(self):
        assert _coerce_payload({}) == {}

    def test_plain_dict(self):
        d = {"key": "value"}
        assert _coerce_payload(d) == d

    def test_lambda_body_json_string(self):
        payload = {"body": json.dumps({"aan_equifax_contributed": True})}
        result = _coerce_payload(payload)
        assert result == {"aan_equifax_contributed": True}

    def test_lambda_body_invalid_json(self):
        payload = {"body": "not json"}
        assert _coerce_payload(payload) == {}

    def test_json_string(self):
        result = _coerce_payload('{"key": "val"}')
        assert result == {"key": "val"}

    def test_invalid_json_string(self):
        assert _coerce_payload("not json") == {}

    def test_empty_string(self):
        assert _coerce_payload("") == {}


# ---------------------------------------------------------------------------
# populate_aan_cra_sources
# ---------------------------------------------------------------------------

class TestPopulateAanCraSources:
    def test_all_true(self):
        result = populate_aan_cra_sources({
            "aan_equifax_contributed": True,
            "aan_experian_contributed": True,
            "aan_tu_contributed": True,
            "aan_clarity_contributed": True,
            "aan_plaid_contributed": True,
        })
        assert result["aan_cra_source_1"] == "Equifax"
        assert result["aan_cra_source_2"] == "Experian"
        assert result["aan_cra_source_3"] == "TransUnion"
        assert result["aan_cra_source_4"] == "Clarity"
        assert result["aan_cra_source_5_"] == "Plaid"

    def test_none_true(self):
        result = populate_aan_cra_sources({
            "aan_equifax_contributed": False,
            "aan_experian_contributed": False,
            "aan_tu_contributed": False,
        })
        assert result["aan_cra_source_1"] is None
        assert result["aan_cra_source_2"] is None

    def test_partial(self):
        result = populate_aan_cra_sources({
            "aan_equifax_contributed": False,
            "aan_experian_contributed": True,
            "aan_tu_contributed": True,
        })
        assert result["aan_cra_source_1"] == "Experian"
        assert result["aan_cra_source_2"] == "TransUnion"
        assert result["aan_cra_source_3"] is None

    def test_equifax_alt_key(self):
        """aan_equifax_contributed2 should also activate Equifax."""
        result = populate_aan_cra_sources({
            "aan_equifax_contributed2": "Yes",
        })
        assert result["aan_cra_source_1"] == "Equifax"

    def test_kwargs_interface(self):
        result = populate_aan_cra_sources(
            aan_equifax_contributed=True,
            aan_plaid_contributed="1",
        )
        assert result["aan_cra_source_1"] == "Equifax"
        assert result["aan_cra_source_2"] == "Plaid"
        assert result["aan_cra_source_3"] is None

    def test_json_string_input(self):
        payload = json.dumps({"aan_clarity_contributed": True})
        result = populate_aan_cra_sources(payload)
        assert result["aan_cra_source_1"] == "Clarity"

    def test_always_returns_five_keys(self):
        result = populate_aan_cra_sources({})
        assert len(result) == 5
