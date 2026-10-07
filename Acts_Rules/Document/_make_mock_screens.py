"""Builds HTML mock screens (one per Nature of Document) into Mock_Screens/.

Fields, Article rules and the Article decision wizard are generated from
_stamp_article_inputs_data.py so the screens stay in step with the
Stamp_Duty_Article_Determination_Inputs workbook.
"""

import html
import json
import os
import re
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _stamp_article_inputs_data as D  # noqa: E402
from _make_stamp_duty_article_inputs import flow_rows  # noqa: E402

OUT = os.path.join(HERE, "Mock_Screens")
SCREENS = os.path.join(OUT, "screens")

INPUT = {i[0]: i for i in D.INPUTS}
RULES = OrderedDict((r["key"], r) for r in D.RULES)
NATURE = {n[0]: n for n in D.DOCUMENT_NATURES}
INTENT = dict(D.TRANSACTION_INTENTS)

PROPERTY_TAB_IDS = {"AGR-02", "AGR-03", "AGR-11", "AGR-12", "AGR-13", "LON-04"}
VALUATION_IDS = ["GEN-09", "PRP-03", "PRP-07", "PRP-09"]
MOVABLE_IDS = {"PRP-08", "PRP-10"}
PARTY_IDS = {"GEN-05", "GEN-06", "GEN-07"}
DOC_IDS = {"GEN-01", "GEN-02", "GEN-03", "GEN-04"}
CREDIT_IDS = ["GEN-11", "GEN-12", "POA-04", "AGR-14", "AGR-15", "LSE-06", "LSE-11", "STL-03", "PRT-03", "LON-11"]

# (requirement, allowed kinds, note)
PROPERTY = {
    "DN-05": ("Conditional", ["Immovable", "Movable"],
              "Needed when the agreement relates to sale, lease-cum-sale, joint development, mortgage or sale of movables."),
    "DN-06": ("Mandatory", ["Immovable", "Movable"],
              "Deposit of title deeds: immovable property. Pawn / pledge: movable property (goods / jewels)."),
    "DN-07": ("Optional", ["Immovable", "Movable"], "Only if the power is exercised over specific property."),
    "DN-11": ("Mandatory", ["Immovable", "Movable"], "Property that is the subject matter of the award."),
    "DN-14": ("Conditional", ["Immovable", "Movable"], "Pre-filled from the original instrument being cancelled."),
    "DN-15": ("Mandatory", ["Immovable", "Movable"], "One property per lot sold in the public auction."),
    "DN-20": ("Optional", ["Immovable", "Movable"], "Property conveyed by the debtor for the benefit of creditors."),
    "DN-21": ("Mandatory", ["Immovable", "Movable", "TDR"], "Property conveyed."),
    "DN-25": ("Mandatory", ["Movable"], "Goods covered by the delivery order."),
    "DN-27": ("Mandatory", ["Immovable", "Movable"], "At least two properties: one from each party."),
    "DN-28": ("Mandatory", ["Immovable", "Movable"], "Mortgaged property on which further charge is created."),
    "DN-29": ("Mandatory", ["Immovable", "Movable"], "Property gifted."),
    "DN-31": ("Mandatory", ["Immovable", "Movable"], "Property leased."),
    "DN-34": ("Mandatory", ["Immovable", "Movable"], "Property licensed."),
    "DN-36": ("Mandatory", ["Immovable", "Movable"], "Property mortgaged / hypothecated."),
    "DN-37": ("Mandatory", ["Immovable"], "Agricultural land on which the crop is raised."),
    "DN-41": ("Mandatory", ["Immovable", "Movable"], "All properties being partitioned."),
    "DN-42": ("Conditional", ["Immovable"],
              "Needed when immovable property remains with the firm or is allotted to a partner on dissolution."),
    "DN-43": ("Conditional", ["Immovable"], "Needed for reconstruction / amalgamation of LLP (Karnataka property)."),
    "DN-44": ("Conditional", ["Immovable", "TDR"], "Needed when the PoA is to sell or develop property."),
    "DN-47": ("Mandatory", ["Immovable"], "Property being reconveyed to the mortgagor."),
    "DN-48": ("Mandatory", ["Immovable", "Movable"], "Property in which the right / claim is released."),
    "DN-51": ("Mandatory", ["Immovable", "Movable"], "Property settled."),
    "DN-54": ("Mandatory", ["Immovable", "Movable"], "Property under the lease being surrendered."),
    "DN-55": ("Conditional", ["Immovable", "Movable"], "Needed for transfer of trust property."),
    "DN-56": ("Mandatory", ["Immovable"], "Leased property being assigned."),
    "DN-57": ("Mandatory", ["Immovable", "Movable"], "Property under the licence being transferred."),
    "DN-58": ("Conditional", ["Immovable", "Movable"], "Needed when the trust involves transfer of property."),
    "DN-59": ("Mandatory", ["Movable"], "Goods covered by the warrant."),
}

ALLOTMENT = {
    "DN-27": "Show which property each party gives and receives. Duty is on the property of greatest value (Art 26).",
    "DN-29": "Only when there are several donees: show which property goes to which donee.",
    "DN-41": "Allot each property to a share. Duty is per share (Art 39).",
    "DN-51": "Only when several beneficiaries: show which property goes to which beneficiary.",
}

PARTY_LABELS = {
    "DN-01": ("Debtor / Acknowledging party", "Creditor / Sender"),
    "DN-02": ("Obligor (Administrator)", "Obligee"),
    "DN-03": ("Natural parent / Giver", "Adoptive parent / Taker"),
    "DN-04": ("Deponent", ""),
    "DN-05": ("First party", "Second party"),
    "DN-06": ("Borrower / Pledgor", "Lender / Pledgee"),
    "DN-07": ("Donee of the power", "Appointee"),
    "DN-08": ("Valuer", "Party"),
    "DN-09": ("Master / Employer", "Apprentice"),
    "DN-10": ("Company / Subscribers", ""),
    "DN-11": ("Arbitrator", "Parties to the award"),
    "DN-12": ("Obligor", "Obligee"),
    "DN-13": ("Master of the ship", "Lender"),
    "DN-14": ("Executant", "Claimant"),
    "DN-15": ("Selling authority / Court", "Auction purchaser"),
    "DN-16": ("Company", "Shareholder"),
    "DN-17": ("State Bar Council", "Advocate"),
    "DN-18": ("Ship owner", "Charterer"),
    "DN-19": ("Stock exchange member", "Clearing house"),
    "DN-20": ("Debtor", "Creditors"),
    "DN-21": ("Seller / Vendor", "Purchaser"),
    "DN-22": ("Issuing public officer", "Applicant"),
    "DN-23": ("Executant", "Claimant"),
    "DN-24": ("Obligor", "Customs / Excise authority"),
    "DN-25": ("Owner of goods", "Person entitled to delivery"),
    "DN-26": ("Spouse 1", "Spouse 2"),
    "DN-27": ("First party", "Second party"),
    "DN-28": ("Mortgagor", "Mortgagee"),
    "DN-29": ("Donor", "Donee"),
    "DN-30": ("Indemnifier", "Indemnity holder"),
    "DN-31": ("Lessor", "Lessee"),
    "DN-32": ("Company", "Allottee"),
    "DN-33": ("Creditors", "Debtor"),
    "DN-34": ("Licensor", "Licensee"),
    "DN-35": ("Subscribers", "Company"),
    "DN-36": ("Mortgagor / Borrower", "Mortgagee / Lender"),
    "DN-37": ("Mortgagor (Cultivator)", "Mortgagee"),
    "DN-38": ("Notary Public", "Applicant"),
    "DN-39": ("Broker / Agent", "Principal / Client"),
    "DN-40": ("Master of the ship", ""),
    "DN-41": ("Co-owners (sharers)", "Co-owners (sharers)"),
    "DN-42": ("Partners", "Partners"),
    "DN-43": ("Designated partners", "Partners"),
    "DN-44": ("Principal", "Attorney (Agent)"),
    "DN-45": ("Notary Public", "Holder of bill / note"),
    "DN-46": ("Master of the ship", ""),
    "DN-47": ("Mortgagee", "Mortgagor"),
    "DN-48": ("Releasor", "Releasee"),
    "DN-49": ("Borrower", "Lender"),
    "DN-50": ("Surety / Obligor", "Obligee"),
    "DN-51": ("Settlor", "Settlee / Beneficiary"),
    "DN-52": ("Company", "Bearer"),
    "DN-53": ("Shipper", "Carrier"),
    "DN-54": ("Lessee (surrendering)", "Lessor"),
    "DN-55": ("Transferor", "Transferee"),
    "DN-56": ("Assignor (Lessee)", "Assignee"),
    "DN-57": ("Transferor (Licensee)", "Transferee"),
    "DN-58": ("Author of trust", "Trustee"),
    "DN-59": ("Warehouse keeper / Custodian", "Holder"),
}

FAMILY_COLUMN = {"DN-29": 0, "DN-51": 1, "DN-48": 2, "DN-31": 3, "DN-44": 4}

LOOKUPS = {
    "Transaction Intent": [f"{c} - {t}" for c, t in D.TRANSACTION_INTENTS],
    "Nature of Document": [f"{c} - {t}" for c, t, _i, _a in D.DOCUMENT_NATURES],
    "Agreement Subject": [f"{c} - {t}" for c, t, _a in D.AGREEMENT_SUBJECTS],
    "POA Purpose": [f"{c} - {t}" for c, t, _a in D.POA_PURPOSES],
    "Relationship": D.RELATIONSHIPS,
    "Allotting Authority": D.ALLOTTING_AUTHORITIES,
    "Form of Security": ["Deposit of title deeds", "Pawn / pledge of movable property"] + D.SECURITY_FORMS
                        + ["Mortgage of crop", "Further charge"],
}
SPECIAL_OPTIONS = {
    "PRP-03": [f"{c} - {t}" for c, t in D.LOCAL_LIMITS],
    "CMP-04": ["Amalgamation (incl. subsidiary with parent)", "Reconstruction / Demerger"],
    "TRS-02": ["Trust to Trust", "Trust to Trustee / Beneficiary", "Trustee to Trust / Trustee / Beneficiary"],
    "MSC-08": ["Not exempt", "Extract of birth / marriage / death register", "Copy required by law for public record"],
}
AMOUNT2_LABELS = {
    "LON-08": ("Total charge (original + further charges)", "Duty already paid"),
    "LLP-03": ("Market value of Karnataka property", "Consideration"),
}
LSE10_PARTS = ["Average annual royalty", "Average annual payment (final price offer / share of value)",
               "Premium", "Money advanced", "Security deposit incl. performance guarantee", "Fine",
               "Value of estimated resources"]
MOVABLE_CATEGORIES = ["Goods", "Vehicle", "Shares / securities", "Debentures", "Intellectual property rights",
                      "Receivables", "Jewels", "Industrial machinery", "Money", "Other"]

e = html.escape


def slug(code, name):
    return f"{code}_{re.sub(r'[^A-Za-z0-9]+', '_', name).strip('_')[:60]}.html"


def page_name(code):
    return slug(code, NATURE[code][1])


def options_for(iid):
    if iid in SPECIAL_OPTIONS:
        return SPECIAL_OPTIONS[iid]
    allowed = INPUT[iid][5]
    if allowed.startswith("See Lookup_Lists"):
        for key, vals in LOOKUPS.items():
            if key in allowed:
                return vals
        return []
    if allowed == D.YN:
        return []
    if ";" in allowed:
        return [a.strip() for a in allowed.split(";") if a.strip()]
    if ", " in allowed:
        return [a.strip() for a in allowed.split(", ") if a.strip()]
    return [a.strip() for a in allowed.split(" / ") if a.strip()]


def select(name, opts, disabled=False, selected=None):
    out = [f"<select name='{e(name)}'{' disabled' if disabled else ''}><option value=''>-- Select --</option>"]
    for o in opts:
        sel = " selected" if selected and o == selected else ""
        out.append(f"<option{sel}>{e(o)}</option>")
    out.append("</select>")
    return "".join(out)


def radios(name, opts=("Yes", "No")):
    return "<div class='radio-group'>" + "".join(
        f"<label><input type='radio' name='{e(name)}'> {e(o)}</label>" for o in opts) + "</div>"


def checks(name, opts):
    return "<div class='check-group'>" + "".join(
        f"<label><input type='checkbox' name='{e(name)}'> {e(o)}</label>" for o in opts) + "</div>"


def money(name, placeholder="0", ro=False):
    attr = " readonly placeholder='Calculated by system'" if ro else f" placeholder='{placeholder}'"
    return f"<div class='money'><input type='number' name='{e(name)}'{attr}></div>"


def text(name, placeholder="", ro=False):
    attr = " readonly" if ro else ""
    return f"<input type='text' name='{e(name)}' placeholder='{e(placeholder)}'{attr}>"


def rent_grid():
    rows = "".join(
        f"<tr><td>Year {i}</td><td><div class='money'><input type='number' class='rent'></div></td>"
        f"<td class='annual'></td></tr>" for i in range(1, 4))
    return ("<div class='rent-grid'><table class='tbl'><thead><tr><th>Year</th><th>Monthly rent / fee</th>"
            f"<th>Annual</th></tr></thead><tbody>{rows}</tbody></table>"
            "<div class='inline' style='margin-top:6px'><button type='button' class='btn small add-year'>+ Add year"
            "</button><label style='flex:0 0 auto'>Average annual rent</label>"
            "<input type='text' class='aar' readonly placeholder='Auto'></div></div>")


def mv_grid():
    return ("<table class='tbl'><thead><tr><th>Property</th><th>Given by</th><th>Market value (system)</th></tr>"
            "</thead><tbody><tr><td>Property 1</td><td>First party</td><td>Auto</td></tr>"
            "<tr><td>Property 2</td><td>Second party</td><td>Auto</td></tr></tbody></table>"
            "<div class='hint'>System uses the property of greatest value.</div>")


def controls(iid):
    inp = INPUT[iid]
    dtype, source = inp[4], inp[6]
    ro = source.startswith("System")
    parts = [p.strip().lower() for p in dtype.split(" + ")]
    out = []
    for p in parts:
        if p.startswith("dropdown"):
            out.append(select(iid, options_for(iid), disabled=ro))
        elif p.startswith("multi-select"):
            out.append(checks(iid, options_for(iid)))
        elif p.startswith("yes/no"):
            label = "Transferor is a public religious & charitable trust?" if iid == "TRS-02" else ""
            out.append((f"<div class='hint'>{label}</div>" if label else "") + radios(iid))
        elif p in ("doc ref", "ref"):
            out.append(text(iid + "-ref", "Earlier document / registration no."))
        elif p == "article":
            out.append(text(iid + "-art", "Article of original instrument"))
        elif p == "amount x 2":
            a, b = AMOUNT2_LABELS.get(iid, ("Amount 1", "Amount 2"))
            out.append(f"<div class='inline'><div><div class='hint'>{e(a)}</div>{money(iid + '-1')}</div>"
                       f"<div><div class='hint'>{e(b)}</div>{money(iid + '-2')}</div></div>")
        elif p == "amounts":
            out.append("<div class='grid'>" + "".join(
                f"<div><div class='hint'>{e(x)}</div>{money(iid + '-' + str(k))}</div>"
                for k, x in enumerate(LSE10_PARTS)) + "</div>")
        elif p.startswith("amount"):
            out.append(money(iid, ro=ro))
        elif p == "date":
            out.append(f"<input type='date' name='{e(iid)}'>")
        elif p == "number + flag":
            out.append(f"<div class='inline'><input type='number' step='0.01' name='{e(iid)}' placeholder='Years'>"
                       f"{checks(iid + '-flag', ['Perpetual', 'No definite term'])}</div>")
        elif p.startswith("number"):
            out.append(f"<input type='number' name='{e(iid)}'>")
        elif p.startswith("grid"):
            out.append(rent_grid() if iid == "LSE-03" else mv_grid())
        elif p in ("text", "list of matters"):
            continue
        else:
            out.append(text(iid))
    if not out:
        out.append(text(iid, ro=ro))
    return "".join(out)


def field(iid, roles=None, wide=False, label=None):
    inp = INPUT[iid]
    roles = roles or set()
    badges = ""
    if inp[6].startswith("System"):
        badges += "<span class='badge auto'>Auto</span>"
    if "I" in roles:
        badges += "<span class='badge id' title='Used to identify the Article'>Article</span>"
    if "C" in roles:
        badges += "<span class='badge calc' title='Used to calculate duty'>Duty</span>"
    if "E" in roles:
        badges += "<span class='badge ex' title='Exemption / credit check'>Check</span>"
    cls = "field wide" if wide or inp[4].startswith(("Grid", "Amounts", "Multi-select")) else "field"
    return (f"<div class='{cls}'><label>{e(label or inp[2])}<span class='fid'>{iid}</span>{badges}</label>"
            f"<div class='hint'>{e(inp[3])}</div>{controls(iid)}</div>")


def generic_field(label, control, hint="", wide=False):
    cls = "field wide" if wide else "field"
    h = f"<div class='hint'>{e(hint)}</div>" if hint else ""
    return f"<div class='{cls}'><label>{e(label)}</label>{h}{control}</div>"


def nature_inputs(code):
    roles = OrderedDict()
    for r in D.RULES:
        if r["nature"] != code:
            continue
        for i in r["id_in"]:
            roles.setdefault(i, set()).add("I")
        for i in r["calc_in"]:
            roles.setdefault(i, set()).add("C")
        for i in r["adj_in"]:
            roles.setdefault(i, set()).add("E")
    return roles


def rule_keys_in(textval):
    keys = []
    for tok in re.findall(r"(?:=>|else)\s*([0-9][0-9A-Za-z\-]*(?:\([^)]*\)|-[A-Za-z]+)*)", textval):
        if tok in RULES and tok not in keys:
            keys.append(tok)
    return keys


def wizard_data(code):
    rows = [r for r in flow_rows() if r[0] == code]
    steps = OrderedDict()
    referenced = set()
    for _c, _n, step, inp, q, ans, res in rows:
        s = steps.setdefault(step, {"input": inp, "question": q, "options": []})
        opt = {"answer": ans, "result": res, "keys": [], "next": None, "link": None}
        if "=>" in res:
            opt["keys"] = rule_keys_in(res)
            referenced.update(opt["keys"])
        else:
            m = re.search(r"Step\s+(\w+)", res)
            g = re.search(r"Go to (DN-\d+)", res)
            if m and any(r[2] == m.group(1) for r in rows):
                opt["next"] = m.group(1)
            elif g:
                opt["link"] = page_name(g.group(1))
        s["options"].append(opt)
    start = "0" if "0" in steps else next(iter(steps))
    if "0" in steps and "1" in steps and not any(o["answer"] == "No" for o in steps["0"]["options"]):
        steps["0"]["options"].append({"answer": "No", "result": "Step 1", "keys": [], "next": "1", "link": None})
    nature_keys = [k for k, r in RULES.items() if r["nature"] == code]
    rules = {}
    for k in list(OrderedDict.fromkeys(nature_keys + sorted(referenced))):
        r = RULES[k]
        rules[k] = {
            "instrument": r["instrument"], "basis": r["basis"], "duty": r["duty"], "min": r["min"],
            "max": r["max"], "proviso": r["proviso"], "exempt": r["exempt"], "s45a": r["s45a"],
            "calc": ", ".join(f"{i} {INPUT[i][2]}" for i in r["calc_in"]),
        }
    return {"start": start, "steps": steps, "rules": rules}


def nav(prev_tab, next_tab):
    left = f"<button class='btn' data-goto='{prev_tab}'>&larr; Back</button>" if prev_tab else "<span></span>"
    right = f"<button class='btn primary' data-goto='{next_tab}'>Save &amp; Next &rarr;</button>" if next_tab else ""
    return f"<div class='actions'>{left}{right}</div>"


def panel_doc(code):
    n = NATURE[code]
    ex, cl = PARTY_LABELS.get(code, ("Executant", "Claimant"))
    return f"""
<div class='card'><h2>Document type <span class='flowref'>Flow steps 1&ndash;4</span></h2>
<p class='desc'>One transaction per application. The nature of document decides which property, party and transaction
fields are shown in the next tabs.</p>
<div class='grid'>
{generic_field('Application number', text('appno', 'KAV/DR/2026/000123', ro=True), 'Generated by the system (step 2)')}
{field('GEN-03')}
{generic_field('What does this document do? (GEN-01)', select('GEN-01', LOOKUPS['Transaction Intent'], True, f"{n[2]} - {INTENT[n[2]]}"))}
{generic_field('Nature of document (GEN-02)', select('GEN-02', LOOKUPS['Nature of Document'], True, f"{code} - {n[1]}"))}
{field('GEN-04')}
{generic_field('Party labels for this document', text('labels', f"{ex}{' / ' + cl if cl else ''}", ro=True), 'Used on the Parties tab and in the draft deed')}
</div></div>"""


def panel_property(code, roles):
    if code not in PROPERTY:
        return """<div class='empty'><b>No property schedule for this nature of document.</b><br>
Flow step 5 &rarr; No: the application goes straight to party details.</div>"""
    req, kinds, note = PROPERTY[code]
    prop_fields = [i for i in roles if i.startswith("PRP-") or i in PROPERTY_TAB_IDS]
    attr_ids = [i for i in prop_fields if i not in VALUATION_IDS and i not in MOVABLE_IDS]
    val_ids = [i for i in VALUATION_IDS if i in roles]
    mov_ids = [i for i in prop_fields if i in MOVABLE_IDS]
    has_imm = "Immovable" in kinds
    out = [f"<div class='note{' amber' if req != 'Mandatory' else ''}'><b>Property: {req}.</b> {e(note)} "
           f"Allowed kinds: {', '.join(kinds)}.</div>"]
    out.append("""<div class='card prop-list'><h2>Property schedule</h2>
<table class='tbl'><thead><tr><th>#</th><th>Kind</th><th>Location / ID</th><th>Extent / share</th>
<th>Consideration apportioned</th><th>Guidance value</th><th>Stays / 22-A</th><th></th></tr></thead>
<tbody><tr><td colspan='8' style='text-align:center;color:#5f6b7a'>No property added yet</td></tr></tbody></table>
</div>""")
    out.append(f"<div class='card'><h2>Add property <span class='flowref'>Flow steps 6&ndash;19</span></h2>"
               f"<div class='grid'>{generic_field('Property kind (step 6)', radios('kind', kinds))}</div>")
    if has_imm:
        out.append(f"""<h3>Immovable property &ndash; location <span class='flowref'>Steps 8&ndash;11</span></h3>
<div class='grid three'>
{generic_field('Is the property in Karnataka?', radios('in_ka'))}
{generic_field('Agriculture or non-agriculture?', radios('agri', ['Non-agriculture', 'Agriculture']))}
{generic_field('District', select('district', ['Bengaluru Urban', 'Mysuru', 'Belagavi', '...']))}
{generic_field('Taluk', select('taluk', []))}
{generic_field('Hobli', select('hobli', []))}
{generic_field('Village / Ward', select('village', []))}
{generic_field('Property ID (non-agriculture)', text('pid', 'E-Swathu / E-Aasthi / BDA / KHB ID'))}
{generic_field('Survey No. / Hissa No. (agriculture)', '<div class="inline">' + text('sy', 'Survey No.') + text('hissa', 'Hissa No.') + '</div>')}
{generic_field('Full or part extent?', radios('extent_kind', ['Full extent', 'Part extent']))}
</div><div style='margin-top:10px'><button class='btn'>Fetch owners &amp; attributes (step 12)</button></div>
<h3>Imported from source of truth <span class='flowref'>Step 12 &ndash; citizen confirms</span></h3>
<table class='tbl'><thead><tr><th>Owner (executant)</th><th>Share</th><th>Source</th></tr></thead>
<tbody><tr><td>Imported owner name</td><td>1/1</td><td>E-Swathu / Bhoomi RTC</td></tr></tbody></table>
<div class='grid three' style='margin-top:10px'>
{generic_field('Property type', text('i_type', 'Imported', ro=True))}
{generic_field('Property use', text('i_use', 'Imported', ro=True))}
{generic_field('Total extent', text('i_ext', 'Imported', ro=True))}
{generic_field('Khata / RTC type', text('i_khata', 'Imported', ro=True))}
{generic_field('Conversion status', text('i_conv', 'Imported', ro=True))}
{generic_field('Attributes correct?', radios('i_ok', ['Confirm', 'Raise mismatch']))}
</div>
<h3>Property attributes <span class='flowref'>Step 16</span></h3>
<div class='grid'>
{generic_field('Extent / share transferred', '<div class="inline">' + text('ext_tr', 'Area') + select('ext_unit', ['Sq.ft', 'Sq.m', 'Acre-Gunta', 'Undivided share %']) + '</div>')}
{generic_field('Building details', '<div class="inline">' + text('bua', 'Built-up area') + text('floors', 'Floors') + text('yoc', 'Year of construction') + '</div>', 'Needed for the guidance value of buildings')}
{''.join(field(i, roles[i]) for i in attr_ids)}
</div>
<h3>Boundaries, numbers and consideration <span class='flowref'>Step 17</span></h3>
<div class='grid'>
{generic_field('Boundaries', '<div class="grid">' + text('b_n', 'North') + text('b_s', 'South') + text('b_e', 'East') + text('b_w', 'West') + '</div>', wide=True)}
{generic_field('Property numbers (old / new)', text('pnos'))}
{field('GEN-08', roles.get('GEN-08'), label='Consideration apportioned to this property') if 'GEN-08' in roles else ''}
</div>""")
        if val_ids:
            out.append("<h3>Valuation <span class='flowref'>Step 18 &ndash; Guidance Value service</span></h3>"
                       f"<div class='grid'>{''.join(field(i, roles[i]) for i in val_ids)}</div>")
        out.append("<div class='note'>On save, the Stays &amp; Liabilities service checks government / court stays, "
                   "22-B stays, Sec. 22-A prohibited properties, land restrictions and liabilities (steps 20&ndash;21)."
                   "</div>")
        out.append(f"""<h3>Outside Karnataka <span class='flowref'>Step 9</span></h3>
<div class='grid three'>
{generic_field('State', text('o_state'))}
{generic_field('District', text('o_dist'))}
{generic_field('Declared market value', money('o_mv'))}
{generic_field('Property details, number and boundaries', '<textarea rows="2"></textarea>', wide=True)}
</div>""")
    if "Movable" in kinds:
        out.append(f"""<h3>Movable property <span class='flowref'>Step 7a</span></h3>
<div class='grid'>
{generic_field('Category', select('m_cat', MOVABLE_CATEGORIES))}
{generic_field('Description', text('m_desc'))}
{generic_field('Quantity', text('m_qty'))}
{generic_field('Value', money('m_val'))}
{''.join(field(i, roles[i]) for i in mov_ids)}
</div>""")
    if "TDR" in kinds:
        out.append(f"""<h3>Transferable Development Rights <span class='flowref'>Step 7b</span></h3>
<div class='grid'>
{generic_field('TDR certificate (DRC) number', text('tdr_no'))}
{generic_field('Issuing authority', select('tdr_auth', ['BBMP', 'BDA', 'Other ULB']))}
{generic_field('TDR area (sq.m)', text('tdr_area'))}
{generic_field('Originating property', text('tdr_orig', 'Property ID of the originating property'))}
</div>""")
    out.append("<div class='actions'><button class='btn'>Save &amp; add another property</button>"
               "<button class='btn primary'>Save property</button></div></div>")
    return "".join(out)


def panel_parties(code, roles):
    ex, cl = PARTY_LABELS.get(code, ("Executant", "Claimant"))
    cat = select("cat", options_for("GEN-05"))
    rel_used = "GEN-07" in roles
    rel_col = "<th>Relationship to executant <span class='fid'>GEN-07</span></th>" if rel_used else ""
    rel_cell = f"<td>{select('rel', D.RELATIONSHIPS)}</td>" if rel_used else ""
    out = [f"<div class='card'><h2>Party details <span class='flowref'>Flow steps 22&ndash;30</span></h2>"
           "<p class='desc'>Imported owners / transferees are already listed. Add more parties, consenting witnesses "
           "and witnesses. Each person is verified by Aadhaar e-KYC, or by Passport / PAN.</p>"]

    def table(title, with_rel):
        return (f"<h3>{e(title)}</h3><table class='tbl'><thead><tr><th>Name</th>"
                f"<th>Party category <span class='fid'>{'GEN-05' if not with_rel else 'GEN-06'}</span></th>"
                f"{rel_col if with_rel else ''}<th>Represented by</th><th>ID verification</th><th>PAN / Form 97</th>"
                f"</tr></thead><tbody><tr><td>{text('n', 'Name')}</td><td>{cat}</td>{rel_cell if with_rel else ''}"
                f"<td>{select('rep', ['Self', 'PoA holder', 'Guardian of minor', 'Institution representative'])}</td>"
                "<td>Aadhaar e-KYC: pending</td><td>If value &gt; &#8377;20 lakh</td></tr></tbody></table>"
                "<div style='margin-top:6px'><button class='btn small'>+ Add</button></div>")

    out.append(table(ex, False))
    if cl:
        out.append(table(cl, True))
    out.append(table("Witnesses / consenting witnesses", False).replace("<span class='fid'>GEN-05</span>", ""))
    if code in FAMILY_COLUMN:
        col = FAMILY_COLUMN[code]
        art = D.FAMILY_MATRIX_ARTICLES[col][0]
        fam = [r for r in D.RELATIONSHIPS if D.FAMILY_MATRIX[r][col] == "Y"]
        out.append(f"<div class='note amber'><b>Family under {e(art)}:</b> {e(', '.join(fam))}. The relationship "
                   "decides the Article (family / non-family).</div>")
    out.append("</div>")
    return "".join(out)


def panel_allot(code, roles):
    extra = field("PRT-01", roles.get("PRT-01")) if code == "DN-41" and "PRT-01" in roles else ""
    return f"""<div class='card'><h2>Allot property to parties / shares <span class='flowref'>Flow steps 31&ndash;32</span></h2>
<p class='desc'>{e(ALLOTMENT[code])}</p>
<div class='grid'>{extra}</div>
<table class='tbl' style='margin-top:10px'><thead><tr><th>Property</th><th>Allotted to (party / share)</th>
<th>Share %</th><th>Market value (system)</th></tr></thead>
<tbody><tr><td>Property 1</td><td>{select('al1', ['Share 1', 'Share 2', 'Share 3'])}</td><td>{text('p1', '100')}</td><td>Auto</td></tr>
<tr><td>Property 2</td><td>{select('al2', ['Share 1', 'Share 2', 'Share 3'])}</td><td>{text('p2', '100')}</td><td>Auto</td></tr></tbody></table>
</div>"""


def panel_txn(code, roles):
    skip = DOC_IDS | PARTY_IDS | set(CREDIT_IDS) | {"GEN-08", "GEN-09"}
    if code in PROPERTY:
        skip |= {i for i in roles if i.startswith("PRP-") or i in PROPERTY_TAB_IDS}
    if code == "DN-41":
        skip.add("PRT-01")
    ident = [i for i, r in roles.items() if i not in skip and "I" in r]
    calc = [i for i, r in roles.items() if i not in skip and "I" not in r and "C" in r]
    exem = [i for i, r in roles.items() if i not in skip and r == {"E"}]
    if code not in PROPERTY and "GEN-08" in roles:
        calc.insert(0, "GEN-08")
    if code not in PROPERTY and "GEN-09" in roles:
        calc.append("GEN-09")
    if not (ident or calc or exem):
        return """<div class='empty'><b>No further transaction details are needed.</b><br>
The nature of document alone decides the Article.</div>"""
    out = ["<div class='card'><h2>Transaction details <span class='flowref'>Flow step 33</span></h2>"
           "<p class='desc'>Only the fields needed for this nature of document are shown.</p>"]
    if ident:
        out.append("<h3>Details that decide the Article</h3><div class='grid'>"
                   + "".join(field(i, roles[i]) for i in ident) + "</div>")
    if calc:
        out.append("<h3>Details needed to calculate duty</h3><div class='grid'>"
                   + "".join(field(i, roles.get(i)) for i in calc) + "</div>")
    if exem:
        out.append("<h3>Exemption checks (applied automatically by the system)</h3><div class='grid'>"
                   + "".join(field(i, roles[i]) for i in exem) + "</div>")
    out.append("</div>")
    return "".join(out)


def panel_article(code, roles, wiz):
    rows = "".join(
        f"<tr><td><b>{e(k)}</b></td><td>{e(r['instrument'])}</td><td>{e(r['cond'])}</td><td>{e(r['duty'])}</td>"
        f"<td>{e(r['min'])}</td><td>{e(r['max'])}</td></tr>"
        for k, r in RULES.items() if r["nature"] == code)
    credit = [i for i in CREDIT_IDS if i in roles]
    credit_html = ("<div class='grid'>" + "".join(field(i, roles[i]) for i in credit) + "</div>") if credit else \
        "<div class='hint'>No credit / denoting provision for this nature of document.</div>"
    exempts = sorted({r["exempt"] for r in RULES.values() if r["nature"] == code and r["exempt"]})
    ex_opts = exempts or ["(No discretionary exemption configured)"]
    wiz_json = json.dumps(wiz).replace("</", "<\\/")
    return f"""
<div class='card wizard'><h2>Determine the Article <span class='flowref'>Flow steps 34&ndash;35</span></h2>
<p class='desc'>In the live system these answers come from the values already captured; questions are asked only for
missing values. Click through to see how each answer leads to an Article.</p>
<div id='wizard'></div><div id='wizard-result'></div>
<div class='actions'><button class='btn' id='wizard-reset' type='button'>Reset</button>
<span><button class='btn'>Correct the details</button> <button class='btn primary'>Confirm Article</button></span></div>
<script type='application/json' id='wizard-data'>{wiz_json}</script>
</div>
<div class='card'><h2>All Articles possible for this nature of document</h2>
<table class='tbl'><thead><tr><th>Article</th><th>Instrument</th><th>When it applies</th><th>Duty</th><th>Min</th>
<th>Max</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class='card'><h2>Denoting / credit for duty already paid <span class='flowref'>Flow steps 36&ndash;39</span></h2>
<p class='desc'>Sec. 16 / Rule 18 denoting and credit for duty paid on an earlier related instrument between the same
parties for the same property.</p>{credit_html}</div>
<div class='card'><h2>Fee calculation <span class='flowref'>Flow step 40 &ndash; Fee Calculation service</span></h2>
<table class='tbl'><tbody>
<tr><th>Article applied</th><td>Confirmed Article</td></tr>
<tr><th>Stamp duty</th><td>Calculated</td></tr><tr><th>Surcharge</th><td>Calculated</td></tr>
<tr><th>Cess</th><td>Calculated</td></tr><tr><th>Registration fee</th><td>Calculated</td></tr>
<tr><th>Less: denoted / credited duty</th><td>Calculated</td></tr>
<tr><th>Less: rule-based exemption</th><td>Applied automatically</td></tr>
<tr><th>Total payable</th><td><b>Calculated</b></td></tr></tbody></table></div>
<div class='card'><h2>Discretionary exemption <span class='flowref'>Flow steps 41&ndash;43</span></h2>
<div class='grid'>{generic_field('Claim an exemption?', radios('ex_claim'))}
{generic_field('Choose ONE exemption', select('ex_pick', ex_opts))}</div>
<div class='hint'>A claimed exemption is marked Pending Verification and payment is held until the Sub-Registrar approves it.</div>
</div>"""


def panel_payment(code, roles):
    rec = ""
    if code in PROPERTY:
        rec = ("<div class='card'><h2>History of title (recitals) <span class='flowref'>Flow step 44</span></h2>"
               "<table class='tbl'><thead><tr><th>#</th><th>Document / event</th><th>Date</th><th>From</th>"
               "<th>To</th></tr></thead><tbody><tr><td>1</td><td>" + text("r1") + "</td><td>"
               "<input type='date'></td><td>" + text("r1f") + "</td><td>" + text("r1t") + "</td></tr></tbody></table>"
               "<div style='margin-top:6px'><button class='btn small'>+ Add recital</button></div></div>")
    check = ("<div class='note amber'><b>Step 46:</b> total consideration must equal the sum of the consideration "
             "apportioned to each property. If not, the difference is shown and the application cannot proceed.</div>"
             if "GEN-08" in roles and code in PROPERTY else "")
    return rec + f"""<div class='card'><h2>Payment details and covenants <span class='flowref'>Flow step 45</span></h2>
<table class='tbl'><thead><tr><th>Mode</th><th>Amount</th><th>Date</th><th>Reference</th></tr></thead>
<tbody><tr><td>{select('pm', ['Bank transfer', 'Cheque / DD', 'Cash', 'Not applicable'])}</td><td>{money('pa')}</td>
<td><input type='date'></td><td>{text('pr')}</td></tr></tbody></table>
<div style='margin-top:6px'><button class='btn small'>+ Add payment</button></div>
{check}
<div class='field wide' style='margin-top:10px'><label>Covenants (terms)</label><textarea rows='4'></textarea></div></div>"""


def panel_review():
    return """<div class='card'><h2>Review and submit <span class='flowref'>Flow steps 47&ndash;50</span></h2>
<table class='tbl'><tbody>
<tr><th>Document type</th><td>Complete</td></tr><tr><th>Property schedule</th><td>Complete / Not applicable</td></tr>
<tr><th>Parties and witnesses</th><td>Complete</td></tr><tr><th>Transaction details</th><td>Complete</td></tr>
<tr><th>Article confirmed</th><td>Yes</td></tr><tr><th>Fees</th><td>Calculated</td></tr></tbody></table>
<div class='actions'><button class='btn'>Preview draft deed (PDF)</button>
<button class='btn primary'>Submit for scrutiny</button></div>
<div class='hint'>After submission: scrutiny by the Sub-Registrar, approval of any exemption / denoting claim, then
payment, eSign and appointment.</div></div>"""


def build_page(code):
    n = NATURE[code]
    roles = nature_inputs(code)
    wiz = wizard_data(code)
    keys = [k for k, r in RULES.items() if r["nature"] == code]
    req = PROPERTY.get(code, ("Not required",))[0]
    tabs = [("t-doc", "Document Type"), ("t-prop", "Property"), ("t-party", "Parties")]
    if code in ALLOTMENT:
        tabs.append(("t-allot", "Allotment"))
    tabs += [("t-txn", "Transaction Details"), ("t-art", "Article &amp; Duty"), ("t-pay", "Recitals &amp; Payment"),
             ("t-review", "Review &amp; Submit")]
    bodies = {
        "t-doc": panel_doc(code),
        "t-prop": panel_property(code, roles),
        "t-party": panel_parties(code, roles),
        "t-allot": panel_allot(code, roles) if code in ALLOTMENT else "",
        "t-txn": panel_txn(code, roles),
        "t-art": panel_article(code, roles, wiz),
        "t-pay": panel_payment(code, roles),
        "t-review": panel_review(),
    }
    tab_html = "".join(
        f"<button class='tab{' active' if i == 0 else ''}{' na' if t == 't-prop' and code not in PROPERTY else ''}' "
        f"data-tab='{t}'><span class='num'>{i + 1}</span>{lbl}</button>" for i, (t, lbl) in enumerate(tabs))
    panels = []
    for i, (t, _lbl) in enumerate(tabs):
        prev_t = tabs[i - 1][0] if i else None
        next_t = tabs[i + 1][0] if i + 1 < len(tabs) else None
        panels.append(f"<section class='panel{' active' if i == 0 else ''}' id='{t}'>{bodies[t]}{nav(prev_t, next_t)}"
                      "</section>")
    return f"""<!DOCTYPE html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>{e(code)} {e(n[1])} - Kaveri mock screen</title><link rel='stylesheet' href='../assets/style.css'></head>
<body>
<div class='topbar'><div class='brand'>Kaveri Online Services<small>Document Registration &ndash; Pre-Registration Entry</small></div>
<div class='meta'>Mock screen for development &middot; <a href='../index.html'>All natures of document</a></div></div>
<div class='page'>
<div class='page-head'><div><h1>{e(n[1])}</h1>
<div class='sub'>{e(INTENT[n[2]])}</div>
<div class='chips'><span class='chip'>{e(code)}</span><span class='chip'>Article {e(n[3])}</span>
<span class='chip green'>{len(keys)} Article sub-clause(s)</span><span class='chip amber'>Property: {e(req)}</span>
<span class='chip'>{len(roles)} nature-specific field(s)</span></div></div>
<label class='dev-toggle'><input type='checkbox' id='toggle-ids' checked> Show field IDs</label></div>
<div class='tabs'>{tab_html}</div>
{''.join(panels)}
</div><script src='../assets/app.js'></script></body></html>"""


def build_index():
    blocks = []
    for icode, iname in D.TRANSACTION_INTENTS:
        cards = []
        for code, name, intent, art in D.DOCUMENT_NATURES:
            if intent != icode:
                continue
            k = sum(1 for r in RULES.values() if r["nature"] == code)
            f = len(nature_inputs(code))
            req = PROPERTY.get(code, ("Not required",))[0]
            cards.append(f"<a class='ncard' href='screens/{page_name(code)}'><div class='code'>{code} &middot; "
                         f"Article {e(art)}</div><div class='name'>{e(name)}</div><div class='stats'>{k} sub-clause(s)"
                         f" &middot; {f} field(s) &middot; Property: {req}</div></a>")
        blocks.append(f"<div class='intent-block'><h2>{icode} &ndash; {e(iname)}</h2><div class='cards'>"
                      + "".join(cards) + "</div></div>")
    return f"""<!DOCTYPE html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>Kaveri - Mock screens by Nature of Document</title><link rel='stylesheet' href='assets/style.css'></head>
<body><div class='topbar'><div class='brand'>Kaveri Online Services<small>Mock screens &ndash; Nature of Document</small></div>
<div class='meta'>Generated from Stamp_Duty_Article_Determination_Inputs data</div></div>
<div class='page'><div class='page-head'><div><h1>Pre-registration entry &ndash; mock screens</h1>
<div class='sub'>{len(D.DOCUMENT_NATURES)} natures of document grouped by what the document does. Each screen follows
the v13 citizen pre-registration flow: Document Type, Property, Parties, Allotment (where needed), Transaction Details,
Article &amp; Duty, Recitals &amp; Payment, Review.</div></div></div>
<input id='search' class='search' type='text' placeholder='Search nature of document, code or Article...'>
{''.join(blocks)}
<p class='hint' style='margin-top:24px'>Field IDs (e.g. AGR-02) match the Input_Catalogue sheet of
Stamp_Duty_Article_Determination_Inputs.xlsx. Badges: <span class='badge id'>Article</span> decides the Article,
<span class='badge calc'>Duty</span> used in the calculation, <span class='badge ex'>Check</span> exemption / credit,
<span class='badge auto'>Auto</span> filled by the system.</p>
</div><script src='assets/app.js'></script></body></html>"""


def main():
    os.makedirs(SCREENS, exist_ok=True)
    for f in os.listdir(SCREENS):
        if f.endswith(".html"):
            os.remove(os.path.join(SCREENS, f))
    for code, *_rest in D.DOCUMENT_NATURES:
        with open(os.path.join(SCREENS, page_name(code)), "w", encoding="utf-8") as fh:
            fh.write(build_page(code))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(build_index())
    print(f"Wrote {len(D.DOCUMENT_NATURES)} screens + index to {OUT}")


if __name__ == "__main__":
    main()
