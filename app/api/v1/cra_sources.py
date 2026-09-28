"""
API route: POST /v1/cra-sources

Populates prioritized CRA sources from contribution flags.
"""

from fastapi import APIRouter

from app.core.cra_source import populate_aan_cra_sources
from app.models.cra_source import CRASourceRequest, CRASourceResponse

router = APIRouter()


@router.post(
    "/cra-sources",
    response_model=CRASourceResponse,
    summary="Populate CRA Sources",
    description=(
        "Generates a prioritized list of up to 5 contributing Credit Reporting "
        "Agency sources based on boolean flags in the request payload."
    ),
)
def cra_sources(request: CRASourceRequest) -> CRASourceResponse:
    result = populate_aan_cra_sources(request.model_dump())
    return CRASourceResponse(**result)
