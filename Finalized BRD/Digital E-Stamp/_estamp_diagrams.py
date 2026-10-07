# -*- coding: utf-8 -*-
"""Process / architecture diagrams for the Digital E-Stamp BRD (rendered with Pillow)."""
from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = Path(r"C:\Windows\Fonts")
SCALE = 2


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    try:
        return ImageFont.truetype(str(FONT_DIR / name), size * SCALE)
    except OSError:
        return ImageFont.load_default()


LANE_FILL = ["#EAF2FB", "#F3F8EC", "#FFF6E5", "#F4ECF7"]
BOX_FILL = ["#CFE2F7", "#D9EBC6", "#FFE2B3", "#E4D2EE"]
BOX_LINE = "#3A5A80"
ARROW = "#33475B"


def _wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _box(draw, xy, text, fill, font, radius=10, outline=BOX_LINE, bold_first=False):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius * SCALE, fill=fill, outline=outline, width=2 * SCALE)
    lines = _wrap(draw, text, font, (x2 - x1) - 16 * SCALE)
    lh = font.size + 4 * SCALE
    ty = y1 + ((y2 - y1) - lh * len(lines)) / 2
    for ln in lines:
        tw = draw.textlength(ln, font=font)
        draw.text((x1 + ((x2 - x1) - tw) / 2, ty), ln, fill="#1B2733", font=font)
        ty += lh


def _arrow_head(draw, x, y, direction):
    s = 7 * SCALE
    if direction == "down":
        pts = [(x, y), (x - s, y - s * 1.6), (x + s, y - s * 1.6)]
    elif direction == "right":
        pts = [(x, y), (x - s * 1.6, y - s), (x - s * 1.6, y + s)]
    elif direction == "left":
        pts = [(x, y), (x + s * 1.6, y - s), (x + s * 1.6, y + s)]
    else:
        pts = [(x, y), (x - s, y + s * 1.6), (x + s, y + s * 1.6)]
    draw.polygon(pts, fill=ARROW)


def swimlane(path: Path, title: str, lanes: list[str], nodes: dict, edges: list[tuple], rows: int,
             lane_w: int = 300, row_h: int = 92, box_h: int = 64):
    """Vertical swimlane: lanes are columns; nodes = {id: (lane, row, text)}; edges always go downwards."""
    lane_w *= SCALE
    row_h *= SCALE
    box_h *= SCALE
    title_h = 54 * SCALE
    head_h = 44 * SCALE
    pad = 16 * SCALE
    width = lane_w * len(lanes) + pad * 2
    height = title_h + head_h + row_h * rows + pad * 2
    img = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(img)
    d.text((pad, pad), title, fill="#16324F", font=_font(17, True))
    top = pad + title_h
    for i, name in enumerate(lanes):
        x1 = pad + i * lane_w
        d.rectangle((x1, top, x1 + lane_w, height - pad), fill=LANE_FILL[i % 4], outline="#9FB3C8", width=SCALE)
        d.rectangle((x1, top, x1 + lane_w, top + head_h), fill="#16324F")
        f = _font(12, True)
        tw = d.textlength(name, font=f)
        d.text((x1 + (lane_w - tw) / 2, top + (head_h - f.size) / 2 - 2 * SCALE), name, fill="white", font=f)

    body_top = top + head_h
    bw = lane_w - 40 * SCALE

    def rect(nid):
        lane, row, _ = nodes[nid]
        cx = pad + lane * lane_w + lane_w / 2
        cy = body_top + row * row_h + row_h / 2
        return cx - bw / 2, cy - box_h / 2, cx + bw / 2, cy + box_h / 2

    for a, b, *lbl in edges:
        ax1, ay1, ax2, ay2 = rect(a)
        bx1, by1, bx2, by2 = rect(b)
        sx, sy = (ax1 + ax2) / 2, ay2
        tx, ty = (bx1 + bx2) / 2, by1
        if abs(sx - tx) < 1:
            d.line((sx, sy, tx, ty), fill=ARROW, width=2 * SCALE)
        else:
            my = ty - 12 * SCALE
            d.line((sx, sy, sx, my), fill=ARROW, width=2 * SCALE)
            d.line((sx, my, tx, my), fill=ARROW, width=2 * SCALE)
            d.line((tx, my, tx, ty), fill=ARROW, width=2 * SCALE)
        _arrow_head(d, tx, ty, "down")
        if lbl:
            f = _font(9)
            d.text((tx + 6 * SCALE, ty - 30 * SCALE), lbl[0], fill="#8A2D0A", font=f)

    f = _font(12)
    for nid, (lane, _row, text) in nodes.items():
        _box(d, rect(nid), text, BOX_FILL[lane % 4], f)
    img.save(path, dpi=(220, 220))
    return path


def estamp_process(path: Path) -> Path:
    lanes = ["Citizen / Applicant / Parties", "Kaveri 3.0 - Digital E-Stamp",
             "Template Generation Service", "External services"]
    n = {
        "s1": (0, 0, "1. Login (mobile OTP) and select 'Digital E-Stamp'"),
        "x1": (3, 1, "UIDAI Aadhaar e-KYC (OTP) / DSC for non-e-KYC"),
        "s2": (1, 2, "2. Select nature of document and stamp sub-article (optionally registrable only)"),
        "s3": (0, 3, "3. Enter / fetch schedule (property) details"),
        "x3": (3, 4, "Bhoomi / E-Swathu / E-Aasthi / ULMS fetch"),
        "s4": (1, 5, "4. Validate GL/GR, alienation, relaxed fields; auto schedule description"),
        "s5": (0, 6, "5. Add parties (OTP, e-KYC) and witnesses; allocate schedules"),
        "s6": (1, 7, "6. Name match (>=80%), minimum parties, witness rule; compute stamp duty"),
        "s7": (0, 8, "7. Enter deed terms / clauses (template-guided)"),
        "s8": (2, 9, "8. Render DRAFT PDF (watermarked) from approved template version"),
        "s9": (0, 10, "9. Preview, confirm, freeze data"),
        "x9": (3, 11, "Khajane-II payment / challan verification"),
        "s10": (1, 12, "10. Allot e-Stamp UIN; record duty paid"),
        "s11": (2, 13, "11. Render FINAL PDF: certificate page, UIN each page, QR, signature boxes"),
        "x11": (3, 14, "eSign by every party (Aadhaar eSign / DSC)"),
        "s12": (1, 15, "12. Apply department seal; publish to Verify; DigiLocker push; SMS"),
        "s13": (0, 16, "13. Download signed digital e-Stamp deed"),
    }
    e = [("s1", "x1"), ("x1", "s2"), ("s2", "s3"), ("s3", "x3"), ("x3", "s4"), ("s4", "s5"), ("s5", "s6"),
         ("s6", "s7"), ("s7", "s8"), ("s8", "s9"), ("s9", "x9"), ("x9", "s10", "Paid"), ("s10", "s11"),
         ("s11", "x11"), ("x11", "s12", "All signed"), ("s12", "s13")]
    return swimlane(path, "Digital E-Stamp - To-Be process (Online and Assisted)", lanes, n, e, rows=17)


def verify_lock_process(path: Path) -> Path:
    lanes = ["Citizen / Any person", "Document Registration (SRO)", "Kaveri 3.0 - Digital E-Stamp",
             "DC of Stamps / Khajane-II"]
    n = {
        "v1": (0, 0, "A1. Verify: enter UIN or scan QR"),
        "v2": (2, 1, "A2. Show masked certificate details and status (Issued / Locked / Cancelled)"),
        "r1": (1, 2, "B1. Pre-registration: presentant quotes e-Stamp UIN"),
        "r2": (2, 3, "B2. Validate UIN, parties, amount, status = Issued; fetch deed PDF"),
        "r3": (1, 4, "B3. SR verifies (Rule 29) and registers document"),
        "r4": (2, 5, "B4. Lock UIN (Rule 30); status = Locked / Used"),
        "c1": (0, 6, "C1. Apply for cancellation / refund (Form-4) of an Issued, unlocked UIN"),
        "c2": (3, 7, "C2. DC of Stamps verifies (Secs 47-52-A); approve / reject"),
        "c3": (2, 8, "C3. Cancel and lock certificate; endorse 'Cancelled' on PDF"),
        "c4": (3, 9, "C4. Refund to applicant via treasury"),
    }
    e = [("v1", "v2"), ("r1", "r2"), ("r2", "r3"), ("r3", "r4"),
         ("c1", "c2"), ("c2", "c3", "Approved"), ("c3", "c4")]
    return swimlane(path, "Digital E-Stamp - three separate flows: verify (A), lock on use (B), "
                    "cancellation and refund of an unlocked e-Stamp (C)", lanes, n, e, rows=10,
                    row_h=96)


def template_service_architecture(path: Path) -> Path:
    W, H = 1500 * SCALE, 860 * SCALE
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    S = SCALE
    d.text((20 * S, 16 * S), "Template Generation Microservice - shared by Digital E-Stamp and Document Registration",
           fill="#16324F", font=_font(17, True))
    f = _font(11)
    fb = _font(12, True)

    def box(x, y, w, h, text, fill, bold=False):
        _box(d, (x * S, y * S, (x + w) * S, (y + h) * S), text, fill, fb if bold else f)

    def arrow(x1, y1, x2, y2, label=None, both=False):
        d.line((x1 * S, y1 * S, x2 * S, y2 * S), fill=ARROW, width=2 * S)
        if x2 > x1 and y1 == y2:
            _arrow_head(d, x2 * S, y2 * S, "right")
            if both:
                _arrow_head(d, x1 * S, y1 * S, "left")
        elif y2 > y1:
            _arrow_head(d, x2 * S, y2 * S, "down")
            if both:
                _arrow_head(d, x1 * S, y1 * S, "up")
        else:
            _arrow_head(d, x2 * S, y2 * S, "up")
        if label:
            d.text(((x1 + x2) / 2 * S + 6 * S, (y1 + y2) / 2 * S - 22 * S), label, fill="#8A2D0A", font=_font(9))

    # consumers
    d.text((40 * S, 70 * S), "Consumers", fill="#16324F", font=fb)
    box(30, 100, 260, 90, "Digital E-Stamp module (deed + e-Stamp certificate)", BOX_FILL[0], True)
    box(30, 230, 260, 90, "Document Registration module (deed, endorsements, certificates)", BOX_FILL[0], True)
    box(30, 370, 260, 80, "Template Admin portal (IT Cell + DSR Legal) - maker-checker", BOX_FILL[3])

    box(370, 100, 170, 350, "API Gateway (OAuth2 client credentials, mTLS, rate limits)", "#E8EEF4")
    arrow(290, 145, 370, 145, "render")
    arrow(290, 275, 370, 275, "render")
    arrow(290, 410, 370, 410, "publish")

    # service boundary
    d.rounded_rectangle((590 * S, 70 * S, 1180 * S, 640 * S), radius=14 * S, outline="#16324F", width=3 * S,
                        fill="#F7FAFD")
    d.text((610 * S, 80 * S), "Template Generation Service (stateless, horizontally scalable)", fill="#16324F",
           font=fb)
    arrow(540, 240, 610, 240)
    comps = [
        (610, 120, "Template Registry - ID, version, locale, DN / sub-article mapping, status"),
        (890, 120, "Payload schema validator (JSON Schema from field workbook)"),
        (610, 240, "Data binder - merge fields, repeating groups, conditional clauses"),
        (890, 240, "Layout engine - DOCX template to PDF/A (Kannada + English fonts)"),
        (610, 360, "Stamping - DRAFT watermark / e-Stamp UIN on each page / QR / page x of y"),
        (890, 360, "Signature placeholders - named boxes per party for eSign / DSC"),
        (610, 480, "Job manager - sync render or async job + callback"),
        (890, 480, "Audit and hash - SHA-256, template version, consumer, masked payload log"),
    ]
    for x, y, t in comps:
        box(x, y, 260, 95, t, BOX_FILL[2])

    # stores
    box(1240, 120, 230, 85, "Template repository (versioned DOCX + schema)", BOX_FILL[1])
    box(1240, 280, 230, 85, "Object store (Scality) - rendered PDFs, signed URLs", BOX_FILL[1])
    box(1240, 440, 230, 85, "Audit log / SIEM; metrics and alerts", BOX_FILL[1])
    arrow(1180, 162, 1240, 162, both=True)
    arrow(1180, 322, 1240, 322)
    arrow(1180, 482, 1240, 482)

    d.text((40 * S, 690 * S), "Rules: the service never computes stamp duty and never signs on behalf of a party; "
           "consumers own business data, workflow and signing.", fill="#1B2733", font=f)
    d.text((40 * S, 720 * S), "In-flight applications stay pinned to the template version used for their first draft; "
           "only approved versions can be rendered in FINAL mode.", fill="#1B2733", font=f)
    d.text((40 * S, 750 * S), "Output: PDF/A-2b, A4, left margin 3.5 cm and right margin 1.5 cm (e-Stamping Rule 23(2)), "
           "document_id and SHA-256 returned to the consumer.", fill="#1B2733", font=f)
    img.save(path, dpi=(220, 220))
    return path


if __name__ == "__main__":
    out = Path(__file__).parent
    estamp_process(out / "EStamp_ToBe_Process.png")
    verify_lock_process(out / "EStamp_Verify_Lock_Cancel.png")
    template_service_architecture(out / "Template_Service_Architecture.png")
    print("diagrams ok")
