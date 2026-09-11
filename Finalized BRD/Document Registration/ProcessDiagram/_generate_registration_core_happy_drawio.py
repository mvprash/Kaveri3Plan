#!/usr/bin/env python3
"""Generate Registration core (Registration + Appointment) happy-path swimlane.

Happy path exclusions (not drawn as pending branches):
  - Sec. 45-A undervaluation referral to District Registrar
  - Stamp Act impounding
  - Party appearance pending (Secs. 34–39 summons / non-appearance)
  - Private attendance pending (Sec. 31 private residence)

Sources:
  - Requirement Discussions/Daily Reports/Document_Registration_requirement_27082026_v1.1.docx
  - Requirement Discussions/Daily Reports/Document_Registration_requirement_28082026_v1.1.docx
  - ProcessDiagrams/Document_Registration_Online (As-Is process map)
  - Format: Registration_Appeal_Part_XII.png

Outputs (under Finalized BRD/Document Registration/ProcessDiagram):
  - Registration_Core_Appointment_Happy_Flow.drawio
  - Registration_Core_Appointment_Happy_Flow.mmd
  - Registration_Core_Appointment_Happy_Flow.png
"""
from __future__ import annotations

import html
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

OUTPUT_DIR = Path(__file__).resolve().parent
TITLE = "Registration Core – Registration & Appointment (Happy Path)"
STEM = "Registration_Core_Appointment_Happy_Flow"

LANES = [
    ("lane_citizen", "Citizen", "#fff2cc", "#d6b656"),
    ("lane_system", "System", "#e1f5e0", "#82b366"),
    ("lane_sr", "Sub-Registrar", "#dae8fc", "#6c8ebf"),
    ("lane_dr", "District Registrar", "#e1d5e7", "#9673a6"),
]

LANE_Y = 90
LANE_H = 150
LANE_X = 40
LANE_W = 4200
LABEL_W = 130

# (id, label, lane, x, w, h, kind, fill, stroke)
NODES = [
    # ── Citizen ──────────────────────────────────────────────────────────
    ("start", "Start", "lane_citizen", 20, 70, 40, "ellipse", "#dae8fc", "#6c8ebf"),
    (
        "login",
        "Log on to\ndepartment portal",
        "lane_citizen",
        110,
        120,
        50,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "selectService",
        "Select Document\nRegistration service",
        "lane_citizen",
        250,
        130,
        50,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "selectSRO",
        "Select SRO by property\njurisdiction (Sec. 28)",
        "lane_citizen",
        400,
        140,
        50,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "enterDetails",
        "Enter application details\n(article, property, parties,\nvaluation characteristics)",
        "lane_citizen",
        560,
        160,
        70,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "previewSubmit",
        "Review summary &\nsubmit for verification",
        "lane_citizen",
        740,
        140,
        50,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "payFees",
        "Pay stamp duty &\nregistration fee",
        "lane_citizen",
        1060,
        130,
        50,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "bookSlot",
        "Book appointment\nslot (date & time)",
        "lane_citizen",
        1280,
        130,
        50,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "visitSRO",
        "Visit SRO on\nappointed date\n(office attendance)",
        "lane_citizen",
        1680,
        130,
        60,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "kiosk",
        "Mark presence\nat kiosk",
        "lane_citizen",
        1830,
        110,
        50,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "presentDoc",
        "Present document;\nall parties appear\nat SRO (Sec. 34)",
        "lane_citizen",
        2060,
        140,
        60,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "signEndorse",
        "Sign Form 60/61,\nthumb copy,\nendorsements & summary",
        "lane_citizen",
        2860,
        150,
        60,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "receiveDoc",
        "Receive registered\ndocument + scanned\ncopy & EC",
        "lane_citizen",
        3720,
        130,
        60,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "endOk",
        "End\n(Registered)",
        "lane_citizen",
        3880,
        100,
        50,
        "ellipse",
        "#d5e8d4",
        "#82b366",
    ),
    # ── System ───────────────────────────────────────────────────────────
    (
        "sysValidate",
        "Validate jurisdiction &\napplication completeness",
        "lane_system",
        560,
        150,
        55,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysCalcDuty",
        "Compute SD / RF\n(consideration ≥ guideline;\nno 45-A trigger)",
        "lane_system",
        740,
        150,
        70,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysRecordPay",
        "Record payment;\ngenerate receipt",
        "lane_system",
        1060,
        130,
        50,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysConfirmSlot",
        "Confirm slot against\noffice hours / holidays;\nnotify citizen;\nstatus = Appointment booked",
        "lane_system",
        1280,
        160,
        80,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysReadyPresent",
        "Update status =\nReady for presentation",
        "lane_system",
        1830,
        140,
        55,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysRegisters",
        "Update Book / Index /\nJ-slip; generate\nRegistration No.",
        "lane_system",
        3040,
        140,
        70,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysScanCert",
        "Scan document;\nprint Index II;\nSec. 60 certificate",
        "lane_system",
        3380,
        140,
        70,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysStatusReg",
        "Status = Registered;\nprepare return of document",
        "lane_system",
        3560,
        140,
        55,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    # ── Sub-Registrar ────────────────────────────────────────────────────
    (
        "srReview",
        "Review application;\nSend to Applicant\nfor Payment",
        "lane_sr",
        900,
        140,
        70,
        "rect",
        "#dae8fc",
        "#6c8ebf",
    ),
    (
        "srCallParties",
        "Call parties on\nappointment",
        "lane_sr",
        1960,
        120,
        50,
        "rect",
        "#dae8fc",
        "#6c8ebf",
    ),
    (
        "srExamine",
        "Examine document &\nSD / RF (Secs. 34–35;\nRules 40–46)",
        "lane_sr",
        2220,
        150,
        60,
        "rect",
        "#dae8fc",
        "#6c8ebf",
    ),
    (
        "srStampOk",
        "Full SD/RF &\nno undervaluation\n/ impound?",
        "lane_sr",
        2400,
        130,
        80,
        "diamond",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "srPartiesOk",
        "All parties present\n& admit execution\nat SRO office?",
        "lane_sr",
        2580,
        130,
        80,
        "diamond",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "srAdmit",
        "Admit document;\ncapture photo / thumb;\nenter payment details",
        "lane_sr",
        2760,
        150,
        70,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "srRegister",
        "Attach endorsements;\nCheck & Register;\nDSC / seal (Sec. 60)",
        "lane_sr",
        3200,
        150,
        70,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "srReturn",
        "Return registered\ndocument to citizen",
        "lane_sr",
        3560,
        130,
        55,
        "rect",
        "#dae8fc",
        "#6c8ebf",
    ),
    # ── District Registrar (happy path: supporting / not invoked) ────────
    (
        "drMaster",
        "District / sub-district /\nSRO master & holiday\ncalendar (Secs. 5–7;\nRules 3, 5)",
        "lane_dr",
        400,
        160,
        70,
        "rect",
        "#e1d5e7",
        "#9673a6",
    ),
    (
        "drNotInvoked",
        "Not invoked in happy path:\nno Sec. 45-A undervaluation\n& no Stamp Act impound\nreferral from SRO",
        "lane_dr",
        2400,
        180,
        80,
        "rect",
        "#f5f5f5",
        "#999999",
    ),
]

NODE_Y_BIAS: dict[str, float] = {}

EDGES: list[tuple[str, str, str]] = [
    # Intake
    ("start", "login", ""),
    ("login", "selectService", ""),
    ("selectService", "selectSRO", ""),
    ("selectSRO", "drMaster", ""),
    ("drMaster", "enterDetails", ""),
    ("enterDetails", "sysValidate", ""),
    ("sysValidate", "previewSubmit", ""),
    ("previewSubmit", "sysCalcDuty", ""),
    ("sysCalcDuty", "srReview", ""),
    # Payment & appointment
    ("srReview", "payFees", ""),
    ("payFees", "sysRecordPay", ""),
    ("sysRecordPay", "bookSlot", ""),
    ("bookSlot", "sysConfirmSlot", ""),
    ("sysConfirmSlot", "visitSRO", ""),
    # Presentation
    ("visitSRO", "kiosk", ""),
    ("kiosk", "sysReadyPresent", ""),
    ("sysReadyPresent", "srCallParties", ""),
    ("srCallParties", "presentDoc", ""),
    ("presentDoc", "srExamine", ""),
    ("srExamine", "srStampOk", ""),
    # Happy-path confirmations (No / Yes continue; pending branches excluded)
    ("srStampOk", "srPartiesOk", "Yes\n(happy path)"),
    ("srStampOk", "drNotInvoked", "No → 45-A /\nImpound\n(out of scope)"),
    ("srPartiesOk", "srAdmit", "Yes — all present\nat SRO office"),
    # Completion
    ("srAdmit", "signEndorse", ""),
    ("signEndorse", "sysRegisters", ""),
    ("sysRegisters", "srRegister", ""),
    ("srRegister", "sysScanCert", ""),
    ("sysScanCert", "sysStatusReg", ""),
    ("sysStatusReg", "srReturn", ""),
    ("srReturn", "receiveDoc", ""),
    ("receiveDoc", "endOk", ""),
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
        '  <mxCell id="subtitle" value="Happy path — no undervaluation (45-A), no impounding, no party-appearance pending, no private attendance (Sec. 31)" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=11;fontColor=#666666;" vertex="1" parent="1">',
        f'    <mxGeometry x="{LANE_X + 650}" y="58" width="1200" height="24" as="geometry"/>',
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
        # Grey dashed style for out-of-scope edge to DR
        if tgt == "drNotInvoked":
            edge_style = (
                "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
                "html=1;fontSize=8;endArrow=classic;fontColor=#666666;dashed=1;"
                "strokeColor=#999999;"
            )
        else:
            edge_style = (
                "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
                "html=1;fontSize=9;endArrow=classic;fontColor=#333333;"
            )
        cells.append(
            f'  <mxCell id="{mx_id}"{label_attr} style="{edge_style}" edge="1" parent="1" source="{node_mx[src]}" target="{node_mx[tgt]}">'
        )
        cells.append('    <mxGeometry relative="1" as="geometry"/>')
        cells.append("  </mxCell>")

    legend_y = LANE_Y + len(LANES) * LANE_H + 20
    legend = (
        "Happy path (Sr.12 Registration + Appointment): Citizen online intake → SR sends for payment → "
        "pay SD/RF → book SRO appointment (Rules 3/5) → office presentation with all parties present → "
        "admit & register (Secs. 34–35, 58–61) → Sec. 60 certificate → return document. "
        "Excluded branches: Sec. 45-A undervaluation & Stamp Act impound (DR referral); "
        "party-appearance pending (Secs. 36–39); private attendance / Sec. 31. "
        "Sources: Document_Registration_requirement_27082026_v1.1 / 28082026_v1.1."
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
  <diagram id="reg-core-happy" name="{esc(TITLE)}">
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


def _load_font(paths, size):
    from PIL import ImageFont

    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def render_png_pillow(out_png: Path) -> None:
    """Swimlane PNG matching draw.io lane order (Part XII format)."""
    from PIL import Image, ImageDraw

    margin = 40
    title_h = 70
    lane_h = 160
    lane_label_w = 140
    width = LANE_W + margin * 2
    height = title_h + len(LANES) * lane_h + 110
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

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
    font_title = _load_font(bold_candidates, 18)
    font_small = _load_font(font_candidates, 9)
    font_lane = _load_font(bold_candidates, 11)

    draw.text((margin + 400, 12), TITLE, fill="#1a1a1a", font=font_title)
    draw.text(
        (margin + 280, 42),
        "Happy path — no 45-A undervaluation · no impound · no party-appearance pending · no Sec. 31 private attendance",
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
        # Wrap lane label
        words = label.split()
        lines_l = []
        cur = ""
        for w in words:
            trial = f"{cur} {w}".strip()
            if len(trial) > 12 and cur:
                lines_l.append(cur)
                cur = w
            else:
                cur = trial
        if cur:
            lines_l.append(cur)
        ty = y + lane_h // 2 - 7 * len(lines_l)
        for line in lines_l:
            bbox = draw.textbbox((0, 0), line, font=font_lane)
            tw = bbox[2] - bbox[0]
            draw.text(
                (margin + (lane_label_w - tw) // 2, ty),
                line,
                fill="white",
                font=font_lane,
            )
            ty += 14

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
        # Vertical hand-off when target is left/right overlapping
        if abs(sx - tx) < 40:
            sx = x1
            tx = x2
            sy = abs_pos[src][1] + abs_pos[src][3]
            ty = abs_pos[tgt][1]
            mid_y = (sy + ty) // 2
            color = "#999999" if tgt == "drNotInvoked" else "#444444"
            draw.line([(sx, sy), (sx, mid_y), (tx, mid_y), (tx, ty)], fill=color, width=1)
            draw.polygon([(tx, ty), (tx - 4, ty - 8), (tx + 4, ty - 8)], fill=color)
        else:
            mid_x = (sx + tx) // 2
            color = "#999999" if tgt == "drNotInvoked" else "#444444"
            draw.line([(sx, sy), (mid_x, sy), (mid_x, ty), (tx, ty)], fill=color, width=1)
            draw.polygon([(tx, ty), (tx - 8, ty - 4), (tx - 8, ty + 4)], fill=color)
            if label:
                clean = label.replace("\n", " ")
                draw.text(
                    (mid_x + 4, min(sy, ty) - 12),
                    clean[:40],
                    fill="#333333",
                    font=font_small,
                )

    note_y = title_h + len(LANES) * lane_h + 12
    draw.rectangle(
        [margin, note_y, margin + LANE_W, note_y + 55],
        outline="#999999",
        fill="#f5f5f5",
    )
    note1 = (
        "Happy path: Online intake → SR send-for-payment → Pay SD/RF → Book appointment → "
        "Office presentation (all parties) → Admit & Register → Sec. 60 certificate → Return document."
    )
    note2 = (
        "Excluded: Sec. 45-A undervaluation & Stamp Act impound (DR); party-appearance pending (Secs. 36–39); "
        "private attendance (Sec. 31). Actors: Citizen · System · Sub-Registrar · District Registrar."
    )
    draw.text((margin + 10, note_y + 8), note1, fill="#333333", font=font_small)
    draw.text((margin + 10, note_y + 28), note2, fill="#555555", font=font_small)

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
    for p in sorted(OUTPUT_DIR.glob(f"{STEM}*")):
        print(f"  {p.name} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
