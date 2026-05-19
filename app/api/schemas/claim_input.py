"""
Pydantic input schemas for claim submission.

Rule 18: Strict Pydantic schemas for all tool interfaces.
Rule 22: Structured output formats for Gemini responses.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ClaimInput(BaseModel):
    """Structured input extracted from the user's multimodal claim submission."""

    claim_id: str = Field(
        description="Unique claim identifier (auto-generated if not provided)",
    )
    claimant_name: str = Field(
        description="Full name of the person filing the claim",
    )
    policy_number: str = Field(
        description="Insurance policy number",
    )
    incident_date: str = Field(
        description="Date of the incident (ISO 8601 format preferred)",
    )
    incident_description: str = Field(
        description="Detailed narrative description of the incident",
    )
    incident_type: Literal["auto", "property", "health", "liability"] = Field(
        description="Category of insurance claim",
    )
    estimated_amount: float | None = Field(
        default=None,
        description="Claimant's estimated damage amount in USD",
    )
    claimant_contact: str | None = Field(
        default=None,
        description="Contact information (email or phone)",
    )


class ClaimSubmission(BaseModel):
    """Raw multimodal claim submission from the user interface."""

    claim_text: str = Field(
        description="Free-text description of the claim from the user",
    )
    policy_filename: str | None = Field(
        default=None,
        description="Filename of the uploaded policy PDF",
    )
    evidence_filenames: list[str] = Field(
        default_factory=list,
        description="Filenames of uploaded evidence images/videos",
    )
