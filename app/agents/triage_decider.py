"""
TriageDecider Agent — Final adjudication authority.

Synthesizes all sub-agent analyses into a definitive claim decision
using a strict decision matrix.

Rule 23: CoT mandatory for final verdict.
Rule 28: Complete audit trail in the reasoning chain.
"""

from loguru import logger

from app.tools.decision_tools import make_triage_decision


class TriageDeciderAgent:
    """Specialist agent for final triage decision."""

    name = "TriageDecider"

    def run(
        self,
        claim_description: str,
        coverage_analysis: dict,
        damage_assessment: dict,
        fraud_risk: dict,
    ) -> dict:
        """
        Execute the final triage decision pipeline.

        Args:
            claim_description: Original claim text.
            coverage_analysis: CoverageAnalysis from PolicyAnalyzer.
            damage_assessment: DamageAssessment from DamageAssessor.
            fraud_risk: FraudRiskAssessment from FraudDetector.

        Returns:
            Dictionary with decision, payout, summary, and reasoning steps.
        """
        logger.info(f"[{self.name}] Agent activated — making final triage decision")

        result = make_triage_decision(
            claim_description=claim_description,
            coverage_analysis=coverage_analysis,
            damage_assessment=damage_assessment,
            fraud_risk=fraud_risk,
        )

        logger.info(f"[{self.name}] Verdict: {result.get('decision')} "
                     f"(payout=${result.get('payout_amount')})")
        return result
