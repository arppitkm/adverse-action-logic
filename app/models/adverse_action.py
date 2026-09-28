"""
Pydantic request/response models for the unified Adverse Action endpoint.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from app.models.cra_calculations import (
    AppScoreFailReasonsRequest,
    AppScoreFailReasonsResponse,
)
from app.models.cra_source import CRASourceRequest, CRASourceResponse
from app.models.vantage import VantageReasonsRequest, VantageReasonsResponse


class AdverseActionRequest(BaseModel):
    """
    Unified request for all adverse action calculations.

    All three sub-inputs are optional. Missing sections produce
    empty/null outputs rather than errors.
    """

    aan_source_input: Optional[CRASourceRequest] = Field(
        default=None,
        description="CRA source contribution flags",
    )
    cra_calc_input: Optional[AppScoreFailReasonsRequest] = Field(
        default=None,
        description="Risk model weights and fail reason fields",
    )
    vantage_reasons_input: Optional[VantageReasonsRequest] = Field(
        default=None,
        description="Vantage score reason codes to resolve",
    )


class AdverseActionResponse(BaseModel):
    """
    Unified response from all adverse action calculations.
    """

    adverse_action_request_input: Dict[str, Any] = Field(
        description="Echo of the full request payload",
    )
    aan_cra_sources: CRASourceResponse
    cra_fail_reasons: AppScoreFailReasonsResponse
    vantage_reasons: Dict[str, Any] = Field(
        default_factory=dict,
        description="Vantage reason code/description pairs",
    )
