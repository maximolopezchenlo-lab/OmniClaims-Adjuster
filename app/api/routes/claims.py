"""
Claims processing API routes.

Exposes the OmniClaims Adjuster pipeline as REST endpoints
for both the Gradio frontend and direct API consumers.

Rule 22: Structured JSON output enforced via Pydantic.
Rule 27: Streaming support for real-time feedback.
"""

import json
import asyncio
from pathlib import Path
from loguru import logger

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse

from app.agents.orchestrator import OrchestratorAgent
from app.core.file_manager import save_uploaded_file, cleanup_uploaded_file
from app.api.schemas.claim_output import ClaimDecision

router = APIRouter(prefix="/claims", tags=["Claims"])


@router.post("/process", response_model=ClaimDecision)
async def process_claim(
    claim_text: str = Form(..., description="Free-text claim description"),
    policy_file: UploadFile | None = File(None, description="Policy PDF document"),
    evidence_files: list[UploadFile] = File(default=[], description="Damage evidence images/videos"),
) -> ClaimDecision:
    """
    Process an insurance claim through the full multi-agent pipeline.

    Accepts multimodal input:
    - claim_text: Required free-text description
    - policy_file: Optional PDF policy document
    - evidence_files: Optional damage evidence images/videos

    Returns a complete ClaimDecision with reasoning chain.
    """
    logger.info(f"API: Received claim submission "
                f"(policy={'yes' if policy_file else 'no'}, "
                f"evidence={len(evidence_files)} files)")

    saved_files: list[Path] = []
    policy_path: str | None = None
    evidence_paths: list[str] = []

    try:
        # Save policy PDF if provided
        if policy_file and policy_file.filename:
            content = await policy_file.read()
            path = save_uploaded_file(content, policy_file.filename)
            policy_path = str(path)
            saved_files.append(path)
            logger.info(f"API: Policy file saved: {policy_file.filename}")

        # Save evidence files
        for ef in evidence_files:
            if ef.filename:
                content = await ef.read()
                path = save_uploaded_file(content, ef.filename)
                evidence_paths.append(str(path))
                saved_files.append(path)

        if evidence_paths:
            logger.info(f"API: {len(evidence_paths)} evidence files saved")

        # Run the full pipeline (blocking — runs in thread pool)
        orchestrator = OrchestratorAgent()
        result = await asyncio.to_thread(
            orchestrator.process_claim,
            claim_text=claim_text,
            policy_file_path=policy_path,
            evidence_file_paths=evidence_paths if evidence_paths else None,
        )

        return result

    finally:
        # Cleanup uploaded files
        for path in saved_files:
            cleanup_uploaded_file(path)


@router.post("/process/stream")
async def process_claim_stream(
    claim_text: str = Form(..., description="Free-text claim description"),
) -> StreamingResponse:
    """
    Stream claim processing updates in real-time.

    Rule 27: Streaming responses for the demo UI.
    Sends Server-Sent Events (SSE) with progress updates.
    """

    async def event_generator():
        steps = [
            ("intake", "📋 Extracting claim data..."),
            ("policy", "📄 Analyzing insurance policy..."),
            ("damage", "🔍 Assessing damage evidence..."),
            ("fraud", "🛡️ Cross-validating for fraud..."),
            ("decision", "⚖️ Making final triage decision..."),
        ]

        for step_id, message in steps:
            yield f"data: {json.dumps({'step': step_id, 'message': message, 'status': 'running'})}\n\n"
            await asyncio.sleep(0.1)

        # Run the actual pipeline
        orchestrator = OrchestratorAgent()
        result = await asyncio.to_thread(
            orchestrator.process_claim,
            claim_text=claim_text,
        )

        yield f"data: {json.dumps({'step': 'complete', 'message': '✅ Claim processed!', 'status': 'done', 'result': result.model_dump(mode='json')})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
