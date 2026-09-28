"""
FastAPI application factory.

Creates and configures the FastAPI app with CORS middleware,
exception handlers, health check, and API routes.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.config import get_settings


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "MRS_30 — Adverse Action Logic microservice. "
            "Provides CRA source population, application score fail reasons, "
            "and Vantage score reason code lookups for the Lend API system."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ----- CORS -----
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ----- Global exception handler -----
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(exc) if settings.debug else None,
            },
        )

    # ----- Health check -----
    @app.get(
        "/health",
        tags=["Health"],
        summary="Health Check",
    )
    def health_check():
        return {
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.app_version,
        }

    # ----- Mount API routes -----
    app.include_router(api_router)

    return app


# Module-level app instance (used by uvicorn and Mangum)
app = create_app()
