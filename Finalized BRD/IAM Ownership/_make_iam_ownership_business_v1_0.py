# -*- coding: utf-8 -*-
"""Create Kaveri3_IAM_Ownership_Business_v1.0.docx — plain-language (client) edition: who does what, Kaveri application vs IAM, by business activity."""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import _make_iam_ownership_v1_0 as base  # noqa: E402

OUT_DIR = Path(r"Finalized BRD/IAM Ownership")
DST = OUT_DIR / "Kaveri3_IAM_Ownership_Business_v1.0.docx"
DIAGRAM = OUT_DIR / "IAM_Ownership_Business_Overview_v1.0.png"

DOC_VERSION = "1.0"
DOC_DATE = "05-10-2026"

KAV = "Kaveri application"
IAM = "IAM"
BOTH = "Both"
base.OWNER_FILL.update({IAM: "DDEBF7", BOTH: "FFF2CC"})

INTRO = [
    "Kaveri 3.0 is made up of two parts that work together:",
]
PARTS = [
    "Kaveri application — where the Department's work is done: offices, posts, roles, transfers, leave, and reports.",
    "IAM (Identity and Access Management) — the sign-in system: it keeps every user's login details, checks OTP, face or biometrics, and lets the user in.",
]
PURPOSE_END = (
    "This document explains, in simple terms, which part does what for each activity in the User "
    "Management BRD. It does not change any requirement in the BRD."
)

RULES = [
    "IAM answers: \"Who is this person, and may they sign in?\"",
    "Kaveri application answers: \"Which post, office and role does this person hold, and what work may they do?\"",
    "Department administrators do all their work in Kaveri application screens. They never need to open the IAM system.",
]

# (activity, kaveri summary, iam summary, owner, BRD section)
SUMMARY = [
    ["Citizen registration", "Aadhaar e-KYC link with UIDAI", "Account, Username, email and mobile OTP", BOTH, "4.1"],
    ["DSR Officer registration", "Screen, posts with vacancy, office checks", "Creates the login (KGID)", BOTH, "4.6.1"],
    ["Other Department user registration", "Screen, Username, role, end date", "Creates the login", BOTH, "4.6.2"],
    ["Citizen and Other Department user login", "Home page and allowed menus", "Captcha, OTP, lock-out, sign-out rules", IAM, "4.2, 4.3"],
    ["DSR Officer login and post selection", "Posts held, leave check, additional charge", "Captcha, face / biometric, access for the selected post", BOTH, "4.5.2"],
    ["Lost mobile, change of mobile or email", "Profile and admin screens", "OTP / PIN checks and update", IAM, "4.5.2.2, 4.5.2.3"],
    ["Transfer In", "Whole process", "No action", KAV, "4.6.4"],
    ["Relieving / Transfer Out", "Whole process and night-time update", "Ends the officer's open session", KAV, "4.6.3, 4.6.5"],
    ["Temporary absence and temporary charge", "Whole process", "Blocks sign-in during absence", KAV, "4.6.6"],
    ["Creating / modifying roles and their access", "Whole process", "No set-up; applies roles at sign-in", KAV, "4.5.1, 4.5.4, 4.5.6"],
    ["Creating / modifying sanctioned posts for each office", "Whole process", "No part", KAV, "4.5.3"],
    ["Creating / managing reporting hierarchies", "Whole process", "No part", KAV, "4.5.7, 4.5.8"],
    ["Suspend, deactivate or reactivate a user", "Screen, reason and history", "Stops or allows sign-in", BOTH, "4.7"],
    ["Kaveri 2.0 citizen migration", "Selecting, checking and reconciling data", "Creates accounts; first-login activation", BOTH, "4.8"],
    ["Reports and audit", "Keeps all records; all reports", "Passes sign-in records to Kaveri", KAV, "6"],
]

# (title, owner, one-line summary, [step rows: who, what happens], optional note)
ACTIVITIES = [
    ("Citizen registration", BOTH,
     "A citizen registers on their own; no approval is needed.",
     [["Citizen", "Opens Register and enters a preferred Username, email address and mobile number."],
      ["IAM", "Checks that the Username is free, sends one OTP to the email and one to the mobile, and checks both."],
      ["Kaveri application", "Connects to UIDAI and completes Aadhaar e-KYC."],
      ["IAM", "Records e-KYC as completed and creates the citizen's account."]],
     None),
    ("DSR Officer registration", BOTH,
     "An authorised administrator creates the officer and assigns post(s).",
     [["Administrator (Kaveri screen)", "Enters the officer's KGID (this becomes the Username) and mobile number."],
      ["Kaveri application", "Shows only posts with a vacancy at offices under the administrator; the administrator selects one or more posts."],
      ["IAM", "Creates the officer's login with KGID as Username and the mobile number."],
      ["Kaveri application", "Records the post(s) held by the officer."]],
     "Face / biometric details used for sign-in are held by IAM."),
    ("Other Department user registration", BOTH,
     "An authorised administrator creates the user with exactly one role.",
     [["Administrator (Kaveri screen)", "Selects the Department and enters Employee ID or KGID, official email, mobile, one role and an optional end date."],
      ["Kaveri application", "Forms the Username (Department Code + Employee ID / KGID) and checks it and the email domain."],
      ["IAM", "Creates the user's login."],
      ["Kaveri application", "Keeps the role and end date; on the end date it asks IAM to stop the login."]],
     None),
    ("Citizen and Other Department user login", IAM,
     "Sign-in is with Username, Captcha and OTP — there are no passwords.",
     [["User", "Enters Username and Captcha."],
      ["IAM", "Sends an OTP to the registered mobile and checks it. After 5 wrong attempts the Username is locked for 15 minutes."],
      ["IAM", "Opens the session. Signs the user out after 10 minutes without activity or after 4 hours. Only one session per user is allowed."],
      ["Kaveri application", "Shows the home page and only the menus the user's role is allowed to use."]],
     None),
    ("DSR Officer login and post selection", BOTH,
     "Sign-in is with KGID, Captcha and face or biometrics — no OTP.",
     [["Officer", "Enters KGID and Captcha."],
      ["IAM", "Checks the officer's face or biometrics."],
      ["Kaveri application", "Checks the officer is not on leave or absence today, and lists the posts the officer holds plus any temporary charge."],
      ["Officer", "Selects one post (selected automatically if only one)."],
      ["IAM and Kaveri application", "Access is given only for the selected post. Kaveri shows \"Role — Post — Office\" in the header."]],
     "Additional charge: after sign-in, the officer may take charge of an empty post under them in the same office. Kaveri lists the posts and records the charge; IAM switches access to that post until the officer switches back."),
    ("Lost mobile, change of mobile or email", IAM,
     "Each user type has its own rule.",
     [["Citizen — lost mobile", "IAM runs Aadhaar e-KYC, sends a PIN to the registered email, then an OTP to the new mobile, and updates the mobile."],
      ["Citizen / DSR Officer — change after sign-in", "Started from the Kaveri profile screen; IAM sends an OTP to the new mobile or email and updates it."],
      ["Other Department user", "Only an administrator can change mobile or email, in a Kaveri screen with a reason; IAM updates it."]],
     None),
    ("Transfer In", KAV,
     "A superior places an officer in a post that has a vacancy.",
     [["Superior (Kaveri screen)", "Selects the officer, an office under them, and a post with a vacancy; enters the Transfer / Reporting Order."],
      ["Kaveri application", "Checks the vacancy and reporting hierarchy, and records the officer in the post with immediate effect."],
      ["IAM", "No action. At the next sign-in the officer sees the new post."]],
     None),
    ("Relieving / Transfer Out", KAV,
     "A superior relieves an officer from a post.",
     [["Superior (Kaveri screen)", "Selects the officer's post and enters the Relieving Date, Relieving Reason and Relieving Order."],
      ["Kaveri application", "Keeps the officer in the post until the end of the Relieving Date."],
      ["Kaveri application (after midnight)", "Removes the officer from the post and updates the vacancy count."],
      ["IAM", "On Kaveri's request, ends any open session the officer has for that post."]],
     None),
    ("Temporary absence and temporary charge", KAV,
     "A superior records Leave, OOD or other absence and may give temporary charge to another officer.",
     [["Superior (Kaveri screen)", "Records the absence type, reason and from / to dates."],
      ["Kaveri application", "Keeps the post occupied (no vacancy is created)."],
      ["IAM", "Does not allow the absent officer to sign in during the absence and ends any open session."],
      ["Superior (Kaveri screen)", "Optionally gives temporary charge of the post to another officer."],
      ["Kaveri application", "The covering officer sees \"Temporary charge\" at sign-in. After the end date the charge is removed and the officer can sign in again."]],
     None),
    ("Creating / modifying roles and their access", KAV,
     "Roles and what each role can do are maintained only in the Kaveri application.",
     [["Application Admin (Kaveri screen)", "Creates and modifies roles, divisions, and which role belongs to which post."],
      ["Application Admin (Kaveri screen)", "Maintains modules and functions, and which role may use which function."],
      ["IAM", "No set-up. At sign-in, the roles of the selected post are applied to the user's session."]],
     None),
    ("Creating / modifying sanctioned posts for each office", KAV,
     "Posts and sanctioned strength are maintained only in the Kaveri application.",
     [["Application Admin (Kaveri screen)", "Maintains the list of posts and which posts are allowed in each type of office."],
      ["Application Admin (Kaveri screen)", "Sets the sanctioned strength of each post in each office."],
      ["Kaveri application", "Shows sanctioned, occupied and vacant counts for every post in every office."],
      ["IAM", "No part."]],
     None),
    ("Creating / managing reporting hierarchies", KAV,
     "Office hierarchy and officer reporting hierarchy are maintained only in the Kaveri application.",
     [["Application Admin (Kaveri screen)", "Maintains the office hierarchy (MS Building → IGR → DRO → SRO) and the officer reporting hierarchy."],
      ["Kaveri application", "Uses the hierarchies to decide who can create users, transfer, relieve or record absence for whom."],
      ["IAM", "No part."]],
     None),
    ("Suspend, deactivate or reactivate a user", BOTH,
     "An administrator stops or restores a user's access.",
     [["Administrator (Kaveri screen)", "Selects the user and enters the reason."],
      ["Kaveri application", "Keeps the reason and history and informs the user by SMS / email."],
      ["IAM", "Stops (or allows) sign-in immediately and ends any open session."]],
     None),
    ("Kaveri 2.0 citizen migration", BOTH,
     "Existing e-KYC-verified citizens are moved from Kaveri 2.0 so they need not register again.",
     [["Kaveri IT Cell (Kaveri application)", "Selects only citizens with e-KYC = true, checks the data, and confirms the counts match."],
      ["IAM", "Creates each account with the Kaveri 2.0 email ID as Username, the mobile and the email."],
      ["Citizen (first sign-in)", "Signs in with email ID, Captcha and OTP, verifies the email by OTP and accepts the privacy notice; the account then becomes active."]],
     None),
    ("Reports and audit", KAV,
     "All reports come from the Kaveri application.",
     [["IAM", "Records every sign-in, failed attempt and sign-out and passes them to the Kaveri application."],
      ["Kaveri application", "Keeps all records together and produces all reports listed in the BRD."]],
     None),
]

SUPPORT = [
    ["Department administrators", "Use Kaveri application screens only."],
    ["Application Admin", "Maintains roles, posts, sanctioned posts, hierarchies and access in Kaveri application screens."],
    ["Kaveri IT Cell", "Runs and looks after the IAM system and the Kaveri application; only Kaveri IT Cell staff open the IAM system."],
    ["Kaveri development team", "Builds the Kaveri application and the sign-in steps in IAM."],
]


def make_diagram(path: Path) -> None:
    W, H = 1800, 900
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    f_t = ImageFont.truetype(r"C:\Windows\Fonts\calibrib.ttf", 40)
    f_s = ImageFont.truetype(r"C:\Windows\Fonts\calibri.ttf", 28)
    f_i = ImageFont.truetype(r"C:\Windows\Fonts\calibri.ttf", 30)

    def panel(x0, title, sub, items, fill, out, tcol):
        d.rounded_rectangle((x0, 30, x0 + 760, 870), radius=22, fill=fill, outline=out, width=5)
        d.text((x0 + 40, 60), title, font=f_t, fill=tcol)
        d.text((x0 + 40, 115), sub, font=f_s, fill="#404040")
        y = 190
        for it in items:
            d.ellipse((x0 + 45, y + 11, x0 + 59, y + 25), fill=out)
            d.text((x0 + 80, y), it, font=f_i, fill="black")
            y += 58

    panel(40, "Kaveri application", "Department work",
          ["Screens for all administrators", "Posts held and post selection list",
           "Transfer In, Relieving / Transfer Out", "Temporary absence and charges",
           "Roles and what each role can do", "Sanctioned posts for each office",
           "Office and officer hierarchies", "Aadhaar e-KYC link with UIDAI",
           "SMS / email messages", "All records and reports"],
          "#F3F9EF", "#548235", "#375623")
    panel(1000, "IAM", "Identity and sign-in",
          ["Username and login details", "Mobile, email, e-KYC status",
           "Captcha and OTP checks", "Face / biometric check (DSR)",
           "Lock-out after wrong attempts", "Session: 10 min idle, 4 hours",
           "One session per user", "Stop / allow sign-in",
           "Access only for the selected post", "Sign-in records to Kaveri"],
          "#EEF4FB", "#2F5597", "#1F3A5F")

    for y, label in ((380, "work together"),):
        d.line((810, y, 990, y), fill="#404040", width=4)
        d.polygon([(990, y), (970, y - 12), (970, y + 12)], fill="#404040")
        d.polygon([(810, y), (830, y - 12), (830, y + 12)], fill="#404040")
        w = d.textlength(label, font=f_s)
        d.text((900 - w / 2, y - 45), label, font=f_s, fill="#1F3A5F")
    img.save(path)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    make_diagram(DIAGRAM)

    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

    sec = doc.sections[0]
    base.set_portrait(sec)
    base.header_footer(sec)
    sec.header.paragraphs[0].runs[0].text = "Kaveri 3.0  |  Who Does What — Kaveri Application and IAM"

    base.heading(doc, "Kaveri 3.0 — Who Does What: Kaveri Application and IAM", 0)
    base.para(doc, "User Management activities in simple terms")

    base.heading(doc, "Document Control", 2)
    base.add_table(doc, ["Field", "Value"], [
        ["Document ID", "DD-K3-IAM-002"],
        ["Version", DOC_VERSION],
        ["Status", "Draft for review"],
        ["Related documents", f"{base.BRD_REF}; Kaveri3_IAM_Ownership_Matrix_v1.0 (technical edition, DD-K3-IAM-001)"],
        ["Author (BA)", "Nandha Kumar"],
        ["Product Owner", "M V Prashanth"],
        ["Domain expert / reviewer", "Prabhakar Naik"],
        ["Target audience", "Department of Stamps and Registration — business owners and administrators"],
        ["Last updated", DOC_DATE],
    ], [5.0, 12.0])

    base.heading(doc, "Version History", 2)
    base.add_table(doc, ["Version", "Date", "Author", "Description"], [
        [DOC_VERSION, DOC_DATE, "Nandha Kumar", "Plain-language edition of the IAM ownership matrix, organised by User Management activity."],
    ], [2.0, 2.5, 3.0, 9.5])

    base.heading(doc, "1. Purpose", 1)
    for t in INTRO:
        base.para(doc, t)
    base.bullets(doc, PARTS)
    base.para(doc, PURPOSE_END)

    base.heading(doc, "2. The Simple Rule", 1)
    base.bullets(doc, RULES)
    doc.add_picture(str(DIAGRAM), width=Cm(16.0))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    base.heading(doc, "3. Summary — Who Does What", 1)
    base.para(doc, "Main owner colours: green = Kaveri application; blue = IAM; amber = both.")
    base.add_table(doc, ["Activity", "Kaveri application", "IAM", "Main owner", "BRD section"],
                   SUMMARY, [4.6, 4.4, 4.4, 2.0, 1.6], owner_col=3)

    base.heading(doc, "4. Activities in Detail", 1)
    for i, (title, owner, summary, steps, note) in enumerate(ACTIVITIES, start=1):
        base.heading(doc, f"4.{i} {title}", 2)
        p = doc.add_paragraph()
        r = p.add_run("Main owner: ")
        r.bold = True
        p.add_run(f"{owner}.  {summary}")
        rows = [[str(n), who, what] for n, (who, what) in enumerate(steps, start=1)]
        base.add_table(doc, ["Step", "Who", "What happens"], rows, [1.2, 4.6, 11.2])
        if note:
            base.para(doc, note)

    base.heading(doc, "5. Who Looks After What", 1)
    base.add_table(doc, ["Who", "Responsibility"], SUPPORT, [5.0, 12.0])

    base.heading(doc, "Approval", 1)
    base.para(doc, "By signing below, the stakeholders confirm they have reviewed and approved this document.")
    base.add_table(doc, ["Name", "Role", "Signature", "Date"], [
        ["M V Prashanth", "Product Owner", "", ""],
        ["Prabhakar Naik", "Domain expert / reviewer", "", ""],
        ["", "Kaveri IT Cell", "", ""],
    ], [4.5, 5.0, 4.0, 3.5])

    doc.save(str(DST))
    print(f"Saved {DST}")


if __name__ == "__main__":
    main()
