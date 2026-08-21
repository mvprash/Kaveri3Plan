# Project Plan

## Kaveri 3.0 — Programme Delivery Plan (Phase-wise)

| Field | Value |
|--------|--------|
| **Document ID** | PLAN-K3-PROG-001 |
| **Version** | 0.2 (Draft) |
| **Status** | Draft for PO / Steering / Architecture review |
| **Programme** | Kaveri 3.0 — Registration Department, Government of Karnataka |
| **Requirements schedule** | `Requirement Discussions/Schedule/Kaveri_Requirements_Updated_Schedule_v3_DocumentSubModules.xlsx` |
| **Modules catalogue** | `Requirement Discussions/Modules/DocumentRegistration/Kaveri_2.0_Moduleslist.xlsx` |
| **IT Cell resources** | `K3_ITCellRequirement.pdf` (39 posts) |
| **Legal corpus (Document)** | `Acts_Rules/Document/` |
| **Programme constraint** | **All modules Go Live within 11 months** of programme start |
| **Audience** | Steering, PO, PM, BA, Domain Expert, Architects, Tech Leads, QA, DevOps, Security, Ops |
| **Last updated** | 2026-08-20 |

---

## Document control

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.1 | 2026-08-20 | Delivery | Programme plan: SDLC + 4 phases mapped to schedule v3 and Acts/Rules |
| 0.2 | 2026-08-20 | Delivery | Compressed to **11-month all-modules go-live**; staffing locked to `K3_ITCellRequirement.pdf` (39 posts); heavy parallel delivery |

**Related documents**

| ID / Path | Title |
|-----------|--------|
| `K3_ITCellRequirement.pdf` | IT Cell resource types, JD, qualifications (Total **39**) |
| Schedule v3 | Requirements discussion calendar (17-08-2026 → 15-10-2026) |
| PLAN-K3-MRG-HMA-001 | Marriage module project plan (Hindu Marriage) — align waves to Phase 1 |
| BRD-K3-MRG-HMA-001 | Marriage BRD |
| HLD-K3-MRG-HMA-001 | Marriage HLD |
| RTM-K3-* | Requirements traceability matrices (per module) |
| DEC-K3-PROG-001 | Programme decision log |

---

## 1. Purpose and objectives

### 1.1 Purpose

Define the end-to-end programme plan for Kaveri 3.0 covering:

1. Business Requirements (discussion + BRD)  
2. HLD  
3. SDD  
4. LLD  
5. Technical Architecture  
6. Software Development  
7. Software Testing  
8. Software Deployment  
9. Go Live  

Delivery is **phase-wise**. BR dates follow schedule v3. **All four delivery phases must achieve Go Live within an 11-month programme window**, executed by the **Kaveri IT Cell resource mix** in `K3_ITCellRequirement.pdf`.

### 1.2 Hard programme constraint

| Item | Value |
|------|--------|
| Programme start (T0) | **17-08-2026** (BR schedule start / requirements kick-off) |
| Programme end (all modules live) | **16-07-2027** (**T0 + 11 months**) |
| Implication | Phases **overlap**; design/build/test run in parallel; Phase 3 is the critical path |

### 1.3 Business objectives

| # | Objective | Measure |
|---|-----------|---------|
| O1 | All committed modules live within 11 months | Phase 4 (last) Go Live ≤ 16-07-2027 |
| O2 | Enforce Registration / Stamp Acts & Rules in software | Legal / Domain Expert sign-off on forms, fees, registers |
| O3 | Shared platform once (Identity, eKYC, eSign, Khajane, scanning, audit) | Reuse across phases |
| O4 | Fit delivery to IT Cell capacity (39 posts) | No phantom headcount; wave-based allocation |
| O5 | Meet e-Gov NFR bar | GIGW, WCAG, STQC/security, HA/DR |

### 1.4 Delivery phases

| Phase | In scope | Primary legal anchors |
|-------|----------|------------------------|
| **Phase 1** | Marriage (+ CC), User Management, eKYC, eSign, Khajane, Marriage dashboard & MIS, Scanning | HMA 1955 / Karnataka Rules 1966; SMA if promoted; Registration Act / Rules (CC, scanning) |
| **Phase 2** | Market Valuator (CVC + GIS), Stamp Duty & Guideline calculators, E-Stamp templates | Stamp Act 1957 + Schedule 2022; CVC Rules 2003; e-Stamping rules |
| **Phase 3** | Document Registration (sub-modules), EC, Document Dashboard & MIS, Verify/PoA, DRO/IGRO as agreed | Registration Act 1908 + Karnataka Amendments (incl. Act 47 of 2024); Rules 1965 |
| **Phase 4** | Firm Registration (DRO) | Firm/Societies framework as frozen in Firm BR; Societies (Amendment) Rules 2021 |

**Cross-cutting assigned early:** Refund, Audit, MDM → Phase 1 foundation; extended in later phases.

---

## 2. Inputs and planning basis

### 2.1 Requirements schedule (v3)

| Item | Value |
|------|--------|
| Start | 17-08-2026 |
| Finish | 15-10-2026 (60 calendar days) |
| Attendees | Committee, AIGR Comp, Kaveri IT Cell, KPMU |
| Exclusions | Sundays; 2nd & 4th Saturdays; GoK gazetted holidays |

### 2.2 BR discussion calendar (unchanged source of truth)

| Sr. | Module | Topic | Planned dates |
|-----|--------|-------|---------------|
| 1–7 | Marriage | Hindu / Special / BRE / Reporting / Integration / Dashboard | 17-08-2026 |
| 8 | Marriage | Audit | 18-08-2026 |
| 9 | Marriage | BRD | 19-08-2026 to 21-08-2026 |
| 10–11 | User Management | Discussion + BRD | 24-08-2026 to 25-08-2026 |
| 12 | Document | Registration, Appointment, Status | 25-08-2026 to 27-08-2026 |
| 13 | Document | Stamp duty / fee; Guideline value | 28-08-2026 to 29-08-2026 |
| 14 | Document | CVC Valuation; GIS | 31-08-2026 to 01-09-2026 |
| 15 | Document | Rule 17(2)/(3); Old pending release | 02-09-2026 to 03-09-2026 |
| 16 | Document | Filing, **Scanning**, Memo | 04-09-2026 to 05-09-2026 |
| 17 | Document | Re-Registration; Will after death | 07-09-2026 |
| 18 | Document | 68(2); Rule 123 | 08-09-2026 |
| 19 | Document | Integration, exemption, Court, Liability | 09-09-2026 to 10-09-2026 |
| 20 | Document | Investigation & Search; Verify | 11-09-2026 |
| 21 | Document | PoA Authentication | 15-09-2026 |
| 22 | Document | DRO undervaluation / will / adjudication | 16-09-2026 to 17-09-2026 |
| 23 | Document | IGRO Appeal | 18-09-2026 |
| 24 | Document | BRE, MIS #35–40, Dashboard | 19-09-2026 to 21-09-2026 |
| 25 | Digital E-Stamp | Templates | 22-09-2026 to 01-10-2026 |
| 26 | EC | Encumbrance Search | 03-10-2026 |
| 27 | CC | Certified Copies | 05-10-2026 |
| 28 | Doc/EC/CC/Verify/PoA | Consolidated BRD | 19-09-2026 to 05-10-2026 |
| 29–31 | Firm | Issues, BRE/MIS, BRD | 06-10-2026 to 14-10-2026 |
| 32–35 | Refund / Audit / MDM | Discussion + BRD | 12-10-2026 to 15-10-2026 |

### 2.3 Sub-module → phase map

| Delivery phase | Modules list # / topics |
|----------------|-------------------------|
| Phase 1 | #29–31 Marriage; #47 User Mgmt; #25 CC; #12 Scanning; eKYC/eSign/Khajane; Marriage MIS/Dashboard; #28/#33/#46 foundation (Refund/Audit/MDM) |
| Phase 2 | #4–5 Stamp duty & guideline; #21–22 CVC & GIS; #50 E-Stamping templates |
| Phase 3 | #1–3, #6–20, #23–24, #26–27, #35–40, #42–45 Document/EC/Verify/PoA/DRO/IGRO/MIS |
| Phase 4 | #41 Firm Registration |

Deferred outside 11-month committed go-live unless Steering promotes: #32 Legacy digitisation, #34 Accounts, #48 Mobile, #49 Training (training still executed as change stream).

---

## 3. IT Cell resources (`K3_ITCellRequirement.pdf`)

### 3.1 Approved roster — Total **39** posts

| Sl. | Resource type | Posts | Band | Primary contribution |
|-----|---------------|------:|------|----------------------|
| 1 | Product Owner | 1 | A | Roadmap, backlog, sprint goals, stakeholder alignment |
| 2 | Project Manager | 1 | A | Plan, risks, milestones, vendor/SLA, O&M reporting |
| 3 | Technical Architect | 1 | B | HLD, Tech Architecture, microservices, scale (≥10k concurrent) |
| 4 | Integration Engineer | 1 | B | Khajane, eKYC/Aadhaar, eSign, DigiLocker, API gateway/Kafka |
| 5 | Business Analyst | 2 | C | BRD/FRD, workshops, RTM, UAT support |
| 6 | Full Stack Developer | **8** | C | **5 Senior Lead** + **3 Developer** — APIs, UI, services |
| 7 | UI/UX Designer | 1 | C | Wireframes, GIGW/WCAG, EN+KN |
| 8 | Database Administrator | 1 | C | PostgreSQL HA, tuning, backup/recovery |
| 9 | Data Migration Specialist | 1 | B | Legacy ETL, EC index backfill, schema mapping |
| 10 | Test Engineers | 4 | C | Functional, regression, UAT packs |
| 11 | Performance & Security Test Lead | 1 | B | Load, vuln assessment, CERT-In/MeitY checklists |
| 12 | DevOps & Release Manager | 1 | A | CI/CD, K8s, envs, release trains |
| 13 | Security Specialist | 1 | A | GIGW/Aadhaar security, STQC path, hardening |
| 14 | L2 Support Engineers | 6 | C | Tickets, hypercare, field support (Kannada) |
| 15 | Content Manager | 1 | A | Manuals, SOPs, bilingual docs, training content |
| 16 | Domain Expert | 1 | B | Stamps & Registration SME (≥20 yrs dept service) |
| 17 | Technology Lead | 2 | A | Design/code review, tech standards, mentoring |
| 18 | Quality Assurance | 2 | A | QA framework (1 Senior + 1 QA), automation |
| 19 | BI and Analytics | 1 | B | Dashboards, MIS, ETL to analytics |
| 20 | AI/ML Specialist | 1 | B | Predictive/NLP/CV where approved (optional accelerators) |
| 21 | Transition Expert | 1 | B | Change, KT, post go-live sustainability |
| | **Total** | **39** | | |

### 3.2 Delivery capacity (build-critical roles)

| Capability | Headcount | Notes for 11-month plan |
|------------|----------:|---------------------------|
| Product / PM / Transition | 1+1+1 = 3 | Single PO/PM critical path; no parallel POs |
| Architecture / Tech Leads | 1+2 = 3 | One arch owns all phases; TLs split domain streams |
| BA + Domain + Content | 2+1+1 = 4 | BRD parallelisation limited to 2 BA streams |
| Full Stack | 8 | **Primary bottleneck** — wave allocation mandatory |
| Integration | 1 | Serialise adapter work: Khajane → eSign → eKYC → GIS/e-Stamp |
| UI/UX | 1 | Design system once; module screens incremental |
| DBA + Migration | 1+1 = 2 | Migration peaks Phase 3 (EC/registers) |
| QA + Test Eng + Perf/Sec Test | 2+4+1 = 7 | Shared test factory across overlapping phases |
| DevOps + Security | 1+1 = 2 | Shared envs/releases for all phases |
| L2 Support | 6 | Ramp per go-live; not full-time build |
| BI + AI/ML | 1+1 = 2 | Dashboards/MIS; AI only if PO prioritises |

### 3.3 Resource allocation by phase (indicative FTEs from the 39)

Allocation is **time-sliced**, not additive beyond 39.

| Role | Phase 1 peak | Phase 2 peak | Phase 3 peak | Phase 4 peak |
|------|-------------:|-------------:|-------------:|-------------:|
| Product Owner | 1.0 | 0.5 | 1.0 | 0.4 |
| Project Manager | 1.0 | 1.0 | 1.0 | 1.0 |
| Technical Architect | 1.0 | 0.6 | 1.0 | 0.3 |
| Technology Lead | 2.0 | 1.0 | 2.0 | 1.0 |
| BA | 2.0 | 1.0 | 2.0 | 1.0 |
| Domain Expert | 1.0 | 0.8 | 1.0 | 0.5 |
| Full Stack (of 8) | 6 | 4 | 8 | 3 |
| Integration | 1.0 | 0.8 | 1.0 | 0.3 |
| UI/UX | 1.0 | 0.4 | 1.0 | 0.3 |
| DBA | 1.0 | 0.5 | 1.0 | 0.3 |
| Data Migration | 0.3 | 0.3 | 1.0 | 0.2 |
| Test Eng + QA + Perf/Sec | 5 | 3 | 7 | 3 |
| DevOps | 1.0 | 0.6 | 1.0 | 0.5 |
| Security | 1.0 | 0.5 | 1.0 | 0.3 |
| BI Analytics | 0.6 | 0.3 | 1.0 | 0.4 |
| AI/ML | 0.2 | 0.2 | 0.5 | 0.2 |
| Content Manager | 0.8 | 0.4 | 1.0 | 0.5 |
| Transition Expert | 0.3 | 0.3 | 0.8 | 1.0 |
| L2 Support | 2→6 | 3 | 6 | 4 |

**Rule:** When Phase 1 and Phase 3 overlap, Full Stack prioritises **Phase 3 critical path** after Phase 1 UAT freeze; Phase 2 calculators stay on a **dedicated squad of 3–4** developers.

---

## 4. Scope by delivery phase

### 4.1 Phase 1 — Marriage platform & citizen services

Marriage (Online eSign + Offline DEO), Certified Copies, User Management, eKYC, eSign, Khajane payment, Scanning spine, Marriage Dashboard & MIS, Refund/Audit/MDM foundation.

### 4.2 Phase 2 — Valuation & stamp duty microservices

Stamp Duty Calculator, Guideline Value Calculator, Market Valuator (CVC), GIS Valuation, E-Stamp template catalogue.

### 4.3 Phase 3 — Document Registration & Encumbrance

Core registration, appointment, status; filings (Rule 17, FRUITS, memo); corrections/re-regn/will; integration/court/liability; Verify & PoA; EC; DRO undervaluation/will/adjudication; IGRO appeal; Document dashboards & MIS #35–40 (agreed subset).

### 4.4 Phase 4 — Firm Registration

Firm Registration (DRO #41), Firm MIS/Dashboard/Audit; reuse Phase 1 platform.

---

## 5. Legal framework (summary)

| Corpus (`Acts_Rules/Document/`) | Phases |
|---------------------------------|--------|
| Registration Act 1908; Karnataka Registration Rules 1965 | 1 (CC/scan), 3 |
| Karnataka Registration Amendments incl. Act 47 of 2024 | 3 |
| Karnataka Stamp Act 1957; Schedule 2022; Stamp Rules 1958 | 2, 3 |
| E-Stamping payment; Franking Rules 2000; CVC Rules 2003 | 2, 3 |
| Societies Registration (Amendment) Rules 2021 | 4 |
| Marriage Acts/Rules under `Acts_Rules/Marriage/` | 1 |

No production statutory artefact without Domain Expert / Legal template lock.

---

## 6. Delivery approach (11-month mode)

### 6.1 Principles

1. **11-month hard end** — Phase 4 Go Live ≤ 16-07-2027.  
2. **BR schedule intact** — 17-08-2026 → 15-10-2026.  
3. **Maximum safe overlap** — Design Phase N+1 while building Phase N.  
4. **Platform first, thin verticals** — Identity/eKYC/eSign/Khajane/Scan in Phase 1 weeks 1–6.  
5. **Squad model on 8 developers** — Platform/Marriage | Calculators | Document/EC | Firm (late).  
6. **Pilot where needed** — Phase 3 may pilot 1–2 SROs then statewide **inside** the 11-month window.  
7. **Scope discipline** — Mobile, Accounts, full legacy digitisation stay out unless Steering swaps scope.

### 6.2 Methodology

| Aspect | Approach |
|--------|----------|
| Cadence | 2-week sprints (≈22 sprints in 11 months) |
| Environments | Dev → SIT → UAT → Pre-Prod → Prod (+ DR) |
| DoD | Code + tests + contract update + audit event + EN/KN where UI/PDF |
| Traceability | BR/FR/US ↔ service ↔ TC in RTM |

### 6.3 SDLC stages (every phase)

BRD → HLD → Technical Architecture → SDD → LLD → Development → Testing → Deployment → Go Live  
(with compressed, overlapping windows per §7).

---

## 7. Programme timeline — 11 months

### 7.1 Master calendar

```text
2026                                              2027
Aug        Oct         Dec         Feb         Apr         Jun         Jul
│◄─ BR ─►│
│◄──────── Phase 1 Design+Build+Test ────────►│ P1 GL
│    │◄────── Phase 2 Design+Build+Test ──────────────►│ P2 GL
│         │◄──────────── Phase 3 (critical path) ──────────────────►│ P3 GL
│              Firm BR │              │◄── Phase 4 Build+Test ──►│ P4 GL
T0=17-Aug-2026                                                      T+11=16-Jul-2027
```

| Delivery phase | BR complete | Design (HLD→LLD) | Development | Testing | Deploy | **Go Live** |
|----------------|-------------|------------------|-------------|---------|--------|-------------|
| **Phase 1** | Marriage 21-08; User Mgmt 25-08; Scan 05-09; CC 05-10; Refund/Audit/MDM 15-10 | 24-08-2026 → 17-10-2026 | 08-09-2026 → 19-12-2026 | 24-11-2026 → 16-01-2027 | 19-01-2027 → 30-01-2027 | **02-02-2027** |
| **Phase 2** | Stamp/CVC/GIS 01-09; E-Stamp 01-10; in Doc BRD 05-10 | 22-09-2026 → 21-11-2026 | 27-10-2026 → 27-02-2027 | 01-02-2027 → 27-03-2027 | 30-03-2027 → 10-04-2027 | **13-04-2027** |
| **Phase 3** | Doc/EC BRD 05-10-2026 | 06-10-2026 → 19-12-2026 | 01-12-2026 → 08-05-2027 | 15-03-2027 → 12-06-2027 | 15-06-2027 → 26-06-2027 | **30-06-2027** |
| **Phase 4** | Firm BRD 14-10-2026 | 02-03-2027 → 17-04-2027 | 06-04-2027 → 20-06-2027 | 25-05-2027 → 04-07-2027 | 07-07-2027 → 11-07-2027 | **14-07-2027** |

**All modules Go Live complete: 14-07-2027** (within 11 months; buffer to 16-07-2027).

### 7.2 Month-by-month view (T0 = Aug 2026)

| Month | Calendar | Focus |
|------:|----------|--------|
| M1 | Aug 2026 | BR Marriage/User Mgmt; Phase 1 HLD start; platform AD |
| M2 | Sep 2026 | Document BR; Phase 1 build (platform + intake); Phase 2 design start |
| M3 | Oct 2026 | BR window close 15-10; Phase 1 Online path; Phase 2/3 design; migration plan |
| M4 | Nov 2026 | Phase 1 Offline/Scan/CC; Phase 2 calculator build; Phase 3 SDD/LLD |
| M5 | Dec 2026 | Phase 1 feature freeze; Phase 3 core regn build starts; Phase 2 continues |
| M6 | Jan 2027 | **Phase 1 UAT → Deploy → Go Live (02-02)**; Phase 2/3 build |
| M7 | Feb 2027 | Phase 1 hypercare; Phase 2 UAT prep; Phase 3 filings/EC |
| M8 | Mar 2027 | Phase 2 UAT; Phase 3 EC + DRO paths; Phase 4 design start |
| M9 | Apr 2027 | **Phase 2 Go Live (13-04)**; Phase 3 harden; Phase 4 build |
| M10 | May 2027 | Phase 3 UAT intensive; Phase 4 build |
| M11 | Jun 2027 | **Phase 3 Go Live (30-06)**; Phase 4 UAT |
| M11+ | Jul 2027 | Phase 4 Deploy → **Go Live (14-07)**; programme close |

### 7.3 Phase 1 — SDLC detail (compressed)

| Stage | Start | End | Owners (IT Cell) |
|-------|-------|-----|------------------|
| Business Requirements | 17-08-2026 | 15-10-2026 | BA (2), Domain Expert, PO |
| HLD + Technical Architecture | 24-08-2026 | 03-10-2026 | Technical Architect, Tech Leads |
| SDD | 08-09-2026 | 17-10-2026 | Tech Leads, Full Stack Seniors |
| LLD | 22-09-2026 | 31-10-2026 | Tech Leads, Full Stack |
| Software Development | 08-09-2026 | 19-12-2026 | Full Stack (6), Integration, DBA, UI/UX |
| Software Testing | 24-11-2026 | 16-01-2027 | QA (2), Test Eng (4), Perf/Sec Lead |
| Software Deployment | 19-01-2027 | 30-01-2027 | DevOps, Security, DBA |
| Go Live + hypercare | 02-02-2027 | +3 weeks | Transition, L2 (ramp to 6), PM |

**Phase 1 waves (≈17 weeks build)**

| Wave | Window | Focus | Dev squad |
|------|--------|-------|-----------|
| W0 | 08-09 → 03-10 | User Mgmt, masters, audit, gateway, scan contract, Khajane/eSign/eKYC stubs | 4 FS + Integration |
| W1 | 06-10 → 31-10 | Marriage intake both channels | 4 FS |
| W2 | 03-11 → 28-11 | Online: eSign, SR, pay-after-approve, DSC, cert | 5 FS + Integration |
| W3 | 01-12 → 19-12 | Offline, DEO, scanning, CC, Marriage MIS/Dashboard | 6 FS + BI |

### 7.4 Phase 2 — SDLC detail

| Stage | Start | End |
|-------|-------|-----|
| Business Requirements | 28-08-2026 | 05-10-2026 |
| HLD / Tech Arch / SDD / LLD | 22-09-2026 | 21-11-2026 |
| Software Development | 27-10-2026 | 27-02-2027 |
| Software Testing | 01-02-2027 | 27-03-2027 |
| Deploy | 30-03-2027 | 10-04-2027 |
| Go Live | **13-04-2027** | Hypercare 2 weeks |

Squad: **3–4 Full Stack** dedicated + Domain Expert (duty rules) + Integration (e-Stamp/GIS).

### 7.5 Phase 3 — SDLC detail (critical path)

| Stage | Start | End |
|-------|-------|-----|
| Business Requirements | 25-08-2026 | 05-10-2026 |
| HLD / Tech Arch | 06-10-2026 | 28-11-2026 |
| SDD / LLD | 10-11-2026 | 19-12-2026 |
| Software Development | 01-12-2026 | 08-05-2027 |
| Software Testing | 15-03-2027 | 12-06-2027 |
| Deploy (pilot → state) | 15-06-2027 | 26-06-2027 |
| Go Live | **30-06-2027** | Hypercare 4 weeks (overlaps Phase 4) |

**Phase 3 sub-waves**

| Sub-wave | Window | Scope |
|----------|--------|-------|
| D1 | Dec–Jan | Registration + appointment + status + duty bind (Phase 2 APIs) |
| D2 | Feb–Mar | Filings, memo, scanning ops, corrections |
| D3 | Mar–Apr | EC + migration cutover rehearsal |
| D4 | Apr–May | Verify, PoA, DRO/IGRO, Document MIS/Dashboard |

Migration Specialist + DBA peak on D3.

### 7.6 Phase 4 — SDLC detail

| Stage | Start | End |
|-------|-------|-----|
| Business Requirements | 06-10-2026 | 14-10-2026 |
| Design (HLD→LLD) | 02-03-2027 | 17-04-2027 |
| Software Development | 06-04-2027 | 20-06-2027 |
| Software Testing | 25-05-2027 | 04-07-2027 |
| Deploy | 07-07-2027 | 11-07-2027 |
| Go Live | **14-07-2027** | Hypercare 2 weeks |

Uses platform from Phase 1; **3 Full Stack** after Phase 3 feature freeze.

---

## 8. Service / component build order

### 8.1 Phase 1

1. identity-access / User Management  
2. master-data, audit, notification, gateway, object-store  
3. ekyc-adapter → esign-adapter → khajane-adapter (Integration Engineer serial)  
4. scanning-ingest-service  
5. marriage-* services  
6. certified-copy-service  
7. marriage dashboard + MIS (BI)

### 8.2 Phase 2

1. stamp-duty-calculator-service  
2. guideline-value-service  
3. market-valuator-cvc-service  
4. gis-valuation-service  
5. e-stamp-template-service  

### 8.3 Phase 3

1. document-registration + appointment + status  
2. bind Phase 2 calculators  
3. filings / memo / scan ops  
4. corrections / re-regn / will  
5. integration / court / liability  
6. verify + poa  
7. encumbrance-search (+ migration)  
8. DRO / IGRO  
9. Document MIS / dashboards  

### 8.4 Phase 4

1. firm-registration-service  
2. firm MIS / dashboard / audit views  

---

## 9. Testing strategy (shared test factory)

| Layer | Owners | Notes under 11-month plan |
|-------|--------|---------------------------|
| Unit / API | Full Stack + QA | Required in DoD every sprint |
| Contract | Tech Leads + Integration | Protect phase overlap |
| SIT | Integration + Test Eng | Adapter sandboxes early (M2–M3) |
| UAT | BA + Domain + Test Eng | Per-phase exit; no slip beyond buffer |
| Statutory PDF | Domain + Content + QA | Forms lock before UAT |
| Perf / Security | Perf&Sec Test Lead + Security | Gate before each Go Live |
| Regression | QA automation | Full suite before Phase 3/4 GL |

RTM mandatory from design freeze of each phase.

---

## 10. Deployment and go-live

### 10.1 Release strategy

| Phase | Strategy | Hypercare |
|-------|----------|-----------|
| 1 | Statewide platform + Marriage + CC | 3 weeks; L2 → 6 |
| 2 | Calculators behind flags; 1–2 week shadow optional | 2 weeks |
| 3 | Pilot SRO(s) in deploy window then statewide **by 30-06-2027** | 4 weeks |
| 4 | DRO enablement | 2 weeks |

### 10.2 Go-live gate (each phase)

- [ ] Must-scope RTM green  
- [ ] Domain Expert form/fee lock  
- [ ] Security + perf + DR evidence  
- [ ] Runbooks + L2 roster  
- [ ] Training (Content + Transition)  
- [ ] Rollback criteria  
- [ ] PO + PM + Architect + Domain + Steering sign-off  

### 10.3 Programme success (11-month)

| # | Criterion | Target date |
|---|-----------|-------------|
| S1 | Phase 1 live (Marriage, CC, User Mgmt, eKYC, eSign, Khajane, Scan, Marriage MIS/Dash) | 02-02-2027 |
| S2 | Phase 2 live (Valuator + Stamp/Guideline calculators) | 13-04-2027 |
| S3 | Phase 3 live (Document Registration + EC + Document MIS/Dash) | 30-06-2027 |
| S4 | Phase 4 live (Firm Registration) | 14-07-2027 |
| S5 | **All modules Go Live complete** | **≤ 16-07-2027** |

---

## 11. Milestones

| ID | Milestone | Target | Owner |
|----|-----------|--------|-------|
| M-T0 | Programme start | 17-08-2026 | PO / PM |
| M-BR | BR window complete | 15-10-2026 | BA / PO |
| M-P1-DES | Phase 1 design freeze | 17-10-2026 | Architect |
| M-P1-GL | Phase 1 Go Live | 02-02-2027 | Steering |
| M-P2-GL | Phase 2 Go Live | 13-04-2027 | Steering |
| M-P3-GL | Phase 3 Go Live | 30-06-2027 | Steering |
| M-P4-GL | Phase 4 Go Live — **programme complete** | 14-07-2027 | Steering |
| M-END | 11-month window end | 16-07-2027 | PM |

---

## 12. Dependencies

| Dependency | Needed by | Risk if late |
|------------|-----------|--------------|
| IT Cell onboarding of 39 posts | M1–M2 | 11-month plan fails |
| BR schedule adherence | All designs | Compresses build further |
| Khajane / eSign / eKYC sandboxes | Phase 1 SIT (Nov 2026) | Phase 1 GL slip → cascade |
| Stamp Schedule 2022 digitised | Phase 2 build | Calculator UAT fail |
| CVC / GIS feeds | Phase 2 | De-scope GIS or slip |
| EC historical index migration | Phase 3 D3 | EC not statewide by 30-06 |
| Act 47 SOPs | Phase 3 SDD | Refusal/cancel gaps |
| Firm Act set freeze (Sr.29–31) | Phase 4 design | Rework in M9–M11 |

---

## 13. Risks (11-month specific)

| ID | Risk | Impact | Mitigation | Owner |
|----|------|--------|------------|-------|
| R-01 | Only 8 Full Stack for 4 phases | Schedule | Squad waves; freeze scope; no parallel greenfield | PO / Tech Leads |
| R-02 | Single Integration Engineer serialises adapters | Phase 1/2 slip | Stub-first; vendor war-rooms; priority Khajane→eSign→eKYC | Integration / PM |
| R-03 | BR slip past 15-10-2026 | Loses design float | Protect Sr.9–11; BA pair split Marriage vs Document | PM / BA |
| R-04 | Phase 3 too large for Jun GL | Misses 11-month end | Must/Should split inside Phase 3; geographic pilot inside Jun window | PO / Architect |
| R-05 | Resource late joining | Lost M1–M2 | Stagger onboarding; contractors only if Steering approves within 39 model | PM |
| R-06 | Overlap regression | Defect leakage | Contract tests + automated regression owned by QA | QA |
| R-07 | EC migration quality | Phase 3 GL incomplete | Migration spike in Oct–Nov; rehearsal in Apr | Migration / DBA |
| R-08 | Scope creep (mobile/legacy/accounts) | Breaks 11-month | Change board; swap-in only with equal swap-out | Steering |
| R-09 | L2 overloaded across hypercares | Ops failure | Transition Expert playbooks; freeze non-critical changes in Jul | Transition / PM |

---

## 14. Governance

| Forum | Frequency | Purpose |
|-------|-----------|---------|
| Daily stand-up (squads) | Daily | Delivery |
| Sprint review/retro | Bi-weekly | Inspect/adapt |
| Architecture sync | Weekly | AD/NFR |
| Integration war-room | Weekly (M2–M6) | Adapters |
| Steering | Fortnightly in 11-month window | Scope, risk, go-live calls |
| BR workshops | Per schedule v3 | Domain lock |

### Quality gates

| Gate | When |
|------|------|
| G-BR | Per module BRD sign-off |
| G-DES | Design freeze per phase |
| G-SIT | Adapters green |
| G-UAT | E2E signed |
| G-NFR | Perf/security/DR |
| G-GL | Steering checklist |

---

## 15. Training and change

| Audience | Timing | Owner |
|----------|--------|-------|
| SRO / DEO | Before each phase GL | Content + Transition + Domain |
| DRO / IGRO | Phase 3–4 | Domain + Content |
| Citizens (help/KB) | Phase 1 onward | Content + UI/UX |
| L2 | From Phase 1 Pre-Prod | Transition + L2 leads |

---

## 16. Immediate next actions

1. Steering approve **v0.2 constraint**: all modules Go Live by **14-07-2027** (≤ 16-07-2027).  
2. Complete onboarding against `K3_ITCellRequirement.pdf` (39 posts) — critical path for M1–M2.  
3. Finish Marriage BRD (Sr.9) and User Management (Sr.10–11) on schedule.  
4. Architect freeze Phase 1 platform ADs by **03-10-2026**.  
5. Form three squads: Platform/Marriage | Calculators | Document/EC (Firm joins M9).  
6. Book Khajane/eSign/eKYC sandboxes for November SIT.  
7. Start Stamp Schedule 2022 + EC migration assessment immediately after Sr.13–14 / Sr.26.  

---

## 17. Acceptance

| Role | Name | Signature / Date | Comments |
|------|------|------------------|----------|
| Product Owner | | | |
| Project Manager | | | |
| Technical Architect | | | |
| Domain Expert | | | |
| AIGR / IGSR nominee | | | |
| KPMU nominee | | | |

---

## Appendix A — IT Cell headcount checksum

| Category | Posts |
|----------|------:|
| Leadership (PO, PM, Transition, Content, Security, DevOps) | 1+1+1+1+1+1 = 6 |
| Architecture / Tech Lead | 1+2 = 3 |
| BA / Domain | 2+1 = 3 |
| Engineering (FS, Integration, UI/UX, DBA, Migration) | 8+1+1+1+1 = 12 |
| Quality (QA, Test Eng, Perf/Sec) | 2+4+1 = 7 |
| Analytics (BI, AI/ML) | 1+1 = 2 |
| L2 Support | 6 |
| **Total** | **39** |

Source: `K3_ITCellRequirement.pdf`.

## Appendix B — BR Sr. → phase → GL

| BR topics | Phase | Go Live |
|-----------|-------|---------|
| Marriage, User Mgmt, Scanning, CC, Refund/Audit/MDM, eKYC/eSign/Khajane | 1 | 02-02-2027 |
| Stamp/Guideline, CVC/GIS, E-Stamp templates | 2 | 13-04-2027 |
| Document Registration, EC, Document MIS/Dash, Verify/PoA, DRO/IGRO | 3 | 30-06-2027 |
| Firm Registration | 4 | 14-07-2027 |

## Appendix C — Changes from v0.1

| Item | v0.1 | v0.2 |
|------|------|------|
| Phase 1 GL | 23-03-2027 | **02-02-2027** |
| Phase 2 GL | 12-07-2027 | **13-04-2027** |
| Phase 3 GL | 24-01-2028 | **30-06-2027** |
| Phase 4 GL | 11-09-2028 | **14-07-2027** |
| Programme end | ~Sep 2028 | **≤ 16-07-2027 (11 months)** |
| Staffing | Indicative FTE bands | **Locked to IT Cell 39 posts** |
| Execution | Mostly sequential phases | **Heavy parallel squads** |

---

*End of Programme Project Plan v0.2 — 11-month all-modules go-live; resources per `K3_ITCellRequirement.pdf`.*
