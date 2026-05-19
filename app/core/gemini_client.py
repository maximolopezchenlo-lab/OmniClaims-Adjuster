"""
Shared Gemini client initialization.

Provides a singleton client for the google-genai SDK with
retry logic (Rule 29) and model validation.
"""

from google import genai
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings


def get_gemini_client() -> genai.Client:
    """
    Initialize and return a Gemini API client.

    Uses the API key from environment settings (Rule 15).
    """
    client = genai.Client(api_key=settings.gemini_api_key)
    logger.info("Gemini client initialized successfully")
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
