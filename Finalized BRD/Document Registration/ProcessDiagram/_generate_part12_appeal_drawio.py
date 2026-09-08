#!/usr/bin/env python3
"""Generate Classic Part XII (Secs. 71–77) Registration Appeal swimlane diagram.

Outputs (under Finalized BRD/Document Registration/ProcessDiagram):
  - Registration_Appeal_Part_XII.drawio
  - Registration_Appeal_Part_XII.mmd
  - Registration_Appeal_Part_XII.png  (via mermaid-cli when available;
    otherwise a Pillow fallback swimlane PNG)
"""
from __future__ import annotations

import html
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

OUTPUT_DIR = Path(__file__).resolve().parent
TITLE = "Registration Appeal – Classic Part XII (Secs. 71–77)"
STEM = "Registration_Appeal_Part_XII"

LANES = [
    ("lane_citizen", "Citizen", "#fff2cc", "#d6b656"),
    ("lane_system", "System", "#e1f5e0", "#82b366"),
    ("lane_sr", "Sub-Registrar", "#dae8fc", "#6c8ebf"),
    ("lane_dr", "District Registrar", "#e1d5e7", "#9673a6"),
    ("lane_court", "Civil Court", "#f8cecc", "#b85450"),
]

LANE_Y = 90
LANE_H = 140
LANE_X = 40
LANE_W = 3400
LABEL_W = 120

# (id, label, lane, x, w, h, kind, fill, stroke)
NODES = [
    # Citizen
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
        "getRefusalCopy",
        "Obtains refusal order\n/ Book 2 copy (Sec. 71)",
        "lane_citizen",
        560,
        150,
        50,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "choosePath",
        "Denial of\nexecution?",
        "lane_citizen",
        740,
        110,
        70,
        "diamond",
        "#ffffff",
        "#000000",
    ),
    (
        "fileAppeal72",
        "Sec. 72 appeal to DR\nwithin 30 days\n(refusal copy + original)",
        "lane_citizen",
        900,
        160,
        60,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "fileApp73",
        "Sec. 73 application\nto DR within 30 days\n(verified like plaint)",
        "lane_citizen",
        900,
        160,
        60,
        "rect",
        "#ffe6cc",
        "#d79b00",
    ),
    (
        "presentAfterOrder",
        "Present document again\nwithin 30 days of\nDR / Court order",
        "lane_citizen",
        1980,
        150,
        60,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "decideSuit",
        "File Sec. 77\nsuit ≤ 30 days?",
        "lane_citizen",
        2180,
        120,
        70,
        "diamond",
        "#ffffff",
        "#000000",
    ),
    (
        "fileSuit",
        "Institute civil suit\n(Sec. 77)",
        "lane_citizen",
        2360,
        130,
        50,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "noSuit",
        "No suit filed",
        "lane_citizen",
        2360,
        110,
        40,
        "rect",
        "#f5f5f5",
        "#666666",
    ),
    (
        "presentAfterDecree",
        "Present within 30 days\nof Court decree",
        "lane_citizen",
        2900,
        140,
        50,
        "rect",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "receiveRegistered",
        "Receives registered\ndocument",
        "lane_citizen",
        3180,
        120,
        50,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    ("endOk", "End\n(Registered)", "lane_citizen", 3340, 90, 50, "ellipse", "#d5e8d4", "#82b366"),
    (
        "endRefused",
        "End\n(Finally refused)",
        "lane_citizen",
        2520,
        110,
        50,
        "ellipse",
        "#f8cecc",
        "#b85450",
    ),
    # System
    (
        "sysBook2",
        "Record refusal in Book 2;\nupdate status = Refused;\nnotify citizen;\ngenerate copy",
        "lane_system",
        360,
        170,
        70,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysValidateAppeal",
        "Validate ≤ 30 days;\nregister Sec. 72 appeal;\nschedule DR hearing",
        "lane_system",
        1100,
        160,
        70,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysValidate73",
        "Validate ≤ 30 days;\nregister Sec. 73 application;\nlist for Sec. 74 enquiry",
        "lane_system",
        1100,
        160,
        70,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysBook2_76",
        "Record Sec. 76 refusal\nin Book 2; notify citizen;\ncopy on demand",
        "lane_system",
        1980,
        160,
        70,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysCheck30",
        "Verify presentation\nwithin 30 days of\norder / decree",
        "lane_system",
        2160,
        140,
        70,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "sysEffectDate",
        "Effect as of original\npresentation date\n(Sec. 75)",
        "lane_system",
        3040,
        140,
        70,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    # Sub-Registrar
    (
        "srExamine",
        "Examine document &\nstatutory compliance",
        "lane_sr",
        110,
        150,
        55,
        "rect",
        "#dae8fc",
        "#6c8ebf",
    ),
    (
        "srDecide",
        "Admit to\nregistration?",
        "lane_sr",
        290,
        110,
        70,
        "diamond",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "srRegisterDirect",
        "Admit & register\ndocument",
        "lane_sr",
        440,
        120,
        50,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "endOkDirect",
        "End\n(Registered)",
        "lane_citizen",
        440,
        100,
        50,
        "ellipse",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "srRefuse71",
        "Sec. 71 refusal order;\nreasons in Book 2;\nendorse; copy on demand\n(except wrong jurisdiction)",
        "lane_sr",
        360,
        180,
        80,
        "rect",
        "#f8cecc",
        "#b85450",
    ),
    (
        "srRegister75",
        "Register as ordered\n(Sec. 75 / decree);\nendorsements & certificate",
        "lane_sr",
        2900,
        160,
        70,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    # District Registrar
    (
        "drHear72",
        "Hear Sec. 72 appeal\n(Rules 175–180)",
        "lane_dr",
        1320,
        140,
        60,
        "rect",
        "#e1d5e7",
        "#9673a6",
    ),
    (
        "drEnquiry74",
        "Sec. 74 enquiry:\n(a) executed?\n(b) requirements met?",
        "lane_dr",
        1320,
        150,
        70,
        "rect",
        "#e1d5e7",
        "#9673a6",
    ),
    (
        "drDecide",
        "Order\nregistration?",
        "lane_dr",
        1540,
        110,
        70,
        "diamond",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "drOrder75",
        "Sec. 75 — Order to\nregister; communicate",
        "lane_dr",
        1720,
        140,
        60,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "drRefuse76",
        "Sec. 76 — Refusal order;\nreasons in Book 2",
        "lane_dr",
        1720,
        140,
        60,
        "rect",
        "#f8cecc",
        "#b85450",
    ),
    # Civil Court
    (
        "courtHear",
        "Try Sec. 77 suit",
        "lane_court",
        2520,
        130,
        50,
        "rect",
        "#f8cecc",
        "#b85450",
    ),
    (
        "courtDecide",
        "Decree directs\nregistration?",
        "lane_court",
        2700,
        120,
        70,
        "diamond",
        "#fff2cc",
        "#d6b656",
    ),
    (
        "courtDecreeYes",
        "Decree: register\nthe document",
        "lane_court",
        2880,
        130,
        50,
        "rect",
        "#d5e8d4",
        "#82b366",
    ),
    (
        "courtDismiss",
        "Dismiss suit /\nuphold refusal",
        "lane_court",
        2880,
        130,
        50,
        "rect",
        "#f8cecc",
        "#b85450",
    ),
]

# Vertical offsets within lane for parallel branches (fraction of LANE_H from top of content)
NODE_Y_BIAS: dict[str, float] = {
    # upper branch = Sec 72 appeal
    "fileAppeal72": 0.12,
    "sysValidateAppeal": 0.12,
    "drHear72": 0.12,
    # lower branch = Sec 73 application
    "fileApp73": 0.52,
    "sysValidate73": 0.52,
    "drEnquiry74": 0.48,
    # suit yes vs no
    "fileSuit": 0.12,
    "noSuit": 0.55,
    "endRefused": 0.52,
    "courtDismiss": 0.55,
    "courtDecreeYes": 0.12,
    "presentAfterDecree": 0.12,
}

EDGES: list[tuple[str, str, str]] = [
    ("start", "presentDoc", ""),
    ("presentDoc", "srExamine", ""),
    ("srExamine", "srDecide", ""),
    ("srDecide", "srRegisterDirect", "Yes"),
    ("srDecide", "srRefuse71", "No"),
    ("srRegisterDirect", "endOkDirect", ""),
    ("receiveRegistered", "endOk", ""),
    ("srRefuse71", "sysBook2", ""),
    ("sysBook2", "getRefusalCopy", ""),
    ("getRefusalCopy", "choosePath", ""),
    # Sec 72 path (No = not denial of execution)
    ("choosePath", "fileAppeal72", "No — other ground\n(Sec. 72)"),
    ("fileAppeal72", "sysValidateAppeal", ""),
    ("sysValidateAppeal", "drHear72", ""),
    ("drHear72", "drDecide", ""),
    # Sec 73 path (Yes = denial of execution)
    ("choosePath", "fileApp73", "Yes — denial\n(Sec. 73)"),
    ("fileApp73", "sysValidate73", ""),
    ("sysValidate73", "drEnquiry74", ""),
    ("drEnquiry74", "drDecide", ""),
    # DR decision
    ("drDecide", "drOrder75", "Yes"),
    ("drDecide", "drRefuse76", "No"),
    ("drOrder75", "presentAfterOrder", ""),
    ("drRefuse76", "sysBook2_76", ""),
    ("sysBook2_76", "decideSuit", ""),
    # After order to register
    ("presentAfterOrder", "sysCheck30", ""),
    ("sysCheck30", "srRegister75", ""),
    ("srRegister75", "sysEffectDate", ""),
    ("sysEffectDate", "receiveRegistered", ""),
    # Suit branch
    ("decideSuit", "fileSuit", "Yes"),
    ("decideSuit", "noSuit", "No"),
    ("noSuit", "endRefused", ""),
    ("fileSuit", "courtHear", ""),
    ("courtHear", "courtDecide", ""),
    ("courtDecide", "courtDecreeYes", "Yes"),
    ("courtDecide", "courtDismiss", "No"),
    ("courtDecreeYes", "presentAfterDecree", ""),
    ("presentAfterDecree", "sysCheck30", ""),
    ("courtDismiss", "endRefused", ""),
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
        f'    <mxGeometry x="{LANE_X + 900}" y="30" width="700" height="30" as="geometry"/>',
        "  </mxCell>",
        f'  <mxCell id="subtitle" value="Registration Act, 1908 — Refusal to Register &amp; Appeal (excludes Karnataka Secs. 22-B/C/D)" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=11;fontColor=#666666;" vertex="1" parent="1">',
        f'    <mxGeometry x="{LANE_X + 800}" y="58" width="900" height="24" as="geometry"/>',
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

    # Legend
    legend_y = LANE_Y + len(LANES) * LANE_H + 20
    cells.append(
        f'  <mxCell id="{next_id}" value="Legend / notes: Sec. 71 SR refusal (Book 2) → Sec. 72 appeal (other grounds) or Sec. 73 application (denial of execution) → Sec. 74 enquiry → Sec. 75 order to register (present ≤30 days; effect from original date) or Sec. 76 DR refusal → Sec. 77 civil suit ≤30 days. Wrong-jurisdiction refusal is outside Sec. 71 appeal path." style="text;html=1;strokeColor=#999999;fillColor=#f5f5f5;align=left;verticalAlign=middle;fontSize=10;spacingLeft=8;spacingRight=8;" vertex="1" parent="1">'
    )
    cells.append(
        f'    <mxGeometry x="{LANE_X}" y="{legend_y}" width="{LANE_W}" height="50" as="geometry"/>'
    )
    cells.append("  </mxCell>")

    body = "\n".join(cells)
    page_h = legend_y + 80
    return f"""<mxfile host="app.diagrams.net" agent="Kaveri3-Plan" version="24.7.0" type="device">
  <diagram id="reg-appeal-part12" name="{esc(TITLE)}">
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
    """Fallback swimlane PNG if mermaid-cli / drawio export unavailable."""
    from PIL import Image, ImageDraw, ImageFont

    margin = 40
    title_h = 70
    lane_h = 150
    lane_label_w = 130
    width = LANE_W + margin * 2
    height = title_h + len(LANES) * lane_h + 90
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
        font_lane = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
    except OSError:
        font_title = font = font_small = font_lane = ImageFont.load_default()

    draw.text((margin + 400, 16), TITLE, fill="#1a1a1a", font=font_title)
    draw.text(
        (margin + 350, 44),
        "Registration Act, 1908 — Secs. 71–77 (Classic Part XII)",
        fill="#555555",
        font=font_small,
    )

    lane_top = {lid: title_h + i * lane_h for i, (lid, *_) in enumerate(LANES)}
    for i, (lid, label, fill, stroke) in enumerate(LANES):
        y = lane_top[lid]
        # lane background
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
        # vertical label
        tw = draw.textbbox((0, 0), label, font=font_lane)[2]
        draw.text(
            (margin + 20, y + lane_h // 2 - 6),
            label,
            fill="white",
            font=font_lane,
        )

    # node absolute positions
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
        # text
        lines = label.split("\n")
        ty = ay + max(4, (h - 12 * len(lines)) // 2)
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_small)
            tw = bbox[2] - bbox[0]
            draw.text((ax + (w - tw) // 2, ty), line, fill="#111111", font=font_small)
            ty += 12

    def center(box):
        ax, ay, w, h = box
        return ax + w // 2, ay + h // 2

    for src, tgt, label in EDGES:
        if src not in abs_pos or tgt not in abs_pos:
            continue
        x1, y1 = center(abs_pos[src])
        x2, y2 = center(abs_pos[tgt])
        # exit right of source / enter left of target when possible
        sx = abs_pos[src][0] + abs_pos[src][2]
        sy = y1
        tx = abs_pos[tgt][0]
        ty = y2
        mid_x = (sx + tx) // 2
        draw.line([(sx, sy), (mid_x, sy), (mid_x, ty), (tx, ty)], fill="#444444", width=1)
        # arrow head
        draw.polygon([(tx, ty), (tx - 8, ty - 4), (tx - 8, ty + 4)], fill="#444444")
        if label:
            clean = label.replace("\n", " ")
            draw.text((mid_x + 4, min(sy, ty) - 12), clean, fill="#333333", font=font_small)

    note_y = title_h + len(LANES) * lane_h + 10
    draw.rectangle(
        [margin, note_y, margin + LANE_W, note_y + 45],
        outline="#999999",
        fill="#f5f5f5",
    )
    draw.text(
        (margin + 10, note_y + 8),
        "Sec. 71 SR refusal (Book 2) → Sec. 72 appeal (other grounds) OR Sec. 73 application (denial of execution) → "
        "Sec. 74 enquiry → Sec. 75 order (present ≤30 days; effect from original date) OR Sec. 76 DR refusal → Sec. 77 suit ≤30 days.",
        fill="#333333",
        font=font_small,
    )
    draw.text(
        (margin + 10, note_y + 24),
        "Actors: Citizen · System · Sub-Registrar · District Registrar · Civil Court. Excludes Karnataka Secs. 22-B / 22-C / 22-D.",
        fill="#555555",
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
            "3200",
            "-s",
            "2",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if r.returncode == 0 and out_png.exists():
            print(f"Wrote mermaid PNG: {out_png}")
            return True
        print("mermaid-cli failed:", r.stderr[-500:] if r.stderr else r.stdout[-500:])
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
    # Authoritative swimlane PNG matching draw.io lane order
    render_png_pillow(png_path)

    print("Done. Files:")
    for p in sorted(OUTPUT_DIR.glob(f"{STEM}.*")):
        print(f"  {p.name} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
