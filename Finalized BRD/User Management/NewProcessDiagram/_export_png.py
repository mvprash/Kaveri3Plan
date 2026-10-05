# -*- coding: utf-8 -*-
"""Export every .drawio file in this folder to PNG.

Renders each file as saved (including manual edits made in draw.io) with the official
diagrams.net viewer in headless Chrome (needs internet access to load viewer-static.min.js).
"""
from __future__ import annotations

import html
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
SCALE = 2
BORDER = 10


def diagram_extent(xml: str) -> tuple[int, int]:
    width = height = 0.0
    for cell in ET.fromstring(xml).iter("mxCell"):
        geo = cell.find("mxGeometry")
        if cell.get("vertex") != "1" or geo is None:
            continue
        width = max(width, float(geo.get("x", 0)) + float(geo.get("width", 0)))
        height = max(height, float(geo.get("y", 0)) + float(geo.get("height", 0)))
    return int(width), int(height)


def export(drawio: Path, tmp: Path) -> Path:
    xml = drawio.read_text(encoding="utf-8")
    diagram_w, diagram_h = diagram_extent(xml)
    cfg = html.escape(json.dumps({"xml": xml, "auto-fit": False, "resize": False, "zoom": 1,
                                  "border": BORDER, "toolbar": ""}), quote=True)
    page = tmp / f"{drawio.stem}.html"
    page.write_text(
        '<html><body style="margin:0;background:#ffffff">'
        f'<div class="mxgraph" data-mxgraph="{cfg}"></div>'
        '<script src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>'
        "</body></html>",
        encoding="utf-8",
    )
    png = drawio.with_suffix(".png")
    subprocess.run(
        [
            str(CHROME), "--headless=new", "--disable-gpu", "--hide-scrollbars",
            f"--force-device-scale-factor={SCALE}",
            f"--window-size={diagram_w + 2 * BORDER + 40},{diagram_h + 2 * BORDER + 80}",
            "--virtual-time-budget=20000", f"--screenshot={png}", page.as_uri(),
        ],
        check=True, capture_output=True, timeout=120,
    )
    return png


def main():
    names = sys.argv[1:]
    files = [OUT_DIR / f"{n}.drawio" for n in names] if names else sorted(OUT_DIR.glob("*.drawio"))
    with tempfile.TemporaryDirectory() as tmp:
        for drawio in files:
            print("Wrote", export(drawio, Path(tmp)).name)


if __name__ == "__main__":
    main()
