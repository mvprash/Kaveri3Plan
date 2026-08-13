"""Generate cleaner C4-style architecture diagrams (PNG) for Hindu Marriage HLD."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(r"E:\MVP\Kaveri 3.0\Source Code\Kaveri 3 Plan\ArchitectureDiagrams")
OUT.mkdir(parents=True, exist_ok=True)

FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"

PERSON = ("#08427B", "#FFFFFF")
SYSTEM = ("#1168BD", "#FFFFFF")
EXT = ("#8A8A8A", "#FFFFFF")
CONTAINER = ("#438DD5", "#FFFFFF")
COMPONENT = ("#85BBF0", "#0B2C4A")
BOUNDARY = "#666666"
BG = "#F7F9FC"
ARROW = "#2A2A2A"
MUTED = "#445566"


def fnt(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def rr(draw, box, fill, outline, width=2, radius=12):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def center(draw, xy, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((xy[0] - w / 2, xy[1] - h / 2), text, font=font, fill=fill)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def box(draw, x, y, w, h, title, subtitle="", body="", fill="#1168BD", fg="#FFFFFF", outline=None, radius=12):
    outline = outline or "#0A4F8A"
    rr(draw, (x, y, x + w, y + h), fill=fill, outline=outline, width=2, radius=radius)
    cx = x + w / 2
    ty = y + 12
    center(draw, (cx, ty + 8), title, fnt(14, True), fg)
    ty += 26
    if subtitle:
        center(draw, (cx, ty + 6), subtitle, fnt(10), fg)
        ty += 18
    if body:
        for line in wrap(draw, body, fnt(10), w - 20):
            center(draw, (cx, ty + 6), line, fnt(10), fg)
            ty += 14
    return (x, y, x + w, y + h)


def person(draw, cx, cy, label, detail=""):
    draw.ellipse((cx - 12, cy - 28, cx + 12, cy - 4), fill=PERSON[0], outline="#062F57", width=2)
    draw.rounded_rectangle((cx - 18, cy - 2, cx + 18, cy + 30), radius=16, fill=PERSON[0], outline="#062F57", width=2)
    center(draw, (cx, cy + 46), label, fnt(12, True), "#083B66")
    if detail:
        center(draw, (cx, cy + 62), detail, fnt(9), MUTED)


def arrow(draw, x1, y1, x2, y2, label="", label_bg=True):
    draw.line((x1, y1, x2, y2), fill=ARROW, width=2)
    ang = math.atan2(y2 - y1, x2 - x1)
    ah = 9
    p1 = (x2 - ah * math.cos(ang - 0.45), y2 - ah * math.sin(ang - 0.45))
    p2 = (x2 - ah * math.cos(ang + 0.45), y2 - ah * math.sin(ang + 0.45))
    draw.polygon([(x2, y2), p1, p2], fill=ARROW)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 8
        font = fnt(9)
        lines = wrap(draw, label, font, 140)
        tw = max(draw.textlength(ln, font=font) for ln in lines)
        th = 12 * len(lines)
        if label_bg:
            draw.rectangle((mx - tw / 2 - 3, my - th / 2 - 2, mx + tw / 2 + 3, my + th / 2 + 2), fill="#FFFFFF", outline="#E0E0E0")
        for i, ln in enumerate(lines):
            center(draw, (mx, my - th / 2 + 6 + i * 12), ln, font, ARROW)


def header(draw, w, title, subtitle):
    draw.rectangle((0, 0, w, 64), fill="#0B3A67")
    center(draw, (w / 2, 24), title, fnt(20, True), "#FFFFFF")
    center(draw, (w / 2, 46), subtitle, fnt(12), "#D6E8F8")


def legend(draw, x, y, items):
    draw.text((x, y), "Legend", font=fnt(11, True), fill="#333")
    yy = y + 18
    for color, label in items:
        draw.rounded_rectangle((x, yy, x + 18, yy + 12), radius=3, fill=color)
        draw.text((x + 26, yy - 2), label, font=fnt(10), fill="#333")
        yy += 18


def gen_context():
    W, H = 1700, 980
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, W, "C4 Level 1 — System Context", "Hindu Marriage Registration · Kaveri 3.0")

    # Boundary for org systems/people only (externals outside)
    rr(d, (40, 90, 980, 900), fill="#FFFFFF", outline=BOUNDARY, width=2, radius=8)
    d.text((55, 100), "Karnataka Registration Department / e-Governance boundary", font=fnt(11, True), fill=BOUNDARY)

    # People row
    people = [
        (150, 200, "Citizen", "Applicant"),
        (360, 200, "Sub-Registrar", "Registrar"),
        (570, 200, "DEO", "Offline upload"),
        (780, 200, "IGSR / Admin", "Oversight / MIS"),
    ]
    for cx, cy, lab, det in people:
        person(d, cx, cy, lab, det)

    # System of interest
    box(
        d,
        180,
        360,
        620,
        150,
        "Kaveri 3.0",
        "[Software System]",
        "Hindu Marriage Registration (Online & Offline) — HMA 1955 / Karnataka Rules 1966",
        fill=SYSTEM[0],
        fg=SYSTEM[1],
        outline="#0A4F8A",
    )

    # Internal note
    box(
        d,
        180,
        560,
        620,
        90,
        "Includes Hindu Marriage domain + shared platform services",
        "[Logical]",
        "Identity, Masters, Payment orchestration, Docs, Notify, Audit, Signing adapters",
        fill="#E8F1FA",
        fg="#0B3A67",
        outline="#1168BD",
    )

    legend(
        d,
        60,
        700,
        [
            (PERSON[0], "Person"),
            (SYSTEM[0], "Software system"),
            (EXT[0], "External system"),
        ],
    )

    # External systems (right, outside boundary)
    d.text((1040, 100), "External systems", font=fnt(12, True), fill=BOUNDARY)
    externals = [
        (1020, 140, "Payment Gateway / Treasury", "Fee collection · Form VI"),
        (1020, 260, "eSign Provider", "Citizen eSign (Online)"),
        (1020, 380, "DSC / Signing Service", "SR digital signature"),
        (1020, 500, "Aadhaar / eKYC", "Identity (if approved)"),
        (1020, 620, "SMS / Email Gateway", "Alerts EN + KN"),
        (1020, 740, "DigiLocker", "Form II-A push [TBD]"),
    ]
    for x, y, t, b in externals:
        box(d, x, y, 620, 90, t, "[External System]", b, fill=EXT[0], fg=EXT[1], outline="#666")

    # People -> system
    arrow(d, 150, 270, 320, 360, "Uses portal")
    arrow(d, 360, 270, 400, 360, "Scrutiny / DSC")
    arrow(d, 570, 270, 520, 360, "Upload scans")
    arrow(d, 780, 270, 700, 360, "MIS / oversight")

    # System -> externals
    arrow(d, 800, 400, 1020, 185, "Collect fee")
    arrow(d, 800, 420, 1020, 305, "eSign Form 1A")
    arrow(d, 800, 440, 1020, 425, "Apply SR DSC")
    arrow(d, 800, 460, 1020, 545, "Verify identity")
    arrow(d, 800, 500, 1020, 665, "Send alerts")
    arrow(d, 800, 520, 1020, 785, "Push certificate")

    path = OUT / "C4_L1_System_Context.png"
    img.save(path, "PNG")
    print("Wrote", path)


def gen_containers():
    W, H = 1900, 1180
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, W, "C4 Level 2 — Container Diagram", "Kaveri 3.0 · Hindu Marriage Registration")

    rr(d, (30, 80, 1870, 1140), fill="#FFFFFF", outline=BOUNDARY, width=2, radius=8)
    d.text((45, 90), "Kaveri 3.0 Platform", font=fnt(12, True), fill=BOUNDARY)

    # Actors
    person(d, 90, 200, "Citizen")
    person(d, 90, 400, "SR / DEO")
    person(d, 90, 600, "Admin")

    # UIs
    box(d, 180, 140, 210, 100, "Citizen Portal", "[Web App]", "Online & Offline wizard", fill=CONTAINER[0])
    box(d, 180, 340, 210, 100, "Officer Workbench", "[Web App]", "SR queues + DEO console", fill=CONTAINER[0])
    box(d, 180, 540, 210, 100, "Admin / MIS UI", "[Web App]", "Reports & config", fill=CONTAINER[0])

    # Gateway + BFFs
    box(d, 460, 320, 220, 120, "API Gateway", "[Gateway]", "AuthZ, WAF, rate limit, TLS", fill=CONTAINER[0])
    box(d, 740, 140, 200, 95, "Citizen BFF", "[API]", "UI aggregation", fill=CONTAINER[0])
    box(d, 740, 330, 200, 95, "Officer BFF", "[API]", "SR + DEO APIs", fill=CONTAINER[0])
    box(d, 740, 520, 200, 95, "Admin BFF", "[API]", "MIS / admin APIs", fill=CONTAINER[0])

    # Domain
    rr(d, (980, 110, 1480, 760), fill="#F0F7FF", outline="#1168BD", width=2, radius=8)
    d.text((995, 120), "Hindu Marriage domain", font=fnt(11, True), fill="#1168BD")

    domain = [
        (1000, 150, "Workflow Orchestrator", "Online / Offline FSM"),
        (1240, 150, "Application Intake", "Parties & witnesses"),
        (1000, 270, "Verification Service", "Online / S1 / S2"),
        (1240, 270, "Payment & Fee", "PG + Form VI"),
        (1000, 390, "Document & Forms", "PDF, scans, AV"),
        (1240, 390, "Appointment", "Offline slots"),
        (1000, 510, "Register & Certificate", "Serial, II / II-A"),
        (1240, 510, "eSign / DSC Adapters", "Signing integrations"),
        (1000, 630, "MIS Reporting", "Channel MIS, Form III"),
        (1240, 630, "Integration Gateway", "External I/O façade"),
    ]
    for x, y, t, b in domain:
        box(d, x, y, 220, 95, t, "[Microservice]", b, fill=CONTAINER[0])

    # Data stores (right of domain, not overlapping)
    rr(d, (1520, 110, 1840, 430), fill="#F5FAFC", outline="#3F6F8A", width=2, radius=8)
    d.text((1535, 120), "Data stores", font=fnt(11, True), fill="#3F6F8A")
    box(d, 1540, 150, 280, 80, "PostgreSQL (HA)", "[Database]", "DB-per-service", fill="#3F6F8A")
    box(d, 1540, 250, 280, 80, "Redis", "[Cache]", "Locks / slots / session", fill="#3F6F8A")
    box(d, 1540, 350, 280, 80, "Object Store", "[Blob]", "Photos, scans, PDFs", fill="#3F6F8A")

    # Shared platform
    rr(d, (180, 800, 1840, 1100), fill="#F5F5F5", outline="#888", width=2, radius=8)
    d.text((195, 810), "Shared platform containers", font=fnt(11, True), fill="#555")
    shared = [
        (200, 850, "Identity / IdP", "SSO, RBAC, MFA"),
        (470, 850, "Master Data", "Offices, fees, holidays"),
        (740, 850, "Notification", "SMS / Email EN+KN"),
        (1010, 850, "Audit Store", "Immutable events"),
        (1280, 850, "Event Bus", "Kafka / equivalent"),
        (1550, 850, "Secrets Vault", "Keys & credentials"),
    ]
    for x, y, t, b in shared:
        box(d, x, y, 250, 90, t, "[Platform]", b, fill="#5B8C5A", outline="#3E6B3D")

    # Also put object store note already above; add second row note
    box(d, 200, 970, 520, 90, "Document Object Store (platform)", "[S3-compatible]", "Shared with Document & Forms service", fill="#5B8C5A", outline="#3E6B3D")
    box(d, 760, 970, 520, 90, "Observability stack", "[Ops]", "OpenTelemetry, Prometheus, ELK", fill="#5B8C5A", outline="#3E6B3D")

    # Arrows
    arrow(d, 90, 250, 180, 190, "HTTPS")
    arrow(d, 90, 450, 180, 390, "HTTPS")
    arrow(d, 90, 650, 180, 590, "HTTPS")
    arrow(d, 390, 190, 460, 360, "")
    arrow(d, 390, 390, 460, 380, "")
    arrow(d, 390, 590, 460, 420, "")
    arrow(d, 680, 380, 740, 185, "")
    arrow(d, 680, 380, 740, 375, "")
    arrow(d, 680, 380, 740, 565, "")
    arrow(d, 940, 185, 1000, 195, "REST")
    arrow(d, 940, 375, 1000, 315, "REST")
    arrow(d, 940, 565, 1000, 675, "REST")
    arrow(d, 1460, 200, 1520, 190, "")
    arrow(d, 1460, 430, 1520, 290, "")
    arrow(d, 1460, 560, 1520, 390, "")

    path = OUT / "C4_L2_Containers.png"
    img.save(path, "PNG")
    print("Wrote", path)


def gen_components():
    W, H = 1800, 1120
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, W, "C4 Level 3 — Component Diagram", "Hindu Marriage domain · key components")

    rr(d, (30, 80, 1770, 1080), fill="#FFFFFF", outline=BOUNDARY, width=2, radius=8)
    d.text((45, 90), "Zoom-in: Hindu Marriage Registration components", font=fnt(12, True), fill=BOUNDARY)

    # External containers
    box(d, 50, 140, 200, 80, "Citizen BFF", "[Container]", "Intake / pay / print", fill=EXT[0], outline="#666")
    box(d, 50, 280, 200, 80, "Officer BFF", "[Container]", "Verify / DEO / DSC", fill=EXT[0], outline="#666")
    box(d, 50, 420, 200, 80, "Ext. Adapters", "[Container]", "PG · eSign · DSC · SMS", fill=EXT[0], outline="#666")

    # Component groups
    groups = [
        (280, 120, "Intake components", [
            (290, 150, "Channel & Prerequisite", "Ack + Online/Offline"),
            (540, 150, "Application Aggregate", "Marriage / parties / ×3 witnesses"),
            (790, 150, "Validation Rules", "Age, date, Sec.5 declarations"),
        ]),
        (280, 280, "Workflow components", [
            (290, 310, "Workflow Engine", "HMA_ONLINE / HMA_OFFLINE"),
            (540, 310, "Status Projector", "§7.6 tracker read-model"),
            (790, 310, "Rework Router", "S1→citizen; S2→DEO"),
        ]),
        (280, 440, "Scrutiny & Offline evidence", [
            (290, 470, "Scrutiny Decision", "Stage-tagged Approve/Reject"),
            (540, 470, "Refusal Order Gen", "Written order PDF"),
            (790, 470, "DEO Checklist", "Signature completeness"),
        ]),
        (280, 600, "Fee, appointment, documents", [
            (290, 630, "Fee Calculator", "Schedule + RD48"),
            (540, 630, "Payment Saga", "Pay + appointment (Offline)"),
            (790, 630, "Slot Manager", "Hold / confirm / release"),
            (1040, 630, "Form Template Engine", "Form I / IA / II print"),
            (1290, 630, "Scan Ingest + AV", "Versioned uploads"),
            (1540, 630, "eSign Session Mgr", "Artefact + retry"),
        ]),
        (280, 780, "Register & certificate", [
            (290, 810, "Register Allocator", "Serial / page / volume"),
            (540, 810, "Certificate Issuer", "Form II-A + QR/seal"),
            (790, 810, "DSC Session Mgr", "Expiry gate before issue"),
        ]),
    ]

    for gx, gy, title, items in groups:
        # group label only
        d.text((gx, gy), title, font=fnt(11, True), fill="#1168BD")
        for x, y, t, b in items:
            box(d, x, y, 230, 85, t, "[Component]", b, fill=COMPONENT[0], fg=COMPONENT[1], outline="#4A90C8")

    # Stores
    rr(d, (1100, 120, 1740, 560), fill="#F5FAFC", outline="#3F6F8A", width=2, radius=8)
    d.text((1115, 130), "Owned stores / bus", font=fnt(11, True), fill="#3F6F8A")
    stores = [
        (1120, 160, "Application DB", "Intake owned"),
        (1120, 260, "Workflow DB + Redis", "State, locks, timers"),
        (1120, 360, "Document Object Store", "Photos, scans, PDFs"),
        (1120, 460, "Register DB (permanent)", "Rule 10(2) retention"),
        (1430, 160, "Payment DB", "Intents & receipts"),
        (1430, 260, "Appointment DB", "Slots & bookings"),
        (1430, 360, "Audit / Event Bus", "Append-only + Kafka"),
        (1430, 460, "MIS Warehouse", "Async projections"),
    ]
    for x, y, t, b in stores:
        box(d, x, y, 280, 80, t, "[Store]", b, fill="#3F6F8A")

    # Key arrows
    arrow(d, 250, 180, 290, 190, "")
    arrow(d, 250, 320, 290, 350, "")
    arrow(d, 520, 190, 540, 190, "")
    arrow(d, 770, 190, 790, 190, "")
    arrow(d, 405, 235, 405, 310, "submit")
    arrow(d, 405, 395, 405, 470, "decision")
    arrow(d, 405, 555, 405, 630, "approve→pay")
    arrow(d, 770, 670, 790, 670, "")
    arrow(d, 1020, 670, 1040, 670, "")
    arrow(d, 1270, 670, 1290, 670, "")
    arrow(d, 1520, 670, 1540, 670, "Online")
    arrow(d, 405, 715, 405, 810, "after DSC")
    arrow(d, 770, 850, 790, 850, "sign")

    arrow(d, 1020, 190, 1100, 200, "persist")
    arrow(d, 1020, 350, 1100, 300, "state")
    arrow(d, 1520, 715, 1570, 540, "events")
    arrow(d, 870, 850, 1120, 500, "commit")

    path = OUT / "C4_L3_Components.png"
    img.save(path, "PNG")
    print("Wrote", path)


def gen_deployment():
    W, H = 1600, 920
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, W, "C4 — Deployment View", "Primary + DR · Karnataka SDC hosting (illustrative)")

    box(d, 50, 100, 220, 80, "Users", "[Persons]", "Citizen / SR / DEO / Admin", fill=PERSON[0])
    box(d, 330, 100, 220, 80, "WAF / Edge", "[Infrastructure]", "TLS termination", fill=EXT[0], outline="#666")

    # Primary
    rr(d, (50, 220, 760, 860), fill="#FFFFFF", outline="#1168BD", width=3, radius=8)
    d.text((70, 235), "Primary site (SDC)", font=fnt(13, True), fill="#1168BD")
    box(d, 80, 280, 300, 80, "API Gateway Cluster", "[K8s / APIM]", "HA", fill=CONTAINER[0])
    box(d, 410, 280, 300, 80, "BFF Pods", "[K8s HPA]", "Stateless", fill=CONTAINER[0])
    box(d, 80, 390, 300, 80, "Domain Microservices", "[K8s]", "Intake…Certificate", fill=CONTAINER[0])
    box(d, 410, 390, 300, 80, "Workers", "[K8s Jobs]", "PDF, Form III, recon", fill=CONTAINER[0])
    box(d, 80, 500, 300, 80, "PostgreSQL HA", "[Database]", "OLTP + register", fill="#3F6F8A")
    box(d, 410, 500, 300, 80, "Redis + Kafka", "[Data plane]", "Locks / events", fill="#3F6F8A")
    box(d, 80, 610, 630, 80, "Object Store (Primary)", "[S3-compatible]", "Scans, photos, signed PDFs", fill="#3F6F8A")
    box(d, 80, 720, 630, 80, "Observability", "[Ops]", "OTel / Prometheus / ELK", fill="#5B8C5A", outline="#3E6B3D")

    # DR
    rr(d, (840, 220, 1550, 860), fill="#FFF8F0", outline="#C46B1A", width=3, radius=8)
    d.text((860, 235), "DR site", font=fnt(13, True), fill="#C46B1A")
    box(d, 870, 280, 640, 90, "Standby Gateway + Apps", "[Warm/Hot — TBD]", "Failover per NFR-DR", fill=CONTAINER[0])
    box(d, 870, 400, 640, 90, "DB Replica", "[Replication mode TBD]", "RPO target TBD", fill="#3F6F8A")
    box(d, 870, 520, 640, 90, "Object Store Replica", "[Cross-site]", "DEO scan durability", fill="#3F6F8A")
    box(d, 870, 640, 640, 90, "DR Runbooks", "[Ops]", "Failover / failback / recon", fill="#5B8C5A", outline="#3E6B3D")
    box(d, 870, 760, 640, 70, "Confirm RTO/RPO with SDC (NFR-DR-001/002)", "[Open decision]", "", fill=EXT[0], outline="#666")

    arrow(d, 270, 140, 330, 140, "HTTPS")
    arrow(d, 540, 180, 410, 280, "to primary")
    arrow(d, 760, 430, 840, 325, "replication")
    arrow(d, 760, 540, 840, 445, "replication")
    arrow(d, 760, 650, 840, 565, "replication")

    path = OUT / "C4_Deployment.png"
    img.save(path, "PNG")
    print("Wrote", path)


def gen_channel_flow():
    W, H = 1680, 860
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, W, "Channel Workflow across Containers", "Online vs Offline orchestration")

    box(d, 40, 90, 1600, 70, "Shared intake: Login → Prerequisite → Channel select → Declarations → Details", "[Both]", "", fill="#0B3A67")

    rr(d, (40, 190, 820, 800), fill="#EAF6FF", outline="#1168BD", width=2, radius=8)
    d.text((60, 205), "ONLINE — HMA_ONLINE_v1", font=fnt(13, True), fill="#1168BD")
    online = [
        "Office + Summary → Form 1A",
        "eSign Adapter",
        "Verification (single stage)",
        "Payment (after SR approve)",
        "DSC Adapter",
        "Register & Certificate (Form II-A)",
    ]
    y = 250
    for t in online:
        box(d, 70, y, 720, 55, t, "", "", fill=CONTAINER[0])
        if y > 250:
            arrow(d, 430, y - 20, 430, y)
        y += 75
    d.text((70, 720), "Reject → citizen data correction", font=fnt(11, True), fill="#A33")

    rr(d, (860, 190, 1640, 800), fill="#FFF5EB", outline="#C46B1A", width=2, radius=8)
    d.text((880, 205), "OFFLINE — HMA_OFFLINE_v1", font=fnt(13, True), fill="#C46B1A")
    offline = [
        "Verification Stage 1 (data)",
        "Payment + Appointment saga",
        "Print Form I / II / 1A",
        "DEO checklist + scan upload",
        "Verification Stage 2 (signed forms)",
        "DSC → Register & Certificate",
    ]
    y = 250
    for t in offline:
        box(d, 890, y, 720, 55, t, "", "", fill="#E08A3A", outline="#A85A18")
        if y > 250:
            arrow(d, 1250, y - 20, 1250, y)
        y += 75
    d.text((890, 720), "S1 reject → citizen; S2 reject → DEO only", font=fnt(11, True), fill="#A33")

    path = OUT / "C4_Channel_Workflow.png"
    img.save(path, "PNG")
    print("Wrote", path)


if __name__ == "__main__":
    gen_context()
    gen_containers()
    gen_components()
    gen_deployment()
    gen_channel_flow()
    print("Done")
