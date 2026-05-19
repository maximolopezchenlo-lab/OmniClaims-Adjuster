"""
Health check endpoint for the OmniClaims Adjuster API.

Provides system status, model availability, and configuration info
for monitoring and demo verification.
"""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> dict:
    """
    System health check.

    Returns server status, configured models, and auth mode.
    Used by judges to verify the system is live.
    """
    return {
        "status": "healthy",
        "service": "OmniClaims Adjuster",
        "version": "1.0.0-hackathon",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "configuration": {
            "auth_mode": "vertex_ai" if settings.use_vertex_ai else "api_key",
            "project_id": settings.google_cloud_project if settings.use_vertex_ai else None,
            "location": settings.google_cloud_location if settings.use_vertex_ai else None,
            "pro_model": settings.gemini_pro_model,
            "flash_model": settings.gemini_flash_model,
        },
    }


@router.get("/models")
async def list_models() -> dict:
    """List available Gemini models on the configured backend."""
    from app.core.gemini_client import list_available_models

    models = list_available_models()
    gemini_models = [m for m in models if "gemini" in m.lower()]
    return {
        "total": len(gemini_models),
        "models": gemini_models,
    }
