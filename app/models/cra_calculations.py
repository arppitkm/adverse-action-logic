"""
Pydantic request/response models for Application Score Fail Reasons.
"""

from typing import Any, Optional

from pydantic import BaseModel


class AppScoreFailReasonsRequest(BaseModel):
    """
    Request model for application score fail reasons.

    Contains all model_risk_weight_* and model_fail_reason_* fields.
    Extra fields are allowed to support flexible payloads.
    """

    # Weight fields
    model_risk_weight_months_in_ds_program: Optional[Any] = None
    model_risk_weight_num_failed_drafts_ever: Optional[Any] = None
    model_risk_weight_payment_increase_percent: Optional[Any] = None
    model_risk_weight_debt_cc_percent: Optional[Any] = None
    model_risk_weight_mortgage_delinquent_ever_vs_never: Optional[Any] = None
    model_risk_weight_prior_bankruptcy: Optional[Any] = None
    model_risk_weight_num_currently_dq_auto_or_mortgage: Optional[Any] = None
    model_risk_weight_clarity_non_auto_home_inquiries_6mo: Optional[Any] = None
    model_risk_weight_trades_opened_24_months: Optional[Any] = None
    model_risk_weight_max_pil_inq_or_trade_opened_90_days: Optional[Any] = None
    model_risk_weight_max_pil_inq_or_trade_opened_730_days: Optional[Any] = None
    model_risk_weight_loan_to_income_ratio: Optional[Any] = None
    model_risk_weight_bank_days_negative_balance_per_month: Optional[Any] = None
    max_model_risk_weight_liquidity_stress_path_bankruptcy: Optional[Any] = None
    model_risk_weight_opted_in_electronic_income_verification: Optional[Any] = None

    # Fail reason fields
    model_fail_reason_months_in_ds_program: Optional[str] = None
    model_fail_reason_num_failed_drafts_ever: Optional[str] = None
    model_fail_reason_payment_increase_percent: Optional[str] = None
    model_fail_reason_debt_cc_percent: Optional[str] = None
    model_fail_reason_mortgage_delinquent_ever_vs_never: Optional[str] = None
    model_fail_reason_prior_bankruptcy: Optional[str] = None
    model_fail_reason_num_currently_dq_auto_or_mortgage: Optional[str] = None
    model_fail_reason_clarity_non_auto_home_inquiries_6mo: Optional[str] = None
    model_fail_reason_trades_opened_24_months: Optional[str] = None
    model_fail_reason_max_pil_inq_or_trade_opened_90_days: Optional[str] = None
    model_fail_reason_max_pil_inq_or_trade_opened_730_days: Optional[str] = None
    model_fail_reason_loan_to_income_ratio: Optional[str] = None
    model_fail_reason_bank_days_negative_balance_per_month: Optional[str] = None
    model_fail_reason_liquidity_stress_from_app_questions: Optional[str] = None
    model_fail_reason_opted_in_electronic_income_verification: Optional[str] = None

    model_config = {"extra": "allow"}


class AppScoreFailReasonsResponse(BaseModel):
    """Response model for application score fail reasons."""

    fail_reason_app_score1: Optional[str] = None
    fail_reason_app_score2: Optional[str] = None
    fail_reason_app_score3: Optional[str] = None
    fail_reason_app_score4: Optional[str] = None
