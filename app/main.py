"""
OmniClaims Adjuster — FastAPI Application Entry Point.

Rule 26: Optimized for demo latency.
Rule 27: Streaming enabled.
Rule 29: CORS configured for cross-origin Gradio access.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.claims import router as claims_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown events."""
    logger.info("🚀 OmniClaims Adjuster starting up...")
    logger.info(f"   Auth: {'Vertex AI' if settings.use_vertex_ai else 'API Key'}")
    logger.info(f"   Pro model:   {settings.gemini_pro_model}")
    logger.info(f"   Flash model: {settings.gemini_flash_model}")

    # Verify Gemini connectivity at startup
    try:
        from app.core.gemini_client import client
        response = client.models.generate_content(
            model=settings.gemini_flash_model,
            contents="Reply: OK",
        )
        logger.info(f"   Gemini: ✅ Connected ({response.text.strip()})")
    except Exception as e:
        logger.error(f"   Gemini: ❌ Connection failed — {e}")

    yield

    logger.info("OmniClaims Adjuster shutting down.")


app = FastAPI(
    title="OmniClaims Adjuster",
    description=(
        "Autonomous AI-powered insurance claims adjudication agent. "
        "Uses Gemini 3.1 Pro for multi-agent reasoning with full audit trail."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow Gradio and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(health_router, prefix="/api")
app.include_router(claims_router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint — redirect info."""
    return {
        "service": "OmniClaims Adjuster",
        "docs": "/docs",
        "health": "/api/health",
        "ui": "http://localhost:7860",
    }
