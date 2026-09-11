# -*- coding: utf-8 -*-
"""Italicize notification citations in Marriage BRD v8 Acts / Rules / Sections.

Targets §3.1 Applicable Acts, §3.2 Relevant sections, §3.3 Relevant rules
(tables 2–8). Citation trailers appended in v8 (and native instrument refs in
those cells) are set in italic; surrounding requirement text stays roman.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from docx import Document
from docx.table import _Cell
from docx.text.paragraph import Paragraph

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(r"E:\MVP\Kaveri 3.0\Source Code\Kaveri 3 Plan\Finalized BRD\Marriage\RFP")
DOC_PATH = BASE / "BRD_Marriage_BRD_v8.docx"
TMP_PATH = BASE / "BRD_Marriage_BRD_v8._italic_tmp.docx"

# Where an appended / inline notification citation typically begins in a cell.
# Longest / most specific first.
CITATION_STARTERS: tuple[str, ...] = (
    "Notifications:",
    "Notification / rules:",
    "Made under Notification",
    "Aligned with Notification",
    "Procedure under Special Marriage (Karnataka) Rules, 1961 (Notification",
    "Notification No.",
    "Age proof per circular",
    "Age / eligibility evidence per",
    "Age proof per koE",
    "Address proof documents per",
    "Instrument: S.O.",
    "S.O. 4896 (Sub-Registrars",
    "G.S.R. 314",
    "Amendment Rules, 1999",
    "RD/48/MNMU/2023",
)

# Trailing citation must include a §3.4 (or plain 3.4) marker from the v8 append.
CITE_END = re.compile(r"(?:see\s+)?§?3\.4(?:\s*/\s*§?3\.5)?\s*$")


def clear_paragraph(paragraph: Paragraph) -> None:
    p = paragraph._p
    for child in list(p):
        if child.tag.endswith("}r") or child.tag.endswith("}hyperlink"):
            p.remove(child)


def set_runs(paragraph: Paragraph, spans: list[tuple[str, bool]]) -> None:
    """Replace paragraph content with (text, italic) spans; keep paragraph style."""
    clear_paragraph(paragraph)
    for text, italic in spans:
        if not text:
            continue
        run = paragraph.add_run(text)
        run.italic = italic


def set_cell_spans(cell: _Cell, spans: list[tuple[str, bool]]) -> None:
    paras = cell.paragraphs
    if not paras:
        cell.add_paragraph("")
        paras = cell.paragraphs
    set_runs(paras[0], spans)
    for p in paras[1:]:
        clear_paragraph(p)


def find_citation_start(text: str) -> int | None:
    """Return index where the notification citation trailer begins, else None."""
    if not CITE_END.search(text):
        return None

    candidates: list[int] = []
    for starter in CITATION_STARTERS:
        idx = text.find(starter)
        if idx == -1:
            continue
        # Prefer a starter that sits after a "; " separator when present
        if idx > 0:
            before = text[:idx].rstrip()
            if before.endswith(";") or before.endswith("."):
                # include the separating "; " / ". " in the roman part
                sep_start = len(before)
                # skip trailing spaces after separator for roman end
                while sep_start < idx and text[sep_start] in " \t":
                    sep_start += 1
                candidates.append(sep_start if sep_start == idx else idx)
            else:
                candidates.append(idx)
        else:
            candidates.append(0)

    if not candidates:
        return None
    return min(candidates)


def italicize_rule_label_so(cell: _Cell) -> bool:
    """Italicize S.O. 4896 inside 'Rule 3(1) + S.O. 4896'."""
    text = cell.text
    marker = "S.O. 4896"
    if marker not in text:
        return False
    i = text.index(marker)
    spans = [(text[:i], False), (marker, True), (text[i + len(marker) :], False)]
    set_cell_spans(cell, spans)
    return True


def restore_section_mark(cite: str) -> str:
    """Ensure § appears before 3.4 / 3.5 markers in citation trailers."""
    cite = re.sub(r"see\s+3\.4\b", "see §3.4", cite)
    cite = re.sub(r"—\s*3\.4\b", "— §3.4", cite)
    cite = re.sub(r"/\s*3\.5\b", "/ §3.5", cite)
    cite = re.sub(r"§§", "§", cite)
    return cite


def italicize_cell_citation(cell: _Cell) -> bool:
    text = cell.text
    # Normalize NBSP
    text = text.replace("\xa0", " ")
    start = find_citation_start(text)
    if start is None:
        return False
    # Keep a leading "; " / ". " in the roman body when citation starts mid-cell
    body = text[:start]
    cite = restore_section_mark(text[start:])
    if not cite.strip():
        return False
    spans: list[tuple[str, bool]] = []
    if body:
        spans.append((body, False))
    spans.append((cite, True))
    set_cell_spans(cell, spans)
    return True


def main() -> None:
    doc = Document(str(DOC_PATH))
    changed = 0

    # Tables 2–8: Acts, HMA/SMA/PMA sections, HMA/SMA/PMA rules
    for ti in range(2, 9):
        table = doc.tables[ti]
        for ri, row in enumerate(table.rows):
            if ri == 0:
                continue  # header
            for ci, cell in enumerate(row.cells):
                # Rule label with embedded S.O.
                if ti == 6 and ci == 0 and "S.O. 4896" in cell.text:
                    if italicize_rule_label_so(cell):
                        changed += 1
                    continue
                if italicize_cell_citation(cell):
                    changed += 1

    doc.save(str(TMP_PATH))

    # Prefer overwriting v8; fall back to keeping the temp if Word has a lock
    saved_as = TMP_PATH
    try:
        # Replace locked target via os.replace when possible
        import os
        import shutil

        try:
            os.replace(str(TMP_PATH), str(DOC_PATH))
            saved_as = DOC_PATH
        except PermissionError:
            shutil.copy2(str(TMP_PATH), str(DOC_PATH))
            TMP_PATH.unlink(missing_ok=True)
            saved_as = DOC_PATH
    except PermissionError:
        print(
            f"WARNING: {DOC_PATH.name} is locked (close Word). "
            f"Italicized copy saved as {TMP_PATH.name}"
        )

    # Verify from whatever path we could write
    doc2 = Document(str(saved_as))
    italic_cells = 0
    samples: list[str] = []
    for ti in range(2, 9):
        for row in doc2.tables[ti].rows[1:]:
            for cell in row.cells:
                has_italic = any(
                    bool(r.italic) and r.text.strip()
                    for p in cell.paragraphs
                    for r in p.runs
                )
                if has_italic:
                    italic_cells += 1
                    if len(samples) < 6:
                        ital = "".join(
                            r.text
                            for p in cell.paragraphs
                            for r in p.runs
                            if r.italic and r.text
                        )
                        samples.append(f"T{ti}: …{ital[:110]}")

    print(f"Updated {saved_as.name}: {changed} cells rewritten")
    print(f"Verify: {italic_cells} cells contain italic runs")
    for s in samples:
        print(f"  {s}")


if __name__ == "__main__":
    main()
