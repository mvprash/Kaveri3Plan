# -*- coding: utf-8 -*-
"""Build one date-wise consolidated requirement discussion document from:

  - user_management_requirement_25082026.docx
  - Document_Registration_requirement_27082026_v1.1.docx
  - Document_Registration_requirement_28082026_v1.1.docx
  - Document_Registration_requirement_01092026_v2.docx
  - Document_Registration_requirement_02092026_v1.1.docx
  - Document_Registration_requirement_07092026_v1.1.docx
  - Document_Registration_requirement_08092026_v1.1.docx
  - Document_Registration_requirement_09092026_v1.1.docx
  - Document_Registration_requirement_11092026_v1.1.docx

Includes: discussion topics, sections, rules, notifications, pain points,
user stories. Excludes business re-engineering.
"""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(
    r"E:\MVP\Kaveri 3.0\Source Code\Kaveri 3 Plan\Requirement Discussions\Daily Reports"
)
OUT = BASE / "Consolidated_Requirement_Discussions_25082026_to_11092026.docx"
LEGACY_OUT = BASE / "Consolidated_Requirement_Discussions_25082026_to_08092026.docx"
OUT_FALLBACK = BASE / "Consolidated_Requirement_Discussions_25082026_to_11092026_v2.docx"

FONT = "Segoe UI"
TITLE_FONT = "Segoe UI"


def set_run_font(run, size=11, bold=False, color=None, font=FONT):
    run.bold = bold
    run.font.name = font
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font)
    run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color


def add_para(doc, text="", *, size=11, bold=False, space_after=6, space_before=0, align=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    if align is not None:
        p.alignment = align
    if text:
        run = p.add_run(text)
        set_run_font(run, size=size, bold=bold)
    return p


def add_heading_custom(doc, text, level=1):
    sizes = {1: 18, 2: 14, 3: 12.5, 4: 11.5}
    colors = {
        1: RGBColor(0x1F, 0x4E, 0x79),
        2: RGBColor(0x2E, 0x75, 0xB6),
        3: RGBColor(0x2F, 0x54, 0x96),
        4: RGBColor(0x40, 0x40, 0x40),
    }
    p = add_para(
        doc,
        text,
        size=sizes.get(level, 11),
        bold=True,
        space_before=14 if level <= 2 else 8,
        space_after=6,
    )
    for run in p.runs:
        run.font.color.rgb = colors.get(level, RGBColor(0, 0, 0))
    return p


def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        set_run_font(r1, size=10.5, bold=True)
        r2 = p.add_run(text)
        set_run_font(r2, size=10.5)
    else:
        r = p.add_run(text)
        set_run_font(r, size=10.5)
    return p


def add_story(doc, sid, actor, want, so_that):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.space_before = Pt(2)
    r0 = p.add_run(f"{sid}. ")
    set_run_font(r0, size=10.5, bold=True)
    article = "an" if actor[:1].lower() in "aeiou" else "a"
    r1 = p.add_run(f"As {article} {actor}, I want to {want}, so that {so_that}.")
    set_run_font(r1, size=10.5)


def shade_header_row(table, hex_color="1F4E79"):
    for cell in table.rows[0].cells:
        tc_pr = cell._tc.get_or_add_tcPr()
        shd = tc_pr.makeelement(
            qn("w:shd"),
            {
                qn("w:val"): "clear",
                qn("w:color"): "auto",
                qn("w:fill"): hex_color,
            },
        )
        tc_pr.append(shd)
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.bold = True


def add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        run = cell.paragraphs[0].add_run(h)
        set_run_font(run, size=10, bold=True, font="Times New Roman")
    for ri, row in enumerate(rows, start=1):
        for ci, value in enumerate(row):
            cell = table.rows[ri].cells[ci]
            cell.text = ""
            run = cell.paragraphs[0].add_run(str(value))
            set_run_font(run, size=9.5, font="Times New Roman")
    shade_header_row(table)
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)
    doc.add_paragraph()
    return table


def add_meta_table(doc, rows):
    add_table(doc, ["Field", "Details"], rows, col_widths=[1.6, 5.2])


def page_break(doc):
    doc.add_page_break()


def build():
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

    # ----- Cover -----
    add_para(
        doc,
        "KAVERI 3.0 — Requirement Discussions",
        size=12,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
    )
    add_para(
        doc,
        "Consolidated Daily Requirement Notes",
        size=20,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
    )
    add_para(
        doc,
        "25-08-2026 to 11-09-2026",
        size=14,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=12,
    )
    add_para(
        doc,
        "Date-wise consolidation of discussion topics, sections, Acts/Rules, "
        "notifications, ServiceDesk pain points, and user stories. "
        "Business re-engineering content is excluded.",
        size=10.5,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=10,
    )

    add_heading_custom(doc, "Sources", level=2)
    sources = [
        "Requirement Discussions/Daily Reports/user_management_requirement_25082026.docx",
        "Requirement Discussions/Daily Reports/Document_Registration_requirement_27082026_v1.1.docx",
        "Requirement Discussions/Daily Reports/Document_Registration_requirement_28082026_v1.1.docx",
        "Requirement Discussions/Daily Reports/Document_Registration_requirement_01092026_v2.docx",
        "Requirement Discussions/Daily Reports/Document_Registration_requirement_02092026_v1.1.docx",
        "Requirement Discussions/Daily Reports/Document_Registration_requirement_07092026_v1.1.docx",
        "Requirement Discussions/Daily Reports/Document_Registration_requirement_08092026_v1.1.docx",
        "Requirement Discussions/Daily Reports/Document_Registration_requirement_09092026_v1.1.docx",
        "Requirement Discussions/Daily Reports/Document_Registration_requirement_11092026_v1.1.docx",
    ]
    for s in sources:
        add_bullet(doc, s)

    add_heading_custom(doc, "Document contents by date", level=2)
    add_table(
        doc,
        ["Date", "Module / Topics"],
        [
            ["25-08-2026", "User Login, Role Management & Access Control (KT session)"],
            [
                "27-08-2026",
                "Registration core: Registration, Appointment, Status tracking",
            ],
            [
                "28-08-2026",
                "Registration core (continued): SR workflow, slot, payment, stamp / guidance value, impound",
            ],
            [
                "01-09-2026",
                "Guideline value calculation, Valuation Module (CVC) and GIS valuation",
            ],
            [
                "02-09-2026",
                "Rule 17(1)/(2)/(3) filing, Old pending release, Govt/Institutional e-filing",
            ],
            [
                "07-09-2026 to 08-09-2026",
                "Registration Appeal; Will after the death of the testator",
            ],
            [
                "08-09-2026 (Sr.18)",
                "Sec. 68(2) correction; Cross-reference Rule 123",
            ],
            [
                "09-09-2026 to 10-09-2026 (Sr.19)",
                "Integration module; Integration exemption; Court entry; Liability",
            ],
            [
                "11-09-2026",
                "Investigation and Search; Verify Document (registered document / digital e-stamp)",
            ],
        ],
        col_widths=[1.3, 5.5],
    )

    # =====================================================================
    # 25-08-2026 — User Management
    # =====================================================================
    page_break(doc)
    add_heading_custom(doc, "1. 25-08-2026 — User Management", level=1)
    add_meta_table(
        doc,
        [
            ["Date", "25-08-2026"],
            ["Topics", "User Login, Role Management & Access Control (KT session)"],
            [
                "Attendees",
                "Kaveri IT Cell, AIGR Comp, Project Manager, Assistant Manager (CMS)",
            ],
            ["Source", "user_management_requirement_25082026.docx"],
        ],
    )

    add_heading_custom(doc, "1.1 Discussion sections", level=2)

    add_heading_custom(doc, "1. Login & Authentication", level=3)
    add_bullet(
        doc,
        "Password option to be removed. Login will require only user ID, OTP generation, and captcha; user is allowed to log in only when all three match.",
        bold_prefix="Password Removal: ",
    )
    add_bullet(
        doc,
        "Department users will have the option to log in using biometric authentication. Biometric authentication is to be updated every 5 years.",
        bold_prefix="Biometric Authentication: ",
    )

    add_heading_custom(doc, "2. Role Selection & Switching", level=3)
    add_bullet(
        doc,
        "Once logged in, the user is allowed to select a role from the available list; actions and activities must get updated accordingly.",
        bold_prefix="Role Selection Post-Login: ",
    )
    add_bullet(
        doc,
        "User can switch to any of the assigned roles whenever needed.",
        bold_prefix="Role Switching: ",
    )

    add_heading_custom(doc, "3. Primary & Secondary Roles", level=3)
    add_bullet(
        doc,
        "A primary role must be assigned to the user at the time of account creation. Primary role cannot have an end date.",
        bold_prefix="Primary Role: ",
    )
    add_bullet(
        doc,
        "All additional roles will be treated as secondary roles, and all secondary roles must have an end date.",
        bold_prefix="Secondary Roles: ",
    )
    add_bullet(
        doc,
        "After the end date, the secondary role access must be removed from the user's access.",
        bold_prefix="Access Removal: ",
    )

    add_heading_custom(doc, "4. Role Change & Approval", level=3)
    add_bullet(
        doc,
        "For any additional role access, provision is needed to capture the approval letter.",
        bold_prefix="Additional Role Approval: ",
    )
    add_bullet(
        doc,
        "Primary role access can be changed at any time in the future, but an approval letter is needed.",
        bold_prefix="Primary Role Change: ",
    )
    add_bullet(
        doc,
        "Change of primary role access can be due to promotion, office transfer, or demotion – provision needed to capture the changed role.",
        bold_prefix="Reason for Change: ",
    )
    add_bullet(
        doc,
        "Provision needed to set the change of role to an effective date in the future as well.",
        bold_prefix="Future Effective Date: ",
    )

    add_heading_custom(doc, "5. Role Management (Super Admin)", level=3)
    add_bullet(
        doc,
        "Role must be an adding option; super admin can add any number of roles needed.",
        bold_prefix="Adding Roles: ",
    )
    add_bullet(
        doc,
        "Role must capture abbreviation and acronym, which can be displayed throughout the application wherever necessary.",
        bold_prefix="Abbreviation & Acronym: ",
    )
    add_bullet(
        doc,
        "A few roles can edit the roles of peers and subordinates; provision needed to enable/disable this permission per role.",
        bold_prefix="Peer/Subordinate Role Editing: ",
    )
    add_bullet(
        doc,
        "Super admin will set the hierarchy level of the roles.",
        bold_prefix="Hierarchy Level: ",
    )

    add_heading_custom(doc, "6. Letters", level=3)
    add_bullet(
        doc,
        "Relieving and joining letters for roles can be generated from the application, using a letter format shared by the department – reducing offline activity.",
        bold_prefix="Relieving & Joining Letters: ",
    )

    add_heading_custom(doc, "7. Account Creation", level=3)
    add_bullet(
        doc,
        "User account creation happens instantly; no approval process is necessary.",
        bold_prefix="Instant Creation: ",
    )

    add_heading_custom(doc, "8. Reports", level=3)
    add_bullet(
        doc,
        "Necessary reports are needed showing how many users logged in every day, including the roles of those users.",
        bold_prefix="Daily Login Report: ",
    )

    add_heading_custom(doc, "1.2 Acts / Rules / Notifications", level=2)
    add_para(
        doc,
        "Not captured in the 25-08-2026 source note (KT session focused on login and role-management behaviour).",
        size=10.5,
    )

    add_heading_custom(doc, "1.3 Pain points", level=2)
    add_para(
        doc,
        "No ServiceDesk pain-point mapping was attached to the 25-08-2026 user-management note.",
        size=10.5,
    )

    add_heading_custom(doc, "1.4 User stories", level=2)
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
            ["US-LG-01", "Citizen", "As a Citizen, I need to log in with my Username + Captcha + OTP sent only to my registered mobile, with no password option, so that I can access KAVERI securely.", "FR-UM-005, FR-UM-009, FR-UM-010, FR-UM-011"],
            ["US-LG-02", "DSR Officer", "As a DSR Officer, I need to log in with my KGID + Captcha + Face authentication or Biometrics (no OTP and no password), so that I can access the office application.", "FR-UM-006, FR-UM-009"],
            ["US-LG-03", "Other Department user", "As an Other Department user, I need to log in with my Username (Department Code concatenated with Employee ID or KGID) + Captcha + OTP (no biometrics), so that I can access my allotted modules.", "FR-UM-007, FR-UM-009"],
            ["US-PS-01", "DSR Officer", "As a DSR Officer with more than one active sanctioned-post occupancy, I need to select exactly one assigned post labelled \"Role — Post Name — Office Name (Office Code)\" after authentication (auto-select if only one), so that session Module Function claims come from that assigned post only.", "FR-UM-052, FR-UM-038"],
            ["US-AC-01", "DSR Officer", "As a DSR Officer already logged in under my assigned post, I need to take additional charge of a wholly unoccupied subordinate post at the same office without logout, switch back to assigned-post context when needed, and see the active context in the header, so that I can cover vacant desks for the session without retaining assigned-post privileges while in additional charge.", "FR-UM-053, FR-UM-054, FR-UM-066(b)"],
            ["US-CR-01", "Citizen", "As a Citizen, I need to self-register instantly (preferred Username availability check, email OTP, mobile OTP, and mandatory Aadhaar e-KYC) with no approval workflow, so that I can start using the portal without delay.", "FR-UM-001, FR-UM-062, FR-UM-063, FR-UM-085"],
            ["US-CR-02", "Authorised administrator", "As an authorised administrator, I need to create DSR Officers and Other Department users instantly without maker-checker, assigning at least one sanctioned post with available capacity for DSR Officers (no Primary/Secondary role distinction) or exactly one Other Department role, so that onboarding is not delayed.", "FR-UM-002, FR-UM-003, FR-UM-017, FR-UM-029, FR-UM-030, FR-UM-051"],
            ["US-RM-01", "Application Admin", "As Application Admin, I need to maintain a single unified Role Master and User Master (differentiated by Role Category / User Category), with unique role names, abbreviations as displayed via Post–Role mapping, and hierarchy via the DSR Officer Hierarchy Master, so that access and reporting lines stay configurable.", "FR-UM-016, FR-UM-028, FR-UM-034, FR-UM-035, FR-UM-043, FR-UM-047"],
            ["US-TO-01", "Hierarchy superior", "As a hierarchy superior (within office span and immediate-parent post parentage), I need to relieve a subordinate from a post occupancy capturing Relieving Date, enumerated Relieving Reason, and Relieving Order (number / upload), so that Transfer Out is auditable and occupancy ends after the Relieving Date via the midnight refresh job.", "FR-UM-057, FR-UM-058, FR-UM-068, FR-UM-087"],
            ["US-TI-01", "Hierarchy superior", "As a hierarchy superior, I need to Transfer In an officer to a Post + Office that already has available capacity, capturing Transfer / Reporting Order (immediate effect; no Joining Date), so that the officer can select that post at the next login.", "FR-UM-060, FR-UM-066(a)"],
            ["US-RP-01", "Management / Admin", "As management, I need login-attempt audit reports (successful and failed) over a selected date range, plus role/permission, sanctioned-post occupancy, additional-charge, and Transfer Out/In history reports, so that access and establishment can be monitored.", "BRD §6 Reporting Requirements; FR-UM-053; FR-UM-057–FR-UM-060"],
            ["US-TA-01", "District Registrar", "As District Registrar of DRO Bengaluru, I need to record Leave for the Sub-Registrar of SRO Yeshwanthapura (SRO A) from 01-Sep-2026 to 05-Sep-2026 so that the officer cannot access KAVERI during that period.", "FR-UM-079, FR-UM-080"],
            ["US-TA-02", "District Registrar", "As the same District Registrar, I need to give temporary charge of SRO Yeshwanthapura (SRO A) Sub-Registrar work to the Sub-Registrar of SRO Jayanagar (SRO B) under my district for the leave period so that SRO A work continues.", "FR-UM-082, FR-UM-083"],
            ["US-TA-03", "AIGR (Admin)", "As AIGR (Admin), I need to record OOD / Leave for District Registrar of DRO Mysuru and assign temporary charge of that DRO post to the District Registrar of DRO Bengaluru (another district under me) so that DRO Mysuru work continues.", "FR-UM-079, FR-UM-082"],
            ["US-TA-04", "Covering Sub-Registrar", "As Sub-Registrar of SRO B holding temporary charge of SRO A, I need to log in and choose whether to work as SR of B or under temporary charge of A.", "FR-UM-052 lists both; one context; FR-UM-083"],
        ],
        col_widths=[0.9, 1.3, 3.4, 1.6],
    )

    # =====================================================================
    # 27-08-2026
    # =====================================================================
    page_break(doc)
    add_heading_custom(
        doc,
        "2. 27-08-2026 — Registration Core (Registration, Appointment, Status tracking)",
        level=1,
    )
    add_meta_table(
        doc,
        [
            ["Date", "27-08-2026"],
            [
                "Topics",
                "Registration core: Registration, Appointment, Status tracking (current issues & process walkthrough)",
            ],
            [
                "Attendees",
                "Kaveri IT Cell, AIGR Comp, Project Manager, Assistant Manager (CMS)",
            ],
            [
                "Version",
                "1.1 (04-09-2026) — Acts, Rules, notifications and ServiceDesk pain points added",
            ],
            ["Source", "Document_Registration_requirement_27082026_v1.1.docx"],
        ],
    )

    add_heading_custom(doc, "2.1 Discussion sections", level=2)

    add_heading_custom(doc, "Document Classification", level=3)
    add_bullet(
        doc,
        "Upgrade the current standard dropdown menus to a more intuitive, requirement-based selection interface to improve the citizen experience.",
        bold_prefix="Article/Sub-Article Selection: ",
    )

    add_heading_custom(doc, "Village Index Selection", level=3)
    add_bullet(
        doc,
        "Evaluate the technical feasibility of implementing geofencing for location accuracy.",
        bold_prefix="Geofencing: ",
    )
    add_bullet(
        doc,
        "Integrate with KSRSAC to automatically retrieve and populate Index-II village details.",
        bold_prefix="KSRSAC Integration: ",
    )

    add_heading_custom(doc, "Property Details Interface", level=3)
    add_bullet(
        doc,
        'Remove the "East to West" and "North to South" text fields specifically for agricultural properties.',
        bold_prefix="Boundary Fields: ",
    )
    add_bullet(
        doc,
        "Implement a feature to display the property map visually, indicating the East, West, North, and South boundaries.",
        bold_prefix="Visual Mapping: ",
    )

    add_heading_custom(doc, "Party Information Interface", level=3)
    add_bullet(
        doc,
        'Update party labels automatically based on the transaction type (e.g., "Seller and Purchaser" for sales, or "Donor and Donee" for gifts).',
        bold_prefix="Dynamic Role Labels: ",
    )
    add_bullet(
        doc,
        "Deploy service-specific SMS/message templates for Aadhaar OTP authentication.",
        bold_prefix="Aadhaar Integration: ",
    )
    add_bullet(
        doc,
        "Auto-populate the gender field based on the user's selected salutation.",
        bold_prefix="Smart Form Logic: ",
    )
    add_bullet(
        doc,
        "Configure the schedule allocation feature to appear only for transaction types that explicitly require it, hiding it for all others.",
        bold_prefix="Conditional Scheduling: ",
    )

    add_heading_custom(doc, "Property Valuation", level=3)
    add_bullet(
        doc,
        "Hide the base valuation rate from citizens. Users should only select the property's physical characteristics (e.g., commercial, residential, dry, wet) to proceed.",
        bold_prefix="User Interface Streamlining: ",
    )

    add_heading_custom(doc, "Review and Submission", level=3)
    add_bullet(
        doc,
        'Ensure the "Consideration Amount" field label changes dynamically based on the nature of the document being submitted.',
        bold_prefix="Dynamic Captions: ",
    )
    add_bullet(
        doc,
        "Mandate a comprehensive document summary preview for the applicant to review before finalizing their submission for verification.",
        bold_prefix="Pre-Submission Preview: ",
    )

    add_heading_custom(doc, "2.2 Primary Acts (Sections)", level=2)
    add_table(
        doc,
        ["Act", "Sections", "Relevance"],
        [
            [
                "The Registration Act, 1908 (Central Act 16 of 1908)",
                "Secs. 17–22, 23, 25, 28–35, 51–52, 58–61, 71–77, 78",
                "Compulsory / optional registration; presentation time & place; examination; endorsements & Sec. 60 certificate; refusal / appeal; registration fees — core Registration and Status tracking",
            ],
            [
                "The Registration Act, 1908",
                "Secs. 5–7, 10–12, 28–31",
                "Districts / sub-districts; Registrars & Sub-Registrars; place of registration — Appointment office selection and jurisdiction routing",
            ],
            [
                "The Registration (Karnataka Amendment) Act, 2023 (Karnataka Act 47 of 2024)",
                "Secs. 22-B, 22-C, 22-D, 81-A, 81-B",
                "Refusal / cancellation of forged or prohibited documents; appeal; penalties — registration intake validation",
            ],
            [
                "The Karnataka Stamp Act, 1957",
                "Secs. 3, 10, 33–39, 45-A, Schedule",
                "Stamp duty chargeable; payment modes; impounding; undervaluation reference — touched in 28-08 discussion",
            ],
            [
                "The Transfer of Property Act, 1882",
                "Sec. 54",
                "Sale of immovable property of value > ₹100 requires registered instrument — drives Article / transaction-type selection for conveyance",
            ],
        ],
        col_widths=[2.2, 1.8, 2.8],
    )

    add_heading_custom(doc, "2.3 Primary Rules", level=2)
    add_table(
        doc,
        ["Rule", "Key provisions", "Relevance to topic"],
        [
            [
                "Karnataka Registration Rules, 1965 — Ch. II",
                "Rules 3, 5",
                "Office hours and holidays — Appointment / slot calendar",
            ],
            [
                "Karnataka Registration Rules, 1965 — Ch. VI",
                "Rules 13–15",
                "Territorial divisions; survey / city survey description — Village Index and property details (KSRSAC / GIS)",
            ],
            [
                "Karnataka Registration Rules, 1965 — Ch. IX",
                "Rules 37, 40–46, 51–55",
                "Office where document may be registered; presentation; examination; endorsement; suspension (fine / stamp); condonation — Registration & Status",
            ],
            [
                "Karnataka Registration Rules, 1965 — Ch. XII / XVI",
                "Rules 71–73, 78–79, 94, 104",
                "Executant examination; thumb impression / photograph; endorsements; Sec. 60 certificate — Registration completion",
            ],
            [
                "Karnataka Registration Rules, 1965 — Ch. XVII / XXV",
                "Rules 110–118, 175–188",
                "Receipts; return of document; appeal against refusal — Status tracking termini",
            ],
            [
                "Karnataka Stamp Rules, 1958 / e-Stamping Rules, 2009",
                "Stamp payment procedures",
                "Impressed / franking / e-Stamp at presentation — Payment visibility (28-08)",
            ],
        ],
        col_widths=[2.4, 1.6, 2.8],
    )

    add_heading_custom(doc, "2.4 Notifications / amendments", level=2)
    add_table(
        doc,
        ["Instrument", "Effect", "Relevance"],
        [
            [
                "RGN 2/2002-03 (1 Apr 2002; w.e.f. 4 Apr 2002)",
                "Rule 19-A document sheets; Rules 22-A–22-C; Rule 40 photograph / digital photo",
                "Document format and photo at presentation",
            ],
            [
                "RD 403 ESR 85 (27 May 1986) as amended by RD/46/MNMU/2025 (29 Aug 2025)",
                "Table of Registration Fees under Sec. 78 — fee revision w.e.f. 31 Aug 2025",
                "Registration fee calculator / payment amount",
            ],
            [
                "RD 380 MUNOMU 2008 (8 Apr 2009)",
                "Karnataka Stamp (Payment of Duty by Means of e-Stamping) Rules, 2009",
                "e-Stamp payment and verification at SRO",
            ],
            [
                "Stamp Act Sec. 45-B (Act 8 of 2003) / Undervaluation Rules, 1977 (GSR 81)",
                "CVC market value guidelines; Sec. 45-A reference / Form I",
                "Guidance value & undervaluation / impound (noted on 28-08)",
            ],
        ],
        col_widths=[2.4, 2.2, 2.2],
    )

    add_heading_custom(doc, "2.5 Pain points", level=2)
    add_para(
        doc,
        "Registration core — Registration, Appointment, Status tracking (aligned to 27-08 discussion notes). "
        "Source: ServiceDeskIssuesList.xlsx (OverallList + Categorized).",
        size=10,
        space_after=6,
    )
    add_table(
        doc,
        ["Pain point", "Evidence (tickets / categorized)"],
        [
            [
                "Article / sub-article selection & instrument mapping",
                "Release Deed Article Issue (17714); Stamp Duty wrong for partition sub-article 39-b (31257); Gift Deed stamp duty double (93306)",
            ],
            [
                "Village / Index / road master gaps",
                "Village index absent / split villages (13949); road names wrong (95135); road option not showing for agriculture land (31819); Sy. No. not fetching from Bhoomi (20170, 30045); wrong village shown (29600)",
            ],
            [
                "Property schedule / boundary capture fails",
                "Unable to save the property schedule (24450); Unable to Save and Continue after 11E Sketch (24247); property details not in dept summary (95367)",
            ],
            [
                "Party information save / display errors",
                "Unable to save party info (30276); claimant details missing in summary (25784, 28927, 29588); executant name showing None (22789); claimant photo at executant place (27709)",
            ],
            [
                "Property valuation / fee after valuation",
                "Market valuation blank / not showing (29357, 29532, 27923); valuate → fee zero & Save disabled (28596); fee zero in summary (26292)",
            ],
            [
                "Pre-submission summary / review broken",
                "Unable to generate / view document summary (27360, 27805, 30609, 12009); consideration / market value wrong in summary (6187, 10531); sub-article name not in dept summary (92782); challan not in summary (31168, 29793)",
            ],
            [
                "Appointment / schedule after intake",
                "Unable to Schedule for Appointment (27283, 30478, 30908); schedule not reflecting (28240); schedule option missing after payment (Categorized: 27283, 30478, 28812, 30908)",
            ],
            [
                "Status / step stuck after registration flow",
                "Check and Register (Step 7) disabled (94299, 94264, 92559); applications stuck in Step 5 (23243, 25183); pending shows in Step 1 instead of Minute Book (22599, 31762)",
            ],
        ],
        col_widths=[2.6, 4.2],
    )

    add_heading_custom(doc, "2.6 User stories", level=2)
    add_para(
        doc,
        "Derived from 27-08 discussion sections and mapped Acts/Rules.",
        size=10,
        space_after=8,
    )
    for s in [
        (
            "US-REG-01",
            "citizen",
            "select article / sub-article through a requirement-based interface instead of opaque dropdowns",
            "I choose the correct instrument for my transaction",
        ),
        (
            "US-REG-02",
            "citizen / Sub-Registrar",
            "retrieve Index-II village details via KSRSAC (and evaluate geofencing for location accuracy)",
            "village and location masters are accurate at intake",
        ),
        (
            "US-REG-03",
            "citizen",
            "enter agricultural property boundaries without East-West / North-South text fields and see boundaries on a visual map",
            "property schedule capture matches field practice",
        ),
        (
            "US-REG-04",
            "citizen",
            "see party labels that change with transaction type (Seller/Purchaser, Donor/Donee, etc.)",
            "party roles are clear for the deed type",
        ),
        (
            "US-REG-05",
            "citizen",
            "authenticate with Aadhaar OTP using service-specific SMS templates and auto-filled gender from salutation",
            "party capture is faster and less error-prone",
        ),
        (
            "US-REG-06",
            "citizen",
            "see schedule allocation only when the transaction type requires it",
            "unnecessary appointment steps are hidden",
        ),
        (
            "US-REG-07",
            "citizen",
            "complete valuation by selecting physical characteristics without seeing the base rate",
            "valuation UI stays simple while duty still uses official rates",
        ),
        (
            "US-REG-08",
            "citizen",
            "review a full document summary with dynamic consideration captions before submission",
            "I can correct errors before verification",
        ),
    ]:
        add_story(doc, *s)

    # =====================================================================
    # 28-08-2026
    # =====================================================================
    page_break(doc)
    add_heading_custom(
        doc,
        "3. 28-08-2026 — Registration Core (SR workflow, Slot, Payment, Stamp / Guidance value)",
        level=1,
    )
    add_meta_table(
        doc,
        [
            ["Date", "28-08-2026"],
            [
                "Topics",
                "Registration core: Registration, Appointment, Status tracking (continued) — SR workflow, slot, payment, stamp / guidance value, impound",
            ],
            [
                "Attendees",
                "Kaveri IT Cell, AIGR Comp, Project Manager, Assistant Manager (CMS)",
            ],
            [
                "Version",
                "1.1 (04-09-2026) — Acts, Rules, notifications and ServiceDesk pain points added",
            ],
            ["Source", "Document_Registration_requirement_28082026_v1.1.docx"],
        ],
    )

    add_heading_custom(doc, "3.1 Discussion sections", level=2)

    sections_2808 = [
        (
            "1. SR Level Approval Workflow",
            [
                (
                    "Action Buttons: ",
                    'At the first level of approval from SR, provide two buttons – “Send to Applicant for Payment” and “Send Back for Correction.”',
                ),
                (
                    "Payment Visibility on Correction: ",
                    "If the application is sent back for correction, the payment option should not display in the employee login.",
                ),
            ],
        ),
        (
            "2. SRO Road Selection",
            [
                (
                    "Under-Valuation & Impound Workflow: ",
                    "For roads selected by the SRO, the under-valuation and impound workflow is to be built in Version 3.0.",
                ),
            ],
        ),
        (
            "3. Date & Time Format",
            [
                (
                    "Time Format Change: ",
                    "Change the date/time format from 24-hour to 12-hour format.",
                ),
            ],
        ),
        (
            "4. Slot Booking",
            [
                (
                    "Tatkal Slot Booking: ",
                    "Provide provision to book a tatkal slot at the required time slot.",
                ),
                (
                    "Percentage-Based Amount: ",
                    "Provide provision to set the amount based on a percentage.",
                ),
                (
                    "Rescheduling with Fine: ",
                    "Rescheduling a fixed slot should happen with a fine – provision to be checked and understood further.",
                ),
            ],
        ),
        (
            "5. Payment Visibility",
            [
                (
                    "Sub-Registrar Payment: ",
                    "Payment made in front of the Sub-Registrar should be projected more prominently to the citizen.",
                ),
            ],
        ),
        (
            "6. Withdrawal Workflow",
            [
                (
                    "Simplify Withdrawal: ",
                    "The withdrawal option from allocation application to DEO should be made simple; workflow to be prepared.",
                ),
            ],
        ),
        (
            "7. Application Type Naming",
            [
                (
                    "Renaming: ",
                    "Application type to be renamed as “transaction type” in the DEO login.",
                ),
            ],
        ),
        (
            "8. Application Number Display",
            [
                (
                    "Consistent Display: ",
                    "Application number to be displayed throughout the application flow.",
                ),
            ],
        ),
        (
            "9. Calculations",
            [
                (
                    "Stamp duty and registrar fee: ",
                    "Stamp duty and registrar fee calculation — the Stamp Act has to be studied.",
                ),
                (
                    "Guidance value: ",
                    "Guidance value calculation — the valuation rules as per gazette has to be studied.",
                ),
            ],
        ),
        (
            "10. Summary",
            [
                ("Rework Summary: ", "Summary needs to be reworked."),
                (
                    "Document Number: ",
                    "Document number to be displayed in the summary.",
                ),
            ],
        ),
    ]
    for title, bullets in sections_2808:
        add_heading_custom(doc, title, level=3)
        for bp, txt in bullets:
            add_bullet(doc, txt, bold_prefix=bp)

    add_heading_custom(doc, "3.2 Primary Acts (Sections)", level=2)
    add_para(
        doc,
        "Same Act/section set as 27-08 (Registration Act core + Karnataka Amendment + Stamp Act + T.P. Act Sec. 54), with 28-08 emphasis on stamp duty, guidance value and impound.",
        size=10,
        space_after=6,
    )
    add_table(
        doc,
        ["Act", "Sections", "Relevance"],
        [
            [
                "The Registration Act, 1908",
                "Secs. 17–22, 23, 25, 28–35, 51–52, 58–61, 71–77, 78",
                "Core Registration and Status tracking",
            ],
            [
                "The Registration Act, 1908",
                "Secs. 5–7, 10–12, 28–31",
                "Appointment office selection and jurisdiction routing",
            ],
            [
                "Registration (Karnataka Amendment) Act, 2023",
                "Secs. 22-B, 22-C, 22-D, 81-A, 81-B",
                "Refusal / cancellation; intake validation",
            ],
            [
                "Karnataka Stamp Act, 1957",
                "Secs. 3, 10, 33–39, 45-A, Schedule",
                "Stamp duty / payment / impound / undervaluation (28-08 focus)",
            ],
            [
                "Transfer of Property Act, 1882",
                "Sec. 54",
                "Conveyance / transaction-type selection",
            ],
        ],
        col_widths=[2.2, 1.8, 2.8],
    )

    add_heading_custom(doc, "3.3 Primary Rules", level=2)
    add_para(
        doc,
        "Same Registration Rules / Stamp Rules set as 27-08; e-Stamping Rules especially relevant to payment visibility discussed on 28-08.",
        size=10,
        space_after=6,
    )
    add_table(
        doc,
        ["Rule", "Key provisions", "Relevance"],
        [
            ["KR Rules Ch. II — Rules 3, 5", "Office hours / holidays", "Slot calendar"],
            [
                "KR Rules Ch. VI — Rules 13–15",
                "Survey / territorial description",
                "Village Index / GIS",
            ],
            [
                "KR Rules Ch. IX — Rules 37, 40–46, 51–55",
                "Presentation / examination / suspension",
                "Registration & Status",
            ],
            [
                "KR Rules Ch. XII / XVI — Rules 71–73, 78–79, 94, 104",
                "Examination / photo / Sec. 60",
                "Registration completion",
            ],
            [
                "KR Rules Ch. XVII / XXV — Rules 110–118, 175–188",
                "Receipts / return / appeal",
                "Status termini",
            ],
            [
                "Stamp Rules 1958 / e-Stamping Rules 2009",
                "Stamp payment procedures",
                "Payment visibility at SRO",
            ],
        ],
        col_widths=[2.6, 2.0, 2.2],
    )

    add_heading_custom(doc, "3.4 Notifications / amendments", level=2)
    add_table(
        doc,
        ["Instrument", "Effect", "Relevance"],
        [
            [
                "RGN 2/2002-03",
                "Document sheets; photo rules",
                "Presentation format",
            ],
            [
                "RD 403 ESR 85 / RD/46/MNMU/2025",
                "Registration fee table revision w.e.f. 31 Aug 2025",
                "Fee calculator / payment amount",
            ],
            [
                "RD 380 MUNOMU 2008",
                "e-Stamping Rules, 2009",
                "e-Stamp at SRO",
            ],
            [
                "Stamp Act Sec. 45-B / Undervaluation Rules, 1977",
                "CVC guidelines; Sec. 45-A / Form I",
                "Guidance value & undervaluation / impound",
            ],
        ],
        col_widths=[2.4, 2.2, 2.2],
    )
    add_para(
        doc,
        "Cross-reference (28-08): Detailed study of Karnataka Stamp Act Schedule and CVC / Undervaluation Rules was flagged (items 2, 9). "
        "Full legal tables for those topics are also covered under the 01-09-2026 note.",
        size=10,
        space_after=8,
    )

    add_heading_custom(doc, "3.5 Pain points", level=2)
    add_table(
        doc,
        ["Pain point", "Evidence (tickets / categorized)"],
        [
            [
                "SR send to payment / send back for correction",
                "After verification unable to send to citizen for payment / rectify (94523, 92990, 92566, 88608, 83818, 31346 — pending count 6); after evaluation send does not proceed (30960, 31484); sent-back apps still ask for payment with amount 0 (88309, 27587)",
            ],
            [
                "Payment visibility & payment failures",
                "Unable to make payment (29349, 29407); payment error (94275); payment completed but still Make Payment (92384, 28335, 26151); payment details not in 10A (27824)",
            ],
            [
                "Slot booking / tatkal / reschedule",
                "Unable to schedule (27283 P1, 30478, 30908); time slot issue (30841); unable to re-schedule (91929); after payment still pending while citizen books slot (28335)",
            ],
            [
                "Withdrawal workflow",
                "Withdraw option not available for rejected application (93043); citizen unable to withdraw (24685, 23807); withdrawn app still pending in DEO (9494, 23080); withdraw auto-generated registration number (8691); payment withdraw issue (28630)",
            ],
            [
                "Stamp duty & registration fee calculation",
                "Unable to Calculate Stamp duty and Registration fee (23369); fees calculation category pending (74 tickets); partition / gift article wrong duty (31257, 93306, 31130); fee zero after valuation (28596, 26292)",
            ],
            [
                "Guidance value / undervaluation & impound",
                "Pending for 45-A undervaluation (93336… — count 6); unable to release 45-A pending (13204, 14582, 31209–31212); Impound related issue (30024); CVC rates not displaying (31481, 31521); rural building valued at TMC/CMC rates (29393)",
            ],
            [
                "Summary / document number display",
                "Summary not generating (27360, 27805, 30609); document number generated but still in DEO Step-1 Generate Summary (28388); document number / challan / consideration missing or wrong in summary (31168, 6187, 10531)",
            ],
            [
                "Status tracking — wrong step / DSC / acknowledgement",
                "Digital Sign option / SR name missing at Step 9 (95322, 27050, 95349); Unable to Print acknowledgement at Step 10 (88602); slot allocation — registration complete but still in DEO Step 3 (28586); app number / status inconsistent across logins",
            ],
        ],
        col_widths=[2.6, 4.2],
    )

    add_heading_custom(doc, "3.6 User stories", level=2)
    add_para(
        doc,
        "Derived from 28-08 discussion sections.",
        size=10,
        space_after=8,
    )
    for s in [
        (
            "US-SR-01",
            "Sub-Registrar",
            "choose “Send to Applicant for Payment” or “Send Back for Correction” at first-level approval",
            "the application moves cleanly to payment or correction without ambiguity",
        ),
        (
            "US-SR-02",
            "DEO / department user",
            "hide the payment option when an application is sent back for correction",
            "employees are not prompted to collect payment on a correction cycle",
        ),
        (
            "US-SLOT-01",
            "citizen",
            "book a tatkal slot at a required time and understand percentage-based amounts and reschedule-with-fine rules",
            "urgent appointments can be secured under clear fee rules",
        ),
        (
            "US-PAY-01",
            "citizen",
            "clearly see payments made in front of the Sub-Registrar",
            "SRO-counter payments are visible and trusted",
        ),
        (
            "US-WD-01",
            "citizen / DEO",
            "withdraw an application from allocation to DEO through a simple workflow",
            "withdrawals do not leave orphan pending states",
        ),
        (
            "US-TXN-01",
            "DEO",
            "see “transaction type” (renamed from application type) and the application number throughout the flow",
            "naming and identifiers stay consistent",
        ),
        (
            "US-FEE-01",
            "citizen / Sub-Registrar",
            "calculate stamp duty and registration fee using Stamp Act / gazette valuation rules",
            "fee and duty match legal schedules",
        ),
        (
            "US-SUM-01",
            "citizen / DEO",
            "view a reworked summary that includes the document number",
            "summary is usable for verification and status tracking",
        ),
    ]:
        add_story(doc, *s)

    # =====================================================================
    # 01-09-2026
    # =====================================================================
    page_break(doc)
    add_heading_custom(
        doc,
        "4. 01-09-2026 — Guideline Value, CVC Valuation Module & GIS Valuation",
        level=1,
    )
    add_meta_table(
        doc,
        [
            ["Date", "01-09-2026"],
            [
                "Topics",
                "Guideline value calculation, Valuation Module (CVC) and GIS valuation",
            ],
            ["Attendees", "Kaveri IT Cell, DIGR- Valuation"],
            ["Source", "Document_Registration_requirement_01092026_v2.docx"],
        ],
    )

    add_heading_custom(doc, "4.1 Discussion sections / legal mapping", level=2)

    add_heading_custom(doc, "1. Guideline value calculation", level=3)
    add_table(
        doc,
        ["Type", "Instrument", "Relevance"],
        [
            [
                "Act",
                "Karnataka Stamp Act, 1957 — Sec. 45-A",
                "SRO compares consideration with market value guidelines published under Sec. 45-B; if undervalued, estimates value, seeks duty, or refers to Deputy Commissioner",
            ],
            [
                "Act",
                "Karnataka Stamp Act, 1957 — Sec. 45-B",
                "Authority to estimate, publish and revise market value guidelines (guideline rates used in calculation)",
            ],
            [
                "Act",
                "Karnataka Stamp Act, 1957 — Sec. 3 + Schedule",
                "Stamp duty is ad valorem on market value for listed instruments (conveyance, gift, exchange, etc.)",
            ],
            [
                "Rules",
                "Karnataka Stamp (Prevention of Undervaluation of Instruments) Rules, 1977",
                "Procedure + Form I (property particulars / market value)",
            ],
            [
                "Supporting",
                "Registration Rules 13–15",
                "Survey / territorial description needed to pick the correct guideline rate for a property",
            ],
        ],
        col_widths=[1.2, 2.4, 3.2],
    )

    add_heading_custom(doc, "2. Valuation Data Entry Module (CVC)", level=3)
    add_table(
        doc,
        ["Type", "Instrument", "Relevance"],
        [
            [
                "Act",
                "Karnataka Stamp Act, 1957 — Sec. 45-B (primary)",
                "CVC under IGR & Commissioner of Stamps estimates, publishes, revises market value guidelines; may form district / sub-district market valuation sub-committees; final authority on policy and methodology",
            ],
            [
                "Act",
                "Karnataka Stamp Act, 1957 — Sec. 2(ac)",
                'Defines “Central Valuation Committee”',
            ],
            [
                "Act",
                "Karnataka Stamp Act, 1957 — Sec. 45-A",
                "Guidelines published by CVC are applied at registration for stamp duty",
            ],
            [
                "Rules",
                "Prevention of Undervaluation Rules, 1977 (GSR 81 / RD 73 EST 74)",
                "Operational rules when Sec. 45-A is invoked (Form I, DC order, appeal)",
            ],
            [
                "Notification / amendment",
                "Act 8 of 2003 (w.e.f. 1-4-2003)",
                "Substituted / strengthened Sec. 45-B CVC framework",
            ],
            [
                "Amendment",
                "RD 264 MUNOMU 99 (18-8-1999)",
                "Amendments to Undervaluation Rules",
            ],
        ],
        col_widths=[1.4, 2.4, 3.0],
    )

    add_heading_custom(doc, "3. GIS valuation", level=3)
    add_para(
        doc,
        "GIS valuation is an implementation layer on top of CVC guideline rates, to be integrated with KSRSAC (Karnataka State Remote Sensing Department).",
        size=10.5,
    )

    add_heading_custom(doc, "4.2 Pain points", level=2)
    add_heading_custom(doc, "Guideline value calculation", level=3)
    add_table(
        doc,
        ["Pain point", "Evidence (tickets / categorized)"],
        [
            [
                "Wrong / blank market (guideline) value shown",
                "Market value blank on sale deed (29357); valuation not showing (29532); agriculture land valuation not showing (27923); wrong market value (31438); market value wrong in EC (18690); market value not in SR login (29931)",
            ],
            [
                "Wrong building rate applied for rural properties",
                "Rural properties calculated on TMC/CMC rates instead of rural rates (29393; Categorized: 93332)",
            ],
            [
                "Unit-level valuation fails (gunta / area)",
                "Valuation for 1 gunta not showing (31788); gunta/cent conversion issues (24718, 26498, 6097)",
            ],
            [
                "Duty / fee calculator fails after valuation",
                "Unable to calculate stamp duty & registration fee (23369); citizen valuate → fee zero, Save disabled (28596); fee zero in summary (26292)",
            ],
            [
                "Adjudicated Sec. 45-A value not respected",
                "Summary shows market value higher than DR-adjudicated value under 45(A) (10531); citizen sees SR value higher than undervaluation amount (31773)",
            ],
            [
                "Instrument-specific gaps",
                "Request for market-value estimation for trust deed (31534); partition/gift fee/duty wrong on articles (31257, 93306)",
            ],
            [
                "CVC rates missing in SR and Citizen login",
                "“In CVC module some rates are not displaying in SR Login And Citizen login” (31481 P1, 31521)",
            ],
            [
                "Cannot correct CVC rates in Citizen login",
                "“Correction Rate in CVC Citizen login” (21795)",
            ],
            [
                "Generic CVC module failures",
                "“CVC issue” (15278); payment issue after CVC (31574 P1)",
            ],
            [
                "Revaluation / send-back workflow broken",
                "App moved for revaluation then stuck / need withdraw (23267); after evaluation, SR cannot send application further (30960, 31484)",
            ],
            [
                "Undervaluation (Sec. 45-A) data / payment stuck",
                "Undervaluation data fetch failure (25098); unable to pay for undervaluation (31071); pending 45-A in Kaveri-1 (27140)",
            ],
        ],
        col_widths=[2.6, 4.2],
    )

    add_heading_custom(doc, "4.3 User stories", level=2)
    add_para(
        doc,
        "User stories mapped to the Acts, Rules, notifications and GIS notes listed in the 01-09-2026 discussion note.",
        size=10,
        space_after=8,
    )

    add_heading_custom(doc, "Guideline value calculation", level=3)
    add_para(doc, "Karnataka Stamp Act, 1957 — Sec. 45-A", size=10, bold=True, space_after=2)
    add_story(
        doc,
        "US-GV-01",
        "Sub-Registrar",
        "compare the consideration in the instrument with the market value guidelines published under Sec. 45-B",
        "if the property is undervalued I can estimate the value, collect the extra duty, or refer the case to the Deputy Commissioner",
    )
    add_para(doc, "Karnataka Stamp Act, 1957 — Sec. 45-B", size=10, bold=True, space_after=2)
    add_story(
        doc,
        "US-GV-02",
        "citizen / Sub-Registrar",
        "use the official market value guidelines published and revised under Sec. 45-B in guideline value calculation",
        "stamp duty is computed on the current notified guideline rates and not on an unofficial figure",
    )
    add_para(doc, "Karnataka Stamp Act, 1957 — Sec. 3 + Schedule", size=10, bold=True, space_after=2)
    add_story(
        doc,
        "US-GV-03",
        "citizen / Sub-Registrar",
        "calculate stamp duty ad valorem on market value for Schedule instruments (conveyance, gift, exchange and other listed articles)",
        "the correct Schedule article and rate are applied after guideline value is arrived at",
    )
    add_para(
        doc,
        "Karnataka Stamp (Prevention of Undervaluation of Instruments) Rules, 1977",
        size=10,
        bold=True,
        space_after=2,
    )
    add_story(
        doc,
        "US-GV-04",
        "Sub-Registrar",
        "capture property particulars and market value in Form I when starting a Sec. 45-A reference",
        "the undervaluation case follows the notified procedure and has a complete property statement",
    )
    add_para(doc, "Registration Rules 13–15 (supporting)", size=10, bold=True, space_after=2)
    add_story(
        doc,
        "US-GV-05",
        "citizen / Sub-Registrar",
        "enter survey number, territorial division and property description as required by Registration Rules 13–15",
        "the system can pick the correct guideline rate for that property",
    )

    add_heading_custom(doc, "Valuation Data Entry Module (CVC)", level=3)
    add_para(doc, "Karnataka Stamp Act, 1957 — Sec. 45-B (primary)", size=10, bold=True, space_after=2)
    add_story(
        doc,
        "US-CVC-01",
        "IGR / Central Valuation Committee",
        "estimate, publish and revise market value guidelines and constitute district / sub-district market valuation sub-committees",
        "CVC remains the final authority for policy, methodology and administration of guideline rates in the State",
    )
    add_story(
        doc,
        "US-CVC-02",
        "CVC / valuation data-entry officer",
        "enter, update and publish guideline rates in the Valuation Module for use by SR and citizen logins",
        "rates are available for guideline value calculation and do not go missing in office or citizen screens",
    )
    add_para(doc, "Karnataka Stamp Act, 1957 — Sec. 2(ac)", size=10, bold=True, space_after=2)
    add_story(
        doc,
        "US-CVC-03",
        "system administrator / department user",
        "maintain Central Valuation Committee as the statutory body defined in Sec. 2(ac)",
        "valuation masters and approvals are owned by the correct legal entity",
    )
    add_para(doc, "Karnataka Stamp Act, 1957 — Sec. 45-A", size=10, bold=True, space_after=2)
    add_story(
        doc,
        "US-CVC-04",
        "Sub-Registrar",
        "apply the CVC-published guidelines at the time of registration for stamp duty",
        "duty is charged on the higher of consideration and guideline value where Sec. 45-A applies",
    )
    add_story(
        doc,
        "US-CVC-05",
        "citizen / Sub-Registrar",
        "see and use the District Registrar’s adjudicated Sec. 45-A value instead of an automatically higher guideline figure",
        "the summary and payment match the legally decided market value",
    )
    add_para(
        doc,
        "Prevention of Undervaluation Rules, 1977 (GSR 81 / RD 73 EST 74)",
        size=10,
        bold=True,
        space_after=2,
    )
    add_story(
        doc,
        "US-CVC-06",
        "Sub-Registrar / Deputy Commissioner",
        "run Form I capture, DC determination of market value, and the appeal path under the 1977 Rules",
        "a Sec. 45-A undervaluation case can be completed, paid and released without a data or payment stuck state",
    )
    add_para(doc, "Notification / amendment — Act 8 of 2003 (w.e.f. 1-4-2003)", size=10, bold=True, space_after=2)
    add_story(
        doc,
        "US-CVC-07",
        "CVC administrator",
        "operate the Valuation Module on the Sec. 45-B framework as strengthened by Act 8 of 2003",
        "guideline publication, revision cycles and sub-committee working match the current CVC law",
    )
    add_para(doc, "Amendment — RD 264 MUNOMU 99 (18-8-1999)", size=10, bold=True, space_after=2)
    add_story(
        doc,
        "US-CVC-08",
        "Deputy Commissioner / District Registrar",
        "follow the undervaluation workflow as amended by RD 264 MUNOMU 99 (no obsolete provisional / Rule 6 path)",
        "orders and screens match the Rules now in force",
    )

    add_heading_custom(doc, "GIS valuation", level=3)
    add_para(
        doc,
        "GIS + CVC guideline rates (KSRSAC integration)",
        size=10,
        bold=True,
        space_after=2,
    )
    add_story(
        doc,
        "US-GIS-01",
        "citizen / Sub-Registrar",
        "locate the property on GIS (KSRSAC) and apply the matching CVC guideline rate for that area",
        "valuation uses the correct spatial rate and not a neighbouring village, road or urban slab",
    )
    add_para(doc, "Registration Rules 13–15 / survey description", size=10, bold=True, space_after=2)
    add_story(
        doc,
        "US-GIS-02",
        "citizen / Sub-Registrar",
        "map survey number, Pot Hissa / city survey and territorial division to the GIS layer",
        "guideline value can be calculated even for small extents (for example 1 gunta) with the correct rural or urban building rate",
    )
    add_story(
        doc,
        "US-GIS-03",
        "valuation / GIS administrator",
        "keep village, road and survey masters aligned between Kaveri, CVC rates and KSRSAC",
        "wrong road names, missing village splits and failed survey fetch do not produce a blank or wrong market value",
    )

    # =====================================================================
    # 02-09-2026
    # =====================================================================
    page_break(doc)
    add_heading_custom(
        doc,
        "5. 02-09-2026 — Rule 17 Filing, Old Pending Release & Govt/Institutional E-filing",
        level=1,
    )
    add_meta_table(
        doc,
        [
            ["Date", "02-09-2026"],
            [
                "Topics",
                "Rule 17(2) filing, Rule 17(3) filing, Old pending release module, e-filing from Govt/Institutional, Rule 17(1)",
            ],
            ["Attendees", "Kaveri IT Cell, AIGR Computers team"],
            [
                "Version",
                "1.1 (04-09-2026) — Rule 17(i) Part IV and Part V listed separately; Part VI added in section A",
            ],
            ["Source", "Document_Registration_requirement_02092026_v1.1.docx"],
        ],
    )

    add_heading_custom(doc, "5.1 Primary Acts (Sections)", level=2)
    add_table(
        doc,
        ["Act", "Sections", "Relevance"],
        [
            [
                "The Registration Act, 1908",
                "Sec. 19, 62",
                "Documents in a language not understood / translations & copies → feed Rule 17(ii) filing",
            ],
            [
                "The Registration Act, 1908",
                "Sec. 21",
                "Maps/plans with documents → Rule 17(i) Part II",
            ],
            [
                "The Registration Act, 1908",
                "Sec. 64–67",
                "Memoranda across offices/districts → Rule 17(i) Part I",
            ],
            [
                "The Registration Act, 1908",
                "Sec. 23, 25, 34",
                "Time of presentation; delay & fine → old pending (condonation / fine pending)",
            ],
            [
                "The Registration Act, 1908",
                "Sec. 33 (Stamp Act cross-link via Rules)",
                "Impounding inadequately stamped docs → pending",
            ],
            [
                "The Registration Act, 1908",
                "Sec. 71–77",
                "Refusal / appeal → pending until disposed",
            ],
            [
                "The Registration Act, 1908",
                "Sec. 88",
                "Registration of documents executed by Government officers / public functionaries → Govt/Institutional filing",
            ],
            [
                "The Registration Act, 1908",
                "Sec. 89",
                "Copies of certain orders, certificates and instruments to be sent to registering officers and filed → institutional / court / revenue filing",
            ],
            [
                "The Registration Act, 1908",
                "Sec. 90–91",
                "Exemption of certain Govt documents from registration; inspection/copies",
            ],
            [
                "Karnataka Stamp Act, 1957",
                "Secs. 33–39, 45-A",
                "Impounding / undervaluation → documents held pending until duty adjudicated / paid",
            ],
            [
                "Related filing statutes (via Rule 17 Parts III–V)",
                "Land Acquisition Act; Karnataka Land Improvement Loans Act, 1963; Karnataka Agriculturists Loans Act, 1963; Karnataka Co-operative Societies Act, 1959 (Sec. 85-A)",
                "Source instruments filed into Book 1 supplements",
            ],
        ],
        col_widths=[2.2, 1.8, 2.8],
    )

    add_heading_custom(doc, "5.2 Primary Rules", level=2)
    add_heading_custom(doc, "A. Rule 17 filing", level=3)
    add_table(
        doc,
        ["Rule", "Module mapping", "What it covers"],
        [
            [
                "Rule 17(i) Part I",
                "Related institutional / memo filing",
                "Supplements to Book 1 for Secs. 64–67 memoranda",
            ],
            [
                "Rule 17(i) Part II",
                "Related",
                "Copies of maps/plans (Sec. 21)",
            ],
            [
                "Rule 17(i) Part III",
                "Institutional filing",
                "(a) Court / Revenue sale certificates; (b) Land Acquisition statements from DC",
            ],
            [
                "Rule 17(i) Part IV",
                "Institutional / revenue filing",
                "Copies of instruments and collateral securities under Karnataka Land Improvement Loans Act, 1963 and Karnataka Agriculturists Loans Act, 1963, received from Revenue officers",
            ],
            [
                "Rule 17(i) Part V",
                "Institutional / bank filing",
                "Copies of instruments received from Land Development Banks under Sec. 85-A of the Karnataka Co-operative Societies Act, 1959",
            ],
            [
                "Rule 17(i) Part VI",
                "Institutional filing",
                "Court Charge Creation",
            ],
            [
                "Rule 17(ii) = modules Rule 17(2) (#6)",
                "Rule 17(2) filing",
                "Separate file for copies and translations (Secs. 19, 62 / Rule 12(1)); cross-reference to register entry",
            ],
            [
                "Rule 17(iii) = modules Rule 17(3) (#7)",
                "Rule 17(3) filing",
                "Separate file for communications on cancellation / modification / rectification of previously filed or registered papers",
            ],
        ],
        col_widths=[2.2, 1.8, 2.8],
    )

    add_heading_custom(doc, "B. Old pending release (#8)", level=3)
    add_table(
        doc,
        ["Rule", "Relevance"],
        [
            [
                "Rule 23",
                "Minute Book — note suspension, refusal, summons, withdrawal, stamp impound, out-of-hours receipt",
            ],
            [
                "Rule 24 + Forms 9, 10, 11",
                "Daily Register; registers of impounded, unclaimed, and deficient fee/stamp documents",
            ],
            [
                "Rules 46, 51–55",
                "Suspension for delay fine or stamp impounding; fine rates; condonation of delay",
            ],
            [
                "Rules 110–118",
                "Receipts; return of registered document; loss of receipt; objection to return; registration after stamp adjudication → release / collection",
            ],
            [
                "Rule 116",
                "Registration of impounded document after stamp adjudication",
            ],
        ],
        col_widths=[2.2, 4.6],
    )

    add_heading_custom(doc, "C. Govt / Institutional e-filing", level=3)
    add_table(
        doc,
        ["Rule", "Relevance"],
        [
            [
                "Rule 40(i)",
                "Normal docs presented in person — except documents forwarded under Sec. 89",
            ],
            [
                "Rule 40(ii)",
                "Doc under Sec. 88(2) may be presented through a messenger with covering letter of Govt officer / public functionary",
            ],
            [
                "Rule 40(iii)",
                "Not accepted by post, except as otherwise provided in law",
            ],
            [
                "Rule 41–45",
                "Examination, defects, presentation endorsement (also applies after institutional intake)",
            ],
            [
                "Rule 12",
                "Filing of copies/translations (links to Rule 17(ii))",
            ],
        ],
        col_widths=[1.8, 5.0],
    )

    add_heading_custom(doc, "5.3 Notifications / amendments", level=2)
    add_table(
        doc,
        ["Notification", "Effect for this topic"],
        [
            [
                "Karnataka Registration Rules, 1965 (under Registration Act Sec. 69)",
                "Parent instrument for Rule 17 and pending procedures",
            ],
            [
                "RGN 2/2002-03 (1 Apr 2002; w.e.f. 4 Apr 2002)",
                "Rule 19-A document sheets; Rules 22-A–22-C; Rule 40 photograph / digital photo — applies when institutional filings are registered/endorsed",
            ],
            [
                "RGN/287/02-03 (29 Mar 2003)",
                "Document sheet specifications",
            ],
            [
                "Karnataka Registration (Amendment) Rules, 1971 (and later GSRs)",
                "Amendments to Rule 17 Parts IV–V and related filing text",
            ],
            [
                "Stamp / fee notifications (e.g. RD/46/MNMU/2025)",
                "Fee columns on pending-release screens; not the filing authority itself",
            ],
            [
                "Registration (Karnataka Amendment) Act, 2023 (Act 47 of 2024)",
                "Secs. 22-B–22-D — refusal/cancellation can generate Rule 17(iii)-type communications",
            ],
        ],
        col_widths=[3.0, 3.8],
    )

    add_heading_custom(doc, "5.4 Pain points", level=2)

    add_heading_custom(doc, "1. Rule 17(2) / Rule 17(3) filing", level=3)
    add_table(
        doc,
        ["Pain point", "Evidence"],
        [
            ["Rule 17(3) filing cannot be saved", "RULE 17 (3) Not save (30558)"],
            [
                "Rule 17(3) endorsement sheet not generated in DEO login",
                "“Rule 17(3) Unable to generate endorsement sheet in the DEO login” (95069, 94894, 94647, 94312 — pending count 1)",
            ],
            [
                "Rule 17(3) / null-and-void entry problems",
                "Document No.05436/2012-13, null and void in rule 17/3 (30223); generic Rule 17(3) (22825 P1)",
            ],
            [
                "Rule 17(iii) filing not working / unclear in Kaveri 2.0",
                "Filing of document as per rule 17(iii) (13048)",
            ],
            [
                "Rule 17 Part-VI entry",
                "Entry vide Rule 17 Part-VI (16176) — part not clearly supported / mapped in K2",
            ],
            [
                "Rule 17 not enabled / guidance needed in Kaveri 2.0",
                "Request to allow operation of Rule 17 in Kaveri 2.0 per Special Collector order (16501 P1)",
            ],
            [
                "Related Book-1 Part-IV institutional filing stuck at DSC",
                "FRUITS / Book-1 Part-IV docs unable to digital sign (28216)",
            ],
        ],
        col_widths=[2.8, 4.0],
    )
    add_para(
        doc,
        "Note: Explicit Rule 17(2) tickets are scarce; most named tickets are Rule 17(3) / 17(iii). Memo filing (Secs. 64–67 / Rule 17 Part I–related) also fails often — see below.",
        size=9.5,
        space_after=8,
    )

    add_heading_custom(doc, "2. Old pending release module", level=3)
    add_para(
        doc,
        "Categorized under Pending document Registration (pending count 7).",
        size=10,
        space_after=4,
    )
    add_table(
        doc,
        ["Pain point", "Evidence"],
        [
            [
                "Cannot release pending documents",
                "Unable to release pending document (17870, 7911, 10870, 20667, 27481, 27696, 30254…); citizen unable to release (29388)",
            ],
            [
                "Cannot retrieve / import Kaveri-1 pending docs into K2",
                "Unable to retrieve (11104, 11550, 26384, 30808); K1 import issue (24116, 29902); “No Property Details Found” (30957); unable to register K1 pending (30603, 30795)",
            ],
            [
                "Pending shows in wrong place (not Minute Book)",
                "Pending app in SR Step 1 instead of Minute Book (22599, 31762); K1 pending release shows in Citizen Book Appointment instead of SR Minute Book (26982)",
            ],
            [
                "After Minute Book / DR approval, property details won’t save",
                "“Unable to save property numbers after DR approval (Pending release from Minute Book)” (95370)",
            ],
            [
                "Pending for condonation of delay stuck",
                "Delay condonation issues (18075, 18302, 20097, 21145, 23198); Categorized: pending for condonation + 45-A (93336, 93031, 92988… — count 6)",
            ],
            [
                "45-A undervaluation pending cannot be released",
                "Unable to release 45-A (13204, 14582, 28425, 31209–31212, 30735…); wrong step (25815, 28393); pending still got registration number (19525, 30452, 31653)",
            ],
            [
                "After release, fee/challan / integration broken",
                "Stamp duty / fee / cess / challan columns blank on 45-A pending release (30156); J-slip not sent after 45-A pending release (21405, 23789, 27544); extra stamp/fee entry needed at registration of 45-A pending (18425)",
            ],
            [
                "Impound-related pending",
                "Impound related issue (30024)",
            ],
            [
                "Old (pre-2003) pending — party details cannot be entered",
                "Unable to enter executant details for pending prior to 2003 (31315)",
            ],
            [
                "Cannot generate application for old pending",
                "Unable to generate application of Pending Doc No.28/2010-11 (14577 P1)",
            ],
            [
                "Pending number not on department summary",
                "Pending number not reflecting in dept summary (92285, 90623)",
            ],
        ],
        col_widths=[2.8, 4.0],
    )

    add_heading_custom(doc, "3. E-filing from Govt / Institutional", level=3)
    add_heading_custom(doc, "A. FRUITS / bank–institutional e-filing", level=4)
    add_table(
        doc,
        ["Pain point", "Evidence"],
        [
            [
                "FRUITS applications not visible in SR login though bank says submitted",
                "15467, 10061",
            ],
            ["SRO code not mapped (intake fails)", "24581, 25905, 27404"],
            ["Owner name truncated (100-char limit)", "25107"],
            ["Unable to clear / complete FRUITS filing", "27622"],
            ["Digital sign fails on FRUITS / Book-1 Part-IV", "28216; also 85981"],
            ["Junk FRUITS apps stuck in Step-1 needing delete", "22716"],
        ],
        col_widths=[3.4, 3.4],
    )
    add_heading_custom(doc, "B. Court / institutional order entry", level=4)
    add_table(
        doc,
        ["Pain point", "Evidence"],
        [
            ["Court entry not reflecting in citizen login after dept entry", "5184"],
            ["OTP / cancel court case failures", "94903, 93570, 95596, 93179…"],
            ["Wrong survey / wrong jurisdiction after save", "29744, 43971"],
        ],
        col_widths=[3.4, 3.4],
    )
    add_heading_custom(doc, "C. Memo filing (Rule 17 Part I–related)", level=4)
    add_table(
        doc,
        ["Pain point", "Evidence"],
        [
            ["Unable to file memo K1 → K2", "8354, 11076, 22543, 23933"],
            ["Memo not received at destination SRO / wrong location", "29153, 63230"],
            ["General memo filing failures", "18566, 23172, 27438, 28251, 29096"],
        ],
        col_widths=[3.4, 3.4],
    )

    add_heading_custom(doc, "5.5 User stories", level=2)

    add_heading_custom(doc, "Rule 17(i) — Book 1 supplements", level=3)
    add_story(
        doc,
        "US-17.1",
        "Sub-Registrar / DEO",
        "file court/revenue/bank/maps/memo papers into the correct Book 1 supplement part",
        "institutional filings are stored in the right official folder",
    )
    add_story(
        doc,
        "US-17.2",
        "Govt / Court / Bank sender",
        "submit sale certificates, Land Acquisition statements, loan papers, or maps for filing",
        "they are recorded under Rule 17(i) without treating them as a normal citizen deed",
    )

    add_heading_custom(doc, "Rule 17(ii) — Copies and translations", level=3)
    add_story(
        doc,
        "US-17.3",
        "citizen / presentant",
        "submit a translation/copy when my document is in an unknown language (Sec. 19/62)",
        "the SRO can examine and register my document",
    )
    add_story(
        doc,
        "US-17.4",
        "Sub-Registrar / DEO",
        "store the copy/translation in a separate Rule 17(ii) file and link it to the register entry",
        "extra papers are preserved and easy to retrieve later",
    )

    add_heading_custom(doc, "Rule 17(iii) — Cancel / modify / correct communications", level=3)
    add_story(
        doc,
        "US-17.5",
        "other department / court / revenue officer",
        "send a cancellation, modification, or rectification communication for an already filed/registered paper",
        "the registration office records the later change",
    )
    add_story(
        doc,
        "US-17.6",
        "Sub-Registrar / DEO",
        "file that communication under Rule 17(iii) and cross-link it to the original entry",
        "anyone searching later can see the document was cancelled, modified, or corrected",
    )

    add_heading_custom(doc, "5.6 Open query (from source)", level=2)
    add_bullet(
        doc,
        "If paperless, whether the template should be generated for the required languages.",
    )

    # =====================================================================
    # 07-09-2026 to 08-09-2026 — Registration Appeal & Will after death
    # =====================================================================
    page_break(doc)
    add_heading_custom(
        doc,
        "6. 07-09-2026 to 08-09-2026 — Registration Appeal & Will After Death of Testator",
        level=1,
    )
    add_meta_table(
        doc,
        [
            ["Date", "07-09-2026 to 08-09-2026"],
            [
                "Topics",
                "Registration Appeal and Will After the death of the testator documents",
            ],
            [
                "Attendees",
                "Kaveri IT Cell, AIGR Computers team, Domain Expert and committee members",
            ],
            [
                "Version",
                "1.1 (08-09-2026) — Acts, sections, Rules and notifications added for Registration Appeal and Will After the death of the testator",
            ],
            ["Source", "Document_Registration_requirement_07092026_v1.1.docx"],
        ],
    )
    add_para(
        doc,
        "Scope: (1) Registration Appeal against refusal / related Registrar orders; "
        "(2) Will after the death of the testator (presentation / registration and "
        "proceedings on deposited sealed covers). Source folder referenced in note: Acts_Rules/Document/.",
        size=10.5,
        space_after=8,
    )

    add_heading_custom(doc, "6.1 Primary Acts", level=2)
    add_table(
        doc,
        ["Act / instrument", "Role", "Relevance to topics"],
        [
            [
                "The Registration Act, 1908 (Central Act 16 of 1908)",
                "Primary",
                "Registration Appeal (Part XII — Secs. 71–77); Wills presentation & deposit (Parts VIII–IX — Secs. 40–46); wills may be presented/deposited at any time (Sec. 27); optional registration of wills (Sec. 18)",
            ],
            [
                "The Registration (Karnataka Amendment) Act, 2023 (Karnataka Act 47 of 2024)",
                "Related — Appeal",
                "Sec. 22-D — appeal against District Registrar’s order cancelling registration under Sec. 22-C (forged / prohibited documents)",
            ],
            [
                "The Karnataka Registration Rules, 1965",
                "Primary (Rules)",
                "Appeals & enquiries (Ch. XXV — Rules 175–191); Wills / authorities to adopt (Ch. XIV — Rules 83–86); sealed covers containing wills (Ch. XV — Rules 87–93); withdrawal of sealed covers (Ch. XXXII — Rule 213)",
            ],
            [
                "The Indian Succession Act, 1925",
                "Related — Will after death (reference)",
                "Probate / letters of administration and succession proof often accompany post-death will registration or opening of deposited sealed covers — confirm with Domain Expert whether Kaveri 3.0 captures probate/court order as a prerequisite",
            ],
        ],
        col_widths=[2.4, 1.4, 3.0],
    )

    add_heading_custom(doc, "6.2 Relevant sections", level=2)
    add_heading_custom(doc, "6.2.1 Registration Appeal", level=3)
    add_table(
        doc,
        ["Section", "Topic", "BRD / system relevance"],
        [
            [
                "Sec. 71",
                "Reasons for refusal to register to be recorded",
                "SRO must record reasons — starting point for appeal / application",
            ],
            [
                "Sec. 72",
                "Appeal to Registrar — refusal on ground other than denial of execution",
                "Primary Registration Appeal path to District Registrar",
            ],
            [
                "Sec. 73",
                "Application to Registrar — refusal on ground of denial of execution",
                "Separate application (not styled as Sec. 72 appeal) when execution is denied",
            ],
            [
                "Sec. 74",
                "Procedure of Registrar on such application",
                "Enquiry workflow at DR login",
            ],
            [
                "Sec. 75",
                "Order by Registrar to register and procedure thereon",
                "Direction to register; re-presentation / status 'Ordered to register'",
            ],
            [
                "Sec. 76",
                "Order of refusal by Registrar",
                "DR refusal — end of departmental appeal (unless Sec. 22-D path applies)",
            ],
            [
                "Sec. 77",
                "Suit in case of order of refusal by Registrar",
                "Civil Court suit within 30 days — court-ordered registration status",
            ],
            [
                "Sec. 22-D (Kar. Amd. 2023)",
                "Appeal against District Registrar cancellation under Sec. 22-C",
                "Appeal of forged/prohibited document cancellation — parallel appeal track",
            ],
            [
                "Sec. 68",
                "Power of Registrar to superintend and control Sub-Registrars",
                "DR oversight of SRO refusal / appeal handling",
            ],
        ],
        col_widths=[1.6, 2.4, 2.8],
    )

    add_heading_custom(doc, "6.2.2 Will After the death of the testator", level=3)
    add_table(
        doc,
        ["Section", "Topic", "BRD / system relevance"],
        [
            [
                "Sec. 18",
                "Documents of which registration is optional — includes wills",
                "Will registration is optional (not compulsory under Sec. 17)",
            ],
            [
                "Sec. 27",
                "Wills may be presented or deposited at any time",
                "No 4-month presentation bar for wills — including after death of testator",
            ],
            [
                "Sec. 40",
                "Persons entitled to present wills and authorities to adopt",
                "Who may present after death (executor / legatee / person claiming under will)",
            ],
            [
                "Sec. 41",
                "Registration of wills and authorities to adopt",
                "Procedure for registering a will when presented (Book 3)",
            ],
            [
                "Sec. 42",
                "Deposit of wills",
                "Sealed-cover deposit with Registrar during testator’s lifetime",
            ],
            [
                "Sec. 43",
                "Procedure on deposit of wills",
                "Receipt / entry of deposited sealed cover",
            ],
            [
                "Sec. 44",
                "Withdrawal of sealed cover deposited under Sec. 42",
                "Testator may withdraw sealed cover during lifetime",
            ],
            [
                "Sec. 45",
                "Proceedings on death of depositor",
                "Core section for Will after death of testator — opening / delivery of deposited sealed cover to Court or entitled person as prescribed",
            ],
            [
                "Sec. 46",
                "Saving of certain enactments and powers of Courts",
                "Court powers over wills / probate not affected",
            ],
            [
                "Sec. 51",
                "Register-books — Book 3 (wills and authorities to adopt)",
                "Statutory book for will registration entries",
            ],
        ],
        col_widths=[1.4, 2.6, 2.8],
    )

    add_heading_custom(doc, "6.3 Primary Rules — Karnataka Registration Rules, 1965", level=2)
    add_heading_custom(doc, "6.3.1 Registration Appeal", level=3)
    add_table(
        doc,
        ["Rule", "Requirement", "System feature"],
        [
            [
                "Rule 171–174 (Ch. XXIV)",
                "Refusal to register — reasons; partial refusal; etc.",
                "Pre-appeal refusal record at SRO",
            ],
            [
                "Rule 175",
                "Appeal against refusal",
                "Intake of Sec. 72 appeal",
            ],
            [
                "Rule 176",
                "Appeal by whom to be preferred",
                "Who can file the appeal",
            ],
            [
                "Rule 177",
                "Persons who can appear in an enquiry connected with a will or authority to adopt",
                "Cross-link — will-related enquiry appearance",
            ],
            [
                "Rule 179–180",
                "Procedure of disposing appeal; endorsement on order",
                "DR enquiry and order endorsement",
            ],
            [
                "Rule 181",
                "Appeal against refusal to register a will",
                "Specific appeal path when the refused document is a will",
            ],
            [
                "Rule 182–183",
                "Refusal based on non-appearance; communication of orders",
                "Special refusal / notice workflow",
            ],
            [
                "Rule 184 / 188",
                "Registration ordered by Registrar or Court; order directing registration after enquiry",
                "Re-presentation and registration after successful appeal / court order",
            ],
            [
                "Rule 185–187, 190–191",
                "File of appeal orders; refusal orders; no appeal when returned at presentant’s request; limitation on appeals",
                "Appeal file maintenance, limitation and exclusions",
            ],
            [
                "Rule 108–109",
                "Endorsement on document registered under Sec. 74; presented by order of Registrar or Court",
                "Endorsement templates after appeal / court direction",
            ],
        ],
        col_widths=[1.8, 2.6, 2.4],
    )

    add_heading_custom(doc, "6.3.2 Will After the death of the testator", level=3)
    add_table(
        doc,
        ["Rule", "Requirement", "System feature"],
        [
            [
                "Rule 83",
                "Registration of a Will or authority to adopt",
                "SRO/DR procedure when will is presented for registration",
            ],
            [
                "Rule 84",
                "Return of Will or authority to adopt after the death of Testator — unregistered",
                "Directly covers Will after death of the testator when still unregistered",
            ],
            [
                "Rule 85",
                "Registration of revocation or cancellation of a Will or authority to adopt",
                "Revocation / cancellation registration",
            ],
            [
                "Rule 86",
                "Unclaimed Wills",
                "Custody / disposal of unclaimed wills",
            ],
            [
                "Rules 87–89",
                "Sealed covers — manner of entries; deposit by persons; wills sent by post",
                "Deposit workflow (lifetime deposit under Sec. 42)",
            ],
            [
                "Rules 90–93",
                "Endorsements when sealed cover is sent to Court; forwardal; opening procedure",
                "Post-death opening / Court production of deposited will (Sec. 45)",
            ],
            [
                "Rule 213 (Ch. XXXII)",
                "Withdrawal of sealed covers",
                "Withdrawal under Sec. 44",
            ],
            [
                "Rule 177 / 181",
                "Enquiry appearance for will; appeal against refusal to register a will",
                "Overlap with Registration Appeal when will registration is refused",
            ],
        ],
        col_widths=[1.8, 2.6, 2.4],
    )

    add_heading_custom(doc, "6.4 Notifications / amendments", level=2)
    add_table(
        doc,
        ["Instrument", "Effect", "Topics"],
        [
            [
                "The Karnataka Registration Rules, 1965 (under Registration Act Sec. 69)",
                "Parent subordinate legislation for appeal and will procedures",
                "Both topics",
            ],
            [
                "RGN 2/2002-03 (1 Apr 2002; w.e.f. 4 Apr 2002)",
                "Document sheets; photograph / digital photo at presentation (Rule 40) — applies when a will is presented for registration",
                "Will registration",
            ],
            [
                "The Registration (Karnataka Amendment) Act, 2023 — Gazette Extra-ordinary No. 480 (19 Oct 2024)",
                "Secs. 22-B–22-D, 81-A–81-B — refusal/cancellation of forged documents and appeal under Sec. 22-D",
                "Registration Appeal (cancellation track)",
            ],
            [
                "RD 403 ESR 85 / RD/46/MNMU/2025 (registration fee table under Sec. 78)",
                "Fee for appeal / application / will registration or deposit as per notified Table of Fees",
                "Both topics — fee masters",
            ],
            [
                "Karnataka Registration (Amendment) Rules / GSR notifications cited in Rules 1965 (incl. 1971 onwards)",
                "Amendments to will / sealed-cover / appeal procedure text embedded in Rules PDF",
                "Both topics",
            ],
        ],
        col_widths=[2.6, 2.6, 1.6],
    )

    add_heading_custom(doc, "6.5 Pain points", level=2)
    add_para(
        doc,
        "No ServiceDesk pain-point mapping was attached to the 07–08 Sep 2026 source note.",
        size=10.5,
    )

    add_heading_custom(doc, "6.6 User stories", level=2)
    add_para(
        doc,
        "Derived from 07–08 Sep 2026 Acts, sections and Rules (source note had no User Stories section).",
        size=10,
        space_after=8,
    )

    add_heading_custom(doc, "Registration Appeal", level=3)
    for s in [
        (
            "US-APL-01",
            "Sub-Registrar",
            "record reasons for refusal under Sec. 71 (and Rules 171–174)",
            "the presentant has a clear starting point for appeal or Sec. 73 application",
        ),
        (
            "US-APL-02",
            "citizen / presentant",
            "file a Sec. 72 appeal to the District Registrar when refusal is on a ground other than denial of execution",
            "my case is taken up on the primary Registration Appeal path",
        ),
        (
            "US-APL-03",
            "citizen / presentant",
            "file a Sec. 73 application when refusal is for denial of execution",
            "the denial-of-execution track is handled separately from a Sec. 72 appeal",
        ),
        (
            "US-APL-04",
            "District Registrar",
            "run the Sec. 74 enquiry, dispose the appeal under Rules 179–180, and order registration (Sec. 75) or refuse (Sec. 76)",
            "appeal outcomes and endorsements are complete and auditable",
        ),
        (
            "US-APL-05",
            "citizen / presentant",
            "re-present the document for registration after a Registrar or Court order (Rules 184 / 188; Rules 108–109)",
            "status moves to 'Ordered to register' and registration can complete",
        ),
        (
            "US-APL-06",
            "citizen / presentant",
            "pursue Sec. 77 civil suit within 30 days after DR refusal, or Sec. 22-D appeal against Sec. 22-C cancellation",
            "court-ordered registration and forged/prohibited cancellation appeals are supported",
        ),
    ]:
        add_story(doc, *s)

    add_heading_custom(doc, "Will After the death of the testator", level=3)
    for s in [
        (
            "US-WILL-01",
            "executor / legatee / person claiming under the will",
            "present a will for registration after the testator’s death under Secs. 27, 40 and 41 (Book 3), without the ordinary 4-month bar",
            "optional will registration can proceed post-death",
        ),
        (
            "US-WILL-02",
            "testator (during lifetime)",
            "deposit a sealed-cover will with the Registrar (Secs. 42–43; Rules 87–89) and withdraw it if needed (Sec. 44; Rule 213)",
            "lifetime deposit and withdrawal are recorded correctly",
        ),
        (
            "US-WILL-03",
            "entitled person / Court / District Registrar",
            "open or forward a deposited sealed cover after death of the depositor under Sec. 45 and Rules 90–93",
            "proceedings on death of depositor follow the prescribed sealed-cover workflow",
        ),
        (
            "US-WILL-04",
            "Sub-Registrar / District Registrar",
            "return an unregistered will after death of the testator under Rule 84, register revocation/cancellation under Rule 85, and manage unclaimed wills under Rule 86",
            "post-death will custody and related registrations are handled",
        ),
        (
            "US-WILL-05",
            "citizen / presentant",
            "appeal refusal to register a will under Rule 181 (with Rule 177 enquiry appearance where applicable)",
            "will-registration refusals use the correct appeal path",
        ),
    ]:
        add_story(doc, *s)

    add_heading_custom(doc, "6.7 Open query (from source)", level=2)
    add_bullet(
        doc,
        "Confirm with Domain Expert whether Kaveri 3.0 should capture probate / letters of administration / court order "
        "(Indian Succession Act, 1925) as a prerequisite for post-death will registration or opening of deposited sealed covers.",
    )

    # =====================================================================
    # 08-09-2026 (Sr.18) — Sec. 68(2) correction & Cross-reference Rule 123
    # =====================================================================
    page_break(doc)
    add_heading_custom(
        doc,
        "7. 08-09-2026 — Sec. 68(2) correction & Cross-reference Rule 123",
        level=1,
    )
    add_meta_table(
        doc,
        [
            ["Date", "08-09-2026"],
            [
                "Topics",
                "Sec. 68(2) correction and Cross-reference Rule 123 — Schedule Sr.18; modules #14, #15",
            ],
            [
                "Attendees",
                "Kaveri IT Cell, AIGR Computers team, Domain Expert and committee members",
            ],
            [
                "Version",
                "1.1 (15-09-2026) — Acts, sections, Rules, notifications, pain points and user stories for Sec. 68(2) correction and Rule 123 cross-reference",
            ],
            [
                "Source",
                "Document_Registration_requirement_08092026_v1.1.docx",
            ],
        ],
    )
    add_para(
        doc,
        "Scope: (1) Sec. 68(2) correction of errors regarding the book or office in which a document was "
        "registered (wrong book / wrong office / related rectification under District Registrar’s order); "
        "(2) Cross-reference under Rule 123 when a later document or communication revokes, cancels, "
        "rectifies or modifies a previously registered or Rule 17-filed entry, including index notes.",
        size=10.5,
        space_after=8,
    )

    add_heading_custom(doc, "7.1 Primary Acts", level=2)
    add_table(
        doc,
        ["Act / instrument", "Role", "Relevance to topics"],
        [
            [
                "The Registration Act, 1908 (Central Act 16 of 1908)",
                "Primary — Sec. 68(2) correction",
                "Sec. 68(2) — DR may order rectification of any error regarding the book or office of registration; Sec. 68(1) — SRO under DR control; Secs. 51, 54–55 — books and indexes after correction",
            ],
            [
                "The Karnataka Registration Rules, 1965",
                "Primary (Rules) — 68(2) correction & Rule 123 cross-reference",
                "Ch. XXIII Rules 167–169 — wrong book / wrong office under Sec. 68; Rule 123 — mutual footnotes and index notes; Rule 165 — memorandum erratum and index cross-references",
            ],
        ],
        col_widths=[2.4, 1.8, 2.6],
    )

    add_heading_custom(doc, "7.2 Relevant sections", level=2)
    add_heading_custom(doc, "7.2.1 Sec. 68(2) correction", level=3)
    add_table(
        doc,
        ["Section", "Topic", "BRD / system relevance"],
        [
            [
                "Sec. 68(1)",
                "Registrar superintendence and control of Sub-Registrars",
                "DR owns oversight of SRO acts / omissions feeding correction cases",
            ],
            [
                "Sec. 68(2)",
                "Registrar’s order to rectify error regarding book or office of registration",
                "Core 68(2) correction module — DR order (complaint or suo motu) for wrong book / wrong office / related error",
            ],
            [
                "Sec. 51",
                "Register-books to be kept",
                "Target book / volume / page after correction must match statutory books",
            ],
            [
                "Secs. 54–55",
                "Indexes Nos. I–IV",
                "Index entries corrected / cross-referenced when book or particulars are rectified",
            ],
            [
                "Secs. 64–66",
                "Memoranda / copies to other offices",
                "Wrong-office / wrong-book corrections may require free re-forwardal (Rules 168–169)",
            ],
        ],
        col_widths=[1.4, 2.6, 2.8],
    )
    add_heading_custom(doc, "7.2.2 Cross-reference Rule 123 (context)", level=3)
    add_table(
        doc,
        ["Section", "Topic", "BRD / system relevance"],
        [
            [
                "Sec. 89 / Rule 17 filing",
                "Documents / returns filed under Sec. 89 and Rule 17 supplements",
                "Rule 123 also applies when a later document/communication affects a Sec. 89 / Rule 17 filed paper",
            ],
            [
                "Sec. 17 / optional & compulsory registration",
                "Later deed that revokes, cancels, rectifies or modifies an earlier deed",
                "New registration under ordinary rules; Rule 123 then places cross-notes on both entries",
            ],
        ],
        col_widths=[1.8, 2.4, 2.6],
    )

    add_heading_custom(doc, "7.3 Relevant Rules — Karnataka Registration Rules, 1965", level=2)
    add_heading_custom(doc, "7.3.1 Sec. 68(2) correction / Errors in Registration", level=3)
    add_table(
        doc,
        ["Rule", "Requirement", "System feature"],
        [
            [
                "Rule 167 (Ch. XXIII)",
                "Wrong Book — DR sanction; fresh copy in proper book; red-ink footnotes both ways; indexes cross-referenced",
                "68(2) wrong-book correction workflow",
            ],
            [
                "Rule 168",
                "Memo/copy under Secs. 64–67 for wrong Book — error notice / fresh memo free of cost",
                "Cross-office memo repair after wrong-book registration",
            ],
            [
                "Rule 169",
                "Wrong office — apply to Registrar under Sec. 68; re-register without fee; free memo to proper office",
                "Core 68(2) wrong-office correction path",
            ],
            [
                "Rule 165",
                "Memorandum corrections — erratum in Supplement Book 1 Part I; index cross-references",
                "Memo / index correction supporting 68(2) consistency",
            ],
        ],
        col_widths=[1.6, 2.8, 2.4],
    )
    add_heading_custom(doc, "7.3.2 Cross-reference Rule 123", level=3)
    add_table(
        doc,
        ["Rule", "Requirement", "System feature"],
        [
            [
                "Rule 123(i)",
                "Mutual footnotes when a later document/communication revokes, cancels, rectifies or modifies an earlier registered / Rule 17-filed entry",
                "Bidirectional cross-reference notes (Document No. / volume / page / supplement)",
            ],
            [
                "Rule 123(ii)",
                "Index No. II note for immovable property; index-item rectification notes in Indexes I–IV",
                "Index cross-reference and item rectification",
            ],
            [
                "Rule 124 (related)",
                "Note when Court declares registered document a forgery / false personation",
                "Related foot-note path (not primary Rule 123 revoke/modify track)",
            ],
            [
                "Rule 17 (related)",
                "Supplement parts that Rule 123 may point to",
                "Cross-link targets include Rule 17 filed papers and Sec. 89 returns",
            ],
        ],
        col_widths=[1.6, 2.8, 2.4],
    )

    add_heading_custom(doc, "7.4 Notifications / amendments", level=2)
    add_table(
        doc,
        ["Instrument", "Effect", "Topics"],
        [
            [
                "The Karnataka Registration Rules, 1965 (under Registration Act Sec. 69)",
                "Parent rules for Errors in Registration (Ch. XXIII) and Rule 123 notes",
                "Both topics",
            ],
            [
                "RD 403 ESR 85 / RD/46/MNMU/2025 (Table of Fees under Sec. 78)",
                "Fresh registration under Rule 169 after Sec. 68 direction is without fee",
                "68(2) correction — fee exception",
            ],
            [
                "ServiceDesk / Kaveri 2.0 68(2) correction module practice",
                "Operational 68(2) correction, re-scan, index correction and verify steps — re-engineer in Kaveri 3.0",
                "68(2) correction — as-is pain points",
            ],
        ],
        col_widths=[2.6, 2.6, 1.6],
    )

    add_heading_custom(doc, "7.5 Pain points", level=2)
    add_para(
        doc,
        "Source: ServiceDeskIssuesList.xlsx — tickets naming 68(2) / 68 correction.",
        size=10.5,
        space_after=4,
    )
    for rid, subj in [
        ("8788", "68(2) note Re-scanning issue"),
        ("15135", "68(2) correction module Hobli name not working"),
        ("18321", "68(2) Verification issue"),
        ("19748", "68 correction not able to verify document"),
        ("20158", "68(2) Rescan completed but not reflecting in KOS while applying for CC"),
        ("20763 / 20772", "68(2) correction module issue / MODULE error"),
        ("21319 / 27261 / 28486", "68 correction error / unable to update / section correction issue"),
        ("29418", "68(2) Index Correction"),
        ("29586 / 31576", "68(2) correction Issue (e.g. SRO Nelamangala) / 68(2) correction"),
    ]:
        add_bullet(doc, subj, bold_prefix=f"{rid}: ")

    add_heading_custom(doc, "7.6 User stories", level=2)
    add_para(
        doc,
        "Taken from Document_Registration_requirement_08092026_v1.1.docx §6 "
        "(Schedule Sr.18 — modules #14, #15).",
        size=10,
        space_after=8,
    )
    add_heading_custom(doc, "Sec. 68(2) correction", level=3)
    for s in [
        (
            "US-682-01",
            "citizen / executant / claimant",
            "complain to the District Registrar under Sec. 68(2) that my document was registered in the wrong book or wrong office (or has a related registration error)",
            "the Registrar can issue a rectification order consistent with the Act",
        ),
        (
            "US-682-02",
            "District Registrar",
            "issue a Sec. 68(2) order (on complaint or otherwise) directing rectification of the book or office error, and track the case to closure",
            "SRO action and status are auditable against the Registrar’s order",
        ),
        (
            "US-682-03",
            "Sub-Registrar",
            "after DR sanction under Rule 167, re-copy a wrong-book entry into the proper book with red-ink footnotes both ways and create proper index entries with cross-references (without cancelling the original serial)",
            "both books and indexes remain consistent and searchable",
        ),
        (
            "US-682-04",
            "Sub-Registrar / citizen",
            "complete wrong-office correction under Rule 169 — advise parties, receive Sec. 68 direction, re-register without fee with endorsement citing the order, and forward free memo/copy to the proper office",
            "the document is correctly recorded in the proper office without double fee",
        ),
        (
            "US-682-05",
            "Sub-Registrar / DEO",
            "send an erratum for a memorandum/copy under Rule 165 / 168, file it in Supplement Book 1 Part I, correct indexes with cross-references, and re-scan / verify corrected pages where the module requires it",
            "cross-office copies and citizen CC/EC views show the corrected record",
        ),
    ]:
        add_story(doc, *s)

    add_heading_custom(doc, "Cross-reference Rule 123", level=3)
    for s in [
        (
            "US-123-01",
            "Sub-Registrar / DEO",
            "auto-prompt and save Rule 123(i) mutual footnotes on both entries (Document No., volume, page, supplement part) when registering a deed that revokes, cancels, rectifies or modifies an earlier registered or Rule 17-filed document",
            "anyone reading either entry sees the linked revoke/modify relationship",
        ),
        (
            "US-123-02",
            "Sub-Registrar / DEO",
            "on receipt of a Revenue Officer or Court communication that similarly revokes / cancels / rectifies / modifies a filed or registered paper, file the communication and apply the same Rule 123 cross-notes",
            "institutional modifications are visible from both the old and new records",
        ),
        (
            "US-123-03",
            "Sub-Registrar / DEO",
            "for immovable-property cases, write the corresponding Index No. II note, and when an index item is rectified write the note in Index I/II/III/IV under Rule 123(ii)",
            "property and name indexes stay aligned with the register footnotes",
        ),
        (
            "US-123-04",
            "citizen / search user",
            "see Rule 123 cross-references when I search, take EC, or view a certified copy of either the original or the later modifying document",
            "I am not misled by an obsolete register entry that was later modified",
        ),
    ]:
        add_story(doc, *s)

    add_heading_custom(doc, "7.7 Open notes (from source)", level=2)
    add_bullet(
        doc,
        "Rule 123 mutual footnotes are distinct from Sec. 68(2) rectification of wrong book/office.",
    )
    add_bullet(
        doc,
        "Pre-registration “send back for correction” in the SR approval workflow (28-08 discussion) is a separate intake path.",
    )
    add_bullet(
        doc,
        "Sec. 22-B/22-C forged/prohibited cancellation (Kar. Amd. 2023) is a parallel track, not the Rule 123 revoke/modify note.",
    )

    # =====================================================================
    # 09-09-2026 to 10-09-2026 (Sr.19) — Integration / exemption / Court / Liability
    # =====================================================================
    page_break(doc)
    add_heading_custom(
        doc,
        "8. 09-09-2026 to 10-09-2026 — Integration, Exemption, Court entry & Liability",
        level=1,
    )
    add_meta_table(
        doc,
        [
            ["Date", "09-09-2026 to 10-09-2026"],
            [
                "Topics",
                "Integration module; Integration exemption; Court entry; Liability — Schedule Sr.19; modules #3, #16, #17, #18",
            ],
            [
                "Attendees",
                "Kaveri IT Cell, AIGR Computers team, Domain Expert and committee members",
            ],
            [
                "Version",
                "1.1 (15-09-2026) — Acts, sections, Rules, notifications, pain points and user stories for Integration, Integration exemption, Court entry and Liability",
            ],
            [
                "Source",
                "Document_Registration_requirement_09092026_v1.1.docx",
            ],
        ],
    )
    add_para(
        doc,
        "Scope: (1) Integration module — post-registration push to Bhoomi / RDPR / related systems via Integration Report; "
        "(2) Integration exemption — deed / Sec. 90 / stamp-exempt classes that skip or specially handle external push; "
        "(3) Court entry — Sec. 89 / Rule 17 Court certificates and Court-order capture; "
        "(4) Liability — DR liability filing that must appear correctly on EC / property search.",
        size=10.5,
        space_after=8,
    )

    add_heading_custom(doc, "8.1 Primary Acts", level=2)
    add_table(
        doc,
        ["Act / instrument", "Role", "Relevance to topics"],
        [
            [
                "The Registration Act, 1908 (Central Act 16 of 1908)",
                "Primary — Court entry; Integration context; Liability visibility",
                "Sec. 89 — Court/revenue certificates filed in Book 1; Secs. 64–67 — outbound memo pattern for integration; Sec. 90–91 — Govt document exemption; Sec. 57 / EC — liability visibility",
            ],
            [
                "The Karnataka Registration Rules, 1965",
                "Primary (Rules)",
                "Rule 17 Court/institutional supplements; Rules 148–154 EC; Rules 184/188 Court-ordered registration; Rule 166 Court decree copies",
            ],
            [
                "The Karnataka Stamp Act, 1957 (+ Schedule)",
                "Related — Integration exemption (stamp-exempt instruments)",
                "Sec. 3 / Schedule exemptions — 100% stamp-exempt flows and receipt/integration handling",
            ],
        ],
        col_widths=[2.4, 1.8, 2.6],
    )

    add_heading_custom(doc, "8.2 Relevant sections", level=2)
    add_heading_custom(doc, "8.2.1 Integration module", level=3)
    add_table(
        doc,
        ["Section", "Topic", "BRD / system relevance"],
        [
            ["Secs. 64–67", "Memoranda / copies to other offices", "Outbound transmission pattern for Bhoomi / RDPR J-slip / XML push"],
            ["Sec. 60–61", "Certificate of registration; completion", "Integration trigger after registration complete"],
            ["Sec. 51 / Indexes", "Register books and indexes", "Source of truth for Integration Report payloads"],
        ],
        col_widths=[1.4, 2.6, 2.8],
    )
    add_heading_custom(doc, "8.2.2 Integration exemption", level=3)
    add_table(
        doc,
        ["Section", "Topic", "BRD / system relevance"],
        [
            ["Sec. 90", "Exemption of certain Govt documents from registration", "Candidates for Integration exemption / non-push"],
            ["Sec. 91", "Inspection and copies of Sec. 90 documents", "Exempted records remain inspectable"],
            ["Sec. 17 proviso / State exemptions", "State may exempt certain leases etc.", "Configurable exemption master"],
            ["Stamp Act Sec. 3 + Schedule", "Stamp-exempt / remitted instruments", "Exempt registration without false challan/integration failure"],
        ],
        col_widths=[1.8, 2.4, 2.6],
    )
    add_heading_custom(doc, "8.2.3 Court entry", level=3)
    add_table(
        doc,
        ["Section", "Topic", "BRD / system relevance"],
        [
            ["Sec. 89(2)", "Court certificate of sale — file in Book 1", "Primary Court entry statutory path"],
            ["Sec. 89(1),(3),(4)", "Loan / Revenue sale certificates filed in Book 1", "Parallel institutional entry paths"],
            ["Sec. 17", "Decrees and orders of Court", "Court decrees presented or filed as directed"],
            ["Secs. 75 / 77", "Registrar or Court order directing registration", "Court-ordered registration status"],
        ],
        col_widths=[1.4, 2.6, 2.8],
    )
    add_heading_custom(doc, "8.2.4 Liability", level=3)
    add_table(
        doc,
        ["Section", "Topic", "BRD / system relevance"],
        [
            ["Sec. 57 / Rules 148–154", "Search and Certificate of encumbrance", "Liability filings must appear/remove correctly on EC"],
            ["Sec. 68 / Rule 123", "DR control; cross-notes on modification", "Liability order attach / remove under DR control"],
            ["Stamp Act — charge context", "Rights/liabilities; undervaluation references", "Confirm exact statutory instrument for Liability Filing with Domain Expert"],
        ],
        col_widths=[1.8, 2.4, 2.6],
    )

    add_heading_custom(doc, "8.3 Relevant Rules — Karnataka Registration Rules, 1965", level=2)
    add_table(
        doc,
        ["Rule", "Requirement", "System feature"],
        [
            ["Rule 17 (esp. Part I)", "Court / Revenue sale certificates; institutional filings", "Court entry + institutional intake"],
            ["Rules 148–154", "Certificate of encumbrance", "Liability notes on EC"],
            ["Rules 184 / 188", "Registration ordered by Registrar or Court", "Court-directed registration"],
            ["Rule 166", "Copy of memo or decree of a Court", "Court decree copy handling"],
            ["Rule 123", "Cross-notes when communication modifies earlier entry", "Related Court / liability communications"],
            ["Rules 202 / Sec. 88", "Govt officers exempt from personal appearance", "Related institutional presentant exemption"],
        ],
        col_widths=[1.8, 2.6, 2.4],
    )

    add_heading_custom(doc, "8.4 Notifications / amendments", level=2)
    add_table(
        doc,
        ["Instrument", "Effect", "Topics"],
        [
            [
                "The Karnataka Registration Rules, 1965 (under Registration Act Sec. 69)",
                "Parent rules for Rule 17 Court/institutional filing and EC rules",
                "Court entry; Liability (EC)",
            ],
            [
                "RD 403 ESR 85 / RD/46/MNMU/2025 (Table of Fees under Sec. 78)",
                "Fees for filing / copies / EC; exempted instruments fee handling",
                "Integration exemption; Court entry",
            ],
            [
                "Bhoomi / RDPR / land-record integration MoU & technical specs",
                "J-slip / XML push contracts, retry, partial upload",
                "Integration module",
            ],
            [
                "Stamp Schedule / exemption notifications",
                "100% stamp-exempt document classes and receipt display rules",
                "Integration exemption",
            ],
        ],
        col_widths=[2.6, 2.6, 1.6],
    )

    add_heading_custom(doc, "8.5 Pain points", level=2)
    add_para(doc, "Source: ServiceDeskIssuesList.xlsx (OverallList + Categorized).", size=10.5, space_after=4)
    add_heading_custom(doc, "Integration module", level=3)
    for rid, subj in [
        ("11870 / 18110", "Integration Report / Document number not reflected"),
        ("16847 / 19405 / 19669", "Unable to push to Bhoomi / J-slip not showing in Integration Report"),
        ("23558 / 23977 / 29214 / 30472", "Document not in Integration Report"),
        ("28334 / 30496 / 30742", "RDPR/XML/J-slip failures from Integration Report"),
        ("Categorized Bhoomi", "J-slip not generated / partial upload / data not found (large pending counts)"),
    ]:
        add_bullet(doc, subj, bold_prefix=f"{rid}: ")
    add_heading_custom(doc, "Integration exemption", level=3)
    add_bullet(
        doc,
        "Stamp duty 100% exempted documents — challan reference not showing in receipt details",
        bold_prefix="31768: ",
    )
    add_heading_custom(doc, "Court entry", level=3)
    for rid, subj in [
        ("5184", "Court entry not reflecting in citizen login after dept entry"),
        ("21896", "Court entry to be cancelled"),
        ("27219 / 27231", "Court Order Issue"),
        ("29744", "Court order Sy. No. mismatch between FDA and SR login"),
        ("94903 / 93570…", "OTP / cancel court case failures (Categorized)"),
    ]:
        add_bullet(doc, subj, bold_prefix=f"{rid}: ")
    add_heading_custom(doc, "Liability", level=3)
    for rid, subj in [
        ("20687", "Liability Filing issue"),
        ("29127", "Liability financial year issue / FY not reflecting in DR login"),
        ("29332", "Liability need remove in EC"),
        ("30317", "Liability Entry wrongly displaying for different Sy. No. / village"),
        ("95242", "Wrong district SRO names while filing Liability Note"),
        ("95253 / 94932…", "Kaveri 1 documents not fetched for Liability Filing"),
        ("94109", "Unable to fetch liability data in SR and DR login"),
    ]:
        add_bullet(doc, subj, bold_prefix=f"{rid}: ")

    add_heading_custom(doc, "8.6 User stories", level=2)
    add_para(
        doc,
        "Taken from Document_Registration_requirement_09092026_v1.1.docx §6 "
        "(Schedule Sr.19 — modules #3, #16, #17, #18).",
        size=10,
        space_after=8,
    )
    add_heading_custom(doc, "Integration module", level=3)
    for s in [
        (
            "US-INT-01",
            "Sub-Registrar / DEO",
            "see a registered document in the Integration Report after registration completes and push it to Bhoomi / RDPR (or other configured systems) with correct survey, party and office payloads",
            "land-record systems receive a complete J-slip / XML without manual rework",
        ),
        (
            "US-INT-02",
            "Sub-Registrar / support user",
            "re-push or diagnose a failed / missing Integration Report entry (partial upload, reference number not generated, document not listed)",
            "stuck integrations can be cleared without data loss",
        ),
        (
            "US-INT-03",
            "system / integration service",
            "build outbound payloads from the registered Book 1 entry and indexes (Secs. 51, 60–61 pattern) and acknowledge success/failure per target system",
            "audit trail shows what was sent and when",
        ),
    ]:
        add_story(doc, *s)
    add_heading_custom(doc, "Integration exemption", level=3)
    for s in [
        (
            "US-IEX-01",
            "Application Admin / Domain Expert",
            "maintain an Integration exemption master (deed type / article / Sec. 90 class / stamp-exempt class) so selected registrations skip external push",
            "exempt instruments do not clog Integration Report or fail on missing challan data",
        ),
        (
            "US-IEX-02",
            "Sub-Registrar / citizen",
            "complete registration of a 100% stamp-duty exempt document with clear receipt details and without false challan / integration errors",
            "exempt flows finish cleanly",
        ),
    ]:
        add_story(doc, *s)
    add_heading_custom(doc, "Court entry", level=3)
    for s in [
        (
            "US-CRT-01",
            "Court / departmental user",
            "enter or file a Court sale certificate / Court order under Sec. 89(2) and Rule 17 so it is stored in the correct Book 1 supplement",
            "the Court entry is searchable and linked to the right property",
        ),
        (
            "US-CRT-02",
            "Sub-Registrar / FDA",
            "capture Court order property particulars (survey, village, parties) once so the same data appears consistently in citizen and SR logins",
            "citizens see the Court entry and wrong Sy. No. mismatches are avoided",
        ),
        (
            "US-CRT-03",
            "Sub-Registrar",
            "cancel or correct a Court entry when authorised, with OTP / audit where required",
            "erroneous Court entries do not remain visible on citizen search",
        ),
        (
            "US-CRT-04",
            "citizen / presentant",
            "re-present a document for registration when a Court (or Registrar) has ordered registration under Rules 184 / 188",
            "Court-directed registration completes with the correct endorsement",
        ),
    ]:
        add_story(doc, *s)
    add_heading_custom(doc, "Liability", level=3)
    for s in [
        (
            "US-LIA-01",
            "District Registrar",
            "file a Liability note / order against the correct district, SRO, village and survey number for a chosen financial year",
            "the liability attaches only to the intended property",
        ),
        (
            "US-LIA-02",
            "Sub-Registrar / citizen (EC user)",
            "see active Liability filings on Certificate of encumbrance / property search (Rules 148–154) and not see removed or wrong-property liabilities",
            "EC reflects true departmental liability status",
        ),
        (
            "US-LIA-03",
            "District Registrar / Sub-Registrar",
            "search Liability by document number or property number, including legacy Kaveri 1 records, and remove or correct a wrongly filed liability",
            "FY / jurisdiction / fetch failures do not block liability maintenance",
        ),
    ]:
        add_story(doc, *s)

    add_heading_custom(doc, "8.7 Open notes (from source)", level=2)
    add_bullet(
        doc,
        "Integration push to Bhoomi/RDPR is largely departmental/technical; statutory anchors are Secs. 64–67 (outbound memo pattern) and post–Sec. 60 completion.",
    )
    add_bullet(
        doc,
        "Confirm with Domain Expert (1) the authoritative exemption matrix for Integration exemption, and (2) the exact legal instrument governing Liability Filing beyond EC practice under Rules 148–154.",
    )
    add_bullet(
        doc,
        "FRUITS bank e-filing remains primarily Sr.16 / Rule 17 Part IV–V; only overlapping Court/institutional filing is in scope here.",
    )

    # =====================================================================
    # 11-09-2026 — Investigation & Search; Verify Document
    # =====================================================================
    page_break(doc)
    add_heading_custom(
        doc,
        "9. 11-09-2026 — Investigation and Search; Verify Document",
        level=1,
    )
    add_meta_table(
        doc,
        [
            ["Date", "11-09-2026"],
            [
                "Topics",
                "Investigation and Search; Verify Document (registered document / issued digital e-stamp) — Schedule Sr.20; modules #20, #26",
            ],
            [
                "Attendees",
                "Kaveri IT Cell, AIGR Computers team, Domain Expert and committee members",
            ],
            [
                "Version",
                "1.1 (15-09-2026) — Acts, sections, Rules, notifications and user stories for Investigation & Search and Verify Document (registered deed / e-stamp)",
            ],
            [
                "Source",
                "Document_Registration_requirement_11092026_v1.1.docx",
            ],
        ],
    )

    add_para(
        doc,
        "Scope: (1) Investigation and Search of registration records (Books / indexes / EC / certified copies), "
        "including access usable by Investigation agencies under Sec. 57; (2) Verify Document — verification of an "
        "already-registered document and of an issued digital e-stamp certificate. EC functional issues (Sr.26) are "
        "out of scope except as the search path under Rules 148–154.",
        size=10.5,
        space_after=8,
    )

    add_heading_custom(doc, "9.1 Primary Acts", level=2)
    add_table(
        doc,
        ["Act / instrument", "Role", "Relevance to topics"],
        [
            [
                "The Registration Act, 1908 (Central Act 16 of 1908)",
                "Primary — Investigation & Search; Verify registered document",
                "Sec. 57 — inspection of Books 1–2 / indexes and certified copies (open to any person, including Investigation agencies, for Book 1–2); Secs. 51, 54–55 — register-books and indexes; Secs. 78–79 — fees; Sec. 57(5) — certified copy admissible to prove contents",
            ],
            [
                "The Karnataka Registration Rules, 1965",
                "Primary (Rules) — Investigation & Search",
                "Chapter XX (Rules 135–154) — Inspection, Searches and Grant of Certified Copies",
            ],
            [
                "The Karnataka Stamp Act, 1957",
                "Related — Verify e-stamp / stamp authenticity",
                "Stamp / impressed-stamp framework; Sec. 10 payment modes; Secs. 33–34 examination of instruments not duly stamped",
            ],
            [
                "Karnataka Stamp (Payment of Stamp Duty by means of e-Stamping) Rules, 2009",
                "Primary — Verify Document (digital e-stamp)",
                "Rule 11 — CRA software (UIN, search/view, lock); Rule 24 — details on CRA website; Rules 29–30 — SRO/DR/DC verify UIN and lock certificate",
            ],
        ],
        col_widths=[2.4, 1.8, 2.6],
    )

    add_heading_custom(doc, "9.2 Relevant sections", level=2)
    add_heading_custom(doc, "9.2.1 Investigation and Search", level=3)
    add_table(
        doc,
        ["Section", "Topic", "BRD / system relevance"],
        [
            [
                "Sec. 57(1)",
                "Inspection of Books 1 & 2 and Index to Book 1; certified copies",
                "Core Investigation & Search — any person (incl. Investigation agencies) may inspect / obtain copies on payment of fee",
            ],
            [
                "Sec. 57(2)–(3)",
                "Copies from Book 3 and Book 4 — restricted persons",
                "Search/copy for Investigation agencies limited unless applicant is executant / claimant / agent / representative",
            ],
            [
                "Sec. 57(4)",
                "Search of Book 3 / 4 entries only by registering officer",
                "Officer-mediated search workflow for restricted books",
            ],
            [
                "Sec. 57(5)",
                "Certified copies signed & sealed; admissible to prove contents",
                "Legal effect of Verify Document / certified extract of a registered deed",
            ],
            [
                "Sec. 51",
                "Register-books to be kept in the several offices",
                "Book structure that Investigation & Search and Verify Document query",
            ],
            [
                "Secs. 54–55",
                "Indexes to be prepared and their particulars",
                "Name / property indexes used in search and EC preparation",
            ],
            [
                "Secs. 78–79",
                "Fees table; publication; remittance",
                "Search / inspection / copy fee masters (Table of Fees under Sec. 78)",
            ],
            [
                "Sec. 91",
                "Inspection and copies of maps / surveys / certain Govt documents",
                "Related public-record inspection path (fee as notified)",
            ],
        ],
        col_widths=[1.4, 2.6, 2.8],
    )

    add_heading_custom(
        doc,
        "9.2.2 Verify Document (registered document / digital e-stamp)",
        level=3,
    )
    add_table(
        doc,
        ["Section", "Topic", "BRD / system relevance"],
        [
            [
                "Sec. 57 (Registration Act)",
                "Certified copy / inspection as proof of registered document",
                "Citizen / officer / agency verifies that a deed was registered and reads its registered contents",
            ],
            [
                "Sec. 60 (Registration Act)",
                "Certificate of registration endorsed on the document",
                "Verify that the instrument bears a valid registration certificate (number, book, page)",
            ],
            [
                "Stamp Act — Sec. 10 / payment modes",
                "How stamp duty may be paid (incl. e-stamp)",
                "Context for verifying that duty was paid by an issued digital e-stamp certificate",
            ],
            [
                "Stamp Act — Secs. 33–34",
                "Examination / impounding; inadmissibility if not duly stamped",
                "SRO must satisfy that the instrument (incl. via e-stamp) is duly stamped before acting on / registering it",
            ],
        ],
        col_widths=[1.8, 2.4, 2.6],
    )

    add_heading_custom(doc, "9.3 Relevant Rules", level=2)
    add_heading_custom(
        doc,
        "9.3.1 Investigation and Search — Karnataka Registration Rules, 1965",
        level=3,
    )
    add_table(
        doc,
        ["Rule", "Requirement", "System feature"],
        [
            [
                "Rule 135–136 (Ch. XX)",
                "Applications in writing; no inspection of unregistered documents",
                "Investigation / search intake; block search of documents still under registration",
            ],
            [
                "Rule 137–139",
                "Search fee in advance; Form No. 22 applications; fee registers",
                "Search application, fee collection and unsuccessful-search handling",
            ],
            [
                "Rule 140–142",
                "Endorsement on copies under Sec. 57; post forwardal; copy fee rules",
                "Certified-copy issue path used for Verify Document of registered deeds",
            ],
            [
                "Rule 144",
                "Grant of copies of deeds in Book No. 4",
                "Restrict copy grant to persons interested as per Sec. 57(3)",
            ],
            [
                "Rule 146–147",
                "Application for making a search; no Court-fee stamp on search apps",
                "Party vs office-assisted search; result notation on application",
            ],
            [
                "Rules 148–154",
                "Certificate of encumbrance — particulars, language, multi-office, dual search",
                "EC search workflow (property / person list) feeding Investigation & Search",
            ],
            [
                "Rules 155–156",
                "Production of Register books in Court; safe-custody fees via Court",
                "Court / agency production of original register books when required",
            ],
        ],
        col_widths=[1.8, 2.6, 2.4],
    )

    add_heading_custom(
        doc,
        "9.3.2 Verify Document — e-Stamping Rules, 2009 & Registration Rules",
        level=3,
    )
    add_table(
        doc,
        ["Rule", "Requirement", "System feature"],
        [
            [
                "e-Stamp Rules — Rule 11(a),(j),(n),(o)",
                "Unique identification number; barcode/security; departmental search/view; details on CRA server",
                "Verify Document — lookup of issued digital e-stamp by UIN / barcode",
            ],
            [
                "e-Stamp Rules — Rule 11(l)–(m)",
                "Disable/lock e-stamp; cancel spoiled/unused certificates",
                "Prevent reuse after verification; cancel unused certificates",
            ],
            [
                "e-Stamp Rules — Rule 24",
                "Details of issued e-stamp Certificate to be on website / CRA server",
                "Public / authorised online verification of issued e-stamp",
            ],
            [
                "e-Stamp Rules — Rule 28",
                "UIN of e-stamp to be written on each page of the instrument",
                "Capture / display UIN on the deed for verification at presentation",
            ],
            [
                "e-Stamp Rules — Rule 29",
                "Registering officer to verify details of e-stamp certificate",
                "Core Verify Document step — SRO / DR / DC of Stamps enters UIN and matches certificate details",
            ],
            [
                "e-Stamp Rules — Rule 30",
                "Locking of e-stamp certificate after verification",
                "After successful verify, lock UIN to prevent repeated use",
            ],
            [
                "Registration Rules — Rule 140 / Sec. 57(5)",
                "True-copy endorsement on certified copies of registered deeds",
                "Verify registered document via certified copy with statutory seal",
            ],
        ],
        col_widths=[2.0, 2.5, 2.3],
    )

    add_heading_custom(doc, "9.4 Notifications / amendments", level=2)
    add_table(
        doc,
        ["Instrument", "Effect", "Topics"],
        [
            [
                "The Karnataka Registration Rules, 1965 (under Registration Act Sec. 69)",
                "Parent subordinate legislation for Inspection, Searches and Certified Copies",
                "Investigation & Search",
            ],
            [
                "RD 403 ESR 85 / RD/46/MNMU/2025 (registration fee table under Sec. 78)",
                "Search / inspection / certified-copy / EC fees",
                "Investigation & Search — fee masters",
            ],
            [
                "Karnataka Stamp (Payment of Stamp Duty by means of e-Stamping) Rules, 2009",
                "Digital e-stamp issue, website publication, SRO verify & lock",
                "Verify Document (e-stamp)",
            ],
            [
                "Registration Act Sec. 57 practice / CC workflow",
                "Certified copies and Book 1–2 inspection as the statutory verify path for already-registered documents",
                "Verify Document (registered deed)",
            ],
        ],
        col_widths=[2.6, 2.6, 1.6],
    )

    add_heading_custom(doc, "9.5 Pain points", level=2)
    add_para(
        doc,
        "Limited direct ServiceDesk mapping for this topic; one related ticket noted:",
        size=10.5,
        space_after=4,
    )
    add_bullet(
        doc,
        "68 correction not able to verify document (Request ID 19748) — verify-document step failing in a correction flow.",
        bold_prefix="Verify Document: ",
    )

    add_heading_custom(doc, "9.6 User stories", level=2)
    add_para(
        doc,
        "Taken from Document_Registration_requirement_11092026_v1.1.docx §5 "
        "(derived from Schedule Sr.20 Acts, sections and Rules).",
        size=10,
        space_after=8,
    )

    add_heading_custom(doc, "Investigation and Search", level=3)
    for s in [
        (
            "US-IS-01",
            "citizen / Investigation agency / other authorised person",
            "apply for inspection or search of Book 1–2 and Index to Book 1 under Sec. 57(1) and Rules 135–139 (Form No. 22), paying search fee in advance",
            "I can locate registered entries affecting a person or property",
        ),
        (
            "US-IS-02",
            "Sub-Registrar / DEO",
            "run office-assisted search under Rule 146, record the result on the application, and issue a certificate of encumbrance or person-wise list under Rules 148–154",
            "search results and EC / list outputs are complete and auditable",
        ),
        (
            "US-IS-03",
            "citizen / Investigation agency",
            "obtain a signed and sealed certified copy under Sec. 57(5) and Rule 140 when I am entitled",
            "the copy is admissible to prove the contents of the registered document",
        ),
        (
            "US-IS-04",
            "Sub-Registrar",
            "refuse inspection of unregistered documents (Rule 136) and mediate Book 3/4 searches only for entitled persons (Sec. 57(2)–(4); Rule 144)",
            "restricted books stay protected while public books remain searchable",
        ),
        (
            "US-IS-05",
            "Court / Investigation agency (via Court)",
            "requisition production of register books under Rules 155–156 when originals are required",
            "safe custody and return of books are tracked",
        ),
    ]:
        add_story(doc, *s)

    add_heading_custom(doc, "Verify Document (registered document / digital e-stamp)", level=3)
    for s in [
        (
            "US-VD-01",
            "citizen / officer / Investigation agency",
            "verify that a document was registered by inspecting Book 1–2 or obtaining a Sec. 57 certified copy, and check the Sec. 60 registration certificate particulars",
            "I can confirm authenticity of an already-registered deed",
        ),
        (
            "US-VD-02",
            "Sub-Registrar / District Registrar / DC of Stamps",
            "verify an issued digital e-stamp by entering its unique identification number under e-Stamp Rule 29 and matching details on the CRA system / website (Rules 11, 24)",
            "duty payment on the instrument is confirmed before registration proceeds",
        ),
        (
            "US-VD-03",
            "Sub-Registrar / District Registrar / DC of Stamps",
            "lock the e-stamp certificate after successful verification under Rule 30 (and Rule 11(l))",
            "the same UIN cannot be reused on another instrument",
        ),
        (
            "US-VD-04",
            "presentant / DEO",
            "capture the e-stamp UIN on each page of the instrument as required by Rule 28 so that verification can be completed at presentation",
            "verify-and-lock can run without missing UIN data",
        ),
        (
            "US-VD-05",
            "authorised CRA / departmental user",
            "search and view any e-stamp certificate and cancel spoiled/unused certificates under Rule 11(n),(m)",
            "e-stamp inventory and authenticity checks are available to authorised officers",
        ),
    ]:
        add_story(doc, *s)

    add_heading_custom(doc, "9.7 Open notes (from source)", level=2)
    add_bullet(
        doc,
        "Investigation agencies are not a separate named class in Acts_Rules/Document; Book 1–2 inspection under Sec. 57(1) applies to any person. Book 3/4 remain restricted.",
    )
    add_bullet(
        doc,
        "Stamp Act Secs. 67 / 67-B (departmental stamp inspection / premises search) are revenue-officer powers, not Investigation-agency search, and were not expanded in the daily note.",
    )
    add_bullet(
        doc,
        "EC current issues & process improvements remain Schedule Sr.26; only the Rules 148–154 search path is referenced under Sr.20.",
    )

    # ----- End note -----
    page_break(doc)
    add_heading_custom(doc, "Appendix — Scope note", level=1)
    add_bullet(
        doc,
        "This consolidation is date-wise and limited to the named daily reports listed under Sources.",
    )
    add_bullet(
        doc,
        "Business re-engineering content (Document_Registration_Business_Re-Engineering_Document.docx) is intentionally excluded.",
    )
    add_bullet(
        doc,
        "User stories for 25-08 are aligned to BRD_User_Management_v4.23 (ID | Actor | Story | Acceptance). User stories for 27-08, 28-08 and 07–08 Sep were derived from discussion sections / Acts-Rules where the source notes did not include a User Stories section; 01-09, 02-09, 08-09 (Sr.18), 09–10 Sep (Sr.19) and 11-09 user stories are taken from the source documents.",
    )
    add_bullet(
        doc,
        "Pain-point ticket numbers are as recorded in the source daily reports / ServiceDesk mapping (limited for 07–08 Sep Appeal/Will; detailed for 08-09 Sr.18, 09–10 Sep Sr.19 and 11-09).",
    )

    try:
        doc.save(str(OUT))
        print(f"Wrote {OUT}")
    except PermissionError:
        doc.save(str(OUT_FALLBACK))
        print(f"Target locked — wrote {OUT_FALLBACK}")
    if LEGACY_OUT.exists() and LEGACY_OUT.resolve() != OUT.resolve():
        try:
            LEGACY_OUT.unlink()
            print(f"Removed legacy {LEGACY_OUT.name}")
        except PermissionError:
            print(f"Could not remove legacy {LEGACY_OUT.name} (file in use)")



if __name__ == "__main__":
    build()
