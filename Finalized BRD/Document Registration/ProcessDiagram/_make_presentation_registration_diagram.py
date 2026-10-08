# -*- coding: utf-8 -*-
"""Generate the vertical draw.io swimlane diagram (and PNG) for presentation, photo and
thumb capture, and registration of a document at the Sub-Registrar Office.

Uses the same layout as the other Document Registration process diagrams.
"""
from __future__ import annotations

import _make_citizen_preregistration_diagram as base
from _make_citizen_preregistration_diagram import (LANE_HEADER_H, LEGEND, ROW_H, TITLE_H, Diagram, label,
                                                    lane_title)

STEM = "Presentation_PhotoThumb_Registration_Process_v11"
JUMP = "jumpStyle=arc;jumpSize=12;"
TO_REFUSAL = "Refuse registration: go to D (step 40)"
TO_WITHDRAW = "go to E (step 50)"
DR_FLOW = "Separate flow: District Registrar Referral Process; resumes here with the order"


def presentation_registration() -> Diagram:
    main_cx, right_cx = 220, 480
    side_cx, link_cx = 125, 345
    lanes = [
        ("party", lane_title("Parties and Witnesses", "At the Sub-Registrar Office"), 420),
        ("sro", lane_title("Sub-Registrar", "Registration Office"), 620),
        ("deo", lane_title("Data Entry Operator", "Registration Office"), 420),
        ("sys", lane_title("Kaveri System", "Kaveri Online Services"), 440),
        ("ms", lane_title("Kaveri Microservices", "Deed Generation service"), 340),
        ("ext", lane_title("External Systems", "UIDAI e-KYC, e-Sign service provider, DSC certifying authority"), 300),
    ]
    d = Diagram(
        "Presentation Photo Thumb Registration",
        "Document Registration — Presentation, Photo &amp; Thumb Capture, Registration, Refusal and Withdrawal (v11)",
        "What happens at the Sub-Registrar Office after the appointment: the Sub-Registrar presents the document, records admission "
        "(keeping it pending until every executant appears, by summons or commission if needed) and checks for delay in presentation or appearance, "
        "the Data Entry Operator captures photos, thumb impressions and e-Signs, and the Sub-Registrar registers the document, keeps it pending "
        "for a Sec. 45-A referral or Sec. 33 impounding (decided in the District Registrar Referral Process), or refuses registration; "
        "the Deed Generation service produces the endorsement and the registered document from the deed template "
        "(Part XII, Registration Act; Chapter XXIV, Karnataka Registration Rules); the presenter may withdraw the document at any time before registration",
        lanes, rows=67,
    )
    d.lane_centre["sro"] = main_cx

    for row, text in [(2, "A. PRESENTATION"), (23.6, "B. PHOTO, THUMB AND E-SIGN"), (33.6, "C. REGISTRATION"),
                      (46.05, "D. REFUSAL TO REGISTER"), (58.05, "E. WITHDRAWAL BEFORE REGISTRATION")]:
        d._vertex(f"sec_{row}", f"<b>{text}</b>",
                  "text;html=1;align=left;verticalAlign=top;fontSize=13;fontColor=#1f4e79;",
                  d.lane_x["party"] + 12, TITLE_H + LANE_HEADER_H + row * ROW_H + 6, 380, 26)

    n = d.node
    n("s", "party", 0, "start", "Start")
    n("prev", "party", 1, "ext", label("", "Parties and witnesses arrive at the Sub-Registrar Office at the booked appointment", "Previous stage: payment, digital signing and appointment"), box_w=240, box_h=110)

    # A. Presentation
    n("open", "sro", 2, "task", label("1", "Open the application from the Presentation list"))
    n("show", "sys", 3, "task", label("2", "Show the digitally executed deed (with signature status) and the payment for each property: stamp duty, surcharge, cess, registration fee and total"), box_w=280, box_h=130)
    n("check", "sro", 4, "task", label("3", "Verification checklist: presenter's identity and right to present; deed matches the submission; payment and stamp duty (a stamp duty shortfall alone does not stop presentation: mark it for impounding at step 34, Sec. 33; Rule 46(ii), (iii)); language, interlineations, property description, map and date of execution (a date altered to avoid the delay fine is not accepted, Rule 50(iii)); Sec. 22-B (forged, prohibited or attached property). Mark Agree / Disagree with remarks"), box_w=360, box_h=156)
    n("agreed", "sys", 5, "decision", label("4", "All checklist items agreed?", "Stamp duty shortfall marked for impounding counts as agreed"), cx=side_cx, box_w=210, box_h=140)
    n("ground", "sys", 6, "decision", label("5", "Disagree item is a refusal ground? (Rule 171, Sec. 22-B)"), cx=side_cx, box_w=210, box_h=140)
    n("to_d1", "sys", 6, "reject", TO_REFUSAL, cx=link_cx, box_w=170, box_h=80)
    n("withdraw", "sys", 7, "reject", label("6", f"Not presented: the parties cure the defect and return, or the presenter withdraws in writing: {TO_WITHDRAW}", "No appeal (Rule 190)"), cx=side_cx, box_w=220, box_h=150)
    n("withdraw_end", "sys", 7, "end", "End", cx=link_cx + 20)
    n("present", "sro", 8, "task", label("7", "Select the presenter from the parties and present the document"))
    n("rec_pres", "sys", 9, "task", label("8", "Record the presentation: presenter, date, time and office", "Presenter cannot be changed once admission is recorded (Sec. 32, Registration Act)"), box_w=260, box_h=120)
    n("admit", "sro", 10, "task", label("9", "Record admission or denial of execution as each party appears, with the date of appearance", "Refusal grounds: execution denied; minor or unsound mind; death of executant not proved (Sec. 34, 35; Rule 171). Executants may appear at different times (Sec. 34(2))"), box_w=300, box_h=150)
    n("denied", "sys", 11, "decision", label("10", "Refusal ground at admission?"), cx=side_cx, box_w=200, box_h=124)
    n("to_d2", "sys", 11, "reject", TO_REFUSAL, cx=320, box_w=150, box_h=80)
    n("admitted", "sys", 12, "decision", label("11", "Another party present at the counter?"), cx=side_cx)
    n("all_app", "sys", 13, "decision", label("12", "All executants appeared and admitted?"), cx=side_cx, box_w=210, box_h=130)
    n("app_pend", "sro", 14, "task", label("13", "Keep the document pending as Party Appearance Pending: record who has admitted and who is absent, with the date; record in the Minute Book. Admissions already recorded stay", "Sec. 34(2); Rule 172"), cx=right_cx, box_w=270, box_h=140)
    n("app_sys", "sys", 15, "task", label("14", "Calculate the last date for appearance (4 months from execution; up to 4 more with condonation), notify the applicant and the absent executants and list the document as Pending Appearance", "Sec. 34(1), (2)"), cx=side_cx, box_w=240, box_h=140)
    n("bring_q", "sys", 16, "decision", label("14a", "How will the absent executant appear?"), cx=side_cx, box_w=210, box_h=130)
    n("summons", "sro", 17, "task", label("14b", "Presenter applies for a summons: issue the summons to the absent executant on payment of the peon's fee (Add Challan), have it served, and keep the document pending as Summons Issued until the date fixed; record in the Minute Book", "Sec. 36, 37, 39; Rule 23(e)"), cx=475, box_w=270, box_h=140)
    n("comm", "sro", 17, "task", label("14c", "Executant exempt from appearing (illness or bodily infirmity, in jail, or exempt by law): visit the residence or jail, or issue a commission; keep the document pending as Commission Report Pending until the examination or the commissioner's report is recorded", "Sec. 31, 33, 38"), cx=185, box_w=270, box_h=140)
    n("app_dec", "sys", 18, "decision", label("15", "Absent executant appeared by the last date?"), cx=side_cx, box_w=200, box_h=130)
    n("to_d8", "sys", 18, "reject", label("", "No — time expired, executant keeping away, or presenter asks for return as to the absent executant: go to D (step 40)", "Rule 171(viii) and note to (xi); Rule 172"), cx=318, box_w=150, box_h=140)
    n("late", "sys", 19, "decision", label("16", "Presented, or an executant appeared, more than 4 months after execution?", "From each execution date (Sec. 23, 24); decree date / arrival in India (Sec. 23, 26); wills exempt (Sec. 27); appearance: Sec. 34(1)"), cx=side_cx, box_w=240, box_h=156)
    n("late_max", "sys", 20, "decision", label("17", "Delay more than 4 months beyond the time allowed?", "Rule 171(vi) / (viii)"), cx=side_cx, box_w=220, box_h=140)
    n("to_d6", "sys", 20, "reject", TO_REFUSAL, cx=link_cx, box_w=150, box_h=80)
    n("late_pend", "sro", 21, "task", label("18", "Take the written condonation application (urgent necessity or unavoidable accident), suspend registration and refer it to the District Registrar whether or not the reason is satisfactory; record in the Minute Book", "Sec. 25, 34(1); Rules 46, 51, 55(i)"), cx=right_cx, box_w=270, box_h=140)
    n("dr1", "sro", 22, "ext", label("", "District Registrar Referral Process — condonation of delay", DR_FLOW), cx=right_cx, box_w=250, box_h=110)
    n("condoned", "sro", 23, "decision", label("19", "Order received: delay condoned and fine paid?", "Rejected / unpaid: Rule 171(vi), (viii), (xvi)"), cx=right_cx, box_w=220, box_h=150)
    n("to_d7", "sro", 23, "reject", TO_REFUSAL, cx=main_cx - 40, box_w=150, box_h=80)

    # B. Photo, thumb and e-Sign
    n("ident", "deo", 24, "task", label("20", "Select at least two identifiers from the witnesses, or add a new identifier"))
    n("ident_ok", "sys", 25, "decision", label("21", "At least two identifiers?"))
    n("cap_party", "deo", 26, "task", label("22", "For each party: assign the identifiers, capture the photo (camera) and thumb impression (biometric device); run Aadhaar e-KYC and name match"), box_w=300, box_h=130)
    n("ekyc", "ext", 26, "task", label("23", "UIDAI e-KYC: return name, date of birth, address and photo for the name match"))
    n("cap_wit", "deo", 27, "task", label("24", "For each witness / identifier: capture the photo; run Aadhaar e-KYC and name match"), box_w=260)
    n("esign", "party", 28, "task", label("25", "Each party and witness e-Signs at the counter, or on their own mobile through a link (Get Link)"), box_w=240, box_h=120)
    n("esp", "ext", 28, "task", label("26", "e-Sign service provider: Aadhaar OTP and the e-Signature"))
    n("all_done", "sys", 30, "decision", label("27", "Photo, thumb, e-KYC and e-Sign done for every party and witness?"), cx=side_cx, box_w=240, box_h=140)
    n("id_ok", "sys", 31, "decision", label("28", "Executants identified and agents' authority accepted? (Sec. 34(3))"), cx=side_cx, box_w=240, box_h=150)
    n("to_d3", "sys", 31, "reject", TO_REFUSAL, cx=link_cx, box_w=170, box_h=80)
    n("gen", "deo", 32, "task", label("29", "Generate the endorsement"))
    n("gen_sys", "ms", 33, "task", label("30", "Deed Generation service: generate the endorsement from the endorsement part of the deed template: presentation, fee details, presenter, admission by each executant with e-KYC details, photo, thumb and e-Sign, the identifiers and, if the delay was condoned, the Registrar's order number and date, fine and period of delay", "Rule 55(ii)"), box_w=300, box_h=156)

    # C. Registration
    n("review", "sro", 34, "task", label("31", "Review the endorsement together with the digitally executed deed"))
    n("review_ok", "sys", 35, "decision", label("32", "Refusal ground found on review? (Sec. 22-B, Rule 171)"), cx=side_cx, box_w=240, box_h=146)
    n("to_d4", "sys", 35, "reject", TO_REFUSAL, cx=link_cx, box_w=170, box_h=80)
    n("partial", "sys", 36, "decision", label("33", "Stamp duty short?", "Partial payment by the applicant, or shortfall marked at step 3 or found on review"), cx=side_cx, box_w=240, box_h=150)
    n("kind", "sro", 37, "decision", label("34", "Market value understated in an instrument listed in Sec. 45-A, or stamp duty short (Sec. 33)?"), cx=right_cx, box_w=250, box_h=150)
    n("p45", "sro", 38, "task", label("34a", "Sec. 45-A: communicate the estimated market value to the parties; unless they pay duty on it, keep the process of registration pending and refer the matter with a copy of the instrument to the District Registrar; record in the Minute Book", "Sec. 45-A(1), Karnataka Stamp Act"), cx=190, box_w=250, box_h=150)
    n("p33", "sro", 38, "task", label("34b", "Sec. 33: impound; write \"Impounded under Section 33\" below the presentation endorsement, sign and date it; send the original to the District Registrar with the reasons, suspending registration; enter in the Register of Impounded Documents and the Minute Book", "Sec. 33, 37(2); Rules 23(a), 24(iii)(a), 46(ii)"), cx=right_cx, box_w=260, box_h=150)
    n("dr2", "sro", 39, "ext", label("", "District Registrar Referral Process — Sec. 45-A referral / Sec. 33 impounded document", DR_FLOW), cx=right_cx, box_w=260, box_h=110)
    n("paid", "sro", 40, "decision", label("35", "Order received and the amount due paid?", "Rule 116. Unpaid: Rule 171 (xvi)"), cx=right_cx, box_w=230, box_h=150)
    n("to_d5", "sys", 40, "reject", TO_REFUSAL, cx=side_cx, box_w=170, box_h=80)
    n("dsc", "sro", 41, "task", label("36", "Sign the endorsement with the DSC: select the certificate and enter the password"), box_w=240)
    n("ca", "ext", 41, "task", label("37", "Certifying authority: certificate valid and not revoked"))
    n("register", "sro", 42, "task", label("38", "Register the document"))
    n("reg_sys", "sys", 43, "task", label("39", "Generate the registration number (office–book–serial–financial year, e.g. GAN-1-00006-2026-27) and send it with the DSC-signed endorsement to the Deed Generation service"), box_w=320, box_h=150)
    n("reg_doc", "ms", 43, "task", label("39a", "Deed Generation service: add the registration number, book number and the signed endorsement to the locked deed and return the registered document (PDF); the executed deed text is not changed"), box_w=300, box_h=150)
    n("reg_done", "sys", 44, "task", label("39b", "Store the registered document with its hash, mark Registration Completed and notify the applicant"), box_w=280, box_h=110)
    n("final", "party", 44, "ext", label("", "Registered document available to the applicant for download", "Next stage: post-registration"), box_w=240)
    n("e", "party", 45, "end", "End")

    # D. Refusal to register
    n("d_in", "sro", 46, "reject", label("", "Refusal ground found at step 5, 10, 15, 17, 19, 28, 32 or 35"), box_w=240, box_h=80)
    n("juris", "sro", 47, "decision", label("40", "Property outside this office's jurisdiction?"), box_w=210, box_h=130)
    n("ret", "sro", 47, "ext", label("", "Return the document for presentation at the office having jurisdiction", "Not a refusal; no Book 2 entry (Sec. 28, Sec. 71(1))"), cx=right_cx, box_w=230, box_h=120)
    n("ret_end", "sro", 48, "end", "End", cx=right_cx)
    n("order", "sro", 48, "task", label("41", "Pass the refusal order: select the ground(s) under Rule 171 / Sec. 22-B and record the reasons", "Sec. 71(1), Registration Act"), box_w=250, box_h=130)
    n("part_x", "sys", 49, "decision", label("42", "Some executants admitted and others denied or did not appear?"), cx=side_cx, box_w=220, box_h=140)
    n("part_reg", "sys", 49, "task", label("43", "Register as to the executants who admitted; endorse the refusal for the others below the certificate", "Rules 106, 172 &amp; 173"), cx=link_cx, box_w=170, box_h=150)
    n("book2", "sys", 50, "task", label("44", "Record the reasons in Book 2 (Record of reasons for refusal to register) and endorse \"Registration refused\" on the document", "Sec. 71(1); Rule 171; Book 2 kept permanently (Rule 205)"), box_w=320, box_h=140)
    n("dsc2", "sro", 51, "task", label("45", "Sign the refusal order and the endorsement with the DSC"), box_w=240)
    n("notify", "sys", 52, "task", label("46", "Block re-presentation of the document in every office unless registration is directed (Sec. 71(2)); refund half the registration fee and all copying fees, but not any delay fine (Rule 193 and note); notify the presenter and return the refused document (Rule 112)"), box_w=340, box_h=150)
    n("recv", "party", 53, "task", label("47", "Presenter receives the refused document; an executant or claimant may apply for a copy of the reasons"), box_w=260, box_h=120)
    n("copy", "sys", 54, "task", label("48", "Issue a free copy of the recorded reasons without delay", "Sec. 71(1)"), box_w=260)
    n("denial", "sys", 55, "decision", label("49", "Refused for denial of execution? (Sec. 35; Rule 187)"), box_w=250, box_h=150)
    n("app73", "party", 56, "ext", label("", "District Registrar Referral Process — Sec. 73 application (within 30 days)", "Separate flow: District Registrar Referral Process, section D"), cx=110, box_w=200, box_h=150)
    n("app72", "party", 56, "ext", label("", "District Registrar Referral Process — Sec. 72 appeal (within 30 days)", "Separate flow: District Registrar Referral Process, section D"), cx=315, box_w=190, box_h=150)
    n("d_end", "party", 57, "end", "End")

    # E. Withdrawal before registration
    n("w_in", "sro", 58, "reject", label("", "Presenter asks to withdraw at step 6, or while the document is pending at step 13, 14b, 14c, 18, 34a, 34b or 35 — any time before registration (step 38)"), box_w=320, box_h=100)
    n("w_req", "party", 59, "task", label("50", "Presenter submits the written withdrawal request, signed, with the reason"), box_w=240, box_h=110)
    n("w_check", "sro", 60, "task", label("51", "Verify the presenter's identity and the request; record the withdrawal, date and reason in the Minute Book and approve it with the DSC", "Rules 23(f), 193(i). Not a refusal: no Book 2 entry, no Sec. 71(2) block; no appeal (Rule 190)"), box_w=300, box_h=140)
    n("w_dr", "sys", 61, "decision", label("52", "Document referred to the District Registrar (step 18, 34a or 34b)?"), cx=side_cx, box_w=210, box_h=140)
    n("w_drn", "sys", 61, "ext", label("", "District Registrar Referral Process — intimation of withdrawal; an impounded document is released only on the District Registrar's order", "Stamp duty proceedings under Sec. 33 are not closed by the withdrawal"), cx=link_cx + 10, box_w=180, box_h=150)
    n("w_sys", "sys", 62, "task", label("53", "Mark the application Withdrawn; cancel the pending appearance dates, summons, commission and appointment; remove it from the pending lists", "The document may be presented again later"), box_w=320, box_h=130)
    n("w_notify", "sys", 63, "task", label("54", "Endorse \"Withdrawn\" on the document with the document number and date, notify the presenter and the parties, and return the document", "The endorsement is the evidence for the stamp duty refund"), box_w=300, box_h=130)
    n("w_recv", "party", 64, "task", label("55", "Presenter receives the returned document"), box_w=240)
    n("w_ref", "party", 65, "ext", label("", "Refund Process — half the registration fee and all copying fees (Rules 193–195), and the stamp duty (Sec. 47, Karnataka Stamp Act)", "Separate flow: Refund Process"), box_w=280, box_h=130)
    n("w_end", "party", 66, "end", "End")

    e = d.edge
    down = "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
    right = "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
    to_sys = "exitX=1;exitY=0.5;entryX=0.5;entryY=0;"
    to_sro = "exitX=0;exitY=0.5;entryX=0.5;entryY=0;"
    loop_x = d.lane_x["sys"] + d.lane_w["sys"] - 15

    def entry_x(node: str, x_abs: int) -> str:
        x, _, w, _ = d.nodes[node]
        return f"{(x_abs - x) / w:.2f}"

    e("s", "prev", extra=down)
    e("prev", "open", "Appointment", extra=to_sys)
    e("open", "show", extra=to_sys)
    e("show", "check", extra=to_sro)
    e("check", "agreed", extra=to_sys)
    e("agreed", "present", "Yes", extra=to_sro)
    e("agreed", "ground", "No", back=True, extra=down)
    e("ground", "to_d1", "Yes", back=True, extra=right)
    e("ground", "withdraw", "No", back=True, extra=down)
    e("withdraw", "withdraw_end", "Cure and return", extra=right)
    e("present", "rec_pres", extra=to_sys)
    e("rec_pres", "admit", extra=to_sro)
    e("admit", "denied", extra="exitX=1;exitY=0.3;entryX=0.5;entryY=0;")
    e("denied", "to_d2", "Yes", back=True, extra=right)
    e("denied", "admitted", "No", extra=down)
    e("admitted", "admit", "Yes — next party", back=True, extra="exitX=1;exitY=0.5;entryX=1;entryY=0.75;",
      points=[(loop_x, d.cy("admitted")), (loop_x, d.nodes["admit"][1] + d.nodes["admit"][3] * 3 // 4)], label_pos=-0.85)
    e("admitted", "all_app", "No", extra=down)
    yes_x = d.lane_x["sys"] + d.lane_w["sys"] - 40
    e("all_app", "late", "Yes", extra="exitX=1;exitY=0.5;entryX=1;entryY=0.5;",
      points=[(yes_x, d.cy("all_app")), (yes_x, d.cy("late"))], label_pos=-0.8)
    e("all_app", "app_pend", "No — executant absent", extra=to_sro, label_pos=-0.6)
    e("app_pend", "app_sys", extra=f"exitX=0.5;exitY=1;entryX=0;entryY=0.5;" + JUMP)
    e("app_sys", "bring_q", extra=down)
    merge_y = d.nodes["app_dec"][1] - 8
    app_top = (d.cxn("app_dec"), merge_y)
    e("bring_q", "app_dec", "New appointment", extra=down, label_pos=-0.5)
    e("bring_q", "comm", "Home visit / commission (Sec. 38)", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;",
      points=[(d.cxn("comm"), d.cy("bring_q"))], label_pos=-0.6)
    e("bring_q", "summons", "Summons (Sec. 36)", extra="exitX=0.25;exitY=0.75;entryX=0.5;entryY=0;" + JUMP,
      points=[(d.nodes["bring_q"][0] + d.nodes["bring_q"][2] // 4, d.nodes["summons"][1] - 20),
              (d.cxn("summons"), d.nodes["summons"][1] - 20)], label_pos=-0.4)
    e("summons", "app_dec", extra=down + JUMP, points=[(d.cxn("summons"), merge_y), app_top])
    e("comm", "app_dec", extra=down + JUMP, points=[(d.cxn("comm"), merge_y), app_top])
    back_x = d.lane_x["sro"] + 30
    e("app_dec", "admit", "Yes — record admission", back=True, extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;" + JUMP,
      points=[(back_x, d.cy("app_dec")), (back_x, d.cy("admit"))], label_pos=-0.7)
    e("app_dec", "to_d8", "No", back=True, extra=right)
    e("late", "ident", "No — within time", extra=to_sro, label_pos=-0.7)
    e("late", "late_max", "Yes", extra=down)
    e("late_max", "to_d6", "Yes", back=True, extra=right)
    e("late_max", "late_pend", "No — up to 4 months", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;" + JUMP, label_pos=-0.7)
    e("late_pend", "dr1", "Referred", extra=down)
    e("dr1", "condoned", "Order", extra=down)
    e("condoned", "to_d7", "No", back=True, extra="exitX=0;exitY=0.5;entryX=1;entryY=0.5;")
    e("condoned", "ident", "Yes — condoned", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;", label_pos=-0.5)
    e("ident", "ident_ok", extra="exitX=1;exitY=0.3;entryX=0.5;entryY=0;")
    e("ident_ok", "ident", "No — add identifiers", back=True, extra="exitX=1;exitY=0.5;entryX=1;entryY=0.75;",
      points=[(loop_x, d.cy("ident_ok")), (loop_x, d.nodes["ident"][1] + d.nodes["ident"][3] * 3 // 4)], label_pos=-0.6)
    e("ident_ok", "cap_party", "Yes", extra=to_sro)
    e("cap_party", "ekyc", "e-KYC (if Aadhaar)", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;startArrow=block;startFill=1;")
    e("cap_party", "cap_wit", extra=down)
    e("cap_wit", "ekyc", "e-KYC", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=1;startArrow=block;startFill=1;" + JUMP)
    e("cap_wit", "esign", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("esign", "esp", "OTP / signature", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;startArrow=block;startFill=1;" + JUMP)
    e("esign", "all_done", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("all_done", "cap_party", "No — complete the pending items", back=True, extra="exitX=1;exitY=0.5;entryX=1;entryY=0.85;" + JUMP,
      points=[(loop_x, d.cy("all_done")), (loop_x, d.nodes["cap_party"][1] + d.nodes["cap_party"][3] * 85 // 100)], label_pos=-0.7)
    e("all_done", "id_ok", "Yes", extra=down)
    e("id_ok", "to_d3", "No", back=True, extra=right)
    e("id_ok", "gen", "Yes", extra=to_sro)
    e("gen", "gen_sys", "Endorsement data", extra=to_sys + JUMP, label_pos=-0.5)
    e("gen_sys", "review", "Endorsement", extra=to_sro + JUMP, label_pos=-0.3)
    e("review", "review_ok", extra=to_sys)
    e("review_ok", "to_d4", "Yes", back=True, extra=right)
    e("review_ok", "partial", "No", extra=down)
    e("partial", "kind", "Yes", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    full_x = d.lane_x["sro"] + 30
    e("partial", "dsc", "No — full payment", extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;" + JUMP,
      points=[(full_x, d.cy("partial")), (full_x, d.cy("dsc"))], label_pos=-0.8)
    e("kind", "p45", "Sec. 45-A", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;", label_pos=-0.5)
    e("kind", "p33", "Sec. 33", extra=down)
    e("p45", "dr2", "Referred", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;", points=[(d.cxn("p45"), d.cy("dr2"))], label_pos=-0.5)
    e("p33", "dr2", "Sent", extra=down)
    e("dr2", "paid", "Order", extra=down)
    e("paid", "to_d5", "No", back=True, extra=right)
    e("paid", "dsc", "Yes — registration resumes", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.7;", label_pos=-0.3)
    e("dsc", "ca", "Validate certificate", extra="exitX=1;exitY=0.3;entryX=0;entryY=0.3;startArrow=block;startFill=1;")
    e("dsc", "register", "DSC signed", extra=down)
    e("register", "reg_sys", extra=to_sys)
    e("reg_sys", "reg_doc", extra=right)
    e("reg_doc", "reg_done", "Registered document", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;",
      points=[(d.cxn("reg_doc"), d.cy("reg_done"))], label_pos=-0.3)
    e("reg_done", "final", "Registered", extra="exitX=0;exitY=0.5;entryX=1;entryY=0.5;")
    e("final", "e", extra=down)

    e("d_in", "juris", extra=down)
    e("juris", "ret", "Yes", extra=right)
    e("ret", "ret_end", extra=down)
    e("juris", "order", "No", extra=down)
    e("order", "part_x", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("part_x", "part_reg", "Yes", extra=right)
    e("part_x", "book2", "No", extra=f"exitX=0.5;exitY=1;entryX={entry_x('book2', d.cxn('part_x'))};entryY=0;")
    e("part_reg", "book2", extra=f"exitX=0.5;exitY=1;entryX={entry_x('book2', d.cxn('part_reg'))};entryY=0;")
    e("book2", "dsc2", extra=to_sro)
    e("dsc2", "notify", extra=to_sys)
    e("notify", "recv", extra=to_sro)
    e("recv", "copy", extra=to_sys)
    e("copy", "denial", extra=down)
    e("denial", "app73", "Yes — Sec. 73 application", extra=to_sro, label_pos=-0.6)
    e("denial", "app72", "No — Sec. 72 appeal", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;", label_pos=-0.4)
    e("app73", "d_end", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("app72", "d_end", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")

    e("w_in", "w_req", extra=to_sro)
    e("w_req", "w_check", extra=to_sys)
    e("w_check", "w_dr", extra=to_sys)
    e("w_dr", "w_drn", "Yes", extra=right)
    e("w_dr", "w_sys", "No", extra=f"exitX=0.5;exitY=1;entryX={entry_x('w_sys', d.cxn('w_dr'))};entryY=0;")
    e("w_drn", "w_sys", "Intimated", extra=f"exitX=0.5;exitY=1;entryX={entry_x('w_sys', d.cxn('w_drn'))};entryY=0;")
    e("w_sys", "w_notify", extra=down)
    e("w_notify", "w_recv", extra=to_sro)
    e("w_recv", "w_ref", "Claim refund", extra=down)
    e("w_ref", "w_end", extra=down)
    d.legend(LEGEND)
    return d


def main():
    base.STEM = STEM
    xml = presentation_registration().xml()
    drawio = base.OUT_DIR / f"{STEM}.drawio"
    drawio.write_text(xml, encoding="utf-8")
    print("Wrote", drawio)
    print("Wrote", base.export_png(xml))


if __name__ == "__main__":
    main()
