# -*- coding: utf-8 -*-
"""Generate the vertical draw.io swimlane diagram (and PNG) for the refund of the registration
fee, copying fees and stamp duty when a document is withdrawn before registration.

Uses the same layout as the other Document Registration process diagrams.
"""
from __future__ import annotations

import _make_citizen_preregistration_diagram as base
from _make_citizen_preregistration_diagram import (LANE_HEADER_H, LEGEND, ROW_H, TITLE_H, Diagram, label,
                                                    lane_title)

STEM = "Refund_Process_v1"
JUMP = "jumpStyle=arc;jumpSize=12;"


def refund_process() -> Diagram:
    side_cx = 125
    lanes = [
        ("party", lane_title("Applicant", "Presenter / payer / e-stamp purchaser"), 380),
        ("sro", lane_title("Sub-Registrar", "Registering Officer who levied the fee"), 340),
        ("sanc", lane_title("Sanctioning Authority", "District Registrar (up to 3 years); Inspector General of Registration (up to 5 years)"), 360),
        ("dcs", lane_title("Deputy Commissioner of Stamps", "District"), 420),
        ("sys", lane_title("Kaveri System", "Kaveri Online Services"), 440),
        ("ext", lane_title("External Systems", "Khajane-II / treasury, e-Stamp system (CRA)"), 300),
    ]
    d = Diagram(
        "Refund Process",
        "Document Registration — Refund of Fees and Stamp Duty on Withdrawal (v1)",
        "When the presenter withdraws a document before the order of registration: A. half the registration fee and all the copying fees are "
        "refunded on sanction by the District Registrar or the Inspector General of Registration (Rules 193–195, Karnataka Registration Rules); "
        "B. the stamp duty is allowed by the Deputy Commissioner of Stamps on a separate application (Chapter V, Karnataka Stamp Act; "
        "Rules 31 and 32, e-Stamping Rules)",
        lanes, rows=21,
    )

    for row, text in [(2, "A. REGISTRATION FEE AND COPYING FEE REFUND (Rules 193–195)"),
                      (11, "B. STAMP DUTY REFUND (Karnataka Stamp Act, Chapter V; e-Stamping Rules 31, 32)")]:
        d._vertex(f"sec_{row}", f"<b>{text}</b>",
                  "text;html=1;align=left;verticalAlign=top;fontSize=13;fontColor=#1f4e79;",
                  d.lane_x["sro"] + 12, TITLE_H + LANE_HEADER_H + row * ROW_H + 6, 640, 26)

    n = d.node
    n("s", "party", 0, "start", "Start")
    n("prev", "party", 1, "ext", label("", "Document withdrawn before the order of registration", "Previous stage: Presentation, Photo &amp; Thumb Registration Process, section E (Rule 193(i))"), box_w=260, box_h=110)

    # A. Registration fee and copying fee refund
    n("a_app", "party", 2, "task", label("1", "Submit the fee refund application (pre-filled from the withdrawal) with the payer's bank account", "Lodged with the Registering Officer who levied the fee (Rule 195(i))"), box_w=260, box_h=120)
    n("a_calc", "sys", 3, "task", label("2", "Calculate the refundable amount: half the registration fee and all the copying fees", "Not refunded: delay fine under Sec. 25 (except under Sec. 70); fees for commission, summons, attendance and travel once earned or spent (Rule 193(ii) and note)"), box_w=300, box_h=140)
    n("a_sro", "sro", 4, "task", label("3", "Verify the application against the withdrawal entry in the Minute Book and the fee receipts; enter it in the refund register (Form 28) and forward it to the sanctioning authority", "Rules 23(f), 195"), box_w=290, box_h=140)
    n("a_time", "sys", 5, "decision", label("4", "Within 3 years of the date of collection?", "Rule 194"), cx=side_cx, box_w=210, box_h=130)
    n("a_t5", "sys", 6, "decision", label("5", "Within 5 years of the date of collection?", "Rule 194"), cx=side_cx, box_w=210, box_h=130)
    n("a_sanc", "sanc", 7, "task", label("6", "Examine the application and pass the order: sanction the refund, or reject it with reasons", "District Registrar up to 3 years; Inspector General of Registration up to 5 years (Rule 194)"), box_w=280, box_h=130)
    n("a_ok", "sys", 8, "decision", label("7", "Refund sanctioned?"), cx=side_cx)
    n("a_bill", "sys", 9, "task", label("8", "Generate the refund bill for the sanctioned amount and send it to the treasury for credit to the payer's bank account"), box_w=300, box_h=120)
    n("a_tr", "ext", 9, "task", label("", "Khajane-II / treasury: credit the refund to the payer's account and confirm"))
    n("a_done", "sys", 10, "task", label("9", "Update the refund register (Form 28) with the outcome — refunded, rejected or time-barred — and notify the applicant", "Rule 195(ii)"), box_w=300, box_h=120)

    # B. Stamp duty refund
    n("b_q", "party", 11, "decision", label("10", "Claim a refund of the stamp duty paid for the withdrawn document?"), box_w=220, box_h=136)
    n("b_app", "party", 12, "task", label("11", "Apply to the Deputy Commissioner of Stamps in Form 4 with the original e-stamp certificate and the withdrawn document, given up to be cancelled", "e-Stamping Rule 31; an authorised person needs the purchaser's notarised authorisation (Form 4)"), box_w=300, box_h=140)
    n("b_time", "dcs", 13, "decision", label("12", "Applied within 6 months of the date of the instrument?", "1 year after first execution if undated (Sec. 48(3))"), cx=120, box_w=220, box_h=146)
    n("b_rej_t", "dcs", 13, "reject", label("", "Time-barred: allowance not admissible", "Sec. 48"), cx=325, box_w=170, box_h=90)
    n("b_ver", "dcs", 14, "task", label("13", "Verify: e-stamp certificate genuine and not used or locked; a Sec. 47(c) ground applies (instrument incomplete, failed of its purpose, void or unfit); no legal proceeding started in which it could be given in evidence", "Sec. 47 and proviso; Karnataka Stamp Rules 16, 17"), cx=165, box_w=300, box_h=150)
    n("b_es", "ext", 14, "task", label("", "e-Stamp system (CRA): certificate details and status"))
    n("b_ok", "dcs", 15, "decision", label("14", "Allowance admissible?"), cx=120, box_w=200, box_h=124)
    n("b_rej", "dcs", 15, "reject", label("", "Rejected: order with reasons", "Appeal to the Chief Controlling Revenue Authority within 60 days (Sec. 52(2))"), cx=325, box_w=170, box_h=130)
    n("b_cancel", "dcs", 16, "task", label("15", "Cancel the e-stamp certificate, endorse the cancellation with signature and seal, and lock it in the e-stamp database; allow the duty less 20 paise per rupee", "Sec. 51; e-Stamping Rule 32(1)"), cx=165, box_w=300, box_h=140)
    n("b_lock", "ext", 16, "task", label("", "e-Stamp system: certificate cancelled and locked against reuse"))
    n("b_pay", "dcs", 17, "task", label("16", "Pay the refund by treasury cheque in favour of the person in whose name the e-stamp certificate was issued; enter it in the register of cancelled certificates", "Monthly report to the Chief Controlling Revenue Authority (e-Stamping Rule 32(2), (3))"), cx=165, box_w=300, box_h=140)
    n("b_tr", "ext", 17, "task", label("", "Treasury: cheque issued to the e-stamp purchaser"))
    n("b_sys", "sys", 18, "task", label("17", "Record the stamp duty refund against the withdrawn application and notify the applicant"), box_w=280)
    n("b_recv", "party", 19, "task", label("18", "Applicant receives the stamp duty refund"), box_w=240)
    n("e", "party", 20, "end", "End")

    e = d.edge
    down = "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
    right = "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
    to_right = "exitX=1;exitY=0.5;entryX=0.5;entryY=0;"
    to_left = "exitX=0;exitY=0.5;entryX=0.5;entryY=0;"
    ext_link = right + "startArrow=block;startFill=1;" + JUMP
    sys_r = d.lane_x["sys"] + d.lane_w["sys"]

    def entry_x(node: str, x_abs: int) -> str:
        x, _, w, _ = d.nodes[node]
        return f"{(x_abs - x) / w:.2f}"

    e("s", "prev", extra=down)
    e("prev", "a_app", "Withdrawn", extra=down)
    e("a_app", "a_calc", extra=to_right)
    e("a_calc", "a_sro", extra=to_left)
    e("a_sro", "a_time", extra=to_right)
    e("a_time", "a_sanc", "Yes — District Registrar", extra=to_left, label_pos=-0.6)
    e("a_time", "a_t5", "No", extra=down)
    sanc_in = d.nodes["a_sanc"][0] + d.nodes["a_sanc"][2] * 4 // 5
    e("a_t5", "a_sanc", "Yes — Inspector General", extra="exitX=0;exitY=0.5;entryX=0.8;entryY=0;" + JUMP,
      points=[(sanc_in, d.cy("a_t5"))], label_pos=-0.6)
    e("a_t5", "a_done", "No — time-barred (Rule 194)", back=True, extra="exitX=1;exitY=0.5;entryX=1;entryY=0.35;" + JUMP,
      points=[(sys_r - 15, d.cy("a_t5")), (sys_r - 15, d.nodes["a_done"][1] + d.nodes["a_done"][3] * 35 // 100)], label_pos=-0.8)
    e("a_sanc", "a_ok", "Order", extra=to_right)
    e("a_ok", "a_bill", "Yes", extra=f"exitX=0.5;exitY=1;entryX={entry_x('a_bill', d.cxn('a_ok'))};entryY=0;")
    e("a_ok", "a_done", "No — rejected", back=True, extra="exitX=1;exitY=0.5;entryX=1;entryY=0.65;" + JUMP,
      points=[(sys_r - 40, d.cy("a_ok")), (sys_r - 40, d.nodes["a_done"][1] + d.nodes["a_done"][3] * 65 // 100)], label_pos=-0.6)
    e("a_bill", "a_tr", "Refund bill", extra=ext_link)
    e("a_bill", "a_done", "Credited", extra=down)
    e("a_done", "b_q", extra=to_left)

    party_l = d.lane_x["party"] + 30
    e("b_q", "e", "No", extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;",
      points=[(party_l, d.cy("b_q")), (party_l, d.cy("e"))], label_pos=-0.9)
    e("b_q", "b_app", "Yes", extra=down)
    e("b_app", "b_time", extra=to_right)
    e("b_time", "b_rej_t", "No", back=True, extra=right)
    e("b_time", "b_ver", "Yes", extra=f"exitX=0.5;exitY=1;entryX={entry_x('b_ver', d.cxn('b_time'))};entryY=0;")
    e("b_ver", "b_es", "Verify certificate", extra=ext_link)
    e("b_ver", "b_ok", extra=f"exitX={entry_x('b_ver', d.cxn('b_ok'))};exitY=1;entryX=0.5;entryY=0;")
    e("b_ok", "b_rej", "No", back=True, extra=right)
    e("b_ok", "b_cancel", "Yes", extra=f"exitX=0.5;exitY=1;entryX={entry_x('b_cancel', d.cxn('b_ok'))};entryY=0;")
    e("b_cancel", "b_lock", "Cancel and lock", extra=ext_link)
    e("b_cancel", "b_pay", extra=down)
    e("b_pay", "b_tr", "Cheque", extra=ext_link)
    e("b_pay", "b_sys", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("b_sys", "b_recv", extra=to_left)
    e("b_recv", "e", extra=down)
    d.legend(LEGEND)
    return d


def main():
    base.STEM = STEM
    xml = refund_process().xml()
    drawio = base.OUT_DIR / f"{STEM}.drawio"
    drawio.write_text(xml, encoding="utf-8")
    print("Wrote", drawio)
    print("Wrote", base.export_png(xml))


if __name__ == "__main__":
    main()
