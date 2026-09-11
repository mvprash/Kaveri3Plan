# Document Registration – Process Diagrams

Swimlane process diagrams for Registration core (happy path) and Registration Act refusal / appeal / cancellation tracks.

---

## 1. Registration Core – Registration & Appointment (Happy Path)

End-to-end **happy path** for Schedule Sr.12 Registration + Appointment: online intake, SR send-for-payment, fee payment, SRO slot booking, office presentation with all parties present, admit & register, Sec. 60 certificate, return of document.

**Excluded branches (not drawn as pending workflows):** Sec. 45-A undervaluation; Stamp Act impounding; party-appearance pending (Secs. 36–39); private attendance (Sec. 31).

Sources: `Requirement Discussions/Daily Reports/Document_Registration_requirement_27082026_v1.1.docx`; `Document_Registration_requirement_28082026_v1.1.docx`; As-Is map in `ProcessDiagrams/Document_Registration_Online/`.

### Actors (lanes)

| Lane | Actor |
|------|--------|
| Citizen | Portal intake, payment, appointment, presentation, receive registered document |
| System | Validation, SD/RF compute, payment & slot confirm, registers, scan / Sec. 60, status |
| Sub-Registrar | Send for payment, examine, admit, Check & Register, return document |
| District Registrar | Jurisdiction / holiday master for appointment; **not invoked** for 45-A / impound on happy path |

### Files

| File | Purpose |
|------|---------|
| `Registration_Core_Appointment_Happy_Flow.drawio` | Editable diagrams.net swimlane (**open this**) |
| `Registration_Core_Appointment_Happy_Flow.png` | Exported PNG |
| `Registration_Core_Appointment_Happy_Flow.mmd` | Mermaid alternative |
| `_generate_registration_core_happy_drawio.py` | Regenerator |

### Flow (summary)

1. Citizen selects SRO by property jurisdiction → enters details → submits  
2. System validates & computes SD/RF (no 45-A trigger) → SR sends for payment  
3. Citizen pays → books appointment → visits SRO on appointed date (office attendance)  
4. SR examines; **happy path** confirms full SD/RF and all parties present at SRO  
5. Admit → endorsements → Check & Register → Sec. 60 → return registered document  

---

## 2. Registration Appeal – Classic Part XII (Secs. 71–77)

Swimlane for the **classic Registration Act Part XII** refusal / appeal path (not Karnataka Secs. 22-B / 22-C / 22-D).

### Actors (lanes)

| Lane | Actor |
|------|--------|
| Citizen | Presentant / person claiming under the document |
| System | Kaveri workflow, Book 2 recording, notifications, timeline checks |
| Sub-Registrar | Examination, Sec. 71 refusal, registration under order/decree |
| District Registrar | Sec. 72 appeal / Sec. 73 application, Sec. 74 enquiry, Sec. 75 / 76 orders |
| Civil Court | Sec. 77 suit and decree |

### Files

| File | Purpose |
|------|---------|
| `Registration_Appeal_Part_XII.drawio` | Editable diagrams.net swimlane (**open this**) |
| `Registration_Appeal_Part_XII.png` | Exported PNG |
| `Registration_Appeal_Part_XII.mmd` | Mermaid alternative |
| `_generate_part12_appeal_drawio.py` | Regenerator |

### Flow (summary)

1. **Sec. 71** — Sub-Registrar refuses → reasons in **Book 2** → copy to citizen  
2. Branch: **denial of execution?**  
   - **No** → **Sec. 72** appeal to District Registrar (≤ 30 days)  
   - **Yes** → **Sec. 73** application (≤ 30 days) → **Sec. 74** enquiry  
3. District Registrar: **Sec. 75** order to register **or** **Sec. 76** refuse  
4. If ordered: present again ≤ 30 days → register (effect from original presentation date)  
5. If Sec. 76: optional **Sec. 77** civil suit ≤ 30 days → decree may direct registration  

---

## 3. Karnataka Secs. 22-B / 22-C / 22-D — Forged / Prohibited Documents

Parallel **cancellation track** under the Registration (Karnataka Amendment) Act, 2023 (Karnataka Act 47 of 2024). Distinct from classic Part XII (Secs. 71–77).

Sources: `Acts_Rules/Document/TheRegistration(KarnatakaAmendment)Act2023(47of2024).pdf`; `Requirement Discussions/Daily Reports/Document_Registration_requirement_07092026_v1.1.docx`.

### Actors (lanes)

| Lane | Actor |
|------|--------|
| Citizen | Presentant / aggrieved person / parties to show-cause |
| System | 22-B screening, Book 2 / indexes, notices, limitation, status updates |
| Sub-Registrar | Sec. 22-B examination & mandatory refusal |
| District Registrar | Sec. 22-C suo motu / complaint, show-cause, cancellation |
| IGR | Sec. 22-D appeal (confirm / modify / cancel DR order) |
| Civil Court | Optional further judicial challenge after IGR (not Sec. 77) |

### Files

| File | Purpose |
|------|---------|
| `Registration_22BCD_Forged_Document.drawio` | Editable diagrams.net swimlane (**open this**) |
| `Registration_22BCD_Forged_Document.png` | Exported PNG |
| `Registration_22BCD_Forged_Document.mmd` | Mermaid alternative |
| `_generate_22bcd_drawio.py` | Regenerator |

### Flow (summary)

1. **Sec. 22-B** — System screens; SR refuses forged / prohibited / attached-property / notified documents (title disputes excluded) → Book 2 / status Refused (22-B)  
2. If no 22-B hit → register (may still face 22-C later)  
3. **Sec. 22-C** — DR suo motu **or** complaint by aggrieved person → Limitation Act (+ condonation) → show-cause to executants, parties, subsequent parties, affected persons → cancel **or** drop  
4. If cancelled → enter in books & indexes; notify (Rule 17(iii))  
5. **Sec. 22-D** — Appeal to **IGR** ≤ 30 days → confirm / modify / cancel DR order  
6. Optional **Civil Court** challenge after IGR (departmentally final if no suit)  
7. Secs. **81-A / 81-B** — penalties for registering in contravention of 22-B (compliance; not drawn as process steps)

**Note:** Statutory appeal under Sec. 22-D lies to the **Inspector General of Registration**, not to Civil Court under Sec. 77.

---

## Open / regenerate

- Open `.drawio` in [diagrams.net](https://app.diagrams.net) or the Draw.io VS Code extension.  
- Regenerate Happy Path: `python _generate_registration_core_happy_drawio.py`  
- Regenerate Part XII: `python _generate_part12_appeal_drawio.py`  
- Regenerate 22-B/C/D: `python _generate_22bcd_drawio.py`
