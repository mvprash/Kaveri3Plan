# -*- coding: utf-8 -*-
"""Create BRD_CVC_Guidance_Value_Fixation_v1.docx

Valuation Module (CVC) — Guidance Value Fixation / Revision.

Sources:
  - Requirement Discussions/Daily Reports/Document_Registration_requirement_01092026_v2.docx
    (discussion window 31-08-2026 to 01-09-2026; Schedule Sr.14 — Valuation Module CVC)
  - Workshop process for General Revision and Fixation for new individual project
  - Acts_Rules/Document — Karnataka Stamp Act 1957 (Secs. 2(ac), 45-A, 45-B);
    Prevention of Undervaluation Rules 1977; Registration Rules 13–15
  - Format reference: Finalized BRD/Marriage/RFP/BRD_Marriage_BRD_v8.docx
"""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(r"E:\MVP\Kaveri 3.0\Source Code\Kaveri 3 Plan\Finalized BRD\CVCGUIDANCEVALUEFIXATION")
DST = BASE / "BRD_CVC_Guidance_Value_Fixation_v1.docx"
OUT_VERSION = "1.1"
OUT_DATE = "22-09-2026"


def shade_cell(cell, hex_fill: str) -> None:
    shading = OxmlElement("w:shd")
    shading.set(qn("w:val"), "clear")
    shading.set(qn("w:fill"), hex_fill)
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_text(cell, text: str, bold: bool = False, size: int = 9) -> None:
    cell.text = ""
    run = cell.paragraphs[0].add_run(text)
    run.bold = bold
    run.font.size = Pt(size)


def add_table(doc: Document, headers: list[str], rows: list[list[str]]) -> None:
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    for i, h in enumerate(headers):
        set_cell_text(table.rows[0].cells[i], h, bold=True)
        shade_cell(table.rows[0].cells[i], "D9E2F3")
    for ri, row in enumerate(rows, start=1):
        for ci, val in enumerate(row):
            set_cell_text(table.rows[ri].cells[ci], val if val is not None else "")
    doc.add_paragraph()


def add_kv_table(doc: Document, rows: list[list[str]]) -> None:
    table = doc.add_table(rows=len(rows), cols=2)
    table.style = "Table Grid"
    for ri, (k, v) in enumerate(rows):
        set_cell_text(table.rows[ri].cells[0], k, bold=True)
        shade_cell(table.rows[ri].cells[0], "F2F2F2")
        set_cell_text(table.rows[ri].cells[1], v)
    doc.add_paragraph()


def add_heading(doc: Document, text: str, level: int) -> None:
    doc.add_heading(text, level=level)


def add_para(doc: Document, text: str, style: str | None = None) -> None:
    if style:
        doc.add_paragraph(text, style=style)
    else:
        doc.add_paragraph(text)


def add_bullets(doc: Document, items: list[str]) -> None:
    for item in items:
        doc.add_paragraph(item, style="List Bullet")


def add_numbered(doc: Document, items: list[str]) -> None:
    for item in items:
        doc.add_paragraph(item, style="List Number")


def add_note(doc: Document, text: str) -> None:
    p = doc.add_paragraph()
    run = p.add_run("Note: ")
    run.bold = True
    run.italic = True
    run2 = p.add_run(text)
    run2.italic = True


def fr_table(doc: Document, rows: list[list[str]]) -> None:
    """Req ID | Requirement | Priority"""
    add_table(doc, ["Req ID", "Requirement", "Priority"], rows)


def build() -> None:
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # ------------------------------------------------------------------
    # Title
    # ------------------------------------------------------------------
    title = doc.add_paragraph()
    run = title.add_run("Business Requirements Document (BRD)")
    run.bold = True
    run.font.size = Pt(18)
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    add_heading(doc, "Valuation Module (CVC) — Guidance Value Fixation", 1)

    # ------------------------------------------------------------------
    # 1. Document control
    # ------------------------------------------------------------------
    add_heading(doc, "Document control", 2)
    add_kv_table(
        doc,
        [
            ["Field", "Value"],
            ["Document ID", "BRD-K3-CVC-GVF-001"],
            ["Version", OUT_VERSION],
            [
                "Status",
                "Draft — based on Sr.14 discussion (31-08-2026 to 01-09-2026) "
                "and workshop process for General Revision / Individual Project fixation",
            ],
            ["Module", "Valuation Module (CVC) — Guidance Value Fixation / Revision"],
            [
                "Schedule / discussion",
                "Schedule Sr.14 — Valuation Module (CVC) and GIS valuation "
                "(modules list #21); discussion dates 31-08-2026 to 01-09-2026",
            ],
            [
                "Legal basis (primary)",
                "The Karnataka Stamp Act, 1957 — Sec. 2(ac), Sec. 45-A, Sec. 45-B "
                "(as substituted / strengthened by Act 8 of 2003, w.e.f. 1-4-2003)",
            ],
            [
                "State rules (primary)",
                "Karnataka Stamp (Prevention of Undervaluation of Instruments) Rules, 1977 "
                "(GSR 81 / RD 73 EST 74; amended RD 264 MUNOMU 99); "
                "Karnataka Registration Rules, 1965 — Rules 13–15 (territorial / survey "
                "description supporting rate selection)",
            ],
            ["Author (BA)", "Nandha Kumar"],
            ["Product Owner", "M V Prashanth"],
            [
                "Domain expert / reviewer",
                "DIGR — Valuation; Kaveri IT Cell; Committee members",
            ],
            [
                "Target audience",
                "Kaveri IT Cell, Department of Stamps and Registration, "
                "Government of Karnataka; Central Valuation Committee (CVC)",
            ],
            ["Last updated", OUT_DATE],
        ],
    )

    add_heading(doc, "Version history", 3)
    add_table(
        doc,
        ["Version", "Date", "Author", "Summary of change", "Approver"],
        [
            [
                "1",
                "18-09-2026",
                "Nandha Kumar",
                "Initial BRD for Guidance Value Fixation — General Revision and "
                "Fixation for new individual project; mapped to Stamp Act Sec. 45-B "
                "and Sr.14 discussion (01-09-2026)",
                "Prashanth",
            ],
            [
                "1.1",
                OUT_DATE,
                "Nandha Kumar",
                "Current state rewritten: no digitised guidance-value revision / "
                "fixation system exists As-Is; removed ServiceDesk pain-point table",
                "Prashanth",
            ],
        ],
    )

    # ------------------------------------------------------------------
    # 2. Executive summary
    # ------------------------------------------------------------------
    add_heading(doc, "Executive summary", 2)
    add_para(
        doc,
        "This document captures the business requirements for the Kaveri 3.0 Valuation "
        "Module (CVC) focused on fixation and revision of market value guidelines "
        "(commonly called guidance / guideline value). The authoritative rates used "
        "across registration for stamp-duty computation are those estimated, published "
        "and revised by the Central Valuation Committee under Sec. 45-B of the "
        "Karnataka Stamp Act, 1957.",
        style="List Paragraph",
    )
    add_para(
        doc,
        "Based on the requirement discussion held between 31-08-2026 and 01-09-2026 "
        "(Document_Registration_requirement_01092026_v2) and the workshop process "
        "walkthrough, two fixation paths are in scope: (1) General Revision — "
        "state-wide periodic revision triggered by the IGR as CVC Chairman; and "
        "(2) Fixation of guidance value for a new individual project — citizen / "
        "party initiated request accepted by the District Registrar under Sec. 45-B.",
        style="List Paragraph",
    )
    add_para(
        doc,
        "The proposed To-Be workflows digitise committee routing (DIGR → DR → SR → "
        "Sub-committee → public opinion → CVC), evidence packs (registration "
        "transaction data, KSRSAC GIS / maps, developer publications, RTC, khata, "
        "town planning), gazette effective-date adoption in Kaveri, and auditability "
        "of every rate version used for duty calculation.",
        style="List Paragraph",
    )

    # ------------------------------------------------------------------
    # 3. Scope
    # ------------------------------------------------------------------
    add_heading(doc, "Scope", 2)
    add_heading(doc, "In scope", 3)
    add_bullets(
        doc,
        [
            "General Revision of market value guidelines for the entire State "
            "(IGR/CVC trigger → DIGR notification → DR → SR proposal → Sub-committee "
            "→ 15-day public opinion → CVC approval → effective date → Kaveri adoption).",
            "Fixation of guidance value for a new individual project / newly developed "
            "property (citizen application → DR acceptance under Sec. 45-B → DR spot "
            "inspection & proposal → Secretary CVC review & finalisation → Chairman "
            "CVC (IGR) approval).",
            "Evidence and reference data used while proposing rates: historical "
            "registration (transaction) data, KSRSAC GIS data / maps, developer "
            "publications, RTC data, khata data, town-planning inputs.",
            "Sub-committee and CVC committee workbenches, minutes, objection handling "
            "after public notice, proposal forwarding DR ↔ CVC.",
            "Publication of proposed revised guideline values for public opinion "
            "(15-day notice) and gazette / effective-date management.",
            "Adoption of approved guidance rates in Kaveri from the gazette effective "
            "date (versioned rate masters for SR and Citizen logins).",
            "Role-based access for IGR, DIGR, DR, SR, Secretary CVC, Sub-committee "
            "members, CVC members; bilingual UI (English + Kannada); audit trail; MIS.",
            "Handoff interfaces to Guideline Value Calculation (#5) and GIS valuation "
            "(#22) so published CVC rates remain the single source of truth.",
        ],
    )
    add_heading(doc, "Out of scope (this BRD)", 3)
    add_bullets(
        doc,
        [
            "Day-to-day guideline value lookup / stamp-duty calculation engine "
            "(Schedule Sr.13 — #4 Stamp duty & Registration fee; #5 Guideline value "
            "calculation) — consumes rates published by this module.",
            "Full GIS valuation spatial engine (Sr.14 #22) — treated as an "
            "implementation layer on top of CVC guideline rates with KSRSAC; only "
            "evidence-use of GIS maps during fixation is in scope here.",
            "Sec. 45-A undervaluation adjudication end-to-end (DRO / DC determination, "
            "appeal) — Sr.22; this BRD only ensures published guidelines exist for "
            "comparison at registration.",
            "Emergency / mid-cycle rate corrections outside the two defined paths "
            "(to be decided separately if required).",
        ],
    )

    # ------------------------------------------------------------------
    # 4. Legal and regulatory reference
    # ------------------------------------------------------------------
    add_heading(doc, "Legal and regulatory reference", 2)

    add_heading(doc, "Applicable Acts", 3)
    add_para(
        doc,
        "The Department of Stamps and Registration, through the Inspector General of "
        "Registration & Commissioner of Stamps (IGR) as Chairman of the Central "
        "Valuation Committee, administers market-value guideline estimation, "
        "publication and revision under the Karnataka Stamp Act, 1957.",
    )
    add_table(
        doc,
        ["Act", "Description"],
        [
            [
                "The Karnataka Stamp Act, 1957",
                "Sec. 2(ac) defines Central Valuation Committee; Sec. 45-B constitutes "
                "CVC under IGR & Commissioner of Stamps for estimation, publication and "
                "revision of market value guidelines and for constituting district / "
                "sub-district market valuation sub-committees; Sec. 45-A applies those "
                "guidelines at registration for undervaluation comparison; Sec. 3 + "
                "Schedule charge stamp duty ad valorem on market value for listed "
                "instruments. Strengthened by Act 8 of 2003 (w.e.f. 1-4-2003).",
            ],
            [
                "The Registration Act, 1908 (supporting)",
                "Registration of instruments; property description and territorial "
                "jurisdiction that drive which guideline rate applies.",
            ],
            [
                "The Karnataka Guarantee of Services to Citizens Act, 2011 (supporting)",
                "Where citizen-facing fixation of guidance value for a new project is "
                "notified as a Sakala service — time-bound acknowledgement and status.",
            ],
        ],
    )

    add_heading(doc, "Relevant sections — Karnataka Stamp Act, 1957", 3)
    add_table(
        doc,
        ["Section", "Topic", "BRD relevance", "Refer section 7 for Implementation"],
        [
            [
                "Sec. 2(ac)",
                "Definition — Central Valuation Committee",
                "CVC is the statutory owner of guideline rate masters and approvals",
                "7.i (actors / entity master); 7.ii–7.iii (approval authority)",
            ],
            [
                "Sec. 45-B",
                "Constitution of CVC; estimation, publication and revision of market "
                "value guidelines; district / sub-district sub-committees; CVC final "
                "authority for policy and methodology",
                "Primary legal basis for General Revision and for fixation of "
                "guidance value for new individual projects (DR acceptance of "
                "citizen request under Sec. 45-B framework)",
                "7.ii General Revision; 7.iii Individual Project Fixation",
            ],
            [
                "Sec. 45-A",
                "Instrument undervalued — registering officer compares consideration "
                "with market value guidelines; reference to Deputy Commissioner",
                "Published guidelines from this module are consumed at registration; "
                "adjudication path is out of scope of this BRD",
                "Handoff to Guideline Value Calculation / Sr.22",
            ],
            [
                "Sec. 3 + Schedule",
                "Instruments chargeable; ad valorem duty on market value",
                "Correct Schedule article applied after guideline value is arrived at",
                "Handoff to Stamp duty engine (Sr.13 #4)",
            ],
            [
                "Sec. 46",
                "Recovery of duties and penalties; charge on property",
                "Post-valuation recovery linkage (supporting)",
                "— (supporting / audit)",
            ],
        ],
    )

    add_heading(doc, "Relevant rules", 3)
    add_para(
        doc,
        "Source folder: Acts_Rules/Document/. The file titled "
        "“Karnataka Stamp (Constitution of Central Valuation Committee for Estimation, "
        "Publication and Revision of Market Value Guidelines of Properties) Rules, "
        "2003.docx” currently embeds the text of the Karnataka Stamp (Prevention of "
        "Undervaluation of Instruments) Rules, 1977 (GSR 81; RD 73 EST 74; amended "
        "RD 264 MUNOMU 99). CVC constitution and market-value guidelines remain "
        "governed by Stamp Act Sec. 45-B. Operational Form I / DC determination "
        "rules support undervaluation cases that consume the published guidelines.",
    )
    add_table(
        doc,
        ["Rule / provision", "Requirement", "Refer section 7 for Implementation"],
        [
            [
                "Stamp Act Sec. 45-B (practice)",
                "CVC under IGR; publish and revise market value guidelines; "
                "constitute market valuation sub-committees",
                "7.ii, 7.iii — revision / fixation workflows",
            ],
            [
                "Undervaluation Rules, 1977 — Rule 3 / Form I",
                "Statement of particulars of property and its market value",
                "Supporting — property statement when Sec. 45-A is invoked "
                "(not the fixation path itself)",
            ],
            [
                "Undervaluation Rules — principles for market value",
                "Factors for land / building valuation",
                "7.ii.d / 7.iii.c — evidence pack and methodology alignment",
            ],
            [
                "RD 264 MUNOMU 99 (18-8-1999)",
                "Amendments to Undervaluation Rules (no obsolete provisional / Rule 6 path)",
                "Ensure screens match Rules now in force",
            ],
            [
                "Registration Rules 13–15",
                "Territorial divisions; survey / Pot Hissa / city survey description",
                "7.ii.d, 7.iii — property identification for rate proposal; "
                "GIS / survey evidence",
            ],
        ],
    )

    add_heading(doc, "Relevant notifications / amendments", 3)
    add_table(
        doc,
        ["Instrument", "Date / No.", "Effect", "BRD relevance"],
        [
            [
                "Act 8 of 2003",
                "w.e.f. 1-4-2003",
                "Substituted / strengthened Sec. 45-B CVC framework",
                "Legal foundation for Valuation Module revision cycles",
            ],
            [
                "GSR 81 / RD 73 EST 74",
                "2-3-1977; Gazette 10-3-1977",
                "Prevention of Undervaluation Rules, 1977",
                "Form I / DC path consuming CVC guidelines",
            ],
            [
                "RD 264 MUNOMU 99",
                "18-8-1999",
                "Amendments to Undervaluation Rules",
                "Current undervaluation procedure alignment",
            ],
            [
                "CVC / IGR order & DIGR notification (operational)",
                "Per revision cycle",
                "Triggers General Revision; DIGR issues notification for fixing "
                "guidance value; CVC gazette fixes effective date",
                "7.ii.a–7.ii.l — General Revision process",
            ],
        ],
    )

    # ------------------------------------------------------------------
    # 5. Stakeholders and actors
    # ------------------------------------------------------------------
    add_heading(doc, "Stakeholders and actors", 2)
    add_table(
        doc,
        ["Actor", "Role in Guidance Value Fixation"],
        [
            [
                "IGR / Chairman CVC",
                "Triggers General Revision by order; approves final guidance value "
                "for individual projects; chairs CVC for state proposals",
            ],
            [
                "DIGR (Valuation)",
                "Issues notification for fixing guidance value; oversees district "
                "cascade; domain reviewer for this BRD",
            ],
            [
                "District Registrar (DR)",
                "Forwards DIGR notification to SR; forwards SR proposals to CVC; "
                "accepts citizen request for individual project fixation under "
                "Sec. 45-B; conducts spot inspection and proposes value",
            ],
            [
                "Sub-Registrar (SR)",
                "Refers evidence data; proposes guidance value; presents to "
                "Sub-committee; publishes for public opinion; revises on objections; "
                "forwards proposal to CVC via DR",
            ],
            [
                "Market Valuation Sub-committee",
                "Members typically include Tahsildar, SR, Secretary, ADLR, PWD AEE "
                "and others as constituted; discusses and revises proposed values "
                "before and after public opinion",
            ],
            [
                "Secretary CVC",
                "Reviews individual-project proposals using evidence pack; "
                "finalises guidance value for IGR approval",
            ],
            [
                "Central Valuation Committee (CVC)",
                "Discusses district proposals under General Revision; approves "
                "proposed guidance value; fixes effective date",
            ],
            [
                "Citizen / Party / Developer",
                "Applies for fixation of guidance value for newly developed property; "
                "submits objections during 15-day public opinion (General Revision)",
            ],
            [
                "Public",
                "May file objections / opinions on published proposed revised "
                "guideline values within 15 days",
            ],
            [
                "Kaveri IT Cell / System Admin",
                "Maintains Valuation Module; publishes approved rates into Kaveri "
                "masters from effective date; integrations (KSRSAC, RTC, etc.)",
            ],
        ],
    )

    # ------------------------------------------------------------------
    # 6. Definitions
    # ------------------------------------------------------------------
    add_heading(doc, "Definitions and glossary", 2)
    add_table(
        doc,
        ["Term", "Definition"],
        [
            [
                "Guidance / Guideline value",
                "Market value guideline rate published under Sec. 45-B for a "
                "territorial unit (village / road / survey / project / property class). "
                "Used for stamp-duty market-value comparison under Sec. 45-A.",
            ],
            [
                "CVC",
                "Central Valuation Committee as defined in Sec. 2(ac) and constituted "
                "under Sec. 45-B.",
            ],
            [
                "General Revision",
                "State-wide (or notified jurisdiction-wide) cycle to revise market "
                "value guidelines, triggered by IGR/CVC Chairman order.",
            ],
            [
                "Individual Project Fixation",
                "Fixation of guidance value for a newly developed property / project "
                "on citizen or party application, accepted by DR under Sec. 45-B.",
            ],
            [
                "Sub-committee",
                "District / sub-district market valuation sub-committee constituted "
                "under Sec. 45-B (e.g. Tahsildar, SR, Secretary, ADLR, PWD AEE).",
            ],
            [
                "Evidence pack",
                "Supporting references used while proposing rates: registration "
                "transaction data, KSRSAC GIS / maps, developer publications, RTC, "
                "khata, town planning.",
            ],
            [
                "Effective date",
                "Date fixed by CVC / gazette from which new guidance rates are "
                "adopted in Kaveri for calculation and display.",
            ],
            [
                "Public opinion period",
                "Fifteen (15) days notice period during which proposed revised "
                "guideline values are published for public objections / opinions.",
            ],
        ],
    )

    # ------------------------------------------------------------------
    # 7. Current state
    # ------------------------------------------------------------------
    add_heading(doc, "Current state", 2)
    add_heading(doc, "As-Is — no digitised revision / fixation system", 3)
    add_para(
        doc,
        "There is presently no end-to-end digitised process in Kaveri (or a "
        "linked departmental system) for Guidance Value Fixation / General Revision "
        "under Sec. 45-B. Committee constitution, rate proposal, Sub-committee "
        "deliberation, public opinion, CVC approval, gazette linkage and "
        "effective-dated adoption of guideline rates are not available as a "
        "system-supported workflow.",
    )
    add_para(
        doc,
        "In short: the As-Is gap is not a set of defects inside an existing "
        "digitised revision module — such a module does not exist. Revision and "
        "fixation of market value guidelines are handled outside a controlled "
        "Kaveri workbench (manual / offline / fragmented practices), with no "
        "single electronic cycle covering order → notification → evidence-backed "
        "proposal → Sub-committee → public notice → CVC decision → gazette "
        "effective date → versioned rate adoption.",
    )
    add_bullets(
        doc,
        [
            "No digitised General Revision cycle (IGR/CVC order through gazette "
            "adoption) in the current system.",
            "No digitised Individual Project guidance-value fixation path "
            "(citizen request → DR under Sec. 45-B → CVC / IGR approval) in the "
            "current system.",
            "No system-of-record for versioned guidance-rate masters tied to "
            "gazette / effective dates for fixation workflows.",
            "Kaveri 3.0 Valuation Module (this BRD) introduces that capability "
            "for the first time as a greenfield process digitisation.",
        ],
    )
    add_note(
        doc,
        "Downstream issues in registration (display or application of guideline "
        "rates at stamp-duty calculation) are out of scope of this As-Is statement; "
        "this section addresses only the absence of a digitised fixation / revision "
        "system under Sec. 45-B.",
    )

    # ------------------------------------------------------------------
    # 8. Future state
    # ------------------------------------------------------------------
    add_heading(doc, "Future state (To-Be)", 2)
    add_para(
        doc,
        "Kaveri 3.0 shall provide an end-to-end Valuation Module workbench for "
        "Guidance Value Fixation with two primary processes. Approved rates shall be "
        "versioned, gazette-linked, and activated in Kaveri only from the notified "
        "effective date.",
    )

    # ---- 8.1 General Revision ----
    add_heading(doc, "Process A — General Revision", 3)
    add_heading(doc, "Channel / trigger model", 4)
    add_bullets(
        doc,
        [
            "Trigger: IGR as CVC Chairman issues an order to revise guidance value "
            "for the entire State (or notified jurisdictions).",
            "Cascade: DIGR notification → DR forwards to SR → SR proposes → "
            "Sub-committee → public opinion (15 days) → Sub-committee (objections) → "
            "DR → CVC approval → effective date → Kaveri adoption.",
            "Channels: Officer workbenches (IGR, DIGR, DR, SR, Sub-committee, CVC); "
            "Citizen / public portal for viewing proposed rates and filing objections "
            "during the notice period.",
        ],
    )

    add_heading(doc, "Process steps — General Revision", 4)
    add_numbered(
        doc,
        [
            "IGR (CVC Chairman) triggers guidance value revision for the entire State "
            "with an order (create Revision Cycle in system; attach order PDF).",
            "DIGR issues a notification for fixing the guidance value (link to "
            "Revision Cycle; notify all DRs).",
            "DR forwards the notification to SRs under the district for guidance "
            "value revision (SR work-items created per jurisdiction).",
            "SR refers historical registration data (transaction data), KSRSAC GIS "
            "data / maps, Developer publications, RTC data, khata data, and town "
            "planning inputs (system evidence pack / attachments).",
            "SR proposes the guidance value for each territorial unit / rate slab "
            "in scope (draft proposal with justification).",
            "SR presents the proposal to the Sub-committee (members: Tahsildar, SR, "
            "Secretary, ADLR, PWD AEE, etc.). The Sub-committee discusses and revises "
            "the proposed guidance value; minutes are recorded.",
            "SR publishes the proposed revised guideline value for public opinion "
            "with a 15-day notice period (portal + office notice board as required).",
            "After 15 days, the Sub-committee again discusses and revises the "
            "proposed guidance value only for the objections received; revised "
            "proposal and objection disposal notes are saved.",
            "SR forwards the proposal to the CVC committee through DR "
            "(DR reviews completeness and routes to CVC).",
            "CVC discusses the proposal and approves the proposed guidance value "
            "(or returns with remarks).",
            "CVC fixes the Effective date.",
            "New guidance rates are adopted in KAVERI from the effective date as "
            "in the gazette (automated or controlled publish of versioned masters "
            "to SR and Citizen logins).",
        ],
    )

    add_heading(doc, "Application / Cycle status model — General Revision", 4)
    add_table(
        doc,
        ["Status", "Meaning", "Owner"],
        [
            ["Draft Order", "IGR preparing / uploaded order not yet issued", "IGR"],
            ["Order Issued", "Revision Cycle opened", "IGR"],
            ["Notification Issued", "DIGR notification circulated", "DIGR"],
            ["Assigned to SR", "DR forwarded; SR work-item open", "DR / SR"],
            ["Proposal Draft", "SR capturing evidence and proposed rates", "SR"],
            ["Sub-committee Review", "First Sub-committee sitting", "Sub-committee"],
            ["Public Opinion Open", "15-day notice running", "SR / Public"],
            ["Objection Disposal", "Post-notice Sub-committee revision", "Sub-committee"],
            ["Pending DR Forward", "SR submitted; with DR", "DR"],
            ["Pending CVC", "With Central Valuation Committee", "CVC"],
            ["Approved", "CVC approved rates; effective date set", "CVC"],
            ["Gazette Linked", "Gazette particulars captured", "CVC / Admin"],
            ["Active in Kaveri", "Rates live from effective date", "System"],
            ["Returned / Clarification", "Returned to prior stage with remarks", "Prior owner"],
        ],
    )

    # ---- 8.2 Individual project ----
    add_heading(doc, "Process B — Fixation of guidance value for new individual project", 3)
    add_heading(doc, "Channel / trigger model", 4)
    add_bullets(
        doc,
        [
            "Trigger: Party / citizen applies for fixation of guidance value for a "
            "newly developed property / project.",
            "Legal gate: As per Sec. 45-B of the Karnataka Stamp Act, 1957, the "
            "District Registrar accepts the request for fixation of the guidance value.",
            "Channels: Citizen portal (Online) and DR office desk (Offline / assisted).",
        ],
    )

    add_heading(doc, "Process steps — Individual Project Fixation", 4)
    add_numbered(
        doc,
        [
            "Party / citizen applies for fixation of guidance value for the newly "
            "developed property (application form, property particulars, project "
            "documents, fee if notified).",
            "As per Sec. 45-B Karnataka Stamp Act, 1957, DR accepts the request for "
            "fixation of the guidance value (or returns for deficiency with reasons).",
            "DR conducts spot inspection and proposes the guidance value "
            "(inspection report + proposed rate + evidence).",
            "Secretary CVC reviews the proposal using registration data (transaction "
            "data), KSRSAC GIS data / maps, Developer publications, RTC data, khata "
            "data, town planning, and finalises the guidance value.",
            "Finalised guidance value is submitted to Chairman CVC (IGR) for approval.",
            "IGR approves the final guidance value (with reference to the same "
            "evidence classes as above). On approval, rates are published / linked "
            "to the project / survey units and adopted in Kaveri per effective date "
            "decided with the approval / gazette.",
        ],
    )

    add_heading(doc, "Application status model — Individual Project Fixation", 4)
    add_table(
        doc,
        ["Status", "Meaning", "Owner"],
        [
            ["Submitted", "Citizen application filed", "Citizen"],
            ["Accepted by DR", "Request accepted under Sec. 45-B", "DR"],
            ["Inspection Scheduled / Done", "Spot inspection", "DR"],
            ["DR Proposed", "DR proposal with proposed value", "DR"],
            ["Secretary CVC Review", "Under review / finalisation", "Secretary CVC"],
            ["Pending IGR Approval", "Submitted to Chairman CVC", "IGR"],
            ["Approved", "IGR approved final guidance value", "IGR"],
            ["Active in Kaveri", "Rate available for calculation / display", "System"],
            ["Returned for Deficiency", "Citizen or DR must remedy", "Prior owner"],
            ["Rejected", "Request rejected with speaking order", "DR / IGR"],
        ],
    )

    add_heading(doc, "What is new in Kaveri 3.0", 3)
    add_bullets(
        doc,
        [
            "Digitised General Revision cycle with order → notification → SR proposal "
            "→ Sub-committee → 15-day public opinion → CVC → effective date → "
            "automatic adoption.",
            "Citizen-initiated Individual Project Fixation with DR acceptance under "
            "Sec. 45-B and Secretary CVC / IGR approval chain.",
            "Structured evidence pack (transaction, KSRSAC GIS, developer publications, "
            "RTC, khata, town planning) attached to every proposal.",
            "Versioned rate masters; no silent overwrite; SR and Citizen logins always "
            "read the effective-dated published version.",
            "Objection capture and Sub-committee disposal limited to objected items "
            "after public notice.",
            "Introduces the first digitised Sec. 45-B fixation / revision workbench "
            "where none exists As-Is (greenfield process digitisation).",
        ],
    )

    # ------------------------------------------------------------------
    # 9. Functional requirements
    # ------------------------------------------------------------------
    add_heading(doc, "Functional requirements", 2)

    add_heading(doc, "Common — actors, masters and evidence", 3)
    fr_table(
        doc,
        [
            [
                "FR-CVC-001",
                "System shall maintain Central Valuation Committee as a statutory "
                "entity per Sec. 2(ac), with Chairman = IGR & Commissioner of Stamps, "
                "Secretary CVC, and member roster.",
                "Must",
            ],
            [
                "FR-CVC-002",
                "System shall maintain district / sub-district Market Valuation "
                "Sub-committee membership (Tahsildar, SR, Secretary, ADLR, PWD AEE, "
                "and other notified members) with validity dates.",
                "Must",
            ],
            [
                "FR-CVC-003",
                "System shall provide an Evidence Pack checklist and file store for: "
                "registration transaction data extract; KSRSAC GIS data / maps; "
                "developer publications; RTC data; khata data; town-planning documents.",
                "Must",
            ],
            [
                "FR-CVC-004",
                "System shall version every guidance-rate record with: territorial "
                "key (district / SRO / village / road / survey / project id / property "
                "class), rate, unit, revision cycle or application id, approval "
                "authority, gazette reference, effective-from, effective-to.",
                "Must",
            ],
            [
                "FR-CVC-005",
                "System shall expose published rates to Guideline Value Calculation "
                "and GIS valuation only when status = Active and current date ≥ "
                "effective-from (and < effective-to if set).",
                "Must",
            ],
            [
                "FR-CVC-006",
                "UI shall be bilingual (English + Kannada); all statutory notices "
                "and orders shall support bilingual generation.",
                "Must",
            ],
            [
                "FR-CVC-007",
                "Every status change, rate edit, committee decision and publish action "
                "shall write an immutable audit trail (user, role, timestamp, before/after).",
                "Must",
            ],
        ],
    )

    add_heading(doc, "General Revision — trigger and cascade", 3)
    fr_table(
        doc,
        [
            [
                "FR-CVC-GR-001",
                "IGR (CVC Chairman) shall create a General Revision Cycle and upload / "
                "capture the order that triggers guidance value revision for the "
                "entire State (or selected jurisdictions).",
                "Must",
            ],
            [
                "FR-CVC-GR-002",
                "DIGR shall issue a notification for fixing the guidance value linked "
                "to the Revision Cycle and notify all District Registrars.",
                "Must",
            ],
            [
                "FR-CVC-GR-003",
                "DR shall forward the notification to one or more SRs; system shall "
                "create SR work-items with due dates and jurisdiction scope.",
                "Must",
            ],
            [
                "FR-CVC-GR-004",
                "SR shall assemble the Evidence Pack (FR-CVC-003) and capture "
                "proposed guidance values with justification notes.",
                "Must",
            ],
            [
                "FR-CVC-GR-005",
                "System shall prevent SR submission to Sub-committee unless mandatory "
                "evidence checklist items are attached or explicitly marked N/A "
                "with reason.",
                "Should",
            ],
        ],
    )

    add_heading(doc, "General Revision — Sub-committee and public opinion", 3)
    fr_table(
        doc,
        [
            [
                "FR-CVC-GR-006",
                "SR shall present the proposal to the Sub-committee; system shall "
                "capture attendance, discussion points, revised rates and minutes.",
                "Must",
            ],
            [
                "FR-CVC-GR-007",
                "After Sub-committee concurrence, SR shall publish proposed revised "
                "guideline values for public opinion with a configurable notice "
                "period defaulting to 15 days.",
                "Must",
            ],
            [
                "FR-CVC-GR-008",
                "Citizens / public shall view proposed rates and file objections / "
                "opinions online (and offline intake at SRO) within the notice period; "
                "each objection shall link to specific rate line(s).",
                "Must",
            ],
            [
                "FR-CVC-GR-009",
                "After the 15-day period closes, Sub-committee shall reconvene; system "
                "shall allow revision only for rate lines that received objections "
                "(or as directed by Sub-committee minutes), with disposal remarks "
                "per objection.",
                "Must",
            ],
            [
                "FR-CVC-GR-010",
                "SR shall forward the final proposal to CVC through DR; DR shall "
                "verify completeness and either forward or return with remarks.",
                "Must",
            ],
        ],
    )

    add_heading(doc, "General Revision — CVC approval and Kaveri adoption", 3)
    fr_table(
        doc,
        [
            [
                "FR-CVC-GR-011",
                "CVC shall discuss proposals on a committee workbench, approve or "
                "return with remarks, and record decision minutes.",
                "Must",
            ],
            [
                "FR-CVC-GR-012",
                "On approval, CVC shall fix the Effective date for the revised rates.",
                "Must",
            ],
            [
                "FR-CVC-GR-013",
                "System shall capture gazette particulars (number, date, PDF) linking "
                "the approved rate set.",
                "Must",
            ],
            [
                "FR-CVC-GR-014",
                "From the effective date as in the gazette, new guidance rates shall "
                "be adopted automatically in Kaveri rate masters for SR and Citizen "
                "logins; prior versions remain queryable for audit / historical "
                "instruments.",
                "Must",
            ],
            [
                "FR-CVC-GR-015",
                "System shall notify DIGR, DR, SR and configured stakeholders when "
                "rates become Active in Kaveri.",
                "Should",
            ],
        ],
    )

    add_heading(doc, "Individual Project Fixation", 3)
    fr_table(
        doc,
        [
            [
                "FR-CVC-IP-001",
                "Citizen / party shall apply online (or via DR desk) for fixation of "
                "guidance value for a newly developed property / project, capturing "
                "applicant, property / project particulars and supporting documents.",
                "Must",
            ],
            [
                "FR-CVC-IP-002",
                "DR shall accept the request for fixation of guidance value under "
                "Sec. 45-B Karnataka Stamp Act, 1957, or return / reject with a "
                "speaking order.",
                "Must",
            ],
            [
                "FR-CVC-IP-003",
                "DR shall record spot inspection (date, officers, observations, "
                "photos / geo-tag if available) and propose the guidance value.",
                "Must",
            ],
            [
                "FR-CVC-IP-004",
                "Secretary CVC shall review the DR proposal using the Evidence Pack "
                "(registration transaction data, KSRSAC GIS / maps, developer "
                "publications, RTC, khata, town planning) and finalise the guidance value.",
                "Must",
            ],
            [
                "FR-CVC-IP-005",
                "Finalised guidance value shall be submitted to Chairman CVC (IGR) "
                "for approval.",
                "Must",
            ],
            [
                "FR-CVC-IP-006",
                "IGR shall approve or return the final guidance value; on approval, "
                "system shall set effective date and publish the project-specific "
                "(or survey-linked) rates into Kaveri masters.",
                "Must",
            ],
            [
                "FR-CVC-IP-007",
                "Approved individual-project rates shall be discoverable in Guideline "
                "Value Calculation for the linked property / project identifiers "
                "without breaking village / road master integrity.",
                "Must",
            ],
        ],
    )

    add_heading(doc, "Notifications", 3)
    fr_table(
        doc,
        [
            [
                "FR-CVC-N-001",
                "System shall send SMS / e-Mail on key events: Revision Cycle opened; "
                "DIGR notification; SR assignment; public opinion open/close; "
                "objection acknowledgement; CVC / IGR decision; rates Active in Kaveri; "
                "individual application status changes.",
                "Must",
            ],
            [
                "FR-CVC-N-002",
                "Public opinion publication shall appear on the citizen portal and "
                "support downloadable proposed rate schedule for the notice period.",
                "Must",
            ],
        ],
    )

    add_heading(doc, "Reports and MIS", 3)
    fr_table(
        doc,
        [
            [
                "FR-CVC-R-001",
                "MIS: open Revision Cycles by status and district; SR proposal "
                "pending ageing; Sub-committee sittings; objection counts; CVC "
                "pending proposals.",
                "Must",
            ],
            [
                "FR-CVC-R-002",
                "MIS: Individual Project applications by status, district, ageing; "
                "approved project rates listing.",
                "Must",
            ],
            [
                "FR-CVC-R-003",
                "Audit report: rate version history for a territorial unit / project "
                "with gazette and approver details.",
                "Must",
            ],
        ],
    )

    add_heading(doc, "Business rules", 3)
    add_table(
        doc,
        ["Rule ID", "Rule"],
        [
            [
                "BR-CVC-01",
                "Only rates approved under General Revision or Individual Project "
                "Fixation (or prior gazette import at go-live) may become Active.",
            ],
            [
                "BR-CVC-02",
                "Public opinion period shall be 15 days unless a different period is "
                "notified in the DIGR / CVC order for that cycle; system stores the "
                "applicable period per cycle.",
            ],
            [
                "BR-CVC-03",
                "Post-notice Sub-committee revision is limited to objected rate lines "
                "unless minutes explicitly authorise wider revision.",
            ],
            [
                "BR-CVC-04",
                "Kaveri shall not display or calculate using future-dated rates before "
                "effective date; historical instruments continue to reference the "
                "version effective on the instrument date / valuation date as defined "
                "with the fee engine.",
            ],
            [
                "BR-CVC-05",
                "Individual Project Fixation acceptance authority is District Registrar "
                "under Sec. 45-B; final approval authority is Chairman CVC (IGR).",
            ],
            [
                "BR-CVC-06",
                "CVC remains final authority for policy and methodology of guideline "
                "rates (Sec. 45-B); system shall not allow SR/Citizen override of "
                "published guideline rates outside authorised modules.",
            ],
        ],
    )

    add_heading(doc, "User interface (high-level)", 3)
    add_bullets(
        doc,
        [
            "IGR / CVC dashboard: open cycles, pending approvals, gazette linking.",
            "DIGR notification console.",
            "DR inbox: forward to SR; individual project accept / inspect / propose; "
            "forward to CVC.",
            "SR workbench: evidence pack, propose rates, Sub-committee agenda, "
            "publish for public opinion, forward via DR.",
            "Sub-committee / CVC meeting screens: attendance, revise rates, minutes, "
            "decisions.",
            "Citizen portal: apply for individual project fixation; view proposed "
            "rates; file objections during notice period; track status.",
        ],
    )

    add_heading(doc, "Integrations", 3)
    add_table(
        doc,
        ["System", "Purpose"],
        [
            ["KSRSAC GIS", "Maps / spatial layers as evidence and for later GIS valuation overlay"],
            ["Registration / transaction store", "Historical registration transaction data for proposals"],
            ["RTC / Bhoomi (or notified land records)", "RTC extracts as evidence"],
            ["Khata / ULBs / property tax systems (as available)", "Khata evidence for urban properties"],
            ["Town planning / BDA / UDA / local planning (as available)", "Layout / planning evidence"],
            ["SMS / e-Mail gateway", "Notifications"],
            ["Payment gateway (if fee notified for individual fixation)", "Application fee collection"],
            ["Guideline Value Calculation / Fee engine", "Consume Active CVC rates"],
            ["Document / gazette repository", "Store orders, notifications, gazette PDFs"],
        ],
    )

    add_heading(doc, "Data requirements", 3)
    add_heading(doc, "Core entities (logical)", 4)
    add_table(
        doc,
        ["Entity", "Key attributes"],
        [
            ["RevisionCycle", "cycle_id, order_ref, scope, status, created_by_IGR, dates"],
            ["DigirNotification", "notification_id, cycle_id, text, issued_on"],
            ["SrProposal", "proposal_id, cycle_id, sro_id, status, evidence_refs"],
            ["ProposedRateLine", "line_id, proposal_id, territorial_key, proposed_rate, unit, remarks"],
            ["SubCommitteeSitting", "sitting_id, proposal_id, members, minutes, outcome"],
            ["PublicNotice", "notice_id, proposal_id, start, end (15 days), publish_channels"],
            ["Objection", "objection_id, notice_id, objector, linked_lines, text, disposal"],
            ["CvcDecision", "decision_id, proposal_id, outcome, effective_date, gazette_ref"],
            ["GuidanceRateVersion", "rate_id, territorial_key, rate, unit, effective_from/to, source"],
            ["IndividualFixationApp", "app_id, applicant, property/project, status, fee"],
            ["InspectionReport", "report_id, app_id, DR, findings, proposed_value"],
            ["SecretaryFinalisation", "final_value, evidence_notes, submitted_to_IGR"],
            ["IgrApproval", "approval_id, app_id, decision, effective_date"],
        ],
    )

    add_heading(doc, "Retention", 4)
    add_para(
        doc,
        "Orders, notifications, proposals, minutes, objections, gazette PDFs and "
        "rate version history shall be retained per Department records-retention "
        "policy and remain available for audit and dispute resolution indefinitely "
        "while the related rate versions can affect registered instruments.",
    )

    add_heading(doc, "Migration (high level)", 4)
    add_para(
        doc,
        "Existing CVC / guideline rate tables from Kaveri 2.0 shall be imported as "
        "baseline GuidanceRateVersion records with source = Legacy, effective dates "
        "as currently applied. Open revision activities (if any) are out of automated "
        "migration and restart under the new workflows after go-live.",
    )

    add_heading(doc, "Requirements traceability matrix (RTM) — template", 3)
    add_table(
        doc,
        ["Req ID", "Legal anchor", "Process", "User story (discussion)", "Priority"],
        [
            ["FR-CVC-001", "Sec. 2(ac)", "Common", "US-CVC-03", "Must"],
            ["FR-CVC-GR-001…015", "Sec. 45-B", "General Revision", "US-CVC-01, US-CVC-07", "Must"],
            ["FR-CVC-IP-001…007", "Sec. 45-B", "Individual Project", "US-CVC-01", "Must"],
            ["FR-CVC-004/005/014", "Sec. 45-B / 45-A handoff", "Publish & adopt", "US-CVC-02, US-GV-02", "Must"],
            ["FR-CVC-003", "Sec. 45-B methodology", "Evidence pack", "US-GIS-01 (evidence)", "Must"],
        ],
    )

    # ------------------------------------------------------------------
    # NFR
    # ------------------------------------------------------------------
    add_heading(doc, "Non-functional requirements", 2)
    add_heading(doc, "Performance and Scalability", 3)
    add_bullets(
        doc,
        [
            "Public opinion pages shall support state-wide concurrent read traffic "
            "during notice windows without degrading SR workbenches.",
            "Rate publish job shall activate large rate sets (state-wide) within an "
            "agreed overnight / controlled window before effective date.",
        ],
    )
    add_heading(doc, "Security and Data Privacy", 3)
    add_bullets(
        doc,
        [
            "Role-based access; maker-checker for publish to Active where configured.",
            "Personal data in objections / applications protected per department policy; "
            "Aadhaar if used only via approved e-KYC patterns.",
        ],
    )
    add_heading(doc, "System Availability and Error Handling", 3)
    add_bullets(
        doc,
        [
            "Publish failure shall not leave partial Active sets; use transactional "
            "activation or clearly marked rollback.",
            "Integration failures (KSRSAC / RTC) shall allow manual evidence upload "
            "with reason code so proposals are not blocked indefinitely.",
        ],
    )
    add_heading(doc, "Security Audit and Compliance (VAPT Policy)", 3)
    add_para(
        doc,
        "Module shall comply with Department / Kaveri 3.0 VAPT and audit requirements "
        "before production go-live.",
    )

    # ------------------------------------------------------------------
    # Risk, fallbacks, training
    # ------------------------------------------------------------------
    add_heading(doc, "Risk and Mitigation Strategy", 2)
    add_table(
        doc,
        ["Risk", "Impact", "Mitigation"],
        [
            [
                "Delayed Sub-committee / CVC sittings",
                "Revision cycle slips; old rates persist",
                "Ageing MIS; escalation to DIGR / IGR; configurable reminders",
            ],
            [
                "Incomplete evidence / wrong GIS join",
                "Incorrect proposed rates",
                "Mandatory evidence checklist; KSRSAC validation; sample audit",
            ],
            [
                "Effective-date publish miss",
                "Duty calculated on stale rates",
                "Pre-publish rehearsal; monitoring on T-1; freeze edits after approve",
            ],
            [
                "Public objection flood",
                "Portal / Sub-committee overload",
                "Rate-line linked objections; batch disposal templates",
            ],
        ],
    )

    add_heading(doc, "System Fallbacks & Error Handling", 2)
    add_bullets(
        doc,
        [
            "If automated gazette-to-rate activation fails, authorised CVC Admin may "
            "trigger controlled manual publish with dual approval and full audit.",
            "If citizen portal is unavailable during public opinion, SRO offline "
            "objection register shall be digitised same day.",
            "Individual Project path: if Secretary CVC returns proposal, DR retains "
            "full history; citizen sees status and deficiency list.",
        ],
    )

    add_heading(doc, "Training and Change Management", 2)
    add_heading(doc, "Target audience", 3)
    add_bullets(
        doc,
        [
            "IGR / CVC secretariat, DIGR Valuation, DRs, SRs, Sub-committee members, "
            "Kaveri IT Cell.",
            "Citizen helpdesk for individual project application and public objections.",
        ],
    )
    add_heading(doc, "Training delivery", 3)
    add_bullets(
        doc,
        [
            "Process walkthrough of General Revision (12 steps) and Individual Project "
            "(6 steps) with sandbox revision cycle.",
            "Job aids: evidence pack checklist; Sub-committee minutes template; "
            "gazette linking checklist.",
        ],
    )
    add_heading(doc, "Citizen change management", 3)
    add_para(
        doc,
        "Portal messaging for public opinion windows and for individual project "
        "fixation eligibility; FAQs linking Sec. 45-B and 15-day notice.",
    )
    add_heading(doc, "Post-Go-Live support", 3)
    add_para(
        doc,
        "Hypercare with DIGR Valuation and IT Cell for first General Revision cycle "
        "and first N individual project approvals.",
    )

    # ------------------------------------------------------------------
    # Appendix
    # ------------------------------------------------------------------
    add_heading(doc, "Appendix A — References", 2)
    add_numbered(
        doc,
        [
            "Requirement Discussions/Daily Reports/Document_Registration_requirement_01092026_v2.docx "
            "(discussion 31-08-2026 to 01-09-2026 — Guideline value calculation; "
            "Valuation Module CVC; GIS valuation).",
            "Requirement Discussions/BR_Discussion_Prep_Pack_Document_StampDuty_Fees_GuidelineValue_28Aug2026.docx "
            "(handoff note to Sr.14 CVC/GIS).",
            "Acts_Rules/Document/THE KARNATAKA STAMP ACT 1957.pdf — Secs. 2(ac), 45-A, 45-B.",
            "Acts_Rules/Document/Karnataka Stamp (Constitution of Central Valuation "
            "Committee…) Rules, 2003.docx — file embeds Prevention of Undervaluation "
            "Rules, 1977 text (GSR 81 / RD 73 EST 74; RD 264 MUNOMU 99).",
            "Acts_Rules/Document/The Karnataka Registration Rules 1965.pdf — Rules 13–15.",
            "Workshop process (user-confirmed): General Revision (12 steps); Fixation "
            "of guidance value for new individual project (6 steps).",
            "Format reference: Finalized BRD/Marriage/RFP/BRD_Marriage_BRD_v8.docx.",
            "Related: Finalized BRD/Document Registration BRD §3.2.4 / §3.3.3 "
            "(CVC legal tables).",
        ],
    )

    add_heading(doc, "Appendix B — Discussion user stories (source mapping)", 2)
    add_para(
        doc,
        "User stories from Document_Registration_requirement_01092026_v2 mapped into "
        "this BRD:",
    )
    add_table(
        doc,
        ["US ID", "Summary", "BRD coverage"],
        [
            [
                "US-CVC-01",
                "IGR / CVC estimate, publish, revise guidelines; constitute sub-committees",
                "Process A & B; FR-CVC-GR-*; FR-CVC-002",
            ],
            [
                "US-CVC-02",
                "Enter, update, publish guideline rates for SR and Citizen",
                "FR-CVC-004, FR-CVC-GR-014, FR-CVC-IP-006",
            ],
            [
                "US-CVC-03",
                "Maintain CVC as statutory body Sec. 2(ac)",
                "FR-CVC-001",
            ],
            [
                "US-CVC-07",
                "Operate on Sec. 45-B framework (Act 8 of 2003)",
                "Legal §; Process A & B",
            ],
            [
                "US-GV-02",
                "Use official Sec. 45-B guidelines in calculation",
                "FR-CVC-005 handoff",
            ],
            [
                "US-GIS-01",
                "Locate property on GIS and apply matching CVC rate",
                "Evidence pack + handoff to GIS module",
            ],
        ],
    )

    add_heading(doc, "Acceptance and sign-off of BRD", 2)
    add_table(
        doc,
        ["Role", "Name", "Signature", "Date"],
        [
            ["Business Analyst", "Nandha Kumar", "", ""],
            ["Product Owner", "M V Prashanth", "", ""],
            ["Domain expert — DIGR Valuation", "", "", ""],
            ["Kaveri IT Cell", "", "", ""],
            ["Committee / Approver", "", "", ""],
        ],
    )

    doc.save(str(DST))
    print(f"Wrote {DST}")


if __name__ == "__main__":
    build()
