# -*- coding: utf-8 -*-
"""Generate the vertical draw.io swimlane diagram (and PNG) for matters decided by the District Registrar
during registration: applications the Sub-Registrar refers (condonation of delay, Registration Act Sec. 25 / 34;
Sec. 45-A under-valuation and Sec. 33 impounded instruments, Karnataka Stamp Act, 1957) and appeals /
applications against a Sub-Registrar's refusal to register (Registration Act Sec. 72–77).

Uses the same layout as the other Document Registration process diagrams.
"""
from __future__ import annotations

import _make_citizen_preregistration_diagram as base
from _make_citizen_preregistration_diagram import LEGEND, Diagram, label, lane_title

STEM = "District_Registrar_Referral_Process_v3"
JUMP = "jumpStyle=arc;jumpSize=12;"


def district_registrar_referral() -> Diagram:
    col_a, col_b, col_c = 160, 450, 740
    lanes = [
        ("sro", lane_title("Sub-Registrar", "Referring office"), 360),
        ("dr", lane_title("District Registrar", "Registrar under the Registration Act; Deputy Commissioner under the Karnataka Stamp Act"), 900),
        ("sys", lane_title("Kaveri System", "Kaveri Online Services"), 440),
        ("party", lane_title("Applicant / Parties", "Portal, SMS, email"), 380),
        ("ext", lane_title("External Systems", "Khajane-II / payment gateway, DSC certifying authority"), 300),
    ]
    d = Diagram(
        "District Registrar Referral",
        "Document Registration — District Registrar Referral Process (v3)",
        "How the District Registrar decides an application referred by the Sub-Registrar while registration is kept pending: "
        "condonation of delay in presentation or appearance (Sec. 25, 34, Registration Act), under-valuation (Sec. 45-A) and "
        "impounded instruments (Sec. 33, 37, 39, 41, Karnataka Stamp Act, 1957); the order goes back to the Sub-Registrar, "
        "who resumes registration. Section D: appeal or application against a Sub-Registrar's refusal to register (Sec. 72–77, Registration Act). "
        "Section E: further remedies against the District Registrar's order",
        lanes, rows=37,
    )
    for row, text in [(1.9, "A–C. APPLICATIONS REFERRED BY THE SUB-REGISTRAR"),
                      (19.1, "D. APPEAL / APPLICATION AGAINST REFUSAL TO REGISTER (Sec. 72–77)"),
                      (31.1, "E. FURTHER REMEDIES AGAINST THE DISTRICT REGISTRAR'S ORDER")]:
        d._vertex(f"sec_{row}", f"<b>{text}</b>",
                  "text;html=1;align=left;verticalAlign=top;fontSize=13;fontColor=#1f4e79;",
                  d.lane_x["dr"] + 12, base.TITLE_H + base.LANE_HEADER_H + row * base.ROW_H + 6, 640, 26)
    d.lane_centre["dr"] = col_b
    n = d.node
    n("s", "sro", 0, "start", "Start")
    n("prev", "sro", 1, "ext", label("", "Application referred by the Sub-Registrar; registration kept pending",
                                     "Presentation flow: step 18 (condonation of delay), step 34a (Sec. 45-A) or step 34b (Sec. 33)"),
      box_w=260, box_h=130)
    n("case", "sys", 2, "task", label("1", "Create the referral case in the District Registrar's queue: case number, type, application and document, the Sub-Registrar's reasons and Minute Book entry; status Pending with District Registrar; notify the applicant"), box_w=320, box_h=150)
    n("open", "dr", 3, "task", label("2", "Open the referral case: view the document, the presentation and admission endorsements and the Sub-Registrar's reasons"), box_w=300, box_h=120)
    n("type", "dr", 4, "decision", label("3", "Type of referral?"), box_w=200, box_h=120)

    # A. Condonation of delay
    n("a_exam", "dr", 5, "task", label("4A", "<b>Condonation of delay.</b> Examine the written application: the reason for the delay (urgent necessity or unavoidable accident) and the period of delay in presentation or appearance; call for an explanation if needed", "Sec. 25(1), 34(1) proviso; Rules 51, 55(i)"), cx=col_a, box_w=250, box_h=156)
    n("a_fine", "dr", 6.5, "task", label("5A", "Kaveri calculates the fine by the length of delay beyond the time allowed: up to 1 week 1×, up to 1 month 2×, up to 2 months 5×, up to 4 months 10× the registration fee", "Rules 52–54: in addition to the registration fee; once for duplicates; later occasions only the difference"), cx=col_a, box_w=250, box_h=156)
    n("a_ord", "dr", 8, "task", label("6A", "Pass the order with reasons: condone the delay and direct acceptance for registration / admission to registration on payment of the fine of ₹… for a delay of …, or reject the application", "Sec. 25(1), 34(1) proviso; Rule 55(ii)"), cx=col_a, box_w=250, box_h=156)

    # B. Sec. 45-A under-valuation
    n("b_notice", "dr", 5, "task", label("4B", "<b>Sec. 45-A under-valuation.</b> Note the 90-day target date from receipt of the reference; issue notice to the parties with the hearing date; they may file objections and evidence of value", "Sec. 45-A(2), Karnataka Stamp Act"), cx=col_b, box_w=250, box_h=156)
    n("b_inq", "dr", 6.5, "task", label("5B", "Hear the parties and hold the inquiry: inspect the property or call for reports if needed, compare with the guidance value and sale instances; determine the market value and the proper duty"), cx=col_b, box_w=250, box_h=156)
    n("b_ord", "dr", 8, "task", label("6B", "Pass the order, as far as possible within 90 days of the reference: market value, proper duty and the difference payable", "Sec. 45-A(2), (4). Not paid within 90 days of the order: interest at 12% a year. Appeal: Regional Commissioner, after depositing 50% of the difference, Sec. 45-A(5)"), cx=col_b, box_w=250, box_h=156)

    # C. Sec. 33 impounded instrument
    n("c_exam", "dr", 5, "task", label("4C", "<b>Sec. 33 impounded instrument.</b> Examine the original instrument sent by the Sub-Registrar: the proper Article, the duty chargeable and the duty paid", "Sec. 37(2), 39(1)"), cx=col_c, box_w=250, box_h=156)
    n("c_ord", "dr", 6.5, "task", label("5C", "Pass the order: certify that it is duly stamped or not chargeable; or require the proper duty or the deficit, with a penalty of ₹5 or up to ten times the deficit", "Sec. 39(1)(a), (b); penalty may be remitted if impounded only under Sec. 13 or 14"), cx=col_c, box_w=250, box_h=156)

    # Common: order, payment and return
    n("dsc", "dr", 9.5, "task", label("7", "Sign the order with the DSC"))
    n("ca", "ext", 9.5, "task", label("8", "Certifying authority: certificate valid and not revoked"))
    n("notify", "sys", 10.5, "task", label("9", "Record the order number and date against the document; send the order to the applicant (SMS, email, portal) and a copy to the Sub-Registrar", "Sec. 45-A(4); Rule 55(ii)"), box_w=300, box_h=130)
    n("payq", "sys", 11.5, "decision", label("10", "Amount payable under the order?", "Fine, duty difference, or deficit duty and penalty"), box_w=240, box_h=140)
    n("pay", "party", 12.5, "task", label("11", "Pay the amount due through Add Challan (online or challan)"))
    n("gw", "ext", 13.5, "task", label("12", "Khajane-II / payment gateway: confirm the payment or challan"))
    n("paid", "sys", 14.5, "decision", label("13", "Paid?"))
    n("endorse", "dr", 15.5, "task", label("14", "Endorse the payment: for Sec. 33, certify on the instrument that the proper duty and penalty were levied, with the amount of each and the name and residence of the payer; for condonation and Sec. 45-A, record the challan against the order", "Sec. 41(1), Karnataka Stamp Act"), box_w=320, box_h=150)
    n("ret", "sys", 16.5, "task", label("15", "Return the document and the order to the Sub-Registrar with the payment status; close the referral case and update the application status", "Sec. 39(3); Rule 116"), box_w=300, box_h=130)
    n("back", "sro", 17.5, "ext", label("", "Sub-Registrar resumes registration",
                                        "Presentation flow: step 19 (condonation) or step 35 (Sec. 45-A / Sec. 33). Rejected or not paid: refusal, Rule 171(vi), (viii), (xvi)"),
      box_w=280, box_h=130)
    n("e", "sro", 18.4, "end", "End")

    # D. Appeal / application against refusal to register
    n("d_s", "party", 19.6, "start", "Start")
    n("d_prev", "party", 20.5, "ext", label("", "Registration refused by the Sub-Registrar; reasons recorded in Book 2 and a copy given",
                                            "Presentation flow: step 49"), box_w=260, box_h=120)
    n("d_file", "party", 21.5, "task", label("16", "Within 30 days of the refusal order, file in person or through an agent holding an authenticated power of attorney (not by post): an appeal under Sec. 72 (any ground other than denial of execution) or an application under Sec. 73 (denial of execution), with a copy of the reasons and verified like a plaint", "Sec. 72(1), 73; Rules 175, 176, 187, 191"), box_w=320, box_h=156)
    n("d_case", "sys", 22.5, "task", label("17", "Create the appeal / application case in the District Registrar's queue with the refusal order, the Book 2 reasons and the original document; check the 30-day limit", "Document held by another person: admitted pending its production, Rule 175(ii)"), box_w=300, box_h=150)
    n("d_admit", "dr", 23.5, "decision", label("18", "Admissible? Filed in time by a person entitled; Sec. 73 application verified"), box_w=260, box_h=150)
    n("d_nm", "dr", 23.5, "reject", label("", "Not admitted: returned for verification within a stated time, or rejected as not maintainable (time-barred, or document withdrawn by the presenter)", "Rules 178, 190; delay in getting the copy of reasons may be excused, Rule 191(ii)"), cx=700, box_w=220, box_h=150)
    n("d_nm_end", "dr", 23.5, "end", "End", cx=850)
    n("d_hear", "sys", 24.5, "task", label("19", "Fix the hearing date; notify the applicant and publish it on the Registrar's notice board; the applicant pays the process fee within a week for notice to the respondent and summons to witnesses", "Rule 179(ii)–(iv); Article XXVI of the Table of Fees"), box_w=300, box_h=150)
    n("d_enq", "dr", 25.5, "task", label("20", "Hear the parties and enquire whether the document was executed and whether the legal requirements are met (Sec. 19–21, 25, etc.); summon and examine witnesses as a Civil Court, adjourn for sufficient cause and decide who bears the costs; record on proceeding sheets (Form 27)", "Sec. 72(1), 74, 75(4); Rules 179, 181, 191(ii), (iii)"), box_w=340, box_h=156)
    n("d_dec", "dr", 26.5, "decision", label("21", "Registration directed?", "Refused if neither party appears, the applicant is absent and the respondent contests, or notice is not served for want of the process fee (Rule 179(v))"), box_w=280, box_h=156)
    n("d_reg", "dr", 27.6, "task", label("22", "Order directing registration, signed with the DSC: recorded separately in the file of appeal orders (not endorsed on the document); abstract endorsed on the appeal; sent to the applicant and the Sub-Registrar (both offices if different); re-presentation unblocked", "Sec. 72(1), 75(1); Rules 180, 183, 185. Minor / unsound-mind ground: register only if the executant appears again and admits execution (Rule 188)"), cx=col_a, box_w=280, box_h=156)
    n("d_ref", "dr", 27.6, "task", label("22a", "Order refusing to direct registration, signed with the DSC: reasons recorded in Book 2; free copy of the reasons on application; sent to the applicant and the Sub-Registrar. No further appeal", "Sec. 76; Rules 179(vii), 180, 183, 186"), cx=col_c, box_w=260, box_h=156)
    n("d_re", "sro", 28.8, "ext", label("", "Document re-presented within 30 days of the order: the Sub-Registrar registers it, taking effect from the first presentation; note in Book 2 under the original refusal", "Sec. 72(2), 75(2), (3); Rule 184. Presentation flow"), box_w=280, box_h=150)
    n("d_suit", "party", 28.8, "ext", label("", "Civil suit within 30 days of the Registrar's refusal for a decree directing registration", "Sec. 77; next stage outside Kaveri"), box_w=260, box_h=120)
    n("d_e1", "sro", 29.8, "end", "End")
    n("d_e2", "party", 29.8, "end", "End")

    # E. Further remedies against the District Registrar's order
    rem_a, rem_b, rem_c, rem_d = 120, 340, 560, 780
    n("e_s", "party", 31.6, "start", "Start")
    n("e_agg", "party", 32.5, "task", label("23", "Party aggrieved by the District Registrar's order (step 9 or step 22a) chooses a further remedy"), box_w=260, box_h=110)
    n("e_q", "sys", 33.3, "decision", label("24", "Order made under?"), box_w=200, box_h=110)
    n("e_a", "dr", 34.5, "ext", label("", "Condonation of delay (A): no appeal. The Inspector General may remit all or part of the fine above the registration fee", "Sec. 70, Registration Act"), cx=rem_a, box_w=210, box_h=170)
    n("e_b", "dr", 34.5, "ext", label("", "Sec. 45-A order (B): appeal to the Regional Commissioner after depositing 50% of the duty difference; deposit refunded if the duty paid is found sufficient. The Chief Controlling Revenue Authority may also revise the order within 5 years", "Sec. 45-A(5), 53-A, Karnataka Stamp Act"), cx=rem_b, box_w=210, box_h=170)
    n("e_c", "dr", 34.5, "ext", label("", "Sec. 39 impounding order (C): no appeal. Refund of penalty (apply within 1 year of payment) or of excess duty (within 6 months of registration) by the Chief Controlling Revenue Authority; revision within 5 years; reference to the High Court", "Sec. 44, 53, 53-A, 54, Karnataka Stamp Act"), cx=rem_c, box_w=210, box_h=170)
    n("e_d", "dr", 34.5, "ext", label("", "Refusal to direct registration (D): no appeal; civil suit within 30 days for a decree directing registration", "Sec. 76(2), 77, Registration Act (see step 22a)"), cx=rem_d, box_w=210, box_h=170)
    n("e_end", "dr", 35.8, "end", "End")

    e = d.edge
    down = "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
    e("s", "prev", extra=down)
    e("prev", "case", "Referred", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;", label_pos=-0.8)
    e("case", "open", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("open", "type", extra=down)
    e("type", "a_exam", "Condonation of delay (Sec. 25 / 34)", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;",
      points=[(d.lane_x["dr"] + col_a, d.cy("type"))], label_pos=-0.4)
    e("type", "b_notice", "Sec. 45-A", extra=down)
    e("type", "c_exam", "Sec. 33 impounding", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;",
      points=[(d.lane_x["dr"] + col_c, d.cy("type"))], label_pos=-0.4)
    e("a_exam", "a_fine", extra=down)
    e("a_fine", "a_ord", extra=down)
    e("b_notice", "b_inq", "Notice to the parties", extra=down)
    e("b_inq", "b_ord", extra=down)
    e("c_exam", "c_ord", extra=down)
    e("a_ord", "dsc", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;", points=[(d.lane_x["dr"] + col_a, d.cy("dsc"))])
    e("b_ord", "dsc", extra=down)
    e("c_ord", "dsc", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;", points=[(d.lane_x["dr"] + col_c, d.cy("dsc"))])
    e("dsc", "ca", "Validate certificate", extra="exitX=1;exitY=0.3;entryX=0;entryY=0.3;startArrow=block;startFill=1;" + JUMP)
    e("dsc", "notify", "Signed order", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;", points=[(d.cxn("dsc"), d.cy("notify"))], label_pos=-0.5)
    e("notify", "payq", extra=down)
    e("payq", "pay", "Yes", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;", label_pos=-0.7)
    no_x = d.lane_x["sys"] + 40
    e("payq", "ret", "No — rejected, no difference, or duly stamped", extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;" + JUMP,
      points=[(no_x, d.cy("payq")), (no_x, d.cy("ret"))], label_pos=-0.6)
    e("pay", "gw", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("gw", "paid", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;", points=[(d.cxn("gw"), d.cy("paid"))])
    e("paid", "endorse", "Yes", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;" + JUMP,
      points=[(d.cxn("endorse"), d.cy("paid"))], label_pos=-0.6)
    e("paid", "ret", "No — not paid in time, or Sec. 45-A appeal filed", extra=down, label_pos=-0.4)
    e("endorse", "ret", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;" + JUMP, points=[(d.cxn("endorse"), d.cy("ret"))])
    e("ret", "back", "Order and document returned", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;",
      points=[(d.cxn("ret"), d.cy("back"))], label_pos=-0.3)
    e("back", "e", extra=down)

    dr_abs = lambda cx: d.lane_x["dr"] + cx  # noqa: E731
    e("d_s", "d_prev", extra=down)
    e("d_prev", "d_file", extra=down)
    e("d_file", "d_case", "Appeal / application", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;", label_pos=-0.6)
    e("d_case", "d_admit", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("d_admit", "d_nm", "No", back=True, extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    e("d_nm", "d_nm_end", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    e("d_admit", "d_hear", "Yes — admitted", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;",
      points=[(dr_abs(col_b), d.cy("d_hear"))], label_pos=-0.6)
    e("d_hear", "d_enq", "Hearing date", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;", label_pos=-0.6)
    e("d_enq", "d_dec", extra=down)
    e("d_dec", "d_reg", "Yes", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;", points=[(dr_abs(col_a), d.cy("d_dec"))])
    e("d_dec", "d_ref", "No", back=True, extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;", points=[(dr_abs(col_c), d.cy("d_dec"))])
    e("d_reg", "d_re", "Order to register", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;",
      points=[(dr_abs(col_a), d.cy("d_re"))], label_pos=-0.4)
    e("d_ref", "d_suit", "Refused", back=True, extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;",
      points=[(dr_abs(col_c), d.cy("d_suit"))], label_pos=-0.4)
    e("d_re", "d_e1", extra=down)
    e("d_suit", "d_e2", extra=down)

    e("e_s", "e_agg", extra=down)
    e("e_agg", "e_q", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    bus_y = d.nodes["e_a"][1] - 30
    for tgt, cx, text in [("e_a", rem_a, "Sec. 25 / 34"), ("e_b", rem_b, "Sec. 45-A"),
                          ("e_c", rem_c, "Sec. 39"), ("e_d", rem_d, "Sec. 72 / 75")]:
        e("e_q", tgt, text, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;",
          points=[(d.cxn("e_q"), bus_y), (dr_abs(cx), bus_y)], label_pos=0.85)
    end_y = d.cy("e_end")
    for src, cx in [("e_a", rem_a), ("e_b", rem_b)]:
        e(src, "e_end", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;", points=[(dr_abs(cx), end_y)])
    for src, cx in [("e_c", rem_c), ("e_d", rem_d)]:
        e(src, "e_end", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;", points=[(dr_abs(cx), end_y)])
    d.legend(LEGEND)
    return d


def main():
    base.STEM = STEM
    xml = district_registrar_referral().xml()
    drawio = base.OUT_DIR / f"{STEM}.drawio"
    drawio.write_text(xml, encoding="utf-8")
    print("Wrote", drawio)
    print("Wrote", base.export_png(xml))


if __name__ == "__main__":
    main()
