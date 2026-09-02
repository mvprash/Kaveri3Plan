# -*- coding: utf-8 -*-
"""Generate sample UI mockups for BRD_User_Management_v4.16.docx.

Outputs:
  - Sample_UI/screens/*.html  — interactive HTML mockups (open index.html)
  - Sample_UI/png/*.png       — PNG wireframes for BRD / review packs

Source: BRD v4.16 workflows (§6.1–§6.7), FR-UM-001 … FR-UM-084.
"""
from __future__ import annotations

import html
import sys
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent
SCREENS_DIR = BASE / "screens"
PNG_DIR = BASE / "png"
STYLES_DIR = BASE / "styles"

W, H = 1280, 800
HEADER_H = 72
FOOTER_H = 36
MARGIN = 48
PRIMARY = (26, 68, 128)
ACCENT = (255, 153, 51)
BG = (245, 247, 250)
CARD = (255, 255, 255)
BORDER = (208, 216, 228)
TEXT = (30, 41, 59)
MUTED = (100, 116, 139)
SUCCESS = (22, 163, 74)
WARN = (217, 119, 6)


@dataclass
class Field:
    label_en: str
    label_kn: str = ""
    value: str = ""
    required: bool = False
    field_type: str = "text"  # text, select, textarea, file, otp, captcha, readonly


@dataclass
class Screen:
    id: str
    title: str
    subtitle: str
    actor: str
    fr_refs: str
    portal: str  # citizen | officer | admin
    fields: list[Field] = field(default_factory=list)
    buttons: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    table_headers: list[str] = field(default_factory=list)
    table_rows: list[list[str]] = field(default_factory=list)
    header_context: str = ""
    sidebar_items: list[str] = field(default_factory=list)
    radio_options: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)
    active_step: int = 0


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    if bold:
        candidates = [
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            *candidates,
        ]
    for path in candidates:
        p = Path(path)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                continue
    return ImageFont.load_default()


def draw_screen_png(screen: Screen, out: Path) -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    f_title = _font(18, True)
    f_sub = _font(12)
    f_label = _font(11)
    f_val = _font(11)
    f_small = _font(10)
    f_btn = _font(12, True)

    # Header
    draw.rectangle([0, 0, W, HEADER_H], fill=PRIMARY)
    draw.text((MARGIN, 14), "KAVERI 3.0", fill=(255, 255, 255), font=f_title)
    draw.text((MARGIN, 40), "User Management — Sample UI (BRD v4.16)", fill=(200, 220, 255), font=f_sub)
    draw.text((W - MARGIN - 280, 22), screen.portal.upper(), fill=ACCENT, font=f_sub)
    draw.text((W - MARGIN - 280, 42), screen.id, fill=(200, 220, 255), font=f_small)

    y = HEADER_H + 20
    draw.text((MARGIN, y), screen.title, fill=TEXT, font=f_title)
    y += 28
    draw.text((MARGIN, y), screen.subtitle, fill=MUTED, font=f_sub)
    y += 18
    draw.text((MARGIN, y), f"Actor: {screen.actor}  |  {screen.fr_refs}", fill=MUTED, font=f_small)
    y += 24

    if screen.header_context:
        draw.rectangle([MARGIN, y, W - MARGIN, y + 34], fill=(232, 240, 254), outline=BORDER)
        draw.text((MARGIN + 12, y + 9), screen.header_context, fill=PRIMARY, font=f_sub)
        y += 44

    if screen.steps:
        sx = MARGIN
        for i, step in enumerate(screen.steps):
            color = PRIMARY if i == screen.active_step else MUTED
            bg = (219, 234, 254) if i == screen.active_step else CARD
            tw = min(180, (W - 2 * MARGIN) // max(len(screen.steps), 1) - 8)
            draw.rectangle([sx, y, sx + tw, y + 28], fill=bg, outline=BORDER)
            draw.text((sx + 8, y + 7), f"{i + 1}. {step[:22]}", fill=color, font=f_small)
            sx += tw + 8
        y += 40

    content_w = W - 2 * MARGIN
    if screen.sidebar_items:
        sw = 220
        draw.rectangle([MARGIN, y, MARGIN + sw, H - FOOTER_H - 16], fill=CARD, outline=BORDER)
        sy = y + 12
        for item in screen.sidebar_items:
            hl = item.startswith("»")
            draw.text((MARGIN + 14, sy), item.lstrip("» "), fill=PRIMARY if hl else TEXT, font=f_sub if hl else f_label)
            sy += 24
        fx = MARGIN + sw + 16
        fw = content_w - sw - 16
    else:
        fx = MARGIN
        fw = content_w

    fy = y
    if screen.radio_options:
        draw.text((fx, fy), "Select one option:", fill=TEXT, font=f_label)
        fy += 22
        for opt in screen.radio_options:
            draw.ellipse([fx, fy + 4, fx + 14, fy + 18], outline=PRIMARY, width=2)
            if screen.radio_options.index(opt) == 0:
                draw.ellipse([fx + 4, fy + 8, fx + 10, fy + 14], fill=PRIMARY)
            draw.text((fx + 22, fy), opt, fill=TEXT, font=f_val)
            fy += 28
        fy += 8

    for fld in screen.fields:
        lbl = fld.label_en
        if fld.label_kn:
            lbl += f"  [{fld.label_kn}]"
        if fld.required:
            lbl += " *"
        draw.text((fx, fy), lbl, fill=TEXT, font=f_label)
        fy += 18
        fh = 56 if fld.field_type == "textarea" else 34
        if fld.field_type == "captcha":
            draw.rectangle([fx, fy, fx + 140, fy + fh], fill=(240, 244, 248), outline=BORDER)
            draw.text((fx + 20, fy + 8), "A7K9M", fill=TEXT, font=f_title)
            draw.rectangle([fx + 156, fy, fx + fw, fy + fh], fill=CARD, outline=BORDER)
        elif fld.field_type == "otp":
            bx = fx
            for _ in range(6):
                draw.rectangle([bx, fy, bx + 36, fy + fh], fill=CARD, outline=BORDER)
                bx += 44
        else:
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=CARD, outline=BORDER)
            if fld.value:
                draw.text((fx + 10, fy + (fh - 14) // 2), fld.value, fill=MUTED, font=f_val)
        fy += fh + 14
        if fy > H - FOOTER_H - 80:
            break

    if screen.table_headers and fy < H - FOOTER_H - 120:
        col_w = fw // len(screen.table_headers)
        hx = fx
        for hdr in screen.table_headers:
            draw.rectangle([hx, fy, hx + col_w - 4, fy + 28], fill=(226, 232, 240), outline=BORDER)
            draw.text((hx + 6, fy + 7), hdr[:18], fill=TEXT, font=f_small)
            hx += col_w
        fy += 28
        for row in screen.table_rows[:4]:
            rx = fx
            for cell in row:
                draw.rectangle([rx, fy, rx + col_w - 4, fy + 26], fill=CARD, outline=BORDER)
                draw.text((rx + 6, fy + 6), cell[:20], fill=TEXT, font=f_small)
                rx += col_w
            fy += 26

    bx = fx
    for btn in screen.buttons:
        bw = max(120, len(btn) * 9 + 24)
        draw.rectangle([bx, H - FOOTER_H - 52, bx + bw, H - FOOTER_H - 18], fill=PRIMARY if bx == fx else CARD, outline=PRIMARY)
        tc = (255, 255, 255) if bx == fx else PRIMARY
        draw.text((bx + 14, H - FOOTER_H - 42), btn, fill=tc, font=f_btn)
        bx += bw + 12

    if screen.notes:
        ny = H - FOOTER_H - 90
        for note in screen.notes[:2]:
            draw.text((fx, ny), f"• {note[:90]}", fill=MUTED, font=f_small)
            ny += 16

    draw.rectangle([0, H - FOOTER_H, W, H], fill=(226, 232, 240))
    draw.text((MARGIN, H - FOOTER_H + 10), "Sample only — not production UI. Bilingual labels per GIGW / Karnataka e-Gov.", fill=MUTED, font=f_small)
    img.save(out)


def render_html_screen(screen: Screen) -> str:
    portal_class = screen.portal
    steps_html = ""
    if screen.steps:
        items = []
        for i, step in enumerate(screen.steps):
            cls = "active" if i == screen.active_step else ""
            items.append(f'<li class="{cls}"><span>{i + 1}</span>{html.escape(step)}</li>')
        steps_html = f'<ol class="steps">{"".join(items)}</ol>'

    sidebar_html = ""
    if screen.sidebar_items:
        items = []
        for item in screen.sidebar_items:
            cls = "active" if item.startswith("»") else ""
            items.append(f'<li class="{cls}">{html.escape(item.lstrip("» "))}</li>')
        sidebar_html = f'<nav class="sidebar"><ul>{"".join(items)}</ul></nav>'

    fields_html = []
    for fld in screen.fields:
        req = ' required' if fld.required else ""
        kn = f'<span class="kn">{html.escape(fld.label_kn)}</span>' if fld.label_kn else ""
        if fld.field_type == "captcha":
            inner = '<div class="captcha-box">A7K9M</div><input type="text" placeholder="Enter captcha">'
        elif fld.field_type == "otp":
            inner = "".join('<input type="text" maxlength="1" class="otp">' for _ in range(6))
        elif fld.field_type == "select":
            inner = f'<select{req}><option>{html.escape(fld.value or "— Select —")}</option></select>'
        elif fld.field_type == "textarea":
            inner = f'<textarea rows="3"{req}>{html.escape(fld.value)}</textarea>'
        elif fld.field_type == "file":
            inner = '<input type="file">'
        elif fld.field_type == "readonly":
            inner = f'<input type="text" value="{html.escape(fld.value)}" readonly>'
        else:
            ph = html.escape(fld.value)
            inner = f'<input type="text" value="{ph}" placeholder="{ph}"{req}>'
        fields_html.append(
            f'<label class="field"><span class="label">{html.escape(fld.label_en)}{kn}'
            f'{" *" if fld.required else ""}</span>{inner}</label>'
        )

    radio_html = ""
    if screen.radio_options:
        opts = []
        for i, opt in enumerate(screen.radio_options):
            chk = " checked" if i == 0 else ""
            opts.append(
                f'<label class="radio"><input type="radio" name="sel"{chk}> '
                f'{html.escape(opt)}</label>'
            )
        radio_html = f'<fieldset class="radio-group">{"".join(opts)}</fieldset>'

    table_html = ""
    if screen.table_headers:
        th = "".join(f"<th>{html.escape(h)}</th>" for h in screen.table_headers)
        rows = []
        for row in screen.table_rows:
            tds = "".join(f"<td>{html.escape(c)}</td>" for c in row)
            rows.append(f"<tr>{tds}</tr>")
        table_html = f'<table><thead><tr>{th}</tr></thead><tbody>{"".join(rows)}</tbody></table>'

    btns = "".join(
        f'<button type="button" class="btn{" primary" if i == 0 else ""}">{html.escape(b)}</button>'
        for i, b in enumerate(screen.buttons)
    )
    notes = "".join(f"<li>{html.escape(n)}</li>" for n in screen.notes)
    ctx = f'<div class="context-bar">{html.escape(screen.header_context)}</div>' if screen.header_context else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(screen.id)} — {html.escape(screen.title)}</title>
  <link rel="stylesheet" href="../styles/kaveri-ui.css">
</head>
<body class="{portal_class}">
  <header class="app-header">
    <div class="brand">KAVERI 3.0</div>
    <div class="meta">User Management · {html.escape(screen.id)} · {html.escape(screen.portal.title())}</div>
  </header>
  <main class="layout">
    {sidebar_html}
    <section class="content">
      <h1>{html.escape(screen.title)}</h1>
      <p class="subtitle">{html.escape(screen.subtitle)}</p>
      <p class="refs">Actor: {html.escape(screen.actor)} · {html.escape(screen.fr_refs)}</p>
      {ctx}
      {steps_html}
      {radio_html}
      <form class="form">{"".join(fields_html)}</form>
      {table_html}
      {"<ul class='notes'>" + notes + "</ul>" if notes else ""}
      <div class="actions">{btns}</div>
    </section>
  </main>
  <footer class="app-footer">Sample UI for BRD v4.16 — not production. Labels bilingual per GIGW.</footer>
</body>
</html>"""


SCREENS: list[Screen] = [
    Screen(
        id="UM-UI-01",
        title="Citizen Login",
        subtitle="Username + Captcha + OTP (passwordless)",
        actor="Citizen (Public user)",
        fr_refs="FR-UM-005, FR-UM-009, FR-UM-010, FR-UM-011",
        portal="citizen",
        fields=[
            Field("Username", "ಬಳಕೆದಾರ ಹೆಸರು", "citizen.ravi.k"),
            Field("Captcha", "ಕ್ಯಾಪ್ಚಾ", field_type="captcha", required=True),
            Field("OTP (sent to registered mobile)", "OTP", field_type="otp", required=True),
        ],
        buttons=["Send OTP", "Login", "Lost / changed mobile number"],
        notes=["No password field anywhere (FR-UM-009)", "OTP dispatched to registered mobile only (FR-UM-010)"],
    ),
    Screen(
        id="UM-UI-02",
        title="DSR Officer Login",
        subtitle="KGID + Captcha + OTP + Biometrics",
        actor="DSR Officer",
        fr_refs="FR-UM-006, FR-UM-011, FR-UM-064",
        portal="officer",
        fields=[
            Field("Username (KGID)", "KGID", "1234567", required=True),
            Field("Captcha", "ಕ್ಯಾಪ್ಚಾ", field_type="captcha", required=True),
            Field("OTP (registered mobile)", "OTP", field_type="otp", required=True),
            Field("Biometric verification", "ಬೈಯೋಮೆಟ್ರಿಕ್", "Place both thumbs on reader", field_type="readonly", required=True),
        ],
        buttons=["Send OTP", "Verify & Continue"],
        notes=["Biometric mandatory for departmental users (FR-UM-006)", "If multiple posts → post selection next (FR-UM-052)"],
    ),
    Screen(
        id="UM-UI-03",
        title="Citizen Self-Registration",
        subtitle="Step 1 — Personal details and Username",
        actor="Citizen",
        fr_refs="FR-UM-001, FR-UM-062, FR-UM-004",
        portal="citizen",
        steps=["Details", "Verify OTP", "Security Q", "Complete"],
        active_step=0,
        fields=[
            Field("Full name", "ಪೂರ್ಣ ಹೆಸರು", required=True),
            Field("Preferred Username", "ಬಳಕೆದಾರ ಹೆಸರು", "ravi.kumar2026", required=True),
            Field("Email address", "ಇಮೇಲ್", "ravi.k@example.com", required=True),
            Field("Mobile number", "ಮೊಬೈಲ್", "9876543210", required=True),
        ],
        buttons=["Check Username", "Continue"],
        notes=["Username unique across User Master (FR-UM-062)", "Email and mobile need not be unique (FR-UM-004)"],
    ),
    Screen(
        id="UM-UI-04",
        title="Citizen Self-Registration",
        subtitle="Step 2 — Dual OTP verification",
        actor="Citizen / System",
        fr_refs="FR-UM-063, FR-UM-055",
        portal="citizen",
        steps=["Details", "Verify OTP", "Security Q", "Complete"],
        active_step=1,
        fields=[
            Field("Email OTP", "ಇಮೇಲ್ OTP", field_type="otp", required=True),
            Field("Mobile OTP", "ಮೊಬೈಲ್ OTP", field_type="otp", required=True),
        ],
        buttons=["Resend email OTP", "Resend mobile OTP", "Verify & Continue"],
        notes=["Both OTPs must verify before account creation (FR-UM-063)", "6-digit OTP; 3 attempts; 30s cooldown (FR-UM-070–072)"],
    ),
    Screen(
        id="UM-UI-05",
        title="Citizen Self-Registration",
        subtitle="Step 3 — Five security questions",
        actor="Citizen",
        fr_refs="FR-UM-055, FR-UM-056",
        portal="citizen",
        steps=["Details", "Verify OTP", "Security Q", "Complete"],
        active_step=2,
        fields=[
            Field("Security question 1", "ಪ್ರಶ್ನೆ 1", "What is your mother's maiden name?", field_type="select", required=True),
            Field("Answer 1", "ಉತ್ತರ 1", required=True),
            Field("Security question 2", "ಪ್ರಶ್ನೆ 2", "First school attended?", field_type="select", required=True),
            Field("Answer 2", "ಉತ್ತರ 2", required=True),
        ],
        buttons=["Save & Create Account"],
        notes=["All five questions mandatory; answers stored hashed (FR-UM-055)", "Used for lost-mobile recovery (FR-UM-056)"],
    ),
    Screen(
        id="UM-UI-06",
        title="Lost / Changed Mobile Number",
        subtitle="Citizen account recovery — security questions + email PIN",
        actor="Citizen",
        fr_refs="FR-UM-056, FR-UM-065",
        portal="citizen",
        fields=[
            Field("Username", "ಬಳಕೆದಾರ ಹೆಸರು", required=True),
            Field("Captcha", "ಕ್ಯಾಪ್ಚಾ", field_type="captcha", required=True),
            Field("Security question (1 of 3 shown)", "ಪ್ರಶ್ನೆ", "What is your mother's maiden name?", field_type="readonly"),
            Field("Answer", "ಉತ್ತರ", required=True),
            Field("PIN (sent to registered email)", "PIN", field_type="otp", required=True),
            Field("New mobile number", "ಹೊಸ ಮೊಬೈಲ್", required=True),
            Field("OTP to new mobile", "OTP", field_type="otp", required=True),
        ],
        buttons=["Verify Questions", "Send PIN", "Update Mobile & Login"],
        notes=["Citizens only — departmental users use admin path (FR-UM-065)", "Three of five questions selected at random (FR-UM-056)"],
    ),
    Screen(
        id="UM-UI-07",
        title="Login Post Selection",
        subtitle="Mandatory when DSR Officer has multiple active post occupancies",
        actor="DSR Officer",
        fr_refs="FR-UM-052, FR-UM-054",
        portal="officer",
        radio_options=[
            "Sub Registrar — Sub Registrar (Computers) — SRO Bangalore South (BLR-S-001)",
            "First Division Assistant — FDA — SRO Bangalore South (BLR-S-001)",
        ],
        buttons=["Confirm & Enter Home"],
        notes=[
            'Label format: "Role — Post Name — Office Name (Office Code)" (FR-UM-052)',
            "Auto-skip if exactly one active post (FR-UM-052)",
        ],
    ),
    Screen(
        id="UM-UI-08",
        title="Officer Home & Session Context",
        subtitle="Header shows assigned post; additional charge available after login",
        actor="DSR Officer",
        fr_refs="FR-UM-053, FR-UM-054",
        portal="officer",
        header_context="Assigned: Sub Registrar — Sub Registrar (Computers) — SRO Bangalore South (BLR-S-001)  |  Active context: Assigned post",
        sidebar_items=["Dashboard", "Marriage Registration", "» User Management", "Reports", "Profile"],
        fields=[
            Field("Switch context", "ಸಂದರ್ಭ", "Assigned post", field_type="select"),
        ],
        buttons=["Additional charge", "Switch post context", "Logout"],
        notes=["Additional charge only for wholly unoccupied subordinate posts (FR-UM-053)", "Module Function claims follow active context (FR-UM-038)"],
    ),
    Screen(
        id="UM-UI-09",
        title="Additional Charge",
        subtitle="Take charge of unoccupied subordinate post without logout",
        actor="DSR Officer",
        fr_refs="FR-UM-053, FR-UM-066(b)",
        portal="officer",
        radio_options=[
            "First Division Assistant — FDA — SRO Bangalore South (wholly unoccupied)",
            "— Clear additional charge — return to assigned post only —",
        ],
        buttons=["Apply Context", "Cancel"],
        notes=["Post-login only; at most one additional charge (FR-UM-053)", "Partial vacancy does not qualify (FR-UM-066(b))"],
    ),
    Screen(
        id="UM-UI-10",
        title="Add DSR Department User",
        subtitle="Admin creates officer with sanctioned post assignment",
        actor="Authorised Administrator",
        fr_refs="FR-UM-002, FR-UM-017, FR-UM-030, FR-UM-045, FR-UM-066(a)",
        portal="admin",
        sidebar_items=["Users", "» Add DSR User", "Transfer", "Masters", "Reports"],
        fields=[
            Field("KGID (becomes Username)", "KGID", "2345678", required=True),
            Field("Full name", "ಹೆಸರು", required=True),
            Field("Official email ID", "ಅಧಿಕೃತ ಇಮೇಲ್", "officer@karnataka.gov.in", required=True),
            Field("Mobile number", "ಮೊಬೈಲ್", required=True),
            Field("Sanctioned post + Office", "ಪದ + ಕಚೇರಿ", "Sub Registrar — SRO Bangalore South", field_type="select", required=True),
            Field("Deputation end date (optional)", "ಅಂತಿಮ ದಿನಾಂಕ", field_type="text"),
            Field("Deputation reason", "ಕಾರಣ", field_type="select"),
            Field("Approval letter", "ಆದೇಶ", field_type="file"),
            Field("Biometric capture", "ಬೈಯೋಮೆಟ್ರಿಕ್", "Both thumbs captured", field_type="readonly", required=True),
        ],
        buttons=["Add another post", "Save User"],
        notes=["At least one post with available capacity required (FR-UM-030)", "KGID validated and unique (FR-UM-064)"],
    ),
    Screen(
        id="UM-UI-11",
        title="Add Other Department User",
        subtitle="Parent department officer with single role assignment",
        actor="Authorised Administrator",
        fr_refs="FR-UM-003, FR-UM-029, FR-UM-034",
        portal="admin",
        sidebar_items=["Users", "» Add Other Dept User", "Masters"],
        fields=[
            Field("KGID (Username)", "KGID", required=True),
            Field("Full name", "ಹೆಸರು", required=True),
            Field("Official email (parent dept)", "ಇಮೇಲ್", required=True),
            Field("Mobile", "ಮೊಬೈಲ್", required=True),
            Field("Parent department", "ಇಲಾಖೆ", "Revenue Department", field_type="select", required=True),
            Field("Designation", "ಹುದ್ದೆ", required=True),
            Field("Role (Other Department category)", "ಪಾತ್ರ", "Treasury Approver", field_type="select", required=True),
            Field("Account end date (optional)", "ಅಂತಿಮ ದಿನಾಂಕ"),
            Field("Authorisation letter / NOC", "NOC", field_type="file"),
        ],
        buttons=["Save User"],
        notes=["Exactly one role mandatory (FR-UM-029)", "No sanctioned posts for Other Department users (FR-UM-034)"],
    ),
    Screen(
        id="UM-UI-12",
        title="Transfer Out / Relieving",
        subtitle="Superior relieves subordinate from post occupancy",
        actor="Hierarchy Superior",
        fr_refs="FR-UM-057, FR-UM-058, FR-UM-059",
        portal="admin",
        sidebar_items=["Users", "» Transfer Out", "Transfer In", "Occupancy"],
        fields=[
            Field("Office (within span)", "ಕಚೇರಿ", "SRO Bangalore South", field_type="select", required=True),
            Field("Officer / Post occupancy", "ಅಧಿಕಾರಿ", "FDA — Kumar R — SRO Bangalore South", field_type="select", required=True),
            Field("Relieving date", "ವಿಮುಕ್ತಿ ದಿನಾಂಕ", "2026-09-15", required=True),
            Field("Relieving order number", "ಆದೇಶ ಸಂ.", required=True),
            Field("Upload relieving order", "ಆದೇಶ ಫೈಲ್", field_type="file"),
        ],
        buttons=["Confirm Relieving"],
        notes=["Lists only offices in actor's span (FR-UM-059)", "Occupancy active until end of relieving date (FR-UM-058)"],
    ),
    Screen(
        id="UM-UI-13",
        title="Transfer In",
        subtitle="Assign officer to vacant or reserved post under superior span",
        actor="Hierarchy Superior",
        fr_refs="FR-UM-060, FR-UM-061, FR-UM-067",
        portal="admin",
        sidebar_items=["Users", "Transfer Out", "» Transfer In"],
        fields=[
            Field("Target Post + Office", "ಗುರಿ ಪದ", "Sub Registrar — SRO Mysuru North", field_type="select", required=True),
            Field("Capacity status", "ಸಾಮರ್ಥ್ಯ", "1 vacancy available", field_type="readonly"),
            Field("Officer (DSR user)", "ಅಧಿಕಾರಿ", "2345678 — Ramesh K", field_type="select", required=True),
            Field("Transfer / Reporting order", "ಆದೇಶ", required=True),
            Field("Joining date", "ಸೇರುವ ದಿನಾಂಕ", "2026-09-20", required=True),
            Field("Upload order", "ಆದೇಶ ಫೈಲ್", field_type="file"),
        ],
        buttons=["Confirm Transfer In"],
        notes=["Login blocked until 12:00 AM IST of joining date if future (FR-UM-061)", "Reserved occupancy when at full strength + pending relieving (FR-UM-067)"],
    ),
    Screen(
        id="UM-UI-14",
        title="Temporary Absence & Charge",
        subtitle="Superior records leave/OOD and optional temporary charge",
        actor="Hierarchy Superior",
        fr_refs="FR-UM-079, FR-UM-082, FR-UM-083",
        portal="admin",
        fields=[
            Field("Officer occupancy", "ಅಧಿಕಾರಿ", "SR — Priya S — SRO Hassan", field_type="select", required=True),
            Field("Absence type", "ವಿಧ", "Leave", field_type="select", required=True),
            Field("Reason code", "ಕಾರಣ", field_type="select", required=True),
            Field("From date", "ದಿನಾಂಕದಿಂದ", required=True),
            Field("To date", "ವರೆಗೆ", required=True),
            Field("Temporary charge officer (optional)", "ತಾತ್ಕಾಲಿಕ", "FDA — Cover Officer", field_type="select"),
        ],
        buttons=["Record Absence", "Assign Temporary Charge"],
        notes=["Login denied for absent officer's Username (FR-UM-080)", "Temporary charge appears in cover officer's login list (FR-UM-083)"],
    ),
    Screen(
        id="UM-UI-15",
        title="Departmental Mobile Change",
        subtitle="Administrator updates mobile — no self-service for departmental users",
        actor="Authorised Administrator",
        fr_refs="FR-UM-065, FR-UM-013",
        portal="admin",
        fields=[
            Field("Search by KGID", "KGID", "1234567", required=True),
            Field("Officer name", "ಹೆಸರು", "Anand Rao", field_type="readonly"),
            Field("Current mobile", "ಪ್ರಸ್ತುತ", "98XXXXXX10", field_type="readonly"),
            Field("New mobile number", "ಹೊಸ ಮೊಬೈಲ್", required=True),
            Field("Reason for change", "ಕಾರಣ", field_type="textarea", required=True),
            Field("OTP verification", "OTP", field_type="otp", required=True),
        ],
        buttons=["Send OTP to new mobile", "Save & Notify"],
        notes=["Reason mandatory; audit logged (FR-UM-065)", "Officer notified on official email"],
    ),
    Screen(
        id="UM-UI-16",
        title="Sanctioned Posts Occupancy",
        subtitle="Strength, occupied count, and vacancy per Post + Office",
        actor="Administrator / Application Admin",
        fr_refs="FR-UM-048, FR-UM-066, FR-UM-027",
        portal="admin",
        sidebar_items=["Masters", "» Sanctioned Posts", "Posts Master", "Office Hierarchy"],
        table_headers=["Post", "Office", "Sanctioned", "Occupied", "Available", "Wholly vacant?"],
        table_rows=[
            ["Sub Registrar", "BLR-S-001", "1", "1", "0", "No"],
            ["FDA", "BLR-S-001", "2", "1", "1", "Yes"],
            ["SDA", "BLR-S-001", "1", "0", "1", "Yes"],
            ["DR", "MYS-N-002", "1", "1", "0", "No"],
        ],
        buttons=["Export", "Refresh"],
        notes=["Two vacancy tests: capacity vs wholly unoccupied (FR-UM-066)", "Counts refreshed by midnight job (FR-UM-068)"],
    ),
    Screen(
        id="UM-UI-17",
        title="Role — Module — Function Mapping",
        subtitle="Application Admin maps privileges via tree UI",
        actor="Application Admin",
        fr_refs="FR-UM-038, FR-UM-041, FR-UM-042",
        portal="admin",
        sidebar_items=["RBAC", "» Role Mapping", "Module Master", "Resource Master"],
        fields=[
            Field("Role", "ಪಾತ್ರ", "Sub Registrar", field_type="select", required=True),
        ],
        table_headers=["Module", "Function", "Granted"],
        table_rows=[
            ["Marriage Registration", "FN-MAR-ADD", "Yes"],
            ["Marriage Registration", "FN-MAR-APPROVE", "Yes"],
            ["Certified Copy", "FN-CC-VIEW", "Yes"],
            ["User Management", "FN-UM-ADMIN", "No"],
        ],
        buttons=["Save Mapping", "Add Function"],
        notes=["Runtime enforcement via session claims (FR-UM-041)", "UI hides unauthorised menus (S-03)"],
    ),
    Screen(
        id="UM-UI-18",
        title="Citizen Profile",
        subtitle="View and update profile after login",
        actor="Citizen",
        fr_refs="FR-UM-013, FR-UM-014",
        portal="citizen",
        fields=[
            Field("Username", "ಬಳಕೆದಾರ", "citizen.ravi.k", field_type="readonly"),
            Field("Full name", "ಹೆಸರು", "Ravi Kumar"),
            Field("Email", "ಇಮೇಲ್", "ravi.k@example.com"),
            Field("Mobile", "ಮೊಬೈಲ್", "9876543210"),
            Field("Profile photo", "ಫೋಟೋ", field_type="file"),
        ],
        buttons=["Save Changes"],
        notes=["Citizen may update mobile/email from profile (FR-UM-013)", "Departmental profile changes via administrator"],
    ),
]


CSS = """/* KAVERI 3.0 User Management — sample UI styles (BRD v4.16) */
:root {
  --primary: #1a4480;
  --accent: #ff9933;
  --bg: #f5f7fa;
  --card: #ffffff;
  --border: #d0d8e4;
  --text: #1e293b;
  --muted: #64748b;
  --header-h: 56px;
  font-family: "Segoe UI", system-ui, sans-serif;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text); min-height: 100vh; }
.app-header {
  background: var(--primary); color: #fff; padding: 12px 32px;
  display: flex; align-items: baseline; gap: 24px;
}
.brand { font-size: 1.25rem; font-weight: 700; }
.meta { font-size: 0.85rem; opacity: 0.85; }
.layout { display: flex; max-width: 1200px; margin: 0 auto; padding: 24px; gap: 24px; }
.sidebar {
  width: 220px; flex-shrink: 0; background: var(--card);
  border: 1px solid var(--border); border-radius: 6px; padding: 12px 0;
}
.sidebar ul { list-style: none; margin: 0; padding: 0; }
.sidebar li { padding: 8px 16px; font-size: 0.9rem; cursor: default; }
.sidebar li.active { color: var(--primary); font-weight: 600; background: #e8f0fe; }
.content { flex: 1; background: var(--card); border: 1px solid var(--border);
  border-radius: 6px; padding: 28px 32px; }
h1 { margin: 0 0 4px; font-size: 1.35rem; }
.subtitle { color: var(--muted); margin: 0 0 4px; }
.refs { font-size: 0.8rem; color: var(--muted); margin: 0 0 20px; }
.context-bar {
  background: #e8f0fe; border: 1px solid var(--border); border-radius: 4px;
  padding: 10px 14px; margin-bottom: 20px; font-size: 0.85rem; color: var(--primary);
}
.steps { display: flex; gap: 8px; list-style: none; padding: 0; margin: 0 0 24px; }
.steps li {
  flex: 1; text-align: center; padding: 8px; font-size: 0.8rem;
  border: 1px solid var(--border); border-radius: 4px; background: var(--card);
}
.steps li.active { background: #dbeafe; border-color: var(--primary); font-weight: 600; }
.steps li span {
  display: inline-block; width: 20px; height: 20px; line-height: 20px;
  border-radius: 50%; background: var(--border); margin-right: 6px; font-size: 0.75rem;
}
.steps li.active span { background: var(--primary); color: #fff; }
.form { display: grid; gap: 16px; max-width: 560px; }
.field .label { display: block; font-size: 0.85rem; margin-bottom: 4px; }
.kn { color: var(--muted); font-size: 0.8rem; margin-left: 6px; }
.field input, .field select, .field textarea {
  width: 100%; padding: 8px 10px; border: 1px solid var(--border);
  border-radius: 4px; font-size: 0.9rem;
}
.captcha-box {
  display: inline-block; background: #f0f4f8; padding: 10px 20px;
  font-size: 1.4rem; letter-spacing: 4px; font-weight: 700; margin-right: 12px;
  border: 1px solid var(--border); vertical-align: middle;
}
.otp { width: 42px !important; text-align: center; margin-right: 6px; }
.radio-group { border: none; padding: 0; margin: 0 0 20px; }
.radio { display: block; padding: 10px 12px; margin-bottom: 8px;
  border: 1px solid var(--border); border-radius: 4px; cursor: default; }
.radio:has(input:checked) { border-color: var(--primary); background: #f0f7ff; }
table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.85rem; }
th, td { border: 1px solid var(--border); padding: 8px 10px; text-align: left; }
th { background: #e2e8f0; }
.notes { font-size: 0.8rem; color: var(--muted); margin: 16px 0; padding-left: 20px; }
.actions { margin-top: 24px; display: flex; gap: 10px; flex-wrap: wrap; }
.btn {
  padding: 10px 18px; border-radius: 4px; border: 1px solid var(--primary);
  background: var(--card); color: var(--primary); font-size: 0.9rem; cursor: default;
}
.btn.primary { background: var(--primary); color: #fff; }
.app-footer {
  text-align: center; padding: 12px; font-size: 0.75rem; color: var(--muted);
  border-top: 1px solid var(--border); margin-top: 32px;
}
body.citizen .app-header { border-bottom: 3px solid var(--accent); }
body.officer .app-header { border-bottom: 3px solid #059669; }
body.admin .app-header { border-bottom: 3px solid #7c3aed; }
"""


def write_index(screens: list[Screen]) -> None:
    rows = []
    for s in screens:
        rows.append(
            f"<tr><td><a href=\"screens/{s.id}.html\">{html.escape(s.id)}</a></td>"
            f"<td>{html.escape(s.title)}</td>"
            f"<td>{html.escape(s.actor)}</td>"
            f"<td>{html.escape(s.portal.title())}</td>"
            f"<td>{html.escape(s.fr_refs)}</td>"
            f"<td><a href=\"png/{s.id}.png\">PNG</a></td></tr>"
        )
    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>KAVERI 3.0 — User Management Sample UI (BRD v4.16)</title>
  <link rel="stylesheet" href="styles/kaveri-ui.css">
  <style>
    .catalog {{ max-width: 1100px; margin: 32px auto; padding: 0 24px; }}
    .catalog h1 {{ margin-bottom: 8px; }}
    .catalog p {{ color: var(--muted); }}
    .catalog table {{ background: var(--card); }}
  </style>
</head>
<body class="admin">
  <header class="app-header">
    <div class="brand">KAVERI 3.0</div>
    <div class="meta">User Management — Sample UI Catalogue · BRD v4.16</div>
  </header>
  <div class="catalog">
    <h1>Sample User Interfaces</h1>
    <p>Derived from <strong>BRD_User_Management_v4.16.docx</strong> workflows (§6.1–§6.7).
       Open HTML mockups in a browser or use PNG wireframes for review packs.</p>
    <table>
      <thead><tr><th>ID</th><th>Screen</th><th>Actor</th><th>Portal</th><th>FR refs</th><th>PNG</th></tr></thead>
      <tbody>{"".join(rows)}</tbody>
    </table>
  </div>
</body>
</html>"""
    (BASE / "index.html").write_text(content, encoding="utf-8")


def main() -> None:
    SCREENS_DIR.mkdir(parents=True, exist_ok=True)
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    STYLES_DIR.mkdir(parents=True, exist_ok=True)
    (STYLES_DIR / "kaveri-ui.css").write_text(CSS, encoding="utf-8")

    for screen in SCREENS:
        html_path = SCREENS_DIR / f"{screen.id}.html"
        html_path.write_text(render_html_screen(screen), encoding="utf-8")
        png_path = PNG_DIR / f"{screen.id}.png"
        draw_screen_png(screen, png_path)
        print(f"  {screen.id}  html + png")

    write_index(SCREENS)
    print(f"\nGenerated {len(SCREENS)} screens → {BASE}")
    print(f"Open: {BASE / 'index.html'}")


if __name__ == "__main__":
    main()
