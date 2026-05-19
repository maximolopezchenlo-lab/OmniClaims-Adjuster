"""
Application configuration via Pydantic BaseSettings.

Loads values from .env file with secure defaults.
Rule 15: API keys injected via environment, never hardcoded.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Central configuration for OmniClaims Adjuster."""

    # --- Gemini API ---
    gemini_api_key: str = Field(
        ...,
        description="Google Gemini API key from AI Studio",
    )
    gemini_pro_model: str = Field(
        default="gemini-3.1-pro-preview",
        description="Gemini 3.1 Pro model for complex reasoning (confirmed in API)",
    )
    gemini_flash_model: str = Field(
        default="gemini-3-flash-preview",
        description="Gemini 3 Flash model for fast UI interactions (confirmed in API)",
    )

    # --- Server ---
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=7860)
    debug: bool = Field(default=False)

    # --- Logging ---
    log_level: str = Field(default="INFO")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


# Singleton instance
settings = Settings()
