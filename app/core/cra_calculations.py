"""
Application Score Fail Reasons Logic.

Computes up to four adverse-action reasons for applications that failed the
application-stage risk score, by ranking risk model variable weights.

Extracted from the LendAPI MRS_30 module (cra_calculations.py).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class RiskVarSpec:
    weight_field: str
    fail_reason_field: str


# --------------------------------------------------------------------------------------
# Embedded table of risk model variables.
#
# Columns:
#   weight_field        – payload key holding the numeric coefficient
#   fail_reason_field   – payload key holding the human-readable fail reason
#
# Row order matters: it determines tie-breaking when two variables share the
# same weight (earlier row wins).
# --------------------------------------------------------------------------------------

RISK_VAR_SPECS: List[RiskVarSpec] = [
    RiskVarSpec(
        weight_field="model_risk_weight_months_in_ds_program",
        fail_reason_field="model_fail_reason_months_in_ds_program",
    ),
    RiskVarSpec(
        weight_field="model_risk_weight_num_failed_drafts_ever",
        fail_reason_field="model_fail_reason_num_failed_drafts_ever",
    ),
    RiskVarSpec(
        weight_field="model_risk_weight_payment_increase_percent",
        fail_reason_field="model_fail_reason_payment_increase_percent",
    ),
    RiskVarSpec(
        weight_field="model_risk_weight_debt_cc_percent",
        fail_reason_field="model_fail_reason_debt_cc_percent",
    ),
    RiskVarSpec(
        weight_field="model_risk_weight_mortgage_delinquent_ever_vs_never",
        fail_reason_field="model_fail_reason_mortgage_delinquent_ever_vs_never",
    ),
    RiskVarSpec(
        weight_field="model_risk_weight_prior_bankruptcy",
        fail_reason_field="model_fail_reason_prior_bankruptcy",
    ),
    RiskVarSpec(
        weight_field="model_risk_weight_num_currently_dq_auto_or_mortgage",
        fail_reason_field="model_fail_reason_num_currently_dq_auto_or_mortgage",
    ),
    RiskVarSpec(
        weight_field="model_risk_weight_clarity_non_auto_home_inquiries_6mo",
        fail_reason_field="model_fail_reason_clarity_non_auto_home_inquiries_6mo",
    ),
    RiskVarSpec(
        weight_field="model_risk_weight_trades_opened_24_months",
        fail_reason_field="model_fail_reason_trades_opened_24_months",
    ),
    RiskVarSpec(
        weight_field="model_risk_weight_max_pil_inq_or_trade_opened_90_days",
        fail_reason_field="model_fail_reason_max_pil_inq_or_trade_opened_90_days",
    ),
    RiskVarSpec(
        weight_field="model_risk_weight_max_pil_inq_or_trade_opened_730_days",
        fail_reason_field="model_fail_reason_max_pil_inq_or_trade_opened_730_days",
    ),
    RiskVarSpec(
        weight_field="model_risk_weight_loan_to_income_ratio",
        fail_reason_field="model_fail_reason_loan_to_income_ratio",
    ),
    RiskVarSpec(
        weight_field="model_risk_weight_bank_days_negative_balance_per_month",
        fail_reason_field="model_fail_reason_bank_days_negative_balance_per_month",
    ),
    RiskVarSpec(
        weight_field="max_model_risk_weight_liquidity_stress_path_bankruptcy",
        fail_reason_field="model_fail_reason_liquidity_stress_from_app_questions",
    ),
    RiskVarSpec(
        weight_field="model_risk_weight_opted_in_electronic_income_verification",
        fail_reason_field="model_fail_reason_opted_in_electronic_income_verification",
    ),
]


def _to_float(value: Any) -> Optional[float]:
    """Best-effort conversion to float; returns None if conversion fails."""
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def build_app_score_fail_reasons(
    application_payload: Dict[str, Any],
    *,
    max_reasons: int = 4,
) -> Dict[str, Optional[str]]:
    """
    Compute up to four adverse action reasons for applications that failed
    the application stage risk score.

    Inputs:
      - application_payload: dict containing weight fields and fail reason
        fields listed in RISK_VAR_SPECS

    Outputs:
      - dict with fail_reason_app_score1..fail_reason_app_score4

    Ranking:
      - include only rows with a strictly positive coefficient (weight > 0)
      - zero is neutral; negative coefficients are favorable — both skipped
      - sort descending by weight (largest positive first)
      - ties break by the order in RISK_VAR_SPECS (first listed wins)
    """
    # Gather positive coefficients only; preserve table order for tie-breaking.
    eligible: List[Tuple[float, int, Optional[str]]] = []
    for idx, spec in enumerate(RISK_VAR_SPECS):
        weight = _to_float(application_payload.get(spec.weight_field))
        if weight is None or weight <= 0:
            continue  # missing, non-numeric, zero (neutral), or negative; skip

        reason = application_payload.get(spec.fail_reason_field)
        eligible.append((weight, idx, reason))

    # Sort by weight descending; idx ensures stable tie-break
    eligible.sort(key=lambda t: (-t[0], t[1]))

    # Take up to max_reasons reasons
    reasons = [t[2] for t in eligible[:max_reasons]]

    # Write to fixed output fields; pad with None if fewer than 4
    out: Dict[str, Optional[str]] = {}
    for i in range(4):
        out[f"fail_reason_app_score{i + 1}"] = (
            reasons[i] if i < len(reasons) else None
        )

    return out
