"""
Application configuration via Pydantic BaseSettings.

Loads values from .env file with secure defaults.
Rule 15: API keys injected via environment, never hardcoded.

Supports TWO authentication modes:
1. API Key mode (Google AI Studio) — set GEMINI_API_KEY
2. Vertex AI mode (Google Cloud $300 credits) — set USE_VERTEX_AI=true + GOOGLE_CLOUD_PROJECT
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Central configuration for OmniClaims Adjuster."""

    # --- Authentication Mode ---
    use_vertex_ai: bool = Field(
        default=False,
        description="If true, use Vertex AI with Google Cloud credentials instead of API key",
    )

    # --- Google AI Studio (API Key mode) ---
    gemini_api_key: str = Field(
        default="",
        description="Google Gemini API key from AI Studio (used when use_vertex_ai=false)",
    )

    # --- Vertex AI (Google Cloud credits mode) ---
    google_cloud_project: str = Field(
        default="",
        description="Google Cloud project ID (used when use_vertex_ai=true)",
    )
    google_cloud_location: str = Field(
        default="global",
        description="Google Cloud region for Vertex AI (global required for 3.x models)",
    )

    # --- Model Configuration ---
    gemini_pro_model: str = Field(
        default="gemini-3.1-pro-preview",
        description="Gemini 3.1 Pro — latest reasoning model (Vertex AI global)",
    )
    gemini_flash_model: str = Field(
        default="gemini-3-flash-preview",
        description="Gemini 3 Flash — fast UI interactions (Vertex AI global)",
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
