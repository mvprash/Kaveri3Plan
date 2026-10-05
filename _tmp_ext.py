import docx
from docx.table import Table
from docx.text.paragraph import Paragraph
d=docx.Document(r'Requirement Discussions/Daily Reports/Consolidated_Requirement_Discussions_25082026_to_11092026.docx')
on=False
for el in d.element.body.iterchildren():
    tag=el.tag.split('}')[1]
    if tag=='p':
        t=Paragraph(el,d).text
        if t.startswith('4. 01-09-2026'): on=True
        elif t.startswith('5. ') and on: on=False
        if on and t.strip(): print('P|',t)
    elif tag=='tbl' and on:
        tb=Table(el,d)
        print('TABLE')
        for r in tb.rows:
            cells=[]
            for c in r.cells:
                if c.text not in cells: cells.append(c.text)
            print('  R|',' || '.join(x.replace('\n',' / ') for x in cells))
