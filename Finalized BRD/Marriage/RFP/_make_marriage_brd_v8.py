# -*- coding: utf-8 -*-
"""Create BRD_Marriage_BRD_v8.docx from v7.

Department / workshop additions:
1. SMA Sec. 15 & 16 — residence / eligibility measured as ≥ 30 days before
   the date of notice application.
2. Cross-link §3.4 notifications into related Acts / sections / rules rows.
3. Multiple cross-references on certified copy of the document.
4. Address capture per e-Governance standard.
5. Citizen selects marriage certificate language + preview before confirm.
6. Remove Form II requirement for Hindu Marriage (Form II-A retained).
7. Birth certificate pull via e-Janma and Marks Card integration.
8. SR Refusal with reason and order before registration / solemnization.
"""
from __future__ import annotations

import re
import shutil
import sys
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(r"E:\MVP\Kaveri 3.0\Source Code\Kaveri 3 Plan\Finalized BRD\Marriage\RFP")
SRC = BASE / "BRD_Marriage_BRD_v7.docx"
DST = BASE / "BRD_Marriage_BRD_v8.docx"
OUT_VERSION = "8"
OUT_DATE = "09-09-2026"

CHANGE_SUMMARY = (
    "SMA Sec. 15/16: residence ≥ 30 days before notice application; "
    "cross-link §3.4 notifications into related Acts/sections/rules; "
    "multiple cross-references on certified copy; e-Governance address "
    "standard; certificate language selection + preview; remove Form II "
    "for Hindu Marriage; e-Janma / Marks Card birth-certificate pull; "
    "SR Refusal with reason and order before registration/solemnization"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def set_para_text(paragraph: Paragraph, text: str) -> None:
    if not paragraph.runs:
        paragraph.add_run(text)
        return
    paragraph.runs[0].text = text
    for r in paragraph.runs[1:]:
        r.text = ""


def set_cell_text(cell: _Cell, text: str) -> None:
    paras = cell.paragraphs
    if not paras:
        cell.add_paragraph(text)
        return
    set_para_text(paras[0], text)
    for p in paras[1:]:
        set_para_text(p, "")


def set_row(table: Table, ri: int, values: list[str]) -> None:
    row = table.rows[ri]
    for ci, val in enumerate(values):
        if ci < len(row.cells):
            set_cell_text(row.cells[ci], val)


def add_version_row(table: Table, values: list[str]) -> None:
    table._tbl.append(deepcopy(table.rows[-1]._tr))
    set_row(table, len(table.rows) - 1, values)


def add_fr_row(table: Table, values: list[str]) -> None:
    table._tbl.append(deepcopy(table.rows[-1]._tr))
    set_row(table, len(table.rows) - 1, values)


def style_name(paragraph: Paragraph) -> str:
    return str(paragraph.style.name) if paragraph.style else ""


def find_para(
    doc: Document,
    exact: str | None = None,
    contains: str | None = None,
    heading_only: bool = False,
) -> Paragraph:
    for p in doc.paragraphs:
        if heading_only and not style_name(p).startswith("Heading"):
            continue
        t = p.text.strip()
        if exact is not None and t == exact:
            return p
        if contains is not None and contains in t:
            return p
    raise KeyError(f"Paragraph not found: exact={exact!r} contains={contains!r}")


def find_table_by_first_cell(doc: Document, first_cell: str) -> Table:
    for table in doc.tables:
        if table.rows and table.rows[0].cells[0].text.strip() == first_cell:
            return table
    raise KeyError(f"Table not found with first cell {first_cell!r}")


def find_row_by_col0(table: Table, value: str):
    for row in table.rows:
        if row.cells[0].text.strip() == value:
            return row
    raise KeyError(f"Row not found: {value!r}")


def append_if_missing(cell: _Cell, addition: str) -> None:
    text = cell.text.strip()
    if addition.strip() in text:
        return
    if not text:
        set_cell_text(cell, addition.strip())
        return
    joiner = " " if text.endswith((".", ";", ":")) else "; "
    set_cell_text(cell, text + joiner + addition.strip())


def replace_in_paragraphs(doc: Document, old: str, new: str) -> int:
    n = 0
    for p in doc.paragraphs:
        if old in p.text:
            set_para_text(p, p.text.replace(old, new))
            n += 1
    return n


def replace_in_tables(doc: Document, old: str, new: str) -> int:
    n = 0
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if old in cell.text:
                    set_cell_text(cell, cell.text.replace(old, new))
                    n += 1
    return n


def replace_everywhere(doc: Document, old: str, new: str) -> int:
    return replace_in_paragraphs(doc, old, new) + replace_in_tables(doc, old, new)


# ---------------------------------------------------------------------------
# 1. SMA Sec. 15 / 16 — 30 days before notice application
# ---------------------------------------------------------------------------
def update_sma_sec_15_16(doc: Document) -> None:
    sma = doc.tables[4]  # Special Marriage Act sections

    r15 = find_row_by_col0(sma, "Sec. 15")
    set_cell_text(
        r15.cells[2],
        "Other Forms eligibility — ceremony performed; parties living together; "
        "ages; residence ≥ 30 days before the date of notice application",
    )

    r16 = find_row_by_col0(sma, "Sec. 16")
    set_cell_text(
        r16.cells[2],
        "Public notice; 30-day objections; certificate with three witnesses; "
        "Sec. 15 conditions (incl. residence ≥ 30 days before the date of "
        "notice application) apply before registration",
    )

    # Keep Sec. 5 consistent (Intended Marriage residence)
    r5 = find_row_by_col0(sma, "Sec. 5")
    set_cell_text(
        r5.cells[2],
        "Generate and capture notice; jurisdiction — ≥ 30 days residence of at "
        "least one party before the date of notice application",
    )

    # FR-SMA-003 already has "immediately preceding the application" — align wording
    fr003 = find_row_by_col0(doc.tables[53], "FR-SMA-003")
    set_cell_text(
        fr003.cells[1],
        "System shall enforce Sec. 15 conditions for Other Forms: ceremony already "
        "performed and parties living together as husband and wife since; neither "
        "party has more than one spouse living; both parties ≥ 21 years at notice "
        "filing date; not within prohibited degrees; residence in the district "
        "≥ 30 days before the date of notice application",
    )

    # Length of residence field note in SMA party particulars (table 55)
    for table in doc.tables:
        for row in table.rows:
            if row.cells[0].text.strip() == "Length of residence":
                notes = row.cells[2].text.strip()
                if "notice application" not in notes.lower():
                    set_cell_text(
                        row.cells[2],
                        "Second Schedule / Sec. 15; validate ≥ 30 days before the "
                        "date of notice application for at least one party "
                        "(Intended: Sec. 5; Other Forms: Sec. 15)",
                    )

    # Business rule BR-SMA-007
    for table in doc.tables:
        for row in table.rows:
            if row.cells[0].text.strip() == "BR-SMA-007":
                set_cell_text(
                    row.cells[1],
                    "Notice jurisdiction requires ≥ 30 days residence of at least "
                    "one party in the district before the date of notice application",
                )
                break


# ---------------------------------------------------------------------------
# 2. Append notifications into related Acts / sections / rules
# ---------------------------------------------------------------------------
def crosslink_notifications(doc: Document) -> None:
    # Intro under notifications heading
    intro = find_para(
        doc,
        contains="Gazette notifications, Government Orders and amendments cited",
    )
    set_para_text(
        intro,
        "Gazette notifications, Government Orders and amendments cited in the "
        "Karnataka Rules or issued under the Acts. Each instrument below is also "
        "cross-referenced on the related Act / section / rule rows in §3.1–§3.3 "
        "so implementers can locate the statutory source beside the mapped "
        "requirement.",
    )

    acts = doc.tables[2]
    hma_secs = doc.tables[3]
    sma_secs = doc.tables[4]
    pma_secs = doc.tables[5]
    hma_rules = doc.tables[6]
    sma_rules = doc.tables[7]
    pma_rules = doc.tables[8]

    # --- Acts table ---
    append_if_missing(
        find_row_by_col0(acts, "The Hindu Marriage Act, 1955").cells[1],
        "Notifications: S.O. 4896 / HD 6 CIM 61 (4 Jul 1966); Registration of "
        "Hindu Marriages (Karnataka) (Amendment) Rules, 1999; G.S.R. 314 / "
        "G.S.R. 394 / HD 5 PIM 69; RD/48/MNMU/2023 (Amendment Rules, 2024); "
        "koE/65/mnmu/2021 (age proof); MME 109 MABHAB 2017 (address proof) — see §3.4",
    )
    append_if_missing(
        find_row_by_col0(acts, "The Special Marriage Act, 1954").cells[1],
        "Notifications: Special Marriage (Karnataka) Rules, 1961 "
        "(Notification No. HD 13MCIM 59(1), 2 May 1961); koE/65/mnmu/2021 "
        "(age proof); MME 109 MABHAB 2017 (address proof) — see §3.4",
    )
    append_if_missing(
        find_row_by_col0(acts, "The Parsi Marriage and Divorce Act, 1936").cells[1],
        "Notifications: Notification No. HD 6 PIM 67 (1967); Parsi Marriages "
        "and Divorce (Karnataka) Rules, 1961 (Notification No. HD 13 CIM 59) — see §3.4",
    )
    append_if_missing(
        find_row_by_col0(
            acts, "The Karnataka Guarantee of Services to Citizens Act, 2011"
        ).cells[1],
        "Notification / rules: Karnataka Guarantee of Services to Citizens "
        "Rules, 2012 (Gazette 29-Feb-2012) — see §3.4",
    )

    # --- HMA sections ---
    append_if_missing(
        find_row_by_col0(hma_secs, "Sec. 5").cells[2],
        "Age proof per circular koE/65/mnmu/2021 (Birth certificate / School "
        "Certificate / medical certificate; Aadhaar not age proof) — §3.4",
    )
    append_if_missing(
        find_row_by_col0(hma_secs, "Sec. 8").cells[2],
        "S.O. 4896 (Sub-Registrars as Registrars); RD/48/MNMU/2023 electronic "
        "filing / register / certificate; Amendment Rules 1999 (Form IA, "
        "II-A, scrutiny/refusal) — §3.4",
    )

    # --- SMA sections ---
    append_if_missing(
        find_row_by_col0(sma_secs, "Sec. 4").cells[2],
        "Age / eligibility evidence per koE/65/mnmu/2021 — §3.4",
    )
    append_if_missing(
        find_row_by_col0(sma_secs, "Sec. 5").cells[2],
        "Address proof documents per MME 109 MABHAB 2017 — §3.4",
    )
    append_if_missing(
        find_row_by_col0(sma_secs, "Sec. 15").cells[2],
        "Age proof per koE/65/mnmu/2021; address proof per MME 109 MABHAB 2017 — §3.4",
    )
    append_if_missing(
        find_row_by_col0(sma_secs, "Sec. 16").cells[2],
        "Procedure under Special Marriage (Karnataka) Rules, 1961 "
        "(Notification No. HD 13MCIM 59(1)) — §3.4",
    )

    # --- Parsi sections ---
    append_if_missing(
        find_row_by_col0(pma_secs, "Sec. 7").cells[2],
        "Notification No. HD 6 PIM 67 — Sub-Registrars as Registrars — §3.4",
    )

    # --- HMA Rules ---
    append_if_missing(
        find_row_by_col0(hma_rules, "Rule 3(1) + S.O. 4896").cells[1],
        "Instrument: S.O. 4896 / HD 6 CIM 61 (4 Jul 1966) — §3.4",
    )
    append_if_missing(
        find_row_by_col0(hma_rules, "Rule 4(1)").cells[1],
        "G.S.R. 314 / G.S.R. 394 / HD 5 PIM 69; RD/48/MNMU/2023 "
        "('or electronically') — §3.4",
    )
    append_if_missing(
        find_row_by_col0(hma_rules, "Rule 4(2)").cells[1],
        "Amendment Rules, 1999 (Form IA) — §3.4",
    )
    append_if_missing(
        find_row_by_col0(hma_rules, "Rule 4(4)").cells[1],
        "RD/48/MNMU/2023 ('or stored electronically'); Kaveri 3.0 does not "
        "require a separate Form II artefact — electronic register endorsement "
        "on Form II-A issuance — §3.4 / §3.5",
    )
    append_if_missing(
        find_row_by_col0(hma_rules, "Rule 4(5)").cells[1],
        "Amendment Rules, 1999 (immediate Form II-A); RD/48/MNMU/2023 — §3.4",
    )
    append_if_missing(
        find_row_by_col0(hma_rules, "Rule 6A").cells[1],
        "Amendment Rules, 1999 (scrutiny / written refusal order) — §3.4",
    )

    # --- SMA Rules ---
    append_if_missing(
        find_row_by_col0(sma_rules, "Rule 4").cells[1],
        "Made under Notification No. HD 13MCIM 59(1), 2 May 1961 — §3.4",
    )
    append_if_missing(
        find_row_by_col0(sma_rules, "Rule 7").cells[1],
        "Notification No. HD 13MCIM 59(1); Other Forms path — §3.4",
    )

    # --- Parsi Rules ---
    append_if_missing(
        find_row_by_col0(pma_rules, "Rule 1").cells[1],
        "Notification No. HD 13 CIM 59; Karnataka Gazette 18 May 1961 — §3.4",
    )
    append_if_missing(
        find_row_by_col0(pma_rules, "Rule 3").cells[1],
        "Aligned with Notification No. HD 6 PIM 67 (Registrar appointment) — §3.4",
    )


# ---------------------------------------------------------------------------
# 3. Remove Form II requirement (Hindu Marriage)
# ---------------------------------------------------------------------------
def remove_form_ii(doc: Document) -> None:
    # Forms mapping table — remove Form II row
    forms = doc.tables[10]
    for row in list(forms.rows):
        if row.cells[0].text.strip() == "Form II":
            forms._tbl.remove(row._tr)
            break

    # Heading / caption — mark not required (keep images in place)
    set_para_text(
        find_para(doc, exact="Form II", heading_only=True),
        "Form II — Not required in Kaveri 3.0",
    )
    set_para_text(
        find_para(doc, contains="Form II — Endorsement on reverse of memorandum"),
        "Form II (Endorsement — Rule 4(4)) is not required in Kaveri 3.0. "
        "Serial no., page and volume are assigned electronically when the "
        "Sub-Registrar digitally signs and Form II-A is issued. Legacy Form II "
        "specimen retained below for reference only.",
    )

    # Scope / statutory artefacts bullets
    replace_everywhere(
        doc,
        "Statutory artefacts: Form I (Memorandum), Form IA (Application), Form II "
        "(Endorsement — Rule 4(4)), Form II-A (Certificate)",
        "Statutory artefacts: Form I (Memorandum), Form IA (Application), "
        "Form II-A (Certificate) — Form II endorsement not required in Kaveri 3.0",
    )
    replace_everywhere(
        doc,
        "Statutory artefacts: Form I (Memorandum), Form IA (Application), Form II "
        "(Endorsement — Rule 4(4)), Form II-A (Certificate) — see §3.5.",
        "Statutory artefacts: Form I (Memorandum), Form IA (Application), "
        "Form II-A (Certificate) — Form II not required; see §3.5.",
    )

    # Key characteristics — Online
    replace_everywhere(
        doc,
        "Form I & Form IA + eSign; SR digital signature applies Form II endorsement and "
        "issues Form II-A certificate",
        "Form I & Form IA + eSign; SR digital signature assigns serial/page/volume and "
        "issues Form II-A certificate (no Form II)",
    )
    # Offline key characteristics / printout
    replace_everywhere(
        doc,
        "Form II (blank endorsement) & Form II-A",
        "Form II-A (no Form II blank endorsement)",
    )
    replace_everywhere(
        doc,
        "Printout taken on Form I, Form IA, Form II (blank endorsement) and Form II-A",
        "Printout taken on Form I, Form IA and Form II-A (Form II not required)",
    )
    replace_everywhere(
        doc,
        "Form II endorsement applied; marriage certificate (Form II-A) generated",
        "Serial/page/volume assigned; marriage certificate (Form II-A) generated",
    )
    replace_everywhere(
        doc,
        "Form II endorsement (Rule 4(4)) then Form II-A available for download",
        "Form II-A available for download (register endorsement electronic; Form II not used)",
    )
    replace_everywhere(
        doc,
        "SR DSC applies Form II endorsement then certificate.",
        "SR DSC assigns serial/page/volume then issues Form II-A certificate.",
    )
    replace_everywhere(
        doc,
        "SR digital signature applies Form II endorsement then certificate.",
        "SR digital signature assigns serial/page/volume then issues Form II-A.",
    )

    # FR headings
    replace_in_paragraphs(
        doc,
        "Offline channel — printout (Form I, Form IA, Form II), DEO upload",
        "Offline channel — printout (Form I, Form IA, Form II-A), DEO upload",
    )
    replace_in_paragraphs(
        doc,
        "Digital signature, Form II endorsement and certificate issuance (Form II-A)",
        "Digital signature, register entry and certificate issuance (Form II-A)",
    )

    # Stakeholders / DEO
    replace_everywhere(
        doc,
        "Online: eSign; Offline: physical signature on printed Form I / IA / II / II-A",
        "Online: eSign; Offline: physical signature on printed Form I / IA / II-A",
    )
    replace_everywhere(
        doc,
        "Check signatures on printed Form I / IA / II / II-A and upload to portal",
        "Check signatures on printed Form I / IA / II-A and upload to portal",
    )
    replace_everywhere(
        doc,
        "DEO-uploaded signed Form I, Form IA, Form II & II-A",
        "DEO-uploaded signed Form I, Form IA & Form II-A",
    )

    # Status model
    replace_everywhere(
        doc,
        "Serial / page / volume assigned, Form II endorsed",
        "Serial / page / volume assigned (electronic register; no Form II)",
    )

    # FR-HMA-061 printout
    fr061 = find_row_by_col0(doc.tables[49], "FR-HMA-061")
    set_cell_text(
        fr061.cells[1],
        "System shall generate a printout of Form I, Form IA and Form II-A with "
        "exact statutory wordings (Form II blank endorsement is not required)",
    )
    set_cell_text(
        fr061.cells[3],
        "Legal sign-off on templates; Form II not in printout pack; Kannada "
        "rendering correct",
    )

    # FR-HMA-080 DSC / certificate
    fr080 = find_row_by_col0(doc.tables[51], "FR-HMA-080")
    set_cell_text(
        fr080.cells[1],
        "On SR digital signature: assign serial no., page, volume; update the "
        "Hindu Marriages Register electronically; then issue Form II-A "
        "(certificate). Separate Form II endorsement artefact is not required",
    )
    set_cell_text(
        fr080.cells[3],
        "Register entry populated with date received, serial/page/volume and "
        "Registrar signature; Form II-A issued — both channels; no Form II",
    )

    # Offline Stage 2 FR may mention Form II
    fr072 = find_row_by_col0(doc.tables[50], "FR-HMA-072")
    txt = fr072.cells[1].text
    if "Form II" in txt and "Form II-A" in txt:
        set_cell_text(
            fr072.cells[1],
            re.sub(r",?\s*Form II(?!-A)", "", txt).replace("  ", " ").strip(),
        )

    # Targeted leftover clean-ups (avoid blanket Form II annotation)
    replace_everywhere(
        doc,
        "7.i.b.B, 7.i.b.C (Form II endorsement / register entry)",
        "7.i.b.B, 7.i.b.C (electronic register endorsement / Form II-A)",
    )
    replace_everywhere(
        doc,
        "Form II, register",
        "register / Form II-A",
    )
    replace_everywhere(
        doc,
        "Verification queue (Online / Offline Stage 1 / Stage 2), allocation, register, refuse",
        "Verification queue (Online / Offline Stage 1 / Stage 2), allocation, "
        "register, refuse (with reason and order)",
    )


# ---------------------------------------------------------------------------
# 4–8. New / updated functional requirements
# ---------------------------------------------------------------------------
def add_new_requirements(doc: Document) -> None:
    # --- Cross-references on certified copy (post-registration) ---
    post_reg = doc.tables[75]
    add_fr_row(
        post_reg,
        [
            "FR-HMA-100",
            "System shall allow the Sub-Registrar / authorized officer to add "
            "multiple cross-references on the certified copy of a registered "
            "marriage document (link to related register entries, prior "
            "certificates, court orders or other marriage records). Cross-"
            "references shall be retained with the certified-copy audit trail",
            "Must",
            "Multiple cross-reference entries savable per certified copy; "
            "visible on extract / certified copy print and in search",
        ],
    )

    # Also Special Marriage post-reg / reports area — add beside SMA notifications
    # Use table 77 (reports) or add near FR-SMA-054 table 76 notifications
    # Prefer adding to post-registration if shared; else SMA reports table
    # Table 75 is shared post-reg — FR-HMA-100 covers marriage module certified copies.

    # --- Address e-Governance standard ---
    # Bridegroom / bride / witness data-capture tables: update address notes
    egov_note = (
        "Address capture shall follow the e-Governance / MeitY address data "
        "standard (structured house/door no., street/locality, village/town/"
        "city, taluk, district, state, PIN / postal code, country) with MDM "
        "codes where available"
    )
    for table in doc.tables:
        for row in table.rows:
            label = row.cells[0].text.strip()
            if label in (
                "Current address of residence",
                "Permanent address of residence",
            ):
                append_if_missing(row.cells[2], egov_note)

    # FR under bridegroom capture — table 38 area uses field catalogue; add FR to
    # jurisdiction/data capture — use Hindu data capture marriage details table 36/37
    # Add to supporting documents / or a dedicated FR on bridegroom table 40 witnesses
    # Best: add to SRO scrutiny? Prefer data-capture — find FR-HMA-008/010 table
    for table in doc.tables:
        for row in table.rows:
            if row.cells[0].text.strip() == "FR-HMA-008":
                # append sibling FR after last row of that table later
                addr_table = table
                break
        else:
            continue
        break
    else:
        addr_table = doc.tables[46]  # fallback

    # Place address FR near post-reg / UI — also add dedicated FR-HMA-101 on
    # data-capture bridegroom FR table if FR-HMA-010 exists
    for table in doc.tables:
        ids = {r.cells[0].text.strip() for r in table.rows}
        if "FR-HMA-010" in ids or "FR-HMA-011" in ids:
            add_fr_row(
                table,
                [
                    "FR-HMA-101",
                    "System shall capture party and witness addresses as per the "
                    "e-Governance address standard (structured components and "
                    "PIN/postal code; MDM-driven district/taluk/village or urban "
                    "locality). Free-text-only address shall not be the sole "
                    "capture mode",
                    "Must",
                    "Structured address fields mandatory; certificate and "
                    "forms render e-Gov standard address without erroneous "
                    "sub-district",
                ],
            )
            break

    # SMA party particulars — FR-SMA-070
    for table in doc.tables:
        ids = {r.cells[0].text.strip() for r in table.rows}
        if "FR-SMA-062" in ids or "FR-SMA-063" in ids:
            add_fr_row(
                table,
                [
                    "FR-SMA-070",
                    "System shall capture Special Marriage party and witness "
                    "addresses as per the e-Governance address standard "
                    "(structured components and PIN/postal code; MDM-driven "
                    "jurisdiction codes)",
                    "Must",
                    "Structured address on notice, declarations and certificate",
                ],
            )
            break

    # --- Certificate language + preview ---
    # Update FR-HMA-037 and add stronger Must FR
    notif_tbl = doc.tables[76]
    fr037 = find_row_by_col0(notif_tbl, "FR-HMA-037")
    set_cell_text(
        fr037.cells[1],
        "Citizen shall select the marriage certificate language (English / "
        "Kannada / bilingual as configured). System shall generate a preview "
        "of the certificate in the selected language for citizen confirmation "
        "before final issuance / download",
    )
    set_cell_text(fr037.cells[2], "Must")
    set_cell_text(
        fr037.cells[3],
        "Language choice stored; preview matches issued PDF; confirm required "
        "before certificate finalize",
    )

    # SMA equivalent
    # Find FR-SMA-054 table (notifications) — paragraphs mention it; table may be 76 shared
    # Add FR-SMA-071 to solemnization/certificate table 61
    for table in doc.tables:
        ids = {r.cells[0].text.strip() for r in table.rows}
        if "FR-SMA-039" in ids or "FR-SMA-040" in ids:
            add_fr_row(
                table,
                [
                    "FR-SMA-071",
                    "Citizen shall select the Special Marriage certificate "
                    "language (English / Kannada / bilingual as configured). "
                    "System shall generate a preview before confirming "
                    "issuance / download (Fourth or Fifth Schedule)",
                    "Must",
                    "Preview in selected language; confirm gate before issue",
                ],
            )
            break

    # --- Birth certificate: e-Janma + Marks Card ---
    fr019 = find_row_by_col0(doc.tables[44], "FR-HMA-019")
    set_cell_text(
        fr019.cells[1],
        "Document checklist: [age proof, address proof, divorce decree if "
        "applicable], the document checklist is configurable.\n"
        "Age proof documents – Birth certificate (pull from e-Janma where "
        "available), School Certificate / Marks Card, if these are not "
        "available then medical certificate from the doctor.\n"
        "AADHAR cannot be considered for age proof.\n"
        "Address Proof Documents: Aadhaar Card, (Electricity/Telephone/Water) "
        "Bill, Voter ID Card, Gas connection certificate, Rental Agreement, "
        "Income Tax Assesment, Employer certificate, Passport, Bank Passbook "
        "(national and regional rural banks).\n"
        "System shall integrate with e-Janma and Marks Card sources to pull "
        "Birth Certificate / school marks-card particulars for age / DOB "
        "verification when the citizen opts in",
    )

    add_fr_row(
        doc.tables[44],
        [
            "FR-HMA-102",
            "System shall integrate with e-Janma and Marks Card services to "
            "retrieve Birth Certificate / marks-card data for age and date-of-"
            "birth verification during marriage registration. Citizen may "
            "still upload age proof manually where pull fails or is unavailable",
            "Must",
            "Successful pull populates DOB / age proof metadata; fallback "
            "upload path retained; audit of source (e-Janma / Marks Card / "
            "manual)",
        ],
    )

    # Integrations table
    integ = doc.tables[83]
    add_fr_row(
        integ,
        [
            "e-Janma (Birth Certificate)",
            "Outbound / Inbound",
            "Pull Birth Certificate particulars for age / DOB verification",
            "Both",
            "Platform / CRS",
            "TBD",
        ],
    )
    add_fr_row(
        integ,
        [
            "Marks Card (school / education board)",
            "Outbound / Inbound",
            "Pull Marks Card / school certificate particulars as alternate "
            "age proof when Birth Certificate is unavailable",
            "Both",
            "Platform / Education",
            "TBD",
        ],
    )

    # SMA supporting docs / eligibility — add FR-SMA-072 near FR-SMA-003 table
    add_fr_row(
        doc.tables[53],
        [
            "FR-SMA-072",
            "System shall integrate with e-Janma and Marks Card to pull Birth "
            "Certificate / marks-card data for Special Marriage age / DOB "
            "verification (Intended Marriage and Other Forms), with manual "
            "upload fallback",
            "Must",
            "Source recorded; aligns with circular koE/65/mnmu/2021 age-proof "
            "list (Aadhaar not age proof)",
        ],
    )

    # --- SR Refusal with reason and order before registration/solemnization ---
    # Strengthen Hindu scrutiny table
    add_fr_row(
        doc.tables[46],
        [
            "FR-HMA-103",
            "Before registration of the marriage, the Sub-Registrar shall have "
            "the option to Refuse the application with a recorded reason and a "
            "brief written / typed order (DSC-signed). Refusal shall be "
            "communicated to the parties and shall block certificate issuance "
            "until remedied or closed",
            "Must",
            "Refuse action available on SR workbench before register entry / "
            "Form II-A; reason + order PDF + notification; audit trail",
        ],
    )
    # Also on SR verification table for channel flow
    add_fr_row(
        doc.tables[50],
        [
            "FR-HMA-104",
            "At Online verification and Offline Stage 1 / Stage 2, SR may select "
            "Refusal (in addition to Approve / Reject-for-correction). Refusal "
            "requires reason code, narrative reason and generates a refusal "
            "order before any registration or certificate step",
            "Must",
            "Refusal distinct from return-for-correction; order issued; "
            "registration / solemnization blocked",
        ],
    )

    # Special Marriage — before solemnization / Other Forms registration
    add_fr_row(
        doc.tables[61],
        [
            "FR-SMA-073",
            "Before solemnization (Intended Marriage) or registration (Other "
            "Forms), the Sub-Registrar / Marriage Officer shall have the option "
            "to Refuse with a recorded reason and a brief written / typed order "
            "(DSC-signed). Refusal shall be communicated to the parties and "
            "shall block solemnization / certificate issuance",
            "Must",
            "Refuse available on SR workbench before Sec. 12 solemnization / "
            "Sec. 15–16 registration; reason + order + notification",
        ],
    )

    # Update FR-SMA-036 acceptance to mention Refusal
    fr036 = find_row_by_col0(doc.tables[61], "FR-SMA-036")
    append_if_missing(
        fr036.cells[1],
        "SR may also Refuse with reason and order (FR-SMA-073) before "
        "solemnization / registration",
    )

    # Stakeholders already says "refuse with order" — ensure glossary
    for table in doc.tables:
        for row in table.rows:
            if row.cells[0].text.strip() == "SR Verification":
                append_if_missing(
                    row.cells[1],
                    "Includes Refuse with reason and order before registration / "
                    "solemnization (FR-HMA-103/104; FR-SMA-073)",
                )
                break

    # What is new — add capability rows if table allows
    what_new = doc.tables[33]
    add_fr_row(
        what_new,
        [
            "13",
            "Certified copy cross-references",
            "Multiple cross-references on certified copy of registered marriage "
            "document (FR-HMA-100)",
        ],
    )
    add_fr_row(
        what_new,
        [
            "14",
            "e-Governance address & certificate language",
            "Address capture per e-Governance standard; citizen selects "
            "certificate language with preview before confirm",
        ],
    )
    add_fr_row(
        what_new,
        [
            "15",
            "Age-proof integrations & SR Refusal",
            "e-Janma and Marks Card pull for Birth Certificate / age proof; "
            "SR Refusal with reason and order before registration/solemnization; "
            "Form II removed for Hindu Marriage",
        ],
    )


# ---------------------------------------------------------------------------
# Document control
# ---------------------------------------------------------------------------
def update_document_control(doc: Document) -> None:
    ctrl = doc.tables[0]
    set_cell_text(ctrl.rows[2].cells[1], OUT_VERSION)
    set_cell_text(
        ctrl.rows[3].cells[1],
        "Final — workshop additions: SMA Sec. 15/16 residence gate; notification "
        "cross-links; certified-copy cross-refs; e-Gov address; certificate "
        "language preview; Form II removed; e-Janma/Marks Card; SR Refusal order",
    )
    set_cell_text(ctrl.rows[11].cells[1], OUT_DATE)

    hist = doc.tables[1]
    # Avoid duplicate version row if re-run
    if hist.rows[-1].cells[0].text.strip() != OUT_VERSION:
        add_version_row(
            hist,
            [
                OUT_VERSION,
                OUT_DATE,
                "Nandha Kumar",
                CHANGE_SUMMARY,
                "Prashanth",
            ],
        )


def main() -> None:
    if not SRC.exists():
        raise FileNotFoundError(SRC)
    shutil.copy2(SRC, DST)
    doc = Document(str(DST))

    update_document_control(doc)
    update_sma_sec_15_16(doc)
    crosslink_notifications(doc)
    remove_form_ii(doc)
    add_new_requirements(doc)

    doc.save(str(DST))

    # Verification
    doc2 = Document(str(DST))
    checks = {
        "Sec15 residence phrase": "30 days before the date of notice application"
        in doc2.tables[4].rows[9].cells[2].text,
        "Sec16 residence phrase": "30 days before the date of notice application"
        in doc2.tables[4].rows[10].cells[2].text,
        "Form II removed from mapping": not any(
            r.cells[0].text.strip() == "Form II" for r in doc2.tables[10].rows
        ),
        "FR-HMA-100": any(
            r.cells[0].text.strip() == "FR-HMA-100" for r in doc2.tables[75].rows
        ),
        "FR-HMA-103 refusal": any(
            r.cells[0].text.strip() == "FR-HMA-103" for r in doc2.tables[46].rows
        ),
        "e-Janma integration": any(
            "e-Janma" in r.cells[0].text for r in doc2.tables[83].rows
        ),
        "FR-HMA-037 language preview": "preview" in find_row_by_col0(
            doc2.tables[76], "FR-HMA-037"
        ).cells[1].text.lower(),
        "HMA Act has notification cross-link": "S.O. 4896"
        in find_row_by_col0(doc2.tables[2], "The Hindu Marriage Act, 1955").cells[1].text,
    }
    print(f"Wrote {DST.name}")
    for k, ok in checks.items():
        print(f"  [{'OK' if ok else 'FAIL'}] {k}")
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
