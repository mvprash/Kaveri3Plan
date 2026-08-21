# Project Plan

## Kaveri 3.0 — Programme Delivery Plan (Phase-wise)

| Field | Value |
|--------|--------|
| **Document ID** | PLAN-K3-PROG-001 |
| **Version** | 0.1 (Draft) |
| **Status** | Draft for PO / Steering / Architecture review |
| **Programme** | Kaveri 3.0 — Registration Department, Government of Karnataka |
| **Requirements schedule** | `Requirement Discussions/Schedule/Kaveri_Requirements_Updated_Schedule_v3_DocumentSubModules.xlsx` |
| **Modules catalogue** | `Requirement Discussions/Modules/DocumentRegistration/Kaveri_2.0_Moduleslist.xlsx` |
| **Legal corpus (Document)** | `Acts_Rules/Document/` |
| **Audience** | Steering, PO, PM, BA, Domain Experts, Solution Architects, Tech Leads, QA, DevOps, Security, Ops |
| **Last updated** | 2026-08-20 |

---

## Document control

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.1 | 2026-08-20 | Delivery | Programme plan: SDLC stages + 4 delivery phases mapped to schedule v3 and Acts/Rules |

**Related documents**

| ID / Path | Title |
|-----------|--------|
| Schedule v3 | Requirements discussion calendar (17-08-2026 → 15-10-2026) |
| PLAN-K3-MRG-HMA-001 | Marriage module project plan (Hindu Marriage) |
| BRD-K3-MRG-HMA-001 | Marriage BRD (in progress per schedule Sr.9) |
| HLD-K3-MRG-HMA-001 | Marriage HLD |
| RTM-K3-* | Requirements traceability matrices (per module, to be maintained) |
| DEC-K3-PROG-001 | Programme decision log (to be opened) |

---

## 1. Purpose and objectives

### 1.1 Purpose

Define the **end-to-end programme plan** for Kaveri 3.0 covering:

1. **Business Requirements** (discussion + BRD)
2. **HLD** (High-Level Design)
3. **SDD** (System / Solution Design)
4. **LLD** (Low-Level Design)
5. **Technical Architecture**
6. **Software Development**
7. **Software Testing**
8. **Software Deployment**
9. **Go Live**

Delivery is **phase-wise**. Business Requirements dates for all modules are taken from schedule v3; subsequent SDLC stages are planned from those BR completion anchors.

### 1.2 Business objectives

| # | Objective | Measure |
|---|-----------|---------|
| O1 | Digitise core citizen and officer journeys on a shared platform | Phase go-lives on schedule with E2E UAT pass |
| O2 | Enforce Registration Act / Stamp Act / Rules compliance in software | Legal / DE sign-off on forms, fees, refusal, registers |
| O3 | Deliver shared platform capabilities once (identity, eKYC, eSign, Khajane, scanning, audit) | Reuse across phases; no duplicate payment/eSign stacks |
| O4 | Reduce As-Is pain (rework, jurisdiction errors, fee disputes, EC delays) | Cycle time, rejection rate, fee recon accuracy |
| O5 | Meet e-Gov NFR bar | GIGW, WCAG, STQC/security, HA/DR |

### 1.3 Delivery phases (programme boundary)

| Delivery phase | In scope (committed) | Primary legal anchors |
|----------------|----------------------|------------------------|
| **Phase 1** | Marriage registration (+ certificate copy), User Management, eKYC, eSign, Khajane payment, Marriage dashboard & MIS, Scanning | HMA 1955 / Karnataka Hindu Marriage Rules 1966; SMA 1954 (if promoted); Registration Act s.57 / CC practice; Registration Rules 1965 (scanning / copies) |
| **Phase 2** | Market Valuator (CVC + guideline / GIS valuation microservices), Stamp Duty Calculators | Karnataka Stamp Act 1957 + Schedule; Stamp Rules 1958; CVC Market Value Guidelines Rules 2003; e-Stamping payment rules |
| **Phase 3** | Document Registration (core + filings + corrections + DRO/IGRO processes as agreed), Encumbrance Search (EC), Document-related Dashboard & MIS | Registration Act 1908 + Karnataka Amendments (incl. Act 47 of 2024); Karnataka Registration Rules 1965; Stamp Act for duty at registration |
| **Phase 4** | Firm Registration (DRO) | Karnataka Societies / Firm registration framework as confirmed in Firm BR workshops; Societies Registration (Amendment) Rules 2021 (fee table updates) |

**Cross-cutting (scheduled in BR window; assigned to earliest consuming phase):** Refund, Audit, Master Data Management, Digital E-Stamp (template design), Verify Document, PoA Authentication — see §3.3.

---

## 2. Inputs and planning basis

### 2.1 Requirements schedule (v3) — planning window

| Item | Value |
|------|--------|
| Start | 17-08-2026 |
| Scheduled finish | 15-10-2026 (60 calendar days) |
| Attendees | Committee, AIGR Comp, Kaveri IT Cell, KPMU |
| Mode | Online / Offline |
| Non-working exclusions | Sundays; 2nd & 4th Saturdays; GoK gazetted holidays |

### 2.2 BR discussion calendar (source of truth)

| Sr. | Module | Topic | Owner | Planned dates | Status (as of schedule) |
|-----|--------|-------|-------|---------------|-------------------------|
| 1–7 | Marriage | Hindu / Special / BRE / Reporting / Integration / Dashboard | DSR | 17-08-2026 | Completed |
| 8 | Marriage | Audit requirements | DSR | 18-08-2026 | Completed |
| 9 | Marriage | BRD | BA | 19-08-2026 to 21-08-2026 | In Progress |
| 10 | User Management | Login, transfer, relieving | DSR, BA | 24-08-2026 | Planned |
| 11 | User Management | BRD | BA | 25-08-2026 | Planned |
| 12 | Document | Registration, Appointment, Status tracking | DSR | 25-08-2026 to 27-08-2026 | Planned |
| 13 | Document | Stamp duty / Regn fee; Guideline value | DSR | 28-08-2026 to 29-08-2026 | Planned |
| 14 | Document | Valuation (CVC) and GIS valuation | DSR | 31-08-2026 to 01-09-2026 | Planned |
| 15 | Document | Rule 17(2), 17(3), Old pending release | DSR | 02-09-2026 to 03-09-2026 | Planned |
| 16 | Document | Filing (FRUITS), Scanning, Memo transmission | DSR | 04-09-2026 to 05-09-2026 | Planned |
| 17 | Document | Re-Registration; Will after death of testator | DSR | 07-09-2026 | Planned |
| 18 | Document | 68(2) correction; Cross-reference Rule 123 | DSR | 08-09-2026 | Planned |
| 19 | Document | Integration, exemption, Court entry, Liability | DSR | 09-09-2026 to 10-09-2026 | Planned |
| 20 | Document | Investigation & Search; Verify Document | DSR | 11-09-2026 | Planned |
| 21 | Document | Power of Attorney Authentication | DSR | 15-09-2026 | Planned |
| 22 | Document | DRO: Undervaluation, Deposit of will, Adjudication | DSR | 16-09-2026 to 17-09-2026 | Planned |
| 23 | Document | IGRO Appeal | DSR | 18-09-2026 | Planned |
| 24 | Document | BRE, MIS (#35–40), Dashboard (SR/DR/IGR) | DSR | 19-09-2026 to 21-09-2026 | Planned |
| 25 | Digital E-Stamp | Template design (all document types) | DSR | 22-09-2026 to 01-10-2026 | Planned |
| 26 | Encumbrance Search | EC issues & improvements | DSR | 03-10-2026 | Planned |
| 27 | Certified Copies | CC issues & improvements | DSR | 05-10-2026 | Planned |
| 28 | Document / EC / CC / Verify / PoA | Consolidated BRD | BA | 19-09-2026 to 05-10-2026 | Planned |
| 29–30 | Firm | Issues, BRE, MIS, Dashboard, Audit | DSR | 06-10-2026 to 09-10-2026 | Planned |
| 31 | Firm | BRD | BA | 12-10-2026 to 14-10-2026 | Planned |
| 32 | Refund | Process capture | DSR | 12-10-2026 | Planned |
| 33 | Audit | Audit module | DSR | 13-10-2026 | Planned |
| 34 | MDM | Master Data Management | DSR | 14-10-2026 | Planned |
| 35 | Refund / Audit / MDM | BRD | BA | 15-10-2026 | Planned |

### 2.3 Sub-module catalogue mapping (Modules list #1–50)

| # | Main | Sub-module | BR Sr. | Delivery phase |
|---|------|------------|--------|----------------|
| 29–31 | Marriage | Hindu / Special / Other forms | 1–9 | **Phase 1** |
| 47 | User Management | User Management | 10–11 | **Phase 1** |
| 25 | CC | Certified Copies | 27–28 | **Phase 1** |
| 12 | Registration | Scanning | 16 | **Phase 1** (shared platform) |
| — | Platform | eKYC, eSign, Khajane payment | Cross-cut (Marriage BR + platform) | **Phase 1** |
| — | MIS / Dashboard | Marriage-scoped | 1–7, 24 (pattern) | **Phase 1** |
| 4–5 | Registration | Stamp duty & fee; Guideline value | 13 | **Phase 2** |
| 21–22 | Registration | CVC Valuation; GIS valuation | 14 | **Phase 2** |
| 50 | E-Stamping | Digital E-Stamp | 25 | **Phase 2** (calc/templates); full instrument bind in Phase 3 |
| 1–2, 19 | Registration | Registration, Appointment, Status | 12 | **Phase 3** |
| 6–18, 20, 23 | Registration | Filings, memo, corrections, integration, search, re-regn | 15–20 | **Phase 3** |
| 26–27 | Verify / PoA | Verify Document; PoA Authentication | 20–21, 28 | **Phase 3** |
| 42–45 | DRO / IGRO | Undervaluation, Will deposit, Adjudication, Appeal | 22–23 | **Phase 3** |
| 24 | EC | Encumbrance Search | 26, 28 | **Phase 3** |
| 35–40 | MIS | Statutory / Statistical / Integration / Computer / Recon / HR | 24, 28 | **Phase 3** (Document); Marriage subset in Phase 1 |
| 41 | DRO | Firm Registration | 29–31 | **Phase 4** |
| 28, 33, 46 | Cross-cut | Refund, Audit, MDM | 32–35 | **Phase 1** foundation + extend per phase |
| 32, 34, 48–49 | Deferred | Legacy digitisation, Accounts, Mobile, Training | Not in this BR iteration | Backlog / parallel workstreams |

---

## 3. Scope by delivery phase

### 3.1 Phase 1 — Marriage platform & citizen services

**In scope**

| Area | Scope notes |
|------|-------------|
| Marriage | Hindu Marriage registration (Online eSign + Offline DEO) per Marriage BRD/HLD; Special Marriage if PO promotes after Sr.1–7 outcomes |
| Certified Copies (CC) | Citizen/officer request, fee, search, issue of certified extracts/copies (Marriage + shared CC spine usable later for Document) |
| User Management | Login, roles, office mapping, transfer, relieving, RBAC |
| eKYC | Identity proofing adapter (UIDAI / approved eKYC) for citizen and officer flows as decided |
| eSign | eSign adapter; hard gate before SR queue (Marriage Online); reusable for later modules |
| Khajane payment | Treasury / Khajane-II payment & reconciliation adapter; pay-after-approve for Marriage |
| Scanning | Scan ingest, AV, indexing hooks, DEO/SRO upload path (Marriage Offline + shared service) |
| Marriage Dashboard | SR / DR / IGR operational views for marriage volumes, pendency, SLA |
| Marriage MIS | Channel MIS, fee recon (marriage), statutory extracts as agreed in Marriage workshops |

**Out of Phase 1 (unless Steering promotes)**

Full Document Registration, EC property search, CVC market-value microservice go-live, Firm registration, mobile app, legacy ETL.

### 3.2 Phase 2 — Valuation & stamp duty microservices

**In scope**

| Service | Scope notes |
|---------|-------------|
| Stamp Duty Calculator | Instrument-wise duty & registration fee per Stamp Act Schedule + department circulars; versioned rate cards |
| Guideline Value Calculator | Guideline / market-value input to duty; alignment to published guidelines |
| Market Valuator (CVC) | Central Valuation Committee rules workflow support; estimation / publication / revision hooks per 2003 Rules |
| GIS Valuation | Geospatial parcel / property valuation assist (as scoped in Sr.14) |
| E-Stamp templates | Digital e-stamp template catalogue (Sr.25) consumed by calculators and later registration |

**Depends on:** Phase 1 payment/audit/masters; Stamp Act schedule master data; CVC publication feeds.

### 3.3 Phase 3 — Document Registration & Encumbrance

**In scope**

| Area | Sub-modules (#) |
|------|-----------------|
| Core registration | Registration, Appointment, Status tracking (#1, #2, #19) |
| Filings & scanning ops | Rule 17(2)/(3), Old pending release, FRUITS filing, Scanning (extend), Memo (#6–8, #11–13) |
| Corrections & special | Re-Registration, Will after death, 68(2), Rule 123 cross-ref (#9–10, #14–15, #23) |
| Integration & liability | Integration, exemption, Court entry, Liability (#3, #16–18) |
| Search & authenticity | Investigation & Search, Verify Document, PoA Authentication (#20, #26, #27) |
| DRO / IGRO | Undervaluation, Deposit of will, Adjudication, Appeal (#42–45) |
| EC | Encumbrance certificate search & issue (#24) |
| Dashboard & MIS | SR/DR/IGR dashboards; MIS packs #35–40 for Document/EC |

**Legal emphasis:** Compulsory/optional registration (ss.17–18), time/place (ss.23–29), re-registration (s.23A), computerised books (s.16A), Karnataka Amendments including forged-document controls (ss.22-B/C/D, 81-A/B per Act 47 of 2024), Rules 1965 books/forms/indexes, stamp adjudication & undervaluation paths.

### 3.4 Phase 4 — Firm Registration

**In scope**

| Area | Notes |
|------|--------|
| Firm Registration (DRO #41) | Intake, scrutiny, fee, certificate/register, amendments as scoped in Sr.29–31 |
| Firm MIS / Dashboard / Audit | Per Sr.30 |
| Reuse | User Mgmt, eKYC, eSign, Khajane, scanning, audit, MDM from earlier phases |

---

## 4. Legal and regulatory framework

### 4.1 Document corpus (`Acts_Rules/Document/`)

| Instrument | Relevance to phases |
|------------|---------------------|
| Registration Act, 1908 | Phase 3 core; CC/EC statutory basis; Phase 1 CC overlap |
| Karnataka Registration Rules, 1965 | Books, forms, indexes, office hours, seals, languages, Rule 17 supplements, Rule 123, scanning/filing practice |
| Registration (Karnataka Amendment) Acts 1975–2002, 2023 (Act 47 of 2024) | State-specific powers, forged document refusal/cancel/appeal/penalties |
| Karnataka Stamp Act, 1957 (+ Amendments 2011–2014) | Phase 2 calculators; Phase 3 duty at registration; adjudication |
| Karnataka Stamp Act Schedule 2022 | Rate card master for calculators |
| Karnataka Stamps Rules, 1958 | Stamp procedural rules |
| Payment of Stamp Duty by means of e-Stamping | Phase 2–3 e-stamp payment |
| Franking Impression of Stamps Rules, 2000 | Franking path if retained |
| CVC Market Value Guidelines Rules, 2003 | Phase 2 Market Valuator |
| Instruments governed by Stamp Act 1899 (reference) | Instrument classification input |
| Karnataka Societies Registration (Amendment) Rules, 2021 | Phase 4 fee/table updates (confirm Act set in Firm BR) |
| Lo-61-2019-20 / Registration notifications | Operational circulars for process design |

### 4.2 Marriage corpus (Phase 1)

Referenced from `Acts_Rules/Marriage/` and existing Marriage BRD/HLD: Hindu Marriage Act 1955; Registration of Hindu Marriage (Karnataka) Rules 1966; Special Marriage Act 1954 & Karnataka Rules 1961; RD48 fee notification; Form I / IA / II / II-A / III / VI.

### 4.3 Design rule

No production release of a statutory form, fee, refusal order, register entry, or certificate without **Domain Expert / Legal** template lock for that module.

---

## 5. Delivery approach

### 5.1 Principles

1. **BR schedule first** — discussion dates locked in schedule v3; BRD owners (BA) draft in parallel where noted.
2. **Platform before domain** — User Management, eKYC, eSign, Khajane, Audit, MDM, Scanning spine in Phase 1 before Document-heavy Phase 3.
3. **Calculators before registration** — Phase 2 valuation/duty services stable before Phase 3 registration fee/duty binding.
4. **One SDLC stack per phase** — BRD → HLD → Tech Architecture → SDD → LLD → Build → Test → Deploy → Go Live, with overlap only where contracts are frozen.
5. **Marriage is the pathfinder** — Phase 1 proves Online/Offline, payment-after-approve, DSC/eSign, scanning, MIS patterns reused later.
6. **Statutory lock early** — forms and fee schedules before UAT PDF/print gates.

### 5.2 Methodology

| Aspect | Approach |
|--------|----------|
| Cadence | 2-week sprints |
| Environments | Dev → SIT → UAT → Pre-Prod → Prod (+ isolated DR) |
| Definition of Done | Code + tests + OpenAPI/contract update + audit event + bilingual check where UI/PDF |
| Traceability | BR/FR/US ↔ service ↔ TC in RTM per module |
| Architecture style | API gateway, microservices, event bus, BFF per channel, adapters for Khajane / eSign / eKYC / DSC |

### 5.3 SDLC stage definitions (programme-wide)

| Stage | Exit artefact | Exit gate |
|-------|---------------|-----------|
| **Business Requirements** | Discussion MoM + approved BRD + prioritised backlog | BRD sign-off (PO + DE) |
| **HLD** | Context, containers, workflows, integrations, NFR targets | Architecture acceptance |
| **Technical Architecture** | Runtime, security, data, HA/DR, observability standards | Platform AD decisions closed |
| **SDD** | Service catalogue, APIs, state machines, data model L1, sequence flows | Design review |
| **LLD** | Class/module design, DB schemas, API payloads, error catalogues | Build-ready review |
| **Software Development** | Deployable services + UI + adapters | Sprint DoD + code review |
| **Software Testing** | SIT + UAT + NFR + statutory PDF packs | Test exit report |
| **Software Deployment** | Release notes, runbooks, infra as code, config | CAB / change approval |
| **Go Live** | Cutover checklist, hypercare, rollback | Steering go-live signature |

---

## 6. Programme timeline (indicative)

> Dates below are **indicative** and assume BR schedule v3 holds, staffing is available, and Phase 1 platform ADs close on time. Steering confirms calendar at kick-off.

### 6.1 Master timeline

```text
2026                         2027                          2028
Aug───Oct │ Nov──────Mar │ Apr────Jul │ Aug──────────Jan │ Feb───Apr
│  BR ALL │              │            │                 │
│ Ph1 Design+Build ──────────► Ph1 GL │                 │
│     Ph2 Design ──► Ph2 Build ───────► Ph2 GL          │
│           Ph3 Design ──► Ph3 Build ───────────────────► Ph3 GL
│                     Ph4 Design+Build ─────────────────────────► Ph4 GL
```

| Delivery phase | BR complete (anchor) | Design (HLD→LLD) | Development | Testing | Deploy | Go Live (target) |
|----------------|----------------------|------------------|-------------|---------|--------|------------------|
| **Phase 1** | Marriage BRD 21-08-2026; User Mgmt 25-08; Scanning discuss 05-09; CC 05-10; Refund/Audit/MDM BRD 15-10 | 24-08-2026 → 30-10-2026 | 21-09-2026 → 05-02-2027 | 01-12-2026 → 05-03-2027 | 08-03-2027 → 20-03-2027 | **23-03-2027** |
| **Phase 2** | Stamp/Guideline 29-08; CVC/GIS 01-09; E-Stamp discuss 01-10; in Doc BRD 05-10 | 06-10-2026 → 18-12-2026 | 04-01-2027 → 28-05-2027 | 15-04-2027 → 25-06-2027 | 28-06-2027 → 09-07-2027 | **12-07-2027** |
| **Phase 3** | Doc/EC/CC/Verify/PoA BRD 05-10-2026 | 19-10-2026 → 26-02-2027 | 01-03-2027 → 26-11-2027 | 01-09-2027 → 23-12-2027 | 03-01-2028 → 21-01-2028 | **24-01-2028** |
| **Phase 4** | Firm BRD 14-10-2026 | 15-01-2028 → 17-03-2028 | 20-03-2028 → 28-07-2028 | 05-06-2028 → 25-08-2028 | 28-08-2028 → 08-09-2028 | **11-09-2028** |

### 6.2 Phase 1 — detailed SDLC plan

| Stage | Start | End | Key activities | Owners |
|-------|-------|-----|----------------|--------|
| Business Requirements | 17-08-2026 | 15-10-2026 | Sr.1–11, 16 (scanning), 27 (CC), 32–35; Marriage & User Mgmt BRDs; platform NFR for eKYC/eSign/Khajane | DSR, BA, PO |
| HLD | 24-08-2026 | 26-09-2026 | Platform + Marriage + CC + Scanning containers; Online/Offline workflows; integration contracts | Architects |
| Technical Architecture | 24-08-2026 | 10-10-2026 | Identity, gateway, event bus, secrets, HA/DR, Khajane/eSign/eKYC AD | Platform Arch |
| SDD | 08-09-2026 | 24-10-2026 | Service catalogue, state machines, API contracts, data model | Module + Platform TLs |
| LLD | 22-09-2026 | 07-11-2026 | Schemas, payloads, error codes, UI wire→component map | Tech Leads |
| Software Development | 21-09-2026 | 05-02-2027 | P0 platform spine → Marriage Online → Offline → CC → Dash/MIS | Eng teams |
| Software Testing | 01-12-2026 | 05-03-2027 | SIT adapters; UAT Online/Offline/CC; statutory PDF; perf/security | QA, Security |
| Software Deployment | 08-03-2027 | 20-03-2027 | Pre-Prod soak, Prod release train, config & DSC rollout | DevOps, Ops |
| Go Live | 23-03-2027 | Hypercare 4 wks | Smoke E2E; war room; rollback criteria | Steering, Ops |

**Phase 1 build waves (aligned to Marriage plan)**

| Wave | Weeks (from 21-09-2026) | Focus |
|------|-------------------------|--------|
| W0 Platform | 1–4 | User Mgmt/Identity, Masters, Audit, Notify, Gateway, Object store, Scanning ingest contract |
| W1 Intake | 5–8 | Marriage common intake; eKYC hook |
| W2 Online | 9–14 | eSign, SR verify, Khajane pay-after-approve, DSC, Form II-A |
| W3 Offline + Scan | 15–20 | Appointment, print, DEO, Stage-2, scanning checklist |
| W4 CC + MIS | 21–24 | Certified copy flows; Marriage dashboard & MIS |
| W5 Harden | 25–28 | NFR, STQC, DR, training, go-live |

### 6.3 Phase 2 — detailed SDLC plan

| Stage | Start | End | Key activities |
|-------|-------|-----|----------------|
| Business Requirements | 28-08-2026 | 05-10-2026 | Sr.13–14, 25; calculator rules & CVC/GIS scope in Doc BRD |
| HLD | 06-10-2026 | 07-11-2026 | Microservice boundaries; rate-card versioning; GIS integration |
| Technical Architecture | 06-10-2026 | 21-11-2026 | Calc engine runtime; caching; audit of duty computations |
| SDD | 27-10-2026 | 05-12-2026 | APIs for duty, guideline, CVC, GIS; e-stamp template service |
| LLD | 17-11-2026 | 18-12-2026 | Formula engine design, schedule tables, exception paths |
| Software Development | 04-01-2027 | 28-05-2027 | Calculators + valuator + GIS + template catalogue |
| Software Testing | 15-04-2027 | 25-06-2027 | Golden-instrument test pack vs Schedule 2022; CVC scenarios |
| Software Deployment | 28-06-2027 | 09-07-2027 | Rate-card promotion controls |
| Go Live | 12-07-2027 | Hypercare 3 wks | Shadow-mode vs As-Is optional before hard cutover |

### 6.4 Phase 3 — detailed SDLC plan

| Stage | Start | End | Key activities |
|-------|-------|-----|----------------|
| Business Requirements | 25-08-2026 | 05-10-2026 | Sr.12–24, 26, 28 |
| HLD | 19-10-2026 | 18-12-2026 | Full registration workflow; EC search model; DRO/IGRO |
| Technical Architecture | 19-10-2026 | 30-01-2027 | Register books digital model; EC index store; forged-doc controls |
| SDD | 16-11-2026 | 26-02-2027 | Appointment saga; Rule 17 filings; memo; undervaluation; appeal |
| LLD | 05-01-2027 | 26-03-2027 | Book/volume/serial; EC index schemas; integration contracts |
| Software Development | 01-03-2027 | 26-11-2027 | Core regn → filings → EC → DRO/IGRO → Document MIS |
| Software Testing | 01-09-2027 | 23-12-2027 | Multi-instrument UAT; EC accuracy; Act 47 refusal/cancel paths |
| Software Deployment | 03-01-2028 | 21-01-2028 | Office-wise rollout plan (pilot SRO → district → state) |
| Go Live | 24-01-2028 | Hypercare 6 wks | Phased geographic cutover recommended |

### 6.5 Phase 4 — detailed SDLC plan

| Stage | Start | End | Key activities |
|-------|-------|-----|----------------|
| Business Requirements | 06-10-2026 | 14-10-2026 | Sr.29–31 |
| HLD / Tech Arch / SDD / LLD | 15-01-2028 | 17-03-2028 | Firm domain on shared platform |
| Software Development | 20-03-2028 | 28-07-2028 | Firm registration + MIS/Dashboard |
| Software Testing | 05-06-2028 | 25-08-2028 | DRO UAT + audit trails |
| Software Deployment | 28-08-2028 | 08-09-2028 | DRO office enablement |
| Go Live | 11-09-2028 | Hypercare 3 wks | Statewide Firm module |

---

## 7. Workstreams and organisation

| Workstream | Responsibilities | Primary phases |
|------------|------------------|----------------|
| Product / BA | Backlog, BRDs, RTM, UAT scenarios, EN/KN content | All |
| Domain / Legal | Statutory forms, fees, refusal/cancel rules, template lock | All |
| Architecture | HLD, Tech Arch, AD log, NFR | All |
| Platform | Identity/User Mgmt, Gateway, Audit, Notify, Doc/Scan store, Event bus | 1 → reuse |
| Integrations | Khajane, eSign, eKYC, DSC, SMS/Email, GIS, e-Stamp provider | 1–3 |
| Marriage domain | Intake → certify (see Marriage plan) | 1 |
| Valuation / Duty | Calculators, CVC, GIS | 2 |
| Document / EC domain | Registration, EC, DRO/IGRO extensions | 3 |
| Firm domain | Firm registration | 4 |
| UI/UX | Citizen portal, SRO/DRO/IGRO workbenches, DEO, Admin/MIS | All |
| QA | SIT/UAT/NFR/statutory packs | All |
| Security | RBAC, STQC, PII, AV, signing integrity | All |
| DevOps / SDC | CI/CD, envs, HA/DR, observability | All |
| Ops / Change | Runbooks, training, go-live, hypercare | All |

### 7.1 Indicative capacity (programme peak)

| Role | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|------|---------|---------|---------|---------|
| PO | 0.5 | 0.3 | 0.5 | 0.3 |
| BA | 2 | 1 | 3 | 1 |
| Domain / Legal | 0.5 | 0.5 | 1 | 0.5 |
| Architects | 1.5 | 1 | 2 | 0.5 |
| Backend eng | 8 | 4 | 12 | 4 |
| Frontend eng | 4 | 2 | 6 | 2 |
| Integration | 2 | 2 | 3 | 1 |
| QA | 4 | 2 | 6 | 2 |
| DevOps | 2 | 1 | 2 | 1 |
| Security | 0.5 | 0.5 | 1 | 0.3 |
| PM | 1 | 1 | 1 | 1 |

Exact FTE to be confirmed by delivery lead against vendor / department capacity.

---

## 8. Service / component build order

### 8.1 Phase 1

| Order | Component | Notes |
|-------|-----------|-------|
| 1 | identity-access / User Management | Roles, transfer, relieving, office scope |
| 2 | master-data, audit, notification, gateway, object-store | Platform spine |
| 3 | ekyc-adapter, esign-adapter, khajane-payment-adapter | Shared adapters |
| 4 | scanning-ingest-service | Shared; Marriage Offline first consumer |
| 5 | marriage-* services | Per Marriage HLD catalogue |
| 6 | certified-copy-service | Marriage + generic CC spine |
| 7 | marriage-dashboard + mis-reporting (marriage pack) | Operational + statutory |

### 8.2 Phase 2

| Order | Component |
|-------|-----------|
| 1 | stamp-duty-calculator-service |
| 2 | guideline-value-service |
| 3 | market-valuator-cvc-service |
| 4 | gis-valuation-service |
| 5 | e-stamp-template-service |

### 8.3 Phase 3

| Order | Component |
|-------|-----------|
| 1 | document-registration-intake + appointment + status |
| 2 | duty/fee bind to Phase 2 calculators |
| 3 | filing / memo / scanning ops extensions |
| 4 | correction / re-registration / will modules |
| 5 | integration / court / liability |
| 6 | verify-document + poa-authentication |
| 7 | encumbrance-search-service |
| 8 | dro-undervaluation / will-deposit / adjudication |
| 9 | igro-appeal |
| 10 | document EC dashboards + MIS packs #35–40 |

### 8.4 Phase 4

| Order | Component |
|-------|-----------|
| 1 | firm-registration-service |
| 2 | firm dashboard / MIS / audit views |

---

## 9. Testing strategy

| Layer | Phase 1 focus | Phase 2 focus | Phase 3 focus | Phase 4 focus |
|-------|---------------|---------------|---------------|---------------|
| Unit / API | Age, witnesses, pay gate, RBAC | Duty formulas, versioned schedules | Workflow transitions, book serials | Firm validations |
| Contract | BFF ↔ services; adapters mocked | Calc API consumers | EC index API; DRO/IGRO | Firm APIs |
| SIT | Khajane, eSign, eKYC, DSC, scan | E-stamp provider; GIS feed | Multi-office; FRUITS/memo | DRO offices |
| UAT | Online/Offline Marriage; CC | Instrument golden set | Full regn + EC + appeal | Firm E2E |
| Statutory / Legal | Forms I–II-A, VI, III | Schedule 2022 samples | Register books, refusal under Act 47 | Firm certificates |
| NFR | ≥ concurrent bar share; DR | Calc latency at peak | EC search SLAs; write load | Moderate |
| Security | STQC path, PII, AV | Integrity of duty audit | Forged-doc controls | RBAC DRO |

Each phase maintains **RTM-K3-P{n}-*** with FR → UC → TC status from design freeze onward.

---

## 10. Deployment and go-live approach

### 10.1 Environment progression

Dev → SIT → UAT → Pre-Prod (prod-like) → Prod; DR isolated and drilled before each phase go-live gate.

### 10.2 Release strategy

| Phase | Strategy |
|-------|----------|
| Phase 1 | Statewide platform + Marriage + CC; feature flags for Online vs Offline if needed |
| Phase 2 | Deploy calculators behind flags; optional shadow compare vs As-Is for 2–4 weeks |
| Phase 3 | **Pilot SRO → District → State**; EC indexes backfilled before cutover |
| Phase 4 | DRO office-wise enablement |

### 10.3 Go-live gate (every phase)

- [ ] BRD Must scope traced to passed UAT in RTM  
- [ ] Legal/DE form & fee lock  
- [ ] Security / STQC evidence for delta  
- [ ] Perf gate for phase share of load  
- [ ] DR drill evidence (RPO/RTO)  
- [ ] Ops runbooks + L1/L2/L3 roster  
- [ ] Training completion for impacted roles  
- [ ] Hypercare plan + rollback criteria  
- [ ] Steering signatures  

### 10.4 Hypercare

| Phase | Duration | Focus |
|-------|----------|-------|
| 1 | 4 weeks | Pay stuck, eSign abandon, scan upload, certificate/DSC |
| 2 | 3 weeks | Duty mismatches, guideline disputes |
| 3 | 6 weeks | Appointment, EC accuracy, undervaluation, forged-doc refusals |
| 4 | 3 weeks | Firm certificate / amendment defects |

---

## 11. Milestones

| ID | Milestone | Target | Owner |
|----|-----------|--------|-------|
| M-BR-END | Requirements window complete (Sr.35) | 15-10-2026 | PO / BA |
| M-P1-HLD | Phase 1 HLD + Tech Arch accepted | 10-10-2026 | Architects |
| M-P1-UAT | Phase 1 UAT complete | 05-03-2027 | QA / PO |
| M-P1-GL | Phase 1 Go Live | 23-03-2027 | Steering |
| M-P2-HLD | Phase 2 design accepted | 18-12-2026 | Architects |
| M-P2-GL | Phase 2 Go Live | 12-07-2027 | Steering |
| M-P3-HLD | Phase 3 HLD accepted | 18-12-2026 | Architects |
| M-P3-PILOT | Phase 3 pilot SRO live | 24-01-2028 | Ops / PO |
| M-P3-STATE | Phase 3 statewide | +6–10 weeks after pilot | Steering |
| M-P4-GL | Phase 4 Go Live | 11-09-2028 | Steering |

---

## 12. Dependencies

| Dependency | Needed by | Risk if late |
|------------|-----------|--------------|
| Schedule v3 BR workshops on time | All design starts | Cascading slip |
| Marriage BRD / HLD acceptance | Phase 1 build | Pathfinder delay |
| Khajane credentials & UAT merchant | Phase 1 Online pay | UAT blocked |
| eSign provider + legal signatory set | Phase 1 Online | Online MVP blocked |
| eKYC approval / sandbox | Phase 1 identity | Workaround manual KYC |
| DSC provisioning for SRO/DRO | Phase 1–3 certify paths | Certificate blocked |
| Stamp Act Schedule 2022 master digitisation | Phase 2 | Wrong duty |
| CVC guideline publication feeds | Phase 2 valuator | Stale values |
| GIS data sharing MoU | Phase 2 GIS | Feature defer |
| EC historical index migration plan | Phase 3 | EC go-live incomplete |
| Act 47 of 2024 process SOPs | Phase 3 | Refusal/cancel gaps |
| Firm Act/Rules confirmation in Sr.29–31 | Phase 4 | Scope churn |
| SDC capacity / HA-DR | Each go-live | Gate fail |

---

## 13. Risks

| ID | Risk | Phase | Mitigation | Owner |
|----|------|-------|------------|-------|
| R-01 | BR window slip past 15-10-2026 | All | Protect critical path Sr.9–11 for Phase 1; parallel BA | PM / PO |
| R-02 | eSign / Khajane / eKYC vendor delay | 1 | Mock adapters; weekly vendor war-room | Integration |
| R-03 | Scope creep (mobile, legacy ETL, accounts) | All | Explicit backlog; Steering change control | PO |
| R-04 | Phase 2 formulas disagree with field practice | 2 | Golden instrument pack with DE; shadow mode | DE / QA |
| R-05 | EC data quality / incomplete backfill | 3 | Early migration spike; pilot office proof | Arch / Ops |
| R-06 | Document Phase 3 too large for single release | 3 | Sub-wave releases inside Phase 3; geographic pilot | PM |
| R-07 | Act 47 forged-doc workflow ambiguity | 3 | Legal workshop before SDD freeze | Legal / DE |
| R-08 | Firm legal basis unclear vs Societies vs Partnership | 4 | Close in Sr.29–31; freeze Act set in Firm BRD | DE / PO |
| R-09 | Shared platform regressions across phases | 2–4 | Contract tests; versioned APIs; regression suite | QA / Arch |
| R-10 | Bilingual / GIGW defects late | 1–3 | Early PDF/UI gates each phase | Content / QA |

---

## 14. Governance and quality gates

### 14.1 Cadence

| Forum | Frequency | Purpose |
|-------|-----------|---------|
| Sprint ceremonies | Bi-weekly | Delivery |
| Domain / Legal workshops | Per schedule v3 + follow-ups | BR + statutory lock |
| Architecture sync | Weekly | AD/NFR/integrations |
| Phase steering | Monthly + at each M-* milestone | Scope, risk, go-live |
| Vendor integration | Weekly in active adapter windows | Khajane/eSign/eKYC/GIS |

### 14.2 Phase quality gates

| Gate | When | Criteria |
|------|------|----------|
| G-BR | End of module BRD | PO + DE sign-off |
| G-HLD | End HLD / Tech Arch | Architecture acceptance |
| G-SDD/LLD | Design freeze | Build-ready; OpenAPI published |
| G-SIT | Mid/late build | Adapters green in SIT |
| G-UAT | End test | E2E scenarios signed |
| G-SEC/NFR | Pre-deploy | Security + perf + DR |
| G-GL | Go Live | Steering checklist complete |

---

## 15. Training and change management

| Audience | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|----------|---------|---------|---------|---------|
| Citizens | Marriage channels, CC, payment, tracker | Duty estimators (if exposed) | Document appointment, EC, CC extend | Firm application |
| SRO | Marriage queues, DSC, scan/DEO | Duty override / view | Full registration workbench | — |
| DEO | Offline checklist, scanning | — | Filing/scan volumes | — |
| DRO | — | CVC participation views | Undervaluation, will, adjudication | Firm registration |
| IGRO | Marriage MIS | — | Appeal | — |
| L1/L2 support | Pay/eSign/scan runbooks | Duty mismatch | EC/appointment/regn | Firm defects |

---

## 16. Success criteria

| # | Criterion | Evidence |
|---|-----------|----------|
| S1 | Phase 1: Marriage Online + Offline + CC live with Khajane, eSign, eKYC, scanning | Prod smoke + RTM |
| S2 | Phase 1: User Management transfer/relieving operational | UAT + audit |
| S3 | Phase 1: Marriage dashboard & MIS available to SR/DR/IGR | Report pack sign-off |
| S4 | Phase 2: Stamp duty & guideline calculators match golden instruments | DE sign-off |
| S5 | Phase 2: Market Valuator / GIS services consumed by approved clients | Contract tests |
| S6 | Phase 3: Document registration E2E including fee/duty bind | Pilot then statewide |
| S7 | Phase 3: EC issued with agreed historical coverage | Data migration report |
| S8 | Phase 3: Document dashboards & MIS #35–40 (agreed subset) live | IGSR sign-off |
| S9 | Phase 4: Firm Registration live at DRO | Prod smoke |
| S10 | Each phase: security, DR, training, hypercare complete | Gate artefacts |

---

## 17. Immediate next actions (programme)

1. Steering confirm **four delivery phases** and indicative go-live dates in §6.  
2. Keep schedule v3 execution: complete Marriage BRD (Sr.9), then User Management (Sr.10–11).  
3. Open **DEC-K3-PROG-001** and lock Phase 1 platform ADs (identity, workflow engine, Khajane ownership, eSign provider).  
4. Stand up Phase 1 platform backlog (User Mgmt, eKYC, eSign, Khajane, scanning, audit).  
5. Align Marriage module plan (`PLAN-K3-MRG-HMA-001`) as **Wave detail** under Phase 1.  
6. Start digitising Stamp Schedule 2022 and CVC guideline masters for Phase 2 readiness.  
7. Commission EC index migration assessment spike before Phase 3 SDD freeze.  
8. Confirm Firm statutory Act set during Sr.29–31 (Oct 2026).

---

## 18. Acceptance of this plan

| Role | Name | Signature / Date | Comments |
|------|------|------------------|----------|
| Product Owner | | | |
| Project / Delivery Manager | | | |
| Solution Architect | | | |
| Domain Expert / Legal | | | |
| AIGR / IGSR nominee | | | |
| KPMU nominee | | | |

---

## Appendix A — BR Sr. → Delivery phase → SDLC start anchors

| BR Sr. | Module topic | Delivery phase | Design may start after |
|--------|--------------|----------------|------------------------|
| 1–9 | Marriage + Marriage BRD | Phase 1 | 21-08-2026 |
| 10–11 | User Management | Phase 1 | 25-08-2026 |
| 16 (Scanning) | Scanning | Phase 1 | 05-09-2026 |
| 27–28 (CC part) | Certified Copies | Phase 1 | 05-10-2026 |
| 32–35 | Refund, Audit, MDM | Phase 1 foundation | 15-10-2026 |
| 13–14, 25 | Duty, Guideline, CVC, GIS, E-Stamp | Phase 2 | 05-10-2026 |
| 12, 15–24, 26, 28 | Document Registration, EC, MIS, DRO/IGRO | Phase 3 | 05-10-2026 |
| 29–31 | Firm | Phase 4 | 14-10-2026 |

## Appendix B — Acts/Rules quick index

| Path under `Acts_Rules/Document/` | Use |
|-----------------------------------|-----|
| `the_registration_act,_1908.pdf` | Registration / EC / CC foundation |
| `The Karnataka Registration Rules 1965.pdf` | Books, forms, Rule 17, Rule 123, office practice |
| `TheRegistration(KarnatakaAmendment)Act2023(47of2024).pdf` | Forged document refuse/cancel/appeal/penalties |
| `Registration(KarnatakaAmendment)Act*.pdf` | Historical Karnataka amendments |
| `THE KARNATAKA STAMP ACT 1957.pdf` | Stamp duty framework |
| `Karnataka Stamp Act 1957 Schedule 2022.pdf` | Calculator rate card |
| `Karnataka Stamps Rules 1958.pdf` | Stamp procedures |
| `THE KARNATAKA STAMP- Payment of Stamp Duty by means of e-Stamping.pdf` | E-stamping |
| `Karnataka Stamp (Constitution of Central Valuation Committee...) Rules, 2003.docx` | Market Valuator |
| `Karnataka Stamp (Franking Impression Of Stamps) Rules, 2000.docx` | Franking |
| `INSTRUMENTS GOVERNED BY THE STAMP ACT 1899.docx` | Instrument list reference |
| `KarnatakaSocietiesRegistration(Amendment)Rules,2021.pdf` | Firm/Societies fee table updates |

## Appendix C — Document sub-module reference (schedule sheet)

Full mapping of Modules #1–50 to BR Sr. numbers is maintained in schedule workbook sheet **Document Sub-Modules Ref** and summarised in §2.3 of this plan.

---

*End of Programme Project Plan v0.1 — confirm dates and staffing with Steering; track BR schedule adherence weekly against `Kaveri_Requirements_Updated_Schedule_v3_DocumentSubModules.xlsx`.*
