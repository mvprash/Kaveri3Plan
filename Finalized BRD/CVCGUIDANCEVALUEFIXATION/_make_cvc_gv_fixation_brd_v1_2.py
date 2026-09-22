# -*- coding: utf-8 -*-
"""Create BRD_CVC_Guidance_Value_Fixation_v1.2.docx from the current v1.docx.

Adds presentation slides 5–7 content into Legal and regulatory reference:
  - Rule 3: Central Valuation Committee — Composition
  - Rule 4: Market Valuation Sub-Committees — Composition
  - Rule 6: Guidelines for estimating guidance value (+ e-source tags)

Base file is the user-updated BRD_CVC_Guidance_Value_Fixation_v1.docx (v1.1).
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from docx.text.paragraph import Paragraph

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(r"E:\MVP\Kaveri 3.0\Source Code\Kaveri 3 Plan\Finalized BRD\CVCGUIDANCEVALUEFIXATION")
SRC = BASE / "BRD_CVC_Guidance_Value_Fixation_v1.docx"
DST = BASE / "BRD_CVC_Guidance_Value_Fixation_v1.2.docx"
OUT_VERSION = "1.2"
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


def insert_paragraph_before(paragraph: Paragraph, text: str = "", style: str | None = None) -> Paragraph:
    """Insert a new paragraph immediately before `paragraph`."""
    new_p = OxmlElement("w:p")
    paragraph._p.addprevious(new_p)
    new_para = Paragraph(new_p, paragraph._parent)
    if style:
        new_para.style = style
    if text:
        new_para.add_run(text)
    return new_para


def insert_heading_before(paragraph: Paragraph, text: str, level: int) -> Paragraph:
    style = f"Heading {level}"
    return insert_paragraph_before(paragraph, text, style=style)


def insert_para_before(paragraph: Paragraph, text: str) -> Paragraph:
    return insert_paragraph_before(paragraph, text)


def insert_bullets_before(paragraph: Paragraph, items: list[str]) -> None:
    # Insert in reverse so final order is correct (each addprevious stacks upward).
    for item in reversed(items):
        insert_paragraph_before(paragraph, item, style="List Bullet")


def insert_table_before(paragraph: Paragraph, headers: list[str], rows: list[list[str]]) -> None:
    """Create a table and place it before `paragraph`."""
    # python-docx has no native insert-table-before; add at end then move XML.
    doc = paragraph.part.document
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    for i, h in enumerate(headers):
        set_cell_text(table.rows[0].cells[i], h, bold=True)
        shade_cell(table.rows[0].cells[i], "D9E2F3")
    for ri, row in enumerate(rows, start=1):
        for ci, val in enumerate(row):
            set_cell_text(table.rows[ri].cells[ci], val if val is not None else "")

    tbl = table._tbl
    tbl.getparent().remove(tbl)
    paragraph._p.addprevious(tbl)
    # spacer paragraph after table (before the anchor)
    insert_paragraph_before(paragraph, "")


def find_paragraph(doc: Document, exact: str | None = None, contains: str | None = None) -> Paragraph:
    for p in doc.paragraphs:
        t = p.text.strip()
        if exact is not None and t == exact:
            return p
        if contains is not None and contains in t:
            return p
    raise SystemExit(f"Paragraph not found: exact={exact!r} contains={contains!r}")


def update_document_control_version(doc: Document) -> None:
    for table in doc.tables:
        if len(table.rows) < 2 or len(table.columns) != 2:
            continue
        # Document-control key/value table: first row often Field | Value
        first = [c.text.strip() for c in table.rows[0].cells]
        if first[:2] != ["Field", "Value"] and first[0] not in ("Document ID", "Field"):
            # Accept kv tables that start with Document ID
            if first[0] != "Document ID" and "Document ID" not in [
                r.cells[0].text.strip() for r in table.rows
            ]:
                continue
        for row in table.rows:
            key = row.cells[0].text.strip()
            if key == "Version" and len(row.cells) >= 2:
                set_cell_text(row.cells[1], OUT_VERSION)
            if key == "Last updated" and len(row.cells) >= 2:
                set_cell_text(row.cells[1], OUT_DATE)


def append_version_history_row(doc: Document) -> None:
    for table in doc.tables:
        if not table.rows:
            continue
        headers = [c.text.strip() for c in table.rows[0].cells]
        if headers[:3] == ["Version", "Date", "Author"]:
            row = table.add_row()
            values = [
                OUT_VERSION,
                OUT_DATE,
                "Nandha Kumar",
                "Added CVC Rules 2003 content from presentation slides 5–7: "
                "CVC composition (Rule 3), Market Valuation Sub-Committees (Rule 4), "
                "guidelines for estimating guidance value with e-source tags (Rule 6)",
                "Prashanth",
            ]
            for i, val in enumerate(values):
                if i < len(row.cells):
                    set_cell_text(row.cells[i], val)
            return
    raise SystemExit("Version history table not found")


def insert_slide_content(doc: Document) -> None:
    """Insert Rules 3 / 4 / 6 sections before Stakeholders and actors.

    Blocks are inserted Rule 3 → Rule 4 → Rule 6 so final order is correct
    (each block is added before the Stakeholders anchor).
    """
    anchor = find_paragraph(doc, exact="Stakeholders and actors")

    # --- Rule 3 (first) ---
    insert_heading_before(
        anchor,
        "Central Valuation Committee — Composition (Rule 3)",
        3,
    )
    insert_para_before(
        anchor,
        "Source: Karnataka Stamp (Constitution of Central Valuation Committee for "
        "Estimation, Publication and Revision of Market Value Guidelines of Properties) "
        "Rules, 2003 — Rule 3, under Sec. 45-B of the Karnataka Stamp Act, 1957 "
        "(presentation slide 5).",
    )
    insert_table_before(
        anchor,
        ["Role / item", "Detail (Rule 3)"],
        [
            ["Chairman", "Commissioner of Stamps (IGR)"],
            ["Member Secretary", "DIGR (Valuation)"],
            ["Strength", "Total number of members shall not exceed twenty"],
            [
                "Members — one representative from each",
                "(i) Directorate of Town Planning; "
                "(ii) Directorate of Survey and Settlement; "
                "(iii) Bangalore City Corporation; "
                "(iv) Bangalore Development Authority; "
                "(v) Income-tax Department; "
                "(vi) Karnataka Public Works Department; "
                "(vii) Karnataka Irrigation Department; "
                "(viii) Registration and Stamps Department; "
                "(ix) Institute of Chartered Valuers; "
                "(x) Federation of Karnataka Chamber of Commerce and Industries; "
                "(xi) Any other person having expertise in the subject.",
            ],
        ],
    )
    insert_para_before(
        anchor,
        "Non-official members: term of two years, subject to the pleasure of the "
        "Government. Member Secretary handles day-to-day administration, "
        "correspondence, and compilation / publication of market value guidelines data.",
    )

    # --- Rule 4 ---
    insert_heading_before(
        anchor,
        "Market Valuation Sub-Committees — Composition (Rule 4)",
        3,
    )
    insert_para_before(
        anchor,
        "Source: Karnataka Stamp (Constitution of Central Valuation Committee for "
        "Estimation, Publication and Revision of Market Value Guidelines of Properties) "
        "Rules, 2003 — Rule 4 (presentation slide 6).",
    )
    insert_table_before(
        anchor,
        ["Aspect", "Provision (Rule 4)"],
        [
            [
                "Constitution",
                "CVC may constitute Market Valuation Sub-Committees for each "
                "sub-district and district for estimation and revision of market "
                "value guidelines of properties.",
            ],
            ["Head (sub-district)", "Tahsildar of the concerned taluk"],
            ["Member Secretary", "Sub-Registrar of the said sub-district"],
            ["Office", "Office of the Sub-Registrar"],
            [
                "Members drawn from",
                "Departments of Revenue; Survey and Settlement; Public Works; and "
                "Municipal Councils or Town Panchayaths.",
            ],
            [
                "Administrative control",
                "Registrar of the district (District Sub-Committees function under "
                "the Registrar of the district).",
            ],
            ["Supervisory control", "Central Valuation Committee"],
        ],
    )
    insert_para_before(
        anchor,
        "Sub-Registrar (Member Secretary) looks after administration of the "
        "Sub-Committees, correspondence, and compilation of market-value data as per "
        "Sub-Committee resolutions. CVC office (Rule 3): Office of the Inspector "
        "General of Registration and Commissioner of Stamps, or such other place as "
        "the Committee decides.",
    )

    # --- Rule 6 ---
    insert_heading_before(
        anchor,
        "Guidelines for estimating guidance value — Rule 6 (CVC Rules, 2003)",
        3,
    )
    insert_para_before(
        anchor,
        "Each Market Valuation Sub-Committee shall prepare statements showing average "
        "rates of agricultural and non-agricultural lands, and residential, commercial "
        "and industrial sites, using the following general guidelines as reference. "
        "These factors are also the evidence basis when proposing a new guidance value "
        "(presentation slide 7).",
    )
    insert_table_before(
        anchor,
        ["Category (Rule 6)", "Guidelines (summary)", "e-Source / Department tags"],
        [
            [
                "Lands — R.6(1)(a)",
                "Dry / garden / wet classification; soil class in survey records; "
                "other valuation influencers; value of adjacent / vicinity lands; "
                "crop nature & 5-year average yield; nearness to road & market; "
                "distance from village, location, level; transport & irrigation "
                "facilities (tank / well / pumpset).",
                "#Bhoomi/RTC  #SSLR  #KSRSAC-GIS  #Agriculture  #Irrigation  "
                "#Kaveri-Regn  #DTCP",
            ],
            [
                "House sites — R.6(1)(b)",
                "General locality site values; proximity to road / rail / bus; "
                "proximity to market & shops; offices, hospitals, schools; "
                "development / industrial activity; land tax & local body valuation; "
                "other material / special features (e.g. bore-well, lawn, garden, pool).",
                "#Kaveri-Regn  #KSRSAC-GIS  #ULB/e-Aasthi  #DTCP/BDA/UDA  #Transport",
            ],
            [
                "Other properties — R.6(1)(c)",
                "Nature & condition of property; purpose for which used; any other "
                "special valuation features.",
                "#Kaveri-Regn  #ULB-BldgPlan  #Khata  #KSRSAC-GIS",
            ],
            [
                "Rate suggestions — R.6(2)",
                "Non-agricultural / industrial: agricultural-rate multiple (village) "
                "or per sq.ft (town/city); agricultural: dry / wet / garden with "
                "village proximity; plantations (coconut / areca): treat as garden "
                "lands; buildings: PWD construction norms for the area; electricity, "
                "water, drainage counted in construction cost (not as ‘special’ features).",
                "#Bhoomi  #PWD-SoR  #Horticulture  #BESCOM/ESCOM  #BWSSB/ULB",
            ],
        ],
    )
    insert_para_before(
        anchor,
        "Rule 6 factors are the statutory checklist for Sub-Committee average-rate "
        "statements and for evidence packs attached to General Revision / Individual "
        "Project fixation proposals. Primary electronic feeds (as available): Kaveri "
        "registration transactions; Bhoomi/RTC & SSLR survey; KSRSAC GIS layers; ULB "
        "khata / property tax (e-Aasthi); DTCP / BDA / UDA planning; PWD Schedule of "
        "Rates; Agriculture / Horticulture / Irrigation department systems; utility "
        "masters (BESCOM/ESCOM, BWSSB/KUWSDB). Registrar verifies Sub-Committee "
        "statements (discrepancies remitted for rectification within 15 days); "
        "examined booklets / soft copies reach the Secretary, CVC in the first week "
        "of January of the next calendar year.",
    )


def main():
    if not SRC.exists():
        raise SystemExit(f"Source BRD not found: {SRC}")

    shutil.copy2(SRC, DST)
    doc = Document(str(DST))

    update_document_control_version(doc)
    append_version_history_row(doc)
    insert_slide_content(doc)

    try:
        doc.save(str(DST))
    except PermissionError:
        alt = BASE / "BRD_CVC_Guidance_Value_Fixation_v1.2_updated.docx"
        doc.save(str(alt))
        print(f"NOTE: {DST.name} locked; wrote {alt.name}")
        return

    print(f"Wrote {DST}")
    # verify headings
    for p in doc.paragraphs:
        if p.style.name.startswith("Heading") and (
            "Rule 3" in p.text or "Rule 4" in p.text or "Rule 6" in p.text
            or "Composition" in p.text or "estimating" in p.text.lower()
        ):
            print(f"  {p.style.name}: {p.text}")


if __name__ == "__main__":
    main()
