# -*- coding: utf-8 -*-
"""Build one date-wise consolidated requirement discussion document from:

  - user_management_requirement_25082026.docx
  - Document_Registration_requirement_27082026_v1.1.docx
  - Document_Registration_requirement_28082026_v1.1.docx
  - Document_Registration_requirement_01092026_v2.docx
  - Document_Registration_requirement_02092026_v1.1.docx

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
OUT = BASE / "Consolidated_Requirement_Discussions_25082026_to_02092026.docx"

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
    r1 = p.add_run(f"As a {actor}, I want to {want}, so that {so_that}.")
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
        "25-08-2026 to 02-09-2026",
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
        "Derived from the 25-08-2026 discussion sections.",
        size=10,
        space_after=8,
    )
    stories_2508 = [
        (
            "US-UM-01",
            "department / citizen user",
            "log in with User ID + OTP + captcha only (no password)",
            "authentication is simpler and consistent with OTP-based access",
        ),
        (
            "US-UM-02",
            "department user",
            "optionally authenticate using biometrics that are refreshed every 5 years",
            "secure biometric login is available for office users",
        ),
        (
            "US-UM-03",
            "logged-in user",
            "select a role from my assigned list after login and have menus/actions update accordingly",
            "I work under the correct role context",
        ),
        (
            "US-UM-04",
            "logged-in user",
            "switch among my assigned roles whenever needed",
            "I do not need to log out to change role context",
        ),
        (
            "US-UM-05",
            "admin / creator",
            "assign a primary role without an end date at account creation",
            "every user has a permanent home role",
        ),
        (
            "US-UM-06",
            "admin",
            "assign secondary roles with mandatory end dates and auto-remove access after expiry",
            "temporary access cannot continue beyond the approved period",
        ),
        (
            "US-UM-07",
            "admin",
            "capture an approval letter when granting additional roles or changing the primary role",
            "role changes remain auditable",
        ),
        (
            "US-UM-08",
            "admin",
            "record the reason for primary-role change (promotion / transfer / demotion) and set a future effective date",
            "role changes can be scheduled and justified",
        ),
        (
            "US-UM-09",
            "super admin",
            "add roles with abbreviation/acronym, hierarchy level, and peer/subordinate edit permission flags",
            "role masters stay configurable for the department",
        ),
        (
            "US-UM-10",
            "department officer",
            "generate relieving and joining letters from the application in the department format",
            "offline letter work is reduced",
        ),
        (
            "US-UM-11",
            "admin",
            "create a user account instantly without an approval workflow",
            "onboarding is not delayed by multi-level approvals",
        ),
        (
            "US-UM-12",
            "management / admin",
            "view a daily login report with user counts and roles",
            "login activity can be monitored",
        ),
    ]
    for s in stories_2508:
        add_story(doc, *s)

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

    # ----- End note -----
    page_break(doc)
    add_heading_custom(doc, "Appendix — Scope note", level=1)
    add_bullet(
        doc,
        "This consolidation is date-wise and limited to the five named daily reports.",
    )
    add_bullet(
        doc,
        "Business re-engineering content (Document_Registration_Business_Re-Engineering_Document.docx) is intentionally excluded.",
    )
    add_bullet(
        doc,
        "User stories for 25-08, 27-08 and 28-08 were derived from discussion sections where the source notes did not yet include a User Stories section; 01-09 and 02-09 user stories are taken from the source documents.",
    )
    add_bullet(
        doc,
        "Pain-point ticket numbers are as recorded in the source daily reports / ServiceDesk mapping.",
    )

    doc.save(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
