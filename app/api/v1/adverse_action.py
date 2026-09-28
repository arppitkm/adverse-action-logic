"""
API route: POST /v1/adverse-action

Unified handler that orchestrates all three adverse action calculations
in a single request.
"""

from fastapi import APIRouter

from app.core.cra_calculations import build_app_score_fail_reasons
from app.core.cra_source import populate_aan_cra_sources
from app.core.vantage_reasons import get_vantage_reasons
from app.models.adverse_action import AdverseActionRequest, AdverseActionResponse
from app.models.cra_calculations import AppScoreFailReasonsResponse
from app.models.cra_source import CRASourceResponse

router = APIRouter()


@router.post(
    "/adverse-action",
    response_model=AdverseActionResponse,
    summary="Unified Adverse Action Calculation",
    description=(
        "Processes all three adverse action calculations in a single request: "
        "CRA source population, application score fail reasons, and Vantage "
        "score reason code lookup. Each section is independent; missing inputs "
        "produce null outputs rather than errors."
    ),
)
def adverse_action(request: AdverseActionRequest) -> AdverseActionResponse:
    # Echo the full request back
    request_echo = request.model_dump(mode="json")

    # --- CRA Sources ---
    if request.aan_source_input is not None:
        cra_result = populate_aan_cra_sources(
            request.aan_source_input.model_dump()
        )
    else:
        cra_result = {
            "aan_cra_source_1": None,
            "aan_cra_source_2": None,
            "aan_cra_source_3": None,
            "aan_cra_source_4": None,
            "aan_cra_source_5_": None,
        }

    # --- App Score Fail Reasons ---
    if request.cra_calc_input is not None:
        fail_result = build_app_score_fail_reasons(
            request.cra_calc_input.model_dump()
        )
    else:
        fail_result = {
            "fail_reason_app_score1": None,
            "fail_reason_app_score2": None,
            "fail_reason_app_score3": None,
            "fail_reason_app_score4": None,
        }

    # --- Vantage Reasons ---
    if request.vantage_reasons_input is not None:
        vantage_result = get_vantage_reasons(
            request.vantage_reasons_input.input_data
        )
    else:
        vantage_result = {}

    return AdverseActionResponse(
        adverse_action_request_input=request_echo,
        aan_cra_sources=CRASourceResponse(**cra_result),
        cra_fail_reasons=AppScoreFailReasonsResponse(**fail_result),
        vantage_reasons=vantage_result,
    )
