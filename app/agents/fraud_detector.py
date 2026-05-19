"""
FraudDetector Agent — Cross-validation fraud analysis specialist.

Compares all evidence sources to detect inconsistencies,
fraud patterns, and timeline anomalies.

Rule 23: CoT mandatory for fraud risk assessment.
Rule 28: Transparent audit trail for every red flag.
"""

from loguru import logger

from app.tools.fraud_tools import detect_fraud_risk


class FraudDetectorAgent:
    """Specialist agent for fraud detection and cross-validation."""

    name = "FraudDetector"

    def run(
        self,
        claim_description: str,
        coverage_analysis: dict,
        damage_assessment: dict,
    ) -> dict:
        """
        Execute the fraud detection pipeline.

        Args:
            claim_description: Original claim text.
            coverage_analysis: Results from PolicyAnalyzer.
            damage_assessment: Results from DamageAssessor.

        Returns:
            FraudRiskAssessment-compatible dictionary.
        """
        logger.info(f"[{self.name}] Agent activated — cross-validating evidence")

        result = detect_fraud_risk(
            claim_description=claim_description,
            coverage_analysis=coverage_analysis,
            damage_assessment=damage_assessment,
        )

        logger.info(f"[{self.name}] Analysis complete — "
                     f"risk={result.get('risk_level')}, score={result.get('risk_score')}")
        return result
