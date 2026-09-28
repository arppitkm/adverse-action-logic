"""
API route: POST /v1/vantage-reasons

Maps Vantage score reason codes to human-readable descriptions.
"""

from fastapi import APIRouter

from app.core.vantage_reasons import get_vantage_reasons
from app.models.vantage import VantageReasonsRequest

router = APIRouter()


@router.post(
    "/vantage-reasons",
    summary="Resolve Vantage Reason Codes",
    description=(
        "Maps up to 5 Vantage score reason codes (integers or zero-padded "
        "strings) to their human-readable descriptions. Preserves input order."
    ),
)
def vantage_reasons(request: VantageReasonsRequest) -> dict:
    return get_vantage_reasons(request.input_data)
