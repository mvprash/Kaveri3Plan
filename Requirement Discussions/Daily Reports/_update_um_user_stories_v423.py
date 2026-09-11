# -*- coding: utf-8 -*-
"""Update 25-08-2026 daily report and consolidated doc user stories
from Finalized BRD/User Management/BRD_User_Management_v4.23.docx.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(
    r"E:\MVP\Kaveri 3.0\Source Code\Kaveri 3 Plan\Requirement Discussions\Daily Reports"
)
UM_25 = BASE / "user_management_requirement_25082026.docx"
CONSOL_SCRIPT = BASE / "_make_consolidated_daily_requirements.py"
BRD_REF = "Finalized BRD/User Management/BRD_User_Management_v4.23.docx"

# ID | Actor | Story | Acceptance — aligned to BRD v4.23 (section 4.5.2 / 4.6.6 / §6)
USER_STORIES: list[tuple[str, str, str, str]] = [
    (
        "US-LG-01",
        "Citizen",
        "As a Citizen, I need to log in with my Username + Captcha + OTP sent only to my registered mobile, with no password option, so that I can access KAVERI securely.",
        "FR-UM-005, FR-UM-009, FR-UM-010, FR-UM-011",
    ),
    (
        "US-LG-02",
        "DSR Officer",
        "As a DSR Officer, I need to log in with my KGID + Captcha + Face authentication or Biometrics (no OTP and no password), so that I can access the office application.",
        "FR-UM-006, FR-UM-009",
    ),
    (
        "US-LG-03",
        "Other Department user",
        "As an Other Department user, I need to log in with my Username (Department Code concatenated with Employee ID or KGID) + Captcha + OTP (no biometrics), so that I can access my allotted modules.",
        "FR-UM-007, FR-UM-009",
    ),
    (
        "US-PS-01",
        "DSR Officer",
        'As a DSR Officer with more than one active sanctioned-post occupancy, I need to select exactly one assigned post labelled "Role — Post Name — Office Name (Office Code)" after authentication (auto-select if only one), so that session Module Function claims come from that assigned post only.',
        "FR-UM-052, FR-UM-038",
    ),
    (
        "US-AC-01",
        "DSR Officer",
        "As a DSR Officer already logged in under my assigned post, I need to take additional charge of a wholly unoccupied subordinate post at the same office without logout, switch back to assigned-post context when needed, and see the active context in the header, so that I can cover vacant desks for the session without retaining assigned-post privileges while in additional charge.",
        "FR-UM-053, FR-UM-054, FR-UM-066(b)",
    ),
    (
        "US-CR-01",
        "Citizen",
        "As a Citizen, I need to self-register instantly (preferred Username availability check, email OTP, mobile OTP, and mandatory Aadhaar e-KYC) with no approval workflow, so that I can start using the portal without delay.",
        "FR-UM-001, FR-UM-062, FR-UM-063, FR-UM-085",
    ),
    (
        "US-CR-02",
        "Authorised administrator",
        "As an authorised administrator, I need to create DSR Officers and Other Department users instantly without maker-checker, assigning at least one sanctioned post with available capacity for DSR Officers (no Primary/Secondary role distinction) or exactly one Other Department role, so that onboarding is not delayed.",
        "FR-UM-002, FR-UM-003, FR-UM-017, FR-UM-029, FR-UM-030, FR-UM-051",
    ),
    (
        "US-RM-01",
        "Application Admin",
        "As Application Admin, I need to maintain a single unified Role Master and User Master (differentiated by Role Category / User Category), with unique role names, abbreviations as displayed via Post–Role mapping, and hierarchy via the DSR Officer Hierarchy Master, so that access and reporting lines stay configurable.",
        "FR-UM-016, FR-UM-028, FR-UM-034, FR-UM-035, FR-UM-043, FR-UM-047",
    ),
    (
        "US-TO-01",
        "Hierarchy superior",
        "As a hierarchy superior (within office span and immediate-parent post parentage), I need to relieve a subordinate from a post occupancy capturing Relieving Date, enumerated Relieving Reason, and Relieving Order (number / upload), so that Transfer Out is auditable and occupancy ends after the Relieving Date via the midnight refresh job.",
        "FR-UM-057, FR-UM-058, FR-UM-068, FR-UM-087",
    ),
    (
        "US-TI-01",
        "Hierarchy superior",
        "As a hierarchy superior, I need to Transfer In an officer to a Post + Office that already has available capacity, capturing Transfer / Reporting Order (immediate effect; no Joining Date), so that the officer can select that post at the next login.",
        "FR-UM-060, FR-UM-066(a)",
    ),
    (
        "US-RP-01",
        "Management / Admin",
        "As management, I need login-attempt audit reports (successful and failed) over a selected date range, plus role/permission, sanctioned-post occupancy, additional-charge, and Transfer Out/In history reports, so that access and establishment can be monitored.",
        "BRD §6 Reporting Requirements; FR-UM-053; FR-UM-057–FR-UM-060",
    ),
    (
        "US-TA-01",
        "District Registrar",
        "As District Registrar of DRO Bengaluru, I need to record Leave for the Sub-Registrar of SRO Yeshwanthapura (SRO A) from 01-Sep-2026 to 05-Sep-2026 so that the officer cannot access KAVERI during that period.",
        "FR-UM-079, FR-UM-080",
    ),
    (
        "US-TA-02",
        "District Registrar",
        "As the same District Registrar, I need to give temporary charge of SRO Yeshwanthapura (SRO A) Sub-Registrar work to the Sub-Registrar of SRO Jayanagar (SRO B) under my district for the leave period so that SRO A work continues.",
        "FR-UM-082, FR-UM-083",
    ),
    (
        "US-TA-03",
        "AIGR (Admin)",
        "As AIGR (Admin), I need to record OOD / Leave for District Registrar of DRO Mysuru and assign temporary charge of that DRO post to the District Registrar of DRO Bengaluru (another district under me) so that DRO Mysuru work continues.",
        "FR-UM-079, FR-UM-082",
    ),
    (
        "US-TA-04",
        "Covering Sub-Registrar",
        "As Sub-Registrar of SRO B holding temporary charge of SRO A, I need to log in and choose whether to work as SR of B or under temporary charge of A.",
        "FR-UM-052 lists both; one context; FR-UM-083",
    ),
]

NOTE = (
    "User stories aligned to BRD_User_Management_v4.23 (Login / RBAC / Temporary Absence / Reporting). "
    "Format: ID | Actor | Story | Acceptance (system) — same pattern as BRD §4.6.6. "
    "KT notes on Primary/Secondary roles, password+OTP for all categories, and biometric refresh every 5 years "
    "are superseded by FR-UM-017/030 (no Primary/Secondary), FR-UM-005–007/009 (category-specific auth, no password), "
    "and FR-UM-006 (DSR face/biometric without OTP)."
)


def set_run_font(run, size=10, bold=False, font="Times New Roman", color=None):
    run.bold = bold
    run.font.name = font
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font)
    run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color


def shade_header(table):
    for cell in table.rows[0].cells:
        tc_pr = cell._tc.get_or_add_tcPr()
        shd = tc_pr.makeelement(
            qn("w:shd"),
            {
                qn("w:val"): "clear",
                qn("w:color"): "auto",
                qn("w:fill"): "1F4E79",
            },
        )
        tc_pr.append(shd)
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.bold = True


def add_stories_table(doc: Document) -> None:
    p = doc.add_paragraph()
    r = p.add_run("User Stories")
    set_run_font(r, size=14, bold=True, font="Segoe UI", color=RGBColor(0x1F, 0x4E, 0x79))

    p2 = doc.add_paragraph()
    r2 = p2.add_run(NOTE)
    set_run_font(r2, size=10, font="Segoe UI")

    p3 = doc.add_paragraph()
    r3 = p3.add_run(f"Source: {BRD_REF}")
    set_run_font(r3, size=9.5, bold=True, font="Segoe UI")

    headers = ["ID", "Actor", "Story", "Acceptance (system)"]
    table = doc.add_table(rows=1 + len(USER_STORIES), cols=4)
    # Prefer an existing table style from the source doc (some daily notes lack "Table Grid").
    if doc.tables:
        try:
            style_name = doc.tables[0].style.name if doc.tables[0].style else None
            if style_name:
                table.style = style_name
        except (KeyError, AttributeError, ValueError):
            pass
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        run = cell.paragraphs[0].add_run(h)
        set_run_font(run, size=10, bold=True)
    for ri, row in enumerate(USER_STORIES, start=1):
        for ci, val in enumerate(row):
            cell = table.rows[ri].cells[ci]
            cell.text = ""
            run = cell.paragraphs[0].add_run(val)
            set_run_font(run, size=9)
    shade_header(table)
    for row in table.rows:
        row.cells[0].width = Inches(0.9)
        row.cells[1].width = Inches(1.3)
        row.cells[2].width = Inches(3.4)
        row.cells[3].width = Inches(1.6)


def update_25_08() -> None:
    doc = Document(str(UM_25))
    # Remove previously appended User Stories if re-run
    # Detect by scanning paragraphs for heading "User Stories"
    # Simpler: if last paragraphs already contain US-LG-01, rebuild from original body
    # by truncating after last original content. Original file had no User Stories.
    texts = [p.text.strip() for p in doc.paragraphs]
    if any(t.startswith("User Stories") for t in texts) or any(
        "US-LG-01" in t for t in texts
    ):
        # Drop trailing user-stories paragraphs added previously; keep tables + original paras
        # Rebuild: copy until before first "User Stories" heading
        # Easiest reliable approach: re-extract from known original content via zip if needed.
        # Instead: clear body elements after meta+discussion by rewriting from scratch of known original.
        pass

    # If document already has our stories table, remove from "User Stories" onward
    body = doc.element.body
    children = list(body)
    cut_from = None
    # Walk paragraphs in document order via body children
    from docx.oxml.ns import qn as _qn

    for idx, child in enumerate(children):
        if child.tag != _qn("w:p"):
            continue
        texts_runs = [
            (t.text or "")
            for t in child.findall(".//" + _qn("w:t"))
        ]
        text = "".join(texts_runs).strip()
        if text == "User Stories" or text.startswith("User stories aligned to BRD_User_Management"):
            cut_from = idx
            break
        if text.startswith("US-LG-01") or text.startswith("US-UM-01"):
            cut_from = idx
            break

    if cut_from is not None:
        for child in children[cut_from:]:
            # keep sectPr
            if child.tag == _qn("w:sectPr"):
                continue
            body.remove(child)

    # Also remove any leftover tables that only contain user-story headers after cut
    # (if cut landed mid-table, tables after are removed with children)

    add_stories_table(doc)
    doc.save(str(UM_25))
    print(f"Updated {UM_25.name}")


def patch_consolidated_script() -> None:
    src = CONSOL_SCRIPT.read_text(encoding="utf-8")

    # Replace section 1.4 User stories block through end of stories loop
    pattern = re.compile(
        r'    add_heading_custom\(doc, "1\.4 User stories", level=2\).*?'
        r"    for s in stories_2508:\n"
        r"        add_story\(doc, \*s\)\n",
        re.DOTALL,
    )

    replacement = '''    add_heading_custom(doc, "1.4 User stories", level=2)
    add_para(
        doc,
        "Aligned to BRD_User_Management_v4.23 (Login / RBAC / Temporary Absence / Reporting). "
        "Format matches BRD §4.6.6: ID | Actor | Story | Acceptance (system). "
        "KT notes on Primary/Secondary roles, password+OTP for all categories, and biometric "
        "refresh every 5 years are superseded by FR-UM-017/030, FR-UM-005–007/009, and FR-UM-006.",
        size=10,
        space_after=6,
    )
    add_para(
        doc,
        "Source: Finalized BRD/User Management/BRD_User_Management_v4.23.docx",
        size=9.5,
        bold=True,
        space_after=8,
    )
    add_table(
        doc,
        ["ID", "Actor", "Story", "Acceptance (system)"],
        [
'''

    rows_py = []
    for sid, actor, story, acc in USER_STORIES:
        # escape for Python string
        def esc(s: str) -> str:
            return s.replace("\\", "\\\\").replace('"', '\\"')

        rows_py.append(
            f'            ["{esc(sid)}", "{esc(actor)}", "{esc(story)}", "{esc(acc)}"],'
        )
    replacement += "\n".join(rows_py)
    replacement += """
        ],
        col_widths=[0.9, 1.3, 3.4, 1.6],
    )
"""

    new_src, n = pattern.subn(replacement, src, count=1)
    if n != 1:
        raise RuntimeError(f"Failed to patch consolidated script (matches={n})")

    # Update appendix note about user stories sources
    new_src = new_src.replace(
        "User stories for 25-08, 27-08, 28-08 and 07–08 Sep were derived from discussion sections / Acts-Rules where the source notes did not include a User Stories section; 01-09 and 02-09 user stories are taken from the source documents.",
        "User stories for 25-08 are aligned to BRD_User_Management_v4.23 (ID | Actor | Story | Acceptance). "
        "User stories for 27-08, 28-08 and 07–08 Sep were derived from discussion sections / Acts-Rules where the source notes did not include a User Stories section; 01-09 and 02-09 user stories are taken from the source documents.",
    )

    CONSOL_SCRIPT.write_text(new_src, encoding="utf-8")
    print(f"Patched {CONSOL_SCRIPT.name}")


def main() -> None:
    patch_consolidated_script()
    update_25_08()


if __name__ == "__main__":
    main()
