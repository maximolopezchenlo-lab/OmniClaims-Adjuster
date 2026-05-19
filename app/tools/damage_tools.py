"""
Damage assessment tools for the DamageAssessor agent.

These functions use Gemini's native vision capabilities to analyze
damage evidence from images and videos.

Rule 3: Native multimodality for damage analysis.
Rule 18: Strict Pydantic-validated tool interfaces.
"""

import json
import base64
import mimetypes
from pathlib import Path
from loguru import logger

from app.core.gemini_client import generate_json_with_retry, upload_file
from app.core.prompts import DAMAGE_ASSESSOR_SYSTEM_PROMPT
from app.config import settings

# Supported image MIME types
IMAGE_MIMES = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
VIDEO_MIMES = {".mp4", ".avi", ".mov", ".webm"}


def _load_image_as_part(file_path: str) -> dict:
    """Load a local image file as an inline data part for Gemini."""
    path = Path(file_path)
    mime_type, _ = mimetypes.guess_type(str(path))
    if not mime_type:
        mime_type = "image/jpeg"

    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

    return {"inline_data": {"mime_type": mime_type, "data": data}}


def assess_damage(
    claim_description: str,
    evidence_file_paths: list[str] | None = None,
) -> dict:
    """
    Analyze damage evidence images/videos and assess severity.

    Uses Gemini 3.1 Pro's native vision (Rule 3) to evaluate damage
    from photographs and video evidence submitted with the claim.

    Args:
        claim_description: Text description of the claimed damage.
        evidence_file_paths: Paths to evidence image/video files.

    Returns:
        DamageAssessment-compatible dictionary.
    """
    logger.info(f"DamageAssessor: Starting damage analysis ({len(evidence_file_paths or [])} files)")

    contents = [DAMAGE_ASSESSOR_SYSTEM_PROMPT + "\n\n"]
    contents.append(f"CLAIM DESCRIPTION:\n{claim_description}\n\n")

    evidence_count = 0

    if evidence_file_paths:
        contents.append("DAMAGE EVIDENCE:\n")
        for file_path in evidence_file_paths:
            path = Path(file_path)
            suffix = path.suffix.lower()

            if suffix in IMAGE_MIMES:
                # Inline image for faster processing
                try:
                    image_part = _load_image_as_part(file_path)
                    contents.append(image_part)
                    contents.append(f"\n[Image: {path.name}]\n")
                    evidence_count += 1
                    logger.debug(f"DamageAssessor: Loaded image {path.name}")
                except Exception as e:
                    logger.warning(f"DamageAssessor: Failed to load {path.name}: {e}")

            elif suffix in VIDEO_MIMES:
                # Use Files API for video uploads
                try:
                    uploaded = upload_file(file_path, display_name=path.name)
                    contents.append(uploaded)
                    contents.append(f"\n[Video: {path.name}]\n")
                    evidence_count += 1
                    logger.debug(f"DamageAssessor: Uploaded video {path.name}")
                except Exception as e:
                    logger.warning(f"DamageAssessor: Video upload failed for {path.name}: {e}")
            else:
                logger.warning(f"DamageAssessor: Unsupported file type {suffix}")

    if evidence_count == 0:
        contents.append(
            "NOTE: No visual evidence files were provided. "
            "Base your assessment solely on the claim description. "
            "Set consistency_with_description to false and note the lack of evidence.\n"
        )
        logger.warning("DamageAssessor: No evidence files — text-only analysis")

    contents.append(
        "\nAnalyze ALL evidence provided above. "
        "Return a JSON object with: damage_severity (minor/moderate/severe/total_loss), "
        "damage_description (str), estimated_repair_cost (float), "
        "consistency_with_description (bool), visual_evidence_summary (str), "
        "affected_components (list[str]). "
        "Think step-by-step: describe what you SEE, then INFER, then CONCLUDE."
    )

    result_json = generate_json_with_retry(
        model=settings.gemini_pro_model,
        contents=contents,
    )

    result = json.loads(result_json)
    logger.info(f"DamageAssessor: Severity={result.get('damage_severity')}, "
                f"Cost=${result.get('estimated_repair_cost')}")
    return result
