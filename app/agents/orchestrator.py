"""
OmniClaims Orchestrator — Central coordination agent.

This is the brain of the system. It orchestrates 4 specialist sub-agents
in sequence to process insurance claims autonomously and produce a
complete, auditable ClaimDecision.

Rule 1: Gemini 3.1 Pro as central brain for orchestration.
Rule 16: Asynchronous parallel work where possible.
Rule 19: Self-correcting error handling.
Rule 28: Transparent decision audit trail.
"""

import json
import time
from datetime import datetime, timezone
from loguru import logger

from app.agents.policy_analyzer import PolicyAnalyzerAgent
from app.agents.damage_assessor import DamageAssessorAgent
from app.agents.fraud_detector import FraudDetectorAgent
from app.agents.triage_decider import TriageDeciderAgent

from app.core.gemini_client import generate_json_with_retry
from app.core.prompts import CLAIM_INTAKE_PROMPT
from app.config import settings

from app.api.schemas.claim_output import (
    ClaimDecision,
    CoverageAnalysis,
    DamageAssessment,
    FraudRiskAssessment,
    ReasoningStep,
)


class OrchestratorAgent:
    """
    Central orchestrator that coordinates the full claim adjudication pipeline.

    Pipeline sequence:
    1. Claim Intake (extract structured data from free-text)
    2. PolicyAnalyzer (analyze coverage)
    3. DamageAssessor (evaluate visual evidence)
    4. FraudDetector (cross-validate all evidence)
    5. TriageDecider (make final decision)

    All results are assembled into a ClaimDecision with a full
    reasoning chain for audit transparency.
    """

    name = "Orchestrator"

    def __init__(self):
        self.policy_analyzer = PolicyAnalyzerAgent()
        self.damage_assessor = DamageAssessorAgent()
        self.fraud_detector = FraudDetectorAgent()
        self.triage_decider = TriageDeciderAgent()
        self.models_used: list[str] = []

    def process_claim(
        self,
        claim_text: str,
        policy_file_path: str | None = None,
        policy_text: str | None = None,
        evidence_file_paths: list[str] | None = None,
    ) -> ClaimDecision:
        """
        Execute the full claim adjudication pipeline.

        This is the main entry point for processing a claim through all
        sub-agents. Returns a complete ClaimDecision with audit trail.

        Args:
            claim_text: Free-text claim description from the user.
            policy_file_path: Path to the uploaded policy PDF (optional).
            policy_text: Raw text of the policy (fallback).
            evidence_file_paths: Paths to damage evidence files (optional).

        Returns:
            Complete ClaimDecision with all sub-analyses and reasoning chain.
        """
        start_time = time.time()
        reasoning_chain: list[dict] = []
        self.models_used = []

        logger.info(f"{'='*60}")
        logger.info(f"[{self.name}] ===  NEW CLAIM RECEIVED  ===")
        logger.info(f"{'='*60}")

        # =====================================================================
        # STEP 1: Claim Intake — Extract structured data from free text
        # =====================================================================
        logger.info(f"[{self.name}] Step 1/5: Claim Intake")
        step_start = time.time()

        claim_data = self._extract_claim_data(claim_text)

        reasoning_chain.append({
            "step_number": 1,
            "agent_name": self.name,
            "action": "Claim Intake — extracting structured data",
            "finding": f"Extracted claim ID: {claim_data.get('claim_id', 'N/A')}, "
                       f"type: {claim_data.get('incident_type', 'N/A')}",
            "confidence": 0.95,
            "evidence_references": ["user_submission"],
        })
        self.models_used.append(settings.gemini_flash_model)
        logger.info(f"[{self.name}] Step 1 complete ({time.time() - step_start:.1f}s)")

        # =====================================================================
        # STEP 2: Policy Analysis
        # =====================================================================
        logger.info(f"[{self.name}] Step 2/5: Policy Analysis")
        step_start = time.time()

        coverage_analysis = self.policy_analyzer.run(
            claim_description=claim_text,
            policy_file_path=policy_file_path,
            policy_text=policy_text,
        )

        reasoning_chain.append({
            "step_number": 2,
            "agent_name": self.policy_analyzer.name,
            "action": "Policy coverage analysis",
            "finding": f"Coverage: {'YES' if coverage_analysis.get('is_covered') else 'NO'}. "
                       f"Deductible: ${coverage_analysis.get('deductible_amount', 0)}, "
                       f"Limit: ${coverage_analysis.get('coverage_limit', 0)}",
            "confidence": 0.9,
            "evidence_references": coverage_analysis.get("relevant_clauses", []),
        })
        self.models_used.append(settings.gemini_pro_model)
        logger.info(f"[{self.name}] Step 2 complete ({time.time() - step_start:.1f}s)")

        # =====================================================================
        # STEP 3: Damage Assessment
        # =====================================================================
        logger.info(f"[{self.name}] Step 3/5: Damage Assessment")
        step_start = time.time()

        damage_assessment = self.damage_assessor.run(
            claim_description=claim_text,
            evidence_file_paths=evidence_file_paths,
        )

        reasoning_chain.append({
            "step_number": 3,
            "agent_name": self.damage_assessor.name,
            "action": "Visual damage evidence analysis",
            "finding": f"Severity: {damage_assessment.get('damage_severity')}. "
                       f"Estimated cost: ${damage_assessment.get('estimated_repair_cost', 0)}. "
                       f"Consistent: {damage_assessment.get('consistency_with_description')}",
            "confidence": 0.85,
            "evidence_references": damage_assessment.get("affected_components", []),
        })
        self.models_used.append(settings.gemini_pro_model)
        logger.info(f"[{self.name}] Step 3 complete ({time.time() - step_start:.1f}s)")

        # =====================================================================
        # STEP 4: Fraud Detection
        # =====================================================================
        logger.info(f"[{self.name}] Step 4/5: Fraud Detection")
        step_start = time.time()

        fraud_risk = self.fraud_detector.run(
            claim_description=claim_text,
            coverage_analysis=coverage_analysis,
            damage_assessment=damage_assessment,
        )

        reasoning_chain.append({
            "step_number": 4,
            "agent_name": self.fraud_detector.name,
            "action": "Fraud cross-validation analysis",
            "finding": f"Risk level: {fraud_risk.get('risk_level')}. "
                       f"Score: {fraud_risk.get('risk_score')}. "
                       f"Red flags: {len(fraud_risk.get('red_flags', []))}",
            "confidence": fraud_risk.get("risk_score", 0.5),
            "evidence_references": fraud_risk.get("red_flags", []),
        })
        self.models_used.append(settings.gemini_pro_model)
        logger.info(f"[{self.name}] Step 4 complete ({time.time() - step_start:.1f}s)")

        # =====================================================================
        # STEP 5: Final Triage Decision
        # =====================================================================
        logger.info(f"[{self.name}] Step 5/5: Final Triage Decision")
        step_start = time.time()

        triage_result = self.triage_decider.run(
            claim_description=claim_text,
            coverage_analysis=coverage_analysis,
            damage_assessment=damage_assessment,
            fraud_risk=fraud_risk,
        )

        reasoning_chain.append({
            "step_number": 5,
            "agent_name": self.triage_decider.name,
            "action": "Final triage decision",
            "finding": f"Decision: {triage_result.get('decision')}. "
                       f"Payout: ${triage_result.get('payout_amount', 'N/A')}. "
                       f"Summary: {triage_result.get('decision_summary', '')}",
            "confidence": 0.92,
            "evidence_references": ["coverage_analysis", "damage_assessment", "fraud_risk"],
        })
        self.models_used.append(settings.gemini_pro_model)
        logger.info(f"[{self.name}] Step 5 complete ({time.time() - step_start:.1f}s)")

        # =====================================================================
        # ASSEMBLE FINAL CLAIM DECISION
        # =====================================================================
        total_time = time.time() - start_time

        # Build validated Pydantic model
        claim_decision = ClaimDecision(
            claim_id=claim_data.get("claim_id", f"CLM-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')}"),
            decision=triage_result.get("decision", "HUMAN_REVIEW_REQUIRED"),
            decision_summary=triage_result.get("decision_summary", "Decision pending review"),
            payout_amount=triage_result.get("payout_amount"),
            coverage_analysis=CoverageAnalysis(**coverage_analysis),
            damage_assessment=DamageAssessment(**damage_assessment),
            fraud_risk=FraudRiskAssessment(**fraud_risk),
            reasoning_chain=[ReasoningStep(**step) for step in reasoning_chain],
            total_processing_time_seconds=round(total_time, 2),
            models_used=list(set(self.models_used)),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        logger.info(f"{'='*60}")
        logger.info(f"[{self.name}] ===  CLAIM PROCESSED  ===")
        logger.info(f"  Decision: {claim_decision.decision}")
        logger.info(f"  Payout:   ${claim_decision.payout_amount}")
        logger.info(f"  Time:     {total_time:.1f}s")
        logger.info(f"{'='*60}")

        return claim_decision

    def _extract_claim_data(self, claim_text: str) -> dict:
        """
        Extract structured claim data from free-text user input.

        Uses Gemini Flash for speed (Rule 26: <1s latency for UI interactions).
        """
        prompt = CLAIM_INTAKE_PROMPT.format(claim_text=claim_text)

        try:
            result_json = generate_json_with_retry(
                model=settings.gemini_flash_model,
                contents=[prompt],
            )
            return json.loads(result_json)
        except Exception as e:
            logger.warning(f"[{self.name}] Claim extraction failed: {e}")
            return {
                "claim_id": f"CLM-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')}",
                "claimant_name": "Unknown",
                "policy_number": "PENDING",
                "incident_date": datetime.now(timezone.utc).isoformat(),
                "incident_description": claim_text,
                "incident_type": "auto",
                "estimated_amount": None,
                "claimant_contact": None,
            }
