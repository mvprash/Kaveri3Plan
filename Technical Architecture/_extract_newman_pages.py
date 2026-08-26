# -*- coding: utf-8 -*-
"""Extract Newman book pages for tooling recommendations by layer."""
from pypdf import PdfReader
from pathlib import Path

path = Path(r"E:\Prashanth\Official\Kaveri 3.0\Kaveri3Plan\Books\Building Microservices Designing Fine-Grained Systems 2nd By Sam Newman.pdf")
out = Path(r"E:\Prashanth\Official\Kaveri 3.0\Kaveri3Plan\Technical Architecture\_newman_tool_extracts.txt")
r = PdfReader(str(path))

# 1-indexed page ranges of interest (from earlier index + TOC knowledge)
ranges = [
    (17, 45, "Ch1 microservices overview / tech notes"),
    (125, 195, "Ch4-5 communication styles and implementing communication"),
    (196, 222, "Service discovery, gateway, mesh, resilience basics"),
    (223, 250, "Ch6 Workflow / sagas"),
    (251, 280, "Ch7 Build"),
    (293, 350, "Ch8 Deployment containers k8s FaaS"),
    (360, 390, "Ch9 Testing / contracts"),
    (395, 430, "Ch10 Observability"),
    (432, 480, "Ch11 Security"),
    (484, 520, "Ch12 Resiliency"),
    (570, 605, "Ch14 UI BFF GraphQL"),
]

parts = []
for start, end, label in ranges:
    parts.append(f"\n\n{'='*80}\n{label} (PDF pages {start}-{end})\n{'='*80}\n")
    for i in range(start - 1, min(end, len(r.pages))):
        t = r.pages[i].extract_text() or ""
        parts.append(f"\n--- PAGE {i+1} ---\n{t}")

out.write_text("".join(parts), encoding="utf-8", errors="replace")
print("Wrote", out, "chars", out.stat().st_size)
