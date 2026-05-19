"""
Shared Gemini client initialization.

Supports TWO authentication modes:
1. API Key mode (Google AI Studio) — simpler, but requires paid credits on AI Studio
2. Vertex AI mode (Google Cloud) — uses $300 free trial credits via Vertex AI

Rule 15: API keys injected via environment, never hardcoded.
Rule 29: Exponential backoff retry for production stability.
"""

from google import genai
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings


def get_gemini_client() -> genai.Client:
    """
    Initialize and return a Gemini API client.

    Automatically selects authentication mode based on config:
    - If USE_VERTEX_AI=true: Uses Google Cloud credentials (ADC) + project ID
    - Otherwise: Uses GEMINI_API_KEY from AI Studio
    """
    if settings.use_vertex_ai:
        client = genai.Client(
            vertexai=True,
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
        )
        logger.info(
            f"Gemini client initialized via Vertex AI "
            f"(project={settings.google_cloud_project}, "
            f"location={settings.google_cloud_location})"
        )
    else:
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is required when USE_VERTEX_AI is false. "
                "Set it in your .env file or switch to Vertex AI mode."
            )
        client = genai.Client(api_key=settings.gemini_api_key)
        logger.info("Gemini client initialized via API Key (Google AI Studio)")

    return client


# Singleton client instance
client = get_gemini_client()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
)
def generate_with_retry(
    model: str,
    contents: list,
    config: dict | None = None,
) -> str:
    """
    Generate content with exponential backoff retry.

    Rule 29: Backoff strategy to prevent demo crashes under load.
    """
    generation_config = config or {}

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generation_config,
    )
    return response.text


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
)
def generate_json_with_retry(
    model: str,
    contents: list,
    response_schema: dict | None = None,
) -> str:
    """
    Generate structured JSON content with retry.

    Rule 22: Enforces response_mime_type="application/json".
    """
    config = {
        "response_mime_type": "application/json",
    }
    if response_schema:
        config["response_schema"] = response_schema

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )
    return response.text


def list_available_models() -> list[str]:
    """List all available Gemini models for verification."""
    models = []
    for model in client.models.list():
        models.append(model.name)
    return models


def upload_file(file_path: str, display_name: str | None = None) -> object:
    """
    Upload a file to Gemini's Files API for multimodal processing.

    Supports: PDF, images (JPEG/PNG), video (MP4), audio (WAV/MP3).
    Files are stored temporarily (~48 hours) on Google's servers.
    """
    upload_kwargs = {"file": file_path}
    if display_name:
        upload_kwargs["config"] = {"display_name": display_name}

    uploaded = client.files.upload(**upload_kwargs)
    logger.info(f"File uploaded: {uploaded.name} ({uploaded.mime_type})")
    return uploaded
