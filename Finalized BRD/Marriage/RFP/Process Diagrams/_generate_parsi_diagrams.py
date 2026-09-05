# -*- coding: utf-8 -*-
"""Generate Parsi Marriage Online/Offline process diagrams (draw.io + PNG)."""
from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path(__file__).resolve().parent
PARSI_DIR = OUTPUT_DIR / "Parsi Marriage"

LANE_H = 150
LANE_X = 40
LANE_W = 3200
LABEL_W = 120
LANE_Y = 80


@dataclass
class Node:
    id: str
    label: str
    lane: int
    x: int
    w: int = 150
    h: int = 50
    kind: str = "rect"
    y_off: int = 0


@dataclass
class Edge:
    src: str
    tgt: str
    label: str = ""


@dataclass
class DiagramSpec:
    name: str
    title: str
    lanes: list[str]
    nodes: list[Node]
    edges: list[Edge]


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def node_style(kind: str) -> str:
    base = "whiteSpace=wrap;html=1;fontSize=10;align=center;"
    styles = {
        "rect": f"rounded=1;arcSize=12;{base}fillColor=#ffffff;strokeColor=#333333;",
        "diamond": f"rhombus;{base}fillColor=#fff2cc;strokeColor=#d6b656;",
        "ellipse": f"ellipse;{base}fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1",
        "document": f"shape=document;{base}fillColor=#ffffff;strokeColor=#333333;",
        "cylinder": (
            f"shape=cylinder3;boundedLbl=1;{base}"
            f"fillColor=#f5f5f5;strokeColor=#666666;"
        ),
        "subprocess": (
            f"shape=process;whiteSpace=wrap;html=1;fontSize=10;align=center;"
            f"fillColor=#ffffff;strokeColor=#333333;"
        ),
        "step": (
            f"shape=step;perimeter=stepPerimeter;whiteSpace=wrap;html=1;"
            f"fixedSize=1;fontSize=10;fillColor=#ffffff;strokeColor=#333333;"
        ),
        "parallelogram": (
            f"shape=parallelogram;perimeter=parallelogramPerimeter;"
            f"whiteSpace=wrap;html=1;fixedSize=1;fontSize=10;"
            f"fillColor=#ffffff;strokeColor=#333333;"
        ),
        "cert": (
            f"shape=mxgraph.basic.document;whiteSpace=wrap;html=1;fontSize=10;"
            f"fillColor=#dae8fc;strokeColor=#6c8ebf;"
        ),
    }
    return styles.get(kind, styles["rect"])


def lane_style(idx: int) -> str:
    fills = ["#fff2cc", "#e1f5e0", "#dae8fc", "#f5f5f5"]
    strokes = ["#d6b656", "#82b366", "#6c8ebf", "#666666"]
    fill = fills[idx % len(fills)]
    stroke = strokes[idx % len(strokes)]
    return (
        f"swimlane;horizontal=0;whiteSpace=wrap;html=1;startSize={LABEL_W};"
        f"fillColor={fill};strokeColor={stroke};fontStyle=1;fontSize=12;align=center;"
    )


def build_drawio(spec: DiagramSpec) -> str:
    cells: list[str] = [
        '  <mxCell id="0"/>',
        '  <mxCell id="1" parent="0"/>',
        (
            f'  <mxCell id="title" value="{esc(spec.title)}" '
            f'style="text;html=1;strokeColor=none;fillColor=none;align=center;'
            f'verticalAlign=middle;fontSize=16;fontStyle=1" vertex="1" parent="1">'
        ),
        f'    <mxGeometry x="700" y="30" width="700" height="30" as="geometry"/>',
        "  </mxCell>",
    ]

    lane_ids: list[str] = []
    for i, lane_name in enumerate(spec.lanes):
        lid = str(i + 2)
        lane_ids.append(lid)
        y = LANE_Y + i * LANE_H
        cells.append(
            f'  <mxCell id="{lid}" value="{esc(lane_name)}" '
            f'style="{lane_style(i)}" vertex="1" parent="1">'
        )
        cells.append(
            f'    <mxGeometry x="{LANE_X}" y="{y}" width="{LANE_W}" '
            f'height="{LANE_H}" as="geometry"/>'
        )
        cells.append("  </mxCell>")

    node_mx: dict[str, str] = {}
    next_id = len(spec.lanes) + 2
    for node in spec.nodes:
        mx_id = str(next_id)
        node_mx[node.id] = mx_id
        next_id += 1
        parent = lane_ids[node.lane]
        y_off = max(20, (LANE_H - node.h) // 2 - 10) + node.y_off
        cells.append(
            f'  <mxCell id="{mx_id}" value="{node.label}" '
            f'style="{node_style(node.kind)}" vertex="1" parent="{parent}">'
        )
        cells.append(
            f'    <mxGeometry x="{node.x + LABEL_W}" y="{y_off}" '
            f'width="{node.w}" height="{node.h}" as="geometry"/>'
        )
        cells.append("  </mxCell>")

    for edge in spec.edges:
        mx_id = str(next_id)
        next_id += 1
        label_attr = f' value="{esc(edge.label)}"' if edge.label else ""
        cells.append(
            f'  <mxCell id="{mx_id}"{label_attr} '
            f'style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;'
            f'jettySize=auto;html=1;fontSize=9;endArrow=classic;" edge="1" parent="1" '
            f'source="{node_mx[edge.src]}" target="{node_mx[edge.tgt]}">'
        )
        cells.append('    <mxGeometry relative="1" as="geometry"/>')
        cells.append("  </mxCell>")

    page_h = LANE_Y + len(spec.lanes) * LANE_H + 60
    page_w = max(3400, max((n.x + n.w for n in spec.nodes), default=0) + LABEL_W + 200)
    body = "\n".join(cells)
    return f"""<mxfile host="app.diagrams.net" agent="Kaveri3-Plan" version="24.7.0" type="device">
  <diagram id="{esc(spec.name)}" name="{esc(spec.title)}">
    <mxGraphModel dx="2200" dy="1400" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{page_w}" pageHeight="{page_h}" math="0" shadow="0">
      <root>
{body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""


def parsi_marriage_online() -> DiagramSpec:
    return DiagramSpec(
        name="parsi-marriage-online",
        title="Parsi Marriage Online",
        lanes=["CITIZENS", "SYSTEM", "Sub Registrar"],
        nodes=[
            Node("start", "START", 0, 30, 70, 40, "ellipse"),
            Node("login", "LogOn to Portal", 0, 120, 120, 44, "step"),
            Node("newApp", "Start a new Application", 0, 260, 140, 44),
            Node("mreg", "Marriage Registration", 0, 420, 140, 44),
            Node("channel", "Parsi Marriage Online", 0, 580, 150, 44, "subprocess"),
            Node(
                "prereq",
                "Read and continue with Prerequisite for marriage&#xa;"
                "and complete declaration (Ashirvad / Sec. 3–4)",
                1,
                120,
                220,
                70,
                "document",
            ),
            Node(
                "capture",
                "Capture Schedule II particulars: marriage,&#xa;"
                "husband &amp; wife (e-KYC / Face Auth),&#xa;"
                "priest &amp; 2 Parsi witnesses",
                1,
                380,
                240,
                80,
                "cylinder",
            ),
            Node(
                "office",
                "Select Sub-Registrar office&#xa;(place of solemnization), review summary",
                1,
                660,
                210,
                60,
                "parallelogram",
            ),
            Node(
                "forms",
                "Submit Schedule II&#xa;Certificate of Marriage",
                1,
                910,
                180,
                55,
            ),
            Node("esign", "Proceed with eSign", 1, 1130, 130, 44, "document"),
            Node("srVerify", "SR Verification", 2, 1130, 120, 80, "diamond"),
            Node("payment", "Proceed for Online Payment", 1, 1360, 160, 44, "step"),
            Node(
                "srDsc",
                "SR Digitally Signs;&#xa;enter certificate in Marriage Register",
                2,
                1560,
                190,
                60,
            ),
            Node(
                "cert",
                "Registration complete;&#xa;certified extract available",
                2,
                1800,
                170,
                60,
                "cert",
            ),
        ],
        edges=[
            Edge("start", "login"),
            Edge("login", "newApp"),
            Edge("newApp", "mreg"),
            Edge("mreg", "channel"),
            Edge("channel", "prereq"),
            Edge("prereq", "capture"),
            Edge("capture", "office"),
            Edge("office", "forms"),
            Edge("forms", "esign"),
            Edge("esign", "srVerify"),
            Edge("srVerify", "payment", "Approves"),
            Edge("srVerify", "capture", "Rejects"),
            Edge("payment", "srDsc"),
            Edge("srDsc", "cert"),
        ],
    )


def parsi_marriage_offline() -> DiagramSpec:
    return DiagramSpec(
        name="parsi-marriage-offline",
        title="Parsi Marriage Offline",
        lanes=["CITIZENS", "SYSTEM", "Sub Registrar", "Data Entry Operator"],
        nodes=[
            Node("start", "START", 0, 30, 70, 40, "ellipse"),
            Node("login", "LogOn to Portal", 0, 120, 120, 44, "step"),
            Node("newApp", "Start a new Application", 0, 260, 140, 44),
            Node("mreg", "Marriage Registration", 0, 420, 140, 44),
            Node("channel", "Parsi Marriage Offline", 0, 580, 150, 44, "subprocess"),
            Node(
                "prereq",
                "Read and continue with Prerequisite for marriage&#xa;"
                "and complete declaration (Ashirvad / Sec. 3–4)",
                1,
                120,
                220,
                70,
                "document",
            ),
            Node(
                "aadhaar",
                "If Aadhaar Information&#xa;Available?",
                1,
                380,
                130,
                90,
                "diamond",
            ),
            Node(
                "ekyc",
                "e-KYC / Face Authentication&#xa;Husband &amp; Wife details",
                1,
                560,
                180,
                55,
                "cylinder",
                y_off=-38,
            ),
            Node(
                "manual",
                "Enter Husband &amp; Wife&#xa;details (manual)",
                1,
                560,
                170,
                55,
                "cylinder",
                y_off=38,
            ),
            Node(
                "capture",
                "Enter marriage, priest,&#xa;husband, wife &amp; 2 witness details&#xa;"
                "(Schedule II fields)",
                1,
                780,
                210,
                70,
                "cylinder",
            ),
            Node("srVerify1", "SR Verification&#xa;(Stage 1)", 2, 1040, 120, 80, "diamond"),
            Node(
                "payment",
                "Makes Payment and&#xa;schedule appointment",
                1,
                1200,
                170,
                50,
                "step",
            ),
            Node(
                "printout",
                "Printout of Schedule II&#xa;Certificate of Marriage",
                1,
                1410,
                180,
                55,
                "document",
            ),
            Node("allocate", "SR allocates to DEO", 2, 1410, 140, 50),
            Node(
                "deoUpload",
                "Check priest / parties / witnesses&#xa;signatures; scan &amp; upload",
                3,
                1620,
                200,
                60,
            ),
            Node("srVerify2", "SR Verification&#xa;(Stage 2)", 2, 1860, 120, 80, "diamond"),
            Node(
                "srDsc",
                "SR Digitally Signs;&#xa;enter certificate in Marriage Register",
                2,
                2060,
                190,
                60,
            ),
            Node(
                "cert",
                "Registration complete;&#xa;certified extract available",
                2,
                2300,
                170,
                60,
                "cert",
            ),
        ],
        edges=[
            Edge("start", "login"),
            Edge("login", "newApp"),
            Edge("newApp", "mreg"),
            Edge("mreg", "channel"),
            Edge("channel", "prereq"),
            Edge("prereq", "aadhaar"),
            Edge("aadhaar", "ekyc", "YES"),
            Edge("aadhaar", "manual", "NO"),
            Edge("ekyc", "capture"),
            Edge("manual", "capture"),
            Edge("capture", "srVerify1"),
            Edge("srVerify1", "payment", "Approves"),
            Edge("srVerify1", "capture", "Rejects"),
            Edge("payment", "printout"),
            Edge("printout", "allocate"),
            Edge("allocate", "deoUpload"),
            Edge("deoUpload", "srVerify2"),
            Edge("srVerify2", "srDsc", "Approves"),
            Edge("srVerify2", "deoUpload", "Rejects"),
            Edge("srDsc", "cert"),
        ],
    )


# --- PNG swimlane renderer (BRD-ready) ---

LANE_COLORS = [
    ((255, 242, 204), (214, 182, 86)),
    ((225, 245, 224), (130, 179, 102)),
    ((218, 232, 252), (108, 142, 191)),
    ((245, 245, 245), (102, 102, 102)),
]


def _font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> list[str]:
    text = text.replace("&#xa;", "\n").replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")
    lines: list[str] = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = f"{cur} {w}"
            if draw.textlength(trial, font=font) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def render_png(spec: DiagramSpec, out_path: Path) -> None:
    pad = 24
    title_h = 48
    lane_h = 130
    label_w = 110
    scale = 1.0
    # Compute content width from nodes
    max_x = max(n.x + n.w for n in spec.nodes) + 80
    width = int(label_w + max_x * scale + pad * 2)
    height = title_h + len(spec.lanes) * lane_h + pad * 2

    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    title_font = _font(20, bold=True)
    lane_font = _font(12, bold=True)
    node_font = _font(10)
    edge_font = _font(9)

    # Title
    tw = draw.textlength(spec.title, font=title_font)
    draw.text(((width - tw) / 2, 12), spec.title, fill=(30, 30, 30), font=title_font)

    lane_top = title_h + 8
    # Lanes
    for i, name in enumerate(spec.lanes):
        y0 = lane_top + i * lane_h
        fill, stroke = LANE_COLORS[i % len(LANE_COLORS)]
        draw.rectangle(
            [pad, y0, width - pad, y0 + lane_h],
            fill=fill + (255,),
            outline=stroke + (255,),
            width=2,
        )
        draw.rectangle(
            [pad, y0, pad + label_w, y0 + lane_h],
            fill=fill + (255,),
            outline=stroke + (255,),
            width=2,
        )
        lines = _wrap(draw, name, lane_font, label_w - 16)
        lh = 14
        ty = y0 + (lane_h - len(lines) * lh) / 2
        for li, line in enumerate(lines):
            lw = draw.textlength(line, font=lane_font)
            draw.text(
                (pad + (label_w - lw) / 2, ty + li * lh),
                line,
                fill=(40, 40, 40),
                font=lane_font,
            )

    # Node positions
    positions: dict[str, tuple[float, float, float, float]] = {}
    for node in spec.nodes:
        y0 = lane_top + node.lane * lane_h
        x = pad + label_w + node.x * scale
        y = y0 + (lane_h - node.h) / 2 + node.y_off
        w, h = node.w * scale, node.h
        positions[node.id] = (x, y, w, h)

        label = (
            node.label.replace("&#xa;", "\n")
            .replace("&amp;", "&")
            .replace("&gt;", ">")
            .replace("&lt;", "<")
        )
        if node.kind == "ellipse":
            draw.ellipse([x, y, x + w, y + h], fill=(218, 232, 252), outline=(108, 142, 191), width=2)
        elif node.kind == "diamond":
            cx, cy = x + w / 2, y + h / 2
            pts = [(cx, y), (x + w, cy), (cx, y + h), (x, cy)]
            draw.polygon(pts, fill=(255, 242, 204), outline=(214, 182, 86), width=2)
        else:
            fill = (218, 232, 252) if node.kind == "cert" else (255, 255, 255)
            outline = (108, 142, 191) if node.kind == "cert" else (51, 51, 51)
            draw.rounded_rectangle(
                [x, y, x + w, y + h], radius=8, fill=fill, outline=outline, width=2
            )

        lines = _wrap(draw, label, node_font, w - 12)
        lh = 12
        ty = y + (h - len(lines) * lh) / 2
        for li, line in enumerate(lines):
            lw = draw.textlength(line, font=node_font)
            draw.text((x + (w - lw) / 2, ty + li * lh), line, fill=(20, 20, 20), font=node_font)

    def center(nid: str) -> tuple[float, float]:
        x, y, w, h = positions[nid]
        return x + w / 2, y + h / 2

    def right(nid: str) -> tuple[float, float]:
        x, y, w, h = positions[nid]
        return x + w, y + h / 2

    def left(nid: str) -> tuple[float, float]:
        x, y, w, h = positions[nid]
        return x, y + h / 2

    for edge in spec.edges:
        sx, sy = right(edge.src)
        tx, ty = left(edge.tgt)
        # Reject loops go back leftward — draw curved below
        if tx < sx - 20:
            mid_y = max(sy, ty) + 36
            path = [(sx, sy), (sx + 12, sy), (sx + 12, mid_y), (tx - 12, mid_y), (tx - 12, ty), (tx, ty)]
            draw.line(path, fill=(80, 80, 80), width=2)
            # arrow
            draw.polygon([(tx, ty), (tx - 8, ty - 5), (tx - 8, ty + 5)], fill=(80, 80, 80))
            if edge.label:
                lw = draw.textlength(edge.label, font=edge_font)
                draw.text(
                    ((sx + tx) / 2 - lw / 2, mid_y - 14),
                    edge.label,
                    fill=(120, 40, 40),
                    font=edge_font,
                )
        else:
            # Orthogonal: horizontal then vertical then horizontal
            mid_x = (sx + tx) / 2
            path = [(sx, sy), (mid_x, sy), (mid_x, ty), (tx, ty)]
            draw.line(path, fill=(80, 80, 80), width=2)
            draw.polygon([(tx, ty), (tx - 8, ty - 5), (tx - 8, ty + 5)], fill=(80, 80, 80))
            if edge.label:
                lw = draw.textlength(edge.label, font=edge_font)
                draw.text(
                    (mid_x - lw / 2, (sy + ty) / 2 - 12),
                    edge.label,
                    fill=(40, 80, 40),
                    font=edge_font,
                )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    print(f"Wrote {out_path} ({img.size[0]}x{img.size[1]})")


def main() -> None:
    PARSI_DIR.mkdir(parents=True, exist_ok=True)
    specs = [
        (PARSI_DIR / "Parsi_Marriage_Online.drawio", parsi_marriage_online()),
        (PARSI_DIR / "Parsi_Marriage_Offline.drawio", parsi_marriage_offline()),
    ]
    for path, spec in specs:
        path.write_text(build_drawio(spec), encoding="utf-8")
        print(f"Wrote {path}")
        render_png(spec, path.with_suffix(".drawio.png"))


if __name__ == "__main__":
    main()
