# -*- coding: utf-8 -*-
"""Generate Marriage process swimlane draw.io diagrams (BRD v1.11 alignment).

Outputs:
  Hindu_Marriage_Online.drawio
  Hindu_Marriage_Offline.drawio
  Special Marriage/Special_Marriage_Notice_Online.drawio
  Special Marriage/Special_Marriage_Notice_Offline.drawio
  Special Marriage/Special_Marriage_Registration_Intended_Marriage.drawio
  Special Marriage/Special_Marriage_Registration_Other_Forms.drawio
"""
from __future__ import annotations

import html
from dataclasses import dataclass, field
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent

LANE_H = 150
LANE_X = 40
LANE_W = 4000
LABEL_W = 120
LANE_Y = 80

MARRIAGE_TAKEN_Q = "Whether Marriage&#xa;already taken place&#xa;or not?"


@dataclass
class Node:
    id: str
    label: str
    lane: int
    x: int
    w: int = 150
    h: int = 50
    kind: str = "rect"  # rect | diamond | ellipse | document | cylinder | subprocess | step


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
        f'    <mxGeometry x="900" y="30" width="700" height="30" as="geometry"/>',
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
        y_off = max(20, (LANE_H - node.h) // 2 - 10)
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
    page_w = max(3800, max((n.x + n.w for n in spec.nodes), default=0) + LABEL_W + 200)
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


def hindu_marriage_online() -> DiagramSpec:
    return DiagramSpec(
        name="hindu-marriage-online",
        title="Hindu Marriage Online",
        lanes=["CITIZENS", "SYSTEM", "Sub Registrar"],
        nodes=[
            Node("start", "START", 0, 30, 70, 40, "ellipse"),
            Node("login", "LogOn to Portal", 0, 120, 120, 44, "step"),
            Node("newApp", "Start a new Application", 0, 260, 140, 44),
            Node("mreg", "Marriage Registration", 0, 420, 140, 44),
            Node("channel", "Hindu Marriage Online", 0, 580, 150, 44, "subprocess"),
            Node(
                "prereq",
                "Read and continue with Prerequisite for marriage&#xa;"
                "and complete declaration",
                1,
                120,
                200,
                60,
                "document",
            ),
            Node(
                "capture",
                "Captures marriage details, e-KYC / Face Authentication&#xa;"
                "on Bride, Bridegroom &amp; 3 witness details",
                1,
                360,
                230,
                70,
                "cylinder",
            ),
            Node(
                "office",
                "Select Sub-Registrar office, review summary",
                1,
                630,
                190,
                50,
                "parallelogram",
            ),
            Node(
                "forms",
                "Submit Form I (Memorandum) &amp; Form IA (Application)",
                1,
                860,
                210,
                50,
            ),
            Node("esign", "Proceed with eSign", 1, 1100, 130, 44, "document"),
            Node("srVerify", "SR Verification", 2, 1100, 120, 80, "diamond"),
            Node("payment", "Proceed for Online Payment", 1, 1340, 160, 44, "step"),
            Node(
                "srDsc",
                "SR Digitally Signs;&#xa;Form II endorsement applied",
                2,
                1540,
                170,
                60,
            ),
            Node(
                "cert",
                "Marriage certificate&#xa;(Form II-A) Issued",
                2,
                1760,
                160,
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


def hindu_marriage_offline() -> DiagramSpec:
    return DiagramSpec(
        name="hindu-marriage-offline",
        title="Hindu Marriage Offline",
        lanes=["CITIZENS", "SYSTEM", "Sub Registrar", "Data Entry Operator"],
        nodes=[
            Node("start", "START", 0, 30, 70, 40, "ellipse"),
            Node("login", "LogOn to Portal", 0, 120, 120, 44, "step"),
            Node("newApp", "Start a new Application", 0, 260, 140, 44),
            Node("mreg", "Marriage Registration", 0, 420, 140, 44),
            Node("channel", "Hindu Marriage Offline", 0, 580, 150, 44, "subprocess"),
            Node(
                "prereq",
                "Read and continue with Prerequisite for marriage&#xa;"
                "and complete declaration",
                1,
                120,
                200,
                60,
                "document",
            ),
            Node(
                "aadhaar",
                "If Aadhaar Information&#xa;Available?",
                1,
                360,
                130,
                90,
                "diamond",
            ),
            Node(
                "ekyc",
                "e-KYC / Face Authentication&#xa;Bride &amp; Bridegroom details",
                1,
                540,
                180,
                60,
                "cylinder",
            ),
            Node(
                "manual",
                "Enter Bride &amp; Bridegroom&#xa;details (manual)",
                1,
                540,
                170,
                60,
                "cylinder",
            ),
            Node(
                "capture",
                "Enters Marriage details, Bride, Bridegroom&#xa;&amp; Witness details",
                1,
                760,
                210,
                60,
                "cylinder",
            ),
            Node("srVerify1", "SR Verification&#xa;(Stage 1)", 2, 1020, 120, 80, "diamond"),
            Node(
                "payment",
                "Makes Payment and&#xa;schedule appointment",
                1,
                1180,
                170,
                50,
                "step",
            ),
            Node(
                "printout",
                "Printout taken on Form I, Form IA,&#xa;"
                "Form II (blank endorsement) &amp; Form II-A",
                1,
                1380,
                240,
                60,
                "document",
            ),
            Node("allocate", "SR allocates to DEO", 2, 1380, 140, 50),
            Node(
                "deoUpload",
                "Check the form on signature&#xa;and uploads on portal",
                3,
                1580,
                180,
                60,
            ),
            Node("srVerify2", "SR Verification&#xa;(Stage 2)", 2, 1800, 120, 80, "diamond"),
            Node(
                "srDsc",
                "SR Digitally Signs;&#xa;Form II endorsement applied",
                2,
                2000,
                170,
                60,
            ),
            Node(
                "cert",
                "Marriage certificate&#xa;(Form II-A) Issued",
                2,
                2220,
                160,
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


def special_marriage_notice_online() -> DiagramSpec:
    return DiagramSpec(
        name="special-marriage-notice-online",
        title="Special Marriage (Intended Marriage/Other Forms) Notice Generation - Online",
        lanes=["CITIZENS", "SYSTEM", "Sub Registrar"],
        nodes=[
            Node("start", "START", 0, 30, 70, 40, "ellipse"),
            Node("login", "LogOn to Portal", 0, 120, 120, 44, "step"),
            Node("newApp", "Start a new Application", 0, 260, 140, 44),
            Node("mreg", "Marriage Registration", 0, 420, 140, 44),
            Node("taken", MARRIAGE_TAKEN_Q, 0, 580, 150, 100, "diamond"),
            Node(
                "intended",
                "Special Marriage&#xa;(Intended Marriage Notice)",
                0,
                780,
                170,
                60,
                "subprocess",
            ),
            Node(
                "other",
                "Special Marriage&#xa;(Other Forms Notice)",
                0,
                780,
                170,
                60,
                "subprocess",
            ),
            Node(
                "marDetails",
                "Enter Marriage Details",
                0,
                980,
                150,
                50,
                "cylinder",
            ),
            Node(
                "prereq",
                "Read and continue with Prerequisite for marriage&#xa;"
                "and complete declaration",
                1,
                200,
                210,
                60,
                "document",
            ),
            Node(
                "ekyc",
                "e-KYC / Face Authentication&#xa;Bride &amp; Bridegroom details",
                1,
                460,
                180,
                60,
                "cylinder",
            ),
            Node(
                "review",
                "Review summary and proceed&#xa;document uploading",
                1,
                680,
                190,
                55,
            ),
            Node(
                "upload",
                "Upload Identity Proof, Photo, Age Proof,&#xa;"
                "Address Proof (Bridegroom &amp; Bride)",
                1,
                900,
                230,
                65,
                "cylinder",
            ),
            Node("srVerify", "SR Verification", 2, 900, 120, 80, "diamond"),
            Node("payment", "First Payment", 1, 1160, 110, 44, "step"),
            Node("noticeGen", "Notice Generated", 1, 1300, 120, 44, "document"),
            Node("esign", "Proceed with e-sign", 0, 1300, 120, 44, "document"),
            Node(
                "portal",
                "Marriage notice displayed in portal",
                1,
                1460,
                190,
                50,
                "document",
            ),
            Node("countdown", "30-day countdown starts", 1, 1680, 140, 44, "ellipse"),
        ],
        edges=[
            Edge("start", "login"),
            Edge("login", "newApp"),
            Edge("newApp", "mreg"),
            Edge("mreg", "taken"),
            Edge("taken", "intended", "No"),
            Edge("taken", "other", "Yes"),
            Edge("other", "marDetails"),
            Edge("intended", "prereq"),
            Edge("marDetails", "prereq"),
            Edge("prereq", "ekyc"),
            Edge("ekyc", "review"),
            Edge("review", "upload"),
            Edge("upload", "srVerify"),
            Edge("srVerify", "payment", "Approves"),
            Edge("srVerify", "prereq", "Rejects"),
            Edge("payment", "noticeGen"),
            Edge("noticeGen", "esign"),
            Edge("esign", "portal"),
            Edge("portal", "countdown"),
        ],
    )


def special_marriage_notice_offline() -> DiagramSpec:
    return DiagramSpec(
        name="special-marriage-notice-offline",
        title="Special Marriage (Intended Marriage/Other Forms) Notice Generation - Offline",
        lanes=["CITIZENS", "SYSTEM", "Sub Registrar", "FDA/SDA/DEO"],
        nodes=[
            Node("start", "START", 0, 30, 70, 40, "ellipse"),
            Node("login", "LogOn to Portal", 0, 120, 120, 44, "step"),
            Node("newApp", "Start a new Application", 0, 260, 140, 44),
            Node("mreg", "Marriage Registration", 0, 420, 140, 44),
            Node("taken", MARRIAGE_TAKEN_Q, 0, 580, 150, 100, "diamond"),
            Node(
                "intended",
                "Special Marriage&#xa;(Intended Marriage Notice)",
                0,
                780,
                170,
                60,
                "subprocess",
            ),
            Node(
                "other",
                "Special Marriage&#xa;(Other Forms Notice)",
                0,
                780,
                170,
                60,
                "subprocess",
            ),
            Node(
                "marDetails",
                "Enter Marriage Details",
                0,
                980,
                150,
                50,
                "cylinder",
            ),
            Node(
                "prereq",
                "Read and continue with Prerequisite for marriage&#xa;"
                "and complete declaration",
                1,
                200,
                210,
                60,
                "document",
            ),
            Node(
                "aadhaar",
                "If Aadhaar Information&#xa;Available?",
                1,
                460,
                130,
                90,
                "diamond",
            ),
            Node(
                "ekyc",
                "e-KYC / Face Authentication&#xa;Bride &amp; Bridegroom details",
                1,
                640,
                180,
                60,
                "cylinder",
            ),
            Node(
                "manual",
                "Enter Bride &amp; Bridegroom&#xa;details (manual)",
                1,
                640,
                170,
                60,
                "cylinder",
            ),
            Node(
                "review",
                "Review summary and proceed&#xa;document uploading",
                1,
                860,
                190,
                55,
            ),
            Node(
                "upload",
                "Upload Identity Proof, Age Proof,&#xa;"
                "Address Proof (Bridegroom &amp; Bride)",
                0,
                1080,
                220,
                60,
                "cylinder",
            ),
            Node("srVerify", "SR Verification", 2, 1080, 120, 80, "diamond"),
            Node(
                "portal",
                "Marriage notice displayed in portal",
                1,
                1260,
                180,
                50,
                "document",
            ),
            Node("payment", "First Payment", 1, 1420, 110, 44, "step"),
            Node(
                "appointment",
                "Schedules appointment with SR",
                1,
                1560,
                160,
                44,
                "step",
            ),
            Node("genNotice", "SR Generates Notice", 2, 1560, 130, 50),
            Node("selectDeo", "Selects DEO", 2, 1740, 100, 44),
            Node(
                "photo",
                "Captures photo of Bride and&#xa;Bridegroom individually",
                3,
                1900,
                180,
                60,
            ),
            Node(
                "printSign",
                "Download Notice, Print, Physical Sign,&#xa;Scan, Upload",
                3,
                2120,
                200,
                60,
                "document",
            ),
            Node(
                "paste",
                "Pastes the Form on respective&#xa;Notice Board",
                3,
                2360,
                170,
                55,
            ),
            Node("countdown", "30-day countdown starts", 3, 2580, 140, 44, "ellipse"),
        ],
        edges=[
            Edge("start", "login"),
            Edge("login", "newApp"),
            Edge("newApp", "mreg"),
            Edge("mreg", "taken"),
            Edge("taken", "intended", "No"),
            Edge("taken", "other", "Yes"),
            Edge("other", "marDetails"),
            Edge("intended", "prereq"),
            Edge("marDetails", "prereq"),
            Edge("prereq", "aadhaar"),
            Edge("aadhaar", "ekyc", "YES"),
            Edge("aadhaar", "manual", "NO"),
            Edge("ekyc", "review"),
            Edge("manual", "review"),
            Edge("review", "upload"),
            Edge("upload", "srVerify"),
            Edge("srVerify", "portal", "Approves"),
            Edge("srVerify", "prereq", "Rejects"),
            Edge("portal", "payment"),
            Edge("payment", "appointment"),
            Edge("appointment", "genNotice"),
            Edge("genNotice", "selectDeo"),
            Edge("selectDeo", "photo"),
            Edge("photo", "printSign"),
            Edge("printSign", "paste"),
            Edge("paste", "countdown"),
        ],
    )


def special_marriage_registration(
    *,
    name: str,
    title: str,
    timeline_label: str,
    ceremony_id: str,
    ceremony_label: str,
    cert_schedule: str,
) -> DiagramSpec:
    """Shared Special Marriage registration swimlane (§7.3.2.2)."""
    return DiagramSpec(
        name=name,
        title=title,
        lanes=["CITIZEN", "SYSTEM", "Sub Registrar", "FDA/SDA/DEO"],
        nodes=[
            Node("login", "Citizen Login portal", 0, 30, 140, 44),
            Node("selectNotice", "Selects Notice", 0, 200, 120, 44),
            Node("timeline", timeline_label, 0, 360, 170, 100, "diamond"),
            Node("noAction", "No Action to be allowed", 0, 580, 150, 44),
            Node("objection", "If any Objection?", 1, 360, 130, 90, "diamond"),
            Node(
                "noticeRemoved",
                "Notice removal from portal,&#xa;tagged as Objected",
                1,
                30,
                190,
                55,
                "document",
            ),
            Node("secondPayment", "Second Payment", 1, 580, 130, 44, "subprocess"),
            Node("scheduleVisit", "Schedules Visit", 1, 760, 120, 50, "cylinder"),
            Node(
                "enquiry",
                "Conducts enquiry by&#xa;summoning all parties",
                2,
                560,
                170,
                55,
            ),
            Node("updateReason", "Updates Objection Reason", 2, 760, 150, 44),
            Node("srVerify", "SR Verification", 2, 960, 120, 80, "diamond"),
            Node("assignDeo", "Assigns to DEO", 2, 1140, 120, 44),
            Node(
                "digitalSig",
                "Digital Signature",
                2,
                2720,
                130,
                55,
                "document",
            ),
            Node("jointPhoto", "Joint Photo capturing", 3, 1320, 140, 44),
            Node(
                "witnessAadhaar",
                "If Aadhaar information&#xa;Available for Witness?",
                3,
                1500,
                150,
                100,
                "diamond",
            ),
            Node(
                "ekycWitness",
                "e-KYC / Face Authentication&#xa;Witness Details",
                3,
                1700,
                170,
                60,
                "cylinder",
            ),
            Node(
                "enterWitness",
                "Enter Witness Details",
                3,
                1700,
                140,
                55,
                "cylinder",
            ),
            Node("genDeclaration", "Generates Declaration", 3, 1920, 140, 44),
            Node("signUpload", "Sign &amp; Upload Declaration", 3, 2100, 150, 44),
            Node(ceremony_id, ceremony_label, 3, 2280, 170, 55),
            Node(
                "genCert",
                f"Generates Marriage Certificate&#xa;({cert_schedule})",
                3,
                2480,
                170,
                55,
            ),
            Node(
                "captureSigns",
                "Capturing sign of Bride,&#xa;Bridegroom, Witness",
                3,
                2680,
                160,
                55,
            ),
            Node("scanCopy", "Scan signed copy", 3, 2880, 120, 44),
            Node(
                "certIssued",
                "Marriage Certificate Issued",
                0,
                3060,
                170,
                60,
                "cert",
            ),
        ],
        edges=[
            Edge("login", "selectNotice"),
            Edge("selectNotice", "timeline"),
            Edge("timeline", "noAction", "NO"),
            Edge("timeline", "objection", "YES"),
            Edge("objection", "enquiry", "YES"),
            Edge("objection", "secondPayment", "NO"),
            Edge("enquiry", "updateReason", "Valid objection"),
            Edge("updateReason", "noticeRemoved"),
            Edge("enquiry", "secondPayment", "Objection Invalid"),
            Edge("secondPayment", "scheduleVisit"),
            Edge("scheduleVisit", "srVerify"),
            Edge("srVerify", "scheduleVisit", "Rejects"),
            Edge("srVerify", "assignDeo", "Approves"),
            Edge("assignDeo", "jointPhoto"),
            Edge("jointPhoto", "witnessAadhaar"),
            Edge("witnessAadhaar", "ekycWitness", "YES"),
            Edge("witnessAadhaar", "enterWitness", "NO"),
            Edge("ekycWitness", "genDeclaration"),
            Edge("enterWitness", "genDeclaration"),
            Edge("genDeclaration", "signUpload"),
            Edge("signUpload", ceremony_id),
            Edge(ceremony_id, "genCert"),
            Edge("genCert", "captureSigns"),
            Edge("captureSigns", "scanCopy"),
            Edge("scanCopy", "digitalSig"),
            Edge("digitalSig", "certIssued"),
        ],
    )


def special_marriage_registration_intended() -> DiagramSpec:
    return special_marriage_registration(
        name="special-marriage-registration-intended",
        title="Special Marriage (Intended Marriage) Marriage Registration",
        timeline_label="Timeline &gt;= 30 days&#xa;and &lt;= 90 days?",
        ceremony_id="solemnization",
        ceremony_label="Marriage solemnization&#xa;(Sec. 12)",
        cert_schedule="Fourth Schedule",
    )


def special_marriage_registration_other_forms() -> DiagramSpec:
    return special_marriage_registration(
        name="special-marriage-registration-other-forms",
        title="Special Marriage Other Forms Marriage Registration",
        timeline_label="Timeline &gt;= 30 days?",
        ceremony_id="registration",
        ceremony_label="Marriage registration&#xa;(Chapter III Sec. 15–16)",
        cert_schedule="Fifth Schedule",
    )


SPECS: list[tuple[Path, DiagramSpec]] = [
    (OUTPUT_DIR / "Hindu_Marriage_Online.drawio", hindu_marriage_online()),
    (OUTPUT_DIR / "Hindu_Marriage_Offline.drawio", hindu_marriage_offline()),
    (
        OUTPUT_DIR / "Special Marriage" / "Special_Marriage_Notice_Online.drawio",
        special_marriage_notice_online(),
    ),
    (
        OUTPUT_DIR / "Special Marriage" / "Special_Marriage_Notice_Offline.drawio",
        special_marriage_notice_offline(),
    ),
    (
        OUTPUT_DIR
        / "Special Marriage"
        / "Special_Marriage_Registration_Intended_Marriage.drawio",
        special_marriage_registration_intended(),
    ),
    (
        OUTPUT_DIR
        / "Special Marriage"
        / "Special_Marriage_Registration_Other_Forms.drawio",
        special_marriage_registration_other_forms(),
    ),
]


def main() -> None:
    for path, spec in SPECS:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(build_drawio(spec), encoding="utf-8")
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
