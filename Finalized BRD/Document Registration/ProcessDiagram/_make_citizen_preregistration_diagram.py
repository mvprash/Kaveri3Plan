# -*- coding: utf-8 -*-
"""Generate the vertical draw.io swimlane diagram (and PNG) for the citizen
pre-registration entry process of Document Registration.

Same layout as the CVC Guidance Value Fixation process diagrams: actors are
vertical lanes and the flow runs top to bottom.
"""
from __future__ import annotations

import html
import json
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import quoteattr

OUT_DIR = Path(__file__).resolve().parent
STEM = "Citizen_PreRegistration_Entry_Process_v4"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
SCALE = 2
BORDER = 10

LANE_HEADER_H = 64
ROW_H = 160
BOX_W, BOX_H = 200, 104
DIA_W, DIA_H = 200, 124
TITLE_H = 90

STYLE = {
    "task": "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;",
    "ext": "rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;dashed=1;fontSize=12;",
    "decision": "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;",
    "start": "ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;fontStyle=1;",
    "end": "ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;strokeWidth=3;fontSize=11;fontStyle=1;",
    "reject": "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=12;",
}
EDGE = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;html=1;endArrow=block;endFill=1;strokeWidth=1.5;fontSize=11;labelBackgroundColor=#ffffff;"
BACK = EDGE + "dashed=1;strokeColor=#b85450;fontColor=#b85450;"
LANE_FILL = ["#dae8fc", "#d5e8d4", "#fff2cc", "#ffe6cc", "#f8cecc", "#e1d5e7", "#f5f5f5"]


def label(num: str, text: str, ref: str = "") -> str:
    head = f"<b>{num}.</b> " if num else ""
    tail = f"<br><font style='font-size:10px' color='#555555'>{ref}</font>" if ref else ""
    return f"{head}{text}{tail}"


def lane_title(name: str, sub: str = "") -> str:
    return name + (f"<br><span style='font-weight:normal;font-size:11px'>{sub}</span>" if sub else "")


class Diagram:
    def __init__(self, name: str, title: str, subtitle: str, lanes: list[tuple[str, str, int]], rows: int):
        self.name = name
        self.cells: list[str] = []
        self.lane_x: dict[str, int] = {}
        self.lane_w: dict[str, int] = {}
        self.nodes: dict[str, tuple[int, int, int, int]] = {}
        self.lane_centre: dict[str, int] = {}
        self.lanes_h = LANE_HEADER_H + rows * ROW_H + 20
        x = 0
        for i, (key, text, w) in enumerate(lanes):
            self.lane_x[key], self.lane_w[key] = x, w
            fill = LANE_FILL[i % len(LANE_FILL)]
            self._vertex(
                f"lane_{key}", text,
                f"swimlane;horizontal=1;html=1;startSize={LANE_HEADER_H};whiteSpace=wrap;"
                f"fillColor={fill};swimlaneFillColor=#fcfcfc;fontSize=13;fontStyle=1;",
                x, TITLE_H, w, self.lanes_h,
            )
            x += w
        self.width = x
        self.height = TITLE_H + self.lanes_h
        self._vertex(
            "title",
            f"<b style='font-size:20px'>{title}</b><br><span style='font-size:12px'>{subtitle}</span>",
            "text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;", 0, 10, self.width, 70,
        )

    def _vertex(self, cid, value, style, x, y, w, h):
        self.cells.append(
            f'<mxCell id="{cid}" value={quoteattr(value)} style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )

    def node(self, cid, lane, row, kind, value, cx: int | None = None, box_h: int | None = None):
        """Place a node in a lane at a row; cx is the centre offset inside the lane (default: lane centre)."""
        if kind == "decision":
            w, h = DIA_W, DIA_H
        elif kind in ("start", "end"):
            w, h = 70, 70
        else:
            w, h = BOX_W, box_h or BOX_H
        centre = cx if cx is not None else self.lane_centre.get(lane, self.lane_w[lane] // 2)
        x = self.lane_x[lane] + centre - w // 2
        y = TITLE_H + LANE_HEADER_H + row * ROW_H + (ROW_H - h) // 2
        self.nodes[cid] = (x, y, w, h)
        self._vertex(cid, value, STYLE[kind], x, y, w, h)

    def cy(self, cid):
        _, y, _, h = self.nodes[cid]
        return y + h // 2

    def edge(self, src, tgt, value="", back=False, points=None, extra="", label_offset=None, label_pos=0.0):
        pts = ""
        if points:
            pts = '<Array as="points">' + "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in points) + "</Array>"
        if label_offset:
            pts += f'<mxPoint x="{label_offset[0]}" y="{label_offset[1]}" as="offset"/>'
        eid = f"e_{src}_{tgt}_{len(self.cells)}"
        self.cells.append(
            f'<mxCell id="{eid}" value={quoteattr(value)} style="{(BACK if back else EDGE) + extra}" edge="1" parent="1" '
            f'source="{src}" target="{tgt}"><mxGeometry x="{label_pos}" relative="1" as="geometry">{pts}</mxGeometry></mxCell>'
        )

    def legend(self, items: list[tuple[str, str]]):
        y = self.height + 30
        self._vertex("legend_t", "<b>Legend</b>", "text;html=1;align=left;", 0, y, 120, 24)
        x = 0
        for i, (kind, text) in enumerate(items):
            w = 70 if kind in ("start", "end") else 160
            h = 70 if kind in ("start", "end") else 56
            self._vertex(f"legend_{i}", text, STYLE[kind], x, y + 30, w, h)
            x += w + 24
        self.height = y + 120

    def xml(self) -> str:
        return (
            '<mxfile host="app.diagrams.net" type="device">'
            f'<diagram id="{self.name}" name="{self.name}">'
            f'<mxGraphModel dx="1600" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
            f'fold="1" page="1" pageScale="1" pageWidth="{max(self.width, 1100) + 40}" pageHeight="{self.height + 40}" math="0" shadow="0">'
            f'<root><mxCell id="0"/><mxCell id="1" parent="0"/>{"".join(self.cells)}</root></mxGraphModel></diagram></mxfile>'
        )


LEGEND = [
    ("start", "Start"),
    ("task", "Step done by the actor in that lane"),
    ("decision", "Decision / check"),
    ("ext", "Next stage (outside this process)"),
    ("reject", "Stop / cannot continue"),
    ("end", "End"),
]


def citizen_pre_registration() -> Diagram:
    cit_w = 920
    left_cx, mid_cx, right_cx, far_cx, movable_cx = 140, 270, 400, 600, 805
    lanes = [
        ("cit", lane_title("Citizen / Applicant", "Party or document writer"), cit_w),
        ("sys", lane_title("Kaveri System", "Kaveri Online Services"), 480),
        ("ext", lane_title("External Systems", "E-Swathu, BBMP E-Aasthi, E-Aasthi, BDA, KHB, Bhoomi, Mojini, UIDAI"), 270),
        ("sro", lane_title("Registration Office", "Sub-Registrar / Admin"), 270),
    ]
    d = Diagram(
        "Citizen Pre-Registration Entry",
        "Document Registration — Citizen Pre-Registration Entry Process (v4)",
        "How a citizen prepares and submits a document registration application online in Kaveri, "
        "up to submission for scrutiny",
        lanes, rows=36,
    )
    d.lane_centre["cit"] = mid_cx
    n = d.node
    n("s", "cit", 0, "start", "Start")
    n("login", "cit", 1, "task", label("1", "Log in to Kaveri Online Services and start a new document registration application"))
    n("appno", "sys", 2, "task", label("2", "Create a unique application number"))
    n("txn", "cit", 3, "task", label("3", "Select the type of transaction (for example Sale)"))
    n("rules", "sys", 4, "task", label("4", "From the transaction type, find whether property is needed and which kind is allowed: immovable, movable or both"))
    n("prop_req", "sys", 5, "decision", label("5", "Property needed for this transaction?"))
    n("kind", "cit", 6, "decision", label("6", "Add which property? (only the allowed kind)"))
    n("movable", "cit", 6, "task", label("7", "Movable: enter the movable property details (description and value)"), cx=movable_cx)
    n("in_ka", "cit", 7, "decision", label("8", "Is the property in Karnataka?"))
    n("outside", "cit", 8, "task", label("9", "Outside Karnataka: enter only the property details, property number and property boundaries", "Court / government stays, 22-B stays and liabilities are not checked"), cx=far_cx)
    n("agri", "cit", 8, "decision", label("10", "Agriculture or non-agriculture property?"))
    n("nonagri_in", "cit", 9, "task", label("11a", "Non-agriculture: give the location (District, Taluk, Hobli, Village) and the Property ID"), cx=left_cx)
    n("agri_in", "cit", 9, "task", label("11b", "Agriculture: give the location, Survey No. and Hissa No.; say whether the full or a part extent is sold"), cx=right_cx)
    n("fetch", "ext", 10, "task", label("12", "Import the owners from the source of truth<br>Non-agriculture: E&#8209;Swathu, BBMP&nbsp;E&#8209;Aasthi, E&#8209;Aasthi, BDA, KHB<br>Agriculture: Bhoomi RTC", "Owners are saved automatically in Kaveri"), box_h=130)
    n("partial", "cit", 11, "decision", label("13", "Agriculture land sold in part?"))
    n("sketch", "ext", 12, "task", label("14", "Import the purchasers (transferees) for the sketch from Mojini", "Purchasers are saved automatically in Kaveri"))
    n("transferee", "cit", 13, "task", label("15", "Select the transferee; the sketch details are added to the property schedule"), cx=right_cx)
    n("owners", "cit", 14, "task", label("16", "Select the owners; enter boundaries, consideration amount and property numbers"))
    n("gv", "sys", 15, "task", label("17", "Calculate the guidance value of the property from the approved rates"))
    n("more_prop", "cit", 16, "decision", label("18", "Save property. Add another property?"))
    n("stays", "sys", 17, "task", label("19", "Check each immovable property in Karnataka for government / court stays, 22-B stays and liabilities", "Not checked for properties outside Karnataka"))
    n("stay22b", "sys", 18, "decision", label("20", "Any 22-B stay found?"), cx=150)
    n("stop", "sys", 18, "reject", label("", "Stop: registration cannot continue. (Court stay = warning only; liabilities are added to the duty)"), cx=370)
    n("stop_end", "sys", 19, "end", "End", cx=370)
    n("parties", "cit", 19, "task", label("21", "Party details: imported owners (sellers) and purchasers are already saved; add other parties, consenting witnesses and witnesses"))
    n("rep", "cit", 20, "task", label("22", "For each party state who acts: self, Power of Attorney holder (registered PoA is verified), guardian of a minor, or institution representative"))
    n("aadhaar", "cit", 21, "decision", label("23", "Does the person have Aadhaar?"))
    n("ekyc", "ext", 22, "task", label("24a", "UIDAI e-KYC: return name, date of birth, address and photo"))
    n("manual_id", "cit", 22, "task", label("24b", "Give Aadhaar Enrollment ID, Passport or PAN, and enter name, date of birth, phone, email and address"), cx=right_cx)
    n("more_party", "cit", 23, "decision", label("25", "Save party. All parties and witnesses added?"))
    n("fees", "sys", 24, "task", label("26", "Calculate stamp duty, surcharge, cess and registration fee under the correct Article"))
    n("exempt", "cit", 25, "decision", label("27", "Claim an exemption?"))
    n("exempt_pick", "cit", 26, "task", label("28", "Choose ONE exemption (Women 10%, Senior Citizen 20%, Physically Handicapped 30%)"), cx=right_cx)
    n("exempt_sys", "sys", 27, "task", label("29", "Reduce the payable amount, mark the claim Pending Verification and hold payment until it is approved"))
    n("recitals", "cit", 28, "task", label("30", "Enter the history of title (recitals) in order"))
    n("payment", "cit", 29, "task", label("31", "Enter consideration payment details (mode, amount, date, reference) and covenants (terms)"))
    n("draft", "sys", 30, "task", label("32", "Prepare the draft deed (PDF) for the applicant to review"))
    n("draft_ok", "cit", 31, "decision", label("33", "Draft deed correct?"))
    n("submit", "cit", 32, "task", label("34", "Submit the application for verification and approval"))
    n("sent", "sys", 33, "task", label("35", "Send the application for scrutiny and tell the applicant they will be notified"))
    n("scrutiny", "sro", 34, "ext", label("36", "Scrutiny of the application and approval of any exemption; then payment, eSign and appointment", "Next stage"))
    n("e", "sro", 35, "end", "End")

    e = d.edge
    down = "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
    loop_x = d.lane_x["cit"] + 16
    far_x = d.lane_x["cit"] + far_cx
    movable_x = d.lane_x["cit"] + movable_cx
    no_prop_x = d.lane_x["sys"] + 40
    parties_y = d.nodes["parties"][1] + d.nodes["parties"][3] // 4

    e("s", "login")
    e("login", "appno")
    e("appno", "txn")
    e("txn", "rules", "Transaction type", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("rules", "prop_req", extra=down)
    e("prop_req", "kind", "Yes", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    e("prop_req", "parties", "No — go to party details", extra="exitX=0;exitY=0.5;entryX=1;entryY=0.25;",
      points=[(no_prop_x, d.cy("prop_req")), (no_prop_x, parties_y)], label_pos=-0.85)
    e("kind", "movable", "Movable", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    e("kind", "in_ka", "Immovable", extra=down)
    e("movable", "more_prop", "Property added", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;",
      points=[(movable_x, d.cy("more_prop"))])
    e("in_ka", "outside", "No", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("in_ka", "agri", "Yes", extra=down)
    e("outside", "more_prop", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;",
      points=[(far_x, d.cy("more_prop"))])
    e("agri", "nonagri_in", "Non-agriculture", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("agri", "agri_in", "Agriculture", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("nonagri_in", "fetch", "Property ID", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;", label_pos=-0.85)
    e("agri_in", "fetch", "Survey No.", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;", label_pos=-0.8)
    e("fetch", "partial", "Owners imported", extra=down)
    e("partial", "sketch", "Yes — send sketch", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    e("sketch", "transferee", "Purchasers imported", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("partial", "owners", "No", extra=down)
    e("transferee", "owners", extra="exitX=0.5;exitY=1;entryX=0.85;entryY=0;")
    e("owners", "gv")
    e("gv", "more_prop", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    e("more_prop", "kind", "Yes — add next property", back=True,
      points=[(loop_x, d.cy("more_prop")), (loop_x, d.cy("kind"))], extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;")
    e("more_prop", "stays", "No — Next", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("stays", "stay22b", extra=down)
    e("stay22b", "stop", "Yes", back=True, extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    e("stop", "stop_end", extra=down)
    e("stay22b", "parties", "No", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("parties", "rep")
    e("rep", "aadhaar")
    e("aadhaar", "ekyc", "Yes", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("aadhaar", "manual_id", "No", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("ekyc", "more_party", "Details fetched", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("manual_id", "more_party", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    e("more_party", "rep", "No — next party", back=True,
      points=[(loop_x, d.cy("more_party")), (loop_x, d.cy("rep"))], extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;")
    e("more_party", "fees", "Yes — Next", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("fees", "exempt", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("exempt", "exempt_pick", "Yes", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("exempt_pick", "exempt_sys", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    e("exempt", "recitals", "No", extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;",
      points=[(d.lane_x["cit"] + 60, d.cy("exempt")), (d.lane_x["cit"] + 60, d.cy("recitals"))])
    e("exempt_sys", "recitals", "Next", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("recitals", "payment")
    e("payment", "draft", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("draft", "draft_ok", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("draft_ok", "recitals", "No — correct the details", back=True,
      points=[(loop_x, d.cy("draft_ok")), (loop_x, d.cy("recitals"))], extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;")
    e("draft_ok", "submit", "Yes")
    e("submit", "sent", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("sent", "scrutiny", "Submitted", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("scrutiny", "e")
    d.legend(LEGEND)
    return d


def diagram_extent(xml: str) -> tuple[int, int]:
    width = height = 0.0
    for cell in ET.fromstring(xml).iter("mxCell"):
        if cell.get("vertex") != "1":
            continue
        geo = cell.find("mxGeometry")
        if geo is None:
            continue
        x, y = float(geo.get("x", 0)), float(geo.get("y", 0))
        width = max(width, x + float(geo.get("width", 0)))
        height = max(height, y + float(geo.get("height", 0)))
    return int(width), int(height)


def export_png(xml: str) -> Path:
    """Render with the diagrams.net viewer in headless Chrome (needs internet access)."""
    diagram_w, diagram_h = diagram_extent(xml)
    cfg = html.escape(json.dumps({"xml": xml, "auto-fit": False, "resize": False, "zoom": 1,
                                  "border": BORDER, "toolbar": ""}), quote=True)
    png = OUT_DIR / f"{STEM}.png"
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / f"{STEM}.html"
        page.write_text(
            '<html><body style="margin:0;background:#ffffff">'
            f'<div class="mxgraph" data-mxgraph="{cfg}"></div>'
            '<script src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>'
            "</body></html>",
            encoding="utf-8",
        )
        subprocess.run(
            [
                str(CHROME), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                f"--force-device-scale-factor={SCALE}",
                f"--window-size={diagram_w + 2 * BORDER + 100},{diagram_h + 2 * BORDER + 40}",
                "--virtual-time-budget=20000", f"--screenshot={png}", page.as_uri(),
            ],
            check=True, capture_output=True, timeout=180,
        )
    return png


def main():
    xml = citizen_pre_registration().xml()
    drawio = OUT_DIR / f"{STEM}.drawio"
    drawio.write_text(xml, encoding="utf-8")
    print("Wrote", drawio)
    print("Wrote", export_png(xml))


if __name__ == "__main__":
    main()
