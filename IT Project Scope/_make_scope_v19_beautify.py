# -*- coding: utf-8 -*-
"""Beautify IT_Project_Scope_Document_v1.8 → v1.9.

- Clean broken icon characters and NBSP on headings
- Apply proper heading styles and document title
- Professional table formatting (header band, borders, widths, fonts)
- Tighten cell paragraph spacing; bold integration names in IS-11
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Twips

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"E:\MVP\Kaveri 3.0\Source Code\Kaveri 3 Plan")
SCOPE_DIR = ROOT / "IT Project Scope"
SRC = SCOPE_DIR / "IT_Project_Scope_Document_v1.8.docx"
OUT = SCOPE_DIR / "IT_Project_Scope_Document_v1.9.docx"
CSG_OUT = ROOT / "CSG Documents" / "IT Project Scope" / "IT_Project_Scope_Document_v1.9.docx"

NAVY = "1F4E79"
NAVY_RGB = RGBColor(0x1F, 0x4E, 0x79)
ALT_ROW = "F2F6FA"
WHITE = "FFFFFF"
BORDER = "8FA3B8"
BODY_RGB = RGBColor(0x24, 0x24, 0x24)


def set_run_font(run, *, name="Calibri", size_pt=10, bold=None, color=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size_pt)
    if bold is not None:
        run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color


def set_cell_shading(cell, fill_hex: str) -> None:
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = tcPr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tcPr.append(shd)
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)


def set_cell_borders(cell, color_hex: str = BORDER, sz: str = "4") -> None:
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn("w:tcBorders"))
    if tcBorders is None:
        tcBorders = OxmlElement("w:tcBorders")
        tcPr.append(tcBorders)
    for edge in ("top", "left", "bottom", "right"):
        el = tcBorders.find(qn(f"w:{edge}"))
        if el is None:
            el = OxmlElement(f"w:{edge}")
            tcBorders.append(el)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), sz)
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color_hex)


def set_cell_margins(cell, top=40, bottom=40, left=60, right=60) -> None:
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.find(qn("w:tcMar"))
    if tcMar is None:
        tcMar = OxmlElement("w:tcMar")
        tcPr.append(tcMar)
    for edge, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = tcMar.find(qn(f"w:{edge}"))
        if el is None:
            el = OxmlElement(f"w:{edge}")
            tcMar.append(el)
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")


def set_row_repeat_header(row) -> None:
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    tblHeader = trPr.find(qn("w:tblHeader"))
    if tblHeader is None:
        tblHeader = OxmlElement("w:tblHeader")
        trPr.append(tblHeader)


def set_table_fixed_layout(table) -> None:
    tbl = table._tbl
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement("w:tblPr")
        tbl.insert(0, tblPr)
    layout = tblPr.find(qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tblPr.append(layout)
    layout.set(qn("w:type"), "fixed")


def set_col_widths(table, widths_cm: list[float]) -> None:
    """Set preferred widths on every cell in each column."""
    for row in table.rows:
        for i, w_cm in enumerate(widths_cm):
            if i >= len(row.cells):
                continue
            cell = row.cells[i]
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcW = tcPr.find(qn("w:tcW"))
            if tcW is None:
                tcW = OxmlElement("w:tcW")
                tcPr.append(tcW)
            # 1 cm ≈ 567 twips
            tcW.set(qn("w:w"), str(int(w_cm * 567)))
            tcW.set(qn("w:type"), "dxa")


def clear_paragraph(para) -> None:
    for r in list(para.runs):
        r._element.getparent().remove(r._element)
    para.text = ""


def format_para(para, *, size_pt=10, bold=False, color=BODY_RGB, space_after=2, space_before=0):
    pf = para.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    if not para.runs:
        run = para.add_run(para.text)
        clear_paragraph(para)
        # restore via new run below after we get text - actually text already cleared
        return
    for run in para.runs:
        set_run_font(run, size_pt=size_pt, bold=bold, color=color)


def rewrite_cell_plain(cell, text: str, *, bold=False, size_pt=10, center=False) -> None:
    # Clear all paragraphs except first
    for p in cell.paragraphs[1:]:
        p._element.getparent().remove(p._element)
    para = cell.paragraphs[0]
    clear_paragraph(para)
    para.paragraph_format.space_before = Pt(0)
    para.paragraph_format.space_after = Pt(0)
    para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    if center:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = para.add_run(text)
    set_run_font(run, size_pt=size_pt, bold=bold, color=BODY_RGB)


def rewrite_cell_multiline(cell, lines: list[str], *, size_pt=9) -> None:
    """Write lines; blank line = spacer; 'Name — desc' gets bold name."""
    for p in cell.paragraphs[1:]:
        p._element.getparent().remove(p._element)
    first = cell.paragraphs[0]
    clear_paragraph(first)

    def style_para(para, space_after=3):
        para.paragraph_format.space_before = Pt(0)
        para.paragraph_format.space_after = Pt(space_after)
        para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT

    if not lines:
        style_para(first, 0)
        return

    for idx, line in enumerate(lines):
        para = first if idx == 0 else cell.add_paragraph()
        style_para(para, space_after=2 if line.strip() else 4)
        clear_paragraph(para)

        if not line.strip():
            continue

        # Bold label before em-dash / en-dash / " – "
        m = re.match(r"^(.*?)(\s+[—–-]\s+)(.*)$", line)
        if m and len(m.group(1)) < 80:
            r1 = para.add_run(m.group(1))
            set_run_font(r1, size_pt=size_pt, bold=True, color=NAVY_RGB)
            r2 = para.add_run(m.group(2) + m.group(3))
            set_run_font(r2, size_pt=size_pt, bold=False, color=BODY_RGB)
        elif line.endswith(":") or (
            len(line) < 60
            and not line.startswith("Boundary")
            and not line.startswith("P.S.")
            and not line.startswith("Source:")
            and idx == 0
        ):
            # Short lead-in / section label
            r = para.add_run(line)
            set_run_font(r, size_pt=size_pt, bold=True, color=BODY_RGB)
        else:
            r = para.add_run(line)
            set_run_font(r, size_pt=size_pt, bold=False, color=BODY_RGB)


def style_header_cell(cell, text: str) -> None:
    set_cell_shading(cell, NAVY)
    set_cell_borders(cell, color_hex="163A5F", sz="6")
    set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    for p in cell.paragraphs[1:]:
        p._element.getparent().remove(p._element)
    para = cell.paragraphs[0]
    clear_paragraph(para)
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(2)
    para.paragraph_format.space_after = Pt(2)
    run = para.add_run(text)
    set_run_font(run, size_pt=10, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))


def style_body_cell(cell, *, alt: bool = False, center: bool = False) -> None:
    set_cell_shading(cell, ALT_ROW if alt else WHITE)
    set_cell_borders(cell)
    set_cell_margins(cell)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
    for para in cell.paragraphs:
        para.paragraph_format.space_before = Pt(0)
        para.paragraph_format.space_after = Pt(2)
        para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        if center:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            if run.font.size is None:
                set_run_font(run, size_pt=9, color=BODY_RGB)
            else:
                # keep existing size but normalize name/color
                set_run_font(
                    run,
                    size_pt=run.font.size.pt,
                    bold=run.font.bold,
                    color=run.font.color.rgb if run.font.color and run.font.color.type else BODY_RGB,
                )


def clean_headings(doc: Document) -> None:
    """Remove PUA icons; normalize section titles."""
    # Collect paragraphs to clear / rewrite
    for para in doc.paragraphs:
        text = para.text.replace("\xa0", " ").strip()
        # Remove private-use / icon junk
        if text == "\ue113" or (len(text) == 1 and ord(text) >= 0xE000):
            clear_paragraph(para)
            para.paragraph_format.space_before = Pt(0)
            para.paragraph_format.space_after = Pt(0)
            continue
        if text == "In Scope":
            clear_paragraph(para)
            run = para.add_run("1. In Scope")
            set_run_font(run, size_pt=16, bold=True, color=NAVY_RGB)
            para.paragraph_format.space_before = Pt(0)
            para.paragraph_format.space_after = Pt(8)
            continue
        if text.startswith("8.1") and "Stakeholder" in text:
            clear_paragraph(para)
            run = para.add_run("2. Key Stakeholders")
            set_run_font(run, size_pt=16, bold=True, color=NAVY_RGB)
            para.paragraph_format.space_before = Pt(16)
            para.paragraph_format.space_after = Pt(8)
            continue


def insert_title_block(doc: Document) -> None:
    """Insert a title block at the top if not already present."""
    first = doc.paragraphs[0].text.replace("\xa0", " ").strip() if doc.paragraphs else ""
    if first.startswith("Kaveri 3.0"):
        return
    # Insert before first paragraph
    p0 = doc.paragraphs[0]._element
    parent = p0.getparent()

    def make_para(text, *, size, bold, color, space_after, align=WD_ALIGN_PARAGRAPH.LEFT):
        from docx.text.paragraph import Paragraph

        new_p = OxmlElement("w:p")
        parent.insert(list(parent).index(p0), new_p)
        para = Paragraph(new_p, doc.paragraphs[0]._parent)
        para.alignment = align
        para.paragraph_format.space_before = Pt(0)
        para.paragraph_format.space_after = Pt(space_after)
        run = para.add_run(text)
        set_run_font(run, size_pt=size, bold=bold, color=color)
        return para

    make_para(
        "Kaveri 3.0 — IT Project Scope",
        size=20,
        bold=True,
        color=NAVY_RGB,
        space_after=2,
    )
    make_para(
        "Department of Stamps and Registration (DSR), Government of Karnataka",
        size=11,
        bold=False,
        color=BODY_RGB,
        space_after=2,
    )
    make_para(
        "Document version 1.9  ·  In Scope & Key Stakeholders",
        size=9,
        bold=False,
        color=RGBColor(0x5A, 0x6A, 0x7A),
        space_after=12,
    )


def beautify_scope_table(table) -> None:
    set_table_fixed_layout(table)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # A4 usable ~16.5 cm with 1.8cm margins
    set_col_widths(table, [2.0, 3.6, 10.9])

    headers = [c.text.strip() for c in table.rows[0].cells]
    for cell, text in zip(table.rows[0].cells, headers):
        style_header_cell(cell, text)
    set_row_repeat_header(table.rows[0])

    for ri, row in enumerate(table.rows[1:], start=1):
        alt = ri % 2 == 0
        # Capture existing lines before restyle
        id_text = row.cells[0].text.strip()
        item_text = row.cells[1].text.strip()
        desc_lines = [p.text for p in row.cells[2].paragraphs]

        rewrite_cell_plain(row.cells[0], id_text, bold=True, size_pt=9, center=True)
        rewrite_cell_plain(row.cells[1], item_text, bold=True, size_pt=9)
        rewrite_cell_multiline(row.cells[2], desc_lines, size_pt=9)

        for ci, cell in enumerate(row.cells):
            style_body_cell(cell, alt=alt, center=(ci == 0))
            if ci == 0:
                for para in cell.paragraphs:
                    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in cell.paragraphs[0].runs:
                    set_run_font(run, size_pt=9, bold=True, color=NAVY_RGB)
            if ci == 1:
                for run in cell.paragraphs[0].runs:
                    set_run_font(run, size_pt=9, bold=True, color=BODY_RGB)


def beautify_stakeholders_table(table) -> None:
    set_table_fixed_layout(table)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_col_widths(table, [3.6, 3.2, 3.4, 3.2, 3.1])

    headers = [c.text.strip() for c in table.rows[0].cells]
    for cell, text in zip(table.rows[0].cells, headers):
        style_header_cell(cell, text)
    set_row_repeat_header(table.rows[0])

    for ri, row in enumerate(table.rows[1:], start=1):
        alt = ri % 2 == 0
        values = [c.text.strip() for c in row.cells]
        for ci, (cell, text) in enumerate(zip(row.cells, values)):
            rewrite_cell_plain(cell, text, bold=(ci == 0), size_pt=8)
            style_body_cell(cell, alt=alt)
            if ci == 0:
                for run in cell.paragraphs[0].runs:
                    set_run_font(run, size_pt=8, bold=True, color=NAVY_RGB)


def set_page(doc: Document) -> None:
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.left_margin = Cm(1.8)
        section.right_margin = Cm(1.8)
        section.top_margin = Cm(1.6)
        section.bottom_margin = Cm(1.6)


def remove_empty_paras(doc: Document) -> None:
    """Collapse runs of empty paragraphs to at most one spacer."""
    body = doc.element.body
    paras = list(doc.paragraphs)
    empty_streak = 0
    to_remove = []
    for para in paras:
        text = para.text.replace("\xa0", "").replace("\ue113", "").strip()
        # Keep styled headings even if somehow empty
        style_name = para.style.name if para.style else ""
        if text == "" and not style_name.startswith("Heading"):
            empty_streak += 1
            if empty_streak > 1:
                to_remove.append(para._element)
        else:
            empty_streak = 0
    for el in to_remove:
        parent = el.getparent()
        if parent is not None:
            parent.remove(el)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Source not found: {SRC}")

    shutil.copy2(SRC, OUT)
    doc = Document(str(OUT))

    set_page(doc)
    insert_title_block(doc)
    clean_headings(doc)
    remove_empty_paras(doc)

    if len(doc.tables) < 2:
        raise SystemExit("Expected In Scope + Stakeholders tables")

    beautify_scope_table(doc.tables[0])
    beautify_stakeholders_table(doc.tables[1])

    doc.save(str(OUT))

    CSG_OUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy2(OUT, CSG_OUT)
        csg_msg = f"Copied: {CSG_OUT}"
    except PermissionError:
        csg_msg = f"Skipped CSG copy (locked): {CSG_OUT}"

    # Quick verify
    v = Document(str(OUT))
    print(f"Created: {OUT}")
    print(csg_msg)
    print("Paragraphs:")
    for i, para in enumerate(v.paragraphs[:8]):
        t = para.text.strip()
        if t:
            print(f"  [{i}] {t[:80]}")
    print(f"Tables: {len(v.tables)} ({len(v.tables[0].rows)} scope rows, {len(v.tables[1].rows)} stakeholder rows)")
    print("Sample IS-11 first lines:")
    for row in v.tables[0].rows:
        if row.cells[0].text.strip() == "IS-11":
            for line in row.cells[2].text.splitlines()[:6]:
                print(f"  {line}")
            break


if __name__ == "__main__":
    main()
