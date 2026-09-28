"""
CRA Source Population Logic.

Generates a prioritized list of up to 5 contributing Credit Reporting Agency
sources based on boolean flags in the application payload.

Extracted from the LendAPI MRS_30 module (aan_cra_source.py).
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Union


# CONFIGURATION: Define the Priority and Input Key mapping here.
# This separates 'data' from 'logic', making it easier to read or modify later.
CRA_MAPPING_CONFIG = [
    ("Equifax",    ["aan_equifax_contributed", "aan_equifax_contributed2"]),
    ("Experian",   ["aan_experian_contributed"]),
    ("TransUnion", ["aan_tu_contributed"]),
    ("Clarity",    ["aan_clarity_contributed"]),
    ("Plaid",      ["aan_plaid_contributed"]),
]


def _is_true(value: Any) -> bool:
    """Normalize common LOS flag formats to boolean."""
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "y", "yes", "true", "t", "on"}
    return bool(value)


def _coerce_payload(obj: Any) -> Dict[str, Any]:
    """
    Coerce LendAPI/Lambda inputs into a dict.
    """
    if not obj:
        return {}

    # If it's a dict, check for Lambda 'body' or return as is
    if isinstance(obj, dict):
        body = obj.get("body")
        if isinstance(body, str):
            try:
                return json.loads(body) or {}
            except (ValueError, TypeError):
                return {}
        return obj

    # If it's a string, try to parse as JSON
    if isinstance(obj, str):
        try:
            return json.loads(obj) or {}
        except (ValueError, TypeError):
            return {}

    return {}


def populate_aan_cra_sources(
    payload: Optional[Union[Dict, str]] = None,
    **kwargs,
) -> Dict[str, Optional[str]]:
    """
    Generates a prioritized list of contributing CRA sources.

    Logic:
      1. Coerces input (dict, json string, or kwargs).
      2. Checks flags based on CRA_MAPPING_CONFIG priority.
      3. Returns the top 5 sources (padded with None).
    """
    # Use kwargs if provided, otherwise parse payload
    data = kwargs if kwargs else _coerce_payload(payload)

    # Filter sources based on the config constant
    # Each entry can have multiple alternative input keys
    # (e.g. aan_equifax_contributed / aan_equifax_contributed2)
    active_sources: List[str] = [
        name
        for name, keys in CRA_MAPPING_CONFIG
        if any(_is_true(data.get(k)) for k in keys)
    ]

    # Pad with None to ensure we always have 5 slots
    sources = (active_sources + [None] * 5)[:5]

    return {
        "aan_cra_source_1": sources[0],
        "aan_cra_source_2": sources[1],
        "aan_cra_source_3": sources[2],
        "aan_cra_source_4": sources[3],
        "aan_cra_source_5_": sources[4],
    }
