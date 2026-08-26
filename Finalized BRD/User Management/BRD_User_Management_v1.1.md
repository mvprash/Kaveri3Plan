# Business Requirements Document (BRD)

## User Management Module

## Document control

| Field | Value |
|--------|--------|
| **Document ID** | BRD-K3-UM-001 |
| **Version** | 1.1 |
| **Status** | Draft / In review |
| **Module** | User Management (departmental identity, office, post, role, group, RBAC) |
| **Legal basis (primary)** | Information Technology Act, 2000; Indian Registration Act, 1908 (appointment of Sub-Registrars); Aadhaar Act, 2016 (where biometric / Aadhaar is used) |
| **State / govt rules (primary)** | Karnataka e-Governance hosting and security norms; MeitY / CERT-In / STQC / GIGW; Khajane-II DDO mapping; Government Orders for office and post creation |
| **Related inputs** | Requirement Discussions/BR_Discussion_Prep_Pack_User_Management_24Aug2026.docx; Requirement Discussions/ServiceDesk Issues/ServiceDeskIssuesList.xlsx; Project_Plan_Kaveri_3.0_Programme_v0.4; Finalized BRD/Marriage/RFP/BRD_Marriage_v1.6.docx |
| **Author (BA)** | Nandha Kumar |
| **Product Owner** | Prashanth |
| **Domain expert / reviewer** | Prabhakar Naik |
| **Target audience** | Kaveri IT Cell, Department of Stamps and Registration, Government of Karnataka |
| **Last updated** | 2026-08-26 |

| Version | Date | Author | Summary of change | Approver |
|---------|------|--------|-------------------|----------|
| 1.0 | 2026-08-26 | Nandha Kumar | Initial User Management BRD for Kaveri 3.0: office, post, role, user, group, RBAC plus login, transfer, relieving, in-charge, DSC binding, audit and jurisdiction enforcement | Prashanth |
| 1.1 | 2026-08-26 | Nandha Kumar | BRD made self-contained for Kaveri 3.0 (no references to the prior application) | Prashanth |

**Distribution:** Kaveri 3.0 BRD workspace (Finalized BRD/User Management)

**Related documents:**

| ID | Title | Link |
|----|--------|------|
| BRD-K3-UM-001 | This document | Finalized BRD/User Management/BRD_User_Management_v1.1.docx |
| PREP-K3-UM-001 | BR Discussion Prep Pack — User Management | Requirement Discussions/BR_Discussion_Prep_Pack_User_Management_24Aug2026.docx |
| BRD-K3-MRG-HMA-001 | Marriage Registration BRD (section pattern source) | Finalized BRD/Marriage/RFP/BRD_Marriage_v1.6.docx |
| RTM-K3-UM-001 | Requirements traceability matrix | Section 13 of this document |
| ANNEX-UM-MAP | Role / group / module privilege matrix | To be prepared and signed before UAT (Appendix C seed roles; full function map TBD) |

## Contents

- 1. Executive summary
- 2. Scope
- 2.1 In scope (User Management — Phase 1)
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
- 7.1 Operating model and admin hierarchy
- 7.2 Office Type
- 7.3 Office
- 7.4 Post
- 7.5 Role
- 7.6 Map Role to Modules / Sub-modules / Functions
- 7.7 User lifecycle
- 7.8 Group
- 7.9 Map Group to Modules / Sub-modules / Functions
- 7.10 Module / Sub-module / Function catalogue
- 7.11 Authentication, password and session
- 7.12 Transfer, relieving, in-charge and additional charge
- 7.13 DSC and officer identity binding
- 7.14 Status models
- 7.15 Process changes versus As-Is
- 8. Functional requirements
- 9. Business rules
- 10. User interface (high-level)
- 11. Integrations
- 12. Data requirements
- 13. Requirements traceability matrix (RTM)
- 14. Acceptance and sign-off
- Appendix A — References
- Appendix B — Delegated administration action matrix
- Appendix C — Seed office types, roles and ID-proof types
- Appendix D — Open questions and decision log

## 1. Executive summary

This document presents a comprehensive assessment of departmental **User Management** for Kaveri 3.0. It is based on department-stated administration needs, ServiceDesk evidence of live operational failures, and the Phase 1 programme mandate that User Management cover **login, roles, office mapping, transfer, relieving and RBAC**.

The current administration model already describes office hierarchy, posts, roles, groups, users and module-function mapping, but it does not reliably support credential lifecycle, in-charge / additional charge, relieving, DSC binding to the active post holder, or hard jurisdiction filters. These gaps surface as login failures, missing officer names in allocation dropdowns, digital-sign identity mismatches, and wrong-office / wrong-district visibility.

The proposed Kaveri 3.0 User Management module is the **identity and access spine** for all departmental logins. It shall provide delegated administration (KPMU / IGR / DIGR / DR / SR), bilingual office and role masters, post-based occupancy, role- and group-based privileges, verified officer identity (KGID, official email, mobile), transfer and relieving with access cut-off, in-charge occupancy, DSC binding to the active SR (or other signing post), immutable audit of privilege changes, and a single master that allocation, MIS, OTP and digital-sign consumers must read.

**Success criteria (measurable):**

- 100% of Phase 1 departmental users (Marriage, CC, scanning, MIS) authenticate and receive menus solely from this module.
- Allocation dropdowns (DEO, SR, in-charge) show only **active post holders** of the correct office / jurisdiction.
- Transfer, relieving and in-charge change take effect on the next session (or within the agreed cut-over window) with DSC and work-queue identity updated.
- Privilege and user-master changes are maker-checker controlled (or dual-control for Super Admin) and fully auditable.
- Reduction in ServiceDesk “login / mapping / in-charge / digital sign identity” tickets versus the current baseline (UM-PP-01 to UM-PP-10).

**Phase / MVP boundary:** Phase 1 delivers departmental User Management for Kaveri 3.0 go-live. Citizen authentication / eKYC account lifecycle is **out of this BRD** unless the Product Owner promotes it (see OQ-UM-11).

## 2. Scope

### 2.1 In scope (User Management — Phase 1)

- Departmental user administration for officers and staff of the Department of Stamps & Registration using Kaveri 3.0.
- Admin hierarchy: Super Admin (KPMU), Department Admin (IGR), DIGR Admin, District Admin (DR), SRO Admin (SR) — with a resolved action matrix (Appendix B).
- Masters: **Office Type**, **Office** (including DDO code, jurisdiction, short name / triplet, anywhere-registration flag, bilingual names, enable/disable), **Post**, **Role**, **Group**, **Module / Sub-module / Function** catalogue.
- User lifecycle: create, view, edit, activate / deactivate, search / filter by office type and office, Government Appointed vs Contract, KGID, official email as login, verified mobile, ID proof, photo, optional PAN verification, optional biometric capture.
- RBAC: map Role and Group to Module / Sub-module / Function (view, add, edit, print, scan, download, approve, sign, and other function verbs as catalogued).
- Data access restriction by **Office ID** (SRO-scoped users) and **Jurisdiction ID** (district- or IGRO-scoped roles).
- **Login, password, unlock, reset, session and (agreed) MFA** for departmental users.
- **Transfer, relieving, in-charge and additional charge** workflows, including history retained for audit and migration (DM-P1-02).
- Binding of **DSC / eSign certificate** to the **active post holder** of a signing role (at minimum Sub-Registrar), so digital-sign and certificate issuance resolve the correct legal name.
- Notifications (SMS / email) for account create, reset, transfer, relieving, privilege change.
- MIS / operational reports for user, role, office occupancy, transfers and privileged actions.
- Bilingual UI: English + Kannada labels for office type, office name, role and group as captured in masters.
- Audit trail of all user-administration and privilege-mapping actions.
- Migration of agreed legacy users, roles, office mappings and transfer / relieving history (depth per data-migration workstream).
- Seed and maintain the departmental roles required by Marriage Phase 1 (SR, DEO, FDA, SDA, DR, IGR and related) so Marriage Online / Offline RBAC can be enforced from this spine.

### 2.2 Out of scope (unless PO promotes)

- Citizen portal registration, citizen password self-service, citizen eKYC account lifecycle (separate identity boundary; Marriage and other citizen BRDs).
- HRMS / payroll as a system of record for appointment, pay and leave (this module consumes or records departmental **application access** occupancy, not the full HR file).
- Rebuild of unrelated departmental systems (Bhoomi and others) except agreed integration keys (office code, DDO, KGID).
- Fine-grained privilege matrices for modules not yet in Phase 1 — catalogue entries may be created, but function mapping for Document / Firm / EC beyond Phase 1 consumers is a later increment.
- CSG developer “Add Module / Function” production self-service after go-live without change-control (catalogue changes are a controlled development / MDM activity).
- Physical access control, CCTV, or non-Kaveri applications.
- Replacement of CCA / eSign provider operations; this BRD only binds certificates already issued to the active post holder.

### 2.3 Assumptions

| ID | Assumption | Owner to validate |
|----|------------|-------------------|
| A-01 | The administration capabilities in this BRD (office, post, role, user, group, mapping) are the baseline to implement and harden | PO, Domain Expert |
| A-02 | Official **email ID is the login name** unless DQ-04 decides otherwise (KGID / mobile / State SSO) | Security, PO |
| A-03 | **Group privilege overrides Role privilege**, unless OQ-UM-06 reverses this | PO, Security |
| A-04 | Existing ~298 offices are created / migrated first; new offices require a scanned Government Order | Domain Expert, KPMU |
| A-05 | Khajane-II DDO codes for DRO and SRO are available in a mapping table for existing offices | Treasury / KPMU |
| A-06 | A signed role / group / module privilege matrix will be completed before UAT | BA, AIGR Computers |
| A-07 | DEO is both a **Role** and a **Post occupancy** at an SRO; allocation dropdowns read active occupancy, not a static name list | PO, Domain Expert |
| A-08 | Citizen identity is out of this BRD; departmental and citizen IdPs remain separate | Security, PO |
| A-09 | Sub-Registrars under the Registration Act act as office heads for SRO Admin functions | Domain Expert |
| A-10 | SMS gateway used on user create remains available for Kaveri 3.0 credential and alert messages | Ops, Arch |

### 2.4 Constraints

- GIGW / MeitY guidelines, accessibility (WCAG 2.x), Karnataka e-Gov hosting and CERT-In / STQC security norms.
- Aadhaar / biometric usage only as approved by the department and UIDAI compliance.
- Least privilege and jurisdiction scoping are **hard filters**, not advisory UI hiding.
- No silent overwrite of statutory or payment identifiers (DDO code, office short name used in registration number triplet) without dual control.
- Privilege and occupancy changes must not break in-flight Marriage (or other) work-queues without an explicit reassignment rule.
- Bilingual master data (English + Kannada) is mandatory for office type, office name, role and group labels used on screens and certificates.

## 3. Legal and regulatory reference

User Management is not a statutory “form” module in the same sense as Marriage, but it implements the department’s legal ability to **authorise officers**, restrict access to registers and fees, and bind digital signatures to the officer who holds the post.

| Instrument | Topic | BRD relevance |
|------------|--------|----------------|
| Information Technology Act, 2000 | Electronic records, digital / electronic signatures, audit | Login, eSign/DSC binding, immutable logs of privilege change |
| IT (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011 | Security practices, SPDI | Officer PII (photo, ID proof, Aadhaar, biometric, mobile) |
| Aadhaar (Targeted Delivery of Financial and Other Subsidies, Benefits and Services) Act, 2016 and UIDAI circulars | Aadhaar / biometric | Optional biometric thumbs and Aadhaar as ID proof — only if approved |
| Indian Registration Act, 1908 | Appointment and jurisdiction of Registrars / Sub-Registrars | Office master, SR as SRO Admin, jurisdiction ID |
| Karnataka Government servant / KGID practice | Unique employee identity for Government Appointed staff | KGID mandatory for Govt Appointee users |
| Khajane-II / Treasury instructions | Drawing and Disbursing Officer codes | DDO code mandatory on DRO and SRO; passed to payment APIs |
| Government Orders creating / renaming / merging offices and posts | Legal existence of office and post | GO scan mandatory for **new** offices; optional for new posts |
| MeitY / CERT-In / STQC / GIGW | Security, audit, accessibility of e-Gov systems | AuthN, session, MFA, audit export |
| CCA / eSign licensed providers | Digital signature certificates | Bind DSC to active signing post holder; revoke on transfer / relieving |

**Government Order rule (operational):**

| Case | GO upload | System handling |
|------|-----------|-----------------|
| Create office among the existing ~298 migrated offices | Not required at cutover if master is migrated from a signed source | Migration checklist; exception log |
| Create **new** office after cutover | **Mandatory** scan of GO | Hard stop without GO artefact |
| Create / change post | Optional; **Should** attach GO or equivalent order in Kaveri 3.0 | Warning if missing; dual control for new post types |
| Transfer / in-charge / additional charge | Order / proceeding as per department practice | Mandatory supporting document on Transfer and Relieving; Should on In-charge |

## 4. Stakeholders and actors

| Actor | Description | Primary goals | Channel involvement |
|-------|-------------|---------------|---------------------|
| Super Admin (KPMU) | Statewide user administration cell | Create offices, roles, groups, users; grant privileges; break-glass support | Department admin console |
| Department Admin (IGR) | Inspector General of Registration as department super-admin for approvals | Same functional breadth as KPMU for administrative approvals; assign DIGR / AIGR | Department admin console |
| DIGR Admin | DIGR / AIGR mapping users to districts | Map DR / HQA / SR / FDA / SDA / DEO; manage users in assigned span | Department admin console |
| District Admin (DR) | District Registrar, head of district | Map HQA / SR / FDA / SDA / DEO in own jurisdiction; assign SR and DEO to SROs | Department admin console |
| SRO Admin (SR) | Sub-Registrar, head of the SRO | Approve / map FDA, SDA, DEO of that office (see OQ-UM-02) | Department admin console |
| Departmental user | Any officer or staff with a Kaveri login (IGR, DIGR, AIGR, DR, SR, FDA, SDA, DEO, HQA, contract staff, etc.) | Log in, see only authorised menus and jurisdiction data, complete assigned work | Department application |
| Data Entry Operator (DEO) | SRO-office operator (Marriage Offline and scanning) | Appear in allocation lists when occupying an active DEO post at that SRO | Consumed by Marriage / scanning; mastered here |
| CSG / development catalogue admin | Controlled role to add Module / Sub-module / Function metadata | Keep privilege catalogue aligned to deployed functions | Restricted console; change-controlled |
| AIGR Computers | Statewide IT admin (confirm whether a distinct Super-Admin-like role — OQ-UM-01) | Privilege matrix, integrations, break-glass with audit | Department admin console |
| Security / audit reviewer | Internal audit, AG, STQC | Inspect user, privilege and occupancy history | Read-only audit extracts |
| Citizen | Not an actor of this module | — | Out of scope |

**RACI (summary) for key administration steps:**

| Step | KPMU | IGR | DIGR | DR | SR | User |
|------|------|-----|------|----|----|------|
| Create Office Type / statewide Role / Group template | A/R | C | I | I | I | — |
| Create Office (new GO) | A/R | C | I | I | I | — |
| Add Post in an office | R (state) / C | C | C | R (district) | C | — |
| Add User in span of control | R | R | R | R | R (if authorised) | I (SMS) |
| Map Role / Group to functions | A/R | C | I | I | I | — |
| Transfer / Relieving | R/A | C | C | R (own district) | C | I |
| In-charge / additional charge | R | C | C | R | C | I |
| Reset password / unlock | R | R | R (span) | R (span) | R (own office staff, if authorised) | R (self-service OTP, if provided) |
| Bind / revoke DSC | R | C | C | C | I | C (token holder) |

## 5. Definitions and glossary

| Term | Definition | Source |
|------|------------|--------|
| Super Admin (KPMU) | Statewide administrator responsible for creating users, roles, groups and granting privileges across the State | This BRD §4 |
| Department Admin | IGR acting as super-admin for administrative approvals and DIGR / AIGR assignment | This BRD §4 |
| Office Type | Classification of office: IGRO, DRO, SRO, Additional DRO, Additional SRO | This BRD §7.2 |
| Office | A concrete office instance (e.g. SRO Yeshwanthapura, DRO Mysuru) with jurisdiction, DDO (where applicable) and bilingual name | This BRD §7.3 |
| Jurisdiction ID | Parent office identifier that scopes data access (IGRO for DRO; DRO for SRO; self for IGRO) | This BRD §7.3 |
| DDO code | Drawing and Disbursing Officer code used with Khajane-II for that DRO / SRO | This BRD §7.3 |
| Short name | 3-character (rarely 4) office code used in the registration-number triplet | This BRD §7.3 |
| Anywhere Registration | SRO flag; if enabled for one SRO under a DRO, remaining SROs under the same DRO are also enabled (with user message) | This BRD §7.3 |
| Post | Occupiable position in an office, described as Role + Office Name (e.g. FDA SRO Chincholi) | This BRD §7.4 |
| Role | Named job function (IGR, DR, SR, FDA, SDA, DEO, …) to which module functions are mapped | This BRD §7.5 |
| Group | Set of users (e.g. IGR Office, DR Office, SR Office) that can carry privileges; **group privilege overrides role privilege** | This BRD §7.8–7.9 |
| Function | Atomic privilege verb under a module / sub-module (view, print, scan, download, approve, sign, …) | This BRD §7.10 |
| Government Appointed | User type requiring KGID, date of joining and service expiry | This BRD §7.7 |
| Contract | User type without KGID mandate; still requires official email, office, role, ID proof | This BRD §7.7 |
| Login name | Official email ID; duplicates rejected | This BRD §7.7 |
| Is Active | Enable / disable flag for user, role, group or (SRO) office | This BRD |
| Transfer | Movement of a user from one office/post to another, with end date on the old occupancy and start on the new | Programme plan Sr.10; 3.0 addition |
| Relieving | End of occupancy at an office with access cut-off, history retained, DSC unbind if applicable | Programme plan Sr.10; ServiceDesk UM-PP-05 |
| In-charge | Temporary occupancy of a post (typically SR) by another officer without a full transfer | ServiceDesk UM-PP-03; 3.0 addition |
| Additional charge | Concurrent occupancy of more than one post / office | 3.0 addition (OQ-UM-03) |
| Active post holder | User whose occupancy of a post is current (start ≤ today ≤ end or open-ended) and Is Active = Yes | 3.0 |
| DSC binding | Association of a digital signature certificate with the user who currently occupies a signing post | Marriage BRD NFR; UM-PP-04 |

## 6. Current state (As-Is)

### 6.1 As-Is process summary

The current departmental application provides an admin console for User Management. Administrators (typically KPMU / nominated department admins) create office types and offices in hierarchy IGRO → DRO (and Additional DRO) → SRO (and Additional SRO), define posts and roles, map roles (and groups) to modules / sub-modules / functions, and create users with official email as login. On create, a password is generated and login + password are sent by SMS.

As-Is administration is **create / edit / enable-disable** oriented. There is no first-class Transfer, Relieving, In-charge or Additional charge workflow. DSC identity for digital sign is not bound to active post occupancy. Allocation dropdowns in other modules often hold stale or unscoped name lists. SRO Admin powers are inconsistent: some notes say the SR maps FDA / SDA / DEO, while others list only View users / View privileges. A signed privilege matrix is not yet available as a controlled annexure (see OQ-UM-12).

**As-Is systems:**

| System | Role | Pain points |
|--------|------|-------------|
| Existing User Management console | Office, post, role, user, group, mapping screens | Incomplete lifecycle; SMS-only credential; weak jurisdiction enforcement in consuming modules |
| Existing module dropdowns (Firm, 68(2), Digital Sign, Dashboard, etc.) | Allocation and identity display | DEO / in-charge / SR names missing or wrong office |
| Khajane mapping table | DDO codes | SRO code not mapped tickets |
| SMS gateway | Login and password delivery | Login issues; OTP to stale mobile (UM-PP-09) |
| ServiceDesk | Workaround for mapping and user removal | No UM taxonomy; mapping treated as tickets (UM-PP-10) |

### 6.2 As-Is pain points

Evidence from ServiceDesk OverallList and Categorized sheets, summarised in the 24-Aug-2026 Prep Pack. There is **no dedicated User Management subcategory**; defects surface inside Firm, Digital Sign, 68(2), Dashboard, Fruits, Liability and others.

| ID | Pain point | Impact | To-Be address (ref) |
|----|------------|--------|---------------------|
| UM-PP-01 | Repeated departmental “Login issue” (tickets 27806, 28657, 29440, 29765, 30215, 30337, 30342 and others) | Officers cannot work; HO Bangalore and multiple SROs | §7.11, FR-UM-126–145 |
| UM-PP-02 | DEO names not reflecting in DR login allocation dropdown (92889, 91889, 91184, 91030) | Cannot allocate work to valid DEOs | §7.4, §7.7, FR-UM-041, FR-UM-088 |
| UM-PP-03 | In-charge SR names not selectable (78456; 21311 in-charge name not reflecting on summary approve) | Temporary charge not modelled | §7.12, FR-UM-154–160 |
| UM-PP-04 | Current Sub-Registrar name not displayed for digital sign Step 9 (27050, 95322) | Wrong or missing signing identity | §7.13, FR-UM-166–175 |
| UM-PP-05 | User removal / deactivation incomplete (11243 — removal of DEO from SRO Udupi login) | Ex-staff retain or partially retain access | §7.12, FR-UM-146–153 |
| UM-PP-06 | SRO / office code not mapped (24581, 25905, 27404; Fruits theme) | Access and integration failures | §7.3, FR-UM-019–035 |
| UM-PP-07 | Wrong office / district users or queues visible (95242, 86121, 20687) | Data leakage and wrong work | §7.1, FR-UM-007–010 |
| UM-PP-08 | Work allocated to a role but not visible in that login (31958, 30840, 28388, 85826) | Fragile user–role–office assignment vs work-queue identity | §7.7, FR-UM-088, BR-UM-012 |
| UM-PP-09 | OTP not delivered / not verifying for departmental actions (94903, 93570, 91300 and others) | Officer mobile master unreliable | §7.7, FR-UM-075, FR-UM-176 |
| UM-PP-10 | Generic “Mapping issue / Mapping Request” via ServiceDesk (18858, 24367, 31943) | No controlled self-service within admin hierarchy | §7.1, §7.6, FR-UM-009 |

**Related themes that consume User Management:** digital sign popup failures in SR login; FDA/SDA department-login search; Sakala vs SR pendency identity; citizen vs department login confusion. These are not all “create user” defects, but they fail when role, office or identity binding is wrong.

## 7. Future state (To-Be)

> **Source of truth:** this BRD, programme plan Sr.10 (login, transfer, relieving) and ServiceDesk UM-PP-01 to UM-PP-10. Swimlanes for administration are **Admin (in span of control)**, **System**, and **User (subject of the change)**.

### 7.1 Operating model and admin hierarchy

#### 7.1.1 Access model

User Management is a **department-console** module. There is no citizen channel.

| Access model | Who | What they do | MVP? |
|--------------|-----|--------------|------|
| Delegated admin console | KPMU, IGR, DIGR, DR, SR (as authorised) | Masters, users, mapping, transfer / in-charge, reset | Yes |
| Self-service (limited) | Departmental user | Change own password (if enabled), view own profile, raise mapping request inside hierarchy | Should |
| Catalogue admin | Controlled development / AIGR Computers role | Add Module / Sub-module / Function metadata | Yes (change-controlled) |
| Read-only audit | Audit / Security roles | Search audit of user and privilege events | Yes |

**Hierarchy of office creation (mandatory order):** IGRO, then DRO and Additional DRO, then SRO and Additional SRO under the correct parent. Users and posts cannot be created for an office that does not exist or is inactive (except IGRO bootstrap).

#### 7.1.2 Delegated span of control

| Admin role | May act on | Must not act on |
|------------|------------|-----------------|
| Super Admin (KPMU) | All offices, all users, all roles/groups, statewide | Citizen accounts (out of module) |
| Department Admin (IGR) | Same functional set as KPMU for administrative approvals; DIGR / AIGR assignment | Unaudited break-glass without reason code |
| DIGR Admin | DR / HQA / SR / FDA / SDA / DEO mapping in assigned districts | Other DIGR spans; statewide role catalogue (unless granted) |
| District Admin (DR) | HQA / SR / FDA / SDA / DEO in own jurisdiction; assign SR and DEO to SROs in district | Other districts; create statewide roles |
| SRO Admin (SR) | FDA / SDA / DEO of that SRO — **Add/Assign if OQ-UM-02 confirms**; otherwise View only | Other SROs; DR/SR users |

Every admin screen **filters lists and actions** to the caller’s span. A DR login must never list another district’s users (UM-PP-07).

#### 7.1.3 Common admin intake steps

1. **START** — authorised admin opens User Management.
2. **Log on** — departmental authentication (§7.11).
3. **Land on Admin Dashboard** — counts of active users, pending maker-checker items, occupancy gaps (offices with no active SR / DEO).
4. **Select function** — Office Type, Office, Post, Role, User, Group, Mapping, Transfer / Relieving / In-charge, Audit / MIS.
5. **Span filter applied automatically** — office type / office dropdowns show only authorised offices.
6. **Submit** — validations; optional maker-checker; audit event; notify subject user where applicable.

### 7.2 Office Type

#### 7.2.1 Purpose

Create and maintain office types used by Create Office. Types must exist before any office of that type can be created.

#### 7.2.2 Process steps

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Admin selects User Management → Office → Create Office Type | Admin | KPMU / IGR |
| 2 | Office Type ID auto-generated | System | Not user-editable |
| 3 | Enter Office Type (IGRO / DRO / SRO / Additional DRO / Additional SRO or approved extension) | Admin | Unique |
| 4 | Enter Description (English) and Description (Kannada) | Admin | Kannada used for labels |
| 5 | Save and Submit | Admin / System | Duplicate type rejected |
| 6 | Type appears in Create Office dropdown | System | |

View / Edit Office Type shall allow rename of descriptions and enable/disable **only if no active office uses a type being disabled**.

### 7.3 Office

#### 7.3.1 Purpose

Create each office of the Department in hierarchy. Existing offices are migrated; any **new** office other than the existing set requires a Government Order scan.

#### 7.3.2 Process steps

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Admin selects User Management → Office → Add Office | Admin | Span-restricted |
| 2 | Upload Government Order | Admin | Mandatory for new offices after cutover |
| 3 | Select Office Type | Admin | List from §7.2 |
| 4 | Select parent jurisdiction | Admin | SRO: list of DROs; DRO: IGRO; IGRO: self (current office id becomes jurisdiction id) |
| 5 | Enter DDO code | Admin | Mandatory for DRO and SRO; from Khajane mapping for existing offices |
| 6 | Enter Office Name (English), Office Name (Kannada), Short Name (3, rarely 4 characters) | Admin | Short name used in registration triplet — unique |
| 7 | Enter address, phone, district, pin code | Admin | All mandatory |
| 8 | Set Is Active | Admin | Enable/disable **mandatory for SRO** |
| 9 | Set Anywhere Registration (SRO only) | Admin | If enabling one SRO under a DRO, warn that remaining SROs under that DRO will also be enabled |
| 10 | Save and Submit | System | Success message; office available for posts and users |

**Jurisdiction cases:**

- **Case 1 — SRO:** Select DRO; that DRO’s office id becomes the SRO’s jurisdiction id (e.g. SRO Yeshwanthapura under DRO Rajajinagar).
- **Case 2 — IGRO:** No parent selection; current office id is jurisdiction id.
- **Case 3 — DRO:** Jurisdiction is IGRO; DDO code mandatory.

Office short name and DDO code changes after go-live require dual control because they affect registration numbers and payments (UM-PP-06).

### 7.4 Post

#### 7.4.1 Purpose

Describe the number and type of posts in each office. Posts are the occupancy slots that users fill. Allocation dropdowns (DEO, SR, in-charge) **read active occupancy of posts**, not free-text names.

#### 7.4.2 Process steps

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Admin selects User Management → Office → Add Post | Admin | |
| 2 | Upload GO to create new post | Admin | Optional; Should in Kaveri 3.0 |
| 3 | Post ID auto-generated | System | |
| 4 | Select Office Type, then Office Name | Admin | Offices listed under selected type / district |
| 5 | Select Role | Admin | e.g. FDA, SDA, DEO, SR |
| 6 | Post Description auto-generated as Role + Office Name | System | e.g. FDA SRO Chincholi; editable only with reason |
| 7 | Save and Submit | System | |

An office may have multiple posts of the same role (e.g. two DEO posts). Vacant posts are visible on the dashboard as occupancy gaps.

### 7.5 Role

#### 7.5.1 Purpose

Maintain the catalogue of roles used on posts and users. Example names: IGR; DIGR Law & Administration / Audit / Intelligence / Vigilance / CVC / Enforcement; AIGR Computers / Administration / Audit; Law Officer; Accounts Superintendent; Superintendent Audit; Statistical Inspector; SR Administration / SR Computers; FDA; SDA; DR; SR; plus DEO and HQA as used in admin sections.

#### 7.5.2 Add Role — process steps

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Department admin opens User Management → Role → Add Role | Admin | Typically KPMU / IGR |
| 2 | Role ID auto-generated | System | |
| 3 | Enter Role Name and short description | Admin | Unique name |
| 4 | Set Is Active | Admin | Enable / disable |
| 5 | Save and Submit | System | |

#### 7.5.3 View / Edit Role — process steps

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Admin opens View / Edit Roles | Admin | Lists all roles in span |
| 2 | Choose Edit on a row | Admin | Available only if caller’s mapping allows |
| 3 | Role Name and Is Active editable | Admin | Disable blocked if active posts/users still use the role (or require reassignment first) |
| 4 | Update and Submit | System | Audit; or cancel returns to list |

### 7.6 Map Role to Modules / Sub-modules / Functions

This is the core RBAC function that governs privileges.

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Admin selects Role → Map Role to Module / Sub-module / Function | Admin | KPMU / IGR; dual control recommended |
| 2 | Select Role | Admin | |
| 3 | System shows existing privileges | System | Tree: Module → Sub-module → Functions |
| 4 | Edit: add or remove mappings | Admin | Refer rebuilt annexure (Appendix C seed + signed matrix) |
| 5 | Save and Submit | System | Maker-checker (FR-UM-191); effective on next login or session refresh |

Effective privilege for a user = **union of Role mappings**, then **Group mappings override** where a group mapping exists for the same function (BR-UM-008; confirm OQ-UM-06).

### 7.7 User lifecycle

#### 7.7.1 Add User — process steps

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Admin selects User Management → User → Add User | Admin | Span of control |
| 2 | Select User Type: Government Appointed or Contract | Admin | |
| 3 | Select Role | Admin | Mandatory; drives default post suggestions |
| 4 | Enter KGID | Admin | Mandatory for Government Appointed; unique |
| 5 | Enter Official Email ID (login name) | System | Duplicate login rejected (“user exists”) |
| 6 | Assign Office; jurisdiction id derived | System | SRO users: data access restricted to that office id; jurisdiction-scoped roles: restricted to jurisdiction id |
| 7 | Optionally assign Post (occupancy) | Admin | Required for SR / DEO / FDA / SDA used in allocation (Must for those roles) |
| 8 | First, Middle, Last name (First mandatory) | Admin | |
| 9 | Phone (mobile) — validated format; used for SMS and OTP | Admin | Must be unique per active user or dual-control exception |
| 10 | Date of joining and Service expiry | Admin | Government Appointed only |
| 11 | ID proof type, number (format-validated), upload scan | Admin | Mandatory; types in Appendix C |
| 12 | PAN (optional); if entered, verify via PAN API | System | |
| 13 | Biometric authentication required? If yes, capture both thumb impressions | Admin | Only if department/UIDAI-approved |
| 14 | Capture user photo | Admin | |
| 15 | Set Is Active (default Enable) | Admin | |
| 16 | Save and Submit | System | Generate password; SMS login name + password; email if gateway available |
| 17 | Force password change on first login | System | In addition to SMS of generated password |

#### 7.7.2 View / Edit User — process steps

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Admin selects View / Edit User | Admin | |
| 2 | Filter by Office Type: IGRO = all department users (if authorised); DRO = that DRO + child SRO users; SRO = that SRO only | System | Per §7.7.2 |
| 3 | Open user; Edit if privilege allows | Admin | |
| 4 | Name fields locked | System | Correction via controlled “name change” with ID proof (Should) |
| 5 | Phone, Role, Is Active, Post occupancy editable | Admin | Role / office change in 3.0 should prefer Transfer workflow rather than silent edit |
| 6 | Update and Submit | System | Audit; session invalidation if role/office/active changed |

### 7.8 Group

#### 7.8.1 Create Group

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Admin selects User → Create Group | Admin | |
| 2 | Group ID auto-generated | System | |
| 3 | Group Name (e.g. IGR Office / DR Office / SR Office) and description | Admin | Name mandatory |
| 4 | Assign Role(s) to the Group | Admin | Mandatory |
| 5 | Is Active — enable/disable if not assigned to users | Admin | |
| 6 | Save and Submit | System | Refer annexure for intended group templates |

#### 7.8.2 View / Edit Group

List all groups in span; Edit allows Group Name, Description, Roles, Is Active (if mapping privilege exists); Update and Submit; Cancel returns to list.

### 7.9 Map Group to Modules / Sub-modules / Functions

Group-to-function mapping remains a **controlled admin** function with the same tree UI as role mapping.

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Admin selects Map Group to Module / Sub-module / Function | Admin | |
| 2 | Select Group; view existing privileges | System | |
| 3 | Edit mappings; Save and Submit | Admin | **Group privilege overrides Role privilege** (BR-UM-008) |

### 7.10 Module / Sub-module / Function catalogue

Maintained so RBAC has a stable catalogue. Examples: Modules = MIS Reports, CVC, Document Registration, User Management, Dashboard; Sub-modules e.g. Statutory Reports; Functions e.g. View, Print, Download.

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Catalogue admin selects Add Module / Sub-module / Function | Catalogue admin | Not a field SR |
| 2 | Enter ID and Name; select parent Module / Sub-module for functions | Admin | Duplicate ID/name rejected with details shown |
| 3 | Save and Submit | System | Available immediately for mapping but production mapping still dual-controlled |

Phase 1 catalogue **Must** include User Management functions plus Marriage (Online/Offline), CC, scanning, Khajane payment operations, Marriage dashboard/MIS, and admin audit/export.

### 7.11 Authentication, password and session

The As-Is model only issues SMS of a generated password on create. Kaveri 3.0 **Must** close UM-PP-01.

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | User enters login name (official email) and password | User | Alternative identifiers if OQ-UM-04 decides |
| 2 | System validates active user, occupancy, not relieved, not expiry-lapsed | System | Government Appointee past service expiry → block with message |
| 3 | Optional MFA / OTP to verified mobile | System | Privileged roles (KPMU, IGR, mapping admins) Should use MFA |
| 4 | Session issued with claims: user id, roles, groups, office id, jurisdiction id, posts | System | Consumed by all modules |
| 5 | Forgot password / unlock | User or Admin | OTP to verified mobile / email; admin reset in span; lockout after N failures |
| 6 | Password change | User | First-login force change; complexity policy |

Failed logins, lockouts and resets are audited. Helpdesk must not need a mapping ticket for simple unlock (UM-PP-10).

### 7.12 Transfer, relieving, in-charge and additional charge

These workflows are **new versus As-Is** and are Phase 1 Must (programme Sr.10).

#### 7.12.1 Transfer

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Admin (in span) starts Transfer | Admin | Select user |
| 2 | Upload transfer order | Admin | Mandatory |
| 3 | Set relieving date/time on current post/office | Admin | |
| 4 | Select new Office, Role, Post | Admin | New office in admin’s span or routed to receiving admin (Should) |
| 5 | Maker-checker approve | Checker | |
| 6 | On effective date: old occupancy ended; new occupancy started; sessions invalidated; DSC unbound from old signing post; work-queue identity updated | System | History retained (DM-P1-02) |
| 7 | Notify user (SMS/email) | System | |

#### 7.12.2 Relieving / deactivation

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Admin starts Relieving (or Disable with relieve reason) | Admin | Addresses UM-PP-05 |
| 2 | Capture last working date, reason, order upload | Admin | |
| 3 | On effective date: Is Active = Disable; office unmapped for access; privileges ineffective; DSC revoked/unbound; user disappears from allocation dropdowns | System | Record retained; login blocked |
| 4 | Notify user and office head | System | |

Disable without relieving date is allowed for immediate security suspension, with mandatory reason code.

#### 7.12.3 In-charge and additional charge

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Admin assigns In-charge or Additional charge to a **post** (typically SR) | Admin | Addresses UM-PP-03 |
| 2 | From / To dates, order upload | Admin | To may be open until revoked |
| 3 | System treats the assignee as **active post holder** for that post for allocation, digital sign name, and SR queues, in addition to or instead of the regular holder per rule BR-UM-018 | System | |
| 4 | Expiry or revoke removes the person from in-charge dropdowns immediately | System | |

### 7.13 DSC and officer identity binding

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | For each signing post (minimum: Sub-Registrar), bind DSC / eSign certificate serial to the **active post holder** | Admin / System | Addresses UM-PP-04 |
| 2 | Digital-sign screens resolve **legal name and certificate** from UM occupancy, not from a stale local cache | Consuming module | Marriage FR-HMA digital sign depends on this |
| 3 | On transfer, relieving, or in-charge change: unbind old, bind new; block sign if no valid binding | System | |
| 4 | Expiry monitoring and alerts to KPMU / office head | System | Should |

DEO must never receive approve / register / sign functions (Marriage NFR-HMA-SEC-011 enforced via this catalogue).

### 7.14 Status models

#### 7.14.1 User account status

| Status | Description | Actor | Next states |
|--------|-------------|-------|-------------|
| Draft | Add User saved not submitted | Admin | Pending checker / Active |
| Pending checker | Awaiting maker-checker | Checker | Active / Rejected |
| Active | Is Active = Enable; occupancy current | System | Locked / Suspended / Relieved / Transferred |
| Locked | Failed logins exceeded | System / Admin | Active (unlock) |
| Suspended | Immediate disable, reason captured | Admin | Active / Relieved |
| Password expired / first-login | Must change password | User | Active |
| Relieved | Occupancy ended; login blocked | Admin | Closed (historical) |
| Transferred | Old occupancy ended; new occupancy Active at new office | System | Active (new) |
| Closed | Terminal historical record | System | — |

#### 7.14.2 Post occupancy status

| Status | Description | Next states |
|--------|-------------|-------------|
| Vacant | No current holder | Occupied / In-charge assigned |
| Occupied | Regular holder current | Vacant (relieve) / Transfer pending / In-charge overlay |
| In-charge assigned | Temporary holder current | Occupied / Vacant |
| Additional charge | Holder also occupies another post | Occupied / Vacant |

#### 7.14.3 Office status

| Status | Description |
|--------|-------------|
| Active | Available for users, posts, transactions |
| Inactive | SRO (or other) disabled; no new transactions; existing users blocked or read-only per rule |

### 7.15 Process changes versus As-Is

| # | Change vs As-Is | Impact |
|---|---------------------|--------|
| C-01 | First-class **Transfer / Relieving** with effective date, GO, access cut-off and history | Closes UM-PP-05; migration entity DM-P1-02 |
| C-02 | **In-charge / additional charge** occupancy | Closes UM-PP-03; SR queues and digital sign |
| C-03 | **Password reset, unlock, first-login change, session claims, optional MFA** | Closes UM-PP-01 |
| C-04 | **DSC binding** to active post holder | Closes UM-PP-04; Marriage certificate signing |
| C-05 | Allocation and MIS **must read active occupancy** from UM | Closes UM-PP-02 / UM-PP-08 |
| C-06 | **Hard jurisdiction filter** on every admin list and as claims for all modules | Closes UM-PP-07 |
| C-07 | **Maker-checker + immutable audit** on user, mapping, transfer, privilege | Not in the current admin console; required for Kaveri 3.0 compliance |
| C-08 | Verified unique **mobile** with update path | Closes UM-PP-09 |
| C-09 | Resolve SR Admin **View-only vs Add/Map** contradiction | OQ-UM-02; Appendix B |
| C-10 | Maintain **privilege matrix** as a controlled annexure | Sign before UAT (OQ-UM-12) |
| C-11 | Mandatory GO for **new** offices; unique short name and DDO validation | Closes UM-PP-06 |
| C-12 | Force consuming modules (Marriage DEO console, digital sign, DR allocation) to use UM APIs — no local officer name lists | Architecture / HLD follow-on |

## 8. Functional requirements

> **Convention:** Req ID `FR-UM-###`. Priority: Must / Should / Could. Trace to this BRD, programme plan or ServiceDesk in the RTM.

### 8.1 Delegated administration and span of control

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-001 | System shall implement admin roles Super Admin (KPMU), Department Admin (IGR), DIGR Admin, District Admin (DR), SRO Admin (SR) | Must | Each role can be assigned; menus match Appendix B |
| FR-UM-002 | Super Admin shall create users, roles, groups and grant privileges statewide | Must | KPMU user completes Add User / Role / Group / Mapping for any office |
| FR-UM-003 | Department Admin (IGR) shall perform the same administration actions as KPMU for administrative approvals and shall assign DIGR / AIGR roles | Must | IGR can assign DIGR/AIGR; actions audited as IGR not KPMU |
| FR-UM-004 | DIGR Admin shall map DR / HQA / SR / FDA / SDA / DEO within assigned districts | Must | Attempt to map a user in an unassigned district is blocked |
| FR-UM-005 | District Admin shall map HQA / SR / FDA / SDA / DEO in own jurisdiction and assign SR and DEO to SROs in that district | Must | Other-district offices do not appear |
| FR-UM-006 | SRO Admin actions on FDA / SDA / DEO shall follow the signed Appendix B (View only **or** Add/Assign — OQ-UM-02) | Must | Automated tests for both configured variants until decision is frozen |
| FR-UM-007 | All lists, searches, dropdowns and APIs shall **hard-filter** by caller office id and jurisdiction id | Must | Cross-jurisdiction record never returned (UM-PP-07) |
| FR-UM-008 | SRO-scoped users shall access transactional data only for their Office ID | Must | Direct API call with another office id returns 403 |
| FR-UM-009 | Mapping and user changes in span shall be completable in the console without a ServiceDesk ticket | Should | Happy-path Add User / Map Role / Transfer has no “raise ticket” mandatory step |
| FR-UM-010 | Admin Dashboard shall show occupancy gaps (office with no active SR or no active DEO) in span | Should | Gap list matches post occupancy |

### 8.2 Office Type

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-011 | System shall create Office Types IGRO, DRO, SRO, Additional DRO, Additional SRO | Must | All five selectable in Add Office |
| FR-UM-012 | Office Type ID shall be auto-generated and not editable | Must | |
| FR-UM-013 | Office Type name plus English and Kannada descriptions shall be captured | Must | Kannada description renders on Kannada UI |
| FR-UM-014 | Duplicate office type name shall be rejected | Must | |
| FR-UM-015 | Disable of an office type shall be blocked while active offices of that type exist | Must | |
| FR-UM-016 | Only Super Admin / Department Admin shall create or disable office types | Must | DR/SR cannot open Create Office Type |

### 8.3 Office

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-019 | Offices shall be created only after parent hierarchy exists (IGRO then DRO then SRO) | Must | Creating SRO without DRO blocked |
| FR-UM-020 | New offices after cutover shall require Government Order upload | Must | Submit without GO fails |
| FR-UM-021 | Office Type dropdown shall list types from §8.2; jurisdiction prompt depends on type | Must | Cases 1–3 in §7.3.2 |
| FR-UM-022 | DDO code shall be mandatory for DRO and SRO; sourced from Khajane mapping for migrated offices | Must | Save without DDO fails for DRO/SRO; IGRO may omit |
| FR-UM-023 | Office Name English, Office Name Kannada, Short Name, address, phone, district, pin code shall be mandatory | Must | |
| FR-UM-024 | Short name shall be 3 characters (4 allowed only as a rare documented exception) and unique among active offices | Must | Duplicate short name rejected |
| FR-UM-025 | Is Active enable/disable shall be mandatory for SRO | Must | |
| FR-UM-026 | Anywhere Registration shall apply only to SRO; enabling one SRO under a DRO shall warn that remaining SROs under that DRO will be enabled and shall apply the flag consistently | Must | Warning shown; sibling SROs updated per confirmed rule |
| FR-UM-027 | Success message shall display on create | Must | |
| FR-UM-028 | Change of short name or DDO after go-live shall require dual control | Must | Single-user change rejected |
| FR-UM-029 | Inactive SRO shall not appear in new-application office selection in consuming modules | Must | Marriage office list excludes inactive SRO |
| FR-UM-030 | Office search by name, district, short name, DDO shall be provided in span | Should | |

### 8.4 Post

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-036 | Admin shall create posts per office with Office Type, Office Name, Role | Must | |
| FR-UM-037 | Post ID shall be auto-generated | Must | |
| FR-UM-038 | Post Description shall default to Role + Office Name | Must | e.g. FDA SRO Chincholi |
| FR-UM-039 | GO upload for new post shall be supported and optional; warning if missing | Should | |
| FR-UM-040 | Multiple posts of the same role in one office shall be allowed | Must | Two DEO posts at one SRO |
| FR-UM-041 | Allocation dropdowns in other modules shall list **active occupants of posts**, not static names | Must | Vacant DEO post does not show a name; occupied post shows current user (UM-PP-02) |
| FR-UM-042 | Vacant posts shall be reportable on dashboard | Should | |

### 8.5 Role

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-046 | Admin shall add Role with auto ID, name, description, Is Active | Must | Seed roles in Appendix C creatable |
| FR-UM-047 | View / Edit Role shall list roles and allow edit of name and Is Active per privilege | Must | |
| FR-UM-048 | Disable Role shall be blocked (or require reassignment) while users or posts still use it | Must | |
| FR-UM-049 | DEO, SR, FDA, SDA, DR, IGR, HQA shall exist as first-class roles for Phase 1 | Must | Marriage DEO console authorises DEO role only |

### 8.6 Map Role to Modules / Sub-modules / Functions

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-056 | Admin shall map a selected role to Module / Sub-module / Function with add and remove | Must | Tree UI; save persists |
| FR-UM-057 | System shall display existing privileges before edit | Must | |
| FR-UM-058 | Functions shall include at least View, Add, Edit, Print, Scan, Download, Approve, Sign as applicable per module | Must | DEO cannot be granted Approve or Sign |
| FR-UM-059 | Mapping changes shall take effect on next login or bounded session refresh | Must | No stale menu after re-login |
| FR-UM-060 | Mapping shall be restricted to Super Admin / Department Admin unless a signed exception exists | Must | DR cannot grant statewide Sign |
| FR-UM-061 | Privilege matrix import / export (annexure) shall be supported for controlled load | Should | CSV/XLSX round-trip of mappings |

### 8.7 Add User

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-066 | Admin shall create departmental users in span of control | Must | Out-of-span office rejected |
| FR-UM-067 | User Type Government Appointed or Contract shall be mandatory | Must | |
| FR-UM-068 | Role shall be mandatory | Must | |
| FR-UM-069 | KGID shall be mandatory and unique for Government Appointed | Must | Contract may omit; duplicate KGID rejected |
| FR-UM-070 | Official email shall be login name, mandatory, unique; if exists show “user exists” | Must | Case-insensitive unique |
| FR-UM-071 | Office assignment shall set jurisdiction id automatically | Must | |
| FR-UM-072 | First Name mandatory; Middle optional; Last optional | Must | |
| FR-UM-073 | Phone / mobile mandatory, format-validated | Must | |
| FR-UM-074 | Date of joining and service expiry captured for Government Appointed | Must | Login blocked after expiry date |
| FR-UM-075 | Mobile used for OTP shall be the verified number on the user record; update path provided | Must | OTP after mobile change uses new number only (UM-PP-09) |
| FR-UM-076 | ID proof type, number (standard format validation) and scan upload mandatory | Must | Types per Appendix C |
| FR-UM-077 | PAN optional; if entered, verify via PAN API before save | Should | Failed PAN verification blocks save or flags for override |
| FR-UM-078 | Optional biometric both thumbs if “biometric required” is Yes | Could | Only if legally approved |
| FR-UM-079 | Capture user photo | Must | |
| FR-UM-080 | Is Active default Enable | Must | |
| FR-UM-081 | On successful create, generate password and send login + password by SMS | Must | SMS logged (not the password in clear in MIS) |
| FR-UM-082 | First login shall require password change | Must | Old generated password cannot be reused as the new password |
| FR-UM-083 | SR, DEO, FDA, SDA users used in allocation shall be assigned an explicit Post occupancy | Must | Save without post blocked for these roles |
| FR-UM-084 | Contract users shall not require KGID, joining or expiry | Must | Other mandatory fields still apply |

### 8.8 View / Edit User

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-091 | IGRO filter (authorised) lists all department users; DRO lists DRO + child SRO users; SRO lists that SRO only | Must | Counts match office tree |
| FR-UM-092 | Edit button only if caller has privilege | Must | |
| FR-UM-093 | First / Middle / Last name not editable on standard Edit | Must | |
| FR-UM-094 | Phone, Role ID, Is Active editable on standard Edit | Must | Name remains locked |
| FR-UM-095 | Office or role change that moves jurisdiction shall be performed via Transfer, not silent Edit | Must | Edit rejects office change with message to use Transfer |
| FR-UM-096 | Deactivate (Is Active = Disable) without relieving shall require reason code | Must | |
| FR-UM-097 | Controlled name-correction with ID proof re-upload | Should | Audit of old/new name |

### 8.9 Group

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-101 | Create Group with auto ID, name, description, assigned role(s), Is Active | Must | Name mandatory; role mandatory |
| FR-UM-102 | View / Edit Group: name, description, roles, Is Active editable per privilege | Must | |
| FR-UM-103 | Disable Group blocked while assigned to users, or users must be unassigned first | Must | |
| FR-UM-104 | Users can be assigned to one or more groups | Must | |
| FR-UM-105 | Map Group to Module / Sub-module / Function with same tree behaviour as role mapping | Must | |
| FR-UM-106 | Where both role and group map the same function, **group privilege shall override role privilege** | Must | Test: role allows View, group denies View → user denied, unless OQ-UM-06 reverses the rule |

### 8.10 Module / Sub-module / Function catalogue

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-116 | Catalogue admin shall add Module with ID and name; duplicate rejected with existing details shown | Must | |
| FR-UM-117 | Add Sub-module under a Module; duplicate rejected | Must | |
| FR-UM-118 | Add Function under Module and Sub-module; duplicate rejected | Must | |
| FR-UM-119 | Field admins (DR/SR) shall not add catalogue entries | Must | Menu hidden |
| FR-UM-120 | Phase 1 catalogue shall include User Management, Marriage, CC, Scanning, Payment, Marriage Dashboard/MIS, Audit export | Must | Mapping screens list these modules |

### 8.11 Authentication, password, lock and session

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-126 | System shall authenticate departmental users by official email and password (unless SSO decided) | Must | Inactive / relieved user cannot login |
| FR-UM-127 | Session shall carry user id, roles, groups, office id, jurisdiction id, active posts | Must | JWT/session inspected in API tests |
| FR-UM-128 | Lock account after configurable consecutive failures | Must | Unlock by admin in span or OTP self-service |
| FR-UM-129 | Admin in span shall reset password and unlock | Must | SMS/email of reset outcome, not the new password in ticket notes |
| FR-UM-130 | Self-service forgot-password via OTP to verified mobile and/or email | Must | OTP not sent to unverified or old number |
| FR-UM-131 | Password complexity, history and expiry policy configurable | Must | Policy documented in NFR/security design |
| FR-UM-132 | Privileged roles (KPMU, IGR, role-mapping admins) shall support MFA | Should | MFA challenge on login |
| FR-UM-133 | Concurrent session limit configurable; transfer/relieve/disable shall terminate sessions | Must | Relieved user cookie rejected |
| FR-UM-134 | Login, logout, failure, lock, unlock, reset shall be audited | Must | |

### 8.12 Transfer, relieving, in-charge, additional charge

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-146 | Transfer shall capture user, from office/post, to office/post/role, effective date/time, order upload | Must | |
| FR-UM-147 | On effective time, old occupancy ends, new occupancy starts, sessions end, allocation lists update | Must | DEO no longer in old SRO dropdown; appears in new |
| FR-UM-148 | Relieving shall capture last date, reason, order; disable login; unmap office access; retain history | Must | UM-PP-05: user gone from old office login lists |
| FR-UM-149 | Immediate suspend without waiting for last working date, with reason | Must | Security incident path |
| FR-UM-150 | Full occupancy history queryable (from/to, office, post, role, order ref) | Must | DM-P1-02 depth |
| FR-UM-154 | In-charge assignment to a post with from/to dates and order | Must | In-charge SR appears in DR selection (UM-PP-03) |
| FR-UM-155 | While in-charge is active, consuming modules treat assignee as active post holder for that post | Must | Digital sign name and SR queue use in-charge person per BR-UM-018 |
| FR-UM-156 | In-charge expiry or revoke removes assignee from dropdowns immediately | Must | |
| FR-UM-157 | Additional charge: user occupies more than one post concurrently with explicit records | Should | Session claims include all active posts |
| FR-UM-158 | Maker-checker on Transfer, Relieving, In-charge | Must | Single user cannot approve own request |

### 8.13 DSC and identity binding

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-166 | System shall bind DSC / eSign certificate serial and subject DN to a user occupying a signing post | Must | |
| FR-UM-167 | Digital-sign consumers shall resolve current SR legal name and certificate from UM | Must | Step 9 shows current SR (UM-PP-04) |
| FR-UM-168 | Unbind on transfer, relieving, or in-charge end; block sign if no valid binding | Must | |
| FR-UM-169 | Alert on certificate expiry before N days | Should | |
| FR-UM-170 | DEO role shall not be grantable Approve, Register or Sign functions | Must | Mapping save rejected |

### 8.14 Notifications

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-176 | SMS (and email if available) on user create with login name | Must | Password via SMS; not echoed in UI after first display |
| FR-UM-177 | Notify on password reset, lock, unlock, transfer, relieving, in-charge, privilege mapping change | Should | EN + KN templates |
| FR-UM-178 | Notify office head when occupancy gap appears (no SR / no DEO) | Could | |

### 8.15 Reports and MIS

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-183 | Report: users by office / role / status in span | Must | |
| FR-UM-184 | Report: vacant posts and in-charge assignments | Must | |
| FR-UM-185 | Report: transfers and relievings in a date range | Must | |
| FR-UM-186 | Report: privileged mapping changes | Must | |
| FR-UM-187 | Export in CSV/PDF within span; no bulk PII dump without authorised role | Must | |
| FR-UM-188 | Recommend ServiceDesk taxonomy category “User Management” with subcategories Login, Mapping, Transfer, In-charge, DSC | Should | Operational, not a system function of UM itself |

### 8.16 Audit and dual control

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FR-UM-191 | Maker-checker (or dual control) for Add User, Role mapping, Group mapping, Transfer, Relieving, In-charge, Office DDO/short-name change | Must | |
| FR-UM-192 | Immutable audit: who, when, before/after, reason, artefact (GO) id | Must | Append-only |
| FR-UM-193 | Audit export for departmental / AG / STQC review | Must | |
| FR-UM-194 | Super Admin break-glass actions require reason code and are highlighted in MIS | Must | |

## 9. Business rules

| Rule ID | Description | Source | System enforcement |
|---------|-------------|--------|-------------------|
| BR-UM-001 | Office hierarchy is IGRO → DRO (and Additional DRO) → SRO (and Additional SRO) | This BRD §7.2–7.3 | Hard stop |
| BR-UM-002 | Data access is restricted by Office ID for SRO users and by Jurisdiction ID for district-scoped roles | This BRD §7.7 | Hard filter on UI and API |
| BR-UM-003 | Official email is unique login name | This BRD §7.7 | Reject duplicate |
| BR-UM-004 | KGID is mandatory and unique for Government Appointed users | This BRD §7.7 | Hard stop |
| BR-UM-005 | DDO code is mandatory for DRO and SRO | This BRD §7.3 | Hard stop |
| BR-UM-006 | New office (non-migrated) requires Government Order | This BRD §7.3 | Hard stop |
| BR-UM-007 | Is Active controls enable/disable of user, role, group; SRO office disable is explicit | This BRD | Login and dropdowns honour flags |
| BR-UM-008 | Group privilege overrides role privilege for the same function | This BRD §7.9 | Evaluation order: group then role |
| BR-UM-009 | Anywhere Registration enabled on one SRO under a DRO implies remaining SROs under that DRO (with message) | This BRD §7.3 | Coordinated update + warning |
| BR-UM-010 | Short name is unique and used in registration triplet — change is dual-controlled | This BRD §7.3; UM-PP-06 | Dual control |
| BR-UM-011 | Name on standard user edit is locked | This BRD §7.7.2 | Fields read-only |
| BR-UM-012 | Work allocation and digital-sign identity use **active post occupancy**, not disconnected name lists | UM-PP-02/04/08 | API contract |
| BR-UM-013 | Relieved or deactivated users disappear from office logins and allocation lists at effective time | UM-PP-05 | Occupancy end |
| BR-UM-014 | Office/role jurisdiction moves use Transfer, not silent Edit | 3.0 | Hard stop on Edit |
| BR-UM-015 | Login blocked if user inactive, locked, relieved, or Government Appointee past service expiry | This BRD | AuthN |
| BR-UM-016 | Privilege mapping and user create in production require maker-checker | 3.0 | Workflow |
| BR-UM-017 | DEO cannot approve, register or digitally sign | Marriage NFR | Mapping validation |
| BR-UM-018 | In-charge holder is the signing / queue identity for that post while the in-charge record is current | UM-PP-03/04 | Occupancy resolver |
| BR-UM-019 | DSC is bound only to the active signing post holder; unsigned if unbound | UM-PP-04 | Sign gate |
| BR-UM-020 | Admins act only inside span of control | This BRD Appendix B | 403 outside span |
| BR-UM-021 | First login must change SMS-issued password | 3.0 / UM-PP-01 | AuthN |
| BR-UM-022 | OTP for departmental actions uses verified mobile on the user master | UM-PP-09 | OTP service |
| BR-UM-023 | Catalogue add is restricted to controlled catalogue-admin role | This BRD §7.10 | RBAC |
| BR-UM-024 | Disable of role/group/type blocked while in use | This BRD | Referential check |
| BR-UM-025 | Kannada labels for office type, office, role and group are taken from master Kannada fields | This BRD | UI |

## 10. User interface (high-level)

| Screen / step | Purpose | Actor | Notes |
|---------------|---------|-------|-------|
| Department login | Authenticate; MFA if required | User | §7.11 |
| First-login password change | Replace SMS password | User | FR-UM-082 |
| Forgot password / unlock | OTP reset | User | FR-UM-130 |
| Admin Dashboard | Span counts, occupancy gaps, pending checker | Admin | FR-UM-010 |
| Create / list Office Type | Master | KPMU / IGR | This BRD §7.2 |
| Add / list Office | Hierarchy, GO, DDO, anywhere registration | KPMU / IGR | This BRD §7.3 |
| Add Post | Role + office occupancy slot | Admin in span | This BRD §7.4 |
| Add / View / Edit Role | Role catalogue | KPMU / IGR | This BRD §7.5 |
| Map Role to functions | RBAC tree | KPMU / IGR | This BRD §7.6 |
| Add User | Full form incl. Govt vs Contract, photo, ID | Admin in span | This BRD §7.7 |
| View / Edit User | Filter IGRO/DRO/SRO | Admin in span | This BRD §7.7.2 |
| Create / View / Edit Group | Group master | KPMU / IGR | This BRD §7.8 |
| Map Group to functions | Override tree | KPMU / IGR | This BRD §7.9 |
| Add Module / Sub-module / Function | Catalogue | Catalogue admin | This BRD §7.10 |
| Transfer | From/to occupancy | Admin | §7.12.1 |
| Relieving / Suspend | Access cut-off | Admin | §7.12.2 |
| In-charge / Additional charge | Temporary occupancy | Admin | §7.12.3 |
| DSC binding | Certificate to post holder | KPMU / authorised | §7.13 |
| Maker-checker inbox | Approve admin requests | Checker | FR-UM-191 |
| Audit search / export | Who/when/what | Audit role | FR-UM-193 |
| MIS reports | Users, vacancies, transfers | Admin in span | §8.15 |
| Own profile | View; limited self-update of phone with verification | User | Should |

**Wireframe links:** Prototype URLs TBD. Kaveri 3.0 UX shall include Transfer, Relieving, In-charge, DSC bind, checker inbox and occupancy dashboard in addition to office, post, role, user, group and mapping screens.

**Bilingual:** All labels `[EN / KN]` — content manager sign-off. Kannada values for office and role come from masters, not free-typed at runtime.

## 11. Integrations

| Integration | Direction | Purpose | Owner | Status |
|-------------|-----------|---------|-------|--------|
| Khajane-II / DDO mapping table | Inbound | DDO codes for DRO/SRO; payment office identity | Treasury / Arch | Existing department rule |
| SMS gateway | Outbound | Login credentials, OTP, transfer/relieve alerts | Ops | Existing; harden |
| Email gateway | Outbound | Official login notices and checker alerts | Ops | TBD |
| PAN verification API | Outbound | Optional PAN check on Add User | Integration | Optional |
| Aadhaar / eKYC / biometric devices | Outbound / device | Optional thumbs and Aadhaar ID proof | Security / Legal | TBD approval |
| DSC / eSign provider | Inbound metadata | Certificate serial, expiry, revoke | Security | 3.0 Must bind |
| State SSO / Seva Sindhu | Outbound/Inbound | If OQ-UM-04 selects SSO | Security | Decision pending |
| HRMS (if any) | Inbound | Optional KGID / transfer order feed | PO | Not assumed |
| Consuming modules (Marriage, CC, Scanning, MIS, payment) | API provide | Session claims, occupancy, office master, privilege check | Arch | Must; no local name lists |
| ServiceDesk | Outbound optional | Ticket only for exceptions outside span | Ops | Reduce UM-PP-10 |
| Audit / SIEM | Outbound | Auth and privilege events | Security | Should |

**Interface requirements:** Architect shall publish User Management APIs for: authenticate/session, get user, list occupants by office+role, get office/jurisdiction, check function permission, occupancy history. Marriage DEO console and SR digital sign are the first consumers.

## 12. Data requirements

### 12.1 Core entities (logical)

- **OfficeType** — code, name EN/KN, active.
- **Office** — type, parent/jurisdiction, DDO, names EN/KN, short name, address, phone, district, pin, active, anywhere-registration, GO artefact.
- **Role** — name, description, active.
- **Post** — office, role, description, active, GO artefact.
- **User** — type (Govt/Contract), KGID, login email, names, phone (verified), joining, expiry, ID proof, PAN, photo, biometric refs, active, status.
- **Occupancy** — user, post, office, role, kind (regular / in-charge / additional), valid from/to, order artefact.
- **Group**, **UserGroup**.
- **Module**, **SubModule**, **Function**.
- **RolePrivilege**, **GroupPrivilege**.
- **Credential** — password hash, MFA factors, lock state (no clear password storage).
- **DscBinding** — user, post, certificate serial, valid from/to.
- **AdminRequest** — maker-checker payload for user/mapping/transfer.
- **AuditEvent** — append-only.

### 12.2 Retention

| Data class | Retention |
|------------|-----------|
| User, occupancy, transfer/relieve history | Permanent for departmental audit / AG (align Legal); not purged because of in-flight register integrity |
| ID proof images, photo, biometric templates | Per SPDI / UIDAI / department policy — TBD Legal (OQ-UM-14) |
| Password hashes, session logs | Security policy — TBD |
| Audit of privilege and login | Not less than security / AG requirement — TBD; default 7 years unless Legal specifies otherwise |
| SMS content of passwords | Must not be stored in application MIS; gateway logs per Ops policy |

### 12.3 Migration (high level)

| Topic | Question for migration workstream |
|-------|-----------------------------------|
| DM-P1-01 | Office / SRO / district masters from the legacy application — volume, duplicate short names, missing DDO |
| DM-P1-02 | Users, roles, transfer/relieving history — agreed depth; password re-issue vs hash migrate |
| Privilege matrix | Build from a signed privilege matrix or extract of live production mappings |
| In-flight occupancies | Who is in-charge SR on cutover day |
| DSC | Re-bind certificates to migrated SR users before Marriage UAT |
| Orphans | Users without office, duplicate emails, duplicate KGID — exception register |

## 13. Requirements traceability matrix (RTM) - template

| Req ID | Act/Rule/Form | Requirement summary | BRD section | UI screen | Test case ID | Status |
|--------|---------------|---------------------|-------------|-----------|--------------|--------|
| FR-UM-001 | This BRD §8.1 | Admin hierarchy KPMU / IGR / DIGR / DR / SR | 8.1 | Admin Dashboard | TC-UM-___ | Draft |
| FR-UM-007 | This BRD §7.7; UM-PP-07 | Hard jurisdiction filter | 8.1 | All admin lists | TC-UM-___ | Draft |
| FR-UM-019 | This BRD §7.3 | Office hierarchy IGRO→DRO→SRO | 8.3 | Add Office | TC-UM-___ | Draft |
| FR-UM-020 | This BRD §7.3 | GO mandatory for new office | 8.3 | Add Office | TC-UM-___ | Draft |
| FR-UM-022 | This BRD §7.3; Khajane | DDO mandatory DRO/SRO | 8.3 | Add Office | TC-UM-___ | Draft |
| FR-UM-026 | This BRD §7.3 | Anywhere Registration sibling warning | 8.3 | Add Office | TC-UM-___ | Draft |
| FR-UM-041 | UM-PP-02 | Allocation reads active occupancy | 8.4 | Consuming dropdowns | TC-UM-___ | Draft |
| FR-UM-056 | This BRD §7.6 | Map role to functions | 8.6 | Map Role | TC-UM-___ | Draft |
| FR-UM-066 | This BRD §7.7 | Add User in span | 8.7 | Add User | TC-UM-___ | Draft |
| FR-UM-069 | This BRD §7.7 | KGID mandatory Govt Appointee | 8.7 | Add User | TC-UM-___ | Draft |
| FR-UM-070 | This BRD §7.7 | Unique official email login | 8.7 | Add User | TC-UM-___ | Draft |
| FR-UM-081 | This BRD §7.7 | SMS login and password on create | 8.7 | Add User | TC-UM-___ | Draft |
| FR-UM-091 | This BRD §7.7.2 | View users by IGRO/DRO/SRO filter | 8.8 | View/Edit User | TC-UM-___ | Draft |
| FR-UM-106 | This BRD §7.9 | Group privilege overrides role | 8.9 | Map Group | TC-UM-___ | Draft |
| FR-UM-126 | UM-PP-01; Sr.10 | Departmental login | 8.11 | Login | TC-UM-___ | Draft |
| FR-UM-130 | UM-PP-01 | Self-service reset / unlock | 8.11 | Forgot password | TC-UM-___ | Draft |
| FR-UM-146 | Programme Sr.10 | Transfer occupancy | 8.12 | Transfer | TC-UM-___ | Draft |
| FR-UM-148 | UM-PP-05; Sr.10 | Relieving access cut-off | 8.12 | Relieving | TC-UM-___ | Draft |
| FR-UM-154 | UM-PP-03 | In-charge assignment | 8.12 | In-charge | TC-UM-___ | Draft |
| FR-UM-167 | UM-PP-04; Marriage DSC | Sign identity from UM occupancy | 8.13 | DSC binding / SR sign | TC-UM-___ | Draft |
| FR-UM-170 | Marriage NFR-HMA-SEC-011 | DEO cannot sign/approve | 8.13 | Map Role | TC-UM-___ | Draft |
| FR-UM-191 | 3.0 compliance | Maker-checker on privilege and user | 8.16 | Checker inbox | TC-UM-___ | Draft |
| BR-UM-008 | This BRD §9 | Group overrides role | 9 | Map Group | TC-UM-___ | Draft |
| BR-UM-012 | UM-PP-02/08 | Occupancy is source of allocation identity | 9 | APIs | TC-UM-___ | Draft |

## 14. Acceptance and sign-off

| Role | Name | Signature / Date | Comments |
|------|------|------------------|----------|
| Product Owner | Prashanth | | |
| Domain Expert | Prabhakar Naik | | |
| IGR nominee | | | |
| AIGR Computers / Kaveri IT Cell | | | |
| Business Analyst | Nandha Kumar | | |
| Security reviewer | | | |

**UAT scope:** Test scenarios derived from FR-UM-* covering: office hierarchy and GO; add user (Govt and Contract); span filters; role and group mapping including override; login / lock / reset; transfer and relieving including dropdown disappearance; in-charge visibility; DSC name on digital sign; DEO cannot sign; maker-checker; audit export. Include negative tests for cross-jurisdiction API access.

**Phase 1 go-live gate (from programme plan):** User Management login / transfer / relieving operational, with Marriage Online/Offline roles (SR, DEO) bound to occupancy.

## Appendix A — References

- BR Discussion Prep Pack — User Management (24 August 2026) — `Requirement Discussions/BR_Discussion_Prep_Pack_User_Management_24Aug2026.docx`
- ServiceDesk issues — `Requirement Discussions/ServiceDesk Issues/ServiceDeskIssuesList.xlsx` (OverallList, Categorized)
- Project Plan Kaveri 3.0 Programme v0.4 — User Management Sr.10–11; Phase 1 Must; DM-P1-02
- Marriage BRD v1.6 (section pattern and consuming RBAC/DSC needs) — `Finalized BRD/Marriage/RFP/BRD_Marriage_v1.6.docx`
- Signed role / group / module privilege matrix — to be completed before UAT (OQ-UM-12)
- Information Technology Act, 2000; Aadhaar Act, 2016; Indian Registration Act, 1908; MeitY / CERT-In / STQC / GIGW guidance
- Khajane-II DDO mapping (department / treasury source)

## Appendix B — Delegated administration action matrix

Proposed delegated actions for Kaveri 3.0. Cells: Y = allowed in span; N = not allowed; C = confirm (OQ-UM-02).

| Action | KPMU Super Admin | IGR Dept Admin | DIGR Admin | DR District Admin | SR SRO Admin |
|--------|------------------|----------------|------------|-------------------|--------------|
| View list of users | Y | Y | Y (span) | Y (jurisdiction) | Y (own SRO FDA/SDA/DEO) |
| View user privileges | Y | Y | Y | Y | Y |
| Add users | Y | Y | Y | Y | C |
| Deactivate / relieve users | Y | Y | Y | Y | C |
| Change role of users | Y | Y | Y | Y (assign roles in span) | C |
| Change group of users | Y | Y | Y | N unless granted | N |
| Change user privileges (ad hoc) | Y | Y | Y | N | N |
| Assign groups | Y | Y | Y | Y (span groups) | N |
| Assign roles / posts | Y | Y | Y | Y | C (FDA/SDA/DEO) |
| View Group / Role | Y | Y | Y | Y (read) | Y (read) |
| Edit / Add Group | Y | Y | N (view only for DIGR unless granted) | N | N |
| Edit / Add Role | Y | Y | N | N | N |
| Map Role/Group to functions | Y | Y | N | N | N |
| Create Office Type / Office | Y | Y | N | N | N |
| Add Post | Y | Y | C | Y (own district) | N |
| Transfer / In-charge | Y | Y | Y (span) | Y (jurisdiction) | N |
| DSC bind | Y | C | N | N | N |
| Catalogue add module/function | Catalogue admin / KPMU | N | N | N | N |

DIGR is treated as view-only for Group/Role catalogue edits. SRO Admin is View users / View privileges unless OQ-UM-02 confirms Add/Assign for FDA/SDA/DEO — **freeze via OQ-UM-02**.

## Appendix C — Seed office types, roles and ID-proof types

**Office types:** IGRO; DRO; SRO; Additional DRO; Additional SRO.

**Seed roles (including Phase 1 consumers):** Super Admin (KPMU); IGR; DIGR Law & Administration; DIGR Audit; DIGR Intelligence; DIGR Vigilance; DIGR CVC; DIGR Enforcement; AIGR Computers; AIGR Administration; AIGR Audit; Law Officer; Accounts Superintendent; Superintendent Audit; Statistical Inspector; District Registrar (DR); Head of Accounting (HQA); Sub-Registrar (SR); SR Administration; SR Computers; FDA; SDA; DEO; Catalogue Admin.

**ID proof types:** PAN; Passport; Driving licence; Bank pass book; Matriculation certificate; Degree of a recognised educational institution; Ration card; Aadhaar Number; Voter ID (EPIC). Validate number format per type.

**User types:** Government Appointed; Contract.

**Group templates:** IGR Office; DR Office; SR Office.

## Appendix D — Open questions and decision log

### D.1 Open questions

Carried from Prep Pack DQ-01…DQ-12 and BRD drafting. Close or park with owner before UAT freeze.

| Q ID | Question | Options / notes | Needed from | Due |
|------|----------|-----------------|-------------|-----|
| OQ-UM-01 | Retain admin hierarchy (KPMU / IGR / DIGR / DR / SR) for Kaveri 3.0? Add AIGR Computers as statewide IT admin? | Keep as-is / simplify / add AIGR Computers | PO, IGR | |
| OQ-UM-02 | What can SR Admin do — only view, or also add/map FDA–SDA–DEO? | Resolve Appendix B contradiction | PO, Domain Expert | |
| OQ-UM-03 | Transfer, Relieving, In-charge, Additional charge: UM workflows vs HRMS vs KPMU ticket? | Recommend native UM workflows (this BRD) | PO | |
| OQ-UM-04 | Login identity: official email only, or KGID / mobile / State SSO? | Impacts UM-PP-01 and OTP | Security, PO | |
| OQ-UM-05 | Password / unlock / reset: self-service vs admin vs SMS OTP? | This BRD assumes both self-service OTP and admin reset | Security | |
| OQ-UM-06 | Group privilege override of Role — keep, reverse, or remove groups? | This BRD proposes group overrides role | PO, Security | |
| OQ-UM-07 | Is DEO a Role, a Post, or both? | This BRD: both; allocation uses occupancy | PO, DE | |
| OQ-UM-08 | DSC binding rules when in-charge changes mid-day? | Effective-time vs next-login | Security, DE | |
| OQ-UM-09 | Jurisdiction enforcement on **all** modules at Phase 1 or phased? | Recommend hard filter on all APIs from day one | Arch, PO | |
| OQ-UM-10 | Maker-checker for Super Admin’s own changes? | Dual Super Admin or after-the-fact audit only | Security | |
| OQ-UM-11 | Scope: departmental UM only, or citizen account lifecycle in this BRD? | This BRD: departmental only | PO | |
| OQ-UM-12 | Maintain a signed privilege matrix as a controlled annexure? | Required before UAT | BA, AIGR Computers | |
| OQ-UM-13 | Anywhere Registration: auto-enable all sibling SROs or only warn? | This BRD proposes message + enable remaining | DE, PO | |
| OQ-UM-14 | Retention of ID proof images, photo, biometrics | Legal / DPDP / UIDAI | Legal | |
| OQ-UM-15 | Password migrate vs forced reset at cutover for all officers | Security vs field disruption | Security, Ops | |

### D.2 Decisions

| Dec ID | Decision | Date | Approver | Impact |
|--------|----------|------|----------|--------|
| DEC-UM-001 | Phase 1 User Management = departmental identity spine (login, roles, office mapping, transfer, relieving, RBAC) | Programme plan v0.4 | Steering / PO | This BRD scope |
| DEC-UM-002 | Office type, office, post, role, user, group, mapping and catalogue functions are **in scope** as baseline | Draft | PO (to confirm) | §7.2–7.10 |
| DEC-UM-003 | Transfer, Relieving, In-charge, DSC binding, reset/unlock, maker-checker, occupancy APIs are **added** for 3.0 | Draft | PO (to confirm) | §7.11–7.13 |
| DEC-UM-004 | Citizen authentication is out of this BRD unless promoted | Draft | PO (OQ-UM-11) | §2.2 |

*End of BRD — replace remaining open questions through the 24–25 August 2026 User Management workshops and Domain Expert review.*
