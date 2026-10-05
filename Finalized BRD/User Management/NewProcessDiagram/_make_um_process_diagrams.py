# -*- coding: utf-8 -*-
"""Generate one vertical draw.io swimlane diagram per activity of the simplified User Management BRD.

Same visual style as the CVC Process A diagram: actors are columns, the flow runs top to bottom.
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import quoteattr

OUT_DIR = Path(__file__).resolve().parent
BRD = "BRD User Management (Simplified) v1.5"

LANE_HEADER_H = 60
ROW_H = 140
BOX_W, BOX_H = 200, 90
DIA_W, DIA_H = 200, 110
TITLE_H = 90

STYLE = {
    "task": "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;",
    "decision": "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;",
    "start": "ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;fontStyle=1;",
    "end": "ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;strokeWidth=3;fontSize=11;fontStyle=1;",
    "reject": "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=12;",
}
EDGE = ("edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;html=1;endArrow=block;endFill=1;"
        "strokeWidth=1.5;fontSize=11;labelBackgroundColor=#ffffff;")
BACK = EDGE + "dashed=1;strokeColor=#b85450;fontColor=#b85450;"
LANE_FILL = ["#dae8fc", "#d5e8d4", "#fff2cc", "#ffe6cc", "#f8cecc", "#e1d5e7", "#f5f5f5"]
LEGEND = [
    ("start", "Start"),
    ("task", "Step done by the person or system in that lane"),
    ("decision", "Check / choice"),
    ("reject", "Stopped / refused"),
    ("end", "End"),
]


def label(num: str, text: str, ref: str = "") -> str:
    head = f"<b>{num}.</b> " if num else ""
    tail = f"<br><font style='font-size:10px' color='#555555'>{ref}</font>" if ref else ""
    return f"{head}{text}{tail}"


def lane(key: str, name: str, sub: str = "", w: int = 260):
    return key, name + (f"<br><span style='font-weight:normal;font-size:11px'>{sub}</span>" if sub else ""), w


class Diagram:
    def __init__(self, stem: str, title: str, reqs: str, lanes, rows: int):
        self.stem = stem
        self.cells: list[str] = []
        self.lane_x: dict[str, int] = {}
        self.lane_w: dict[str, int] = {}
        self.nodes: dict[str, tuple[int, int, int, int]] = {}
        self.where: dict[str, tuple[str, int]] = {}
        lanes_h = LANE_HEADER_H + rows * ROW_H + 20
        x = 0
        for i, (key, text, w) in enumerate(lanes):
            self.lane_x[key], self.lane_w[key] = x, w
            self._vertex(f"lane_{key}", text,
                         f"swimlane;horizontal=1;html=1;startSize={LANE_HEADER_H};whiteSpace=wrap;"
                         f"fillColor={LANE_FILL[i % len(LANE_FILL)]};swimlaneFillColor=#fcfcfc;fontSize=13;fontStyle=1;",
                         x, TITLE_H, w, lanes_h)
            x += w
        self.width = max(x, 760)
        self.height = TITLE_H + lanes_h
        self._vertex("title",
                     f"<b style='font-size:20px'>{title}</b><br>"
                     f"<span style='font-size:12px'>{BRD} — requirements {reqs}</span>",
                     "text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;", 0, 10, self.width, 70)

    def _vertex(self, cid, value, style, x, y, w, h):
        self.cells.append(f'<mxCell id="{cid}" value={quoteattr(value)} style="{style}" vertex="1" parent="1">'
                          f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

    def node(self, cid, lane_key, row, kind, value, cx: int | None = None):
        w, h = {"decision": (DIA_W, DIA_H), "start": (64, 64), "end": (64, 64)}.get(kind, (BOX_W, BOX_H))
        centre = cx if cx is not None else self.lane_w[lane_key] // 2
        x = self.lane_x[lane_key] + centre - w // 2
        y = TITLE_H + LANE_HEADER_H + row * ROW_H + (ROW_H - h) // 2
        self.nodes[cid] = (x, y, w, h)
        self.where[cid] = (lane_key, row)
        self._vertex(cid, value, STYLE[kind], x, y, w, h)

    def cy(self, cid):
        _, y, _, h = self.nodes[cid]
        return y + h // 2

    def edge(self, src, tgt, value="", back=False, points=None, extra=None):
        if extra is None:
            sx, tx = (self.nodes[c][0] + self.nodes[c][2] // 2 for c in (src, tgt))
            if sx == tx:
                extra = "exitX=0.5;exitY=1;entryX=0.5;entryY=0;" if self.where[tgt][1] > self.where[src][1] else ""
            elif self.where[tgt][1] > self.where[src][1]:
                extra = "exitX=0.5;exitY=1;" + ("entryX=0;entryY=0.5;" if tx > sx else "entryX=1;entryY=0.5;")
            else:
                extra = ""
        pts = ""
        if points:
            pts = '<Array as="points">' + "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in points) + "</Array>"
        eid = f"e_{src}_{tgt}_{len(self.cells)}"
        self.cells.append(f'<mxCell id="{eid}" value={quoteattr(value)} style="{(BACK if back else EDGE) + extra}" '
                          f'edge="1" parent="1" source="{src}" target="{tgt}">'
                          f'<mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>')

    def loop(self, src, tgt, value, side="left"):
        """Dashed return arrow from a check back to an earlier step, routed along the side of the lane."""
        lane_key = self.where[src][0]
        if side == "left":
            x = min(self.nodes[src][0], self.nodes[tgt][0]) - 22
            extra = "exitX=0;exitY=0.5;entryX=0;entryY=0.25;"
        else:
            x = max(self.nodes[src][0] + self.nodes[src][2], self.nodes[tgt][0] + self.nodes[tgt][2]) + 22
            extra = "exitX=1;exitY=0.5;entryX=1;entryY=0.25;"
        assert self.lane_x[lane_key] < x < self.lane_x[lane_key] + self.lane_w[lane_key], (src, tgt)
        entry_y = self.nodes[tgt][1] + self.nodes[tgt][3] // 4
        self.edge(src, tgt, value, back=True, points=[(x, self.cy(src)), (x, entry_y)], extra=extra)

    def legend(self):
        y = self.height + 30
        self._vertex("legend_t", "<b>Legend</b>", "text;html=1;align=left;", 0, y, 120, 24)
        x = 0
        for i, (kind, text) in enumerate(LEGEND):
            w, h = (64, 64) if kind in ("start", "end") else (140, 56)
            self._vertex(f"legend_{i}", text, STYLE[kind], x, y + 30, w, h)
            x += w + 20
        self.height = y + 110

    def xml(self) -> str:
        return ('<mxfile host="app.diagrams.net" type="device">'
                f'<diagram id="{self.stem}" name="{self.stem}">'
                f'<mxGraphModel dx="1600" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
                f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.width + 40}" '
                f'pageHeight="{self.height + 40}" math="0" shadow="0">'
                f'<root><mxCell id="0"/><mxCell id="1" parent="0"/>{"".join(self.cells)}</root>'
                '</mxGraphModel></diagram></mxfile>')


ADMIN = lane("adm", "Authorised Administrator")
SYS = lane("sys", "Kaveri System")


def citizen_registration():
    d = Diagram("UM_4_01_Citizen_Registration", "4.1 Citizen Registration", "UM-CIT-01 to 07",
                [lane("cit", "Citizen"), SYS], rows=12)
    n = d.node
    n("s", "cit", 0, "start", "Start")
    n("c1", "cit", 1, "task", label("1", "Open Kaveri and choose Register (any time, no approval needed)", "UM-CIT-01"))
    n("c2", "cit", 2, "task", label("2", "Choose a Username", "UM-CIT-02"))
    n("c2d", "sys", 3, "decision", label("", "Is the Username free?", "UM-CIT-02, 06"))
    n("c3", "cit", 4, "task", label("3", "Enter email and mobile number (no password, no security questions)", "UM-CIT-03, 05"))
    n("c4", "sys", 5, "task", label("4", "Send an OTP to the email and to the mobile", "UM-CIT-03"))
    n("c5", "cit", 6, "task", label("5", "Enter both OTPs", "UM-CIT-03"))
    n("c5d", "sys", 7, "decision", "Both OTPs correct?")
    n("c6", "sys", 8, "task", label("6", "Create the account. The Username can never be changed", "UM-CIT-03, 07"))
    n("c7", "cit", 9, "task", label("7", "Sign in for the first time and complete Aadhaar e-KYC", "UM-CIT-04"))
    n("c7d", "sys", 10, "decision", label("", "e-KYC successful?", "UM-CIT-04"))
    n("c8", "sys", 11, "task", label("8", "Allow the citizen to use all services", "UM-CIT-04"))
    n("e", "cit", 11, "end", "End")
    e = d.edge
    e("s", "c1")
    e("c1", "c2")
    e("c2", "c2d")
    d.loop("c2d", "c2", "No — taken; system suggests other names", side="right")
    e("c2d", "c3", "Yes")
    e("c3", "c4")
    e("c4", "c5")
    e("c5", "c5d")
    d.loop("c5d", "c5", "No — try again", side="right")
    e("c5d", "c6", "Yes")
    e("c6", "c7")
    e("c7", "c7d")
    d.loop("c7d", "c7", "No — only e-KYC is shown until it succeeds", side="right")
    e("c7d", "c8", "Yes")
    e("c8", "e", extra="exitX=0;exitY=0.5;entryX=1;entryY=0.5;")
    return d


def dsr_registration():
    d = Diagram("UM_4_02_DSR_Officer_Registration", "4.2 DSR Officer Registration", "UM-DSR-01 to 08",
                [ADMIN, SYS, lane("off", "DSR Officer", w=500)], rows=11)
    n = d.node
    n("s", "adm", 0, "start", "Start")
    n("d1", "adm", 1, "task", label("1", "Enter the officer's KGID and mobile number", "UM-DSR-01, 02"))
    n("d1d", "sys", 2, "decision", label("", "Is the KGID unique?", "UM-DSR-02"))
    n("d2", "sys", 3, "task", label("2", "Verify the mobile number by OTP", "UM-DSR-02"))
    n("d3", "adm", 4, "task", label("3", "Record the officer's face or biometric details for sign-in", "UM-DSR-06"))
    n("d3d", "adm", 5, "decision", label("", "Give a post now?", "UM-DSR-03"))
    n("d4", "adm", 6, "task", label("4", "Select one or more posts (only posts with a vacancy are shown)", "UM-DSR-03, 04"))
    n("d5", "sys", 7, "task", label("5", "Create the officer (KGID is the Username) and send an SMS", "UM-DSR-02, 07"))
    n("d5d", "sys", 8, "decision", "Post given?")
    n("d6", "off", 9, "task", label("6", "Can sign in with KGID, Captcha and face / biometric", "UM-DSR-06"), cx=130)
    n("d7", "off", 9, "reject", label("7", "Cannot sign in until a post is assigned (activity 4.8)", "UM-DSR-08"), cx=370)
    n("e", "off", 10, "end", "End", cx=250)
    e = d.edge
    e("s", "d1")
    e("d1", "d1d")
    e("d1d", "d1", "No — correct the KGID", back=True, extra="exitX=0.5;exitY=0;entryX=1;entryY=0.5;")
    e("d1d", "d2", "Yes")
    e("d2", "d3")
    e("d3", "d3d")
    e("d3d", "d4", "Yes")
    e("d3d", "d5", "No — assign later", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("d4", "d5")
    e("d5", "d5d")
    e("d5d", "d6", "Yes")
    e("d5d", "d7", "No", back=True, extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("d6", "e", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("d7", "e", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    return d


def odu_registration():
    d = Diagram("UM_4_03_Other_Department_User_Registration", "4.3 Other Department User Registration",
                "UM-ODU-01 to 05", [ADMIN, SYS, lane("odu", "Other Department User")], rows=9)
    n = d.node
    n("s", "adm", 0, "start", "Start")
    n("o1", "adm", 1, "task", label("1", "Select the department", "UM-ODU-01, 02"))
    n("o2", "adm", 2, "task", label("2", "Enter Employee ID or KGID, official email and mobile", "UM-ODU-02"))
    n("o2d", "sys", 3, "decision", label("", "Official email allowed?", "UM-ODU-03"))
    n("o3", "adm", 4, "task", label("3", "Choose one Other Department role; add an End Date if needed", "UM-ODU-04, 05"))
    n("o4", "sys", 5, "task", label("4", "Create the account. Username = department code + ID (e.g. REV-12345)", "UM-ODU-02"))
    n("o5", "odu", 6, "task", label("5", "Sign in with Username, Captcha and OTP", "UM-LOG-02"))
    n("o6", "sys", 7, "task", label("6", "Stop the account automatically on the End Date (if given)", "UM-ODU-05"))
    n("e", "sys", 8, "end", "End")
    e = d.edge
    e("s", "o1")
    e("o1", "o2")
    e("o2", "o2d")
    e("o2d", "o2", "No — personal email refused", back=True, extra="exitX=0.5;exitY=0;entryX=1;entryY=0.5;")
    e("o2d", "o3", "Yes")
    e("o3", "o4")
    e("o4", "o5")
    e("o5", "o6", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("o6", "e")
    return d


def user_logins():
    d = Diagram("UM_4_04_User_Logins", "4.4 User Logins", "UM-LOG-01 to 12",
                [lane("dsr", "DSR Officer"), lane("otp", "Citizen / Other Department User"), lane("sys", "Kaveri System", w=500)],
                rows=11)
    n = d.node
    n("s", "sys", 0, "start", "Start", cx=130)
    n("l0", "sys", 1, "decision", label("", "Which type of user? (no passwords for anyone)", "UM-LOG-01"), cx=130)
    n("l1", "otp", 2, "task", label("1", "Enter Username and Captcha", "UM-LOG-02"))
    n("l2", "dsr", 2, "task", label("1", "Enter KGID and Captcha", "UM-LOG-03"))
    n("l3", "sys", 3, "task", label("2", "Send a 6-digit OTP to the registered mobile (valid 5 minutes)", "UM-LOG-02, 04"), cx=130)
    n("l4", "otp", 4, "task", label("3", "Enter the OTP", "UM-LOG-04"))
    n("l5", "dsr", 4, "task", label("2", "Give face or biometric check (no OTP)", "UM-LOG-03"))
    n("l6", "sys", 5, "decision", label("", "Check passed and not on leave?", "UM-LOG-05, 12"), cx=130)
    n("rej", "sys", 5, "reject", label("", "Refuse sign-in and show the reason. After 5 failures, lock for 15 minutes", "UM-LOG-05, 12"), cx=375)
    n("ex", "sys", 6, "end", "End", cx=375)
    n("l7", "sys", 6, "decision", label("", "DSR Officer with more than one post?", "UM-LOG-09"), cx=130)
    n("l8", "dsr", 7, "task", label("4", "Select one post", "UM-LOG-09"))
    n("l9", "sys", 8, "task", label("5", "Open the home screen. Header shows post, role and office; only that post's work is allowed", "UM-LOG-10, 11"), cx=130)
    n("l10", "sys", 9, "task", label("6", "Sign out after 10 minutes idle or 4 hours. A new sign-in closes the old one", "UM-LOG-06, 07, 08"), cx=130)
    n("e", "sys", 10, "end", "End", cx=130)
    e = d.edge
    e("s", "l0")
    e("l0", "l1", "Citizen / Other Department user")
    e("l0", "l2", "DSR Officer", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("l1", "l3", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("l3", "l4", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("l2", "l5")
    e("l4", "l6", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("l5", "l6", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    e("l6", "rej", "No", back=True, extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    e("rej", "ex")
    e("l6", "l7", "Yes")
    e("l7", "l8", "Yes", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("l7", "l9", "No — one post, selected automatically")
    e("l8", "l9", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("l9", "l10")
    e("l10", "e")
    return d


def lost_mobile():
    d = Diagram("UM_4_05_Lost_Mobile_and_Change_of_Mobile_or_Email", "4.5 Lost Mobile and Change of Mobile or Email",
                "UM-MOB-01 to 06",
                [lane("cit", "Citizen", "Lost mobile"), lane("sys", "Kaveri System"),
                 lane("usr", "Citizen or DSR Officer", "After sign-in"), lane("adm", "Authorised Administrator", "For Other Department users")],
                rows=10)
    n = d.node
    n("s", "sys", 0, "start", "Start")
    n("m0", "sys", 1, "decision", label("", "What is needed?", "UM-MOB-06"))
    n("m1", "cit", 2, "task", label("1", "Enter Username and Captcha", "UM-MOB-01"))
    n("m2", "cit", 3, "task", label("2", "Complete Aadhaar e-KYC", "UM-MOB-01"))
    n("m3", "sys", 4, "task", label("3", "Send a PIN to the registered email", "UM-MOB-01"))
    n("m4", "cit", 5, "task", label("4", "Enter the PIN and the new mobile number", "UM-MOB-01"))
    n("m5", "sys", 6, "task", label("5", "Send an OTP to the new mobile", "UM-MOB-01"))
    n("m6", "cit", 7, "task", label("6", "Enter the OTP (repeated failures lock the reset for 30 minutes)", "UM-MOB-02"))
    n("m7", "sys", 8, "task", label("7", "Update the mobile and inform the citizen by email", "UM-MOB-01"))
    n("u1", "usr", 2, "task", label("1", "Enter the new mobile (citizens can also change email)", "UM-MOB-03, 04"))
    n("u2", "usr", 3, "task", label("2", "Enter the OTP sent to the new mobile or email", "UM-MOB-03, 04"))
    n("u3", "usr", 4, "task", label("3", "Mobile or email is updated", "UM-MOB-03, 04"))
    n("a1", "adm", 2, "task", label("1", "Change the mobile or email and enter a reason", "UM-MOB-05"))
    n("a2", "adm", 3, "task", label("2", "Change is saved and recorded", "UM-MOB-05"))
    n("e", "sys", 9, "end", "End")
    e = d.edge
    e("s", "m0")
    e("m0", "m1", "Citizen lost mobile", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("m0", "u1", "Change after sign-in", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("m0", "a1", "Other Department user", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;",
      points=[(d.nodes["m0"][0] + DIA_W // 2, d.cy("m0") + 80), (d.lane_x["adm"] + 130, d.cy("m0") + 80)])
    e("m1", "m2")
    e("m2", "m3", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("m3", "m4", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("m4", "m5", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("m5", "m6", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("m6", "m7", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("m7", "e")
    e("u1", "u2")
    e("u2", "u3")
    e("u3", "e", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("a1", "a2")
    e("a2", "e", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    return d


def profile_updates():
    d = Diagram("UM_4_06_Profile_Updates", "4.6 Profile Updates", "UM-PRF-01 to 02",
                [lane("usr", "User", "Any signed-in user"), SYS], rows=5)
    n = d.node
    n("s", "usr", 0, "start", "Start")
    n("p1", "usr", 1, "task", label("1", "Sign in and open My Profile"))
    n("p2", "usr", 2, "task", label("2", "Upload a photo, or update address and other contact numbers", "UM-PRF-01, 02"))
    n("p3", "sys", 3, "task", label("3", "Save the profile details"))
    n("e", "sys", 4, "end", "End")
    e = d.edge
    e("s", "p1")
    e("p1", "p2")
    e("p2", "p3")
    e("p3", "e")
    return d


def additional_charge():
    d = Diagram("UM_4_07_Additional_Charge", "4.7 Additional Charge (after sign-in)", "UM-ADC-01 to 05",
                [lane("off", "DSR Officer"), lane("sys", "Kaveri System", w=500)], rows=8)
    n = d.node
    n("s", "off", 0, "start", "Start")
    n("a1", "off", 1, "task", label("1", "Sign in and select the post", "UM-LOG-09"))
    n("a2", "sys", 2, "task", label("2", "Look for posts directly under the officer, in the same office, that nobody holds", "UM-ADC-01, 02"), cx=130)
    n("a2d", "sys", 3, "decision", "Any such post?", cx=130)
    n("rej", "sys", 3, "reject", label("", "No additional charge is offered", "UM-ADC-01"), cx=375)
    n("a3", "off", 4, "task", label("3", "Select one post to take charge of (no order needed; one at a time)", "UM-ADC-03"))
    n("a4", "sys", 5, "task", label("4", "Switch to that post. Header shows the active post; only its work is allowed", "UM-ADC-04, 05"), cx=130)
    n("a5", "off", 6, "task", label("5", "Switch back to own post at any time, without signing out", "UM-ADC-04"))
    n("e", "off", 7, "end", "End")
    e = d.edge
    e("s", "a1")
    e("a1", "a2")
    e("a2", "a2d")
    e("a2d", "rej", "No", back=True, extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    e("a2d", "a3", "Yes")
    e("a3", "a4")
    e("a4", "a5")
    e("a5", "e")
    return d


def assigning_posts():
    d = Diagram("UM_4_08_Assigning_the_DSR_Officer_to_Posts", "4.8 Assigning the DSR Officer to Posts",
                "UM-ASG-01 to 12",
                [lane("igr", "IGR Office", "Authorised user", w=240), lane("sup", "Superior Officer", w=500),
                 lane("sys", "Kaveri System", w=500), lane("off", "DSR Officer", w=500)], rows=9)
    n = d.node
    L, R = 130, 370
    n("s", "igr", 0, "start", "Start")
    n("g1", "igr", 1, "task", label("1", "Upload the movement order for the officer", "UM-ASG-02"))
    n("g2", "sup", 2, "task", label("2", "Select the officer (only offices and posts directly under the superior)", "UM-ASG-03"), cx=250)
    n("g2d", "sup", 3, "decision", label("", "Select the process", "UM-ASG-01"), cx=250)
    n("r1", "sup", 4, "task", label("3", "<b>Transfer Out / Relieving:</b> select the post(s); enter Relieving Date, Order and Reason", "UM-ASG-08"), cx=L)
    n("r2", "sys", 5, "task", label("4", "Officer keeps the post until the end of the Relieving Date", "UM-ASG-09"), cx=L)
    n("r3", "sys", 6, "task", label("5", "After midnight, remove the officer from the post, update vacancy and end any open session", "UM-ASG-10, 11"), cx=L)
    n("r4", "off", 7, "task", label("6", "If no post is left, cannot sign in until a new post is given", "UM-ASG-12"), cx=L)
    n("t1", "sup", 4, "task", label("3", "<b>Transfer In:</b> select a post and enter the Transfer / Reporting Order", "UM-ASG-05"), cx=R)
    n("t1d", "sys", 5, "decision", label("", "Does the post have a vacancy?", "UM-ASG-04, 07"), cx=R)
    n("t2", "sys", 6, "task", label("4", "Place the officer in the post now and update the vacancy count", "UM-ASG-06"), cx=R)
    n("t3", "off", 7, "task", label("5", "Sees the new post at the next sign-in", "UM-ASG-06"), cx=R)
    n("e", "off", 8, "end", "End", cx=250)
    e = d.edge
    e("s", "g1")
    e("g1", "g2")
    e("g2", "g2d")
    e("g2d", "r1", "Transfer Out / Relieving", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("g2d", "t1", "Transfer In", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    high5, high7 = d.cy("t1d") - 78, d.cy("t3") - 72
    e("r1", "r2", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("r2", "r3")
    e("r3", "r4", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("t1", "t1d", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;",
      points=[(d.lane_x["sup"] + R, high5), (d.lane_x["sys"] + R, high5)])
    right = d.lane_x["sys"] + d.lane_w["sys"] - 14
    e("t1d", "t1", "No — post is full; blocked", back=True, extra="exitX=1;exitY=0.5;entryX=1;entryY=0.5;",
      points=[(right, d.cy("t1d")), (right, d.cy("t1"))])
    e("t1d", "t2", "Yes")
    e("t2", "t3", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;",
      points=[(d.lane_x["sys"] + R, high7), (d.lane_x["off"] + R, high7)])
    e("r4", "e", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("t3", "e", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    return d


def temporary_absence():
    d = Diagram("UM_4_09_Temporary_Absence_and_Temporary_Charge", "4.9 Temporary Absence and Temporary Charge",
                "UM-ABS-01 to 07",
                [lane("sup", "Superior Officer"), SYS, lane("abs", "Absent Officer"), lane("cov", "Covering Officer")],
                rows=9)
    n = d.node
    n("s", "sup", 0, "start", "Start")
    n("b1", "sup", 1, "task", label("1", "Record Leave, OOD or Other absence with reason, dates and optional order", "UM-ABS-01, 02"))
    n("b2", "sys", 2, "task", label("2", "Block the officer from signing in. The post does not become vacant", "UM-ABS-03, 04"))
    n("b3", "abs", 3, "task", label("3", "Cannot sign in; message shows the absence type and end date", "UM-LOG-12"))
    n("b3d", "sup", 4, "decision", label("", "Give temporary charge?", "UM-ABS-05"))
    n("b4", "sup", 5, "task", label("4", "Select another officer under the superior (may be at another office)", "UM-ABS-05"))
    n("b5", "cov", 6, "task", label("5", "Sees 'Temporary charge' at sign-in and does only that post's work", "UM-ABS-06"))
    n("b6", "sys", 7, "task", label("6", "End the absence and charge after the to-date (or earlier if cancelled)", "UM-ABS-07"))
    n("e", "sys", 8, "end", "End")
    e = d.edge
    e("s", "b1")
    e("b1", "b2")
    e("b2", "b3")
    e("b3", "b3d", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("b3d", "b4", "Yes")
    e("b3d", "b6", "No", extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;",
      points=[(d.lane_x["sup"] + 14, d.cy("b3d")), (d.lane_x["sup"] + 14, d.cy("b6"))])
    e("b4", "b5")
    e("b5", "b6", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("b6", "e")
    return d


def roles():
    d = Diagram("UM_4_10_Creating_Modifying_Roles_and_Access", "4.10 Creating / Modifying Roles and Their Access",
                "UM-ROL-01 to 10",
                [ADMIN, lane("dom", "Domain Expert"), SYS, lane("usr", "User")], rows=8)
    n = d.node
    n("s", "adm", 0, "start", "Start")
    n("r1", "adm", 1, "task", label("1", "Add, change or deactivate a role and choose its category: Citizen, DSR or Other Department", "UM-ROL-01, 03"))
    n("r2", "adm", 2, "task", label("2", "Set which modules and functions (View, Add, Edit, Approve, Sign, Print, Download) the role may use", "UM-ROL-06"))
    n("r3", "dom", 3, "task", label("3", "Confirm the starting list of roles before go-live", "UM-ROL-03"))
    n("r4", "sys", 4, "task", label("4", "Save the role and record who changed it and when", "UM-ROL-09"))
    n("r5", "adm", 5, "task", label("5", "Give roles to users of the matching category (DSR Officer: one or more; Other Department user: one)", "UM-ROL-07, 10"))
    n("r6", "usr", 6, "task", label("6", "Sees and does only what the role allows; anything else is refused and recorded", "UM-ROL-08"))
    n("e", "usr", 7, "end", "End")
    e = d.edge
    for a, b in [("s", "r1"), ("r1", "r2"), ("r2", "r3"), ("r3", "r4"), ("r5", "r6"), ("r6", "e")]:
        e(a, b)
    e("r4", "r5", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    return d


def sanctioned_posts():
    d = Diagram("UM_4_11_Creating_Modifying_Sanctioned_Posts", "4.11 Creating / Modifying Sanctioned Posts for Each Office",
                "UM-SAN-01 to 05", [ADMIN, SYS], rows=8)
    n = d.node
    n("s", "adm", 0, "start", "Start")
    n("p1", "adm", 1, "task", label("1", "Add or change a post and link it to a division", "UM-SAN-01"))
    n("p2", "adm", 2, "task", label("2", "Set which types of office the post can exist in", "UM-SAN-02"))
    n("p3", "adm", 3, "task", label("3", "Set the sanctioned strength of the post in each office", "UM-SAN-03"))
    n("p4", "sys", 4, "task", label("4", "Save and record the change", "UM-SAN-03"))
    n("p5", "sys", 5, "task", label("5", "Show sanctioned, occupied and vacant counts for every post in every office", "UM-SAN-04"))
    n("p6", "sys", 6, "task", label("6", "Allow officers to be placed only where there is a vacancy", "UM-SAN-05"))
    n("e", "sys", 7, "end", "End")
    e = d.edge
    for a, b in [("s", "p1"), ("p1", "p2"), ("p2", "p3"), ("p3", "p4"), ("p4", "p5"), ("p5", "p6"), ("p6", "e")]:
        e(a, b)
    return d


def hierarchies():
    d = Diagram("UM_4_12_Creating_Managing_Reporting_Hierarchies", "4.12 Creating / Managing Reporting Hierarchies",
                "UM-HIE-01 to 04", [ADMIN, SYS], rows=7)
    n = d.node
    n("s", "adm", 0, "start", "Start")
    n("h1", "adm", 1, "task", label("1", "Add or change an office: code, name, type and parent office", "UM-HIE-01"))
    n("h2", "adm", 2, "task", label("2", "Set the post that each post reports to (one parent post)", "UM-HIE-02"))
    n("h3", "adm", 3, "task", label("3", "Reorder, enable or disable offices and hierarchy entries when needed", "UM-HIE-03"))
    n("h4", "sys", 4, "task", label("4", "Save and record the change", "UM-HIE-03"))
    n("h5", "sys", 5, "task", label("5", "Use the hierarchies to decide what each superior can see and do", "UM-HIE-04"))
    n("e", "sys", 6, "end", "End")
    e = d.edge
    for a, b in [("s", "h1"), ("h1", "h2"), ("h2", "h3"), ("h3", "h4"), ("h4", "h5"), ("h5", "e")]:
        e(a, b)
    return d


def designations():
    d = Diagram("UM_4_13_Creating_Designations_and_Mapping_to_DSR_Officers",
                "4.13 Creating Designations and Mapping Them to DSR Officers", "UM-DSG-01 to 05",
                [ADMIN, SYS], rows=6)
    n = d.node
    n("s", "adm", 0, "start", "Start")
    n("g1", "adm", 1, "task", label("1", "Add or change a designation (code and name); enable or disable it", "UM-DSG-01"))
    n("g2", "adm", 2, "task", label("2", "Select a DSR Officer and choose a designation", "UM-DSG-02, 04"))
    n("g2d", "sys", 3, "decision", label("", "Officer or designation already mapped?", "UM-DSG-03"))
    n("g3", "sys", 4, "task", label("3", "Save the mapping and record who made it and when", "UM-DSG-05"))
    n("e", "sys", 5, "end", "End")
    e = d.edge
    e("s", "g1")
    e("g1", "g2")
    e("g2", "g2d")
    e("g2d", "g2", "Yes — not allowed (always one to one)", back=True, extra="exitX=0.5;exitY=0;entryX=1;entryY=0.5;")
    e("g2d", "g3", "No")
    e("g3", "e")
    return d


def managing_users():
    d = Diagram("UM_4_14_Managing_Users", "4.14 Managing Users", "UM-USR-01 to 06",
                [ADMIN, SYS, lane("usr", "User")], rows=6)
    n = d.node
    n("s", "adm", 0, "start", "Start")
    n("u1", "adm", 1, "task", label("1", "Search for the user by Username / KGID, type, role, office, division or status", "UM-USR-02"))
    n("u2", "adm", 2, "task", label("2", "Change, suspend or deactivate the user, or correct the Username (with a reason where needed)", "UM-USR-01, 03"))
    n("u3", "sys", 3, "task", label("3", "Save at once (no second approval) and record the action", "UM-USR-05, 06"))
    n("u4", "usr", 4, "task", label("4", "Informed by SMS / email when the account is created, suspended or deactivated", "UM-USR-04"))
    n("e", "usr", 5, "end", "End")
    e = d.edge
    for a, b in [("s", "u1"), ("u1", "u2"), ("u2", "u3"), ("u3", "u4"), ("u4", "e")]:
        e(a, b)
    return d


def migration():
    d = Diagram("UM_4_15_Moving_Citizens_from_Kaveri_2_0", "4.15 Moving Citizens from Kaveri 2.0", "UM-MIG-01 to 10",
                [lane("it", "Kaveri IT Cell"), lane("sys", "Kaveri System", w=500), lane("cit", "Citizen")], rows=10)
    n = d.node
    n("s", "it", 0, "start", "Start")
    n("m1", "it", 1, "task", label("1", "Pick Kaveri 2.0 citizens whose e-KYC is completed (others register afresh)", "UM-MIG-01"))
    n("m2", "it", 2, "task", label("2", "Do trial runs first", "UM-MIG-09"))
    n("m3", "sys", 3, "task", label("3", "Move only email ID, mobile, email and e-KYC status (no passwords)", "UM-MIG-02"), cx=130)
    n("m3d", "sys", 4, "decision", label("", "Record correct? (email ID unique, mobile valid)", "UM-MIG-07"), cx=130)
    n("rej", "sys", 4, "reject", label("", "Set aside for correction", "UM-MIG-07"), cx=375)
    n("m4", "sys", 5, "task", label("4", "Create the account: email ID becomes the Username; old records stay linked", "UM-MIG-03, 08"), cx=130)
    n("m5", "sys", 6, "task", label("5", "Send SMS / email in Kannada and English asking the citizen to activate", "UM-MIG-10"), cx=130)
    n("m6", "cit", 7, "task", label("6", "Sign in with email ID, Captcha and OTP; verify the email by OTP (no e-KYC again)", "UM-MIG-04, 05"))
    n("m7", "sys", 8, "task", label("7", "Account becomes active", "UM-MIG-05"), cx=130)
    n("e", "sys", 9, "end", "End", cx=130)
    e = d.edge
    e("s", "m1")
    e("m1", "m2")
    e("m2", "m3")
    e("m3", "m3d")
    e("m3d", "rej", "No", back=True, extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    e("m3d", "m4", "Yes")
    e("m4", "m5")
    e("m5", "m6")
    e("m6", "m7", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("m7", "e")
    return d


BUILDERS = [citizen_registration, dsr_registration, odu_registration, user_logins, lost_mobile, profile_updates,
            additional_charge, assigning_posts, temporary_absence, roles, sanctioned_posts, hierarchies,
            designations, managing_users, migration]


def main():
    for build in BUILDERS:
        d = build()
        d.legend()
        path = OUT_DIR / f"{d.stem}.drawio"
        path.write_text(d.xml(), encoding="utf-8")
        print("Wrote", path.name)


if __name__ == "__main__":
    main()
