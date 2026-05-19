# ⚡ OmniClaims Adjuster

> **Autonomous AI-powered insurance claims adjudication agent.**  
> Built for the **AI Agent Olympics Hackathon** — Milan AI Week 2026  
> 🏆 *Best Use of Gemini* Category

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_3.1_Pro-4285F4?logo=google&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-F97316?logo=gradio&logoColor=white)

---

## 🎯 What It Does

OmniClaims Adjuster is an **autonomous multi-agent system** that processes insurance claims using Gemini 3.1's advanced reasoning capabilities. It receives a claim (text + optional policy PDF + damage photos), coordinates 4 specialist AI agents, and produces a fully auditable adjudication decision — all in under 60 seconds.

### The Pipeline

```
User Submission (text + PDF + images)
         │
         ▼
┌─────────────────────┐
│   🎯 Orchestrator    │  ← Gemini 3 Flash (intake)
│   (Central Brain)    │
└─────────┬───────────┘
          │
    ┌─────┴──────┐
    ▼            ▼
┌──────────┐ ┌──────────┐
│ 📄 Policy │ │ 🔍 Damage │  ← Gemini 3.1 Pro (analysis)
│ Analyzer  │ │ Assessor  │
└─────┬────┘ └─────┬────┘
      │            │
      └──────┬─────┘
             ▼
      ┌──────────────┐
      │  🛡️ Fraud     │  ← Gemini 3.1 Pro (cross-validation)
      │  Detector     │
      └──────┬───────┘
             ▼
      ┌──────────────┐
      │  ⚖️ Triage    │  ← Gemini 3.1 Pro (final decision)
      │  Decider      │
      └──────┬───────┘
             ▼
    ┌─────────────────┐
    │ 📊 ClaimDecision │
    │ (Structured JSON │
    │  + Audit Trail)  │
    └─────────────────┘
```

### Key Features

| Feature | Implementation |
|:--------|:--------------|
| **Multimodal Input** | PDF policy docs, damage photos/videos, free-text claims |
| **Multi-Agent Architecture** | 5 specialized agents coordinated by an Orchestrator |
| **Structured JSON Output** | Pydantic-validated `ClaimDecision` with full schema enforcement |
| **Chain-of-Thought Reasoning** | Every decision step documented with confidence scores |
| **Fraud Detection** | Cross-validation of narrative vs. evidence vs. policy |
| **Transparent Audit Trail** | Complete reasoning chain for regulatory compliance |
| **Premium UI** | Glassmorphism Gradio interface with real-time progress |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Google Cloud account with Vertex AI enabled
- `gcloud` CLI authenticated

### Setup

```bash
# Clone the repository
git clone <repo-url> && cd OmniClaims

# Create virtual environment
python3 -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Google Cloud project ID

# Authenticate with Google Cloud
gcloud auth application-default login
```

### Run

```bash
# Launch the Gradio UI
python -m ui.gradio_app

# Or start the FastAPI backend
uvicorn app.main:app --reload --port 8000
```

Visit `http://localhost:7860` for the UI or `http://localhost:8000/docs` for the API.

---

## 🏗️ Architecture

```
app/
├── agents/               # Multi-agent system
│   ├── orchestrator.py   # Central coordination agent
│   ├── policy_analyzer.py
│   ├── damage_assessor.py
│   ├── fraud_detector.py
│   └── triage_decider.py
├── api/
│   ├── routes/           # FastAPI endpoints
│   │   ├── claims.py     # POST /api/claims/process
│   │   └── health.py     # GET /api/health
│   └── schemas/          # Pydantic models
│       ├── claim_input.py
│       └── claim_output.py
├── core/
│   ├── gemini_client.py  # Dual-auth Gemini client (Vertex AI / API Key)
│   ├── prompts.py        # System prompts for all agents
│   └── file_manager.py   # Multimodal file handling
├── tools/                # Agent tool functions
│   ├── policy_tools.py
│   ├── damage_tools.py
│   ├── fraud_tools.py
│   └── decision_tools.py
├── config.py             # Pydantic Settings
└── main.py               # FastAPI app
ui/
└── gradio_app.py         # Premium Gradio interface
```

### Models Used

| Model | Role | Why |
|:------|:-----|:----|
| `gemini-3.1-pro-preview` | Complex reasoning, policy analysis, fraud detection | Best-in-class structured output and CoT reasoning |
| `gemini-3-flash-preview` | Claim intake, UI interactions | Sub-second latency for real-time UX |

### Authentication

Supports **dual authentication**:

1. **Vertex AI** (recommended): Uses Google Cloud Application Default Credentials + $300 free trial credits
2. **API Key**: Direct Google AI Studio key (fallback)

Configured via `USE_VERTEX_AI=true/false` in `.env`.

---

## 📊 Demo Scenarios

The UI includes 3 pre-built demo scenarios:

| Scenario | Expected Decision | Why |
|:---------|:-----------------|:----|
| 🚗 Auto — Hail Damage | APPROVED or HUMAN_REVIEW | Standard comprehensive claim |
| 🏠 Property — Water Damage | HUMAN_REVIEW | High-value claim, complex assessment |
| 🚑 Auto — Suspicious Rear-End | HUMAN_REVIEW or REJECTED | Multiple fraud red flags |

---

## 🏆 Why "Best Use of Gemini"

1. **Gemini 3.1 Pro**: Latest model with superior structured output and reasoning
2. **Native Multimodality**: PDF + image + text processed simultaneously
3. **JSON Schema Enforcement**: `response_mime_type="application/json"` for validated output
4. **Chain-of-Thought**: Explicit reasoning chains with confidence scoring
5. **Multi-Agent Orchestration**: 5 agents with distinct roles and system prompts
6. **Production-Ready**: Retry logic, error handling, audit trails

---

## 📄 License

MIT License — Built for the AI Agent Olympics Hackathon, Milan AI Week 2026.

---

<p align="center">
  <strong>⚡ OmniClaims Adjuster</strong><br>
  <em>Powered by Gemini 3.1 Pro • Built with ❤️ for the AI Agent Olympics</em>
</p>
