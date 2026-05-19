"""
DamageAssessor Agent — Visual damage evidence analysis specialist.

Uses Gemini's native multimodal vision to evaluate damage from
images and videos submitted with the claim.

Rule 3: Native vision for damage analysis.
Rule 23: CoT mandatory — describe, infer, conclude.
"""

from loguru import logger

from app.tools.damage_tools import assess_damage


class DamageAssessorAgent:
    """Specialist agent for visual damage assessment."""

    name = "DamageAssessor"

    def run(
        self,
        claim_description: str,
        evidence_file_paths: list[str] | None = None,
    ) -> dict:
        """
        Execute the damage assessment pipeline.

        Args:
            claim_description: The incident description from the claim.
            evidence_file_paths: Paths to damage evidence images/videos.

        Returns:
            DamageAssessment-compatible dictionary.
        """
        logger.info(f"[{self.name}] Agent activated — assessing damage evidence")

        result = assess_damage(
            claim_description=claim_description,
            evidence_file_paths=evidence_file_paths,
        )

        logger.info(f"[{self.name}] Assessment complete — "
                     f"severity={result.get('damage_severity')}")
        return result
