import re
from pypdf import PdfReader
def dump(path,out):
    r=PdfReader(path); t="\n".join((p.extract_text() or "") for p in r.pages)
    open(out,"w",encoding="utf-8").write(t); print(path,len(r.pages),len(t))
dump(r"Acts_Rules/Document/THE KARNATAKA STAMP ACT 1957.pdf","_tmp_stamp.txt")
dump(r"Acts_Rules/Document/The Karnataka Registration Rules 1965.pdf","_tmp_regrules.txt")
