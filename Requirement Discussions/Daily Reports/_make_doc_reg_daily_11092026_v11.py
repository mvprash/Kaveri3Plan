# -*- coding: utf-8 -*-
"""Create Document_Registration_requirement_11092026_v1.1.docx

Schedule Sr.20 (11-09-2026) — Investigation and Search; Verify Document.
Format aligned to Document_Registration_requirement_07092026_v1.1.docx.
Source: Acts_Rules/Document/; modules list #20, #26.
Verify Document scoped to verification of registered documents and
issued digital e-stamp certificates.
"""
from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.table import Table

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(
    r"E:\MVP\Kaveri 3.0\Source Code\Kaveri 3 Plan\Requirement Discussions\Daily Reports"
)
DST = BASE / "Document_Registration_requirement_11092026_v1.1.docx"

HEADING_FONT = "Segoe UI"
HEADING_SIZE = Pt(14.5)
SUBHEAD_SIZE = Pt(13.5)
BODY_FONT = "Times New Roman"


def set_run_font(run, *, name=BODY_FONT, size=Pt(12), bold=False):
    run.bold = bold
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = size


def set_cell_text(cell, text: str, *, bold=False, size=Pt(10)) -> None:
    paras = cell.paragraphs
    first = paras[0]
    for extra in paras[1:]:
        extra._element.getparent().remove(extra._element)
    first.text = ""
    run = first.add_run(text)
    set_run_font(run, size=size, bold=bold)


def shade_header_row(table: Table, fill="D9E2F3") -> None:
    for cell in table.rows[0].cells:
        tc_pr = cell._tc.get_or_add_tcPr()
        shd = tc_pr.makeelement(
            qn("w:shd"),
            {qn("w:val"): "clear", qn("w:color"): "auto", qn("w:fill"): fill},
        )
        tc_pr.append(shd)
        for para in cell.paragraphs:
            for run in para.runs:
                run.bold = True


def add_heading(doc: Document, text: str, size=HEADING_SIZE):
    para = doc.add_paragraph()
    run = para.add_run(text)
    set_run_font(run, name=HEADING_FONT, size=size, bold=True)
    return para


def add_note(doc: Document, bold_prefix: str, rest: str):
    para = doc.add_paragraph()
    r1 = para.add_run(bold_prefix)
    set_run_font(r1, name=HEADING_FONT, size=SUBHEAD_SIZE, bold=True)
    r2 = para.add_run(rest)
    set_run_font(r2, name=HEADING_FONT, size=SUBHEAD_SIZE)
    return para


def add_3col_table(doc: Document, headers: list[str], rows: list[list[str]]) -> Table:
    tbl = doc.add_table(rows=1 + len(rows), cols=3)
    tbl.style = "Table Grid"
    for i, h in enumerate(headers):
        set_cell_text(tbl.rows[0].cells[i], h, bold=True, size=Pt(12))
    shade_header_row(tbl)
    for ri, values in enumerate(rows, start=1):
        for ci, value in enumerate(values):
            set_cell_text(tbl.rows[ri].cells[ci], value, size=Pt(10))
    return tbl


ACTS_ROWS = [
    [
        "The Registration Act, 1908 (Central Act 16 of 1908)",
        "Primary — Investigation & Search; Verify registered document",
        "Sec. 57 — inspection of Books 1–2 / indexes and certified copies "
        "(open to any person, including Investigation agencies, for Book 1–2); "
        "Secs. 51, 54–55 — register-books and indexes that are searched; "
        "Secs. 78–79 — fees for searches and copies; Sec. 57(5) — certified copy "
        "admissible to prove contents of the original registered document",
    ],
    [
        "The Karnataka Registration Rules, 1965",
        "Primary (Rules) — Investigation & Search",
        "Chapter XX (Rules 135–154) — Inspection, Searches and Grant of Certified "
        "Copies; applications, fees, encumbrance certificates, production of "
        "register books",
    ],
    [
        "The Karnataka Stamp Act, 1957",
        "Related — Verify e-stamp / stamp authenticity",
        "Stamp / impressed-stamp framework against which an issued e-stamp "
        "certificate is verified at registration; Sec. 10 / payment modes; "
        "Secs. 33–34 — examination of instruments not duly stamped (context for "
        "duty verification at presentation)",
    ],
    [
        "Karnataka Stamp (Payment of Stamp Duty by means of e-Stamping) Rules, 2009",
        "Primary — Verify Document (digital e-stamp)",
        "Rule 11 — CRA software (unique ID, search/view by authorised officers, "
        "lock to prevent reuse); Rule 24 — e-stamp details on CRA website; "
        "Rules 29–30 — Registering Officer / DR / DC of Stamps to verify unique "
        "identification number and lock the certificate after verification",
    ],
]

SECTIONS_INVEST = [
    [
        "Sec. 57(1)",
        "Inspection of Books 1 & 2 and Index to Book 1; certified copies",
        "Core Investigation & Search API — any person (incl. Investigation "
        "agencies) may inspect / obtain copies on payment of fee",
    ],
    [
        "Sec. 57(2)–(3)",
        "Copies from Book 3 (wills) and Book 4 (miscellaneous) — restricted persons",
        "Search/copy for Investigation agencies limited unless applicant is "
        "executant / claimant / agent / representative (or after death for Book 3)",
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
]

SECTIONS_VERIFY = [
    [
        "Sec. 57 (Registration Act)",
        "Certified copy / inspection as proof of registered document",
        "Citizen / officer / agency verifies that a deed was registered and "
        "reads its registered contents via certified copy or Book 1–2 inspection",
    ],
    [
        "Sec. 60 (Registration Act)",
        "Certificate of registration endorsed on the document",
        "Verify that the instrument bears a valid registration certificate "
        "(number, book, page)",
    ],
    [
        "Stamp Act — Sec. 10 / payment modes",
        "How stamp duty may be paid (incl. e-stamp)",
        "Context for verifying that duty on the instrument was paid by an "
        "issued digital e-stamp certificate",
    ],
    [
        "Stamp Act — Secs. 33–34",
        "Examination / impounding; inadmissibility if not duly stamped",
        "SRO must satisfy that the instrument (incl. via e-stamp) is duly stamped "
        "before acting on / registering it",
    ],
]

RULES_INVEST = [
    [
        "Rule 135–136 (Ch. XX)",
        "Applications in writing; no inspection of unregistered documents",
        "Investigation / search intake; block search of documents still under "
        "registration",
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
        "Certificate of encumbrance — particulars, language, multi-office, "
        "dual search, party-made search notes",
        "EC search workflow (property / person list) feeding Investigation & Search",
    ],
    [
        "Rules 155–156",
        "Production of Register books in Court; safe-custody fees via Court",
        "Court / agency production of original register books when required",
    ],
]

RULES_VERIFY = [
    [
        "e-Stamp Rules — Rule 11(a),(j),(n),(o)",
        "Unique identification number; barcode/security; departmental search/"
        "view; details on CRA server",
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
        "Core Verify Document step — SRO / DR / DC of Stamps enters UIN with "
        "password and matches certificate details on system",
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
]

NOTIF_ROWS = [
    [
        "The Karnataka Registration Rules, 1965 (under Registration Act Sec. 69)",
        "Parent subordinate legislation for Inspection, Searches and Certified Copies",
        "Investigation & Search",
    ],
    [
        "RD 403 ESR 85 (27 May 1986) as amended by RD/46/MNMU/2025 "
        "(registration fee table under Sec. 78)",
        "Search / inspection / certified-copy / EC fees",
        "Investigation & Search — fee masters",
    ],
    [
        "Karnataka Stamp (Payment of Stamp Duty by means of e-Stamping) "
        "Rules, 2009 (and CRA agreement / Forms)",
        "Digital e-stamp issue, website publication, SRO verify & lock",
        "Verify Document (e-stamp)",
    ],
    [
        "Registration Act Sec. 57 practice / CC workflow",
        "Certified copies and Book 1–2 inspection as the statutory verify path "
        "for already-registered documents",
        "Verify Document (registered deed)",
    ],
]

STORIES_INVEST = [
    (
        "US-IS-01",
        "citizen / Investigation agency / other authorised person",
        "apply for inspection or search of Book 1–2 and Index to Book 1 under "
        "Sec. 57(1) and Rules 135–139 (Form No. 22), paying search fee in advance",
        "I can locate registered entries affecting a person or property",
    ),
    (
        "US-IS-02",
        "Sub-Registrar / DEO",
        "run office-assisted search under Rule 146, record the result on the "
        "application, and issue a certificate of encumbrance or person-wise list "
        "under Rules 148–154",
        "search results and EC / list outputs are complete and auditable",
    ),
    (
        "US-IS-03",
        "citizen / Investigation agency",
        "obtain a signed and sealed certified copy under Sec. 57(5) and Rule 140 "
        "when I am entitled",
        "the copy is admissible to prove the contents of the registered document",
    ),
    (
        "US-IS-04",
        "Sub-Registrar",
        "refuse inspection of unregistered documents (Rule 136) and mediate "
        "Book 3/4 searches only for entitled persons (Sec. 57(2)–(4); Rule 144)",
        "restricted books stay protected while public books remain searchable",
    ),
    (
        "US-IS-05",
        "Court / Investigation agency (via Court)",
        "requisition production of register books under Rules 155–156 when "
        "originals are required",
        "safe custody and return of books are tracked",
    ),
]

STORIES_VERIFY = [
    (
        "US-VD-01",
        "citizen / officer / Investigation agency",
        "verify that a document was registered by inspecting Book 1–2 or "
        "obtaining a Sec. 57 certified copy, and check the Sec. 60 registration "
        "certificate particulars",
        "I can confirm authenticity of an already-registered deed",
    ),
    (
        "US-VD-02",
        "Sub-Registrar / District Registrar / DC of Stamps",
        "verify an issued digital e-stamp by entering its unique identification "
        "number under e-Stamp Rule 29 and matching details on the CRA system / "
        "website (Rules 11, 24)",
        "duty payment on the instrument is confirmed before registration proceeds",
    ),
    (
        "US-VD-03",
        "Sub-Registrar / District Registrar / DC of Stamps",
        "lock the e-stamp certificate after successful verification under "
        "Rule 30 (and Rule 11(l))",
        "the same UIN cannot be reused on another instrument",
    ),
    (
        "US-VD-04",
        "presentant / DEO",
        "capture the e-stamp UIN on each page of the instrument as required by "
        "Rule 28 so that verification can be completed at presentation",
        "verify-and-lock can run without missing UIN data",
    ),
    (
        "US-VD-05",
        "authorised CRA / departmental user",
        "search and view any e-stamp certificate and cancel spoiled/unused "
        "certificates under Rule 11(n),(m)",
        "e-stamp inventory and authenticity checks are available to authorised "
        "officers",
    ),
]


def add_story(doc: Document, sid: str, actor: str, want: str, so_that: str) -> None:
    para = doc.add_paragraph()
    r0 = para.add_run(f"{sid}. ")
    set_run_font(r0, name=HEADING_FONT, size=Pt(11), bold=True)
    r1 = para.add_run(f"As a {actor}, I want to {want}, so that {so_that}.")
    set_run_font(r1, name=HEADING_FONT, size=Pt(11))


def build_meta(doc: Document) -> None:
    tbl = doc.add_table(rows=4, cols=2)
    tbl.style = "Table Grid"
    rows = [
        ("Date", "11-09-2026"),
        (
            "Topics",
            "Investigation and Search; Verify Document (registered document / "
            "issued digital e-stamp) — Schedule Sr.20; modules #20, #26",
        ),
        (
            "Attendees",
            "Kaveri IT Cell, AIGR Computers team, Domain Expert and committee members",
        ),
        (
            "Version",
            "1.1 (15-09-2026) — Acts, sections, Rules, notifications and user "
            "stories for Investigation & Search and Verify Document "
            "(registered deed / e-stamp)",
        ),
    ]
    for i, (a, b) in enumerate(rows):
        set_cell_text(tbl.rows[i].cells[0], a, bold=True, size=Pt(12))
        set_cell_text(tbl.rows[i].cells[1], b, size=Pt(12))


def main() -> None:
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    build_meta(doc)

    doc.add_paragraph()
    add_note(
        doc,
        "Scope: ",
        "Discussion topic dated 11-09-2026 (Schedule Sr.20) — (1) Investigation "
        "and Search of registration records (Books / indexes / EC / certified "
        "copies), including access usable by Investigation agencies under "
        "Sec. 57; (2) Verify Document — verification of an already-registered "
        "document and of an issued digital e-stamp certificate. "
        "Source folder: Acts_Rules/Document/. EC functional issues (Sr.26) are "
        "out of scope except as the search path under Rules 148–154.",
    )

    doc.add_paragraph()
    add_heading(doc, "1. Primary Acts")
    add_3col_table(
        doc, ["Act / instrument", "Role", "Relevance to topics"], ACTS_ROWS
    )

    doc.add_paragraph()
    add_heading(doc, "2. Relevant sections")

    doc.add_paragraph()
    add_heading(doc, "2.1 Investigation and Search", SUBHEAD_SIZE)
    add_3col_table(
        doc,
        ["Section", "Topic", "BRD / system relevance"],
        SECTIONS_INVEST,
    )

    doc.add_paragraph()
    add_heading(
        doc,
        "2.2 Verify Document (registered document / digital e-stamp)",
        SUBHEAD_SIZE,
    )
    add_3col_table(
        doc,
        ["Section", "Topic", "BRD / system relevance"],
        SECTIONS_VERIFY,
    )

    doc.add_paragraph()
    add_heading(doc, "3. Relevant Rules")

    doc.add_paragraph()
    add_heading(
        doc,
        "3.1 Investigation and Search — Karnataka Registration Rules, 1965",
        SUBHEAD_SIZE,
    )
    add_3col_table(
        doc, ["Rule", "Requirement", "System feature"], RULES_INVEST
    )

    doc.add_paragraph()
    add_heading(
        doc,
        "3.2 Verify Document — e-Stamping Rules, 2009 & Registration Rules",
        SUBHEAD_SIZE,
    )
    add_3col_table(
        doc, ["Rule", "Requirement", "System feature"], RULES_VERIFY
    )

    doc.add_paragraph()
    add_heading(doc, "4. Notifications / amendments")
    add_3col_table(
        doc, ["Instrument", "Effect", "Topics"], NOTIF_ROWS
    )

    doc.add_paragraph()
    add_heading(doc, "5. User Stories")
    intro = doc.add_paragraph()
    r = intro.add_run(
        "Derived from Schedule Sr.20 Acts, sections and Rules "
        "(Investigation & Search — modules #20; Verify Document — modules #26)."
    )
    set_run_font(r, name=HEADING_FONT, size=Pt(11))

    doc.add_paragraph()
    add_heading(doc, "5.1 Investigation and Search", SUBHEAD_SIZE)
    for story in STORIES_INVEST:
        add_story(doc, *story)

    doc.add_paragraph()
    add_heading(
        doc,
        "5.2 Verify Document (registered document / digital e-stamp)",
        SUBHEAD_SIZE,
    )
    for story in STORIES_VERIFY:
        add_story(doc, *story)

    doc.add_paragraph()
    add_note(
        doc,
        "Note: ",
        "Schedule mapping — Investigation and Search = modules list #20; "
        "Verify Document = modules list #26 (both under Sr.20). Investigation "
        "agencies are not named as a separate statutory class in "
        "Acts_Rules/Document; Book 1–2 inspection and certified copies under "
        "Sec. 57(1)/(5) apply to any person. Book 3/4 remain restricted. "
        "Verify Document for e-stamp is Rule 29–30 (UIN verify + lock); for "
        "registered deeds it is Sec. 57 certified copy / Book inspection and "
        "Sec. 60 registration certificate checks. Stamp Act Secs. 67 / 67-B "
        "(departmental stamp inspection / premises search) are revenue-officer "
        "powers, not Investigation-agency search, and are not expanded here.",
    )

    doc.save(str(DST))
    print(f"Wrote {DST}")

    check = Document(str(DST))
    print("tables=", len(check.tables))
    for i, t in enumerate(check.tables):
        print(
            f"  {i}: {len(t.rows)}x{len(t.columns)} | "
            f"{t.rows[0].cells[0].text.strip()[:50]}"
        )
    stories = sum(
        1 for p in check.paragraphs if p.text.strip().startswith(("US-IS-", "US-VD-"))
    )
    print(f"user_stories={stories}")


if __name__ == "__main__":
    main()
