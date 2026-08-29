#!/usr/bin/env python3
"""Generate swimlane draw.io diagram matching DocumentRegistrationProcessMap.pdf."""

from __future__ import annotations

import html
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent
TITLE = "Document Registration – Online"

LANES = [
    ("lane_citizen", "Citizen", "#fff2cc", "#d6b656"),
    ("lane_system", "System", "#e1f5e0", "#82b366"),
    ("lane_sr", "SR", "#dae8fc", "#6c8ebf"),
    ("lane_fda", "FDA/SDA", "#f5f5f5", "#666666"),
]

LANE_Y = 100
LANE_H = 130
LANE_X = 40
LANE_W = 3000
LABEL_W = 100

# (id, label, lane, x, w, h, kind, fill, stroke)
# kind: rect | diamond | ellipse
# x = horizontal offset inside lane content area (after label)
NODES: list[tuple] = [
    # ── Citizen lane ──
    ("start", "Start", "lane_citizen", 30, 60, 36, "ellipse", "#dae8fc", "#6c8ebf"),
    ("login", "Log on to department Portal", "lane_citizen", 110, 130, 44, "rect", "#fff2cc", "#d6b656"),
    ("serviceType", "Select Service Type", "lane_citizen", 260, 120, 44, "rect", "#fff2cc", "#d6b656"),
    ("sro", "Identify the SRO where\nproperty belongs", "lane_citizen", 400, 130, 50, "rect", "#fff2cc", "#d6b656"),
    ("sroOffice", "Identify the Sub-Registrar\nOffice where to apply", "lane_citizen", 550, 140, 50, "rect", "#fff2cc", "#d6b656"),
    ("readForm", "Read Instructions and Enter\nDetails in the displayed form", "lane_citizen", 710, 150, 50, "rect", "#fff2cc", "#d6b656"),
    ("bookSlot", "Book available\ndate and time", "lane_citizen", 880, 110, 44, "rect", "#fff2cc", "#d6b656"),
    ("submitPay", "Submit Form\n& pay Fees", "lane_citizen", 1010, 100, 44, "rect", "#fff2cc", "#d6b656"),
    ("visitSR", "Visits SR", "lane_citizen", 1380, 80, 44, "rect", "#fff2cc", "#d6b656"),
    ("kiosk", "Marks his presence\nin kiosk", "lane_citizen", 1480, 100, 44, "rect", "#fff2cc", "#d6b656"),
    ("presentDoc", "Present document\nto SR", "lane_citizen", 1680, 100, 44, "rect", "#dae8fc", "#6c8ebf"),
    ("collectReceipt", "Collect Receipt", "lane_citizen", 1980, 100, 44, "rect", "#dae8fc", "#6c8ebf"),
    ("signThumbCopy", "Sign Thumb\nImpression copy", "lane_citizen", 2080, 100, 44, "rect", "#dae8fc", "#6c8ebf"),
    ("signForm6061", "Signs Form 60.61;\nSign declaration", "lane_citizen", 2180, 110, 50, "rect", "#dae8fc", "#6c8ebf"),
    ("partiesSign", "Parties and witnesses\nSign Endorsement", "lane_citizen", 2280, 120, 50, "rect", "#dae8fc", "#6c8ebf"),
    ("signSummaryCitizen", "Signs\nSummary Report", "lane_citizen", 2480, 100, 44, "rect", "#dae8fc", "#6c8ebf"),
    ("errorCheck", "Error?", "lane_citizen", 2600, 70, 50, "diamond", "#ffffff", "#000000"),
    ("receiveDoc", "Receives original document\nwith print of scanned copy and EC", "lane_citizen", 2720, 160, 50, "rect", "#f5f5f5", "#666666"),
    ("endSuccess", "End", "lane_citizen", 2900, 60, 36, "ellipse", "#dae8fc", "#6c8ebf"),

    # ── System lane ──
    ("recordPayment", "Record payment,\ngenerate receipt", "lane_system", 1010, 120, 44, "rect", "#d5e8d4", "#82b366"),
    ("validApp", "Valid\nApplication?", "lane_system", 1150, 80, 60, "diamond", "#fff2cc", "#d6b656"),
    ("optionChange", "Option\nfor change", "lane_system", 1260, 80, 60, "diamond", "#fff2cc", "#d6b656"),
    ("forwardSR", "Forward application to SR and\nintimate applicant to visit SR\non appointed date", "lane_system", 1380, 150, 60, "rect", "#fff2cc", "#d6b656"),
    ("minuteBook", "Enter the reason\nin minute book", "lane_system", 1260, 110, 44, "rect", "#fff2cc", "#d6b656"),
    ("genPending", "Generate\npending no.", "lane_system", 1150, 100, 44, "rect", "#d5e8d4", "#82b366"),
    ("printIntimation", "Print\nIntimation", "lane_system", 1040, 90, 44, "rect", "#d5e8d4", "#82b366"),
    ("endReject", "End", "lane_system", 930, 60, 36, "ellipse", "#dae8fc", "#6c8ebf"),
    ("updateStatus", "Update status in system\nas ready for presentation", "lane_system", 1550, 140, 50, "rect", "#fff2cc", "#d6b656"),
    ("recordRegister", "Record in\nappropriate Register", "lane_system", 1880, 120, 44, "rect", "#d5e8d4", "#82b366"),
    ("updateAReg", "Update A Register, Index register,\nGen. J Slip", "lane_system", 2080, 150, 50, "rect", "#d5e8d4", "#82b366"),
    ("genRegNo", "Generate\nRegistration No.", "lane_system", 2180, 110, 44, "rect", "#d5e8d4", "#82b366"),
    ("printSummary", "Print\nsummary report", "lane_system", 2480, 100, 44, "rect", "#d5e8d4", "#82b366"),
    ("scanDoc", "Scan the\nDocument", "lane_system", 2600, 100, 44, "rect", "#d5e8d4", "#82b366"),
    ("printIndexII", "Print the document\nand Index II record", "lane_system", 2720, 120, 44, "rect", "#d5e8d4", "#82b366"),
    ("stop", "Stop", "lane_system", 1920, 60, 36, "ellipse", "#f8cecc", "#b85450"),

    # ── SR lane ──
    ("form6061", "Accept Form 60/61 if PAN not given;\nPrint declaration", "lane_sr", 1010, 150, 50, "rect", "#fff2cc", "#d6b656"),
    ("callsParties", "Calls parties\nto present", "lane_sr", 1620, 100, 44, "rect", "#d5e8d4", "#82b366"),
    ("srExamine", "SR examines the document\nand SD/RF", "lane_sr", 1740, 130, 50, "rect", "#dae8fc", "#6c8ebf"),
    ("fullSDRF", "Full SD/RF\npaid?", "lane_sr", 1580, 80, 60, "diamond", "#fff2cc", "#d6b656"),
    ("referDR", "Refer case to DR\nfor MV/Impound", "lane_sr", 1480, 110, 44, "rect", "#fff2cc", "#d6b656"),
    ("voluntaryExec", "Voluntary execution and\nValid Application?", "lane_sr", 1860, 80, 70, "diamond", "#dae8fc", "#6c8ebf"),
    ("refusalReason", "Enter refusal\nreason in system", "lane_sr", 1980, 110, 44, "rect", "#d5e8d4", "#82b366"),
    ("admitDoc", "Admit document and enter\npayment detail in system", "lane_sr", 2060, 140, 50, "rect", "#d5e8d4", "#82b366"),
    ("attachEndorse", "Attaches signed and sealed\nendorsement to Document", "lane_sr", 2220, 140, 50, "rect", "#dae8fc", "#6c8ebf"),
    ("signSummarySR", "Signs summary\nReport", "lane_sr", 2480, 100, 44, "rect", "#dae8fc", "#6c8ebf"),
    ("genSummary", "Generate\nSummary Report", "lane_sr", 2380, 100, 44, "rect", "#d5e8d4", "#82b366"),
    ("checkRegister", "Check and\nRegister", "lane_sr", 2580, 100, 44, "rect", "#d5e8d4", "#82b366"),
    ("srCorrect", "SR corrects data", "lane_sr", 2660, 100, 44, "rect", "#dae8fc", "#6c8ebf"),
    ("srSignEndorse", "Signs\nEndorsement", "lane_sr", 2720, 90, 44, "rect", "#dae8fc", "#6c8ebf"),

    # ── FDA/SDA lane ──
    ("captureBio", "Capture photograph\nand thumb impression", "lane_fda", 1980, 130, 50, "rect", "#d5e8d4", "#82b366"),
    ("printThumb", "Print Thumb\nImpression", "lane_fda", 2080, 100, 44, "rect", "#d5e8d4", "#82b366"),
    ("printEndorse", "Prints\nEndorsement", "lane_fda", 2580, 100, 44, "rect", "#d5e8d4", "#82b366"),
    ("fileThumbReg", "File in\nThumb Register", "lane_fda", 2720, 100, 44, "rect", "#d5e8d4", "#82b366"),
]

EDGES: list[tuple[str, str, str]] = [
    ("start", "login", ""),
    ("login", "serviceType", ""),
    ("serviceType", "sro", ""),
    ("sro", "sroOffice", ""),
    ("sroOffice", "readForm", ""),
    ("readForm", "bookSlot", ""),
    ("bookSlot", "submitPay", ""),
    ("submitPay", "recordPayment", ""),
    ("submitPay", "validApp", ""),
    ("recordPayment", "form6061", ""),
    ("form6061", "forwardSR", ""),
    ("validApp", "optionChange", "No"),
    ("validApp", "forwardSR", "Yes"),
    ("optionChange", "readForm", "Yes"),
    ("optionChange", "minuteBook", "No"),
    ("minuteBook", "genPending", ""),
    ("genPending", "printIntimation", ""),
    ("printIntimation", "endReject", ""),
    ("forwardSR", "updateStatus", ""),
    ("forwardSR", "visitSR", ""),
    ("visitSR", "kiosk", ""),
    ("kiosk", "updateStatus", ""),
    ("updateStatus", "callsParties", ""),
    ("callsParties", "presentDoc", ""),
    ("presentDoc", "srExamine", ""),
    ("srExamine", "fullSDRF", ""),
    ("fullSDRF", "referDR", "No"),
    ("fullSDRF", "voluntaryExec", "Yes"),
    ("voluntaryExec", "refusalReason", "No"),
    ("voluntaryExec", "admitDoc", "Yes"),
    ("refusalReason", "stop", ""),
    ("admitDoc", "recordRegister", ""),
    ("admitDoc", "captureBio", ""),
    ("captureBio", "printThumb", ""),
    ("printThumb", "collectReceipt", ""),
    ("collectReceipt", "signForm6061", ""),
    ("signForm6061", "signThumbCopy", ""),
    ("signThumbCopy", "updateAReg", ""),
    ("updateAReg", "genRegNo", ""),
    ("genRegNo", "attachEndorse", ""),
    ("attachEndorse", "partiesSign", ""),
    ("partiesSign", "signSummaryCitizen", ""),
    ("signSummaryCitizen", "errorCheck", ""),
    ("errorCheck", "srCorrect", "Yes"),
    ("errorCheck", "printSummary", "No"),
    ("srCorrect", "genSummary", ""),
    ("genSummary", "checkRegister", ""),
    ("printSummary", "signSummarySR", ""),
    ("signSummarySR", "checkRegister", ""),
    ("checkRegister", "printEndorse", ""),
    ("checkRegister", "scanDoc", ""),
    ("printEndorse", "srSignEndorse", ""),
    ("srSignEndorse", "fileThumbReg", ""),
    ("scanDoc", "printIndexII", ""),
    ("printIndexII", "receiveDoc", ""),
    ("receiveDoc", "endSuccess", ""),
]


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def node_style(kind: str, fill: str, stroke: str) -> str:
    base = "whiteSpace=wrap;html=1;fontSize=10;"
    if kind == "diamond":
        return f"rhombus;{base}fillColor={fill};strokeColor={stroke};"
    if kind == "ellipse":
        return f"ellipse;{base}fillColor={fill};strokeColor={stroke};fontStyle=1"
    return f"rounded=0;{base}fillColor={fill};strokeColor={stroke};"


def lane_style(fill: str, stroke: str) -> str:
    return (
        f"swimlane;horizontal=0;whiteSpace=wrap;html=1;"
        f"startSize={LABEL_W};fillColor={fill};strokeColor={stroke};"
        f"fontStyle=1;fontSize=12;align=center;"
    )


def build_drawio() -> str:
    cells: list[str] = [
        '  <mxCell id="0"/>',
        '  <mxCell id="1" parent="0"/>',
        f'  <mxCell id="title" value="{esc(TITLE)}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=16;fontStyle=1" vertex="1" parent="1">',
        f'    <mxGeometry x="{LANE_X + 800}" y="40" width="500" height="30" as="geometry"/>',
        "  </mxCell>",
    ]

    lane_ids: dict[str, str] = {}
    for i, (lid, label, fill, stroke) in enumerate(LANES, start=2):
        lane_ids[lid] = str(i)
        y = LANE_Y + i * 0  # recalc below
        cells.append(
            f'  <mxCell id="{i}" value="{esc(label)}" style="{lane_style(fill, stroke)}" vertex="1" parent="1">'
        )
        cells.append(
            f'    <mxGeometry x="{LANE_X}" y="{LANE_Y + (i-2)*LANE_H}" width="{LANE_W}" height="{LANE_H}" as="geometry"/>'
        )
        cells.append("  </mxCell>")

    # rebuild lane_ids with correct mapping
    lane_ids = {lid: str(i + 2) for i, (lid, *_) in enumerate(LANES)}

    node_mx: dict[str, str] = {}
    next_id = len(LANES) + 2
    for node_id, label, lane, x, w, h, kind, fill, stroke in NODES:
        mx_id = str(next_id)
        node_mx[node_id] = mx_id
        next_id += 1
        y_offset = (LANE_H - h) // 2 - 5
        safe = esc(label.replace("\n", "&#xa;"))
        parent = lane_ids[lane]
        cells.append(
            f'  <mxCell id="{mx_id}" value="{safe}" style="{node_style(kind, fill, stroke)}" vertex="1" parent="{parent}">'
        )
        cells.append(
            f'    <mxGeometry x="{x + LABEL_W}" y="{y_offset}" width="{w}" height="{h}" as="geometry"/>'
        )
        cells.append("  </mxCell>")

    for src, tgt, label in EDGES:
        mx_id = str(next_id)
        next_id += 1
        label_attr = f' value="{esc(label)}"' if label else ""
        cells.append(
            f'  <mxCell id="{mx_id}"{label_attr} style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;fontSize=9;endArrow=classic;" edge="1" parent="1" source="{node_mx[src]}" target="{node_mx[tgt]}">'
        )
        cells.append('    <mxGeometry relative="1" as="geometry"/>')
        cells.append("  </mxCell>")

    body = "\n".join(cells)
    page_h = LANE_Y + len(LANES) * LANE_H + 80
    return f"""<mxfile host="app.diagrams.net" agent="Kaveri3-Plan" version="24.7.0" type="device">
  <diagram id="doc-reg-online-swimlane" name="{esc(TITLE)}">
    <mxGraphModel dx="2000" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="3100" pageHeight="{page_h}" math="0" shadow="0">
      <root>
{body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""


def build_mermaid() -> str:
    """Swimlane-style Mermaid (subgraph per lane)."""
    lane_nodes: dict[str, list[str]] = {l[0]: [] for l in LANES}
    id_lane: dict[str, str] = {}
    for node_id, label, lane, *_ in NODES:
        lane_nodes[lane].append(node_id)
        id_lane[node_id] = lane

    lines = [
        "---",
        f"title: {TITLE} (Swimlane)",
        "---",
        "flowchart LR",
        "",
    ]
    lane_titles = {lid: title for lid, title, *_ in LANES}
    for lid, title in lane_titles.items():
        lines.append(f"    subgraph {lid}[\"{title}\"]")
        lines.append("        direction LR")
        for node_id, label, nlane, *_ in NODES:
            if nlane != lid:
                continue
            clean = label.replace("\n", " ").replace('"', "'")
            kind = next(n[6] for n in NODES if n[0] == node_id)
            if kind == "diamond":
                lines.append(f'        {node_id}{{"{clean}"}}')
            elif kind == "ellipse":
                lines.append(f'        {node_id}(("{clean}"))')
            else:
                lines.append(f'        {node_id}["{clean}"]')
        lines.append("    end")
        lines.append("")

    for src, tgt, label in EDGES:
        arrow = f"-->|{label}|" if label else "-->"
        lines.append(f"    {src} {arrow} {tgt}")

    return "\n".join(lines) + "\n"


def main() -> None:
    drawio = OUTPUT_DIR / "Document_Registration_Online.drawio"
    mermaid = OUTPUT_DIR / "Document_Registration_Online.mmd"
    drawio.write_text(build_drawio(), encoding="utf-8")
    mermaid.write_text(build_mermaid(), encoding="utf-8")
    print(f"Regenerated: {drawio}")
    print(f"Regenerated: {mermaid}")


if __name__ == "__main__":
    main()
