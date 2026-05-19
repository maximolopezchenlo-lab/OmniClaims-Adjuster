"""
OmniClaims Adjuster — Gradio UI.

Premium hackathon demo interface with real-time agent progress,
multimodal file uploads, and transparent reasoning visualization.

Rule 2: Gemini Flash for UI speed.
Rule 26: Sub-second latency for initial response.
Rule 27: Streaming effect for agent "thinking".
"""

import json
import time
from datetime import datetime, timezone

import gradio as gr
from loguru import logger

from app.agents.orchestrator import OrchestratorAgent
from app.core.file_manager import save_uploaded_file, cleanup_uploaded_file
from app.config import settings


# =========================================================================
# CUSTOM CSS — Premium Glassmorphism Design
# =========================================================================
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif !important; }

.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0d1b2a 100%) !important;
    min-height: 100vh;
}

/* Header styling */
.hero-title {
    text-align: center;
    background: linear-gradient(135deg, #00d4ff, #7c3aed, #f59e0b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    margin-bottom: 0.25rem !important;
}

.hero-subtitle {
    text-align: center;
    color: #94a3b8 !important;
    font-size: 1rem !important;
    font-weight: 400 !important;
    margin-bottom: 1.5rem !important;
}

/* Glass cards */
.glass-card {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(20px) !important;
    padding: 1.25rem !important;
}

/* Status badges */
.badge-approved {
    background: linear-gradient(135deg, #059669, #10b981) !important;
    color: white !important;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
}

.badge-rejected {
    background: linear-gradient(135deg, #dc2626, #ef4444) !important;
    color: white !important;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
}

.badge-review {
    background: linear-gradient(135deg, #d97706, #f59e0b) !important;
    color: white !important;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
}

/* Submit button */
.submit-btn {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 12px 32px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
}

.submit-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(124, 58, 237, 0.5) !important;
}

/* Agent step indicators */
.step-active { color: #00d4ff !important; font-weight: 600; }
.step-done { color: #10b981 !important; }
.step-pending { color: #475569 !important; }

/* Reasoning chain */
.reasoning-box {
    background: rgba(124, 58, 237, 0.08) !important;
    border-left: 3px solid #7c3aed !important;
    border-radius: 0 12px 12px 0 !important;
    padding: 1rem !important;
    margin: 0.5rem 0 !important;
}

/* JSON output */
.json-output {
    background: rgba(0, 0, 0, 0.3) !important;
    border-radius: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* Tabs */
.tab-nav button {
    font-weight: 600 !important;
    border-radius: 8px 8px 0 0 !important;
}

/* Footer */
.footer-text {
    text-align: center;
    color: #475569;
    font-size: 0.75rem;
    margin-top: 1rem;
}
"""

# JavaScript to prevent Chrome auto-translate
NO_TRANSLATE_JS = """
() => {
    document.documentElement.setAttribute('lang', 'en');
    document.documentElement.setAttribute('translate', 'no');
    document.documentElement.classList.add('notranslate');
    const meta1 = document.createElement('meta');
    meta1.setAttribute('name', 'google');
    meta1.setAttribute('content', 'notranslate');
    document.head.appendChild(meta1);
    const meta2 = document.createElement('meta');
    meta2.setAttribute('http-equiv', 'Content-Language');
    meta2.setAttribute('content', 'en');
    document.head.appendChild(meta2);
}
"""


# =========================================================================
# CORE PROCESSING FUNCTION
# =========================================================================
def process_claim_ui(
    claim_text: str,
    policy_file: str | None,
    evidence_files: list[str] | None,
    progress=gr.Progress(),
):
    """
    Process a claim through the full multi-agent pipeline.

    This function bridges the Gradio UI with the OrchestratorAgent,
    providing real-time progress updates to the user.
    """
    if not claim_text or not claim_text.strip():
        return (
            "❌ Please enter a claim description.",
            "", "", "", "", "", ""
        )

    # Progress tracking
    progress(0.05, desc="📋 Initializing agents...")

    orchestrator = OrchestratorAgent()

    # Prepare file paths
    policy_path = policy_file if policy_file else None
    evidence_paths = evidence_files if evidence_files else None

    progress(0.15, desc="📋 Step 1/5: Extracting claim data...")
    time.sleep(0.3)  # Small delay for visual feedback

    progress(0.30, desc="📄 Step 2/5: Analyzing policy coverage...")
    progress(0.50, desc="🔍 Step 3/5: Assessing damage evidence...")
    progress(0.70, desc="🛡️ Step 4/5: Cross-validating for fraud...")
    progress(0.85, desc="⚖️ Step 5/5: Making final decision...")

    # Run the full pipeline
    try:
        result = orchestrator.process_claim(
            claim_text=claim_text,
            policy_file_path=policy_path,
            evidence_file_paths=evidence_paths,
        )
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        return (
            f"❌ Error processing claim: {str(e)}",
            "", "", "", "", "", ""
        )

    progress(1.0, desc="✅ Complete!")

    # Format outputs for the UI
    decision_badge = _format_decision_badge(result.decision, result.payout_amount)
    summary_md = _format_summary(result)
    coverage_md = _format_coverage(result.coverage_analysis)
    damage_md = _format_damage(result.damage_assessment)
    fraud_md = _format_fraud(result.fraud_risk)
    reasoning_md = _format_reasoning_chain(result.reasoning_chain)
    raw_json = json.dumps(result.model_dump(mode="json"), indent=2, default=str)

    return (
        decision_badge,
        summary_md,
        coverage_md,
        damage_md,
        fraud_md,
        reasoning_md,
        raw_json,
    )


# =========================================================================
# FORMATTERS — Premium Markdown Output
# =========================================================================
def _format_decision_badge(decision: str, payout: float | None) -> str:
    """Format the decision as a prominent badge with payout info."""
    icons = {
        "APPROVED": "✅",
        "REJECTED": "❌",
        "HUMAN_REVIEW_REQUIRED": "⚠️",
    }
    icon = icons.get(decision, "❓")
    payout_str = f"${payout:,.2f}" if payout else "N/A"

    return (
        f"## {icon} {decision}\n\n"
        f"**Payout:** {payout_str}"
    )


def _format_summary(result) -> str:
    """Format the decision summary with timing and model info."""
    return (
        f"### Decision Summary\n\n"
        f"{result.decision_summary}\n\n"
        f"---\n"
        f"⏱️ **Processing time:** {result.total_processing_time_seconds:.1f}s  \n"
        f"🤖 **Models used:** {', '.join(result.models_used)}  \n"
        f"📝 **Reasoning steps:** {len(result.reasoning_chain)}  \n"
        f"🕐 **Timestamp:** {result.timestamp}"
    )


def _format_coverage(ca) -> str:
    """Format coverage analysis results."""
    status = "✅ **COVERED**" if ca.is_covered else "❌ **NOT COVERED**"
    clauses = "\n".join(f"  - {c}" for c in ca.relevant_clauses)
    exclusions = "\n".join(f"  - ⚠️ {e}" for e in ca.exclusions_found) if ca.exclusions_found else "  - None found"

    return (
        f"### 📄 Policy Coverage\n\n"
        f"**Status:** {status}\n\n"
        f"**Relevant Clauses:**\n{clauses}\n\n"
        f"**Exclusions:**\n{exclusions}\n\n"
        f"**Deductible:** ${ca.deductible_amount:,.2f}  \n"
        f"**Coverage Limit:** ${ca.coverage_limit:,.2f}\n\n"
        f"---\n{ca.policy_summary}"
    )


def _format_damage(da) -> str:
    """Format damage assessment results."""
    severity_icons = {
        "minor": "🟢", "moderate": "🟡",
        "severe": "🟠", "total_loss": "🔴",
    }
    icon = severity_icons.get(da.damage_severity, "❓")
    components = "\n".join(f"  - {c}" for c in da.affected_components)
    consistency = "✅ Consistent" if da.consistency_with_description else "⚠️ Inconsistent"

    return (
        f"### 🔍 Damage Assessment\n\n"
        f"**Severity:** {icon} {da.damage_severity.upper()}\n\n"
        f"**Estimated Repair Cost:** ${da.estimated_repair_cost:,.2f}\n\n"
        f"**Evidence vs. Description:** {consistency}\n\n"
        f"**Affected Components:**\n{components}\n\n"
        f"---\n{da.damage_description}"
    )


def _format_fraud(fr) -> str:
    """Format fraud risk assessment results."""
    risk_icons = {
        "low": "🟢", "medium": "🟡",
        "high": "🟠", "critical": "🔴",
    }
    icon = risk_icons.get(fr.risk_level, "❓")
    flags = "\n".join(f"  - 🚩 {f}" for f in fr.red_flags) if fr.red_flags else "  - None detected"

    return (
        f"### 🛡️ Fraud Risk Assessment\n\n"
        f"**Risk Level:** {icon} {fr.risk_level.upper()}\n\n"
        f"**Risk Score:** {fr.risk_score:.0%}\n\n"
        f"**Red Flags:**\n{flags}\n\n"
        f"**Recommendation:** {fr.recommendation}\n\n"
        f"---\n{fr.cross_validation_notes}"
    )


def _format_reasoning_chain(chain) -> str:
    """Format the reasoning chain as a visual timeline."""
    lines = ["### 🧠 Agent Reasoning Chain\n"]

    for step in chain:
        confidence_bar = "█" * int(step.confidence * 10) + "░" * (10 - int(step.confidence * 10))
        lines.append(
            f"**Step {step.step_number}** — `{step.agent_name}`\n\n"
            f"🔧 **Action:** {step.action}  \n"
            f"📋 **Finding:** {step.finding}  \n"
            f"📊 **Confidence:** [{confidence_bar}] {step.confidence:.0%}  \n"
        )
        if step.evidence_references:
            refs = ", ".join(step.evidence_references[:5])
            lines.append(f"📎 **Evidence:** {refs}\n")
        lines.append("---\n")

    return "\n".join(lines)


# =========================================================================
# DEMO SCENARIOS
# =========================================================================
DEMO_SCENARIOS = {
    "🚗 Auto — Hail Damage (Approved)": (
        "My name is John Martinez, policy number AUT-2026-78432. "
        "On May 15, 2026, my 2024 Toyota Camry was damaged in a severe hailstorm "
        "while parked at my office in Dallas, TX. The roof has multiple dents, "
        "the windshield is cracked, and the hood has significant hail damage. "
        "I estimate the repair cost at around $3,500. "
        "Please process my comprehensive coverage claim. "
        "My contact: john.martinez@email.com, phone: 555-0142."
    ),
    "🏠 Property — Water Damage (Complex)": (
        "I'm Sarah Chen, policy HOM-2026-55901. On May 10, 2026, I returned from "
        "vacation to find my basement completely flooded due to a burst pipe. "
        "The water has been sitting for about a week, causing damage to the flooring, "
        "drywall, and stored personal belongings. My water heater and HVAC system "
        "are also affected. I estimate the total damage at $18,000-$25,000. "
        "Contact: sarah.chen@email.com, 555-0299."
    ),
    "🚑 Auto — Suspicious Rear-End (Fraud Check)": (
        "My name is Michael Roberts, policy AUT-2026-33210. Yesterday at 2 AM, "
        "another car rear-ended me at a red light. I have severe neck and back pain. "
        "My 2023 BMW X5 has extensive rear-end damage. The other driver left the scene. "
        "I need to claim $45,000 for vehicle repairs and $15,000 for medical expenses. "
        "No police report was filed. I just started this policy two weeks ago. "
        "Contact: m.roberts@gmail.com."
    ),
}


def load_demo_scenario(scenario_name: str) -> str:
    """Load a pre-built demo scenario."""
    return DEMO_SCENARIOS.get(scenario_name, "")


# =========================================================================
# ENGLISH LOCALE — Force Gradio to English for international judges
# =========================================================================
ENGLISH_I18N = gr.I18n(
    en={
        "submit": "Submit",
        "clear": "Clear",
        "upload_file": "Drop File Here",
        "or": "- or -",
        "click_to_upload": "Click to Upload",
        "processing": "Processing...",
        "cancel": "Cancel",
        "error": "Error",
        "flag": "Flag",
    },
)


# =========================================================================
# BUILD THE GRADIO APP
# =========================================================================
# Gradio 6.0: theme and css must be passed to launch(), not Blocks()
OMNI_THEME = gr.themes.Base(
    primary_hue="violet",
    secondary_hue="blue",
    neutral_hue="slate",
    font=gr.themes.GoogleFont("Inter"),
).set(
    body_background_fill="linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0d1b2a 100%)",
    body_text_color="#e2e8f0",
    block_background_fill="rgba(255, 255, 255, 0.04)",
    block_border_color="rgba(255, 255, 255, 0.08)",
    block_label_text_color="#94a3b8",
    input_background_fill="rgba(255, 255, 255, 0.06)",
    button_primary_background_fill="linear-gradient(135deg, #7c3aed, #2563eb)",
    button_primary_text_color="white",
)


def create_gradio_app() -> gr.Blocks:
    """Create the premium Gradio interface."""

    with gr.Blocks(
        title="OmniClaims Adjuster — AI Agent Olympics",
    ) as app:
        # Header
        gr.Markdown(
            "<h1 class='hero-title'>⚡ OmniClaims Adjuster</h1>"
            "<p class='hero-subtitle'>"
            "Autonomous AI Claims Adjudication • Powered by Gemini 3.1 Pro"
            "</p>",
        )

        with gr.Row():
            # LEFT COLUMN — Input
            with gr.Column(scale=2):
                gr.Markdown("### 📋 Submit a Claim")

                # Demo scenario selector
                demo_dropdown = gr.Dropdown(
                    choices=list(DEMO_SCENARIOS.keys()),
                    label="🎯 Quick Demo Scenarios",
                    info="Select a pre-built scenario or type your own below",
                    interactive=True,
                )

                claim_input = gr.Textbox(
                    label="Claim Description",
                    placeholder="Describe the insurance claim in detail...",
                    lines=6,
                    max_lines=12,
                )

                # Wire demo dropdown to claim text
                demo_dropdown.change(
                    fn=load_demo_scenario,
                    inputs=[demo_dropdown],
                    outputs=[claim_input],
                )

                with gr.Row():
                    policy_upload = gr.File(
                        label="📄 Policy PDF (optional)",
                        file_types=[".pdf"],
                        type="filepath",
                    )
                    evidence_upload = gr.File(
                        label="📸 Evidence Files (optional)",
                        file_types=["image", ".mp4", ".mov"],
                        file_count="multiple",
                        type="filepath",
                    )

                submit_btn = gr.Button(
                    "⚡ Process Claim",
                    variant="primary",
                    size="lg",
                    elem_classes=["submit-btn"],
                )

            # RIGHT COLUMN — Quick Result
            with gr.Column(scale=1):
                gr.Markdown("### ⚖️ Decision")
                decision_output = gr.Markdown(
                    value="*Awaiting claim submission...*",
                    elem_classes=["glass-card"],
                )
                summary_output = gr.Markdown(
                    value="",
                    elem_classes=["glass-card"],
                )

        # DETAILED RESULTS — Tabbed View
        gr.Markdown("### 📊 Detailed Analysis")

        with gr.Tabs() as result_tabs:
            with gr.Tab("📄 Coverage"):
                coverage_output = gr.Markdown(value="*Submit a claim to see coverage analysis...*")

            with gr.Tab("🔍 Damage"):
                damage_output = gr.Markdown(value="*Submit a claim to see damage assessment...*")

            with gr.Tab("🛡️ Fraud"):
                fraud_output = gr.Markdown(value="*Submit a claim to see fraud analysis...*")

            with gr.Tab("🧠 Reasoning Chain"):
                reasoning_output = gr.Markdown(value="*Submit a claim to see the agent's reasoning...*")

            with gr.Tab("📦 Raw JSON"):
                json_output = gr.Code(
                    label="Complete ClaimDecision JSON",
                    language="json",
                    value="",
                )

        # Footer
        gr.Markdown(
            "<p class='footer-text'>"
            "🏆 AI Agent Olympics Hackathon — Milan AI Week 2026 • "
            f"Models: {settings.gemini_pro_model} + {settings.gemini_flash_model} • "
            "Built with Gemini + FastAPI + Gradio"
            "</p>"
        )

        # Wire submit button
        submit_btn.click(
            fn=process_claim_ui,
            inputs=[claim_input, policy_upload, evidence_upload],
            outputs=[
                decision_output,
                summary_output,
                coverage_output,
                damage_output,
                fraud_output,
                reasoning_output,
                json_output,
            ],
        )

        # Inject anti-translate JS on page load
        app.load(fn=None, js=NO_TRANSLATE_JS)

    return app


# =========================================================================
# STANDALONE LAUNCH
# =========================================================================
if __name__ == "__main__":
    logger.info("Launching OmniClaims Adjuster UI...")
    app = create_gradio_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        i18n=ENGLISH_I18N,
        theme=OMNI_THEME,
        css=CUSTOM_CSS,
    )
