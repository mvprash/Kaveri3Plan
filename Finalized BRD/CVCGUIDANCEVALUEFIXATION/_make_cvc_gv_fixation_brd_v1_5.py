# -*- coding: utf-8 -*-
"""Create BRD_CVC_Guidance_Value_Fixation_v1.5.docx from v1.4.

Adds valuation-area requirements:
  - extent in square metres
  - geo-coordinates / geo-fence mapping
  - Non-Agri & Agriculture rates (configurable masters)
  - Agriculture: Dry, Wet, Bhagayat (configurable)
  - Non-Agri: Residential, Commercial, Industrial (configurable)
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from docx import Document
from docx.shared import Pt

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(r"E:\MVP\Kaveri 3.0\Source Code\Kaveri 3 Plan\Finalized BRD\CVCGUIDANCEVALUEFIXATION")
SRC = BASE / "BRD_CVC_Guidance_Value_Fixation_v1.4.docx"
DST = BASE / "BRD_CVC_Guidance_Value_Fixation_v1.5.docx"
OUT_VERSION = "1.5"
OUT_DATE = "22-09-2026"

NEW_FRS = [
    (
        "FR-CVC-008",
        "For each valuation area, the system shall capture the area / extent in "
        "square metres (m²). The unit of measure for extent shall be square metres "
        "as the system standard (display conversion to other units may be provided "
        "without changing the stored m² value).",
        "Must",
    ),
    (
        "FR-CVC-009",
        "For each valuation area, the system shall capture and map the "
        "geo-coordinates of the area (geo-fence / polygon). The geo-fence shall be "
        "stored against the valuation area master and usable for spatial "
        "identification, evidence overlay (e.g. KSRSAC) and rate application.",
        "Must",
    ),
    (
        "FR-CVC-010",
        "For each valuation area, the system shall capture Non-Agricultural and "
        "Agricultural guidance rates. Rate category types (Non-Agri / Agriculture) "
        "shall be driven by configurable masters maintained by authorised CVC / "
        "DIGR Admin.",
        "Must",
    ),
    (
        "FR-CVC-011",
        "Where the rate category is Agriculture, the system shall capture rates "
        "under Dry, Wet and Bhagayat (garden) classifications. These agricultural "
        "sub-types shall be configurable masters (codes, labels in English/Kannada, "
        "active flag) and shall not be hard-coded beyond the seeded default set.",
        "Must",
    ),
    (
        "FR-CVC-012",
        "Where the rate category is Non-Agricultural, the system shall capture rates "
        "under Residential, Commercial and Industrial classifications. These "
        "non-agricultural sub-types shall be configurable masters (codes, labels in "
        "English/Kannada, active flag) and shall not be hard-coded beyond the seeded "
        "default set.",
        "Must",
    ),
]


def set_cell_text(cell, text: str, bold: bool = False, size: int = 9) -> None:
    cell.text = ""
    run = cell.paragraphs[0].add_run(text)
    run.bold = bold
    run.font.size = Pt(size)


def update_document_control_version(doc: Document) -> None:
    for table in doc.tables:
        if len(table.columns) != 2:
            continue
        keys = [r.cells[0].text.strip() for r in table.rows]
        if "Document ID" not in keys:
            continue
        for row in table.rows:
            key = row.cells[0].text.strip()
            if key == "Version":
                set_cell_text(row.cells[1], OUT_VERSION)
            if key == "Last updated":
                set_cell_text(row.cells[1], OUT_DATE)


def append_version_history_row(doc: Document) -> None:
    for table in doc.tables:
        if not table.rows:
            continue
        headers = [c.text.strip() for c in table.rows[0].cells]
        if headers[:3] != ["Version", "Date", "Author"]:
            continue
        for r in table.rows[1:]:
            if r.cells[0].text.strip() == OUT_VERSION:
                return
        row = table.add_row()
        values = [
            OUT_VERSION,
            OUT_DATE,
            "Nandha Kumar",
            "Added FR-CVC-008…012: valuation area extent (m²), geo-fence, "
            "Non-Agri/Agriculture rates with Dry/Wet/Bhagayat and "
            "Residential/Commercial/Industrial configurable masters; data entities updated",
            "Prashanth",
        ]
        for i, val in enumerate(values):
            if i < len(row.cells):
                set_cell_text(row.cells[i], val)
        return


def find_common_fr_table(doc: Document):
    for table in doc.tables:
        if not table.rows or table.rows[0].cells[0].text.strip() != "Req ID":
            continue
        ids = [r.cells[0].text.strip() for r in table.rows[1:]]
        if "FR-CVC-001" in ids and "FR-CVC-007" in ids:
            return table
    return None


def append_frs(doc: Document) -> None:
    table = find_common_fr_table(doc)
    if table is None:
        raise SystemExit("Common FR table not found")
    existing = {r.cells[0].text.strip() for r in table.rows[1:]}
    for req_id, text, priority in NEW_FRS:
        if req_id in existing:
            for r in table.rows[1:]:
                if r.cells[0].text.strip() == req_id:
                    set_cell_text(r.cells[1], text)
                    set_cell_text(r.cells[2], priority)
                    break
            continue
        row = table.add_row()
        set_cell_text(row.cells[0], req_id, bold=True)
        set_cell_text(row.cells[1], text)
        set_cell_text(row.cells[2], priority)


def update_data_entities(doc: Document) -> None:
    for table in doc.tables:
        if not table.rows:
            continue
        hdr = [c.text.strip() for c in table.rows[0].cells]
        if hdr[:2] != ["Entity", "Key attributes"]:
            continue
        entities = {r.cells[0].text.strip(): r for r in table.rows[1:]}

        def upsert(name: str, attrs: str) -> None:
            if name in entities:
                set_cell_text(entities[name].cells[1], attrs)
            else:
                row = table.add_row()
                set_cell_text(row.cells[0], name, bold=True)
                set_cell_text(row.cells[1], attrs)

        upsert(
            "ValuationArea",
            "area_id, name/code, jurisdiction keys, extent_sqm, geo_fence "
            "(polygon coordinates), status, effective dates",
        )
        upsert(
            "RateCategoryMaster",
            "category_code (Agriculture / Non-Agriculture), labels EN/KN, "
            "active flag — configurable",
        )
        upsert(
            "AgriSubTypeMaster",
            "subtype_code (Dry / Wet / Bhagayat), labels EN/KN, active flag — configurable",
        )
        upsert(
            "NonAgriSubTypeMaster",
            "subtype_code (Residential / Commercial / Industrial), labels EN/KN, "
            "active flag — configurable",
        )
        # Enrich proposed / published rate lines
        if "ProposedRateLine" in entities:
            set_cell_text(
                entities["ProposedRateLine"].cells[1],
                "line_id, proposal_id, valuation_area_id, rate_category "
                "(Agri/Non-Agri), sub_type (Dry/Wet/Bhagayat or "
                "Residential/Commercial/Industrial), proposed_rate, unit, "
                "extent_sqm_ref, remarks",
            )
        if "GuidanceRateVersion" in entities:
            set_cell_text(
                entities["GuidanceRateVersion"].cells[1],
                "rate_id, valuation_area_id, rate_category, sub_type, rate, unit, "
                "extent_sqm, geo_fence_ref, effective_from/to, source, version",
            )
        if "PublicNotice" in entities:
            # align with configurable period while touching entities
            attrs = entities["PublicNotice"].cells[1].text
            if "15 days" in attrs:
                set_cell_text(
                    entities["PublicNotice"].cells[1],
                    attrs.replace("end (15 days)", "end (configurable objections period)"),
                )
        return


def update_business_rules_if_present(doc: Document) -> None:
    """Append a short bullet under Business rules if a related para exists."""
    # Find Business rules heading, then look for list after it — insert by
    # appending a new bullet paragraph after the last list item before next heading.
    br_idx = None
    for i, p in enumerate(doc.paragraphs):
        if p.style.name.startswith("Heading") and p.text.strip() == "Business rules":
            br_idx = i
            break
    if br_idx is None:
        return

    # Find insertion point: last list paragraph before next heading
    insert_after = None
    for j in range(br_idx + 1, len(doc.paragraphs)):
        p = doc.paragraphs[j]
        if p.style.name.startswith("Heading"):
            break
        if p.style.name.startswith("List") or p.text.strip().startswith("BR-"):
            insert_after = p

    text = (
        "Each Valuation Area shall store extent in square metres and a geo-fence "
        "(polygon). Guidance rates on an area shall be captured under configurable "
        "Agriculture (Dry / Wet / Bhagayat) and Non-Agriculture (Residential / "
        "Commercial / Industrial) masters (FR-CVC-008…012)."
    )
    # Avoid duplicate
    for p in doc.paragraphs:
        if "FR-CVC-008" in p.text and "geo-fence" in p.text:
            return

    if insert_after is not None:
        new_p = insert_after.insert_paragraph_before(text)
        # insert_paragraph_before puts BEFORE; we want after — use addnext on XML
        # Actually python-docx insert_paragraph_before inserts before that para.
        # Better: clone style from insert_after and place after via XML.
        new_p.style = insert_after.style
        # Move new_p to after insert_after
        new_p._p.getparent().remove(new_p._p)
        insert_after._p.addnext(new_p._p)
    else:
        # fallback: insert before next heading after Business rules
        for j in range(br_idx + 1, len(doc.paragraphs)):
            if doc.paragraphs[j].style.name.startswith("Heading"):
                p = doc.paragraphs[j].insert_paragraph_before(text)
                p.style = "List Bullet"
                return


def update_rtm(doc: Document) -> None:
    for table in doc.tables:
        if not table.rows:
            continue
        hdr = [c.text.strip() for c in table.rows[0].cells]
        if not hdr or hdr[0] not in ("Req ID", "Req ID / FR"):
            # RTM may use "Req ID" with Legal anchor
            pass
        for row in table.rows[1:]:
            cell0 = row.cells[0].text.strip()
            # Add a row for new common FRs if table looks like RTM
            if len(row.cells) >= 4 and cell0 == "FR-CVC-003":
                # insert companion row after common entries if 008 not present
                ids = [r.cells[0].text.strip() for r in table.rows[1:]]
                if any("FR-CVC-008" in x for x in ids):
                    return
                new_row = table.add_row()
                vals = [
                    "FR-CVC-008…012",
                    "Sec. 45-B / Rule 6 methodology",
                    "Valuation area masters (extent, geo-fence, rate types)",
                    "US-CVC / US-GIS evidence",
                    "Must",
                ]
                for i, v in enumerate(vals):
                    if i < len(new_row.cells):
                        set_cell_text(new_row.cells[i], v)
                return


def main():
    if not SRC.exists():
        raise SystemExit(f"Source not found: {SRC}")

    shutil.copy2(SRC, DST)
    doc = Document(str(DST))

    update_document_control_version(doc)
    append_version_history_row(doc)
    append_frs(doc)
    update_data_entities(doc)
    update_business_rules_if_present(doc)
    update_rtm(doc)

    try:
        doc.save(str(DST))
    except PermissionError:
        alt = BASE / "BRD_CVC_Guidance_Value_Fixation_v1.5_updated.docx"
        doc.save(str(alt))
        print(f"NOTE: locked; wrote {alt}")
        return

    print(f"Wrote {DST}")
    table = find_common_fr_table(doc)
    for r in table.rows[1:]:
        rid = r.cells[0].text.strip()
        if rid.startswith("FR-CVC-00") and int(rid.split("-")[-1]) >= 8:
            print(rid, "→", r.cells[1].text.strip()[:100])


if __name__ == "__main__":
    main()
