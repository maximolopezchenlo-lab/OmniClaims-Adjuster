import sys
from ui.gradio_app import process_claim_ui, DEMO_SCENARIOS
from dotenv import load_dotenv

load_dotenv()

scenario = list(DEMO_SCENARIOS.keys())[0]
claim_text = DEMO_SCENARIOS[scenario]

print("Running process_claim_ui...")

def fake_progress(*args, **kwargs):
    print(f"Progress: {kwargs.get('desc')}")

try:
    result = process_claim_ui(claim_text, None, None, progress=fake_progress)
    print("Result tuple length:", len(result))
    if "❌ Error" in result[0]:
        print("Error found in result:", result[0])
    else:
        print("Success.")
except Exception as e:
    import traceback
    traceback.print_exc()
