# -*- coding: utf-8 -*-
"""Export the Registration Core Process A / B / C draw.io diagrams to PNG.

Renders each .drawio file as saved (including manual edits made in draw.io)
with the official diagrams.net viewer in headless Chrome (needs internet access
to load viewer-static.min.js).
"""
from __future__ import annotations

import html
import json
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
SCALE = 2
BORDER = 10

DIAGRAMS = (
    "Process_A_Registration_Application",
    "Process_B_SR_Check_and_Payment",
    "Process_C_Appointment_and_Registration",
)


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


def export(stem: str, tmp: Path) -> Path:
    xml = (OUT_DIR / f"{stem}.drawio").read_text(encoding="utf-8")
    diagram_w, diagram_h = diagram_extent(xml)
    cfg = html.escape(json.dumps({"xml": xml, "auto-fit": False, "resize": False, "zoom": 1,
                                  "border": BORDER, "toolbar": ""}), quote=True)
    page = tmp / f"{stem}.html"
    page.write_text(
        '<html><body style="margin:0;background:#ffffff">'
        f'<div class="mxgraph" data-mxgraph="{cfg}"></div>'
        '<script src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>'
        "</body></html>",
        encoding="utf-8",
    )
    png = OUT_DIR / f"{stem}.png"
    width = diagram_w + 2 * BORDER + 40
    height = diagram_h + 2 * BORDER + 40
    subprocess.run(
        [
            str(CHROME), "--headless=new", "--disable-gpu", "--hide-scrollbars",
            f"--force-device-scale-factor={SCALE}", f"--window-size={width},{height}",
            "--virtual-time-budget=20000", f"--screenshot={png}", page.as_uri(),
        ],
        check=True, capture_output=True, timeout=120,
    )
    return png


def main():
    with tempfile.TemporaryDirectory() as tmp:
        for stem in DIAGRAMS:
            print("Wrote", export(stem, Path(tmp)))


if __name__ == "__main__":
    main()
