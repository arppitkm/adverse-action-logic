"""
Application settings loaded from environment variables.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration via environment variables."""

    app_name: str = "Adverse Action Logic (MRS_30)"
    app_version: str = "1.0.0"
    debug: bool = False
    allowed_origins: list[str] = ["*"]

    model_config = {"env_prefix": "MRS30_"}


def get_settings() -> Settings:
    """Factory for dependency injection."""
    return Settings()
