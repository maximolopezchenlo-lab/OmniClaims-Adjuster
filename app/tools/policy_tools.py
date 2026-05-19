"""
Policy analysis tools for the PolicyAnalyzer agent.

These functions are called by the agent to analyze insurance policy documents
and extract coverage information.

Rule 18: Strict Pydantic-validated tool interfaces.
"""

import json
from loguru import logger

from app.core.gemini_client import generate_json_with_retry, upload_file
from app.core.prompts import POLICY_ANALYZER_SYSTEM_PROMPT
from app.config import settings


def analyze_policy_coverage(
    claim_description: str,
    policy_file_path: str | None = None,
    policy_text: str | None = None,
) -> dict:
    """
    Analyze an insurance policy document against a specific claim.

    Uses Gemini 3.1 Pro's massive context window (Rule 4) to process
    the entire policy document alongside the claim description.

    Args:
        claim_description: Text description of the incident/claim.
        policy_file_path: Path to the policy PDF file (optional).
        policy_text: Raw text of the policy (fallback if no PDF).

    Returns:
        CoverageAnalysis-compatible dictionary with coverage determination.
    """
    logger.info("PolicyAnalyzer: Starting policy coverage analysis")

    contents = [POLICY_ANALYZER_SYSTEM_PROMPT + "\n\n"]

    # Add policy document — use Files API for PDFs (Rule 3: native multimodality)
    if policy_file_path:
        try:
            uploaded = upload_file(policy_file_path, display_name="insurance_policy")
            contents.append(uploaded)
            contents.append("\n\nThe above is the complete insurance policy document.\n\n")
            logger.info(f"PolicyAnalyzer: Policy PDF uploaded via Files API")
        except Exception as e:
            logger.warning(f"PolicyAnalyzer: PDF upload failed ({e}), using text fallback")
            if policy_text:
                contents.append(f"POLICY DOCUMENT TEXT:\n{policy_text}\n\n")
    elif policy_text:
        contents.append(f"POLICY DOCUMENT TEXT:\n{policy_text}\n\n")
    else:
        # Demo mode — use synthetic policy context
        contents.append(
            "POLICY DOCUMENT: Standard comprehensive insurance policy.\n"
            "Coverage: Auto comprehensive, collision, liability. "
            "Deductible: $500. Coverage limit: $50,000. "
            "Exclusions: Intentional damage, racing, commercial use.\n\n"
        )
        logger.info("PolicyAnalyzer: No policy file provided — using demo defaults")

    contents.append(
        f"CLAIM DESCRIPTION:\n{claim_description}\n\n"
        "Analyze this policy against the claim. "
        "Return a JSON object with: is_covered (bool), relevant_clauses (list[str]), "
        "exclusions_found (list[str]), deductible_amount (float), "
        "coverage_limit (float), policy_summary (str). "
        "Think step-by-step before concluding."
    )

    result_json = generate_json_with_retry(
        model=settings.gemini_pro_model,
        contents=contents,
    )

    result = json.loads(result_json)
    logger.info(f"PolicyAnalyzer: Coverage={result.get('is_covered')}")
    return result
