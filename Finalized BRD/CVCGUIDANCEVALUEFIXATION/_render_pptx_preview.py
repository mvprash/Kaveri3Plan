# -*- coding: utf-8 -*-
"""Render a .pptx to PNG slide previews (PowerPoint via PowerShell COM -> PDF -> PyMuPDF).

Usage: python _render_pptx_preview.py <deck.pptx> <out_dir> [zoom]
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import fitz


def render(deck: Path, out_dir: Path, zoom: float = 1.0) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        pdf = Path(tmp) / (deck.stem + ".pdf")
        ps = (
            "$app = New-Object -ComObject PowerPoint.Application; "
            f"$p = $app.Presentations.Open('{deck}', $true, $false, $false); "
            f"$p.SaveAs('{pdf}', 32); $p.Close(); $app.Quit()"
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True, timeout=180)
        doc = fitz.open(pdf)
        for i, page in enumerate(doc, 1):
            page.get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(out_dir / f"slide_{i:02d}.png")
        print(f"Rendered {len(doc)} slides to {out_dir}")
        doc.close()


if __name__ == "__main__":
    render(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), float(sys.argv[3]) if len(sys.argv) > 3 else 1.0)
