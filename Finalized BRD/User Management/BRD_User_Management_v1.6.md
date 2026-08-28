# Business Requirements Document (BRD)

## User Management & Role-Based Access Control (RBAC) Module

## Document control

| Field | Value |
|--------|--------|
| **Document ID** | BRD-K3-UM-001 |
| **Version** | 1.6 |
| **Status** | Draft / In review |
| **Project** | KAVERI 3.0 — Department of Stamps and Registration (DSR), Government of Karnataka |
| **Module** | User Management & Role-Based Access Control (RBAC) |
| **Legal basis (primary)** | Information Technology Act, 2000; Indian Registration Act, 1908 (appointment of Registrars / Sub-Registrars); Aadhaar Act, 2016 (where biometric / Aadhaar is used) |
| **State / govt rules (primary)** | Karnataka e-Governance hosting and security norms; MeitY / CERT-In / STQC / GIGW; Government Orders for office and post creation |
| **Related inputs** | Requirement Discussions/BR_Discussion_Prep_Pack_User_Management_24Aug2026.docx; Finalized BRD/Marriage/RFP/BRD_Marriage_v1.9.docx (section pattern source) |
| **Author (BA)** | Nandha Kumar |
| **Product Owner** | Prashanth |
| **Domain expert / reviewer** | Prabhakar Naik |
| **Target audience** | Kaveri IT Cell, Department of Stamps and Registration, Government of Karnataka |
| **Last updated** | 2026-08-28 |

| Version | Date | Author | Summary of change | Approver |
|---------|------|--------|-------------------|----------|
| 1.0 | 2026-08-26 | Nandha Kumar | Initial User Management BRD for Kaveri 3.0: office, post, role, user, group, RBAC plus login, transfer, relieving, in-charge, DSC binding, audit and jurisdiction enforcement | Prashanth |
| 1.1 | 2026-08-26 | Nandha Kumar | BRD made self-contained for Kaveri 3.0 (no references to the prior application) | Prashanth |
| 1.2 | 2026-08-26 | Nandha Kumar | Replaced technical phrasing with plain language (central departmental login, role and office control used by all modules) | Prashanth |
| 1.3 | 2026-08-26 | Nandha Kumar | Recast as a requirements BRD (not an assessment); removed Phase 1-only framing; tightened executive summary | Prashanth |
| 1.4 | 2026-08-28 | Nandha Kumar | Passwordless OTP/Captcha/Biometric authentication; primary/secondary role model with session role selection; DSR organizational hierarchy; automated joining/relieving letters; dynamic role creation and hierarchy configuration; daily login MIS | Prashanth |
| 1.5 | 2026-08-28 | Nandha Kumar | Recast for KAVERI 3.0: dual user categories (public/citizen and department/officer); instant registration for citizens only; department users created via configurable designated admin roles; sanctioned posts master; department user mapping to sanctioned posts only; split passwordless auth (citizen: username+OTP+Captcha; officer: username+OTP+Captcha+Biometrics) | Prashanth |
| 1.6 | 2026-08-28 | Nandha Kumar | Added third user category — Other Department users (officers/staff from other government departments); created by designated admin roles only (configurable); authentication Username+OTP+Captcha+Biometrics | Prashanth |

**Distribution:** Kaveri 3.0 BRD workspace (Finalized BRD/User Management)

**Related documents:**

| ID | Title | Link |
|----|--------|------|
| BRD-K3-UM-001 | This document | Finalized BRD/User Management/BRD_User_Management_v1.6.docx |
| PREP-K3-UM-001 | BR Discussion Prep Pack — User Management | Requirement Discussions/BR_Discussion_Prep_Pack_User_Management_24Aug2026.docx |
| BRD-K3-MRG-001 | Marriage Registration BRD (section pattern source) | Finalized BRD/Marriage/RFP/BRD_Marriage_v1.9.docx |
| RTM-K3-UM-001 | Requirements traceability matrix | Section 13 of this document |

## Contents

- 1. Executive summary
- 2. Scope
- 2.1 In scope (User Management & RBAC)
- 2.2 Out of scope (unless PO promotes)
- 2.3 Assumptions
- 2.4 Constraints
- 3. Legal and regulatory reference
- 4. Stakeholders and actors
- 5. Definitions and glossary
- 6. Current state (As-Is)
- 6.1 As-Is process summary
- 6.2 As-Is pain points
- 7. Future state (To-Be)
- 7.1 User categories and access model
- 7.2 Organizational hierarchy, posts and sanctioned posts
- 7.3 Public user (citizen) onboarding
- 7.4 Department user (DSR officer) onboarding and lifecycle
- 7.5 Other Department user onboarding and lifecycle
- 7.6 Role-Based Access Control and session management
- 7.7 Authentication and credential management
- 7.8 System administration and configuration
- 7.9 Automated letter generation
- 7.10 Reporting and MIS
- 7.11 Status models
- 8. Functional requirements
- 9. Business rules
- 10. User interface (high-level)
- 11. Integrations
- 12. Data requirements
- 13. Requirements traceability matrix (RTM)
- 14. Acceptance and sign-off
- 15. Non-functional requirements
- 16. Risk and Mitigation Strategy
- 17. System Fallbacks & Error Handling
- 18. Training and Change Management
- Appendix A — References
- Appendix B — DSR organizational hierarchy and seed posts
- Appendix C — Open questions and decision log

## 1. Executive summary

This Business Requirements Document defines the business requirements for the **User Management & Role-Based Access Control (RBAC)** module within the **KAVERI 3.0** ecosystem for the Department of Stamps and Registration (DSR), Government of Karnataka.

The module manages the **lifecycle, authentication, authorization, and hierarchy mapping** of all users of the Kaveri platform. It serves **three** distinct user categories:

| Category | Description | Account creation | Authentication |
|----------|-------------|------------------|----------------|
| **Public users (Citizens)** | Citizens accessing Kaveri portal services (Marriage, Document Registration, etc.) | **Instant self-registration** — no approval required | Username + OTP + Captcha |
| **Department users (DSR Officers)** | Officers and staff of DSR (IGR, DIGR, AIGR, SR, FDA, SDA, etc.) | Created **only** by designated admin roles (e.g. AIGR Admin) — configurable by Application Admin | Username + OTP + Captcha + **Biometrics** |
| **Other Department users** | Officers and staff of **other government departments** requiring access to Kaveri (e.g. Treasury, Revenue, Police, ULB) | Created **only** by designated admin roles (e.g. AIGR Admin) — configurable by Application Admin | Username + OTP + Captcha + **Biometrics** |

The module is the **central identity, login, role, post and office control used by all KAVERI 3.0 modules**.

**Key capabilities (KAVERI 3.0):**

- **Instant citizen registration** with no multi-level approval for public users.
- **Controlled provisioning for DSR and Other Department users** — only roles designated by the Application Admin (e.g. AIGR Admin, Super Admin) may create officer accounts in either departmental category.
- **Sanctioned posts master** capturing departmental posts (IGR, DIGR, AIGR, Sub-Registrar, FDA, SDA, DRO, HQA, etc.) with sanctioned strength per office.
- **Department users mapped exclusively to pre-defined sanctioned posts** — no ad-hoc or unlisted post assignment.
- **Dynamic RBAC** with Primary Role (substantive post, no end date), Secondary Roles (mandatory end date, auto-expiry), and session-based role selection / switching for officers.
- **Split passwordless authentication** — citizens: Username + OTP + Captcha; DSR officers and Other Department users: Username + OTP + Captcha + Biometrics (mandatory).
- Automated **Joining** and **Relieving** letters; hierarchy configuration; daily login MIS; immutable audit.

**Success criteria (measurable):**

- Citizens complete self-registration instantly and authenticate with Username + OTP + Captcha.
- DSR department users are created only by configured designated admin roles and mapped to a sanctioned post.
- Other Department users are created only by configured designated admin roles and assigned module-specific access roles.
- DSR officers and Other Department users authenticate with Username + OTP + Captcha + Biometrics; no password option exists.
- Vacant vs occupied sanctioned posts are visible; no user assigned to a post outside the sanctioned catalogue.
- All user-management actions are fully auditable.

## 2. Scope

### 2.1 In scope (User Management & RBAC)

**User categories:**

- **Public users (Citizens):** instant self-registration, profile management, passwordless login (Username + OTP + Captcha).
- **Department users (DSR Officers):** provisioning by designated admin roles only, mapping to sanctioned DSR posts, passwordless login (Username + OTP + Captcha + Biometrics).
- **Other Department users:** provisioning by designated admin roles only, assignment to module-specific access roles (not DSR sanctioned posts), passwordless login (Username + OTP + Captcha + Biometrics).

**Core capabilities:**

- Sanctioned **posts master** for DSR (IGR, DIGR, AIGR, Sub-Registrar, FDA, SDA, DRO, HQA, and other DSR posts) with sanctioned strength per office.
- Mapping of **DSR department users** to **pre-defined sanctioned posts only**.
- **Other Department user** master with parent department name, designation, and module access roles.
- Configurable **designated admin roles** authorised to create DSR and Other Department users (e.g. AIGR Admin — set by Application Admin).
- DSR organizational hierarchy; dynamic RBAC (primary / secondary / session roles).
- Automated joining and relieving letters; hierarchy configuration; reporting; immutable audit.

### 2.2 Out of scope (unless PO promotes)

- HRMS / payroll as the system of record for appointment, pay, and leave (this module records **application access** occupancy against sanctioned posts, not the full HR file).
- Physical access control, CCTV, or non-Kaveri applications.
- Replacement of CCA / eSign provider operations (this BRD binds certificates to active post holders where applicable).
- Fine-grained privilege matrices for modules not yet designed — catalogue entries may be created in advance; function mapping is completed as each consuming module is specified.

### 2.3 Assumptions

| ID | Assumption | Owner to validate |
|----|------------|-------------------|
| A-01 | The DSR organizational chart and sanctioned post list in Appendix B are authoritative seed data | Domain Expert, IGR |
| A-02 | **Username** is the login identifier for all three user categories | Security, PO |
| A-03 | OTP is delivered to the user's registered mobile and/or email within 5 seconds | Ops, Arch |
| A-04 | Biometric capture devices and UIDAI / department approvals are in place before DSR and Other Department user login is enabled | Security, Legal |
| A-05 | Official letter templates for Joining and Relieving are provided before UAT | Domain Expert |
| A-06 | Application Admin configures which roles may create DSR and Other Department users (default includes AIGR Admin) | PO |
| A-07 | Consuming modules read session role and privilege claims from this module | Arch |
| A-08 | Citizen eKYC / Aadhaar verification may be invoked during citizen registration per consuming-module BRDs | PO, Security |

### 2.4 Constraints

- GIGW / MeitY guidelines, accessibility (WCAG 2.x), Karnataka e-Gov hosting and CERT-In / STQC security norms.
- **No password-based authentication** in KAVERI 3.0.
- **Citizens** authenticate with Username + OTP + Captcha only — biometrics not used for public users.
- **DSR department users** and **Other Department users** must complete Username + OTP + Captcha + Biometrics on every login.
- DSR department users may be assigned **only** to posts in the sanctioned posts master.
- DSR and Other Department user accounts may be created **only** by roles in the designated-creator list (configurable).
- OTP delivery within **5 seconds** (NFR-UM-02).
- Biometric data re-registered every **5 years** for DSR and Other Department users (REQ-UM-013).

## 3. Legal and regulatory reference

| Instrument | Topic | BRD relevance |
|------------|--------|----------------|
| Information Technology Act, 2000 | Electronic records, digital signatures, audit | Passwordless login, eSign/DSC binding, immutable logs |
| IT (SPDI) Rules, 2011 | Security practices, SPDI | Citizen and officer PII (photo, ID proof, Aadhaar, biometric, mobile) |
| Aadhaar Act, 2016 and UIDAI circulars | Aadhaar / biometric | Biometric authentication for department users |
| Indian Registration Act, 1908 | Appointment and jurisdiction of Registrars / Sub-Registrars | Sanctioned posts, SR role, jurisdiction |
| Karnataka Government servant / KGID practice | Unique employee identity | KGID for Government Appointed officers |
| MeitY / CERT-In / STQC / GIGW | Security, audit, accessibility | AuthN, session, audit export |
| Government Orders creating / renaming / merging offices and posts | Legal existence of office and post | GO scan for new offices / posts; sanctioned strength |

## 4. Stakeholders and actors

| Actor | User category | Description | Primary goals |
|-------|---------------|-------------|---------------|
| **Citizen (Public user)** | Public | Any member of the public using Kaveri portal services | Self-register instantly; log in with Username + OTP + Captcha; access citizen services |
| **Application Admin** | Department | Super Admin / KPMU / IGR nominee | Configure designated creator roles; manage sanctioned posts; system-wide configuration |
| **Designated admin (e.g. AIGR Admin)** | Department | Officer role authorised to create DSR and Other Department users | Create user accounts; map DSR users to sanctioned posts; assign Other Department users to access roles |
| **IGR** | Department | Inspector General of Registration | Department-wide oversight; approve primary post changes |
| **DIGR / AIGR / DR / SR / FDA / SDA** | Department | Divisional and field officers | Perform functions under selected session role |
| **Department user (DSR Officer)** | Department | DSR officer or staff with a Kaveri login | Log in (Username + OTP + Captcha + Biometrics); select session role |
| **Other Department user** | Other Department | Officer or staff from another government department with Kaveri access | Log in (Username + OTP + Captcha + Biometrics); access assigned modules |
| **Security / audit reviewer** | Department | Internal audit, AG, STQC | Inspect user, post occupancy and privilege history |

**RACI (summary):**

| Step | Application Admin | Designated admin (e.g. AIGR Admin) | IGR / DIGR | Citizen | DSR Officer | Other Dept user |
|------|-------------------|-------------------------------------|------------|---------|-------------|-----------------|
| Citizen self-registration (instant) | — | — | — | R | — | — |
| Configure designated creator roles | A/R | I | I | — | — | — |
| Create DSR department user | C | A/R | C | — | I | — |
| Create Other Department user | C | A/R | C | — | — | I |
| Map DSR officer to sanctioned post | C | A/R | C | — | I | — |
| Assign Other Department user access roles | C | A/R | C | — | — | I |
| Manage sanctioned posts master | A/R | C | C | — | — | — |
| Citizen login (Username+OTP+Captcha) | — | — | — | R | — | — |
| DSR / Other Dept login (+Biometrics) | — | — | — | — | R | R |
| Session role selection / switch | — | — | — | — | R | — |

## 5. Definitions and glossary

| Term | Definition | Source |
|------|------------|--------|
| Public user (Citizen) | A member of the public registered on the Kaveri portal for citizen-facing services | §7.1 |
| Department user (DSR Officer) | An officer or staff member of DSR with a Kaveri departmental login, mapped to a sanctioned DSR post | §7.1 |
| Other Department user | An officer or staff member of a **government department other than DSR** granted access to specific Kaveri modules | §7.1 |
| Username | Login identifier for all user categories (citizen-chosen or system-assigned per policy) | REQ-UM-025, REQ-UM-026, REQ-UM-027 |
| Instant registration | Citizen account created immediately on self-registration without approval workflow | REQ-UM-001 |
| Designated creator role | A role authorised by Application Admin to create DSR and Other Department user accounts (e.g. AIGR Admin) | REQ-UM-022 |
| Post | A sanctioned position in the department (e.g. Sub-Registrar, FDA, IGR, DIGR) tied to an office | REQ-UM-023 |
| Sanctioned post | A post defined in the posts master with approved strength (headcount) per office; the only posts to which department users may be mapped | REQ-UM-023, REQ-UM-024 |
| Sanctioned strength | Approved number of occupants for a given post at a given office | REQ-UM-023 |
| Primary Role | Officer's substantive post assignment; cannot have an end date | REQ-UM-002 |
| Secondary Role | Additional temporary role; mandatory end date; auto-expires | REQ-UM-003 |
| Session Role | Role selected by an officer after login for the current session | REQ-UM-007 |
| Passwordless Authentication | Login without passwords — citizens: Username + OTP + Captcha; DSR officers and Other Department users: Username + OTP + Captcha + Biometrics | REQ-UM-025, REQ-UM-026, REQ-UM-027 |
| Parent department | The government department to which an Other Department user belongs (e.g. Revenue, Treasury, Police) | REQ-UM-027 |

## 6. Current state (As-Is)

### 6.1 As-Is process summary

The current system mixes citizen and departmental identity boundaries inconsistently. Citizens and officers often share password-based flows. Department user creation is not restricted to designated admin roles. Posts are not maintained as a sanctioned master — users are assigned to free-text roles without sanctioned-strength enforcement. Biometric authentication is optional and not separated by user category.

### 6.2 As-Is pain points

| ID | Pain point | Impact | To-Be address (ref) |
|----|------------|--------|---------------------|
| UM-PP-01 | Password-based login failures and lockouts | Users cannot access services | REQ-UM-025, REQ-UM-026 |
| UM-PP-02 | No separate citizen vs officer identity model | Wrong auth strength; confusion | §7.1, REQ-UM-025, REQ-UM-026 |
| UM-PP-03 | Officers assigned without sanctioned post validation | Over-staffing; audit findings | REQ-UM-023, REQ-UM-024 |
| UM-PP-04 | Any admin can create department users | Uncontrolled provisioning | REQ-UM-022 |
| UM-PP-05 | Citizen registration requires manual approval in some flows | Delayed access | REQ-UM-001 |
| UM-PP-06 | No biometric mandate for departmental users | Weak authentication | REQ-UM-026, REQ-UM-027 |
| UM-PP-07 | Posts (SR, FDA, SDA, IGR, DIGR) not in a unified sanctioned master | Incorrect occupancy reporting | §7.2, REQ-UM-023 |
| UM-PP-08 | No separate category for other-government-department users | Wrong access model for inter-department users | REQ-UM-027 |

## 7. Future state (To-Be)

> **Source of truth:** this BRD, DSR organizational chart, sanctioned posts schedule, and KAVERI 3.0 programme requirements.

### 7.1 User categories and access model

| Access model | User category | Who | Account creation | Authentication | In scope? |
|--------------|---------------|-----|------------------|----------------|-----------|
| Citizen portal (self-service) | Public user (Citizen) | Any citizen | **Instant self-registration** (REQ-UM-001) | Username + OTP + Captcha (REQ-UM-025) | Yes |
| Department console | Department user (DSR Officer) | DSR officers and staff | **Designated admin roles only** (REQ-UM-022) | Username + OTP + Captcha + Biometrics (REQ-UM-026) | Yes |
| Inter-department console | Other Department user | Officers/staff of other govt departments | **Designated admin roles only** (REQ-UM-022) | Username + OTP + Captcha + Biometrics (REQ-UM-027) | Yes |
| Application administration | Application Admin | KPMU / Super Admin | N/A (bootstrap) | DSR / Other Dept auth flow | Yes |

Citizens, DSR department users, and Other Department users are **separate identity domains** with distinct registration paths, authentication flows, and privilege models. A single physical person may hold accounts in more than one category, but these are separate records.

### 7.2 Organizational hierarchy, posts and sanctioned posts

#### 7.2.1 DSR organizational hierarchy (roles)

| Division | Roles |
|----------|-------|
| **Top Management** | Inspector General of Registration & Commissioner of Stamps (IGR) |
| **Division 1 (Admin, Law & Computers)** | DIGR (Admin, Law & Computers), AIGR (Admin), HQA (Admin), SRO (Admin), FDA, SDA |
| **Division 2 (Vigilance)** | DIGR (Vigilance), Law Officer, HQA (RTI) |
| **Division 3 (Computers)** | AIGR (Computers), System Integrator, PMU, Application Developer, SRO (Comp) |
| **Division 4 (Enforcement)** | DIGR (Enforcement), District Registrar (DRO), HQA, Sub Registrar (SRO), FDA, SDA |
| **Division 5 (Intelligence & Audit)** | DIGR (Intelligence), AIGR (Audit), HQA (Audit), Superintendent (Audit) |
| **Division 6 (CVC)** | DIGR CVC, JD Town Planning |

#### 7.2.2 Sanctioned posts master

The system shall maintain a **posts master** listing all departmental posts with abbreviation, acronym, hierarchy level, and **sanctioned strength per office**.

**Seed posts (non-exhaustive):**

| Post name | Abbreviation | Typical office types |
|-----------|--------------|---------------------|
| Inspector General of Registration | IGR | IGRO |
| Deputy Inspector General of Registration | DIGR | IGRO / Division |
| Assistant Inspector General of Registration | AIGR | IGRO / Division |
| District Registrar | DR / DRO | DRO |
| Sub-Registrar | SR / SRO | SRO |
| First Division Assistant | FDA | SRO / IGRO |
| Second Division Assistant | SDA | SRO / IGRO |
| Head of Office / Head Quarters Assistant | HQA | IGRO / DRO / SRO |
| Law Officer | LO | IGRO |
| Superintendent (Audit) | Supdt (Audit) | IGRO |
| Data Entry Operator | DEO | SRO |

#### 7.2.3 Sanctioned posts — process steps

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Application Admin opens Posts Master → Add / Edit Post | Admin | REQ-UM-023 |
| 2 | Enter Post Name, Abbreviation, Acronym, hierarchy level | Admin | REQ-UM-015 |
| 3 | Select office(s); enter sanctioned strength (headcount) per office | Admin | REQ-UM-023 |
| 4 | Upload supporting GO / sanction order (for new posts) | Admin | Should |
| 5 | Save — post available for department user mapping | System | |
| 6 | Dashboard shows vacant vs occupied posts per office | System | REQ-UM-024 |

### 7.3 Public user (citizen) onboarding

#### 7.3.1 Instant citizen self-registration

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Citizen opens Kaveri portal → Register | Citizen | REQ-UM-001 |
| 2 | Enter name, mobile, email, choose Username | Citizen | Username unique |
| 3 | Complete Captcha | Citizen | |
| 4 | Verify mobile / email via OTP | System | |
| 5 | Account created **instantly** — no approval workflow | System | REQ-UM-001 |
| 6 | Citizen may immediately log in | Citizen | REQ-UM-025 |

### 7.4 Department user (DSR officer) onboarding and lifecycle

#### 7.4.1 DSR department user creation (designated admin only)

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Designated admin (e.g. AIGR Admin) opens User Management → Add Department User | Admin | REQ-UM-022; role must be in designated-creator list |
| 2 | System validates caller holds a configured designated creator role | System | Block if not authorised |
| 3 | Enter officer particulars (name, Username, mobile, email, KGID, photo, ID proof) | Admin | |
| 4 | Select **sanctioned post** from posts master (vacant slot only) | Admin | REQ-UM-024; cannot assign unlisted post |
| 5 | Assign as **Primary Role** (mandatory; no end date) | Admin | REQ-UM-002 |
| 6 | Optionally assign **Secondary Role(s)** with end date and approval letter | Admin | REQ-UM-003, REQ-UM-004 |
| 7 | Capture biometrics (mandatory for department users) | Admin / Officer | REQ-UM-026 |
| 8 | Optionally set future effective date | Admin | REQ-UM-006 |
| 9 | Save — account active; post occupancy updated | System | |

#### 7.4.2 Primary post modification

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Designated admin selects officer → Change Primary Post | Admin | Promotion, transfer, demotion |
| 2 | Select new **sanctioned post** (vacant) | Admin | REQ-UM-024 |
| 3 | Enter reason; upload approval letter | Admin | REQ-UM-005 |
| 4 | Set effective date (immediate or future) | Admin | REQ-UM-006 |
| 5 | System updates occupancy; generates Joining / Relieving letter | System | REQ-UM-018 |

#### 7.4.3 Secondary role expiry

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Secondary role end date reached | System | Scheduled job |
| 2 | System automatically removes secondary role access | System | REQ-UM-003 |
| 3 | Audit event logged | System | NFR-UM-01 |

### 7.5 Other Department user onboarding and lifecycle

Other Department users are officers or staff from **government departments other than DSR** who require access to one or more Kaveri modules (e.g. Treasury verification, Revenue cross-check, Police enquiry). They are **not** mapped to DSR sanctioned posts; instead they receive **module-specific access roles** scoped to their parent department.

#### 7.5.1 Other Department user creation (designated admin only)

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Designated admin (e.g. AIGR Admin) opens User Management → Add Other Department User | Admin | REQ-UM-022, REQ-UM-027; role must be in designated-creator list |
| 2 | System validates caller holds a configured designated creator role | System | Block if not authorised |
| 3 | Enter user particulars (name, Username, mobile, email, photo, ID proof) | Admin | |
| 4 | Enter **parent department** name (e.g. Revenue, Treasury, Police, ULB) | Admin | REQ-UM-027 |
| 5 | Enter designation / official title | Admin | REQ-UM-027 |
| 6 | Assign **module access role(s)** (not DSR sanctioned posts) | Admin | REQ-UM-027 |
| 7 | Upload authorisation letter / NOC from parent department | Admin | Should |
| 8 | Capture biometrics (mandatory) | Admin / User | REQ-UM-027 |
| 9 | Set validity period (mandatory end date) | Admin | Should — access expires unless renewed |
| 10 | Save — account active | System | |

#### 7.5.2 Other Department user access renewal / deactivation

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Validity period expires or admin deactivates | System / Admin | |
| 2 | Login blocked; module access removed | System | |
| 3 | Audit event logged | System | NFR-UM-01 |
| 4 | Admin may renew with updated authorisation letter | Admin | |

### 7.6 Role-Based Access Control and session management

*(Applies to DSR department users only.)*

#### 7.6.1 Session role selection

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Officer completes passwordless login (§7.6.2) | Officer / System | |
| 2 | If multiple roles assigned, system presents role list | System | REQ-UM-007 |
| 3 | Officer selects session role | Officer | |
| 4 | Menus and permissions update dynamically | System | |

#### 7.6.2 Dynamic role switching

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Officer clicks Role Switch | Officer | REQ-UM-008 |
| 2 | Select new session role — no logout required | Officer | |
| 3 | Menus update; audit of switch | System | |

#### 7.6.3 Peer / subordinate role editing

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Application Admin configures peer/subordinate editing toggle per role | Admin | REQ-UM-009 |
| 2 | Elevated roles edit peers/subordinates within span | Admin | When toggle enabled |

### 7.7 Authentication and credential management

#### 7.7.1 Citizen (public user) — passwordless login

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Citizen enters **Username** | Citizen | REQ-UM-025 |
| 2 | System displays Captcha | System | |
| 3 | Citizen completes Captcha | Citizen | |
| 4 | Citizen requests OTP | Citizen | |
| 5 | OTP dispatched within 5 seconds | System | NFR-UM-02 |
| 6 | Citizen enters OTP | Citizen | |
| 7 | System validates Username + OTP + Captcha — all three must match | System | No biometrics for citizens |
| 8 | Access granted to citizen portal | System | No password option (REQ-UM-010) |

#### 7.7.2 DSR department user (officer) — passwordless login

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Officer enters **Username** | Officer | REQ-UM-026 |
| 2 | System displays Captcha | System | |
| 3 | Officer completes Captcha | Officer | |
| 4 | Officer requests OTP | Officer | |
| 5 | OTP dispatched within 5 seconds | System | NFR-UM-02 |
| 6 | Officer enters OTP | Officer | |
| 7 | System validates Username + OTP + Captcha | System | |
| 8 | Officer completes **Biometric verification** (mandatory) | Officer / Device | REQ-UM-026, REQ-UM-012 |
| 9 | If biometric data > 5 years old, prompt re-registration first | System | REQ-UM-013 |
| 10 | Access granted; proceed to session role selection (§7.6.1) | System | |

#### 7.7.3 Other Department user — passwordless login

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | User enters **Username** | Other Dept user | REQ-UM-027 |
| 2 | System displays Captcha | System | |
| 3 | User completes Captcha | Other Dept user | |
| 4 | User requests OTP | Other Dept user | |
| 5 | OTP dispatched within 5 seconds | System | NFR-UM-02 |
| 6 | User enters OTP | Other Dept user | |
| 7 | System validates Username + OTP + Captcha | System | |
| 8 | User completes **Biometric verification** (mandatory) | User / Device | REQ-UM-027, REQ-UM-012 |
| 9 | If biometric data > 5 years old, prompt re-registration first | System | REQ-UM-013 |
| 10 | Access granted to assigned modules only | System | No DSR sanctioned post / session role picker |

### 7.8 System administration and configuration

#### 7.8.1 Configure designated creator roles

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Application Admin opens Configuration → Designated Creator Roles | Admin | REQ-UM-022 |
| 2 | Select role(s) authorised to create DSR and Other Department users (e.g. AIGR Admin, Super Admin) | Admin | Configurable list |
| 3 | Save | System | Audit event |

#### 7.8.2 Dynamic role and hierarchy configuration

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Application Admin adds role or adjusts hierarchy | Admin | REQ-UM-014, REQ-UM-017 |
| 2 | Enter Role Name, Abbreviation, Acronym | Admin | REQ-UM-015 |
| 3 | Set reporting relationship | Admin | |
| 4 | Save | System | |

### 7.9 Automated letter generation

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Post / role change triggered | System | REQ-UM-018 |
| 2 | Select Joining or Relieving template | System | REQ-UM-019 |
| 3 | Auto-populate user details, post abbreviations, effective dates | System | |
| 4 | Generate in-app; store with audit reference | System | |

### 7.10 Reporting and MIS

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Admin opens Reports → Daily Login Report | Admin | REQ-UM-020 |
| 2 | Report shows logins by user category (citizen / DSR officer / other department) and session role | System | REQ-UM-021 |
| 3 | Sanctioned post occupancy report (vacant / filled) | Admin | REQ-UM-023 |
| 4 | Export CSV / PDF | Admin | |

### 7.11 Status models

#### 7.11.1 Citizen account status

| Status | Description | Next states |
|--------|-------------|-------------|
| Active | Citizen can log in | Suspended / Closed |
| Suspended | Disabled with reason | Active / Closed |
| Closed | Terminal | — |

#### 7.11.2 DSR department user account status

| Status | Description | Next states |
|--------|-------------|-------------|
| Active | Officer can log in and select session role | Suspended / Relieved |
| Suspended | Immediate disable | Active / Relieved |
| Pending future post change | Scheduled assignment | Active |
| Relieved | Post vacated; login blocked | Closed |
| Closed | Historical record | — |

#### 7.11.3 Other Department user account status

| Status | Description | Next states |
|--------|-------------|-------------|
| Active | User can log in and access assigned modules | Suspended / Expired |
| Suspended | Immediate disable with reason | Active / Deactivated |
| Expired | Validity period ended; login blocked | Renewed / Deactivated |
| Deactivated | Admin revoked access | Closed |
| Closed | Historical record | — |

#### 7.11.4 Sanctioned post occupancy status

| Status | Description | Next states |
|--------|-------------|-------------|
| Vacant | Sanctioned slot unfilled | Occupied |
| Occupied | Officer mapped to post | Vacant (relieve / transfer) |
| Over-capacity | Attempt to exceed sanctioned strength | Blocked by system |

## 8. Functional requirements

> **Convention:** Req ID `REQ-UM-###`. Priority: Must / Should / Could.

### 8.1 User categories and onboarding

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| REQ-UM-001 | **Public users (citizens):** account creation shall happen instantly via self-registration. No multi-level approval process is required to create a citizen profile | Must | Citizen registers and account is active immediately |
| REQ-UM-022 | **DSR department users** and **Other Department users:** accounts shall be created **only** by users holding a **designated creator role** (e.g. AIGR Admin). The list of designated creator roles shall be **configurable by the Application Admin** | Must | Non-designated role cannot access Add Department User or Add Other Department User; AIGR Admin can when configured |
| REQ-UM-002 | A Primary Role (substantive sanctioned post) must be assigned to each department user during account creation. The Primary Role **cannot** have an end date | Must | Save without Primary Role fails for officers |
| REQ-UM-003 | Additional roles are Secondary Roles with mandatory end date; access auto-removed on expiry | Must | Expired secondary role absent from session list |
| REQ-UM-004 | Approval letter required when granting a secondary role | Must | Save without letter fails |
| REQ-UM-005 | Primary post change requires reason and approval letter | Must | Blocked without both |
| REQ-UM-006 | Future-dated role/post changes applied automatically on effective date | Must | Scheduler applies on date |

### 8.2 Sanctioned posts

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| REQ-UM-023 | The system shall maintain a **sanctioned posts master** capturing departmental posts (including IGR, DIGR, AIGR, Sub-Registrar, First Division Assistant, Second Division Assistant, DRO, HQA, and other DSR posts) with **sanctioned strength per office** | Must | Posts master lists all seed posts; strength per office editable |
| REQ-UM-024 | DSR department users shall be mapped **only** to posts defined in the sanctioned posts master. Assignment to a post not in the master or exceeding sanctioned strength shall be blocked | Must | Unlisted post rejected; over-capacity rejected |

### 8.2.1 Other Department users

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| REQ-UM-027 | **Other Department users** (officers/staff from government departments other than DSR) shall be created **only** by designated creator roles (configurable by Application Admin). The system shall capture parent department, designation, module access role(s), and mandatory biometrics. Other Department users shall **not** be mapped to DSR sanctioned posts | Must | Add Other Department User blocked for non-designated roles; parent dept and access roles saved |
| REQ-UM-028 | **Other Department users** shall authenticate using **Username**, **OTP**, **Captcha**, and **Biometrics** (all four mandatory). Access granted only when all four succeed | Must | Login blocked if any factor fails; same auth strength as DSR officers |

### 8.3 Role-Based Access Control and session management

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| REQ-UM-007 | Officers with multiple roles shall select a session role after login; menus update dynamically | Must | Role picker shown; menus match selection |
| REQ-UM-008 | Officers may switch session roles without logout | Must | Switch without re-auth |
| REQ-UM-009 | Application Admin may toggle peer/subordinate role-editing permission per role | Must | Toggle controls elevated-role edit capability |

### 8.4 Authentication and credential management

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| REQ-UM-010 | The traditional password option shall be completely removed from the application for both user categories | Must | No password field on any login screen |
| REQ-UM-025 | **Public users (citizens)** shall authenticate using **Username**, **OTP**, and **Captcha**. Access granted only when all three match. Biometrics shall **not** be used for citizens | Must | Citizen login succeeds with all three; no biometric prompt |
| REQ-UM-026 | **DSR department users (officers)** shall authenticate using **Username**, **OTP**, **Captcha**, and **Biometrics** (all four mandatory). Access granted only when all four succeed | Must | DSR officer login blocked if any factor fails; biometric mandatory |
| REQ-UM-012 | Biometric capture and verification shall be integrated for DSR and Other Department user login | Must | Biometric step present in both departmental login flows |
| REQ-UM-013 | DSR and Other Department users must re-register biometrics every five (5) years | Must | Login blocked until re-registration when expired |

### 8.5 System administration and configuration

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| REQ-UM-014 | Application Admin may create unlimited new roles as needed | Must | New role creatable |
| REQ-UM-015 | Role / post create and edit captures Name, Abbreviation, and Acronym | Must | All three mandatory |
| REQ-UM-016 | Abbreviation / acronym displayed throughout UI (dashboards, audit logs, headers) | Must | Visible in header and audit |
| REQ-UM-017 | Application Admin may configure hierarchy level and reporting relationships for all roles / posts | Must | Hierarchy tree editable |

### 8.6 Automated letter generation

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| REQ-UM-018 | System auto-generates Joining and Relieving letters on post / role change | Must | Letter generated in-app |
| REQ-UM-019 | Official department letter templates auto-populated with user details, dates, post abbreviations | Must | Template matches department format |

### 8.7 Reporting and MIS

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| REQ-UM-020 | Daily report of users logged in, by user category (citizen / DSR officer / other department) | Must | All three category counts per day |
| REQ-UM-021 | Daily login report shows active session roles for officers | Must | Role breakdown in report |

## 9. Business rules

| Rule ID | Description | Source | System enforcement |
|---------|-------------|--------|-------------------|
| BR-UM-001 | Three user categories: Public (Citizen), Department (DSR Officer), and Other Department — separate identity domains | §7.1 | Hard separation |
| BR-UM-002 | Instant registration applies to **citizens only** | REQ-UM-001 | No approval workflow for citizens |
| BR-UM-003 | DSR and Other Department users created **only** by designated creator roles (configurable) | REQ-UM-022 | 403 for non-designated roles |
| BR-UM-004 | DSR department users mapped **only** to sanctioned posts in the posts master | REQ-UM-024 | Hard stop |
| BR-UM-005 | Other Department users **not** mapped to DSR sanctioned posts; assigned module access roles only | REQ-UM-027 | Hard stop on sanctioned post mapping |
| BR-UM-006 | Sanctioned strength per office cannot be exceeded | REQ-UM-023 | Block over-capacity assignment |
| BR-UM-007 | Primary Role mandatory for DSR officers; no end date | REQ-UM-002 | Hard stop |
| BR-UM-008 | Secondary Roles require end date; auto-expire | REQ-UM-003 | Scheduled job |
| BR-UM-009 | Citizen auth: Username + OTP + Captcha only (no biometrics) | REQ-UM-025 | AuthN gate |
| BR-UM-010 | DSR officer auth: Username + OTP + Captcha + Biometrics (all mandatory) | REQ-UM-026 | AuthN gate |
| BR-UM-011 | Other Department user auth: Username + OTP + Captcha + Biometrics (all mandatory) | REQ-UM-028 | AuthN gate |
| BR-UM-012 | No password authentication in KAVERI 3.0 | REQ-UM-010 | Password UI removed |
| BR-UM-013 | Biometric re-registration every 5 years for DSR and Other Department users | REQ-UM-013 | Login block |
| BR-UM-014 | All user-management actions audited (timestamp, IP, actor) | NFR-UM-01 | Immutable audit |

## 10. User interface (high-level)

| Screen / step | Purpose | Actor | User category | Notes |
|---------------|---------|-------|---------------|-------|
| Citizen registration | Instant self-registration | Citizen | Public | REQ-UM-001 |
| Citizen login | Username + Captcha + OTP | Citizen | Public | REQ-UM-025 |
| DSR officer login | Username + Captcha + OTP + Biometrics | DSR Officer | Department | REQ-UM-026 |
| Other Department user login | Username + Captcha + OTP + Biometrics | Other Dept user | Other Department | REQ-UM-028 |
| Biometric re-registration | 5-year mandatory update | DSR Officer / Other Dept user | Department / Other Department | REQ-UM-013 |
| Session role picker | Select role after login | DSR Officer | Department | REQ-UM-007 |
| Role switcher | Change session role | DSR Officer | Department | REQ-UM-008 |
| Add DSR Department User | Create DSR officer (designated admin only) | Designated admin | — | REQ-UM-022 |
| Add Other Department User | Create inter-department user (designated admin only) | Designated admin | — | REQ-UM-027 |
| Map to sanctioned post | Assign DSR officer to vacant post | Designated admin | — | REQ-UM-024 |
| Assign module access roles | Grant Other Department user module access | Designated admin | — | REQ-UM-027 |
| Posts master | Manage sanctioned DSR posts and strength | Application Admin | — | REQ-UM-023 |
| Designated creator config | Configure who may create DSR and Other Dept users | Application Admin | — | REQ-UM-022 |
| Letter preview / download | Joining / Relieving (DSR officers) | Admin / Officer | Department | REQ-UM-018 |
| Daily login report | MIS by category and role | Admin | — | REQ-UM-020, REQ-UM-021 |
| Post occupancy report | Vacant / filled sanctioned posts | Admin | — | REQ-UM-023 |

**Bilingual:** All labels `[EN / KN]` — Kannada values from masters.

## 11. Integrations

| Integration | Direction | Purpose | User category | Status |
|-------------|-----------|---------|---------------|--------|
| SMS gateway | Outbound | OTP delivery | Both | Must; ≤ 5 s |
| Email gateway | Outbound | OTP (alternate) | Both | Should |
| Captcha service | Internal | Bot prevention | Both | Must |
| Biometric device / SDK | Device | DSR and Other Department login verification | Department / Other Department | Must |
| Aadhaar / eKYC | Outbound | Citizen identity (per module BRD) | Public | TBD |
| DSC / eSign provider | Inbound | Certificate metadata | Department | Where applicable |
| Consuming modules | API provide | Session claims, post occupancy | Both | Must |
| Audit / SIEM | Outbound | Auth and admin events | Both | Should |

## 12. Data requirements

### 12.1 Core entities (logical)

- **User** — user category (Public / Department / Other Department), Username, names, mobile, email, KGID (DSR officers), parent department (Other Department users), designation, photo, ID proof, biometric refs, active status.
- **SanctionedPost** — post name, abbreviation, acronym, hierarchy level, office, sanctioned strength, occupied count (DSR only).
- **PostOccupancy** — user (DSR officer), sanctioned post, type (Primary / Secondary), valid from/to, approval letter, status.
- **OtherDepartmentUser** — user, parent department, designation, module access roles, validity period, authorisation letter artefact.
- **DesignatedCreatorRole** — role ID, configured by Application Admin, active flag.
- **Role** — name, abbreviation, acronym, hierarchy, peer-edit toggle.
- **Session** — user, category, selected session role (officers), login timestamp, IP, auth factors used.
- **Letter**, **AuditEvent** — as in prior version.

### 12.2 Retention

| Data class | Retention |
|------------|-----------|
| Citizen, DSR officer, and Other Department accounts, post occupancy | Permanent for audit |
| Biometric templates (DSR and Other Department users) | Per UIDAI policy; re-register every 5 years |
| Audit logs | ≥ 7 years unless Legal specifies otherwise |

### 12.3 Migration (high level)

| Topic | Question for migration workstream |
|-------|-----------------------------------|
| Legacy citizens | Map to public user category; force passwordless at cutover |
| Legacy officers | Map to DSR department users; assign sanctioned posts; re-capture biometrics |
| Other Department users | Identify inter-department users from legacy; migrate with parent dept and access roles |
| Sanctioned posts | Build master from establishment schedule / GO |
| Designated creators | Default: AIGR Admin, Super Admin |

## 13. Requirements traceability matrix (RTM)

| Req ID | Requirement summary | BRD section | UI screen | Test case ID | Status |
|--------|---------------------|-------------|-----------|--------------|--------|
| REQ-UM-001 | Instant citizen self-registration | 7.3.1, 8.1 | Citizen registration | TC-UM-001 | Draft |
| REQ-UM-022 | DSR and Other Dept users via designated creators | 7.4.1, 7.5.1, 8.1 | Add Department User / Add Other Department User | TC-UM-022 | Draft |
| REQ-UM-027 | Other Department user provisioning | 7.5.1, 8.2.1 | Add Other Department User | TC-UM-027 | Draft |
| REQ-UM-028 | Other Dept: Username+OTP+Captcha+Biometrics | 7.7.3, 8.2.1 | Other Department login | TC-UM-028 | Draft |
| REQ-UM-023 | Sanctioned posts master | 7.2, 8.2 | Posts master | TC-UM-023 | Draft |
| REQ-UM-024 | Map officers to sanctioned posts only | 7.4.1, 8.2 | Map to post | TC-UM-024 | Draft |
| REQ-UM-002 | Primary Role, no end date | 7.4.1, 8.1 | Add Department User | TC-UM-002 | Draft |
| REQ-UM-003 | Secondary Role auto-expiry | 7.4.3, 8.1 | Assign Secondary Role | TC-UM-003 | Draft |
| REQ-UM-025 | Citizen: Username+OTP+Captcha | 7.6.1, 8.4 | Citizen login | TC-UM-025 | Draft |
| REQ-UM-026 | DSR officer: Username+OTP+Captcha+Biometrics | 7.7.2, 8.4 | DSR officer login | TC-UM-026 | Draft |
| REQ-UM-007 | Session role selection | 7.5.1, 8.3 | Session role picker | TC-UM-007 | Draft |
| REQ-UM-008 | Role switching | 7.5.2, 8.3 | Role switcher | TC-UM-008 | Draft |
| REQ-UM-010 | No passwords | 8.4 | All login screens | TC-UM-010 | Draft |
| REQ-UM-013 | Biometric re-registration 5 years | 7.6.2, 8.4 | Biometric re-registration | TC-UM-013 | Draft |
| REQ-UM-018 | Auto letters | 7.8, 8.6 | Letter preview | TC-UM-018 | Draft |
| REQ-UM-020 | Daily login report | 7.9, 8.7 | Daily login report | TC-UM-020 | Draft |
| NFR-UM-01 | Audit logging | 15.2 | Audit export | TC-UM-NFR-01 | Draft |
| NFR-UM-02 | OTP ≤ 5 seconds | 15.1 | Login | TC-UM-NFR-02 | Draft |

## 14. Acceptance and sign-off

| Role | Name | Signature / Date | Comments |
|------|------|------------------|----------|
| Product Owner | Prashanth | | |
| Domain Expert | Prabhakar Naik | | |
| IGR nominee | | | |
| AIGR Computers / Kaveri IT Cell | | | |
| Business Analyst | Nandha Kumar | | |
| Security reviewer | | | |

**UAT scope:** Citizen instant registration and Username+OTP+Captcha login; DSR officer creation by designated admin and sanctioned post mapping; Other Department user creation by designated admin with parent department and module roles; DSR and Other Department Username+OTP+Captcha+Biometrics login; session role selection (DSR); biometric 5-year rule; posts master; designated creator configuration; letters; MIS; audit.

**Go-live gate:** Three user categories operational; sanctioned posts enforced for DSR; Other Department access roles enforced; passwordless auth live for all categories.

## 15. Non-functional requirements

### 15.1 Performance (NFR-UM-02)

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| NFR-UM-02 | OTP delivery within 5 seconds for all user categories | Must | 95th percentile ≤ 5 s |

### 15.2 Security and audit (NFR-UM-01)

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| NFR-UM-01 | Every user-management action logged with timestamp, IP address, and actor ID | Must | Immutable audit export |

### 15.3 System availability

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| NFR-UM-03 | Authentication service 99.5% available during business hours | Must | Monitoring dashboard |
| NFR-UM-04 | Scheduled jobs (secondary role expiry, future-dated changes) run at least hourly | Must | Job logs |

### 15.4 Security audit and compliance

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| NFR-UM-05 | MeitY / CERT-In / STQC / GIGW compliance | Must | VAPT before go-live |
| NFR-UM-06 | Biometric data per UIDAI guidelines (DSR and Other Department users) | Must | Security sign-off |

## 16. Risk and Mitigation Strategy

| Risk ID | Risk | Mitigation | Related requirements |
|---------|------|------------|---------------------|
| RS-UM-001 | Unauthorized DSR or Other Department user creation | Designated creator role enforcement; audit | REQ-UM-022 |
| RS-UM-002 | DSR officer assigned to non-sanctioned post | Posts master hard block | REQ-UM-024 |
| RS-UM-003 | Citizen subjected to biometric collection | Separate auth flows; no biometric for citizens | REQ-UM-025 |
| RS-UM-004 | Biometric device failure blocks departmental logins | Admin break-glass with audit (time-limited) | REQ-UM-026, REQ-UM-028, FB-UM-003 |
| RS-UM-005 | Over-capacity post assignment | Sanctioned strength validation | REQ-UM-023, BR-UM-006 |
| RS-UM-006 | Other Department user granted excessive module access | Least-privilege role assignment; periodic access review | REQ-UM-027 |

## 17. System Fallbacks & Error Handling

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FB-UM-001 | OTP gateway unreachable: queue and retry; clear user message | Must | No silent failure |
| FB-UM-002 | Captcha failure: present alternate challenge | Must | Login not blocked |
| FB-UM-003 | Biometric device unavailable: time-limited admin break-glass for DSR and Other Department users with full audit; citizens unaffected | Must | Departmental users only fallback |
| FB-UM-004 | Letter generation failure: log and allow retry | Must | Post change not rolled back |

## 18. Training and Change Management

### 18.1 Target audience

- Application Admins (posts master, designated creators, hierarchy).
- Designated admins (DSR and Other Department user creation, post mapping, access roles).
- DSR officers (passwordless login with biometrics, session roles).
- Other Department users (passwordless login with biometrics, assigned modules).
- Citizens (self-registration and login) — via portal help content.

### 18.2 Training delivery

- Admin training for sanctioned posts, Other Department user provisioning, and designated creator configuration.
- DSR officer and Other Department user training for biometric login.
- Citizen-facing portal guides for registration and OTP login.

### 18.3 Change management

- Communicate removal of passwords for both categories before cutover.
- Communicate biometric enrollment requirement for DSR and Other Department users.
- Pilot with one division before statewide rollout.

### 18.4 Post-Go-Live support

- Hypercare for 30 days; separate helpdesk scripts for citizen, DSR officer, and Other Department user login issues.

## Appendix A — References

- BR Discussion Prep Pack — User Management (24 August 2026)
- Marriage BRD v1.9 — Finalized BRD/Marriage/RFP/BRD_Marriage_v1.9.docx
- Information Technology Act, 2000; Aadhaar Act, 2016; Indian Registration Act, 1908
- MeitY / CERT-In / STQC / GIGW guidance
- DSR Organizational Chart and establishment schedule (sanctioned posts)

## Appendix B — DSR organizational hierarchy and seed posts

### B.1 Hierarchy (divisions and roles)

| Division | Roles |
|----------|-------|
| Top Management | IGR |
| Division 1 — Admin, Law & Computers | DIGR (Admin, Law & Computers), AIGR (Admin), HQA (Admin), SRO (Admin), FDA, SDA |
| Division 2 — Vigilance | DIGR (Vigilance), Law Officer, HQA (RTI) |
| Division 3 — Computers | AIGR (Computers), System Integrator, PMU, Application Developer, SRO (Comp) |
| Division 4 — Enforcement | DIGR (Enforcement), DRO, HQA, SRO, FDA, SDA |
| Division 5 — Intelligence & Audit | DIGR (Intelligence), AIGR (Audit), HQA (Audit), Superintendent (Audit) |
| Division 6 — CVC | DIGR CVC, JD Town Planning |

### B.2 Seed sanctioned posts

| Post | Abbreviation | Notes |
|------|--------------|-------|
| Inspector General of Registration | IGR | Top management |
| Deputy Inspector General of Registration | DIGR | Division head |
| Assistant Inspector General of Registration | AIGR | Includes AIGR Admin (designated creator default) |
| District Registrar | DR | DRO office head |
| Sub-Registrar | SR | SRO office head |
| First Division Assistant | FDA | Field / office staff |
| Second Division Assistant | SDA | Field / office staff |
| Head Quarters Assistant | HQA | Admin / accounts |
| Law Officer | LO | Vigilance / legal |
| Superintendent (Audit) | Supdt (Audit) | Audit division |
| Data Entry Operator | DEO | SRO operations |
| System Integrator | SI | Computers division |
| Application Developer | AD | Computers division |

Sanctioned strength per office is configured in the posts master (REQ-UM-023). Application Admin may add posts (REQ-UM-014).

### B.3 Default designated creator roles

| Role | Designated creator (default) | Configurable? |
|------|------------------------------|---------------|
| AIGR (Admin) | Yes | Yes — Application Admin |
| AIGR (Computers) | Yes | Yes |
| Super Admin (KPMU) | Yes | Yes |
| IGR | Yes | Yes |

## Appendix C — Open questions and decision log

### C.1 Open questions

| Q ID | Question | Options / notes | Needed from | Due |
|------|----------|-----------------|-------------|-----|
| OQ-UM-01 | Citizen Username: mobile number, email, or user-chosen? | Impacts REQ-UM-025 | PO, Security | |
| OQ-UM-02 | Officer Username: official email, KGID, or both? | Impacts REQ-UM-026 | Security, PO | |
| OQ-UM-03 | Sanctioned strength source: establishment schedule or manual entry? | REQ-UM-023 | Domain Expert | |
| OQ-UM-04 | Biometric break-glass duration when device unavailable? | FB-UM-003 | Security | |
| OQ-UM-05 | Can one officer hold Primary post at two offices (additional charge)? | REQ-UM-002 | Domain Expert | |

### C.2 Decisions

| Dec ID | Decision | Date | Approver | Impact |
|--------|----------|------|----------|--------|
| DEC-UM-001 | KAVERI 3.0 — three user categories: Public (Citizen), Department (DSR Officer), Other Department | 2026-08-28 | PO (to confirm) | §7.1 |
| DEC-UM-002 | Instant registration for citizens only; DSR and Other Department users via designated admin | 2026-08-28 | PO (to confirm) | REQ-UM-001, REQ-UM-022 |
| DEC-UM-003 | DSR officers mapped to sanctioned posts only; Other Department users to module access roles | 2026-08-28 | Domain Expert (to confirm) | REQ-UM-024, REQ-UM-027 |
| DEC-UM-004 | Split auth: citizen Username+OTP+Captcha; DSR and Other Department +Biometrics | 2026-08-28 | Security (to confirm) | REQ-UM-025, REQ-UM-026, REQ-UM-028 |
| DEC-UM-005 | AIGR Admin as default designated creator (configurable) | 2026-08-28 | PO (to confirm) | REQ-UM-022 |
| DEC-UM-006 | Other Department users are inter-department govt officers, not DSR staff | 2026-08-28 | PO (to confirm) | REQ-UM-027 |

*End of BRD — User Management & RBAC Module, KAVERI 3.0.*
