# -*- coding: utf-8 -*-
"""Generate the vertical draw.io swimlane diagram (and PNG) for the citizen steps after
scrutiny approval: payment (full or partial), digital signing by parties and witnesses,
and appointment booking.

Uses the same layout as the citizen pre-registration and scrutiny diagrams.
"""
from __future__ import annotations

import _make_citizen_preregistration_diagram as base
from _make_citizen_preregistration_diagram import LEGEND, Diagram, label, lane_title

STEM = "Citizen_Payment_eSign_Appointment_Process_v3"
JUMP = "jumpStyle=arc;jumpSize=12;"


def payment_esign() -> Diagram:
    main_cx, right_cx = 180, 420
    sign_l, sign_m, sign_r = 130, 240, 350
    lanes = [
        ("cit", lane_title("Citizen / Applicant", "Party or document writer"), 560),
        ("party", lane_title("Party", "Executant / claimant / representative — portal or mobile"), 520),
        ("wit", lane_title("Witness", "Portal or mobile"), 520),
        ("sys", lane_title("Kaveri System", "Kaveri Online Services"), 420),
        ("ms", lane_title("Kaveri Microservices", "Deed Generation service"), 300),
        ("ext", lane_title("External Systems", "Khajane-II / payment gateway, e-Sign service provider (UIDAI), DSC certifying authority"), 300),
    ]
    d = Diagram(
        "Payment eSign Appointment",
        "Document Registration — Payment, Digital Signing and Appointment (v3)",
        "What the citizen does after the Sub-Registrar approves the application for payment: "
        "full or partial payment, final deed from the Deed Generation service, e-Sign / DSC by all parties and witnesses "
        "(the e-Sign date is the date of execution), and appointment booking within the time allowed for presentation",
        lanes, rows=37,
    )
    d.lane_centre.update(cit=main_cx, party=sign_m, wit=sign_m)
    n = d.node
    n("s", "cit", 0, "start", "Start")
    n("prev", "cit", 1, "ext", label("", "Application Approved for Payment by the Sub-Registrar", "Previous stage: scrutiny"))

    # A. Payment
    n("notify", "sys", 2, "task", label("1", "Notify the applicant (SMS, email, portal) and show the final payable amounts: stamp duty, surcharge, cess, registration fee and other fees. If the Sub-Registrar re-valued the property, show the declared value, the Sub-Registrar's estimated market value and the extra duty on the difference", "Estimated market value communicated to the parties: Sec. 45-A(1), Karnataka Stamp Act, 1957"), box_w=320, box_h=156)
    n("agree", "cit", 3, "decision", label("2", "Agree to pay the full amount?"))
    n("full", "cit", 4, "task", label("3a", "Full payment: pay online through the payment gateway or enter the challan details"))
    n("partial", "cit", 4.25, "task", label(
        "3b", "Partial payment: pay the registration fee and other fees in full; choose the reason and pay the stamp duty, surcharge and cess agreed<div style='text-align:left'>"
        "• Does not accept the Sub-Registrar's market value (under-valuation) — only for instruments listed in Sec. 45-A; registration kept pending and referred to the District Registrar, Sec. 45-A, Karnataka Stamp Act, 1957<br>"
        "• Pays less stamp duty than required (short levy) — impounded, Sec. 33; deficit plus a penalty of up to ten times the deficit, Sec. 39</div>",
        "Registration fee unpaid: refusal ground, Rule 171(xvi). Dispute on the Article: seek the Deputy Commissioner's opinion under Sec. 31 before signing"),
      cx=right_cx, box_w=270, box_h=270)
    n("gateway", "ext", 5.3, "task", label("4", "Khajane-II / payment gateway: confirm the payment or challan"))
    n("paid", "sys", 6.3, "decision", label("5", "Payment confirmed for the amount chosen?"))
    n("receipt", "sys", 7.3, "task", label("6", "Generate the payment receipt. Partial payment: record the amount paid, the deficit and the reason; mark for Sec. 45-A referral or Sec. 33 impounding"), box_w=300, box_h=130)

    n("deed_gen", "ms", 8.3, "task", label("6a", "Deed Generation service: generate the final deed from the same template and version as the approved draft, adding the stamp duty paid, e-stamp certificate / challan details and the e-Sign field for each signer; remove the DRAFT watermark", "Separate microservice; deed text must match the approved draft"), box_w=270, box_h=156)

    # B. Signing by the parties
    n("prep", "sys", 9.3, "task", label("7", "Store the final deed and prepare the signing list: executants, then claimants / representatives, then witnesses", "Applicant can track each signer: Pending, Link sent, Signed, Failed. Each party's e-Sign date is recorded as that party's date of execution (Sec. 23, 24, 34, Registration Act); the applicant is warned as 4 months from the first signature approaches"), box_w=320, box_h=150)
    n("p_where", "cit", 10.5, "decision", label("8", "Next party signs in the portal or on a mobile?"), box_h=130)
    n("p_link", "sys", 11.5, "task", label("9", "Send a secure, time-limited signing link to the party's registered mobile / email", "Applicant can resend an expired link"), box_w=240, box_h=120)
    n("p_review", "party", 12.5, "task", label("10", "Open the deed (portal or mobile link), review it and agree to sign"))
    n("p_how", "party", 13.5, "decision", label("11", "Sign with e-Sign or DSC?"))
    n("p_esign", "party", 14.5, "task", label("12a", "e-Sign: enter Aadhaar number / Virtual ID and the OTP from UIDAI"), cx=sign_l)
    n("p_dsc", "party", 14.5, "task", label("12b", "DSC: connect the DSC token and enter the PIN"), cx=sign_r)
    n("p_ext", "ext", 15.5, "task", label("13", "e-Sign service provider returns the signed PDF; certifying authority confirms the DSC is valid and not revoked"), box_h=120)
    n("p_ok", "sys", 16.5, "decision", label("14", "Signature valid and signer matches the party?"), box_w=220, box_h=130)
    n("p_all", "sys", 17.5, "decision", label("15", "All parties signed?"))

    # C. Signing by the witnesses
    n("w_avail", "cit", 18.7, "decision", label("16", "Next witness available to sign?"))
    n("w_replace", "cit", 19.6, "task", label("17", "Replace the witness: enter the new witness's details"), cx=right_cx)
    n("w_where", "cit", 20.6, "decision", label("18", "Witness signs in the portal or on a mobile?"), box_h=130)
    n("w_link", "sys", 21.6, "task", label("19", "Send a secure, time-limited signing link to the witness's registered mobile / email"), box_w=240)
    n("w_review", "wit", 22.6, "task", label("20", "Open the deed, check the parties' signatures and agree to attest"))
    n("w_how", "wit", 23.6, "decision", label("21", "Sign with e-Sign or DSC?"))
    n("w_esign", "wit", 24.6, "task", label("22a", "e-Sign: enter Aadhaar number / Virtual ID and the OTP from UIDAI"), cx=sign_l)
    n("w_dsc", "wit", 24.6, "task", label("22b", "DSC: connect the DSC token and enter the PIN"), cx=sign_r)
    n("w_ext", "ext", 25.6, "task", label("23", "e-Sign service provider returns the signed PDF; certifying authority confirms the DSC is valid and not revoked"), box_h=120)
    n("w_ok", "sys", 26.6, "decision", label("24", "Signature valid and signer matches the witness captured?"), box_w=230, box_h=136)
    n("w_all", "sys", 27.6, "decision", label("25", "At least two witnesses signed?"))
    n("lock", "sys", 28.6, "task", label("26", "Lock the fully signed deed so it cannot be changed; calculate the last date for presentation (4 months from the earliest e-Sign date); mark the application Signed – ready for appointment", "Sec. 23, Registration Act"), box_w=280, box_h=140)

    # D. Appointment
    n("slot", "cit", 29.6, "task", label("27", "Choose a date and time slot at the Sub-Registrar Office with jurisdiction; the last date for presentation is shown"), box_w=220, box_h=120)
    n("slot_ok", "sys", 30.6, "decision", label("28", "Slot available?"))
    n("late_chk", "sys", 31.6, "decision", label("29", "Slot after the last date for presentation?"), box_w=220, box_h=130)
    n("late_ok", "cit", 32.6, "decision", label("30", "Warned: a late slot needs a condonation application and a delay fine at the office (Sec. 25; Rule 46). Keep this slot?"), cx=right_cx, box_w=300, box_h=156)
    n("confirm", "sys", 33.6, "task", label("31", "Book the slot and send the appointment confirmation (application number, office, date, time, who and what to bring) by SMS, email and portal"), box_w=280, box_h=130)
    n("next", "cit", 34.6, "ext", label("", "Present the document at the Sub-Registrar Office", "Next stage: presentation and registration (partial payment: Sec. 45-A referral / Sec. 33 impounding; late slot: condonation of delay)"), box_w=240, box_h=130)
    n("e", "cit", 35.6, "end", "End")

    e = d.edge
    down = "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
    left_loop = d.lane_x["cit"] + 30
    cx_cit = d.lane_x["cit"] + main_cx

    e("s", "prev", extra=down)
    e("prev", "notify", "Approved", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("notify", "agree", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("agree", "full", "Yes", extra=down)
    e("agree", "partial", "No", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("full", "gateway", "Full amount", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;", label_pos=-0.85)
    e("partial", "gateway", "Amount agreed", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;", label_pos=-0.6)
    e("gateway", "paid", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("paid", "full", "No / short — pay the difference", back=True, extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;" + JUMP,
      points=[(left_loop, d.cy("paid")), (left_loop, d.cy("full"))], label_pos=-0.4)
    e("paid", "receipt", "Yes", extra=down)
    e("receipt", "deed_gen", "Payment details", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("deed_gen", "prep", "Final deed PDF", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;",
      points=[(d.cxn("deed_gen"), d.cy("prep"))], label_pos=-0.3)

    e("prep", "p_where", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("p_where", "p_review", "Portal", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("p_where", "p_link", "Mobile", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("p_link", "p_review", "Link opened", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("p_review", "p_how", extra=down)
    e("p_how", "p_esign", "e-Sign", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("p_how", "p_dsc", "DSC", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    e("p_esign", "p_ext", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("p_dsc", "p_ext", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("p_ext", "p_ok", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    p_loop = d.lane_x["party"] + d.lane_w["party"] - 20
    e("p_ok", "p_how", "No — sign again", back=True, extra="exitX=0;exitY=0.5;entryX=1;entryY=0.5;" + JUMP,
      points=[(p_loop, d.cy("p_ok")), (p_loop, d.cy("p_how"))], label_pos=-0.5)
    e("p_ok", "p_all", "Yes", extra=down)
    e("p_all", "p_where", "No — next party", back=True, extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;" + JUMP,
      points=[(left_loop, d.cy("p_all")), (left_loop, d.cy("p_where"))], label_pos=-0.3)
    yes_y = d.nodes["w_avail"][1] - 24
    e("p_all", "w_avail", "Yes — witnesses sign next", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;",
      points=[(d.cxn("p_all"), yes_y), (cx_cit, yes_y)], label_pos=-0.4)

    e("w_avail", "w_where", "Yes", extra=down)
    e("w_avail", "w_replace", "No", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    rep_y = d.nodes["w_where"][1] - 20
    e("w_replace", "w_where", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;",
      points=[(d.cxn("w_replace"), rep_y), (cx_cit, rep_y)])
    e("w_where", "w_review", "Portal", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("w_where", "w_link", "Mobile", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("w_link", "w_review", "Link opened", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("w_review", "w_how", extra=down)
    e("w_how", "w_esign", "e-Sign", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("w_how", "w_dsc", "DSC", extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    e("w_esign", "w_ext", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("w_dsc", "w_ext", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("w_ext", "w_ok", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    w_loop = d.lane_x["wit"] + d.lane_w["wit"] - 20
    e("w_ok", "w_how", "No — sign again", back=True, extra="exitX=0;exitY=0.5;entryX=1;entryY=0.5;" + JUMP,
      points=[(w_loop, d.cy("w_ok")), (w_loop, d.cy("w_how"))], label_pos=-0.5)
    e("w_ok", "w_all", "Yes", extra=down)
    e("w_all", "w_avail", "No — next witness", back=True, extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;" + JUMP,
      points=[(left_loop, d.cy("w_all")), (left_loop, d.cy("w_avail"))], label_pos=-0.3)
    e("w_all", "lock", "Yes", extra=down)

    e("lock", "slot", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("slot", "slot_ok", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("slot_ok", "slot", "No — choose another slot", back=True, extra="exitX=0.5;exitY=0;entryX=1;entryY=0.5;")
    e("slot_ok", "late_chk", "Yes", extra=down)
    e("late_chk", "confirm", "No", extra=down)
    e("late_chk", "late_ok", "Yes", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;", label_pos=-0.8)
    e("late_ok", "confirm", "Yes — keep the slot", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;", label_pos=-0.5)
    e("late_ok", "slot", "No — choose an earlier slot", back=True, extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;" + JUMP,
      points=[(left_loop, d.cy("late_ok")), (left_loop, d.cy("slot"))], label_pos=-0.3)
    e("confirm", "next", "Appointment booked", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;",
      points=[(d.cxn("confirm"), d.cy("next"))], label_pos=-0.4)
    e("next", "e", extra=down)
    d.legend(LEGEND)
    return d


def main():
    base.STEM = STEM
    xml = payment_esign().xml()
    drawio = base.OUT_DIR / f"{STEM}.drawio"
    drawio.write_text(xml, encoding="utf-8")
    print("Wrote", drawio)
    print("Wrote", base.export_png(xml))


if __name__ == "__main__":
    main()
