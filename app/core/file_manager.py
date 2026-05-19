"""
File management utilities for multimodal inputs.

Handles temporary storage and upload of user-submitted files
(PDFs, images, videos) to the Gemini Files API.
"""

import os
import uuid
import shutil
from pathlib import Path

from loguru import logger


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_uploaded_file(file_bytes: bytes, original_filename: str) -> Path:
    """
    Save uploaded file bytes to a temporary location.

    Returns the path to the saved file.
    """
    # Generate unique filename to avoid collisions
    ext = Path(original_filename).suffix
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = UPLOAD_DIR / unique_name

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    logger.info(f"Saved uploaded file: {original_filename} -> {file_path}")
    return file_path


def cleanup_uploaded_file(file_path: Path) -> None:
    """Remove a temporary uploaded file after processing."""
    if file_path.exists():
        os.remove(file_path)
        logger.debug(f"Cleaned up file: {file_path}")


def cleanup_all_uploads() -> None:
    """Remove all temporary uploaded files."""
    if UPLOAD_DIR.exists():
        shutil.rmtree(UPLOAD_DIR)
        UPLOAD_DIR.mkdir(exist_ok=True)
        logger.info("Cleaned up all uploaded files")


def get_mime_type(filename: str) -> str:
    """Determine MIME type from file extension."""
    ext = Path(filename).suffix.lower()
    mime_map = {
        ".pdf": "application/pdf",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".mp4": "video/mp4",
        ".mov": "video/quicktime",
        ".avi": "video/x-msvideo",
        ".wav": "audio/wav",
        ".mp3": "audio/mpeg",
        ".webm": "video/webm",
    }
    return mime_map.get(ext, "application/octet-stream")
