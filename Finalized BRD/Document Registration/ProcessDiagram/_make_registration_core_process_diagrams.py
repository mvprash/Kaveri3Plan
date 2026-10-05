# -*- coding: utf-8 -*-
"""Generate vertical draw.io swimlane diagrams for BRD_Registration_Core.

Same layout and style as the CVC Guidance Value Fixation BRD diagrams
(Finalized BRD/CVCGUIDANCEVALUEFIXATION/Process Diagram/_make_process_diagrams.py):
actors are vertical lanes, the flow runs top to bottom, steps use plain language
with the legal reference in grey underneath.

Process A — Filling the registration application (27-08-2026 intake screens).
Process B — Sub-Registrar check and payment.
Process C — Appointment and registration at the Sub-Registrar office.
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import quoteattr

OUT_DIR = Path(__file__).resolve().parent

LANE_HEADER_H = 64
ROW_H = 150
BOX_W, BOX_H = 200, 100
DIA_W, DIA_H = 200, 124
TITLE_H = 90

STYLE = {
    "task": "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;",
    "ext": "rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;dashed=1;fontSize=12;",
    "decision": "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;",
    "start": "ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;fontStyle=1;",
    "end": "ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;strokeWidth=3;fontSize=11;fontStyle=1;",
    "reject": "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=12;",
    "hold": "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=12;",
}
EDGE = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;html=1;endArrow=block;endFill=1;strokeWidth=1.5;fontSize=11;labelBackgroundColor=#ffffff;"
BACK = EDGE + "dashed=1;strokeColor=#b85450;fontColor=#b85450;"
LANE_FILL = ["#dae8fc", "#d5e8d4", "#fff2cc", "#ffe6cc", "#f8cecc", "#e1d5e7", "#f5f5f5"]

RIGHT = "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
LEFT = "exitX=0;exitY=0.5;entryX=1;entryY=0.5;"
DOWN = "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
DOWN_LEFT = "exitX=0.5;exitY=1;entryX=1;entryY=0.5;"
DOWN_RIGHT = "exitX=0.5;exitY=1;entryX=0;entryY=0.5;"


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

    def node(self, cid, lane, row, kind, value, cx: int | None = None):
        """Place a node in a lane at a row; cx is the centre offset inside the lane (default: lane centre)."""
        if kind == "decision":
            w, h = DIA_W, DIA_H
        elif kind in ("start", "end"):
            w, h = 76, 76
        else:
            w, h = BOX_W, BOX_H
        centre = cx if cx is not None else self.lane_w[lane] // 2
        x = self.lane_x[lane] + centre - w // 2
        y = TITLE_H + LANE_HEADER_H + row * ROW_H + (ROW_H - h) // 2
        self.nodes[cid] = (x, y, w, h)
        self._vertex(cid, value, STYLE[kind], x, y, w, h)

    def cy(self, cid):
        _, y, _, h = self.nodes[cid]
        return y + h // 2

    def edge(self, src, tgt, value="", back=False, points=None, extra="", label_offset=None):
        pts = ""
        if points:
            pts = '<Array as="points">' + "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in points) + "</Array>"
        if label_offset:
            pts += f'<mxPoint x="{label_offset[0]}" y="{label_offset[1]}" as="offset"/>'
        eid = f"e_{src}_{tgt}_{len(self.cells)}"
        self.cells.append(
            f'<mxCell id="{eid}" value={quoteattr(value)} style="{(BACK if back else EDGE) + extra}" edge="1" parent="1" '
            f'source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>'
        )

    def loop_left(self, src, tgt, value, lane, offset=14):
        """Dashed return arrow from src back up to tgt along the left edge of a lane."""
        x = self.lane_x[lane] + offset
        self.edge(src, tgt, value, back=True,
                  points=[(x, self.cy(src)), (x, self.cy(tgt))],
                  extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;labelPosition=right;align=left;",
                  label_offset=(6, 0))

    def legend(self, items: list[tuple[str, str]]):
        y = self.height + 30
        self._vertex("legend_t", "<b>Legend</b>", "text;html=1;align=left;", 0, y, 120, 24)
        x, row_y = 0, y + 30
        for i, (kind, text) in enumerate(items):
            w = 70 if kind in ("start", "end") else 150
            h = 70 if kind in ("start", "end") else 56
            if x + w > self.width:
                x, row_y = 0, row_y + 90
            self._vertex(f"legend_{i}", text, STYLE[kind], x, row_y, w, h)
            x += w + 20
        self.height = row_y + 90

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
    ("ext", "Outside system (KSRSAC, Bhoomi, Aadhaar, Bank)"),
    ("hold", "Exception — handled in a separate process"),
    ("reject", "Refusal"),
    ("end", "End"),
]

SUBTITLE = "Registration core — Registration, Appointment and Status tracking (27-08-2026 discussion) — BRD Registration Core v1.0"


def process_a() -> Diagram:
    lanes = [
        ("cit", lane_title("Citizen / Applicant", "Person registering the document"), 270),
        ("sys", lane_title("Kaveri System"), 260),
        ("ext", lane_title("Outside systems", "KSRSAC, Bhoomi, Aadhaar"), 260),
    ]
    d = Diagram(
        "Process A - Registration Application",
        "Process A — Filling the Document Registration Application",
        SUBTITLE, lanes, rows=12,
    )
    n = d.node
    n("a_start", "cit", 0, "start", "Start")
    n("a1", "cit", 1, "task", label("1", "Log in and choose “Register a document”"))
    n("a2", "cit", 2, "task", label("2", "Answer a few simple questions about the deal (sale, gift, partition, loan …)"))
    n("a3", "sys", 2, "task", label("3", "Suggest the matching document type (article) in plain words", "Stamp Act Schedule; Reg. Act Sec. 17"))
    n("a4", "cit", 3, "decision", label("4", "Is the suggested document type correct?"))
    n("a5", "cit", 4, "task", label("5", "Choose where the property is: district, taluk, village"))
    n("a6", "ext", 4, "ext", label("6", "KSRSAC sends village details and map; Bhoomi sends survey no. and extent for farm land", "Rules 13–15"))
    n("a7", "sys", 5, "task", label("7", "Find the right Sub-Registrar office for this property", "Reg. Act Sec. 28"))
    n("a8", "cit", 6, "task", label("8", "Enter boundaries (East, West, North, South) and check the property on the map. Farm land: no size boxes", "Reg. Act Secs. 21–22"))
    n("a9", "cit", 7, "task", label("9", "Add the parties (e.g. Seller and Buyer, Donor and Receiver); gender filled from Mr / Mrs", "Reg. Act Secs. 32–33"))
    n("a10", "ext", 7, "ext", label("10", "Aadhaar sends an OTP that names this service; each party confirms"))
    n("a11", "cit", 8, "task", label("11", "Pick the property type (residential, commercial, dry, wet …). The rate is not shown"))
    n("a12", "sys", 9, "task", label("12", "Work out market value, stamp duty and registration fee", "Stamp Act Secs. 45-A, 45-B; Reg. Act Sec. 78"))
    n("a13", "cit", 10, "task", label("13", "Check the full summary (preview) and submit"))
    n("a14", "sys", 11, "task", label("14", "Give an application number and send it to the Sub-Registrar"))
    n("a_end", "ext", 11, "end", "End<br>Go to B")

    e = d.edge
    e("a_start", "a1")
    e("a1", "a2")
    e("a2", "a3", "Answers", extra=RIGHT)
    e("a3", "a4", "Suggestion", extra=DOWN_LEFT)
    d.loop_left("a4", "a2", "No — change answers", "cit")
    e("a4", "a5", "Yes")
    e("a5", "a6", "Location", extra=RIGHT)
    e("a6", "a7", "Village data", extra=DOWN_LEFT)
    e("a7", "a8", extra=DOWN_LEFT)
    e("a8", "a9")
    e("a9", "a10", "OTP request", extra=RIGHT)
    e("a10", "a11", "Verified", extra=DOWN_LEFT)
    e("a11", "a12", extra=DOWN_RIGHT)
    e("a12", "a13", "Amounts", extra=DOWN_LEFT)
    e("a13", "a14", "Submitted", extra=DOWN_RIGHT)
    e("a14", "a_end", extra=RIGHT)
    d.legend([item for item in LEGEND if item[0] not in ("hold", "reject")])
    return d


def process_b() -> Diagram:
    lanes = [
        ("cit", lane_title("Citizen / Applicant"), 250),
        ("sys", lane_title("Kaveri System"), 250),
        ("sr", lane_title("Sub-Registrar (SR)"), 520),
        ("bank", lane_title("Bank / Treasury", "Payment, e-Stamp"), 250),
    ]
    d = Diagram(
        "Process B - SR Check and Payment",
        "Process B — Sub-Registrar Check and Payment",
        SUBTITLE, lanes, rows=8,
    )
    n = d.node
    n("b_start", "sys", 0, "start", "Start<br>from A")
    n("b1", "sys", 1, "task", label("1", "Check the property and parties against the banned / attached property list", "Karnataka Sec. 22-B"))
    n("b2", "sr", 2, "task", label("2", "Open the application; check the details and the property value"), cx=120)
    n("b3", "sr", 3, "decision", label("3", "Is everything correct?"), cx=120)
    n("b3c", "cit", 3, "task", label("", "Correct only the parts marked by the SR and resubmit"))
    n("b3x", "sr", 3, "reject", label("", "Refuse with written reasons and inform the applicant", "Sec. 22-B / Sec. 71"), cx=400)
    n("b_end_x", "sr", 4, "end", "End", cx=400)
    n("b4", "sr", 4, "task", label("4", "Send to the applicant for payment"), cx=120)
    n("b5", "cit", 5, "task", label("5", "Pay stamp duty and fee online, by challan or e-Stamp", "Stamp Act Sec. 10"))
    n("b6", "bank", 5, "decision", label("6", "Payment received?"))
    n("b7", "sys", 6, "task", label("7", "Give the receipt and open appointment booking right away"))
    n("b_end", "sys", 7, "end", "End<br>Go to C")

    e = d.edge
    e("b_start", "b1")
    e("b1", "b2", "To SR queue", extra=DOWN)
    e("b2", "b3")
    e("b3", "b3c", "Needs correction", back=True, extra="exitX=0;exitY=0.3;entryX=1;entryY=0.3;")
    e("b3c", "b2", "Resubmit", extra="exitX=0.5;exitY=0;entryX=0;entryY=0.5;")
    e("b3", "b3x", "Forged / banned", back=True, extra=RIGHT)
    e("b3x", "b_end_x", extra=DOWN)
    e("b3", "b4", "Yes")
    e("b4", "b5", "Pay now", extra=DOWN)
    e("b5", "b6", "Payment", extra=RIGHT)
    below = d.cy("b5") + 66
    d.edge("b6", "b5", "No — try again", back=True,
           points=[(d.lane_x["bank"] + d.lane_w["bank"] // 2, below), (d.lane_x["cit"] + d.lane_w["cit"] // 2, below)],
           extra="exitX=0.5;exitY=1;entryX=0.5;entryY=1;")
    bank_right = d.lane_x["bank"] + d.lane_w["bank"] - 16
    e("b6", "b7", "Yes", extra="exitX=1;exitY=0.5;entryX=1;entryY=0.5;",
      points=[(bank_right, d.cy("b6")), (bank_right, d.cy("b7"))])
    e("b7", "b_end")
    d.legend([item for item in LEGEND if item[0] not in ("ext", "hold")])
    return d


def process_c() -> Diagram:
    lanes = [
        ("cit", lane_title("Citizen and Parties"), 300),
        ("sys", lane_title("Kaveri System"), 250),
        ("sr", lane_title("Sub-Registrar (SR)"), 250),
        ("dr", lane_title("District Registrar (DR)"), 250),
    ]
    d = Diagram(
        "Process C - Appointment and Registration",
        "Process C — Appointment and Registration at the Sub-Registrar Office",
        SUBTITLE, lanes, rows=14,
    )
    n = d.node
    n("c_start", "cit", 0, "start", "Start<br>from B")
    n("c0", "dr", 0, "task", label("", "Keep office working days, holidays and daily slot limits up to date", "Rules 3, 5"))
    n("c1", "cit", 1, "task", label("1", "Pick a date and time at the Sub-Registrar office"))
    n("c2", "sys", 2, "decision", label("2", "Within 4 months of signing the document?", "Sec. 23"))
    n("c2w", "cit", 2, "hold", label("", "See the late-fee warning; accept the fine or pick an earlier date", "Sec. 25; Rules 51–55"))
    n("c3", "sys", 3, "task", label("3", "Confirm the slot; send SMS and an appointment slip with QR code"))
    n("c4", "cit", 4, "decision", label("4", "Can all parties come on that day?"))
    n("c5", "cit", 5, "task", label("5", "Come to the office on the day; scan the QR code at the kiosk"))
    n("c6", "sys", 5, "task", label("6", "Mark presence and add to the SR’s queue in slot order"))
    n("c7", "sr", 6, "task", label("7", "Call the parties; note the time the document is presented", "Sec. 52"))
    n("c8", "sr", 7, "decision", label("8", "Full stamp duty paid and value not too low?", "Stamp Act Secs. 33–39, 45-A"))
    n("c8x", "dr", 7, "hold", label("", "Document held — impound / value check (separate process)"))
    n("c_end_x", "dr", 8, "end", "End")
    n("c9", "sr", 8, "decision", label("9", "All parties present and agree they signed?", "Secs. 34–35"))
    n("c9x", "sys", 8, "hold", label("", "Kept pending in the Minute Book; parties book a new date", "Rules 51–55"))
    n("c10", "sr", 9, "task", label("10", "Take photo and fingerprints of all parties", "Sec. 32A; Rule 40"))
    n("c11", "cit", 10, "task", label("11", "Parties sign the endorsements", "Secs. 58–59"))
    n("c12", "sr", 11, "task", label("12", "Click “Check and Register”; sign the certificate digitally", "Sec. 60"))
    n("c13", "sys", 12, "task", label("13", "Give the registration number, update books and index, scan the document", "Sec. 51"))
    n("c14", "sr", 13, "task", label("14", "Return the registered document and digital copy", "Sec. 61; Rules 110–118"))
    n("c_end", "cit", 13, "end", "End<br>Registered")

    e = d.edge
    e("c_start", "c1")
    e("c1", "c2", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("c2", "c2w", "No", back=True, extra=LEFT)
    e("c2w", "c3", "Accept fine", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("c2", "c3", "Yes")
    e("c0", "c3", "Office calendar", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("c3", "c4", "Booked", extra=DOWN_LEFT)
    d.loop_left("c4", "c1", "No — change date", "cit")
    e("c4", "c5", "Yes")
    e("c5", "c6", "Check-in", extra=RIGHT)
    e("c6", "c7", extra=DOWN_RIGHT)
    e("c7", "c8")
    e("c8", "c8x", "No", back=True, extra=RIGHT)
    e("c8x", "c_end_x", extra=DOWN)
    e("c8", "c9", "Yes")
    e("c9", "c9x", "No", back=True, extra=LEFT)
    cit_x = d.lane_x["cit"] + 32
    d.edge("c9x", "c1", "Book again", back=True,
           points=[(d.lane_x["sys"] + d.lane_w["sys"] // 2, d.cy("c9x") + 70), (cit_x, d.cy("c9x") + 70), (cit_x, d.cy("c1") + 20)],
           extra="exitX=0.5;exitY=1;entryX=0;entryY=0.7;")
    e("c9", "c10", "Yes")
    e("c10", "c11", extra=DOWN_LEFT)
    e("c11", "c12", extra=DOWN_RIGHT)
    e("c12", "c13", extra=DOWN_LEFT)
    e("c13", "c14", extra=DOWN_RIGHT)
    e("c14", "c_end", extra=LEFT)
    d.legend([item for item in LEGEND if item[0] not in ("ext", "reject")])
    return d


DIAGRAMS = {
    "Process_A_Registration_Application": process_a,
    "Process_B_SR_Check_and_Payment": process_b,
    "Process_C_Appointment_and_Registration": process_c,
}


def main():
    for stem, build in DIAGRAMS.items():
        path = OUT_DIR / f"{stem}.drawio"
        path.write_text(build().xml(), encoding="utf-8")
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
