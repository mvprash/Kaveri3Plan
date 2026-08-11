# Business Requirements Document (BRD) — Template

## Marriage Registration Module — Hindu Marriage (Kaveri 3.0)

| Field | Value |
|--------|--------|
| **Document ID** | BRD-K3-MRG-HMA-001 |
| **Version** | 0.1 (Draft template) |
| **Status** | Draft / In review / Approved |
| **Module** | Marriage Registration |
| **Legal basis (primary)** | The Hindu Marriage Act, 1955 (Central Act 25 of 1955) |
| **State rules (primary)** | Registration of Hindu Marriage (Karnataka) Rules, 1966 |
| **Related inputs** | `Marriage/Hindu Marriage Act, 1955.pdf`, `Marriage/hindu marriage forms.pdf`, `Marriage/REGISTRATIONOFHINDUMARRIAGE_KARNATAKARULES_1966.docx`, `Marriage/RD48MNMU2023-Notification-marriage.pdf` (confirm applicability) |
| **Author (BA)** | [Name] |
| **Product Owner** | [Name] |
| **Domain expert / SRO reviewer** | [Name] |
| **Target audience** | PO, BA, Domain Expert, Solution Architect, Dev, QA, Content |
| **Last updated** | [Date] |

---

## Document control

| Version | Date | Author | Summary of change | Approver |
|---------|------|--------|-------------------|----------|
| 0.1 | [Date] | [BA] | Initial template / discovery draft | [PO] |
| | | | | |

**Distribution:** [Confluence space / SharePoint link]

**Related documents:**

| ID | Title | Link |
|----|--------|------|
| BRD-K3-MRG-HMA-001 | This document | |
| PROC-K3-MRG-HMA-ASIS-001 | As-Is process (Hindu registration) | [TBD] |
| PROC-K3-MRG-HMA-TOBE-001 | To-Be process flows | [TBD] |
| RTM-K3-MRG-HMA-001 | Requirements traceability matrix | [TBD] |
| DEC-K3-MRG-001 | Decision log | [TBD] |
| BRD-K3-MRG-SMA-001 | Special Marriage (separate BRD) | Out of scope for this template unless merged |

---

## 1. Executive summary

**Purpose:** [2–3 sentences — e.g. Enable citizens and Sub-Registrars to register Hindu marriages under Section 8 of the Hindu Marriage Act, 1955, per Karnataka Rules 1966, through Kaveri 3.0 with statutory forms, fees, audit trail, and certificate issuance.]

**Business problem:** [Current pain points from Kaveri 2.0 / manual process — queues, rework, jurisdiction errors, document gaps, Kannada UX, etc.]

**Proposed solution (high level):** [Citizen online application → document upload → fee → SRO scrutiny → register memorandum → Form II-A certificate; optional counter/SRO-assisted path.]

**Success criteria (measurable):** [e.g. % applications registered within X working days; reduction in rejection/rework; statutory compliance sign-off from Domain Expert.]

**Phase / MVP boundary:** [Confirm with PO — Hindu post-solemnization registration only in Phase 1; exclude divorce/nullity workflows unless explicitly in scope.]

---

## 2. Scope

### 2.1 In scope (Hindu Marriage — Phase [1])

- Registration of **already solemnized** Hindu marriages under **Section 8**, HMA 1955.
- Statutory artefacts: **Form I** (Memorandum), **Form IA** (Application), **Form II** (Registrar endorsement), **Form II-A** (Certificate), **Form III** (monthly duplicate bundle certificate to Registrar-General) — system support as applicable.
- Jurisdiction: marriage place **or** ordinary residence of bride/bridegroom (per Karnataka Rule 4, as amended).
- Parties: bride, bridegroom, **three witnesses** (memorandum signed by three witnesses per Rule 4(3)).
- Citizen portal + SRO desk workflows: apply, pay fee, scrutiny, approve/reject, register, issue certificate, reprint/corrected extract (per rules).
- Integrations: [payment, Aadhaar/eKYC, DigiLocker, SMS — mark TBD per PO].
- Bilingual UI: English + Kannada (labels, certificate text where mandated).
- Audit trail, role-based access, MIS/reporting for department.

### 2.2 Out of scope (unless PO promotes)

- Special Marriage Act 1954 (separate BRD).
- Parsi / Christian / Muslim marriage Acts.
- Matrimonial petitions (divorce, judicial separation, restitution) under HMA Part III onward.
- Priest-led solemnization scheduling (unless department requires).
- Legacy data migration detail (flag for Data Migration specialist; high-level requirements only here).

### 2.3 Assumptions

| ID | Assumption | Owner to validate |
|----|------------|-------------------|
| A-01 | Sub-Registrars under Indian Registration Act, 1908 act as **Registrars of Hindu Marriages** for their jurisdiction (Karnataka notification) | Domain Expert |
| A-02 | Registration is **optional** under Section 8 but **mandatory for process** once parties choose to register via Kaveri | Legal / DE |
| A-03 | Joint photograph on memorandum is required as per Form I layout | DE / SRO |
| A-04 | Fee schedule follows Karnataka Rules Schedule + RD48 notification where applicable | Treasury / DE |
| A-05 | [TBD] | |

### 2.4 Constraints

- GIGW / MeitY guidelines, accessibility (WCAG 2.x), Karnataka e-Gov hosting/security norms.
- Aadhaar / eKYC usage only as approved by department and UIDAI compliance.
- No alteration of statutory form **wording** on generated outputs without legal approval.

---

## 3. Legal and regulatory reference

### 3.1 Primary legislation — Hindu Marriage Act, 1955 (selected sections for registration)

| Section | Topic | BRD relevance |
|---------|--------|----------------|
| 2 | Application of Act | Who may register as Hindu marriage (Hindu, Buddhist, Jaina, Sikh; exclusions e.g. Scheduled Tribe unless notified) |
| 3 | Definitions | Custom, sapinda, degrees of prohibited relationship — validation rules |
| 5 | Conditions for marriage | Eligibility declarations in Form IA; system validations where automatable |
| 7 | Ceremonies | Declaration that marriage solemnized per customary rites |
| 8 | Registration | Core registration authority; state rules under sub-section (1) |
| 11–12 | Void / voidable | [Optional] flags for SRO manual review; not full court workflow |
| 17–18 | Penalties | Inform citizen/SRO messaging; no bigamy if spouse living (Sec. 5(i)) |

**Section 5 — conditions (for business rules table):**

| Condition | Statutory requirement | System handling (To-Be) |
|-----------|----------------------|-------------------------|
| 5(i) | Neither party has a spouse living at time of marriage | Mandatory declaration + [TBD: document / cross-check] |
| 5(ii) | Valid consent; no unsoundness of mind etc. | Declaration; SRO may reject |
| 5(iii) | Bridegroom ≥ 21 years; Bride ≥ 18 years at marriage | DOB/age validation vs marriage date |
| 5(iv) | Not within degrees of prohibited relationship (unless custom) | [TBD: relationship capture + rule engine / manual] |
| 5(v) | Not sapindas of each other (unless custom) | [TBD: as above] |

**Section 7:** Marriage solemnized per **customary rites and ceremonies** of either party — capture ceremony type/description; SRO verification.

**Section 8:** Parties may furnish particulars; state may make rules for registration and evidence — drives forms, register, certificate.

### 3.2 Karnataka Rules, 1966 (operational rules)

| Rule | Requirement | System feature |
|------|-------------|----------------|
| 3 | Appointment of Registrars (Sub-Registrars) | Office/jurisdiction master; route application to correct SRO |
| 4(1) | Form I memorandum in **duplicate**; deliver in person or registered post; jurisdiction: place of marriage **or** ordinary residence of bride/bridegroom | Dual copy tracking; office selection logic |
| 4(2) | Memorandum accompanied by **Form IA** application | Linked application record |
| 4(3) | Memorandum and duplicate signed by **three witnesses** | Three witness records + e-sign / signature capture [TBD] |
| 4(4) | Registrar endorsement **Form II** on reverse; paste memorandum in serial register | Register serial no., page, volume; endorsement generation |
| 4(5) | Issue **Form II-A** certificate on completion | Certificate PDF + QR/seal [TBD] |
| 4 (duplicates) | Monthly Form III bundle to Registrar-General | Batch job / export [TBD] |
| 4 (scrutiny) | Scrutinise memorandum + IA; refuse incomplete; written order to parties | Rejection workflow with reason codes |
| 8 | Certified extracts; fees per Schedule | Fee master; receipt Form VI |
| Indices | Form IV, Form V | Reporting / search indexes |

### 3.3 Statutory forms mapping

| Form | Rule ref | Purpose | Generated by |
|------|----------|---------|--------------|
| Form I | Rule 4 | Memorandum of marriage (duplicate) | System from captured data + joint photo |
| Form IA | Rule 4(2) | Application to enter particulars in register | System + party signatures |
| Form II | Rule 4(4) | Endorsement on reverse of memorandum | SRO on registration |
| Form II-A | Rule 4(5) | Certificate of registration | System on approval |
| Form III | Rule 4 (duplicates clause) | Certificate on monthly duplicate bundle | Back-office batch |
| Form VI | Rule on fees | Fee receipt | Payment integration |

---

## 4. Stakeholders and actors

| Actor | Description | Primary goals | Channels |
|-------|-------------|---------------|----------|
| Citizen (applicant) | Bride and/or bridegroom | Submit accurate application, pay fee, receive certificate | Web portal / mobile [TBD] |
| Bride / Bridegroom | Parties to marriage | Sign declarations, provide documents | Portal / SRO counter |
| Witness (×3) | Present at solemnization | Identity, address, signature on memorandum | Portal e-KYC [TBD] / counter |
| Marriage Registrar / Sub-Registrar | Statutory registrar | Scrutiny, register, endorse, refuse with order | SRO desk |
| IGSR / senior office | Oversight | Monitoring, escalations | Admin console |
| Treasury / payment gateway | Fee collection | Reconciliation | Integration |
| Registrar-General | State-level register | Receive Form III duplicates | Batch/export |
| Domain Expert | Validation | Sign-off on rules and forms | Review workshops |
| CSG / Kaveri 2.0 support | Legacy reference | As-is behaviour | KT sessions |

**RACI (summary):** [TBD matrix for key process steps]

---

## 5. Definitions and glossary

| Term | Definition | Source |
|------|------------|--------|
| Memorandum | Form I particulars of marriage | Karnataka Rules |
| Registrar | Registrar of Hindu Marriages (Sub-Registrar) | Rules + notification |
| Register | Paste-book Hindu Marriage Register | Rule 4(4) |
| Solemnization | Performance of customary rites (Section 7) | HMA 1955 |
| Ordinary residence | [Define operational rule for jurisdiction] | DE / Rule 4 |
| Sapinda / prohibited relationship | As Section 3 | HMA 1955 |
| [TBD] | | |

---

## 6. Current state (As-Is)

### 6.1 As-Is process summary

[Describe end-to-end flow: citizen visit / Kaveri 2.0 / manual Form I–IA submission, physical register, certificate issuance.]

**Diagram:** [Insert BPMN / swimlane — Citizen | SRO | Treasury | Register book]

### 6.2 As-Is systems

| System | Role | Pain points |
|--------|------|-------------|
| Kaveri 2.0 | [TBD] | |
| Manual register | Form I paste book | |
| Payment | [Challan / online] | |

### 6.3 As-Is pain points

| ID | Pain point | Impact | To-Be address (ref §) |
|----|------------|--------|------------------------|
| P-01 | [TBD] | | |
| P-02 | | | |

---

## 7. Future state (To-Be)

### 7.1 To-Be process overview

**Happy path (MVP):**

1. Citizen selects **Hindu Marriage Registration** (post-solemnization).
2. Declarations (Section 5, 7, 8 / Form IA text).
3. Capture marriage details (date, place, jurisdiction).
4. Capture bride, bridegroom, three witnesses.
5. Upload documents (joint photo, age proof, address, [TBD]).
6. Pay statutory fee → receipt (Form VI equivalent).
7. Application routed to **Registrar** for jurisdiction.
8. SRO **scrutinises**; may request correction; may **refuse** with brief written order (Rule 4).
9. On approval: assign **serial no. / page / volume**; generate **Form II** endorsement; update register; issue **Form II-A**.
10. Citizen downloads certificate; optional certified extract request later (Rule 8).

**Diagram:** [Insert To-Be BPMN]

### 7.2 Application channels

| Channel | Description | MVP? |
|---------|-------------|------|
| Online (citizen self-service) | Full digital flow | Yes [TBD] |
| SRO-assisted (counter) | Data entry on behalf of citizen | [TBD] |
| Hybrid | Online apply + physical document verification | [TBD] |

### 7.3 Application status model

| Status | Description | Actor | Next states |
|--------|-------------|-------|-------------|
| Draft | Saved not submitted | Citizen | Submitted |
| Submitted | Awaiting payment | Citizen | Paid / Cancelled |
| Paid | Awaiting scrutiny | System | Under scrutiny |
| Query raised | Defect / incomplete | SRO | Resubmitted |
| Rejected | Refusal order issued | SRO | Closed |
| Registered | Entered in register | SRO | Certificate issued |
| Certificate issued | Form II-A delivered | System | Closed |
| [TBD] | | | |

---

## 8. Functional requirements

> **Convention:** Req ID `FR-HMA-###`. Priority: Must / Should / Could. Trace to Act/Rule in RTM.

### 8.1 Eligibility and module entry

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-HMA-001 | System shall allow registration only for marriages claimed to be solemnized under HMA 1955 (Section 2 applicability) | Must | [Given/When/Then] |
| FR-HMA-002 | System shall block or warn if marriage date is in future | Must | |
| FR-HMA-003 | System shall enforce minimum age at **date of marriage**: bridegroom 21, bride 18 (Section 5(iii)) | Must | |
| FR-HMA-004 | System shall capture marital status at time of marriage (unmarried / widower / widow / divorced) per Form I | Must | |

### 8.2 Jurisdiction and office routing

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-HMA-010 | Applicant shall select basis for jurisdiction: place of marriage **or** ordinary residence of bride/bridegroom (Rule 4) | Must | |
| FR-HMA-011 | System shall route application to Sub-Registrar office matching selected jurisdiction | Must | |
| FR-HMA-012 | If memorandum relates to marriage **outside** registrar jurisdiction, system shall support forward to correct registrar with intimation (Rule 4(2) second part / defect rule) | Should | |

### 8.3 Data capture — marriage details (Form I items 1–2)

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-HMA-020 | Capture **date of marriage** | Must | |
| FR-HMA-021 | Capture **place of marriage** with sufficient particulars to locate (address, district, state) | Must | |
| FR-HMA-022 | Capture description of **ceremony / rites** (Section 7) | Should | |

### 8.4 Data capture — bridegroom (Form I §3)

| Field (statutory) | Mandatory | Validation / notes | Kaveri 3.0 field name |
|-------------------|-----------|--------------------|------------------------|
| Full name | Y | | [TBD] |
| Father's name | Y | | |
| Mother's name | Y | | |
| Age at marriage | Y | Cross-check DOB | |
| Usual place of residence | Y | Jurisdiction helper | |
| Address | Y | | |
| Status (unmarried/widower/divorced) | Y | | |
| Signature + date | Y | e-sign / upload [TBD] | |

### 8.5 Data capture — bride (Form I §4)

| Field (statutory) | Mandatory | Validation / notes | Kaveri 3.0 field name |
|-------------------|-----------|--------------------|------------------------|
| Full name | Y | | [TBD] |
| Father's name | Y | | |
| Mother's name | Y | | |
| Age at marriage | Y | | |
| Usual place of residence | Y | | |
| Address | Y | | |
| Status (unmarried/widow/divorced) | Y | | |
| Signature + date | Y | | |

### 8.6 Data capture — witnesses (Form I §5–7, Rule 4(3))

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-HMA-060 | System shall capture **exactly three** witnesses | Must | |
| FR-HMA-061 | Each witness: full name, blood relation if any, age, usual residence, address, signature + date | Must | |
| FR-HMA-062 | Witness identity verification via [Aadhaar e-KYC / manual] | Should | |

### 8.7 Form IA — application and declarations

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-HMA-070 | Generate Form IA addressed to Registrar of Marriage for selected office | Must | |
| FR-HMA-071 | Capture statutory declarations (I) valid marriage registrable under Section 8; (II) Section 5 conditions satisfied; (III) particulars true to best knowledge | Must | Both parties sign |
| FR-HMA-072 | Capture solemnization date in IA narrative (align with Form I) | Must | |

### 8.8 Documents and memorandum

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-HMA-080 | Upload **joint photo** of bride and bridegroom (Form I header) | Must | Attestation workflow [TBD] |
| FR-HMA-081 | Support **duplicate** memorandum (original + duplicate) — print or electronic equivalent | Must | |
| FR-HMA-082 | Document checklist: [age proof, address proof, divorce decree if applicable — DE to confirm] | Must | |

### 8.9 Fees and payments

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-HMA-090 | Apply fee per Karnataka Rules Schedule + applicable notifications | Must | |
| FR-HMA-091 | Issue payment receipt equivalent to Form VI; credit to government account | Must | |
| FR-HMA-092 | Waive search fee when certified copy requested with marriage application (Rule 8 proviso) | Should | |

### 8.10 SRO scrutiny and registration

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-HMA-100 | SRO shall view complete application, documents, payment status | Must | |
| FR-HMA-101 | SRO may require parties to remedy defects within specified time (defect rule) | Must | Audit trail |
| FR-HMA-102 | SRO shall **refuse** incomplete memorandum/IA with brief **written order** communicated to parties | Must | |
| FR-HMA-103 | On acceptance: record receipt date; assign **serial no., page, volume**; generate **Form II** endorsement | Must | |
| FR-HMA-104 | On completion: issue **Form II-A** certificate immediately (Rule 4(5)) | Must | Deliver in person / post / download [TBD] |

### 8.11 Post-registration services

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-HMA-110 | Certified extract from register on application and fee (Rule 8) | Should | |
| FR-HMA-111 | Reprint / duplicate certificate controls with audit | Should | |
| FR-HMA-112 | Correction workflow [TBD — department policy] | Could | |

### 8.12 Notifications

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-HMA-120 | SMS/email on submission, query, rejection, registration, certificate | Should | |
| FR-HMA-121 | Kannada + English notification templates | Should | |

### 8.13 Reports and MIS

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-HMA-130 | Register-wise marriage count by period | Must | |
| FR-HMA-131 | Pending scrutiny aging | Should | |
| FR-HMA-132 | Fee collection reconciliation report | Must | |
| FR-HMA-133 | Monthly duplicate memoranda bundle for Registrar-General (Form III) | Should | |

---

## 9. Business rules

| Rule ID | Description | Statutory ref | System enforcement |
|---------|-------------|---------------|-------------------|
| BR-HMA-001 | No registration without three witness signatures on memorandum | Rule 4(3) | Hard stop at submit |
| BR-HMA-002 | Memorandum must accompany Form IA | Rule 4(2) | Hard stop |
| BR-HMA-003 | Age at marriage ≥ statutory minimum | Sec. 5(iii) | Validation on marriage date |
| BR-HMA-004 | Neither party married at time of marriage | Sec. 5(i) | Declaration + [TBD] |
| BR-HMA-005 | Marriage must be solemnized (past date) | Sec. 7, 8 | Date ≤ today |
| BR-HMA-006 | Jurisdiction routing per Rule 4(1) | Rules 1966 | Office master |
| BR-HMA-007 | Refusal must be in writing | Rule 4(3) scrutiny clause | Rejection letter PDF |
| BR-HMA-008 | [Custom / sapinda exception handling] | Sec. 5(iv)(v) | Manual SRO override [TBD] |

---

## 10. User stories / use cases (template)

### 10.1 Use case format

| Field | Content |
|-------|---------|
| **Use case ID** | UC-HMA-### |
| **Name** | |
| **Actor(s)** | |
| **Preconditions** | |
| **Trigger** | |
| **Main flow** | 1. … 2. … |
| **Alternate flows** | |
| **Postconditions** | |
| **Business rules** | BR-HMA-### |
| **Statutory trace** | Sec. / Rule |

### 10.2 Starter backlog (MVP)

| Story ID | As a… | I want… | So that… | Priority |
|----------|-------|---------|----------|----------|
| US-HMA-01 | Citizen | to start Hindu marriage registration online | I can register my solemnized marriage | Must |
| US-HMA-02 | Citizen | to complete Form I/IA data and declarations | my application is legally complete | Must |
| US-HMA-03 | Citizen | to pay the registration fee online | my application moves to SRO scrutiny | Must |
| US-HMA-04 | SRO | to scrutinize and approve/reject applications | only valid marriages enter the register | Must |
| US-HMA-05 | SRO | to assign register serial and issue Form II-A | parties receive statutory certificate | Must |
| US-HMA-06 | Citizen | to download Form II-A certificate | I have proof of registration | Must |

---

## 11. User interface (high-level)

| Screen / step | Purpose | Statutory alignment | Notes |
|---------------|---------|---------------------|-------|
| Mode selection | Online vs counter | | Prototype: hindu-marriage-mode |
| Declarations | Form IA declarations | Sec. 5, 7, 8 | hindu-marriage-online |
| Marriage details | Date, place, jurisdiction | Form I §1–2 | hindu-marriage-details |
| Bride / Bridegroom | Party particulars | Form I §3–4 | hindu-marriage-bride(groom) |
| Witnesses (×3) | Witness particulars | Form I §5–7 | hindu-marriage-witnesses |
| Review summary | Confirm before pay | | |
| Document upload | Joint photo, proofs | Form I | |
| Payment | Fee | Form VI | |
| SRO workbench | Scrutiny, register, refuse | Form II, register | |
| Certificate view | Form II-A | Rule 4(5) | |

**Wireframe links:** [Figma / prototype URLs]

**Bilingual:** All labels `[EN / KN]` — content manager sign-off.

---

## 12. Integrations

| Integration | Direction | Purpose | Owner | Status |
|-------------|-----------|---------|-------|--------|
| Payment gateway / Treasury | Outbound | Registration fee | | TBD |
| Aadhaar / e-KYC | Outbound | Witness/party identity | | TBD |
| DigiLocker | Outbound/Inbound | Document fetch | | TBD |
| SMS gateway | Outbound | Alerts | | TBD |
| Existing Kaveri master data | Inbound | Districts, SRO offices | | TBD |

**Interface requirements:** [API list TBD by Architect]

---

## 13. Non-functional requirements

**Owners to validate targets:** Solution Architect, DevOps/SDC, Security, DBA, Ops (L2), PO.  
**Baseline signals from programme docs:** design for government-scale concurrency (10,000+ concurrent users as architecture skill bar); GIGW / MeitY / CERT-In / STQC / Aadhaar / UIDAI; Karnataka e-Gov hosting; permanent register preservation (Rule 10(2)).

### 13.1 Availability

| NFR ID | Requirement | Target / measure | Owner |
|--------|-------------|------------------|--------|
| NFR-HMA-AVA-001 | Required service availability for citizen portal and SRO desk (excl. approved maintenance) | [e.g. 99.5% / 99.9% monthly — TBD] | Arch, Ops |
| NFR-HMA-AVA-002 | Planned maintenance windows (day/time, max duration, notice period) | [e.g. Sunday 02:00–06:00 IST; ≥72h notice — TBD] | Ops, PO |
| NFR-HMA-AVA-003 | Unplanned outage communication and status page / SMS to SROs | Process + RACI TBD | Ops |
| NFR-HMA-AVA-004 | High-availability topology for app, API, DB (active-active / active-passive) | Per SDC / Karnataka hosting design — TBD | Arch, SDC |

### 13.2 Performance

| NFR ID | Requirement | Target / measure | Owner |
|--------|-------------|------------------|--------|
| NFR-HMA-PERF-001 | Page / API response-time targets (p95) for key citizen and SRO actions | [e.g. ≤2s browse; ≤3s submit; ≤5s certificate PDF — TBD] | Arch, Perf Lead |
| NFR-HMA-PERF-002 | Peak concurrent users (citizen + SRO combined) | [Align to platform capacity; programme reference ≥10,000 concurrent — confirm Marriage module share — TBD] | Arch |
| NFR-HMA-PERF-003 | Peak transaction volumes (applications submitted, payments, certificate issues per hour/day) | [Baseline from Kaveri 2.0 marriage stats + growth — TBD] | PO, Arch |
| NFR-HMA-PERF-004 | Batch jobs (Form III monthly duplicate bundle) complete within defined window | [e.g. by 05th of month + buffer — TBD] | Arch, DBA |
| NFR-HMA-PERF-005 | Performance / load test gate before go-live | Pass criteria TBD; Perf & Security Test Lead owns | Perf Lead |

### 13.3 Scalability

| NFR ID | Requirement | Target / measure | Owner |
|--------|-------------|------------------|--------|
| NFR-HMA-SCALE-001 | Expected growth in registered citizens / portal users (Y1–Y3) | [TBD from department projections] | PO |
| NFR-HMA-SCALE-002 | Expected growth in marriage registrations per year | [TBD from IGSR / historical volumes] | PO, DE |
| NFR-HMA-SCALE-003 | Document / attachment volume growth (photos, proofs, PDFs) and storage plan | [TBD GB/TB + retention] | Arch, DBA |
| NFR-HMA-SCALE-004 | Integration call volume growth (payment, Aadhaar/eKYC, DigiLocker, SMS) | [TBD TPS / daily caps] | Integration Eng |
| NFR-HMA-SCALE-005 | Horizontal scale-out of app/API; DB scale (read replicas / partitioning) as load grows | Architecture pattern TBD | Arch |

### 13.4 Security

| NFR ID | Requirement | Target / measure | Owner |
|--------|-------------|------------------|--------|
| NFR-HMA-SEC-001 | Authentication: citizen (login / eKYC as approved), SRO / admin (department IdP / SSO) | Mechanism TBD; MFA for privileged roles TBD | Security, Arch |
| NFR-HMA-SEC-002 | Authorization: RBAC for citizen vs SRO vs admin; least privilege; jurisdiction-scoped SRO access | Role matrix signed off | Security, PO |
| NFR-HMA-SEC-003 | Encryption in transit (TLS) and at rest for PII, documents, certificates | TLS 1.2+; at-rest per SDC standard — TBD | Security, SDC |
| NFR-HMA-SEC-004 | Secrets management (keys, DB creds, API keys); no secrets in source | Vault / SDC standard — TBD | DevOps, Security |
| NFR-HMA-SEC-005 | Hardening: OS, containers, WAF, SSL certs, privileged access control | Per MeitY / CERT-In / SDC baseline | Security, DevOps |
| NFR-HMA-SEC-006 | Vulnerability management: periodic scans, patch SLA, third-party / CERT-In / STQC audits | Scan cadence + severity SLAs TBD | Security, Perf Lead |
| NFR-HMA-SEC-007 | Certificate integrity: QR / digital seal / anti-tamper on Form II-A | Mechanism TBD | Arch, Security |
| NFR-HMA-SEC-008 | Aadhaar / eKYC usage only as approved; UIDAI-compliant handling | Compliance checklist | Security, Legal |

### 13.5 Privacy

| NFR ID | Requirement | Target / measure | Owner |
|--------|-------------|------------------|--------|
| NFR-HMA-PRIV-001 | PII inventory for marriage module (parties, witnesses, Aadhaar refs, photos, addresses) | Data classification sheet | Arch, DBA, Security |
| NFR-HMA-PRIV-002 | Masking / redaction in UI, logs, support tools, non-prod environments | Mask Aadhaar and sensitive IDs by default | Security, Dev |
| NFR-HMA-PRIV-003 | Retention: statutory registers permanent per Rule 10(2); operational / log / attachment retention per govt policy | Register = permanent; others TBD | DBA, Legal, DE |
| NFR-HMA-PRIV-004 | Access controls: need-to-know for PII; no bulk export without authorized role | Role + approval path TBD | Security, Ops |
| NFR-HMA-PRIV-005 | Non-prod data: anonymized / synthetic; no raw production PII in lower envs unless approved | Policy TBD | DBA, Security |

### 13.6 Audit

| NFR ID | Requirement | Target / measure | Owner |
|--------|-------------|------------------|--------|
| NFR-HMA-AUD-001 | Immutable audit of status changes, SRO scrutiny actions, approvals/rejections, fee events | Append-only / WORM as designed | Arch, Security |
| NFR-HMA-AUD-002 | Audit of certificate issuance, reprint / duplicate, corrections | Linked to Form II-A / extract | Arch |
| NFR-HMA-AUD-003 | Login / privilege / config-change audit for admin and SRO accounts | Retain per security policy — TBD | Security |
| NFR-HMA-AUD-004 | Audit evidence available for departmental / AG / security audits | Export / report format TBD | Ops, Security |
| NFR-HMA-AUD-005 | Audit log retention and reporting cadence (MIS + on-demand) | Retention TBD; MIS ownership TBD | DBA, PO |

### 13.7 Disaster recovery (DR)

| NFR ID | Requirement | Target / measure | Owner |
|--------|-------------|------------------|--------|
| NFR-HMA-DR-001 | Recovery Point Objective (RPO) | [e.g. ≤15 min / ≤1 h — TBD] | Arch, DBA, SDC |
| NFR-HMA-DR-002 | Recovery Time Objective (RTO) | [e.g. ≤4 h / ≤8 h — TBD] | Arch, Ops, SDC |
| NFR-HMA-DR-003 | DR topology (primary / DR site, replication mode) | Per Karnataka SDC / hosting design — TBD | Arch, SDC |
| NFR-HMA-DR-004 | Failover expectations (auto vs manual; decision authority) | Runbook + drill cadence TBD | Ops, Arch |
| NFR-HMA-DR-005 | Failback expectations and data reconciliation after DR | Runbook TBD | DBA, Ops |
| NFR-HMA-DR-006 | Backup schedule, restore test frequency, last successful restore evidence | [e.g. daily full + continuous WAL; quarterly restore drill — TBD] | DBA |

### 13.8 Operations

| NFR ID | Requirement | Target / measure | Owner |
|--------|-------------|------------------|--------|
| NFR-HMA-OPS-001 | Support model L1 / L2 / L3 with hours of cover and escalation matrix | Model + SLA draft (Transition / Ops) | Ops, PM |
| NFR-HMA-OPS-002 | Monitoring: app health, API latency/errors, DB, integrations, certificate job | Dashboards + thresholds TBD | DevOps, L2 |
| NFR-HMA-OPS-003 | Alerting: severity, paging / ticket routing, acknowledgment SLA | Severity matrix TBD | Ops |
| NFR-HMA-OPS-004 | Incident response: classify, contain, communicate, RCA, post-incident review | ITIL-aligned process TBD | Ops, Security |
| NFR-HMA-OPS-005 | Ownership: service owner, application owner, infra owner, data owner | Named RACI TBD | PO, Arch, SDC |
| NFR-HMA-OPS-006 | Runbooks for critical paths (submit, pay, register, certificate, restore) | Pack complete before go-live | Ops, Arch |

### 13.9 Capacity

| NFR ID | Requirement | Target / measure | Owner |
|--------|-------------|------------------|--------|
| NFR-HMA-CAP-001 | Compute sizing assumptions (app / API / workers) for peak + headroom | [vCPU / nodes — TBD] | Arch, SDC |
| NFR-HMA-CAP-002 | Memory sizing assumptions | [GB — TBD] | Arch, SDC |
| NFR-HMA-CAP-003 | Storage sizing: DB + document/object store + growth for Y1–Y3 | [TB + growth % — TBD] | DBA, Arch |
| NFR-HMA-CAP-004 | Database capacity: connections, IOPS, HA/replica footprint | [TBD] | DBA |
| NFR-HMA-CAP-005 | Network: bandwidth, latency to SDC / DR / integration endpoints | [TBD] | SDC, Arch |
| NFR-HMA-CAP-006 | Capacity review cadence (quarterly or before peak seasons) | Process TBD | Arch, Ops |

### 13.10 Compliance

| NFR ID | Requirement | Target / measure | Owner |
|--------|-------------|------------------|--------|
| NFR-HMA-COMP-001 | GIGW compliance for citizen-facing UI | Checklist sign-off | Content, UI, Security |
| NFR-HMA-COMP-002 | Accessibility: WCAG 2.x, keyboard, screen reader | Level TBD (AA preferred) | UI, QA |
| NFR-HMA-COMP-003 | MeitY / CERT-In security guidelines and advisories | Audit readiness | Security |
| NFR-HMA-COMP-004 | STQC / hosting / security clearance as required by department | Clearance path TBD | Security, SDC |
| NFR-HMA-COMP-005 | Aadhaar / UIDAI and Karnataka e-Gov hosting/security norms | Compliance evidence | Security, Legal |
| NFR-HMA-COMP-006 | Localization: Kannada + English UI; Kannada fonts on screen and PDF certificates | Rendering QA gate | Content, Dev, QA |
| NFR-HMA-COMP-007 | No alteration of statutory form wording without legal approval | Legal sign-off on templates | Legal, DE |
| NFR-HMA-COMP-008 | Government records / archival policy alignment for registers and audit evidence | Policy mapping TBD | DBA, Legal |

### 13.11 NFR open points (decision log)

| # | Topic | Decision needed | Owner | Due |
|---|--------|-----------------|-------|-----|
| NFR-OP-01 | Availability % and maintenance window | Confirm with SDC / Ops | Arch, Ops | |
| NFR-OP-02 | p95 latency + concurrent users + peak TPS | Load model from Kaveri 2.0 + growth | Arch, PO | |
| NFR-OP-03 | RPO / RTO and DR topology | SDC DR standard vs module-specific | Arch, SDC | |
| NFR-OP-04 | AuthN mechanism (citizen + SRO) and MFA | Security design | Security | |
| NFR-OP-05 | PII retention beyond permanent registers | Archive vs purge rules | Legal, DBA | |
| NFR-OP-06 | Certificate QR / digital seal approach | Product + Security | Arch, PO | |
| NFR-OP-07 | L1/L2/L3 hours and incident SLAs | Support model | Ops, PM | |
| NFR-OP-08 | Capacity numbers for go-live sizing | Infra worksheet | Arch, SDC, DBA | |

---

## 14. Data requirements

### 14.1 Core entities (logical)

- Application, Party (Bride/Bridegroom), Witness, MarriageEvent, Document, Payment, ScrutinyDecision, RegisterEntry (serial/page/volume), Certificate (Form II-A), Endorsement (Form II).

### 14.2 Retention

[Per government records policy — permanent preservation of registers per Rule 10(2) — align with DBA/archival policy.]

### 14.3 Migration (high level)

| Topic | Question for migration workstream |
|-------|-----------------------------------|
| Legacy Kaveri 2.0 marriage records | Volume, schema, cutover |
| Physical register back-scan | In scope? |

---

## 15. Requirements traceability matrix (RTM) — template

| Req ID | Act/Rule/Form | Requirement summary | Use case | UI screen | Test case ID | Status |
|--------|---------------|---------------------|----------|-----------|--------------|--------|
| FR-HMA-003 | Sec. 5(iii) | Age validation | UC-HMA-002 | Bride/groom | TC- | Draft |
| FR-HMA-070 | Form IA | Declarations | UC-HMA-001 | Declarations | TC- | Draft |
| FR-HMA-104 | Rule 4(5) | Form II-A issue | UC-HMA-005 | Certificate | TC- | Draft |

---

## 16. Open questions and decision log

### 16.1 Open questions

| Q ID | Question | Raised by | Needed from | Due |
|------|----------|-----------|-------------|-----|
| OQ-001 | Exact fee amounts post RD48 notification | BA | Treasury / DE | |
| OQ-002 | e-Sign validity for Form I/IA vs physical signature | BA | Legal / DE | |
| OQ-003 | Automated sapinda / prohibited relationship checks | BA | DE | |
| OQ-004 | Ordinary residence definition for jurisdiction | BA | DE | |

### 16.2 Decisions

| Dec ID | Decision | Date | Approver | Impact |
|--------|----------|------|----------|--------|
| DEC-001 | Phase 1 scope = Hindu registration only | | PO | |

---

## 17. Acceptance and sign-off

| Role | Name | Signature / Date | Comments |
|------|------|------------------|----------|
| Product Owner | | | |
| Domain Expert | | | |
| IGSR nominee | | | |
| Business Analyst | | | |

**UAT scope:** [Reference test scenarios derived from FR-HMA-* and statutory forms.]

---

## Appendix A — Form I field matrix (duplicate for bridegroom §3, bride §4, witnesses §5–7)

| # | Form I item | Data type | Mandatory | Source / evidence | Kannada label |
|---|-------------|-----------|-----------|-------------------|---------------|
| 1 | Date of marriage | Date | Y | | |
| 2 | Place of marriage | Text/address | Y | | |
| — | Joint photo | Image | Y | Upload | |
| 3a–h | Bridegroom particulars | Various | Y | | |
| 4a–h | Bride particulars | Various | Y | | |
| 5–7 | Three witnesses | Various | Y | | |

---

## Appendix B — Form IA declaration text (verify against latest gazette)

1. Valid marriage solemnized and capable of registration under **Section 8**, HMA 1955.  
2. Conditions in **Section 5** satisfied.  
3. Particulars true to best of knowledge and belief.

[System shall present verbatim approved text; capture husband and wife signatures with timestamp.]

---

## Appendix C — Form II / II-A data elements

**Form II (endorsement):** Date received; serial no.; page; volume; registrar signature; date.

**Form II-A (certificate):** Bride name & parentage; Bridegroom name & parentage; solemnization date; registration date; registrar station; date; seal.

---

## Appendix D — References

- The Hindu Marriage Act, 1955 — `Marriage/Hindu Marriage Act, 1955.pdf`
- Registration of Hindu Marriage (Karnataka) Rules, 1966 — `Marriage/REGISTRATIONOFHINDUMARRIAGE_KARNATAKARULES_1966.docx`
- Statutory forms — `Marriage/hindu marriage forms.pdf`, `Marriage/Form1.pdf`
- Marriage fee / process notification — `Marriage/RD48MNMU2023-Notification-marriage.pdf` (validate)
- Kaveri 3.0 Marriage prototype (UI reference only, not legal source) — `MarriageRegistrationProtoTypeDesign/templates/hindu-marriage-*.html`

---

*End of template — replace all `[TBD]` and bracketed placeholders through discovery, SRO interviews, and Domain Expert review.*
