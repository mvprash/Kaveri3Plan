# -*- coding: utf-8 -*-
"""BRD Marriage v4 → v7: update ONLY §3 Implementation column + §6 Addressed-in column.

Does NOT change heading / outline numbering (keeps 3.i, 3.ii … / 7.i, 7.ii …).
"""
from __future__ import annotations

import re
import shutil
import sys
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.table import _Cell
from docx.text.paragraph import Paragraph

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(r"E:\MVP\Kaveri 3.0\Source Code\Kaveri 3 Plan\Finalized BRD\Marriage\RFP")
SRC = BASE / "BRD_Marriage_BRD_v4.docx"
DST = BASE / "BRD_Marriage_BRD_v7.docx"

# §3 Implementation column — keep roman 7.i.* ; only fix broken / stale tokens
IMPL_REPLACEMENTS: list[tuple[str, str]] = [
    ("7.b.x Hindu Marriage Online and Offline", "7.i.b Hindu Marriage Online and Offline"),
    ("7.b.x", "7.i.b"),
    # Old FRS/back-office decimals that appear inside §3 Implementation notes
    ("8.6 back-office", "8.vii / back-office"),
    ("8.6 MIS / search", "8.vii MIS / search"),
    ("3.viii; 8.7 (GSC acknowledgement and lifecycle — no separate 7 process)",
     "3.viii; 8.viii (GSC acknowledgement and lifecycle — no separate 7 process)"),
]

# §6 Addressed-in cells: keep BRD 7.i… cites; retarget companion-FRS crumbs to this BRD
# Apply longest tokens first.
PAIN_REPLACEMENTS: list[tuple[str, str]] = [
    ("Addressed in (BRD / FRS·NFR)", "Addressed in (this BRD)"),
    ("FRS/NFRS: 10 UI; 15.4 NFR-MRG-VAPT-002", "8.xi UI; 9.iv NFR-MRG-VAPT-002"),
    ("FRS/NFRS: 8.1.3–8.1.5", "8.i.c–8.i.e"),
    ("FRS/NFRS: 8.1.4–8.1.5", "8.i.d–8.i.e"),
    ("FRS/NFRS: 8.2.5–8.2.7", "8.ii.e–8.ii.g"),
    ("FRS/NFRS: 8.1.16", "8.i.p"),
    ("FRS/NFRS: 8.1.15", "8.i.o"),
    ("FRS/NFRS: 8.1.14", "8.i.n"),
    ("FRS/NFRS: 8.1.13", "8.i.m"),
    ("FRS/NFRS: 8.1.11", "8.i.k"),
    ("FRS/NFRS: 8.1.10", "8.i.j"),
    ("FRS/NFRS: 8.1.9", "8.i.i"),
    ("FRS/NFRS: 8.1.6", "8.i.f"),
    ("FRS/NFRS: 8.1.3", "8.i.c"),
    ("FRS/NFRS: 8.1.2", "8.i.b"),
    ("FRS/NFRS: 8.2.8", "8.ii.h"),
    ("FRS/NFRS: 17 FB-MRG-003", "11 FB-MRG-003"),
    ("FRS/NFRS: 8.5", "8.vi"),
    ("FRS/NFRS: 8.6", "8.vii"),
    ("FRS/NFRS: 8.4", "8.v"),
    # Bare old-FRS decimals left beside FR-IDs in the same cell
    ("8.1.16 FR-HMA", "8.i.p FR-HMA"),
    ("8.1.9 FR-HMA", "8.i.i FR-HMA"),
    ("8.1.3; 8.2.2", "8.i.c; 8.ii.b"),
    ("8.1.4–8.1.5; 8.2.3", "8.i.d–8.i.e; 8.ii.c"),
    ("8.3.iii", "8.iii.c"),
    ("8.6 FR-HMA-042", "8.vii FR-HMA-042"),
    ("15.4 NFR-MRG-VAPT-002", "9.iv NFR-MRG-VAPT-002"),
    ("11 Integrations (MDM / address master)", "8.xii Integrations (MDM / address master)"),
    ("12.1 Core entities", "8.xiii.a Core entities"),
    ("16 RS-MRG-003", "10 RS-MRG-003"),
    ("17 FB-MRG-001", "11 FB-MRG-001"),
    ("FRS/NFRS: ", ""),
]

PAIN_INTRO_OLD = (
    "Pain points evidenced from Kaveri 2.0 workshops, ServiceDesk tickets and department discussions. "
    "The Addressed in column maps each item to the To-Be process in this BRD (7) and to functional / "
    "non-functional requirements, fallbacks and risks in the companion FRS and NFRs document "
    "(FRS_and_NFRS_Marriage_v1.22.docx — 8–18)."
)
PAIN_INTRO_NEW = (
    "Pain points evidenced from Kaveri 2.0 workshops, ServiceDesk tickets and department discussions. "
    "The Addressed in column maps each item to the To-Be process in this BRD (§7) and to functional / "
    "non-functional requirements, fallbacks and risks in this document (§§8–11)."
)

WHAT_IS_NEW_OLD_SNIPPET = "FRS_and_NFRS_Marriage_v1.22.docx"
WHAT_IS_NEW_REPLACEMENTS: list[tuple[str, str]] = [
    (
        "Cross-references point to To-Be process in this BRD (7.i–7.v) and to functional / non-functional "
        "requirements in FRS_and_NFRS_Marriage_v1.22.docx.",
        "Cross-references point to To-Be process in this BRD (7.i–7.v) and to functional / non-functional "
        "requirements in §§8–9 of this document.",
    ),
]


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


def add_version_row(table, values: list[str]) -> None:
    table._tbl.append(deepcopy(table.rows[-1]._tr))
    row = table.rows[-1]
    for ci, val in enumerate(values):
        if ci < len(row.cells):
            set_cell_text(row.cells[ci], val)


def apply_map(text: str, pairs: list[tuple[str, str]]) -> str:
    out = text
    for old, new in pairs:
        out = out.replace(old, new)
    return out


def rewrite_impl_cell(text: str) -> str:
    return apply_map(text, IMPL_REPLACEMENTS)


def rewrite_pain_cell(text: str) -> str:
    return apply_map(text, PAIN_REPLACEMENTS)


def is_impl_header_table(table) -> bool:
    if not table.rows:
        return False
    return any("Refer section 7" in c.text for c in table.rows[0].cells)


def is_pain_table(table) -> bool:
    if not table.rows:
        return False
    return any("Addressed in" in c.text for c in table.rows[0].cells)


def update_section3_impl_columns(doc: Document) -> int:
    n = 0
    for table in doc.tables:
        if not is_impl_header_table(table):
            continue
        # last column = Implementation
        for row in table.rows:
            cell = row.cells[-1]
            old = cell.text
            new = rewrite_impl_cell(old)
            if new != old:
                # preserve multi-para if present
                if len(cell.paragraphs) == 1:
                    set_para_text(cell.paragraphs[0], new)
                else:
                    parts = new.split("\n")
                    if len(parts) == len(cell.paragraphs):
                        for para, part in zip(cell.paragraphs, parts):
                            set_para_text(para, part)
                    else:
                        set_cell_text(cell, new)
                n += 1
    return n


def update_section6_addressed_column(doc: Document) -> int:
    n = 0
    # Intro paragraph under As-Is pain points
    for p in doc.paragraphs:
        if "Pain points evidenced" in p.text and "Addressed in column" in p.text:
            if p.text.strip() == PAIN_INTRO_OLD or "FRS_and_NFRS_Marriage_v1.22" in p.text:
                set_para_text(p, PAIN_INTRO_NEW)
                n += 1
            break

    # Related blurb under 7.vi that still points at companion FRS for the same mapping
    for p in doc.paragraphs:
        if WHAT_IS_NEW_OLD_SNIPPET in p.text:
            new = apply_map(p.text, WHAT_IS_NEW_REPLACEMENTS)
            if new != p.text:
                set_para_text(p, new)
                n += 1

    for table in doc.tables:
        if not is_pain_table(table):
            continue
        for row in table.rows:
            cell = row.cells[-1]
            old = cell.text
            new = rewrite_pain_cell(old)
            if new != old:
                if len(cell.paragraphs) == 1:
                    set_para_text(cell.paragraphs[0], new)
                else:
                    parts = new.split("\n")
                    if len(parts) == len(cell.paragraphs):
                        for para, part in zip(cell.paragraphs, parts):
                            set_para_text(para, part)
                    else:
                        set_cell_text(cell, new)
                n += 1
    return n


def update_document_control(doc: Document) -> None:
    ctrl = doc.tables[0]
    set_cell_text(ctrl.rows[2].cells[1], "7")
    set_cell_text(
        ctrl.rows[3].cells[1],
        "Final — §3 Implementation column & §6 Addressed-in column updated (outline numbering unchanged)",
    )
    for row in ctrl.rows:
        if row.cells[0].text.strip().lower().startswith("last updated"):
            set_cell_text(row.cells[1], "09-09-2026")
            break
    hist = doc.tables[1]
    if hist.rows[-1].cells[0].text.strip() != "7":
        add_version_row(
            hist,
            [
                "7",
                "09-09-2026",
                "Nandha Kumar",
                "§3: updated 'Refer section 7 for Implementation' column values; "
                "§6: renamed 'Addressed in (BRD / FRS·NFR)' to 'Addressed in (this BRD)' and "
                "retargeted companion-FRS cites into this document. Outline (3.i / 7.i) unchanged.",
                "Prashanth",
            ],
        )


def verify(doc: Document) -> None:
    # Outline headings still without our decimal rewrite artifacts on Legal children titles
    legal_h3 = [
        p.text.strip()
        for p in doc.paragraphs
        if p.style and p.style.name == "Heading 3"
        and p.text.strip()
        in {
            "Applicable Acts",
            "Relevant sections followed by the Department for Marriage Registration",
            "As-Is pain points",
        }
    ]
    assert "Applicable Acts" in legal_h3

    # §3 still uses roman-style cites (not decimal 7.1.2.1)
    impl_blob = []
    for table in doc.tables:
        if is_impl_header_table(table):
            for row in table.rows[1:]:
                impl_blob.append(row.cells[-1].text)
    joined = "\n".join(impl_blob)
    assert "7.i.b.A" in joined, "Expected roman 7.i.b.A cites preserved in §3"
    assert "7.1.2.1" not in joined, "Must not convert §3 Implementation to decimal 7.1.2.1"
    assert "7.b.x" not in joined, "Broken 7.b.x should be fixed"

    # §6 column renamed
    pain = next(t for t in doc.tables if is_pain_table(t))
    hdr = pain.rows[0].cells[-1].text.strip()
    assert hdr == "Addressed in (this BRD)", hdr
    assert "FRS·NFR" not in hdr
    row1 = pain.rows[1].cells[-1].text
    assert "FRS/NFRS:" not in row1
    assert "7.vi" in row1 or "7.i.a" in row1, row1  # roman To-Be cites kept
    assert "FRS_and_NFRS_Marriage_v1.22" not in "\n".join(p.text for p in doc.paragraphs)

    print("Verification OK")
    print(f"  §3 sample: {doc.tables[3].rows[1].cells[-1].text.strip()}")
    print(f"  §6 header: {hdr}")
    print(f"  §6 row1:   {row1[:130]}")


def main() -> None:
    if not SRC.exists():
        raise FileNotFoundError(SRC)
    shutil.copy2(SRC, DST)
    doc = Document(str(DST))

    n3 = update_section3_impl_columns(doc)
    n6 = update_section6_addressed_column(doc)
    update_document_control(doc)
    doc.save(str(DST))

    out = Document(str(DST))
    print(f"Wrote {DST}")
    print(f"  §3 Implementation cells touched: {n3}")
    print(f"  §6 Addressed-in cells/intro touched: {n6}")
    print(f"  Version: {out.tables[0].rows[2].cells[1].text.strip()}")
    verify(out)


if __name__ == "__main__":
    main()
