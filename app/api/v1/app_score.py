"""
API route: POST /v1/app-score-fail-reasons

Computes top 4 risk model fail reasons ranked by positive coefficient weight.
"""

from fastapi import APIRouter

from app.core.cra_calculations import build_app_score_fail_reasons
from app.models.cra_calculations import (
    AppScoreFailReasonsRequest,
    AppScoreFailReasonsResponse,
)

router = APIRouter()


@router.post(
    "/app-score-fail-reasons",
    response_model=AppScoreFailReasonsResponse,
    summary="Compute App Score Fail Reasons",
    description=(
        "Computes up to 4 adverse action reasons for applications that failed "
        "the application-stage risk score. Ranks risk model variable weights "
        "descending (positive coefficients only)."
    ),
)
def app_score_fail_reasons(
    request: AppScoreFailReasonsRequest,
) -> AppScoreFailReasonsResponse:
    result = build_app_score_fail_reasons(request.model_dump())
    return AppScoreFailReasonsResponse(**result)
