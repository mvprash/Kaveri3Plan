# -*- coding: utf-8 -*-
"""Generate the vertical draw.io swimlane diagram (and PNG) for the Sub-Registrar
scrutiny of a submitted document registration application.

Follows on from the citizen pre-registration entry process and uses the same layout.
"""
from __future__ import annotations

import _make_citizen_preregistration_diagram as base
from _make_citizen_preregistration_diagram import LEGEND, Diagram, label, lane_title

STEM = "Document_Scrutiny_Process_v3"


def scrutiny() -> Diagram:
    main_cx, left_cx, right_cx = 380, 120, 640
    lanes = [
        ("cit", lane_title("Citizen / Applicant", "Party or document writer"), 300),
        ("sys", lane_title("Kaveri System", "Kaveri Online Services"), 400),
        ("sro", lane_title("Sub-Registrar", "Registration Office"), 760),
        ("ms", lane_title("Kaveri Microservices", "Separate services"), 280),
        ("ext", lane_title("External Systems", "E-Swathu, BBMP E-Aasthi, E-Aasthi, BDA, KHB, Bhoomi, Mojini"), 280),
    ]
    d = Diagram(
        "Document Scrutiny",
        "Document Registration — Scrutiny by the Sub-Registrar (v3)",
        "How the Sub-Registrar checks a submitted registration application and approves it for payment, "
        "reverts it for correction or rejects it",
        lanes, rows=21,
    )
    d.lane_centre["sro"] = main_cx
    n = d.node
    n("s", "cit", 0, "start", "Start")
    n("prev", "cit", 1, "ext", label("", "Application submitted for verification and approval", "Previous stage: citizen pre-registration entry"))
    n("open", "sro", 2, "task", label("1", "Open the Pending Scrutiny list, search by application number and open the application"))
    n("show", "sys", 3, "task", label("2", "Show the submitted deed (PDF) and the document details: header, properties, parties, title flow, consideration, covenants and witnesses. Prepare the verification checklist with the captured data shown against each item", "Checklist = common checks + checks for the confirmed Article"), box_w=260, box_h=150)
    n("review", "sro", 4, "task", label("3", "Review the submitted deed and the document details; download the deed or view the history of earlier actions if needed"), box_w=240)
    n("common", "sro", 5.5, "task", label(
        "4", "Common checks:<div style='text-align:left'>"
        "• Transaction type<br>"
        "• Property details imported from the source of truth are intact<br>"
        "• Article selected for the document<br>"
        "• Exemption claimed (if any)<br>"
        "• Area used for property valuation<br>"
        "• Court / government / 22-B stays<br>"
        "• Property within the Sub-Registrar Office limits (Sec. 28, Registration Act)<br>"
        "• Executants, claimants and witnesses captured<br>"
        "• At least two witnesses with full details<br>"
        "• Denoting / credit claim and any uploaded earlier document (if any)</div>"),
      box_w=320, box_h=270)
    n("sot", "ext", 5.5, "task", label("5", "Show the current owners and property details from the source of truth for cross-checking"))
    n("article", "sro", 7, "task", label("6", "Checks for the confirmed Article, e.g. Sale 20(1): stamp duty on the higher of market value and consideration; absolute transfer of ownership; no conditions resembling a lease or mortgage"), box_w=320, box_h=130)
    n("gv_q", "sro", 8, "decision", label("7", "Property guidance value to be re-calculated?"))
    n("gv_in", "sro", 9, "task", label("8", "Correct the valuation details (e.g. area, property type, use) and re-calculate the guidance value"), cx=right_cx)
    n("gv_ms", "ms", 9, "task", label("9", "Guidance Value service: re-calculate the property guidance value", "Separate microservice"))
    n("fee_q", "sro", 10, "decision", label("10", "Stamp duty and other fees to be re-calculated?"))
    n("fee_ms", "ms", 11, "task", label("11", "Fee Calculation service: re-calculate the stamp duty, surcharge, cess, registration fee and other fees", "Separate microservice; old and new amounts kept in the history"), box_h=140)
    n("mark", "sro", 12, "task", label("12", "Mark each item Agree or Disagree, add remarks where needed and save the checklist"), box_w=240)
    n("marked", "sys", 13, "decision", label("13", "Every checklist item marked?"))
    n("saved", "sys", 14, "task", label("14", "Save the checklist and mark the scrutiny as Completed"))
    n("decide", "sro", 15, "decision", label("15", "Decision on the application?"))
    n("revert", "sro", 16, "task", label("16b", "Revert: give the corrections needed (visible to the applicant)"), cx=left_cx)
    n("approve", "sro", 16, "task", label("16a", "Approve for payment; add internal remarks if needed (not visible to the applicant)"))
    n("reject", "sro", 16, "reject", label("16c", "Reject: give the reason for rejection. Kaveri closes the application and notifies the applicant"), cx=right_cx, box_h=120)
    n("reject_end", "sro", 17, "end", "End", cx=right_cx)
    n("revert_sys", "sys", 17, "task", label("17b", "Return the application to the applicant with the remarks and notify them"))
    n("correct", "cit", 18, "task", label("18b", "Correct the application as per the remarks and resubmit it"))
    n("approve_sys", "sys", 18, "task", label("17a", "Mark the application Approved for Payment with the final (re-calculated, if any) amounts, approve any exemption or denoting claim, release the payment hold and notify the applicant"), box_w=260, box_h=150)
    n("next", "cit", 19, "ext", label("18a", "Pay the stamp duty and fees, eSign and book the appointment", "Next stage"))
    n("e", "cit", 20, "end", "End")

    e = d.edge
    down = "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
    loop_x = d.lane_x["cit"] + 16
    e("s", "prev", extra=down)
    e("prev", "open", "Submitted", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("open", "show", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("show", "review", extra="exitX=0.5;exitY=1;entryX=0;entryY=0.5;")
    e("review", "common", extra=down)
    e("common", "sot", "Cross-check (if needed)", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;startArrow=block;startFill=1;")
    e("common", "article", extra=down)
    e("article", "gv_q", extra=down)
    e("gv_q", "gv_in", "Yes", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("gv_in", "gv_ms", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    e("gv_ms", "fee_ms", "New guidance value", extra=down)
    e("gv_q", "fee_q", "No", extra=down)
    fee_x = d.lane_x["sro"] + right_cx
    e("fee_q", "fee_ms", "Yes", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;",
      points=[(fee_x, d.cy("fee_q")), (fee_x, d.cy("fee_ms"))])
    e("fee_q", "mark", "No", extra=down)
    e("fee_ms", "mark", "Re-calculated amounts", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("mark", "marked", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("marked", "mark", "No", back=True, extra="exitX=0.5;exitY=0;entryX=0;entryY=0.5;")
    e("marked", "saved", "Yes", extra=down)
    e("saved", "decide", extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("decide", "approve", "Approve", extra=down)
    e("decide", "revert", "Revert", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("decide", "reject", "Reject", back=True, extra="exitX=1;exitY=0.5;entryX=0.5;entryY=0;")
    e("reject", "reject_end", extra=down)
    e("revert", "revert_sys", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("revert_sys", "correct", "Reverted", extra="exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
    e("correct", "open", "Resubmitted", back=True, extra="exitX=0;exitY=0.5;entryX=0;entryY=0.5;",
      points=[(loop_x, d.cy("correct")), (loop_x, d.cy("open"))])
    e("approve", "approve_sys", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("approve_sys", "next", "Approved for payment", extra="exitX=0.5;exitY=1;entryX=1;entryY=0.5;")
    e("next", "e", extra=down)
    d.legend(LEGEND)
    return d


def main():
    base.STEM = STEM
    xml = scrutiny().xml()
    drawio = base.OUT_DIR / f"{STEM}.drawio"
    drawio.write_text(xml, encoding="utf-8")
    print("Wrote", drawio)
    print("Wrote", base.export_png(xml))


if __name__ == "__main__":
    main()
