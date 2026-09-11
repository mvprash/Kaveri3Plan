#!/usr/bin/env python3
"""Generate Karnataka Secs. 22-B / 22-C / 22-D swimlane process diagram.

Source: The Registration (Karnataka Amendment) Act, 2023 (Karnataka Act 47 of 2024);
Requirement Discussions/Daily Reports/Document_Registration_requirement_07092026_v1.1.docx

Outputs (under Finalized BRD/Document Registration/ProcessDiagram):
  - Registration_22BCD_Forged_Document.drawio
  - Registration_22BCD_Forged_Document.mmd
  - Registration_22BCD_Forged_Document.png  (Pillow swimlane; mermaid optional)
"""
from __future__ import annotations

import html
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

OUTPUT_DIR = Path(__file__).resolve().parent
TITLE = "Karnataka Secs. 22-B / 22-C / 22-D — Forged / Prohibited Documents"
STEM = "Registration_22BCD_Forged_Document"

# Same lane colours / order pattern as Part XII; 5th lane = IGR (Sec. 22-D)
# plus Civil Court for optional further judicial challenge after IGR.
LANES = [
    ("lane_citizen", "Citizen", "#fff2cc", "#d6b656"),
    ("lane_system", "System", "#e1f5e0", "#82b366"),
    ("lane_sr", "Sub-Registrar", "#dae8fc", "#6c8ebf"),
    ("lane_dr", "District Registrar", "#e1d5e7", "#9673a6"),
    ("lane_igr", "IGR", "#ffe6cc", "#d79b00"),
    ("lane_court", "Civil Court", "#f8cecc", "#b85450"),
]

LANE_Y = 90
LANE_H = 140
LANE_X = 40
LANE_W = 4600
LABEL_W = 120

# (id, label, lane, x, w, h, kind, fill, stroke)
NODES = [
    # ── Citizen ──────────────────────────────────────────────────────────
    ("start", "Start", "lane_citizen", 20, 70, 40, "ellipse", "#dae8fc", "#6c8ebf"),
    (
        "presentDoc",
        "Document presented\nfor registration",
        "lane_citizen",
        110,
        130,
        50,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "getRefusal22B",
        "Obtains Sec. 22-B\nrefusal / Book 2 copy",
        "lane_citizen",
        560,
        140,
        50,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "endRefused22B",
        "End\n(Refused 22-B)",
        "lane_citizen",
        740,
        110,
        50,
        "ellipse",
        "#f8cecc",
        "#b85450",
    ),
    (
        "receiveRegistered",
        "Receives registered\ndocument",
        "lane_citizen",
        740,
        120,
        50,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "endOkDirect",
        "End\n(Registered)\n(may face 22-C later)",
        "lane_citizen",
        900,
        130,
        55,
        "ellipse",
        "#d5e8d4",
        "#82b366",
    ),
    # Sec. 22-C track entry (post-registration)
    (
        "start22C",
        "Start\n(Sec. 22-C)",
        "lane_citizen",
        1100,
        100,
        50,
        "ellipse",
        "#dae8fc",
        "#6c8ebf",
    ),
    (
        "fileComplaint",
        "Aggrieved person files\ncomplaint under Sec. 22-C\n(or DR acts suo motu)",
        "lane_citizen",
        1240,
        160,
        60,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "replyShowCause",
        "Executants / parties\nreply to show-cause\nnotice",
        "lane_citizen",
        1820,
        140,
        60,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "decideAppeal22D",
        "File Sec. 22-D\nappeal ≤ 30 days?",
        "lane_citizen",
        2580,
        130,
        70,
        "diamond",
        "#ffffff",
        "#000000",
    ),
    (
        "fileAppeal22D",
        "Appeal to IGR\nwithin 30 days of\ncancellation (Sec. 22-D)",
        "lane_citizen",
        2760,
        150,
        60,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "noAppeal",
        "No appeal filed",
        "lane_citizen",
        2760,
        110,
        40,
        "rect",
        "#f5f5f5",
        "#666666",
    ),
    (
        "endCancelled",
        "End\n(Cancelled stands)",
        "lane_citizen",
        2940,
        120,
        50,
        "ellipse",
        "#f8cecc",
        "#b85450",
    ),
    (
        "receiveRestored",
        "Registration restored\n/ status updated",
        "lane_citizen",
        3880,
        130,
        50,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "endRestored",
        "End\n(Restored)",
        "lane_citizen",
        4060,
        100,
        50,
        "ellipse",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "decideCourt",
        "Further challenge\nin Civil Court?",
        "lane_citizen",
        3880,
        130,
        70,
        "diamond",
        "#ffffff",
        "#000000",
    ),
    (
        "fileSuit",
        "Institute civil suit\n/ writ petition",
        "lane_citizen",
        4060,
        130,
        50,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "endAfterIgr",
        "End\n(IGR order final\ndepartmentally)",
        "lane_citizen",
        4060,
        120,
        55,
        "ellipse",
        "#f5f5f5",
        "#666666",
    ),
    # ── System ───────────────────────────────────────────────────────────
    (
        "sysScreen22B",
        "Screen for Sec. 22-B:\nforged / prohibited /\nattached property /\nnotified class",
        "lane_system",
        110,
        160,
        75,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysBook2_22B",
        "Record Sec. 22-B refusal\nin Book 2; status =\nRefused (22-B); notify;\ngenerate copy",
        "lane_system",
        360,
        170,
        75,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysRegisterComplaint",
        "Register complaint /\nsuo-motu case;\nLimitation Act check\n(+ condonation flag)",
        "lane_system",
        1440,
        160,
        75,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysServeNotice",
        "Serve show-cause\nnotices; track replies\n& affected parties",
        "lane_system",
        1640,
        150,
        70,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysEnterCancel",
        "Enter cancellation in\nrelevant books & indexes;\nupdate status; notify\nparties (Rule 17(iii))",
        "lane_system",
        2300,
        170,
        75,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysClose22C",
        "Close 22-C case;\nregistration stands;\nnotify complainant",
        "lane_system",
        2300,
        150,
        60,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysValidateAppeal",
        "Validate ≤ 30 days;\nregister Sec. 22-D\nappeal; list for IGR",
        "lane_system",
        2960,
        150,
        70,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysApplyIgr",
        "Apply IGR order:\nconfirm / modify /\nrestore registration\nin books & indexes",
        "lane_system",
        3680,
        160,
        75,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    # ── Sub-Registrar ────────────────────────────────────────────────────
    (
        "srExamine",
        "Examine document &\nSec. 22-B compliance\n(title disputes excluded)",
        "lane_sr",
        110,
        160,
        60,
        "rect",
        "#dae8fc",
        "#6c8ebf",
    ),
    (
        "srDecide22B",
        "Hits Sec. 22-B\ngrounds?",
        "lane_sr",
        300,
        120,
        70,
        "diamond",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "srRefuse22B",
        "Sec. 22-B — Refuse\nregistration (forged /\nprohibited / attached /\nnotified)",
        "lane_sr",
        360,
        170,
        70,
        "rect",
        "#f8cecc",
        "#b85450",
    ),
    (
        "srRegister",
        "Admit & register\ndocument\n(subject to later 22-C)",
        "lane_sr",
        560,
        150,
        60,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    # ── District Registrar ───────────────────────────────────────────────
    (
        "drTrigger",
        "Sec. 22-C trigger:\nsuo motu OR complaint\nfrom aggrieved person",
        "lane_dr",
        1240,
        160,
        60,
        "rect",
        "#e1d5e7",
        "#9673a6",
    ),
    (
        "drOpinion",
        "Opinion: registered\nin contravention of\nSec. 22-B?",
        "lane_dr",
        1620,
        140,
        70,
        "diamond",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "drShowCause",
        "Issue show-cause notice\nto executants, parties,\nsubsequent parties &\naffected persons",
        "lane_dr",
        1800,
        170,
        75,
        "rect",
        "#e1d5e7",
        "#9673a6",
    ),
    (
        "drDecideCancel",
        "Cancel\nregistration?",
        "lane_dr",
        2120,
        120,
        70,
        "diamond",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "drCancel",
        "Sec. 22-C — Cancel\nregistration; order\nto books & indexes",
        "lane_dr",
        2300,
        150,
        60,
        "rect",
        "#f8cecc",
        "#b85450",
    ),
    (
        "drNoCancel",
        "Drop / refuse to cancel;\nregistration continues",
        "lane_dr",
        2300,
        150,
        60,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "endStands",
        "End\n(Registration stands)",
        "lane_citizen",
        2500,
        120,
        50,
        "ellipse",
        "#d5e8d4",
        "#82b366",
    ),
    # ── IGR ──────────────────────────────────────────────────────────────
    (
        "igrHear",
        "Hear Sec. 22-D appeal\n(within limitation +\ncondonation if any)",
        "lane_igr",
        3120,
        160,
        60,
        "rect",
        "#ffe6cc",
        "#d79b00",
    ),
    (
        "igrDecide",
        "IGR order\n(confirm / modify /\ncancel DR order)",
        "lane_igr",
        3320,
        150,
        70,
        "diamond",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "igrConfirm",
        "Confirm DR\ncancellation",
        "lane_igr",
        3500,
        120,
        50,
        "rect",
        "#f8cecc",
        "#b85450",
    ),
    (
        "igrSetAside",
        "Cancel / modify DR\norder — restore or\namend registration",
        "lane_igr",
        3500,
        140,
        60,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    # ── Civil Court ──────────────────────────────────────────────────────
    (
        "courtHear",
        "Try civil suit /\nwrit against IGR\n(or DR) order",
        "lane_court",
        4240,
        150,
        60,
        "rect",
        "#f8cecc",
        "#b85450",
    ),
    (
        "courtDecide",
        "Court directs\nrestore / uphold?",
        "lane_court",
        4420,
        120,
        70,
        "diamond",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "courtRestore",
        "Decree / order:\nrestore registration",
        "lane_court",
        4580,
        130,
        50,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "courtUphold",
        "Dismiss / uphold\ncancellation",
        "lane_court",
        4580,
        130,
        50,
        "rect",
        "#f8cecc",
        "#b85450",
    ),
    (
        "endCourtOk",
        "End\n(Court restored)",
        "lane_citizen",
        4740,
        110,
        50,
        "ellipse",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "endCourtNo",
        "End\n(Cancellation final)",
        "lane_citizen",
        4740,
        110,
        50,
        "ellipse",
        "#f8cecc",
        "#b85450",
    ),
]

# Page width for Civil Court branch
LANE_W = 5000

NODE_Y_BIAS: dict[str, float] = {
    # upper = refuse / cancel / confirm paths
    "getRefusal22B": 0.12,
    "endRefused22B": 0.12,
    "sysBook2_22B": 0.12,
    "srRefuse22B": 0.12,
    # lower = register / stands / restore
    "receiveRegistered": 0.52,
    "endOkDirect": 0.52,
    "srRegister": 0.52,
    "sysClose22C": 0.12,
    "drNoCancel": 0.12,
    "endStands": 0.12,
    "drCancel": 0.52,
    "sysEnterCancel": 0.48,
    "fileAppeal22D": 0.12,
    "noAppeal": 0.55,
    "endCancelled": 0.55,
    "igrConfirm": 0.12,
    "igrSetAside": 0.52,
    "receiveRestored": 0.55,
    "endRestored": 0.55,
    "decideCourt": 0.12,
    "fileSuit": 0.12,
    "endAfterIgr": 0.38,
    "courtRestore": 0.12,
    "courtUphold": 0.55,
    "endCourtOk": 0.12,
    "endCourtNo": 0.55,
}

EDGES: list[tuple[str, str, str]] = [
    # Sec. 22-B intake
    ("start", "presentDoc", ""),
    ("presentDoc", "sysScreen22B", ""),
    ("sysScreen22B", "srExamine", ""),
    ("srExamine", "srDecide22B", ""),
    ("srDecide22B", "srRefuse22B", "Yes"),
    ("srDecide22B", "srRegister", "No"),
    ("srRefuse22B", "sysBook2_22B", ""),
    ("sysBook2_22B", "getRefusal22B", ""),
    ("getRefusal22B", "endRefused22B", ""),
    ("srRegister", "receiveRegistered", ""),
    ("receiveRegistered", "endOkDirect", ""),
    # Sec. 22-C (separate post-registration track)
    ("start22C", "fileComplaint", ""),
    ("fileComplaint", "drTrigger", ""),
    ("drTrigger", "sysRegisterComplaint", ""),
    ("sysRegisterComplaint", "drOpinion", ""),
    ("drOpinion", "drShowCause", "Yes"),
    ("drOpinion", "sysClose22C", "No"),
    ("sysClose22C", "endStands", ""),
    ("drShowCause", "sysServeNotice", ""),
    ("sysServeNotice", "replyShowCause", ""),
    ("replyShowCause", "drDecideCancel", ""),
    ("drDecideCancel", "drCancel", "Yes"),
    ("drDecideCancel", "drNoCancel", "No"),
    ("drNoCancel", "sysClose22C", ""),
    ("drCancel", "sysEnterCancel", ""),
    ("sysEnterCancel", "decideAppeal22D", ""),
    # Sec. 22-D
    ("decideAppeal22D", "fileAppeal22D", "Yes"),
    ("decideAppeal22D", "noAppeal", "No"),
    ("noAppeal", "endCancelled", ""),
    ("fileAppeal22D", "sysValidateAppeal", ""),
    ("sysValidateAppeal", "igrHear", ""),
    ("igrHear", "igrDecide", ""),
    ("igrDecide", "igrConfirm", "Confirm"),
    ("igrDecide", "igrSetAside", "Cancel /\nmodify"),
    ("igrConfirm", "sysApplyIgr", ""),
    ("igrSetAside", "sysApplyIgr", ""),
    ("sysApplyIgr", "receiveRestored", "Restored /\nmodified"),
    ("sysApplyIgr", "decideCourt", "Confirmed\ncancel"),
    ("receiveRestored", "endRestored", ""),
    ("decideCourt", "fileSuit", "Yes"),
    ("decideCourt", "endAfterIgr", "No"),
    ("fileSuit", "courtHear", ""),
    ("courtHear", "courtDecide", ""),
    ("courtDecide", "courtRestore", "Restore"),
    ("courtDecide", "courtUphold", "Uphold"),
    ("courtRestore", "endCourtOk", ""),
    ("courtUphold", "endCourtNo", ""),
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
        f'    <mxGeometry x="{LANE_X + 900}" y="30" width="900" height="30" as="geometry"/>',
        "  </mxCell>",
        '  <mxCell id="subtitle" value="Registration (Karnataka Amendment) Act, 2023 — Act 47 of 2024  |  Parallel track to Classic Part XII (Secs. 71–77)" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=11;fontColor=#666666;" vertex="1" parent="1">',
        f'    <mxGeometry x="{LANE_X + 700}" y="58" width="1100" height="24" as="geometry"/>',
        "  </mxCell>",
    ]

    lane_ids = {lid: str(i + 2) for i, (lid, *_) in enumerate(LANES)}
    for i, (lid, label, fill, stroke) in enumerate(LANES):
        mx = lane_ids[lid]
        cells.append(
            f'  <mxCell id="{mx}" value="{esc(label)}" style="{lane_style(fill, stroke)}" vertex="1" parent="1">'
        )
        cells.append(
            f'    <mxGeometry x="{LANE_X}" y="{LANE_Y + i * LANE_H}" width="{LANE_W}" height="{LANE_H}" as="geometry"/>'
        )
        cells.append("  </mxCell>")

    node_mx: dict[str, str] = {}
    next_id = len(LANES) + 2
    for node_id, label, lane, x, w, h, kind, fill, stroke in NODES:
        mx_id = str(next_id)
        node_mx[node_id] = mx_id
        next_id += 1
        bias = NODE_Y_BIAS.get(node_id)
        if bias is None:
            y_offset = max(8, (LANE_H - h) // 2 - 4)
        else:
            y_offset = int(bias * (LANE_H - 10))
            y_offset = max(8, min(y_offset, LANE_H - h - 8))
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
            f'  <mxCell id="{mx_id}"{label_attr} style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;fontSize=9;endArrow=classic;fontColor=#333333;" edge="1" parent="1" source="{node_mx[src]}" target="{node_mx[tgt]}">'
        )
        cells.append('    <mxGeometry relative="1" as="geometry"/>')
        cells.append("  </mxCell>")

    legend_y = LANE_Y + len(LANES) * LANE_H + 20
    legend = (
        "Legend: Sec. 22-B — SR mandatory refusal (forged / prohibited / attached property / notified). "
        "Sec. 22-C — DR cancellation suo motu or on complaint (show-cause → books & indexes). "
        "Sec. 22-D — appeal to IGR ≤ 30 days (confirm / modify / cancel DR order). "
        "Limitation Act + condonation applies to 22-C / 22-D. "
        "Civil Court = optional further judicial challenge (not Sec. 77). "
        "Title disputes excluded from forged-document enquiry. Secs. 81-A / 81-B = penalties (compliance)."
    )
    cells.append(
        f'  <mxCell id="{next_id}" value="{esc(legend)}" style="text;html=1;strokeColor=#999999;fillColor=#f5f5f5;align=left;verticalAlign=middle;fontSize=10;spacingLeft=8;spacingRight=8;" vertex="1" parent="1">'
    )
    cells.append(
        f'    <mxGeometry x="{LANE_X}" y="{legend_y}" width="{LANE_W}" height="55" as="geometry"/>'
    )
    cells.append("  </mxCell>")

    body = "\n".join(cells)
    page_h = legend_y + 90
    return f"""<mxfile host="app.diagrams.net" agent="Kaveri3-Plan" version="24.7.0" type="device">
  <diagram id="reg-22bcd" name="{esc(TITLE)}">
    <mxGraphModel dx="2000" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{LANE_W + 100}" pageHeight="{page_h}" math="0" shadow="0">
      <root>
{body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""


def build_mermaid() -> str:
    lines = [
        "---",
        f"title: {TITLE}",
        "---",
        "flowchart LR",
        "",
    ]
    for lid, title, *_ in LANES:
        lines.append(f'    subgraph {lid}["{title}"]')
        lines.append("        direction LR")
        for node_id, label, nlane, *rest in NODES:
            if nlane != lid:
                continue
            kind = rest[3]
            clean = label.replace("\n", "<br/>").replace('"', "'")
            if kind == "diamond":
                lines.append(f'        {node_id}{{"{clean}"}}')
            elif kind == "ellipse":
                lines.append(f'        {node_id}(("{clean}"))')
            else:
                lines.append(f'        {node_id}["{clean}"]')
        lines.append("    end")
        lines.append("")

    for src, tgt, label in EDGES:
        if label:
            clean = label.replace("\n", " ")
            lines.append(f'    {src} -->|"{clean}"| {tgt}')
        else:
            lines.append(f"    {src} --> {tgt}")
    return "\n".join(lines) + "\n"


def render_png_pillow(out_png: Path) -> None:
    """Fallback swimlane PNG matching draw.io lane order."""
    from PIL import Image, ImageDraw, ImageFont

    margin = 40
    title_h = 70
    lane_h = 150
    lane_label_w = 130
    width = LANE_W + margin * 2
    height = title_h + len(LANES) * lane_h + 100
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    # Windows + Linux font fallbacks
    font_candidates = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    bold_candidates = [
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]

    def load_font(paths, size):
        for p in paths:
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
        return ImageFont.load_default()

    font_title = load_font(bold_candidates, 18)
    font = load_font(font_candidates, 11)
    font_small = load_font(font_candidates, 9)
    font_lane = load_font(bold_candidates, 11)

    draw.text((margin + 350, 12), TITLE, fill="#1a1a1a", font=font_title)
    draw.text(
        (margin + 280, 42),
        "Karnataka Act 47 of 2024 — Secs. 22-B (refuse) · 22-C (DR cancel) · 22-D (appeal to IGR)",
        fill="#555555",
        font=font_small,
    )

    lane_top = {lid: title_h + i * lane_h for i, (lid, *_) in enumerate(LANES)}
    for i, (lid, label, fill, stroke) in enumerate(LANES):
        y = lane_top[lid]
        draw.rectangle(
            [margin, y, margin + LANE_W, y + lane_h],
            outline=stroke,
            width=2,
            fill=fill,
        )
        draw.rectangle(
            [margin, y, margin + lane_label_w, y + lane_h],
            outline=stroke,
            width=2,
            fill=stroke,
        )
        # vertical-ish label (horizontal text for readability)
        bbox = draw.textbbox((0, 0), label, font=font_lane)
        tw = bbox[2] - bbox[0]
        draw.text(
            (margin + (lane_label_w - tw) // 2, y + lane_h // 2 - 8),
            label,
            fill="white",
            font=font_lane,
        )

    abs_pos: dict[str, tuple[int, int, int, int]] = {}
    for node_id, label, lane, x, w, h, kind, fill, stroke in NODES:
        y0 = lane_top[lane]
        bias = NODE_Y_BIAS.get(node_id)
        if bias is None:
            y_off = (lane_h - h) // 2
        else:
            y_off = int(bias * (lane_h - 10))
            y_off = max(8, min(y_off, lane_h - h - 8))
        ax = margin + lane_label_w + x
        ay = y0 + y_off
        abs_pos[node_id] = (ax, ay, w, h)
        if kind == "ellipse":
            draw.ellipse([ax, ay, ax + w, ay + h], outline=stroke, width=2, fill=fill)
        elif kind == "diamond":
            cx, cy = ax + w // 2, ay + h // 2
            pts = [(cx, ay), (ax + w, cy), (cx, ay + h), (ax, cy)]
            draw.polygon(pts, outline=stroke, fill=fill)
        else:
            draw.rectangle([ax, ay, ax + w, ay + h], outline=stroke, width=2, fill=fill)
        lines = label.split("\n")
        ty = ay + max(4, (h - 11 * len(lines)) // 2)
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_small)
            tw = bbox[2] - bbox[0]
            draw.text((ax + (w - tw) // 2, ty), line, fill="#111111", font=font_small)
            ty += 11

    def center(box):
        ax, ay, w, h = box
        return ax + w // 2, ay + h // 2

    for src, tgt, label in EDGES:
        if src not in abs_pos or tgt not in abs_pos:
            continue
        x1, y1 = center(abs_pos[src])
        x2, y2 = center(abs_pos[tgt])
        sx = abs_pos[src][0] + abs_pos[src][2]
        sy = y1
        tx = abs_pos[tgt][0]
        ty = y2
        mid_x = (sx + tx) // 2
        draw.line([(sx, sy), (mid_x, sy), (mid_x, ty), (tx, ty)], fill="#444444", width=1)
        draw.polygon([(tx, ty), (tx - 8, ty - 4), (tx - 8, ty + 4)], fill="#444444")
        if label:
            clean = label.replace("\n", " ")
            draw.text((mid_x + 4, min(sy, ty) - 12), clean, fill="#333333", font=font_small)

    note_y = title_h + len(LANES) * lane_h + 10
    draw.rectangle(
        [margin, note_y, margin + LANE_W, note_y + 55],
        outline="#999999",
        fill="#f5f5f5",
    )
    draw.text(
        (margin + 10, note_y + 6),
        "Sec. 22-B SR refusal → Sec. 22-C DR cancellation (suo motu / complaint + show-cause) → "
        "Sec. 22-D appeal to IGR ≤30 days (confirm / modify / cancel) → optional Civil Court challenge.",
        fill="#333333",
        font=font_small,
    )
    draw.text(
        (margin + 10, note_y + 22),
        "Actors: Citizen · System · Sub-Registrar · District Registrar · IGR · Civil Court. "
        "Limitation Act + condonation on 22-C/22-D. Title disputes excluded. Secs. 81-A/81-B penalties (not shown).",
        fill="#555555",
        font=font_small,
    )
    draw.text(
        (margin + 10, note_y + 38),
        "Source: Karnataka Act 47 of 2024; Document_Registration_requirement_07092026_v1.1.docx",
        fill="#777777",
        font=font_small,
    )

    img.save(out_png, "PNG")
    print(f"Wrote Pillow PNG: {out_png}")


def try_mermaid_png(mmd: Path, out_png: Path) -> bool:
    try:
        cmd = [
            "npx",
            "--yes",
            "@mermaid-js/mermaid-cli",
            "-i",
            str(mmd),
            "-o",
            str(out_png),
            "-b",
            "white",
            "-w",
            "3600",
            "-s",
            "2",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if r.returncode == 0 and out_png.exists():
            print(f"Wrote mermaid PNG: {out_png}")
            return True
        print("mermaid-cli failed:", (r.stderr or r.stdout or "")[-500:])
    except Exception as e:
        print("mermaid-cli unavailable:", e)
    return False


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    drawio_path = OUTPUT_DIR / f"{STEM}.drawio"
    mmd_path = OUTPUT_DIR / f"{STEM}.mmd"
    png_path = OUTPUT_DIR / f"{STEM}.png"

    drawio_path.write_text(build_drawio(), encoding="utf-8")
    mmd_path.write_text(build_mermaid(), encoding="utf-8")
    print(f"Wrote {drawio_path}")
    print(f"Wrote {mmd_path}")

    if not try_mermaid_png(mmd_path, OUTPUT_DIR / f"{STEM}_mermaid.png"):
        print("Skipping mermaid PNG (optional).")
    render_png_pillow(png_path)

    print("Done. Files:")
    for p in sorted(OUTPUT_DIR.glob(f"{STEM}.*")):
        print(f"  {p.name} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
