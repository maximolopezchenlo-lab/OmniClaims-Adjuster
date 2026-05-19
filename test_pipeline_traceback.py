import sys
from app.agents.orchestrator import OrchestratorAgent
from ui.gradio_app import DEMO_SCENARIOS
from dotenv import load_dotenv

load_dotenv()

scenario = list(DEMO_SCENARIOS.keys())[0]
claim_text = DEMO_SCENARIOS[scenario]

print("Running Orchestrator...")
orchestrator = OrchestratorAgent()

try:
    result = orchestrator.process_claim(claim_text=claim_text, policy_file_path=None, evidence_file_paths=None)
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
