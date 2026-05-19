"""
Fraud detection tools for the FraudDetector agent.

Cross-validates all evidence sources to detect inconsistencies
and common fraud patterns.

Rule 23: Chain-of-Thought mandatory for fraud risk assessment.
Rule 18: Strict Pydantic-validated tool interfaces.
"""

import json
from loguru import logger

from app.core.gemini_client import generate_json_with_retry
from app.core.prompts import FRAUD_DETECTOR_SYSTEM_PROMPT
from app.config import settings


def detect_fraud_risk(
    claim_description: str,
    coverage_analysis: dict,
    damage_assessment: dict,
) -> dict:
    """
    Cross-validate all evidence to detect fraud indicators.

    Uses Gemini 3.1 Pro to compare the claim narrative, policy analysis,
    and damage assessment for inconsistencies. Rule 23 enforces step-by-step
    reasoning before assigning a risk level.

    Args:
        claim_description: Original claim text from the user.
        coverage_analysis: Results from PolicyAnalyzer (CoverageAnalysis dict).
        damage_assessment: Results from DamageAssessor (DamageAssessment dict).

    Returns:
        FraudRiskAssessment-compatible dictionary.
    """
    logger.info("FraudDetector: Starting cross-validation analysis")

    contents = [
        FRAUD_DETECTOR_SYSTEM_PROMPT + "\n\n",
        f"=== ORIGINAL CLAIM ===\n{claim_description}\n\n",
        f"=== POLICY ANALYSIS (from PolicyAnalyzer) ===\n"
        f"{json.dumps(coverage_analysis, indent=2)}\n\n",
        f"=== DAMAGE ASSESSMENT (from DamageAssessor) ===\n"
        f"{json.dumps(damage_assessment, indent=2)}\n\n",
        "Cross-validate ALL three sources above. "
        "Look for inconsistencies, timeline issues, and common fraud patterns. "
        "Return a JSON object with: risk_level (low/medium/high/critical), "
        "risk_score (0.0-1.0), red_flags (list[str]), "
        "cross_validation_notes (str), recommendation (str). "
        "Think step-by-step: list observations, then patterns, then your assessment."
    ]

    result_json = generate_json_with_retry(
        model=settings.gemini_pro_model,
        contents=contents,
    )

    result = json.loads(result_json)
    logger.info(f"FraudDetector: Risk={result.get('risk_level')}, "
                f"Score={result.get('risk_score')}")
    return result
