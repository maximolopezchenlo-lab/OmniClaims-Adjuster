"""
Pydantic output schemas for claim decisions.

This is the "money shot" for judges — the structured JSON that demonstrates
Gemini's agentic reasoning with full audit trail.

Rule 18: Strict Pydantic schemas with precise types.
Rule 22: JSON output with enforced schema via response_mime_type.
Rule 23: Chain-of-Thought reasoning captured in ReasoningStep.
Rule 28: Transparent decision audit trail.
"""

from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


class ReasoningStep(BaseModel):
    """Single step in the agent's chain-of-thought reasoning trail."""

    step_number: int = Field(
        description="Sequential step number in the reasoning chain",
    )
    agent_name: str = Field(
        description="Name of the sub-agent that performed this step",
    )
    action: str = Field(
        description="What action was performed (e.g., 'Analyzing policy coverage')",
    )
    finding: str = Field(
        description="What was discovered or concluded in this step",
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score for this finding (0.0 to 1.0)",
    )
    evidence_references: list[str] = Field(
        default_factory=list,
        description="References to source evidence (page numbers, image IDs, etc.)",
    )


class CoverageAnalysis(BaseModel):
    """Results from the PolicyAnalyzer agent's policy document analysis."""

    is_covered: bool = Field(
        description="Whether the incident type is covered under the policy",
    )
    relevant_clauses: list[str] = Field(
        description="Policy clauses relevant to this claim",
    )
    exclusions_found: list[str] = Field(
        default_factory=list,
        description="Any exclusion clauses that may apply",
    )
    deductible_amount: float = Field(
        description="Deductible amount per the policy terms",
    )
    coverage_limit: float = Field(
        description="Maximum coverage limit for this incident type",
    )
    policy_summary: str = Field(
        description="Brief summary of the policy's relevant terms",
    )


class DamageAssessment(BaseModel):
    """Results from the DamageAssessor agent's visual evidence analysis."""

    damage_severity: Literal["minor", "moderate", "severe", "total_loss"] = Field(
        description="Overall severity classification of the damage",
    )
    damage_description: str = Field(
        description="Detailed description of observed damage",
    )
    estimated_repair_cost: float = Field(
        description="Estimated cost to repair or replace the damaged item",
    )
    consistency_with_description: bool = Field(
        description="Whether visual evidence is consistent with the claim narrative",
    )
    visual_evidence_summary: str = Field(
        description="Summary of what was observed in the evidence images/video",
    )
    affected_components: list[str] = Field(
        default_factory=list,
        description="List of specific components or areas affected",
    )


class FraudRiskAssessment(BaseModel):
    """Results from the FraudDetector agent's cross-validation analysis."""

    risk_level: Literal["low", "medium", "high", "critical"] = Field(
        description="Overall fraud risk classification",
    )
    risk_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Numerical fraud risk score (0.0 = no risk, 1.0 = certain fraud)",
    )
    red_flags: list[str] = Field(
        default_factory=list,
        description="Specific fraud indicators detected",
    )
    cross_validation_notes: str = Field(
        description="Notes on consistency between claim description, policy, and evidence",
    )
    recommendation: str = Field(
        description="Recommended action based on fraud risk",
    )


class ClaimDecision(BaseModel):
    """
    Final structured output from the OmniClaims Adjuster.

    This is the complete adjudication result with full transparency
    into the agent's reasoning process — the key differentiator
    for the "Best Use of Gemini" award.
    """

    # --- Core Decision ---
    claim_id: str = Field(
        description="Unique identifier for this claim",
    )
    decision: Literal["APPROVED", "REJECTED", "HUMAN_REVIEW_REQUIRED"] = Field(
        description="Final adjudication decision",
    )
    decision_summary: str = Field(
        description="Human-readable summary explaining the decision",
    )
    payout_amount: float | None = Field(
        default=None,
        description="Approved payout amount (null if rejected or pending review)",
    )

    # --- Detailed Analysis Sections ---
    coverage_analysis: CoverageAnalysis = Field(
        description="Results from policy document analysis",
    )
    damage_assessment: DamageAssessment = Field(
        description="Results from visual damage evidence analysis",
    )
    fraud_risk: FraudRiskAssessment = Field(
        description="Results from fraud detection analysis",
    )

    # --- Agentic Reasoning Trail (KEY DIFFERENTIATOR) ---
    reasoning_chain: list[ReasoningStep] = Field(
        description="Complete chain-of-thought reasoning steps taken by the agent",
    )
    total_processing_time_seconds: float = Field(
        description="Total wall-clock time for the full adjudication pipeline",
    )

    # --- Metadata ---
    models_used: list[str] = Field(
        description="Gemini models invoked during processing",
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="ISO 8601 timestamp of the decision",
    )
