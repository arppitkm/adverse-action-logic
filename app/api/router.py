"""
Top-level API router.

Aggregates all versioned sub-routers into a single router
that is mounted by the FastAPI application.
"""

from fastapi import APIRouter

from app.api.v1 import adverse_action, app_score, cra_sources, vantage

api_router = APIRouter()

# Mount all v1 routes under /v1 prefix
api_router.include_router(
    cra_sources.router,
    prefix="/v1",
    tags=["CRA Sources"],
)
api_router.include_router(
    app_score.router,
    prefix="/v1",
    tags=["App Score Fail Reasons"],
)
api_router.include_router(
    vantage.router,
    prefix="/v1",
    tags=["Vantage Reasons"],
)
api_router.include_router(
    adverse_action.router,
    prefix="/v1",
    tags=["Adverse Action (Unified)"],
)
