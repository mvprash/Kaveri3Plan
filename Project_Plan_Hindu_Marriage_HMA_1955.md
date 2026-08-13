# Project Plan

## Marriage Registration Module — Hindu Marriage (Kaveri 3.0)

| Field | Value |
|--------|--------|
| **Document ID** | PLAN-K3-MRG-HMA-001 |
| **Version** | 0.1 (Draft) |
| **Status** | Draft for PO / Architecture review |
| **Module** | Marriage Registration — Hindu Marriage Act, 1955 |
| **Source BRD** | `BRD_Template_Marriage_Hindu_Marriage_Act_1955.md` (BRD-K3-MRG-HMA-001 v0.3) |
| **Source HLD** | `HLD_Implementation_Design_Hindu_Marriage_HMA_1955.md` (HLD-K3-MRG-HMA-001 v0.2) |
| **Process source** | `ProcessDiagrams/Hindu_Marriage_Online.png`, `ProcessDiagrams/Hindu_Marriage_Offline.png` |
| **Audience** | PO, PM, BA, Domain Expert, Solution Architect, Tech Leads, QA, DevOps, Security |
| **Last updated** | 2026-08-13 |

---

## Document control

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.1 | 2026-08-13 | Delivery | Initial project plan derived from BRD v0.3 To-Be and HLD v0.2 P0–P5 phasing |

**Related documents**

| ID | Title |
|----|--------|
| BRD-K3-MRG-HMA-001 | Business Requirements Document |
| HLD-K3-MRG-HMA-001 | High-Level Technical Design & Implementation Design |
| PROC-K3-MRG-HMA-TOBE-001 | Online / Offline process diagrams |
| RTM-K3-MRG-HMA-001 | Requirements traceability matrix (to be maintained) |
| DEC-K3-MRG-001 | Decision log |

---

## 1. Purpose and objectives

### 1.1 Purpose

Plan delivery of **Hindu marriage registration** under **Section 8, HMA 1955** and **Registration of Hindu Marriage (Karnataka) Rules, 1966** on Kaveri 3.0 — covering both **Online (eSign)** and **Offline (printout + DEO + two-stage SR verification)** channels per approved process diagrams.

### 1.2 Business objectives

| # | Objective | Measure |
|---|-----------|---------|
| O1 | Enable citizens to register already-solemnized Hindu marriages digitally | Online + Offline E2E live |
| O2 | Enforce statutory forms, fees, audit, and certificate issuance | Legal / DE sign-off on Form I / IA / II / II-A |
| O3 | Reduce rework and jurisdiction errors vs As-Is | Rejection / rework rate; cycle time by channel |
| O4 | Bilingual citizen and officer experience | EN + KN UI and certificate QA gate |
| O5 | Meet e-Gov NFR and compliance bar | GIGW, WCAG, STQC/security, DR drill |

### 1.3 MVP boundary (Phase 1)

**In MVP**

- Post-solemnization Hindu marriage registration only
- Both channels: Online and Offline
- Payment **after** first SR approval
- SR DSC before Form II-A
- DEO role (Offline), appointment + printout (Offline)

**Out of MVP** (unless PO promotes)

- Special Marriage Act and other personal-law Acts
- Divorce / nullity / matrimonial petitions
- Priest-led solemnization scheduling
- Full legacy ETL (migration workstream flagged separately)
- DigiLocker push (P4 optional if approved)

---

## 2. Delivery approach

### 2.1 Principles

1. **Process-first** — Online / Offline diagrams and BRD §7.6 status model are the workflow source of truth.
2. **Platform before feature** — shared Identity, Masters, Audit, Notification, Document store before channel MVPs (HLD P0).
3. **Online before Offline** — complete digital path first (P2), then counter path with DEO / Stage 2 (P3).
4. **Hard gates early** — pay-after-approve, eSign gate, Stage-2→DEO rework, DSC-before-certificate built into workflow from day one.
5. **Statutory lock** — form templates legally approved before UAT print/PDF gates.
6. **Decide open questions on the critical path** — OQ-002, OQ-005–008, OQ-012 block design/build.

### 2.2 Methodology

| Aspect | Approach |
|--------|----------|
| Cadence | 2-week sprints |
| Planning horizon | ~26–30 weeks to go-live gate (indicative; confirm with PO) |
| Environments | Dev → SIT → UAT → Pre-Prod → Prod (+ isolated DR) |
| Definition of Done | Code + unit/API tests + OpenAPI updated + audit event + bilingual check where UI/PDF |
| Traceability | FR-HMA / BR-HMA / US-HMA ↔ service ↔ test case in RTM |

### 2.3 Phase overview (from HLD §7.9)

| Phase | Name | Indicative duration | Exit criteria |
|-------|------|---------------------|---------------|
| **P0** | Platform spine | 4 weeks | Shared contracts published; Identity, Gateway, Masters, Audit, Notify, Doc store usable |
| **P1** | Common intake | 4 weeks | Both channels can save drafts through details capture |
| **P2** | Online MVP | 6 weeks | End-to-end Online UAT passed |
| **P3** | Offline MVP | 6 weeks | End-to-end Offline UAT passed |
| **P4** | MIS & compliance | 4 weeks | IGSR reports + Form III signed off |
| **P5** | Hardening & go-live | 4 weeks | Perf/load, STQC/security, DR drill; go-live gate |

**Indicative calendar (subject to PO confirmation):** start 2026-08-18 → go-live ready ~2027-03.

```text
W1────W4  W5────W8  W9────────W14  W15───────W20  W21───W24  W25───W28
│  P0   │  │  P1  │  │    P2     │  │    P3     │  │  P4  │  │  P5  │
 Platform   Intake      Online MVP     Offline MVP    MIS     Harden
```

---

## 3. Scope summary

### 3.1 In scope

| Area | Source |
|------|--------|
| Dual channel: Online (eSign) / Offline (physical + DEO) | BRD §7.1, DEC-002 |
| Forms I, IA, II, II-A, VI; Form III batch | BRD §3.3 |
| Jurisdiction: place of marriage **or** ordinary residence | Rule 4, FR-010/011 |
| Three witnesses; joint photo; bilingual EN/KN | BRD §2.1 |
| Pay after SR approve; Offline pay+appointment saga | FR-093/094, BR-012 |
| Two-stage Offline verification; targeted rework | FR-180–188, BR-016 |
| Microservices per HLD catalogue (intake, workflow, verification, payment, appointment, document/forms, register/cert, adapters) | HLD §5 |

### 3.2 Out of scope

Special Marriage / other Acts; Part III matrimonial court workflows; detailed migration ETL; Exact SDC BOM (capacity worksheet TBD).

### 3.3 Confirmed decisions (do not re-litigate)

| Dec | Decision |
|-----|----------|
| DEC-001 | Phase 1 = Hindu registration only |
| DEC-002 | Both Online and Offline in MVP |
| DEC-003 | Fee after first SR approval |
| DEC-004 | Offline two-stage verification with different reject targets |
| DEC-005 | DEO is a distinct role |

---

## 4. Workstreams

| Workstream | Lead | Responsibilities |
|------------|------|------------------|
| **Product / BA** | PO + BA | Backlog, OQ closure, UAT scenarios, RTM, content EN/KN |
| **Domain / Legal** | DE + Legal | Form wording, age/jurisdiction rules, OQ-002/006/010, template lock |
| **Architecture** | Solution Architect | HLD acceptance, AD-01..03, service contracts, NFR targets |
| **Platform** | Platform Tech Lead | Identity, Gateway, Masters, Audit, Notify, Object store, Event bus |
| **Marriage domain** | Module Tech Lead | Services 3–11 (intake → register/cert), BFFs, workflow defs |
| **UI/UX** | Frontend Lead | Citizen portal, SRO workbench, DEO console, Admin/MIS |
| **Integrations** | Integration Eng | Payment, eSign, DSC, SMS/Email, Aadhaar (if approved) |
| **QA** | QA Lead | SIT/UAT, channel E2E, statutory form PDF checks, accessibility |
| **Security** | Security Lead | RBAC matrix, STQC path, AV on upload, PII, DSC/eSign integrity |
| **DevOps / SDC** | DevOps | CI/CD, envs, HA/DR, observability, capacity |
| **Ops / Change** | Ops + PM | Runbooks, L1/L2/L3, SRO/DEO training, go-live checklist |

---

## 5. Phase detail

### 5.1 P0 — Platform spine (Weeks 1–4)

**Goal:** Reusable platform contracts so Marriage services can build against stable APIs.

| Work package | Deliverables | Primary services |
|--------------|--------------|------------------|
| P0-1 Identity & RBAC skeleton | Roles `CITIZEN`, `SR`, `DEO`, `IGSR_ADMIN`; office-scoped claims | identity-access |
| P0-2 API Gateway / WAF | Routes, mTLS to internals, idempotency header convention | Edge |
| P0-3 Master data | Districts, SRO offices, holidays, fee schedule stub, reason codes | master-data |
| P0-4 Document store | Object store + AV hook contract | document-form (store) |
| P0-5 Audit & notification | Append-only audit API; SMS/Email EN+KN template hooks | audit, notification |
| P0-6 Event bus + observability | Kafka (or equiv), OTel baseline | Platform |
| P0-7 Architecture gate | HLD §15 acceptance: boundaries, state machines, role matrix | Arch / PO |

**Exit criteria**

- [ ] Shared OpenAPI contracts published
- [ ] Non-prod Identity + Gateway working
- [ ] AD-01 (workflow engine), AD-02 (runtime), AD-03 (payment ownership) decided or time-boxed with interim choice
- [ ] NFR-OP-01/03/04 owners and due dates set

**Dependencies:** Platform HLD; SDC access; department IdP decision.

---

### 5.2 P1 — Common intake (Weeks 5–8)

**Goal:** Shared citizen path through prerequisite → channel → declarations → details (both channels).

| Work package | BRD / stories | Deliverables |
|--------------|---------------|--------------|
| P1-1 Prerequisite & channel | FR-140–145, US-07, UC-010 | Screens + audited ack; channel attribute |
| P1-2 Declarations & Form IA capture | FR-070–072, US-02, UC-011 | Statutory text (draft legal), both parties |
| P1-3 Marriage / parties / witnesses | FR-001–004, 020–022, 060–061, US-01 | Validations: age, marriage date ≤ today, exactly 3 witnesses |
| P1-4 Jurisdiction basis | FR-010–011, BR-006 | Place of marriage **or** ordinary residence; office routing stub |
| P1-5 Documents | FR-080–082 | Joint photo upload; checklist TBD with DE |
| P1-6 Workflow spine | FR-200, BR-010–011 | Status model Draft → Details captured; `HMA_ONLINE_v1` / `HMA_OFFLINE_v1` shells |
| P1-7 Citizen BFF + draft APIs | HLD §7.2 | Create/update application, tracker read-model start |

**Exit criteria**

- [ ] Citizen can create draft Online **and** Offline through details capture
- [ ] Channel fork audited; no cross-channel screen leakage
- [ ] Unit + API tests for age / witness / date rules
- [ ] OQ-005 (channel switch) and OQ-012 (Offline office timing) decided or deferred with interim rule

---

### 5.3 P2 — Online MVP (Weeks 9–14)

**Goal:** Full Online happy path and rejection loop: office+summary → Form 1A → eSign → SR verify → pay → DSC → Form II-A.

| Work package | BRD / stories | Deliverables |
|--------------|---------------|--------------|
| P2-1 Office + summary | FR-150–152, US-08, UC-012 | Edit-from-summary; Form 1A submit |
| P2-2 eSign integration | FR-153–156, US-09, UC-013, NFR-SEC-009 | Adapter; resumable retry; hard gate to SR |
| P2-3 SR queue (Online) | FR-100–102, 180, 183, 185–186, 188; US-04, 15, 16; UC-014 | Approve/Reject + written refusal PDF |
| P2-4 Pay after approve | FR-090–091, 093, 095–096; US-03; BR-012 | Payment enabled only at *Approved for payment*; Form VI |
| P2-5 DSC + register + II-A | FR-103–104, 190–194; US-05, 06, 14; UC-020 | Serial/page/volume; QR/seal; portal download |
| P2-6 Notifications (Online set) | FR-120–121, 202 | Submit, reject, pay due, certificate |
| P2-7 Online UAT | RTM Online rows | E2E UAT pack signed by PO / DE |

**Exit criteria**

- [ ] Online E2E UAT passed (happy + reject-to-data-entry + payment retry)
- [ ] OQ-002 eSign signatory set closed with Legal
- [ ] Payment cannot start before SR approve (automated test)
- [ ] Certificate blocked if DSC expired (automated test)

**Critical path risk:** eSign provider selection (NFR-OP-09).

---

### 5.4 P3 — Offline MVP (Weeks 15–20)

**Goal:** Full Offline path: Stage 1 → pay+appointment → print I/II/1A → DEO checklist/upload → Stage 2 → DSC → certificate.

| Work package | BRD / stories | Deliverables |
|--------------|---------------|--------------|
| P3-1 Offline Stage 1 | FR-181, 183; US-04; UC-015 | Pre-payment data verification |
| P3-2 Pay + appointment saga | FR-094, 160–161; US-10; HLD §7.6 | Atomic guided step; no double-book; compensate on PG fail |
| P3-3 Printouts | FR-162–164; US-11; UC-017; OQ-006 | Form I, II, 1A; duplicate memorandum; QR for DEO lookup |
| P3-4 DEO console | FR-165–170; US-12; UC-018; NFR-SEC-011/012 | Signature checklist; versioned upload; office-scoped RBAC |
| P3-5 Offline Stage 2 | FR-182, 184–188; US-13; UC-019 | Stage 2 reject → DEO only; citizen data locked |
| P3-6 DSC + cert (Offline delivery) | FR-193; UC-020 | Counter + download delivery mode |
| P3-7 Offline UAT | RTM Offline rows | E2E UAT incl. Stage 1 & Stage 2 rework |

**Exit criteria**

- [ ] Offline E2E UAT passed
- [ ] Stage 2 rejection never unlocks citizen data entry (automated test)
- [ ] Legal sign-off on print templates (COMP-007)
- [ ] OQ-007 (appointment rules) and OQ-008 (refund after Stage 2 fail) decided or interim policy documented

---

### 5.5 P4 — MIS & compliance (Weeks 21–24)

| Work package | BRD / stories | Deliverables |
|--------------|---------------|--------------|
| P4-1 Channel MIS | FR-130–136; US-18 | Volumes, cycle time, rejection by stage, appointment MIS |
| P4-2 Fee reconciliation | FR-132 | Recon report vs Treasury / PG |
| P4-3 Form III batch | FR-133 | Monthly duplicate bundle to Registrar-General |
| P4-4 DigiLocker (optional) | HLD §10 | Push Form II-A if approved |
| P4-5 GIGW / WCAG / Kannada PDF gate | COMP-001/002/006 | Checklist sign-off |
| P4-6 Post-registration (Should) | FR-110–111 | Certified extract / reprint controls if capacity allows |

**Exit criteria**

- [ ] IGSR / Admin MIS signed off
- [ ] Form III dry-run successful in UAT
- [ ] Accessibility and bilingual PDF gates green

---

### 5.6 P5 — Hardening & go-live (Weeks 25–28)

| Work package | Focus | Exit |
|--------------|-------|------|
| P5-1 Performance / load | Module share of ≥10k concurrent bar; eSign/pay/appointment/upload peaks | Perf gate pass |
| P5-2 Security / STQC | Scans, RBAC review, AV, secrets, UIDAI if eKYC | Security gate |
| P5-3 DR drill | Register DB + object store; RPO/RTO per NFR-OP-03 | Drill evidence |
| P5-4 Ops readiness | Runbooks (pay stuck, eSign abandon, double-book, Form III rerun, restore); L1/L2/L3 | Ops sign-off |
| P5-5 Training | SRO verification queues; DEO checklist; citizen channel guidance | Training complete |
| P5-6 Go-live | Pre-Prod soak; cutover checklist; hypercare plan | Go-live approval |

**Exit criteria**

- [ ] All Must FRs for MVP traced to passed tests in RTM
- [ ] PO + DE + Security + Ops go-live signatures
- [ ] Hypercare roster and rollback criteria published

---

## 6. Milestone schedule

| Milestone | Phase | Target (indicative) | Owner |
|-----------|-------|---------------------|-------|
| M0 — Kick-off & HLD acceptance | P0 | Week 1 | PO / Arch |
| M1 — Platform contracts ready | P0 | Week 4 | Platform TL |
| M2 — Intake draft complete | P1 | Week 8 | Module TL |
| M3 — Online UAT complete | P2 | Week 14 | QA / PO |
| M4 — Offline UAT complete | P3 | Week 20 | QA / PO |
| M5 — MIS / Form III signed off | P4 | Week 24 | IGSR / PO |
| M6 — Go-live gate | P5 | Week 28 | Steering |

---

## 7. Backlog mapping (MVP Must)

| Story | Channel | Target phase |
|-------|---------|--------------|
| US-HMA-01 Start registration | Both | P1 |
| US-HMA-02 Form I/IA data & declarations | Both | P1 |
| US-HMA-07 Prerequisite + channel choice | Both | P1 |
| US-HMA-08 Office + summary | Online | P2 |
| US-HMA-09 eSign | Online | P2 |
| US-HMA-03 Pay after SR approval | Both | P2 / P3 |
| US-HMA-04 Scrutinize approve/reject | Both | P2 / P3 |
| US-HMA-15 Rejection reason & fix | Both | P2 / P3 |
| US-HMA-16 Queues by stage | Both | P2 / P3 |
| US-HMA-05 Serial + Form II-A | Both | P2 / P3 |
| US-HMA-06 Download certificate | Both | P2 / P3 |
| US-HMA-14 SR DSC | Both | P2 / P3 |
| US-HMA-10 Pay + appointment | Offline | P3 |
| US-HMA-11 Print Form I/II/1A | Offline | P3 |
| US-HMA-12 DEO checklist + upload | Offline | P3 |
| US-HMA-13 Stage 2 verification | Offline | P3 |
| US-HMA-17 Tracker | Both | P2 (Should) |
| US-HMA-18 Channel MIS | Both | P4 (Should) |

---

## 8. Service build order

Aligned to HLD §5.1 catalogue:

| Order | Service | Phase start |
|-------|---------|-------------|
| 1 | identity-access, master-data, audit, notification, gateway, object store | P0 |
| 2 | application-intake-service, workflow-orchestrator | P1 |
| 3 | document-form-service (capture + Form 1A PDF) | P1–P2 |
| 4 | esign-adapter-service, verification-service, payment-fee-service | P2 |
| 5 | dsc-signing-adapter, register-certificate-service | P2 |
| 6 | appointment-service; document print + DEO upload path | P3 |
| 7 | mis-reporting-service; Form III job | P4 |
| 8 | integration-gateway hardening; DigiLocker optional | P4–P5 |

UI surfaces: Citizen Portal (P1→P3), SRO Workbench (P2→P3), DEO Console (P3), Admin/MIS (P4).

---

## 9. Team (indicative)

| Role | FTE (indicative) | Notes |
|------|------------------|-------|
| Product Owner | 0.5 | Decisions, UAT |
| BA / Content | 1 | RTM, EN/KN copy, OQs |
| Domain Expert / Legal | 0.25–0.5 | Workshops, form lock |
| Solution Architect | 0.5 | Cross-cutting + AD/OQ |
| Module backend engineers | 4–6 | Domain services |
| Platform engineers | 2–3 | Shared spine |
| Frontend engineers | 2–3 | Portal + workbench + DEO |
| Integration engineer | 1–2 | PG, eSign, DSC |
| QA | 2–3 | Channel E2E + PDF |
| Security | 0.5 | Gates |
| DevOps | 1–2 | Envs, DR, observability |
| PM / Scrum Master | 1 | Plan, risks, steering |

Exact staffing to be confirmed by delivery lead against programme capacity.

---

## 10. Dependencies and external integrations

| Dependency | Needed by | Owner | Risk if late |
|------------|-----------|-------|--------------|
| Platform HLD / runtime standard (AD-02) | P0 | Platform Arch | Service template churn |
| Workflow engine choice (AD-01) | P1 | Arch | Rework of state machine |
| Payment gateway / Treasury credentials | P2 | Integration / Treasury | Online UAT blocked |
| eSign provider + legal validity (OQ-002, NFR-OP-09) | P2 | Legal / Arch / PO | Online MVP blocked |
| DSC provisioning for UAT SROs (NFR-OP-10) | P2 | Security / Ops | Certificate path blocked |
| Fee schedule + RD48 amounts (OQ-001) | P2 | Treasury / DE | Wrong Form VI |
| Legal lock on Form I/II/1A/II-A templates | P2–P3 | Legal / DE | Print/PDF UAT blocked |
| SRO office calendar / holidays for slots | P3 | Master data / DE | Appointment saga blocked |
| Appointment / refund policy (OQ-007, OQ-008) | P3 | PO / Treasury | Offline UAT policy gaps |
| SDC HA/DR targets (NFR-OP-01/03) | P5 | Arch / SDC | Go-live gate fail |

---

## 11. Risks and open questions

### 11.1 Delivery risks

| ID | Risk | Impact | Mitigation | Owner |
|----|------|--------|------------|-------|
| R-01 | eSign provider delay or unclear signatory set | Online MVP slips | Parallel mock adapter; escalate OQ-002 Week 1–2 | PO / Legal |
| R-02 | Form II pre-endorsement print ambiguity (OQ-006) | Offline print redesign | DE workshop in P1; template variants | DE / Arch |
| R-03 | Pay-after-approve refunds after Stage 2 fail (OQ-008) | Payment saga incomplete | Interim: no auto-refund + manual process; design in P3 | Treasury / PO |
| R-04 | Kannada PDF / font rendering defects | Compliance fail | Early PDF spike in P1; COMP-006 gate | Content / QA |
| R-05 | Appointment double-booking under load | Citizen trust | Redis locks + PERF-009 tests in P3/P5 | Arch |
| R-06 | DEO role / staffing unclear (OQ-014) | Offline ops failure | Change management + training in P5 | PO / SRO |
| R-07 | Platform shared services not ready | P1–P2 idle | Module stubs behind interfaces; weekly platform sync | Platform TL |
| R-08 | Scope creep (SMA, divorce, DigiLocker) | Schedule slip | Strict MVP boundary; DigiLocker = P4 optional | PO |

### 11.2 Open questions — close before indicated phase

| Q ID | Question | Close by | Needed from |
|------|----------|----------|-------------|
| OQ-001 | Exact fee amounts (RD48) | P2 start | Treasury / DE |
| OQ-002 | Who must eSign | P2 start | Legal / DE |
| OQ-005 | Channel switch after selection | P1 mid | PO / DE |
| OQ-006 | Form II print before endorsement | P1 end | Legal / DE |
| OQ-007 | Appointment / no-show / refund rules | P3 start | PO / SRO |
| OQ-008 | Refund if Stage 2 fails after pay | P3 start | Treasury / PO |
| OQ-009 | Where physical signing happens | P3 start | DE / SRO |
| OQ-010 | Retention of physical originals | P3 mid | DE / Legal |
| OQ-011 | Citizen docs vs DEO-only uploads Offline | P1 mid | PO / DE |
| OQ-012 | Offline office selection timing | P1 mid | DE |
| OQ-013 | SLA per verification stage | P4 | PO / Ops |
| OQ-014 | Who is DEO / backup | P3 mid | SRO / PO |
| NFR-OP-01..12 | Availability, RPO/RTO, capacity, eSign SLA, etc. | Per HLD §13 | Arch / SDC / Security |

---

## 12. Governance and quality gates

### 12.1 Cadence

| Forum | Frequency | Purpose |
|-------|-----------|---------|
| Sprint planning / review / retro | Bi-weekly | Delivery |
| Domain / Legal workshop | Bi-weekly (P0–P3) | OQs, form lock |
| Architecture sync | Weekly | AD/NFR, integrations |
| Steering (PO, IGSR nominee, Arch, PM) | Monthly + at M0–M6 | Scope, risks, go-live |

### 12.2 Quality gates

| Gate | When | Criteria |
|------|------|----------|
| G0 Architecture | End P0 | HLD §15 acceptance |
| G1 Intake | End P1 | Draft both channels; RTM P1 rows green |
| G2 Online UAT | End P2 | Online E2E + hard-gate tests |
| G3 Offline UAT | End P3 | Offline E2E + Stage-2 routing test |
| G4 Compliance / MIS | End P4 | IGSR + Form III + GIGW/WCAG |
| G5 Go-live | End P5 | Perf, security, DR, ops, training |

### 12.3 Definition of Ready (user story)

- FR/BR linked; channel tagged; acceptance criteria Given/When/Then; OQ not blocking; design spike done if integration.

---

## 13. Test strategy (summary)

| Layer | Focus |
|-------|-------|
| Unit / API | Validations, workflow transitions, RBAC |
| Contract | BFF ↔ services; adapters ↔ providers (mocked) |
| SIT | Integration with PG / eSign / DSC sandboxes |
| UAT Online | UC-010–014, 020; reject loop; pay retry |
| UAT Offline | UC-015–020; DEO re-upload; Stage 2 reject |
| Statutory PDF | Form wording, Kannada glyphs, QR, duplicate memo |
| NFR | Load, appointment contention, upload AV, DR restore |
| Accessibility | WCAG keyboard / screen reader on citizen path |

Maintain **RTM-K3-MRG-HMA-001** with FR → UC → TC status from P1 onward.

---

## 14. Training and change management

| Audience | Timing | Content |
|----------|--------|---------|
| Citizens (help content) | P2–P3 | Channel choice, eSign vs visit, tracker |
| Sub-Registrars | P3–P5 | Queues Online / S1 / S2; refusal orders; DSC |
| Data Entry Operators | P3–P5 | Signature checklist; upload; Stage 2 rework |
| IGSR / Admin | P4–P5 | Channel MIS, Form III, fee recon |
| L1/L2 support | P5 | Runbooks for pay / eSign / appointment / upload |

---

## 15. Success criteria (go-live)

| # | Criterion | Evidence |
|---|-----------|----------|
| S1 | Online registration E2E in Prod smoke | Form II-A issued with DSC |
| S2 | Offline registration E2E in Prod smoke | DEO upload → Stage 2 → certificate |
| S3 | Payment only after first SR approval | Audit + automated regression |
| S4 | Statutory form templates Legal/DE approved | Sign-off record |
| S5 | Channel MIS available to IGSR | Report pack |
| S6 | Security / DR / Perf gates passed | Gate artefacts |
| S7 | SRO + DEO trained; hypercare live | Attendance + roster |

---

## 16. Immediate next actions (Week 0–2)

1. PO confirm indicative timeline and staffing against this plan.
2. Close or time-box **OQ-002, OQ-005, OQ-006, OQ-012** (intake/online blockers).
3. Architecture workshop: accept HLD; decide **AD-01, AD-02, AD-03**.
4. Stand up P0 backlog: Identity roles, masters, audit, gateway.
5. Schedule Legal form-template workshop (Forms I, IA, II, II-A).
6. Open RTM and decision log Confluence/SharePoint locations.
7. Engage Payment / eSign / DSC vendors for sandbox timelines.

---

## 17. Acceptance of this plan

| Role | Name | Signature / Date | Comments |
|------|------|------------------|----------|
| Product Owner | | | |
| Project / Delivery Manager | | | |
| Solution Architect | | | |
| Domain Expert | | | |
| IGSR nominee | | | |

---

## Appendix A — Traceability: BRD capability → phase → services

| BRD capability | Phase | Primary services |
|----------------|-------|------------------|
| Prerequisite + channel | P1 | Intake, Workflow, Audit |
| Data capture Form I/IA | P1 | Intake, Document-Form |
| Online eSign | P2 | eSign Adapter, Document-Form, Workflow |
| Online SR verify + pay + DSC + II-A | P2 | Verification, Payment, DSC, Register-Cert |
| Offline Stage 1 | P3 | Verification, Workflow |
| Pay + appointment | P3 | Payment, Appointment, Workflow |
| Print Form I/II/1A | P3 | Document-Form |
| DEO checklist/upload | P3 | Document-Form, Audit |
| Offline Stage 2 | P3 | Verification, Workflow |
| MIS / Form III | P4 | MIS-Reporting |
| NFR hardening | P5 | Gateway, Observability, DR |

## Appendix B — Reference inputs

- BRD-K3-MRG-HMA-001
- HLD-K3-MRG-HMA-001 (esp. §5 service catalogue, §6 workflows, §7.9 phases)
- Process diagrams — Online & Offline
- HMA 1955; Karnataka Rules 1966; statutory forms
- Architecture diagrams under `ArchitectureDiagrams/`

---

*End of Project Plan v0.1 — replace indicative dates/staffing after PO confirmation; track OQ/AD closures in the decision log.*
