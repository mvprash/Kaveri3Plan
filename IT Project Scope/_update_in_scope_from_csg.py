# -*- coding: utf-8 -*-
"""Update In Scope IS-03 / IS-06 from CSG Documents FRS only (no RFP).

Sources (CSG Documents/FRS Documents):
  - FRS - Kaveri 2.0 v0.2.38 8.docx
  - Paperless registration-I FRS.docx
  - Firm registration FRS V1.7.docx
  - Re-registration FRS v1.4.pdf
  - Will after the death of the testator FRS 1.1.docx
  - K1 pending document_FRS_ V1.1.docx
  - SRO Round-robin for pre-registration.docx
  - GIS based valuation FRS v2.1.docx
  - Book 1 Rule 17 (3) Module FRS V.01.docx
  - Book I_Part III(b) Filing_FRS.docx
  - Book-I Part-I Other Memo Filing FRS V1.1.docx

Writes:
  IT Project Scope/IT_Project_Scope_Document_v1.3.docx
  and refreshes Template1.docx
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from docx import Document

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"E:\MVP\Kaveri 3.0\Source Code\Kaveri 3 Plan")
SCOPE_DIR = ROOT / "IT Project Scope"
SRC = SCOPE_DIR / "IT_Project_Scope_Document_Template1.docx"
# Prefer latest versioned file if Template1 is locked
FALLBACK = SCOPE_DIR / "IT_Project_Scope_Document_v1.2.docx"
OUT = SCOPE_DIR / "IT_Project_Scope_Document_v1.3.docx"
CSG_COPY = ROOT / "CSG Documents" / "IT Project Scope" / "IT_Project_Scope_Document_v1.3.docx"

DOC_REG_LINES = [
    "2 types of registration flows – Paper and Paperless.",
    "Paper – ink-signed deed, physical presentation, scan & store after registration.",
    "Paperless – digital execution (e-Sign / DSC), biometric e-KYC and digital endorsements (Paperless registration-I FRS).",
    "",
    "Application has to support both Online and Offline Process.",
    "Online – via Kaveri Application / Portal.",
    "Offline – at SRO; data entry and registration by SRO / FDA / SDA / DEO.",
    "",
    "Citizen / pre-registration flow (FRS – Kaveri 2.0):",
    "Type of Document – Sale, Mortgage, Lease, DoT, Reconveyance, Partition, Release, Gift, Exchange, Settlement, Agreement, GPA, Will, and other articles.",
    "Property Search – Bhoomi, e-Swathu, e-Aasthi and aligned property databases; Property Schedule.",
    "Market Valuation and Fee Calculation (incl. GIS-based agri valuation per GIS FRS v2.1).",
    "Party Information; Document Summary; SRO Confirmation / pre-registration scrutiny.",
    "Payment (incl. e-Stamp / challan) and Appointment Scheduler.",
    "Anywhere registration with Round-robin SRO allocation for pre-registration scrutiny (SRO Round-robin FRS).",
    "",
    "Department registration flow:",
    "Department login & dashboard; Application allocation to DEO.",
    "Biometric capture (photo / thumb); Aadhaar biometric e-KYC where Aadhaar is POI.",
    "Digital / ink endorsements; Section 60 certificate; unique registration number.",
    "Scan, upload and digitally sign registered document; J-slip to Bhoomi for agricultural property.",
    "Outcomes – Register / Keep Pending / Withdraw / Refuse / Send back to DEO.",
    "",
    "Extended Document Registration capabilities (CSG FRS suite):",
    "Paperless registration – digital execution after scrutiny; merged deed + thumb register e-signed by parties and SR.",
    "Re-registration of refused documents on DR / Court order (Re-registration FRS).",
    "Kaveri-1 pending document release and continuation in Kaveri 2.0 (K1 pending document FRS).",
    "Registration of Wills after death of the testator (Book No. 3).",
    "Book-I filing – Part-I Other Memo, Part III(b), Rule 17(3) communications from other departments.",
    "Exceptional cases – delay condonation, private attendance, undervaluation / impound, PoA presentation, late appearance, etc. (as in master FRS).",
    "Court Order Entry, Liability, Cross Reference, Sec. 68(2) Correction, Filing Document modules supporting registration.",
    "",
    "Boundary: Encumbrance Certificate (IS-04), Certified Copy (IS-05) and Digital E-Stamp issue (IS-07) are separate In-Scope items. Firm filing at DRO is IS-06.",
]

FIRM_REG_LINES = [
    "Firm services (Firm registration FRS V1.7):",
    "New Firm Registration",
    "Amendment – firm name / principal place of business; other places of business; partner name / address; notice of election on attaining majority",
    "Reconstitution – incoming / outgoing partner",
    "Dissolution of Firm",
    "Protest Entry against Register of Firms entry",
    "Index Search of registered firms",
    "Certified Copy of Register of Firms entries / related forms",
    "",
    "Application has to support both Online and Offline Process.",
    "Online – via Kaveri Application / Portal.",
    "Offline – at District Registrar Office (DRO); registration / approval by District Registrar.",
    "",
    "Two-step linkage with Document Registration (IS-03):",
    "1. Partnership / reconstitution / dissolution deed registered at SRO (document registration flow).",
    "2. Firm filing at DRO under the Indian Partnership Act, 1932 (as described in Firm FRS).",
    "",
    "Core capabilities:",
    "Firm name and address uniqueness search; block duplicate / objectionable names (Emblems and Names Act list).",
    "Fee calculation; acknowledgement and fee receipt.",
    "Unique Firm Registration Number; update Register of Firms and its Index.",
    "Print Certificate of Registration / endorsements (e.g. Form C) as per application type.",
    "Scan and upload of application attachments (Form I, partnership deed copy, declaration, ID / address proof).",
    "A-Register accounting entry; MIS reports; DRO checklist for scrutiny.",
    "Integrations – DigiLocker / e-Sign; SAKALA; Aadhaar dependency; Kaveri-1 to Kaveri-2 firm data migration.",
    "",
    "Boundary: Firm module at DRO. Deed registration itself is under IS-03 Document Registration. Society Registration is out of this item.",
    "Limitation (per Firm FRS): Form C of Kaveri-1 firms shown as-is; full Form I–VI / Form A for Kaveri-1 firms not available.",
]


def set_cell_lines(cell, lines: list[str]) -> None:
    if not cell.paragraphs:
        cell.add_paragraph()
    for p in cell.paragraphs[1:]:
        p._element.getparent().remove(p._element)
    first = cell.paragraphs[0]
    for r in list(first.runs):
        r._element.getparent().remove(r._element)
    if lines:
        first.add_run(lines[0])
        for line in lines[1:]:
            cell.add_paragraph(line)
    else:
        first.add_run("")


def find_row(table, scope_id: str):
    for row in table.rows:
        if row.cells[0].text.strip() == scope_id:
            return row
    raise KeyError(scope_id)


def main() -> None:
    base = SRC if SRC.exists() else FALLBACK
    if not base.exists():
        raise SystemExit(f"No base document found: {SRC} or {FALLBACK}")

    shutil.copy2(base, OUT)
    doc = Document(str(OUT))
    table = doc.tables[0]
    set_cell_lines(find_row(table, "IS-03").cells[2], DOC_REG_LINES)
    set_cell_lines(find_row(table, "IS-06").cells[2], FIRM_REG_LINES)
    doc.save(str(OUT))

    # Refresh Template1 if writable
    try:
        shutil.copy2(OUT, SRC)
        tpl_msg = f"Updated: {SRC}"
    except PermissionError:
        tpl_msg = f"Skipped Template1 (locked): {SRC}"

    # Also keep CSG Documents copy in sync
    CSG_COPY.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUT, CSG_COPY)

    verify = Document(str(OUT))
    for sid in ("IS-03", "IS-06"):
        for row in verify.tables[0].rows:
            if row.cells[0].text.strip() == sid:
                text = row.cells[2].text
                print(f"=== {sid} ({len(text)} chars) ===")
                print(text[:400], "...\n")
                break

    print(f"Saved: {OUT}")
    print(f"Copied: {CSG_COPY}")
    print(tpl_msg)


if __name__ == "__main__":
    main()
