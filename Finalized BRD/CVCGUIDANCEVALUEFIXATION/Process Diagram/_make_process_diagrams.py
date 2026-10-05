# -*- coding: utf-8 -*-
"""Generate vertical draw.io swimlane diagrams for BRD_CVC_Guidance_Value_Fixation_v1.7.

Actors are vertical lanes (columns) and the flow runs top to bottom.
Process A — General Revision of guidance value (Rules 5 and 7, 15 stages +
Kaveri system steps). Process B — Guidance value for a new individual project.
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import quoteattr

OUT_DIR = Path(__file__).resolve().parent

LANE_HEADER_H = 64
ROW_H = 160
BOX_W, BOX_H = 190, 100
DIA_W, DIA_H = 196, 124
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
            w, h = 70, 70
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

    def cxn(self, cid):
        x, _, w, _ = self.nodes[cid]
        return x + w // 2

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

    def legend(self, items: list[tuple[str, str]]):
        y = self.height + 30
        self._vertex("legend_t", "<b>Legend</b>", "text;html=1;align=left;", 0, y, 120, 24)
        x = 0
        for i, (kind, text) in enumerate(items):
            w = 70 if kind in ("start", "end") else 150
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
    ("ext", "Kaveri system step (added for Kaveri, not in the Rules)"),
    ("reject", "Rejection"),
    ("end", "End"),
]


def process_a() -> Diagram:
    lanes = [
        ("cvc", lane_title("Central Valuation Committee (CVC)", "Chairman: IGR"), 250),
        ("sec", lane_title("CVC Secretary", "DIGR (Valuation)"), 240),
        ("dr", lane_title("District Registrar (DR)"), 240),
        ("sc", lane_title("Market Valuation Sub-Committee", "Chairman: Tahsildar"), 240),
        ("sr", lane_title("Sub-Committee Secretary", "Sub-Registrar (SR)"), 240),
        ("pub", lane_title("Public / Citizens"), 230),
        ("sys", lane_title("Kaveri System"), 230),
    ]
    d = Diagram(
        "Process A - General Revision",
        "Process A — General Revision of Guidance Value",
        "Based on Rules 5 and 7 of the Karnataka Stamp (Central Valuation Committee) Rules, 2003 — BRD CVC Guidance Value Fixation v1.7",
        lanes, rows=21,
    )
    n = d.node
    n("a_start", "cvc", 0, "start", "Start")
    n("a1", "cvc", 1, "task", label("1", "Send instructions and rate-fixing guidelines to all Sub-Committees for next year (or to one Sub-Committee during the year)", "Rule 5(1)"))
    n("a2", "sc", 2, "task", label("2", "Announce the plan to revise rates in local newspapers and on office notice boards", "Rule 5(2)"))
    n("a3", "pub", 3, "task", label("3", "Send objections or suggestions within 15 days", "Rule 5(2)"))
    n("a4", "sr", 4, "task", label("4", "Sort the objections and suggestions and place them before the Sub-Committee", "Rule 5(2)"))
    n("a5", "sc", 5, "task", label("5", "Meet as often as needed, consider public views and decide the new rates", "Rule 5(2)"))
    n("a6", "sc", 6, "task", label("6", "Prepare the statement of average rates, village-wise and local-body-wise", "Rule 5(2)"))
    n("a7", "sc", 7, "task", label("7", "Chairman and Secretary sign the statement in CVC format, with views on objections", "Rule 5(2)"))
    n("a8", "sr", 8, "task", label("8", "Send printed booklet and soft copy to the District Registrar", "Rule 5(2)"))
    n("a9", "dr", 9, "decision", label("9", "Check statement: any mistakes or missing data?", "Rule 5(3)"))
    n("a10", "sc", 9, "task", label("10", "Correct the mistakes / add missing data and send back within 15 days", "Rule 5(3)"))
    n("a11", "dr", 10, "task", label("11", "Final review, add remarks, send a separate booklet and soft copy for each sub-district", "Rule 5(3)"))
    n("a12", "sec", 11, "task", label("12", "Check the statements and place them before the CVC", "Rule 7(1)"))
    n("a13", "cvc", 12, "task", label("13", "Discuss district-wise rates, accept or reject suggestions, record decisions in the minutes", "Rule 7(2)"))
    n("a13d", "cvc", 13, "decision", "Rates approved?")
    n("a14", "sec", 14, "task", label("14", "Certify (attest) the approved statements and send them to the DR", "Rule 7(3)"))
    n("a14b", "dr", 15, "task", label("14", "Forward to Sub-Committees; keep copies for the public at the DR office", "Rule 7(3)"))
    n("a15", "sc", 16, "task", label("15", "Display approved rates in sub-district offices and SR office; printed copies sold at CVC price", "Rule 7(3)"))
    n("a16", "cvc", 17, "ext", label("16", "Fix the date from which the new rates apply (effective date)", "Kaveri system step"))
    n("a17", "sys", 18, "ext", label("17", "Publish in the e-Gazette through DIPR / Karnataka Rajya Patra", "Kaveri system step"))
    n("a18", "sys", 19, "ext", label("18", "Start using the new rates in Kaveri from the effective date; keep old rates for history", "Kaveri system step"))
    n("a_end", "sys", 20, "end", "End")

    e = d.edge
    e("a_start", "a1")
    e("a1", "a2", "Instructions")
    e("a2", "a3", "Public notice")
    e("a3", "a4", "After 15 days")
    e("a4", "a5")
    e("a5", "a6")
    e("a6", "a7")
    e("a7", "a8")
    e("a8", "a9", "Booklet + soft copy", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("a9", "a10", "Yes", back=True, extra="exitX=1;exitY=0.3;entryX=0;entryY=0.3;")
    e("a10", "a9", "Resubmit", extra="exitX=0;exitY=0.7;entryX=1;entryY=0.7;")
    e("a9", "a11", "No")
    e("a11", "a12", "To CVC Secretary")
    e("a12", "a13")
    e("a13", "a13d")
    left = d.lane_x["cvc"] + 14
    e("a13d", "a12", "No — needs clarification", back=True,
      points=[(left, d.cy("a13d")), (left, d.cy("a12"))], extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;",
      label_offset=(80, 0))
    e("a13d", "a14", "Yes")
    e("a14", "a14b")
    e("a14b", "a15")
    e("a15", "a16")
    e("a16", "a17")
    e("a17", "a18")
    e("a18", "a_end")
    d.legend(LEGEND)
    return d


def process_b() -> Diagram:
    lanes = [
        ("cit", lane_title("Citizen / Developer", "Applicant"), 250),
        ("sys", lane_title("Kaveri System", "with ULMS"), 240),
        ("dr", lane_title("District Registrar (DR)"), 500),
        ("sec", lane_title("CVC Secretary", "DIGR (Valuation)"), 260),
        ("igr", lane_title("IGR", "Chairman, CVC"), 250),
    ]
    d = Diagram(
        "Process B - Individual Project",
        "Process B — Fixing Guidance Value for a New Individual Project",
        "Under Section 45-B of the Karnataka Stamp Act, 1957 — BRD CVC Guidance Value Fixation v1.7",
        lanes, rows=10,
    )
    n = d.node
    n("b_start", "cit", 0, "start", "Start")
    n("b1", "cit", 1, "task", label("1", "Apply online or at the DR office for the new property / project, with ULPIN, documents and fee"))
    n("b2", "sys", 2, "task", label("2", "Fetch the property boundary (map) from ULMS using the ULPIN"))
    n("b3", "dr", 3, "decision", label("3", "Check application: complete and eligible under Sec. 45-B?"), cx=118)
    n("b3r", "cit", 3, "task", label("", "Fix the missing items and resubmit"))
    n("b3x", "dr", 3, "reject", label("", "Reject with written reasons and inform the applicant"), cx=325)
    n("b_end_x", "dr", 3, "end", "End", cx=462)
    n("b4", "dr", 4, "task", label("4", "Visit the site (spot inspection) and propose the guidance value"), cx=118)
    n("b5", "sec", 5, "task", label("5", "Review the proposal using past registrations, GIS maps, RTC, khata, town-planning and developer data; finalise the value"))
    n("b5d", "sec", 6, "decision", "Proposal acceptable?")
    n("b6", "igr", 7, "decision", label("6", "Approve the final guidance value?"))
    n("b7", "igr", 8, "task", label("7", "Approve and fix the date from which the rate applies"))
    n("b8", "sys", 9, "task", label("8", "Add the approved rate to Kaveri from that date and inform the applicant"))
    n("b_end", "cit", 9, "end", "End")

    e = d.edge
    e("b_start", "b1")
    e("b1", "b2", "Application submitted")
    e("b2", "b3", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    e("b3", "b3r", "Needs changes", back=True, extra="exitX=0;exitY=0.5;entryX=1;entryY=0.5;")
    e("b3r", "b2", "Resubmit", extra="exitX=0.5;exitY=0;entryX=0;entryY=0.5;")
    e("b3", "b3x", "Not eligible", back=True, extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    e("b3x", "b_end_x", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    e("b3", "b4", "Accepted", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    e("b4", "b5", "Proposal", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    e("b5", "b5d")
    sec_left = d.lane_x["sec"] + 18
    e("b5d", "b4", "No — return with remarks", back=True,
      points=[(sec_left, d.cy("b5d")), (sec_left, d.cy("b4"))], extra="exitX=0;exitY=0.5;entryX=1;entryY=0.5;")
    e("b5d", "b6", "Yes — send to IGR")
    igr_right = d.lane_x["igr"] + d.lane_w["igr"] - 18
    e("b6", "b5", "No — return", back=True,
      points=[(igr_right, d.cy("b6")), (igr_right, d.cy("b5"))], extra="exitX=1;exitY=0.5;entryX=1;entryY=0.5;")
    e("b6", "b7", "Yes")
    e("b7", "b8")
    e("b8", "b_end", extra="exitX=0;exitY=0.5;entryX=1;entryY=0.5;")
    d.legend([item for item in LEGEND if item[0] != "ext"])
    return d


def main():
    for diagram, fname in ((process_a(), "Process_A_General_Revision.drawio"),
                           (process_b(), "Process_B_Individual_Project_Fixation.drawio")):
        path = OUT_DIR / fname
        path.write_text(diagram.xml(), encoding="utf-8")
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
