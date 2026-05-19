"""
PolicyAnalyzer Agent — Insurance policy document analysis specialist.

Reads the full policy PDF and determines coverage, exclusions, and limits
for the submitted claim.

Rule 4: Leverages massive context window for entire policy documents.
Rule 23: CoT mandatory for coverage determination.
"""

from loguru import logger

from app.tools.policy_tools import analyze_policy_coverage


class PolicyAnalyzerAgent:
    """Specialist agent for insurance policy analysis."""

    name = "PolicyAnalyzer"

    def run(
        self,
        claim_description: str,
        policy_file_path: str | None = None,
        policy_text: str | None = None,
    ) -> dict:
        """
        Execute the policy analysis pipeline.

        Args:
            claim_description: The incident description from the claim.
            policy_file_path: Path to the uploaded policy PDF.
            policy_text: Fallback raw text of the policy.

        Returns:
            CoverageAnalysis-compatible dictionary.
        """
        logger.info(f"[{self.name}] Agent activated — analyzing policy coverage")

        result = analyze_policy_coverage(
            claim_description=claim_description,
            policy_file_path=policy_file_path,
            policy_text=policy_text,
        )

        logger.info(f"[{self.name}] Analysis complete — covered={result.get('is_covered')}")
        return result
