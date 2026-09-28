"""
Pydantic request/response models for Vantage Score Reason Codes.
"""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class VantageReasonsRequest(BaseModel):
    """
    Request model for Vantage score reason code lookup.

    Accepts a list of up to 5 reason codes (integers or zero-padded strings).
    """

    input_data: List[Union[int, str]] = Field(
        ...,
        description="List of Vantage score reason codes (int or string, max 5)",
        max_length=5,
    )


class VantageReasonsResponse(BaseModel):
    """
    Response model for Vantage score reason code lookup.

    Contains dynamically numbered fields (vantage_score_code_1, etc.).
    Uses a flexible dict to accommodate variable number of results.
    """

    # We use model_extra to allow the dynamic numbered keys
    model_config = {"extra": "allow"}

    vantage_score_code_1: Optional[int] = None
    vantage_score_description_1: Optional[str] = None
    vantage_score_code_2: Optional[int] = None
    vantage_score_description_2: Optional[str] = None
    vantage_score_code_3: Optional[int] = None
    vantage_score_description_3: Optional[str] = None
    vantage_score_code_4: Optional[int] = None
    vantage_score_description_4: Optional[str] = None
    vantage_score_code_5: Optional[int] = None
    vantage_score_description_5: Optional[str] = None
