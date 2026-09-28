"""
Pydantic request/response models for CRA Source Population.
"""

from typing import Any, Optional

from pydantic import BaseModel, Field


class CRASourceRequest(BaseModel):
    """
    Request model for CRA source population.

    Each field is a boolean flag (or a string that can be coerced to boolean)
    indicating whether the corresponding CRA contributed data.
    """

    aan_equifax_contributed: Optional[Any] = Field(
        default=None,
        description="Equifax contributed flag (bool, string, or int)",
    )
    aan_equifax_contributed2: Optional[Any] = Field(
        default=None,
        description="Equifax contributed flag (alternative key)",
    )
    aan_experian_contributed: Optional[Any] = Field(
        default=None,
        description="Experian contributed flag",
    )
    aan_tu_contributed: Optional[Any] = Field(
        default=None,
        description="TransUnion contributed flag",
    )
    aan_clarity_contributed: Optional[Any] = Field(
        default=None,
        description="Clarity contributed flag",
    )
    aan_plaid_contributed: Optional[Any] = Field(
        default=None,
        description="Plaid contributed flag",
    )

    model_config = {"extra": "allow"}


class CRASourceResponse(BaseModel):
    """Response model for CRA source population."""

    aan_cra_source_1: Optional[str] = None
    aan_cra_source_2: Optional[str] = None
    aan_cra_source_3: Optional[str] = None
    aan_cra_source_4: Optional[str] = None
    aan_cra_source_5_: Optional[str] = Field(
        default=None,
        description="Fifth CRA source (trailing underscore preserved from legacy)",
    )
