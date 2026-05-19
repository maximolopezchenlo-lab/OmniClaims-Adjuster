"""
Generate realistic sample insurance policy PDFs for demo purposes.

Creates professional-looking policy documents that Gemini can analyze
during the hackathon demonstration.
"""

from fpdf import FPDF
from pathlib import Path
from datetime import date


OUTPUT_DIR = Path("demo_data")
OUTPUT_DIR.mkdir(exist_ok=True)


class PolicyPDF(FPDF):
    """Custom PDF with professional insurance policy styling."""

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(50, 50, 150)
        self.cell(0, 8, "APEX SHIELD INSURANCE CO.", align="L")
        self.cell(0, 8, "Policy Document", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(50, 50, 150)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, f"Apex Shield Insurance Co. | Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(30, 30, 100)
        self.ln(4)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 200, 220)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def section_body(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def clause(self, number: str, text: str):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(50, 50, 50)
        self.cell(15, 6, number)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, text)
        self.ln(1)


def generate_auto_policy():
    """Generate a comprehensive auto insurance policy PDF."""
    pdf = PolicyPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title page
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(30, 30, 100)
    pdf.ln(20)
    pdf.cell(0, 12, "COMPREHENSIVE AUTO", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 12, "INSURANCE POLICY", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "Policy Number: AUT-2026-78432", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Effective Date: January 1, 2026 - December 31, 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Insured: John Martinez", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Vehicle: 2024 Toyota Camry LE", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "VIN: 4T1BF1FK5MU123456", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)

    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "This is a binding contract between the Insured and Apex Shield Insurance Co.", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Read all sections carefully. Contact your agent for questions.", align="C", new_x="LMARGIN", new_y="NEXT")

    # Page 2 - Declarations
    pdf.add_page()
    pdf.section_title("SECTION 1: DECLARATIONS PAGE")
    pdf.section_body(
        "Named Insured: John Martinez\n"
        "Mailing Address: 4521 Elm Street, Dallas, TX 75201\n"
        "Policy Period: January 1, 2026 to December 31, 2026 (12:01 AM Standard Time)\n"
        "Vehicle: 2024 Toyota Camry LE - Silver Metallic\n"
        "VIN: 4T1BF1FK5MU123456\n"
        "Garaging Address: Same as mailing address\n"
        "Primary Use: Personal commuting (< 15,000 miles/year)\n"
        "Annual Premium: $1,847.00 (paid in full)"
    )

    pdf.section_title("SECTION 2: COVERAGE SUMMARY")
    pdf.section_body(
        "A. COMPREHENSIVE COVERAGE (Other Than Collision)\n"
        "   Coverage Limit: $50,000 per occurrence\n"
        "   Deductible: $500\n"
        "   Covers: Fire, theft, vandalism, natural disasters (hail, flood, wind),\n"
        "   falling objects, animal collisions, glass breakage, civil disturbance.\n\n"
        "B. COLLISION COVERAGE\n"
        "   Coverage Limit: $50,000 per occurrence\n"
        "   Deductible: $1,000\n"
        "   Covers: Damage from collision with another vehicle or object,\n"
        "   single-vehicle accidents, rollover events.\n\n"
        "C. LIABILITY COVERAGE\n"
        "   Bodily Injury: $100,000 per person / $300,000 per accident\n"
        "   Property Damage: $50,000 per accident\n\n"
        "D. UNINSURED/UNDERINSURED MOTORIST\n"
        "   Bodily Injury: $100,000 per person / $300,000 per accident\n\n"
        "E. MEDICAL PAYMENTS\n"
        "   Limit: $5,000 per person"
    )

    # Page 3 - Coverage Details
    pdf.add_page()
    pdf.section_title("SECTION 3: COMPREHENSIVE COVERAGE DETAILS")
    pdf.section_body(
        "This section details the perils covered under Comprehensive (Other Than Collision) coverage."
    )

    pdf.clause("3.1", "WEATHER-RELATED DAMAGE: We will pay for direct physical damage to "
               "the covered vehicle caused by hail, windstorm, lightning, flood, earthquake, "
               "or any other natural weather event, subject to the deductible stated in the "
               "Declarations Page ($500).")

    pdf.clause("3.2", "GLASS BREAKAGE: Damage to windshield, windows, and sunroof glass "
               "is covered under comprehensive. Windshield repair may be performed with "
               "no deductible; full replacement is subject to the stated deductible.")

    pdf.clause("3.3", "THEFT AND VANDALISM: Coverage applies to total theft of the vehicle "
               "or damage resulting from attempted theft or vandalism, including keying, "
               "graffiti, and broken windows.")

    pdf.clause("3.4", "FALLING OBJECTS: Damage caused by falling objects including tree "
               "branches, construction debris, or aircraft parts.")

    pdf.clause("3.5", "ANIMAL COLLISION: Damage resulting from collision with an animal "
               "(deer, birds, livestock) is classified as comprehensive, not collision.")

    pdf.clause("3.6", "FIRE AND EXPLOSION: Damage from fire, whether accidental or as a "
               "result of mechanical failure, and explosion damage.")

    pdf.clause("3.7", "CIVIL DISTURBANCE: Damage caused by riots, civil commotion, or "
               "malicious mischief by parties other than the insured.")

    # Page 4 - Exclusions
    pdf.add_page()
    pdf.section_title("SECTION 4: EXCLUSIONS")
    pdf.section_body(
        "The following are specifically excluded from coverage under this policy:"
    )

    pdf.clause("4.1", "INTENTIONAL DAMAGE: Any loss or damage intentionally caused by the "
               "insured, a family member, or any person acting at the direction of the insured. "
               "This includes but is not limited to arson, deliberate destruction, or staging "
               "an accident for the purpose of collecting insurance proceeds.")

    pdf.clause("4.2", "RACING AND COMPETITION: Damage occurring while the vehicle is being "
               "used in any organized or informal racing event, speed contest, demolition derby, "
               "stunt activity, or track day event.")

    pdf.clause("4.3", "COMMERCIAL USE: Damage occurring while the vehicle is being used for "
               "commercial purposes including but not limited to ride-sharing (Uber, Lyft), "
               "delivery services, or as a taxi/livery vehicle, unless a commercial endorsement "
               "is attached to this policy.")

    pdf.clause("4.4", "WAR AND TERRORISM: Loss or damage caused by war (declared or undeclared), "
               "civil war, insurrection, rebellion, revolution, terrorism, or nuclear hazard.")

    pdf.clause("4.5", "MECHANICAL BREAKDOWN: Normal wear and tear, mechanical or electrical "
               "breakdown, or failure of any part or system of the vehicle, unless directly "
               "caused by a covered peril.")

    pdf.clause("4.6", "UNAUTHORIZED DRIVERS: Damage occurring while the vehicle is operated "
               "by any person not listed on this policy, unless the insured has given express "
               "permission for that person to operate the vehicle.")

    pdf.clause("4.7", "PRE-EXISTING DAMAGE: Any damage that existed prior to the inception "
               "date of this policy or prior to the reported date of loss.")

    # Page 5 - Claims Procedures
    pdf.add_page()
    pdf.section_title("SECTION 5: CLAIMS PROCEDURES")

    pdf.clause("5.1", "REPORTING: The insured must report any loss or damage to Apex Shield "
               "within 72 hours of the incident. Failure to report within this timeframe may "
               "result in denial of the claim.")

    pdf.clause("5.2", "DOCUMENTATION: The insured must provide: (a) a completed claim form, "
               "(b) a detailed description of the incident, (c) photographs of the damage, "
               "(d) a police report if applicable, (e) repair estimates from two licensed facilities.")

    pdf.clause("5.3", "INSPECTION: Apex Shield reserves the right to inspect the damaged vehicle "
               "before authorizing repairs. The company may designate a preferred repair facility.")

    pdf.clause("5.4", "PAYMENT: Upon approval, payment will be calculated as follows:\n"
               "   Payout = MIN(Actual Repair Cost, Coverage Limit) - Deductible\n"
               "   Payment will be issued within 15 business days of claim approval.")

    pdf.clause("5.5", "DISPUTE RESOLUTION: Any disputes regarding claim valuation or denial "
               "shall be resolved through binding arbitration in accordance with the laws "
               "of the State of Texas.")

    pdf.section_title("SECTION 6: GENERAL CONDITIONS")

    pdf.clause("6.1", "POLICY PERIOD: This policy is effective from January 1, 2026 through "
               "December 31, 2026. Coverage applies only to incidents occurring within this period.")

    pdf.clause("6.2", "TERRITORY: Coverage applies within the United States, its territories, "
               "and Canada.")

    pdf.clause("6.3", "SUBROGATION: Upon payment of a claim, Apex Shield acquires the right "
               "to recover the amount paid from any responsible third party.")

    pdf.clause("6.4", "CANCELLATION: Either party may cancel this policy with 30 days written notice.")

    # Save
    output_path = OUTPUT_DIR / "sample_policy_auto_AUT-2026-78432.pdf"
    pdf.output(str(output_path))
    print(f"Generated: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
    return output_path


def generate_property_policy():
    """Generate a homeowner's property insurance policy PDF."""
    pdf = PolicyPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(30, 30, 100)
    pdf.ln(20)
    pdf.cell(0, 12, "HOMEOWNER'S PROPERTY", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 12, "INSURANCE POLICY", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "Policy Number: HOM-2026-55901", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Effective: January 1, 2026 - December 31, 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Insured: Sarah Chen", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Property: 782 Oak Lane, Austin, TX 78704", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.add_page()
    pdf.section_title("SECTION 1: DECLARATIONS")
    pdf.section_body(
        "Named Insured: Sarah Chen\n"
        "Property Address: 782 Oak Lane, Austin, TX 78704\n"
        "Construction: Wood Frame, 2-Story, Built 2019\n"
        "Square Footage: 2,400 sq ft\n"
        "Annual Premium: $2,340.00"
    )

    pdf.section_title("SECTION 2: COVERAGE SUMMARY")
    pdf.section_body(
        "A. DWELLING COVERAGE\n"
        "   Limit: $450,000 | Deductible: $1,000\n"
        "   Covers structural damage from covered perils.\n\n"
        "B. PERSONAL PROPERTY\n"
        "   Limit: $225,000 (50% of dwelling) | Deductible: $500\n\n"
        "C. WATER DAMAGE - INTERNAL\n"
        "   Covered: Burst pipes, appliance leaks, accidental discharge.\n"
        "   Limit: $75,000 per occurrence | Deductible: $1,000\n"
        "   Note: Gradual seepage or maintenance-related water damage is EXCLUDED.\n\n"
        "D. LIABILITY\n"
        "   $300,000 per occurrence | $500,000 aggregate"
    )

    pdf.section_title("SECTION 3: EXCLUSIONS")
    pdf.section_body(
        "3.1 FLOOD: External flooding is excluded unless a separate flood endorsement is purchased.\n"
        "3.2 EARTHQUAKE: Not covered under standard policy.\n"
        "3.3 NEGLECT/MAINTENANCE: Damage due to failure to maintain the property.\n"
        "3.4 GRADUAL WATER DAMAGE: Slow leaks, seepage, or condensation over time.\n"
        "3.5 MOLD: Mold remediation is limited to $10,000 per occurrence.\n"
        "3.6 INTENTIONAL ACTS: Damage intentionally caused by the insured."
    )

    pdf.section_title("SECTION 4: CLAIMS")
    pdf.section_body(
        "4.1 Report within 48 hours. Provide photos, receipts, and contractor estimates.\n"
        "4.2 Payout = MIN(Repair Cost, Coverage Limit) - Deductible.\n"
        "4.3 Apex Shield may send an adjuster before approving repairs."
    )

    output_path = OUTPUT_DIR / "sample_policy_home_HOM-2026-55901.pdf"
    pdf.output(str(output_path))
    print(f"Generated: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
    return output_path


if __name__ == "__main__":
    print("Generating demo policy PDFs...")
    generate_auto_policy()
    generate_property_policy()
    print("Done!")
