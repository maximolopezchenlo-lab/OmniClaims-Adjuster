"""
Decision-making tools for the TriageDecider agent.

Synthesizes all sub-agent analyses into a final claim adjudication decision
with payout calculation and transparent reasoning.

Rule 23: CoT mandatory for final decision.
Rule 28: Transparent decision audit trail.
"""

import json
from loguru import logger

from app.core.gemini_client import generate_json_with_retry
from app.core.prompts import TRIAGE_DECIDER_SYSTEM_PROMPT
from app.config import settings


def make_triage_decision(
    claim_description: str,
    coverage_analysis: dict,
    damage_assessment: dict,
    fraud_risk: dict,
) -> dict:
    """
    Synthesize all sub-agent results into a final adjudication decision.

    Applies the decision matrix from the TriageDecider system prompt
    to produce an APPROVED, REJECTED, or HUMAN_REVIEW_REQUIRED verdict.

    Args:
        claim_description: Original claim text.
        coverage_analysis: CoverageAnalysis dict from PolicyAnalyzer.
        damage_assessment: DamageAssessment dict from DamageAssessor.
        fraud_risk: FraudRiskAssessment dict from FraudDetector.

    Returns:
        Dictionary with decision, payout_amount, decision_summary, and reasoning.
    """
    logger.info("TriageDecider: Synthesizing final decision")

    contents = [
        TRIAGE_DECIDER_SYSTEM_PROMPT + "\n\n",
        f"=== ORIGINAL CLAIM ===\n{claim_description}\n\n",
        f"=== COVERAGE ANALYSIS ===\n{json.dumps(coverage_analysis, indent=2)}\n\n",
        f"=== DAMAGE ASSESSMENT ===\n{json.dumps(damage_assessment, indent=2)}\n\n",
        f"=== FRAUD RISK ASSESSMENT ===\n{json.dumps(fraud_risk, indent=2)}\n\n",
        "Based on ALL the above analyses, make your FINAL triage decision. "
        "Apply the decision matrix strictly. "
        "If APPROVED, calculate payout = min(estimated_repair_cost, coverage_limit) - deductible. "
        "Return a JSON object with: decision (APPROVED/REJECTED/HUMAN_REVIEW_REQUIRED), "
        "decision_summary (str — human-readable explanation), "
        "payout_amount (float or null), "
        "reasoning_steps (list of {step_number, action, finding, confidence}). "
        "Think step-by-step before stating your verdict."
    ]

    result_json = generate_json_with_retry(
        model=settings.gemini_pro_model,
        contents=contents,
    )

    result = json.loads(result_json)
    logger.info(f"TriageDecider: Decision={result.get('decision')}, "
                f"Payout=${result.get('payout_amount')}")
    return result
