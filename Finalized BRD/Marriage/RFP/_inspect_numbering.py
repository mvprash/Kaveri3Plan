# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from lxml import etree
import zipfile

sys.stdout.reconfigure(encoding="utf-8")
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

with zipfile.ZipFile("BRD_Marriage_BRD_v1.23.docx") as z:
    root = etree.fromstring(z.read("word/numbering.xml"))

num_to_abs = {}
for num in root.xpath("//w:num", namespaces=NS):
    numId = num.get(f"{W}numId")
    absId = num.find("w:abstractNumId", NS).get(f"{W}val")
    num_to_abs[numId] = absId

interesting = [str(i) for i in range(11, 40)]
for numId in interesting:
    absId = num_to_abs.get(numId)
    if not absId:
        continue
    absn = root.xpath(f'//w:abstractNum[@w:abstractNumId="{absId}"]', namespaces=NS)[0]
    print(f"\nnumId={numId} abstract={absId}")
    for lvl in absn.xpath("./w:lvl", namespaces=NS)[:6]:
        ilvl = lvl.get(f"{W}ilvl")
        fmt = lvl.find("w:numFmt", NS)
        lt = lvl.find("w:lvlText", NS)
        start = lvl.find("w:start", NS)
        fmt_v = fmt.get(f"{W}val") if fmt is not None else None
        lt_v = lt.get(f"{W}val") if lt is not None else None
        start_v = start.get(f"{W}val") if start is not None else None
        print(f"  lvl{ilvl}: fmt={fmt_v} text={lt_v!r} start={start_v}")
