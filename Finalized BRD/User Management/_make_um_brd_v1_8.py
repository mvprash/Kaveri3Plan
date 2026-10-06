import copy
import re
from pathlib import Path

import docx
from docx.shared import Emu, Inches
from docx.table import _Row
from docx.text.paragraph import Paragraph
from PIL import Image

SRC = r"Finalized BRD\User Management\BRD_User_Management_Simplified_v1.7.docx"
DST = r"Finalized BRD\User Management\BRD_User_Management_Simplified_v1.8.docx"
DIAGRAMS = Path(r"Finalized BRD\User Management\NewProcessDiagram")
DATE = "06-10-2026"
d = docx.Document(SRC)


def set_text(p, text):
    p.runs[0].text = text
    for r in p.runs[1:]:
        r._r.getparent().remove(r._r)


def add_row_after(row, values):
    tr = copy.deepcopy(row._tr)
    row._tr.addnext(tr)
    new = _Row(tr, row._parent)
    for cell, text in zip(new.cells, values):
        set_text(cell.paragraphs[0], text)
    return new


def req_rows():
    rows = {}
    for t in d.tables:
        for r in t.rows:
            key = r.cells[0].text.strip()
            if key.startswith("UM-"):
                rows[key] = r
    return rows


reqs = req_rows()
updates = {
    "UM-CIT-03":
        "The citizen enters an email address and a mobile number. The system says at once if the email is already "
        "registered to another account. An OTP is sent to each; when both are entered correctly, the account is "
        "created.",
    "UM-CIT-06":
        "The Username and the email must each be unique across all users; an email already registered to another "
        "account is refused (compared ignoring upper / lower case). The same mobile may be used on more than one "
        "account.",
    "UM-ODU-02":
        "The administrator selects the Department and enters Employee ID or KGID, official email of that "
        "department, and mobile. The official email must not already be registered to another account. The "
        "Username is Department Code + Employee ID / KGID (for example REV-12345).",
    "UM-MIG-07":
        "Records with a wrong or duplicate email ID, a wrong email, an email already used by another account, or "
        "an invalid mobile number, are set aside for correction. If the email is blank, the email ID is used as "
        "the email.",
}
for rid, text in updates.items():
    set_text(reqs[rid].cells[1].paragraphs[0], text)

sec = d.sections[0]
max_w = sec.page_width - sec.left_margin - sec.right_margin
max_h = sec.page_height - sec.top_margin - sec.bottom_margin - Inches(1.2)
pngs = {int(m.group(1)): f for f in DIAGRAMS.glob("UM_4_*.png") if (m := re.match(r"UM_4_(\d+)_", f.name))}
replaced = []
for cap in list(d.paragraphs):
    m = re.match(r"Figure 4\.(\d+): Process diagram", cap.text)
    if not m:
        continue
    num = int(m.group(1))
    pic = Paragraph(cap._p.getprevious(), cap._parent)
    assert pic._p.xpath(".//pic:pic"), cap.text
    for r in list(pic.runs):
        r._r.getparent().remove(r._r)
    png = pngs[num]
    w, h = Image.open(png).size
    scale = min(max_w / w, max_h / h)
    pic.add_run().add_picture(str(png), width=Emu(int(w * scale)), height=Emu(int(h * scale)))
    replaced.append(num)
assert replaced == list(range(1, 10)), replaced

control = {r.cells[0].text: r for r in d.tables[0].rows}
set_text(control["Version"].cells[1].paragraphs[0], "1.8")
set_text(control["Last updated"].cells[1].paragraphs[0], DATE)
add_row_after(d.tables[1].rows[-1], [
    "1.8", DATE, "Nandha Kumar",
    "Email made unique across all users in the user master. UM-CIT-06 reworded (only the mobile may be shared); "
    "duplicate-email checks added to UM-CIT-03, UM-ODU-02 and UM-MIG-07. Process diagrams 4.1 and 4.3 updated "
    "with the email check."])

d.save(DST)
print("Saved", DST)
