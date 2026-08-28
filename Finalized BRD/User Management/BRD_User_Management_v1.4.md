# Business Requirements Document (BRD)

## User Management & Role-Based Access Control (RBAC) Module

## Document control

| Field | Value |
|--------|--------|
| **Document ID** | BRD-K2-UM-001 |
| **Version** | 1.4 |
| **Status** | Draft / In review |
| **Project** | KAVERI 2.0 — Department of Stamps and Registration (DSR), Government of Karnataka |
| **Module** | User Management & Role-Based Access Control (RBAC) |
| **Legal basis (primary)** | Information Technology Act, 2000; Indian Registration Act, 1908 (appointment of Registrars / Sub-Registrars); Aadhaar Act, 2016 (where biometric / Aadhaar is used) |
| **State / govt rules (primary)** | Karnataka e-Governance hosting and security norms; MeitY / CERT-In / STQC / GIGW; Government Orders for office and post creation |
| **Related inputs** | Requirement Discussions/BR_Discussion_Prep_Pack_User_Management_24Aug2026.docx; Requirement Discussions/Kaveri2.0/User Management KAVERI 2.0_v0.3.pdf; Finalized BRD/Marriage/RFP/BRD_Marriage_v1.9.docx (section pattern source) |
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
| 1.4 | 2026-08-28 | Nandha Kumar | Recast for KAVERI 2.0: passwordless OTP/Captcha/Biometric authentication; primary/secondary role model with session role selection; DSR organizational hierarchy; automated joining/relieving letters; dynamic role creation and hierarchy configuration; daily login MIS | Prashanth |

**Distribution:** Kaveri BRD workspace (Finalized BRD/User Management)

**Related documents:**

| ID | Title | Link |
|----|--------|------|
| BRD-K2-UM-001 | This document | Finalized BRD/User Management/BRD_User_Management_v1.4.docx |
| PREP-K2-UM-001 | BR Discussion Prep Pack — User Management | Requirement Discussions/BR_Discussion_Prep_Pack_User_Management_24Aug2026.docx |
| BRD-K3-MRG-001 | Marriage Registration BRD (section pattern source) | Finalized BRD/Marriage/RFP/BRD_Marriage_v1.9.docx |
| RTM-K2-UM-001 | Requirements traceability matrix | Section 13 of this document |

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
- 7.1 Organizational hierarchy and role mapping
- 7.2 User onboarding and lifecycle management
- 7.3 Role-Based Access Control and session management
- 7.4 Authentication and credential management
- 7.5 System administration and configuration
- 7.6 Automated letter generation
- 7.7 Reporting and MIS
- 7.8 Status models
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
- Appendix B — DSR organizational hierarchy (seed roles)
- Appendix C — Open questions and decision log

## 1. Executive summary

This Business Requirements Document defines the business requirements for the **User Management & Role-Based Access Control (RBAC)** module within the **KAVERI 2.0** ecosystem for the Department of Stamps and Registration (DSR), Government of Karnataka.

The module manages the **lifecycle, authentication, authorization, and hierarchy mapping** of all internal departmental users based on the approved organizational structure of DSR. It is the **central departmental login, role and office control used by all KAVERI 2.0 modules**.

**Key capabilities (KAVERI 2.0):**

- Instant creation, modification, and lifecycle management of departmental user accounts — **no multi-level approval** for base profile creation.
- Mapping of users to the predefined DSR organizational hierarchy (IGR through divisional DIGR / AIGR / HQA / SRO / FDA / SDA roles).
- **Dynamic RBAC** supporting **Primary Role** (substantive post, no end date), **Secondary Roles** (mandatory end date, auto-expiry), and **session-based role selection / switching**.
- **Passwordless authentication** using User ID, OTP, Captcha, and optional Biometrics — traditional passwords are removed.
- Automated generation of official **Joining** and **Relieving** letters using department templates.
- System administration, hierarchy configuration, reporting, and immutable audit of all user-management actions.

**Success criteria (measurable):**

- Departmental users authenticate without passwords and receive menus solely from the selected session role.
- Primary and secondary role assignments, including future-dated changes, take effect automatically on the configured date.
- Secondary role access is removed automatically on end-date expiry without manual intervention.
- Daily login MIS shows user count and active session roles.
- All role changes, letter generation, and authentication events are fully auditable.

**Module boundary:** This BRD specifies departmental User Management for KAVERI 2.0. Citizen portal registration and citizen eKYC account lifecycle are **out of this BRD** unless the Product Owner promotes them.

## 2. Scope

### 2.1 In scope (User Management & RBAC)

- Instant creation, modification, and lifecycle management of departmental user accounts.
- Mapping of users to the predefined DSR organizational hierarchy.
- Dynamic Role-Based Access Control (RBAC) supporting primary, secondary, and session-based role switching.
- Passwordless authentication using OTP, Captcha, and Biometrics.
- Automated generation of joining and relieving letters.
- System administration, reporting, and hierarchy configuration.
- Super Admin capabilities: dynamic role creation, role abbreviation capture, hierarchy level configuration, and peer/subordinate role-editing permission toggle.
- Daily login reports segmented by active session role.
- Immutable audit of all user-management actions (timestamp, IP address, actor ID).

### 2.2 Out of scope (unless PO promotes)

- Citizen portal registration, citizen password self-service, and citizen eKYC account lifecycle.
- HRMS / payroll as the system of record for appointment, pay, and leave (this module records **application access** occupancy, not the full HR file).
- Physical access control, CCTV, or non-Kaveri applications.
- Replacement of CCA / eSign provider operations (this BRD binds certificates to active post holders where applicable).
- Fine-grained privilege matrices for modules not yet designed — catalogue entries may be created in advance; function mapping is completed as each consuming module is specified.

### 2.3 Assumptions

| ID | Assumption | Owner to validate |
|----|------------|-------------------|
| A-01 | The DSR organizational chart provided in this BRD is the authoritative hierarchy for role mapping | Domain Expert, IGR |
| A-02 | **User ID** (official departmental identifier / email) is the login identifier for passwordless authentication | Security, PO |
| A-03 | OTP is delivered to the user's registered mobile and/or official email | Ops, Arch |
| A-04 | Biometric capture devices and UIDAI / department approvals are in place before biometric login is enabled | Security, Legal |
| A-05 | Official letter templates for Joining and Relieving are provided and signed by the department before UAT | Domain Expert |
| A-06 | Super Admin (KPMU / IGR nominee) is responsible for dynamic role creation and hierarchy configuration | PO |
| A-07 | Consuming modules (Marriage, Document Registration, etc.) read session role and privilege claims from this module | Arch |

### 2.4 Constraints

- GIGW / MeitY guidelines, accessibility (WCAG 2.x), Karnataka e-Gov hosting and CERT-In / STQC security norms.
- Aadhaar / biometric usage only as approved by the department and UIDAI compliance.
- **No password-based authentication** — the traditional password option is removed from KAVERI 2.0.
- Least privilege and hierarchy scoping are **hard filters**, not advisory UI hiding.
- OTP delivery must complete within **5 seconds** of request (NFR-UM-02).
- Biometric data must be re-registered every **5 years** (REQ-UM-013).

## 3. Legal and regulatory reference

User Management implements the department's legal ability to **authorise officers**, restrict access to registers and fees, and bind digital signatures to the officer who holds the post.

| Instrument | Topic | BRD relevance |
|------------|--------|----------------|
| Information Technology Act, 2000 | Electronic records, digital / electronic signatures, audit | Passwordless login, eSign/DSC binding, immutable logs |
| IT (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011 | Security practices, SPDI | Officer PII (photo, ID proof, Aadhaar, biometric, mobile) |
| Aadhaar Act, 2016 and UIDAI circulars | Aadhaar / biometric | Biometric authentication — only if approved |
| Indian Registration Act, 1908 | Appointment and jurisdiction of Registrars / Sub-Registrars | Office master, SR role, jurisdiction |
| Karnataka Government servant / KGID practice | Unique employee identity | KGID for Government Appointed staff |
| MeitY / CERT-In / STQC / GIGW | Security, audit, accessibility | AuthN, session, audit export |
| Government Orders creating / renaming / merging offices and posts | Legal existence of office and post | GO scan for new offices; approval letters for role changes |

## 4. Stakeholders and actors

| Actor | Description | Primary goals | Channel involvement |
|-------|-------------|---------------|---------------------|
| Inspector General of Registration (IGR) | Top management; head of DSR | Department-wide oversight; approve primary role changes | Department admin console |
| DIGR (division heads) | Division 1–6 heads (Admin/Law/Computers, Vigilance, Computers, Enforcement, Intelligence & Audit, CVC) | Manage users and roles within division span | Department admin console |
| AIGR / HQA / SRO / FDA / SDA | Divisional and field officers and staff | Perform assigned functions under selected session role | Department application |
| Super Admin | Statewide user administration cell (KPMU / IGR nominee) | Create roles, configure hierarchy, manage users statewide | Department admin console |
| Departmental user | Any officer or staff with a Kaveri login | Log in (passwordless), select session role, complete assigned work | Department application |
| Security / audit reviewer | Internal audit, AG, STQC | Inspect user, privilege and occupancy history | Read-only audit extracts |
| Citizen | Not an actor of this module | — | Out of scope |

**RACI (summary) for key administration steps:**

| Step | Super Admin | IGR | DIGR | DR / SRO | User |
|------|-------------|-----|------|----------|------|
| Create user (instant) | A/R | C | C | C | I |
| Assign Primary Role | A/R | C | C | C | I |
| Assign Secondary Role (with approval letter) | A/R | C | C | C | I |
| Change Primary Role (with reason + approval letter) | A/R | C | C | — | I |
| Configure role hierarchy | A/R | C | I | I | — |
| Create new role (dynamic) | A/R | C | I | I | — |
| Toggle peer/subordinate role-editing permission | A/R | C | I | I | — |
| Passwordless login | — | — | — | — | R |
| Session role selection / switch | — | — | — | — | R |

## 5. Definitions and glossary

| Term | Definition | Source |
|------|------------|--------|
| User ID | Unique departmental login identifier (typically official email or KGID-based ID) used for passwordless authentication | REQ-UM-011 |
| Primary Role | The user's substantive post; assigned at account creation; **cannot** have an end date | REQ-UM-002 |
| Secondary Role | Any additional role beyond the Primary Role; **must** have a mandatory end date; auto-removed on expiry | REQ-UM-003 |
| Session Role | The role selected by the user after login for the current session; drives menus and permissions | REQ-UM-007 |
| Role Switching | Changing the active session role without logging out | REQ-UM-008 |
| Approval Letter | Official document uploaded when granting a secondary role or changing a primary role | REQ-UM-004, REQ-UM-005 |
| Effective Date | Future date on which a role change (joining / relieving) is automatically applied | REQ-UM-006 |
| Super Admin | Administrator with ability to create roles, configure hierarchy, and toggle peer/subordinate editing permissions | REQ-UM-009, REQ-UM-014 |
| Role Abbreviation / Acronym | Short form of a role displayed throughout the UI (dashboards, audit logs, headers) | REQ-UM-015, REQ-UM-016 |
| Hierarchy Level | Position of a role in the reporting structure (who reports to whom) | REQ-UM-017 |
| Joining Letter | Auto-generated official letter when a user assumes a new role or location | REQ-UM-018 |
| Relieving Letter | Auto-generated official letter when a user vacates a role or location | REQ-UM-018 |
| Passwordless Authentication | Login using User ID + OTP + Captcha (and optionally Biometrics); no password | REQ-UM-010, REQ-UM-011 |
| Biometric Re-registration | Mandatory update of biometric data every 5 years | REQ-UM-013 |

## 6. Current state (As-Is)

### 6.1 As-Is process summary

The current departmental application provides an admin console for User Management. Administrators create users with official email as login and issue passwords via SMS. Role assignment is single-role oriented without a formal primary/secondary distinction or mandatory end dates for temporary assignments. There is no session-based role selection — users operate under a single assigned role. Authentication is password-based with OTP as a secondary factor in some flows. Joining and relieving letters are prepared offline. Role hierarchy configuration is static and cannot be dynamically extended by Super Admins.

### 6.2 As-Is pain points

| ID | Pain point | Impact | To-Be address (ref) |
|----|------------|--------|---------------------|
| UM-PP-01 | Repeated departmental login issues (password reset, lockout, stale credentials) | Officers cannot work | §7.4, REQ-UM-010–011 |
| UM-PP-02 | No distinction between substantive post and temporary additional charge | Access persists after charge ends | REQ-UM-002, REQ-UM-003 |
| UM-PP-03 | Officers with multiple roles cannot switch context without separate logins | Wrong menus and permissions | REQ-UM-007, REQ-UM-008 |
| UM-PP-04 | Joining / relieving letters prepared manually offline | Administrative delay | REQ-UM-018, REQ-UM-019 |
| UM-PP-05 | Role hierarchy not aligned to current DSR org chart | Incorrect reporting and span of control | §7.1, REQ-UM-017 |
| UM-PP-06 | No daily login report segmented by active role | Limited operational visibility | REQ-UM-020, REQ-UM-021 |
| UM-PP-07 | Biometric data not refreshed on a schedule | Stale biometric templates | REQ-UM-012, REQ-UM-013 |

## 7. Future state (To-Be)

> **Source of truth:** this BRD, DSR organizational chart, and KAVERI 2.0 programme requirements. Swimlanes: **Admin**, **System**, **User**.

### 7.1 Organizational hierarchy and role mapping

Based on the official DSR Organization Chart, the system must support the following hierarchical mapping and associated user roles:

| Division | Roles |
|----------|-------|
| **Top Management** | Inspector General of Registration & Commissioner of Stamps (IGR) |
| **Division 1 (Admin, Law & Computers)** | DIGR (Admin, Law & Computers), AIGR (Admin), HQA (Admin), SRO (Admin), FDA, SDA |
| **Division 2 (Vigilance)** | DIGR (Vigilance), Law Officer, HQA (RTI) |
| **Division 3 (Computers)** | AIGR (Computers), System Integrator, PMU, Application Developer, SRO (Comp) |
| **Division 4 (Enforcement)** | DIGR (Enforcement), District Registrar (DRO), HQA, Sub Registrar (SRO), FDA, SDA |
| **Division 5 (Intelligence & Audit)** | DIGR (Intelligence), AIGR (Audit), HQA (Audit), Superintendent (Audit) |
| **Division 6 (CVC)** | DIGR CVC, JD Town Planning |

Super Admins shall configure the **hierarchy level** of all roles (reporting relationships) via the administration console (REQ-UM-017). Role abbreviations and acronyms shall be displayed throughout the application UI (REQ-UM-016).

#### 7.1.1 Hierarchy configuration — process steps

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Super Admin opens User Management → Hierarchy Configuration | Admin | |
| 2 | System displays current role hierarchy tree | System | Based on DSR org chart seed (Appendix B) |
| 3 | Admin sets / adjusts reporting level for each role | Admin | Who reports to whom |
| 4 | Save and Submit | System | Audit event; effective immediately or on configured date |

### 7.2 User onboarding and lifecycle management

#### 7.2.1 Instant account creation

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Authorised admin opens User Management → Add User | Admin | No multi-level approval for base profile (REQ-UM-001) |
| 2 | Enter user particulars (name, User ID, mobile, email, KGID if applicable, photo, ID proof) | Admin | |
| 3 | Assign **Primary Role** (mandatory) | Admin | Primary Role cannot have an end date (REQ-UM-002) |
| 4 | Optionally assign **Secondary Role(s)** with mandatory end date and approval letter upload | Admin | REQ-UM-003, REQ-UM-004 |
| 5 | Optionally set **future effective date** for role assignment | Admin | REQ-UM-006 |
| 6 | Save — account created instantly | System | User can authenticate once active |

#### 7.2.2 Primary role modification

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Admin selects user → Change Primary Role | Admin | Promotion, transfer, or demotion |
| 2 | Enter reason for change | Admin | Mandatory (REQ-UM-005) |
| 3 | Upload / capture approval letter | Admin | Mandatory (REQ-UM-005) |
| 4 | Set effective date (immediate or future) | Admin | REQ-UM-006 |
| 5 | System applies change on effective date; generates Joining / Relieving letter | System | REQ-UM-018 |

#### 7.2.3 Secondary role expiry

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Secondary role end date reached | System | Scheduled job |
| 2 | System automatically removes secondary role access | System | REQ-UM-003 |
| 3 | Audit event logged | System | NFR-UM-01 |
| 4 | User notified (if configured) | System | |

### 7.3 Role-Based Access Control and session management

#### 7.3.1 Session role selection

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | User completes passwordless login | User / System | §7.4 |
| 2 | If user has multiple assigned roles, system presents role list | System | REQ-UM-007 |
| 3 | User selects desired role for this session | User | |
| 4 | System updates menus, activities, and permissions dynamically | System | Based on selected session role |

#### 7.3.2 Dynamic role switching

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | User clicks Role Switch in active session | User | REQ-UM-008 |
| 2 | System presents list of currently assigned roles | System | Primary + active secondary only |
| 3 | User selects new session role | User | No logout required |
| 4 | Menus and permissions update immediately | System | Audit of role switch |

#### 7.3.3 Peer / subordinate role editing

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Super Admin configures peer/subordinate role-editing permission per role | Admin | REQ-UM-009 |
| 2 | Toggle enable / disable for each role | Admin | Super Admin only |
| 3 | Elevated roles with permission enabled can edit roles/permissions of peers or subordinates | Admin | Within hierarchy span |

### 7.4 Authentication and credential management

#### 7.4.1 Standard passwordless login flow

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | User enters User ID | User | REQ-UM-011 |
| 2 | System displays Captcha challenge | System | REQ-UM-011 |
| 3 | User completes Captcha | User | |
| 4 | User requests OTP | User | |
| 5 | System dispatches OTP to registered device / email within 5 seconds | System | NFR-UM-02 |
| 6 | User enters OTP | User | |
| 7 | System validates User ID + OTP + Captcha — all three must match | System | REQ-UM-011 |
| 8 | Access granted; proceed to session role selection (§7.3.1) | System | No password option (REQ-UM-010) |

#### 7.4.2 Biometric authentication

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | User selects Biometric Login | User | REQ-UM-012 |
| 2 | System captures and verifies biometric | User / Device | |
| 3 | On success, proceed to session role selection | System | |
| 4 | If biometric data older than 5 years, prompt re-registration | System | REQ-UM-013 |
| 5 | User re-registers biometrics before login proceeds | User | Mandatory if expired |

### 7.5 System administration and configuration

#### 7.5.1 Dynamic role creation

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Super Admin opens User Management → Role → Add Role | Admin | REQ-UM-014 |
| 2 | Enter Role Name, Abbreviation, and Acronym | Admin | REQ-UM-015 |
| 3 | Set hierarchy level and reporting relationship | Admin | REQ-UM-017 |
| 4 | Set Is Active | Admin | |
| 5 | Save — role available for assignment | System | Unlimited new roles (REQ-UM-014) |

### 7.6 Automated letter generation

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Role or location change triggered (primary change, transfer, relieving) | System | REQ-UM-018 |
| 2 | System selects official letter template (Joining or Relieving) | System | REQ-UM-019 |
| 3 | Auto-populate user details, effective dates, role abbreviations | System | REQ-UM-019 |
| 4 | Generate letter in-app for review / download / print | System | Reduces offline admin activity |
| 5 | Letter stored with audit reference | System | NFR-UM-01 |

### 7.7 Reporting and MIS

| # | Step | Lane | Notes |
|---|------|------|-------|
| 1 | Authorised admin opens Reports → Daily Login Report | Admin | REQ-UM-020 |
| 2 | Select date (default: today) | Admin | |
| 3 | System generates report: total users logged in, segmented by active session role | System | REQ-UM-021 |
| 4 | Export CSV / PDF | Admin | Span-restricted |

### 7.8 Status models

#### 7.8.1 User account status

| Status | Description | Actor | Next states |
|--------|-------------|-------|-------------|
| Draft | User profile saved, not yet active | Admin | Active |
| Active | User can authenticate and select session role | System | Suspended / Relieved |
| Suspended | Immediate disable with reason | Admin | Active / Relieved |
| Pending future role change | Future-dated primary or secondary change scheduled | System | Active (on effective date) |
| Relieved | User vacated role; login blocked | Admin | Closed (historical) |
| Closed | Terminal historical record | System | — |

#### 7.8.2 Role assignment status

| Status | Description | Next states |
|--------|-------------|-------------|
| Active (Primary) | Current substantive post; no end date | Changed (primary modification) |
| Active (Secondary) | Additional role with end date | Expired / Revoked |
| Scheduled | Future-dated assignment pending | Active / Cancelled |
| Expired | Secondary role end date passed; access removed | — |
| Revoked | Admin manually removed before end date | — |

## 8. Functional requirements

> **Convention:** Req ID `REQ-UM-###` (as specified). Priority: Must / Should / Could.

### 8.1 User onboarding and lifecycle management

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| REQ-UM-001 | User account creation shall happen instantly in the system. No multi-level approval process is required to create the base user profile | Must | Admin creates user; account active immediately without checker workflow |
| REQ-UM-002 | A Primary Role must be assigned to the user during account creation. The Primary Role acts as the user's substantive post and **cannot** have an end date | Must | Save without Primary Role fails; end-date field disabled for Primary Role |
| REQ-UM-003 | Any additional roles assigned to a user will be treated as Secondary Roles. All Secondary Roles **must** have a mandatory end date. After the end date expires, the secondary role access must be automatically removed from the user's account | Must | Secondary role without end date rejected; expired role not in session role list |
| REQ-UM-004 | The system must provide a provision to upload/capture an official approval letter whenever an additional (secondary) role is granted to a user | Must | Save secondary role without approval letter fails |
| REQ-UM-005 | Primary role access can be changed at any time in the future (due to promotion, office transfer, or demotion). The system must capture the specific reason for the change and require the upload/capture of an approval letter to process this change | Must | Primary change without reason or letter blocked; audit captures reason |
| REQ-UM-006 | The system shall provide a provision to configure effective dates for role changes (joining/relieving) in the future. The system will automatically apply the change on the specified date | Must | Future-dated change applied by scheduler on effective date; letter generated |

### 8.2 Role-Based Access Control (RBAC) and session management

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| REQ-UM-007 | Once successfully logged in, users with multiple roles shall be presented with a list of their assigned roles. The user must select their desired role for that session. The system's actions, activities, and menus must update dynamically based on the selected role | Must | Multi-role user sees role picker; menus match selected role |
| REQ-UM-008 | Users must be able to switch between any of their currently assigned roles seamlessly at any point during their active session without needing to log out and log back in | Must | Role switch updates menus without re-authentication |
| REQ-UM-009 | Certain elevated roles shall have the capability to edit the roles/permissions of their peers or subordinates. The system must include a toggle (enable/disable) for super admins to explicitly grant or revoke this specific permission for any given role | Must | Toggle per role; elevated role edits only when enabled and within span |

### 8.3 Authentication and credential management

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| REQ-UM-010 | The traditional password option shall be completely removed from the application | Must | No password field on login; password reset screens removed |
| REQ-UM-011 | Users will authenticate using their User ID, an OTP (One-Time Password) sent to their registered device/email, and a Captcha. Access is granted only when the User ID, OTP, and Captcha match successfully | Must | All three required; any mismatch blocks login |
| REQ-UM-012 | Departmental users shall have the option to log in using biometric authentication | Must | Biometric login path available on login screen |
| REQ-UM-013 | The system must enforce a mandatory updating of the user's biometric authentication data every five (5) years. Users exceeding this limit must be prompted to re-register their biometrics | Must | Login blocked until re-registration when biometric age > 5 years |

### 8.4 System administration and configuration

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| REQ-UM-014 | Roles must be an additive option. Super Admins shall have the ability to create and add an unlimited number of new roles as needed by the department | Must | Super Admin creates new role; no hard limit |
| REQ-UM-015 | When creating or editing a role, the system must capture the Role Name, Abbreviation, and Acronym | Must | All three fields mandatory on role create/edit |
| REQ-UM-016 | The role abbreviation/acronym shall be displayed throughout the application's user interface (e.g., dashboards, audit logs, headers) wherever necessary for quick identification | Must | Abbreviation visible in dashboard header and audit log entries |
| REQ-UM-017 | Super Admins must have the provision to define and set the specific hierarchy level of all roles (e.g., establishing who reports to whom) across the system | Must | Hierarchy tree editable; reporting relationship persisted |

### 8.5 Automated letter generation

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| REQ-UM-018 | To reduce offline administrative activity, the application must automatically generate official Relieving and Joining letters when a user's role or location changes | Must | Letter generated in-app on role/location change |
| REQ-UM-019 | The system must use the official letter formats shared by the department and auto-populate them with the user's details, effective dates, and role abbreviations | Must | Template matches department format; fields auto-filled |

### 8.6 Reporting and MIS

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| REQ-UM-020 | The system must generate and provide access to necessary daily reports showing the exact number of users logged into the system each day | Must | Daily report shows login count per date |
| REQ-UM-021 | The daily login report must explicitly show the active roles being utilized by those logged-in users | Must | Report columns include session role breakdown |

## 9. Business rules

| Rule ID | Description | Source | System enforcement |
|---------|-------------|--------|-------------------|
| BR-UM-001 | Primary Role is mandatory at account creation and cannot have an end date | REQ-UM-002 | Hard stop |
| BR-UM-002 | Secondary Roles must have a mandatory end date and auto-expire | REQ-UM-003 | Hard stop; scheduled job |
| BR-UM-003 | Approval letter required for secondary role grant and primary role change | REQ-UM-004, REQ-UM-005 | Hard stop without upload |
| BR-UM-004 | Future-dated role changes apply automatically on effective date | REQ-UM-006 | Scheduler |
| BR-UM-005 | Session menus and permissions reflect the selected session role only | REQ-UM-007 | Dynamic UI |
| BR-UM-006 | Role switching does not require re-authentication | REQ-UM-008 | Session update |
| BR-UM-007 | Peer/subordinate role editing requires Super Admin toggle per role | REQ-UM-009 | Permission check |
| BR-UM-008 | No password-based authentication in KAVERI 2.0 | REQ-UM-010 | Password UI removed |
| BR-UM-009 | Login requires User ID + OTP + Captcha (all three) | REQ-UM-011 | AuthN gate |
| BR-UM-010 | Biometric data must be re-registered every 5 years | REQ-UM-013 | Login block until re-registration |
| BR-UM-011 | Role abbreviations displayed in UI wherever role is shown | REQ-UM-016 | UI rendering |
| BR-UM-012 | Joining / Relieving letters auto-generated on role or location change | REQ-UM-018 | Letter engine |
| BR-UM-013 | All user-management actions logged with timestamp, IP, and actor ID | NFR-UM-01 | Immutable audit |

## 10. User interface (high-level)

| Screen / step | Purpose | Actor | Notes |
|---------------|---------|-------|-------|
| Passwordless login | User ID + Captcha + OTP | User | REQ-UM-010, REQ-UM-011 |
| Biometric login | Fingerprint / face authentication | User | REQ-UM-012 |
| Biometric re-registration | Mandatory 5-year update | User | REQ-UM-013 |
| Session role picker | Select role after login | User | REQ-UM-007 |
| Role switcher | Change session role in-app | User | REQ-UM-008 |
| Add User (instant) | Create user with Primary Role | Admin | REQ-UM-001, REQ-UM-002 |
| Assign Secondary Role | Grant temporary role with end date and letter | Admin | REQ-UM-003, REQ-UM-004 |
| Change Primary Role | Promotion / transfer / demotion with reason and letter | Admin | REQ-UM-005 |
| Future-dated role change | Schedule joining / relieving | Admin | REQ-UM-006 |
| Add / Edit Role | Dynamic role creation with abbreviation | Super Admin | REQ-UM-014, REQ-UM-015 |
| Hierarchy configuration | Set reporting relationships | Super Admin | REQ-UM-017 |
| Peer/subordinate editing toggle | Enable/disable per role | Super Admin | REQ-UM-009 |
| Letter preview / download | Joining / Relieving letters | Admin / User | REQ-UM-018 |
| Daily login report | MIS with role segmentation | Admin | REQ-UM-020, REQ-UM-021 |
| Audit search / export | Who / when / what | Audit role | NFR-UM-01 |

**Bilingual:** All labels `[EN / KN]` — content manager sign-off. Kannada values for role and office come from masters.

## 11. Integrations

| Integration | Direction | Purpose | Owner | Status |
|-------------|-----------|---------|-------|--------|
| SMS gateway | Outbound | OTP delivery for passwordless login | Ops | Must; ≤ 5 s latency |
| Email gateway | Outbound | OTP delivery (alternate channel) | Ops | Should |
| Biometric device / SDK | Device | Fingerprint / face capture and verification | Security | Must for REQ-UM-012 |
| Captcha service | Internal | Bot prevention on login | Arch | Must |
| Aadhaar / eKYC | Outbound | Optional identity verification | Security / Legal | TBD |
| DSC / eSign provider | Inbound metadata | Certificate serial, expiry | Security | Where signing roles apply |
| Consuming modules (Marriage, Document Registration, MIS) | API provide | Session role, privilege claims, user master | Arch | Must |
| Audit / SIEM | Outbound | Auth and privilege events | Security | Should |

## 12. Data requirements

### 12.1 Core entities (logical)

- **User** — User ID, names, mobile (verified), email, KGID, photo, ID proof, biometric refs, biometric registration date, active status.
- **Role** — name, abbreviation, acronym, hierarchy level, parent role (reporting), active, peer-edit permission flag.
- **UserRoleAssignment** — user, role, type (Primary / Secondary), valid from, valid to (null for Primary), approval letter artefact, reason, effective date, status.
- **Session** — user, selected session role, login timestamp, IP address, auth method (OTP / Biometric).
- **RoleSwitchEvent** — session, from role, to role, timestamp.
- **Letter** — type (Joining / Relieving), user, role, effective date, template ref, generated content, artefact.
- **AuditEvent** — append-only: who, when, IP, action, before/after.

### 12.2 Retention

| Data class | Retention |
|------------|-----------|
| User, role assignment, transfer/relieve history | Permanent for departmental audit |
| Biometric templates | Per UIDAI / department policy; re-register every 5 years |
| Audit of login, role switch, privilege change | Not less than 7 years unless Legal specifies otherwise |
| Generated letters | Permanent with audit reference |

### 12.3 Migration (high level)

| Topic | Question for migration workstream |
|-------|-----------------------------------|
| Legacy users | Map existing users to Primary Role; identify temporary assignments for Secondary Role conversion |
| Password deprecation | Force passwordless login at cutover; no password hash migration |
| Role hierarchy | Seed from DSR org chart (Appendix B); validate with Domain Expert |
| Biometric data | Re-capture or migrate with registration date for 5-year rule |

## 13. Requirements traceability matrix (RTM)

| Req ID | Requirement summary | BRD section | UI screen | Test case ID | Status |
|--------|---------------------|-------------|-----------|--------------|--------|
| REQ-UM-001 | Instant account creation | 7.2.1, 8.1 | Add User | TC-UM-001 | Draft |
| REQ-UM-002 | Primary Role mandatory, no end date | 7.2.1, 8.1 | Add User | TC-UM-002 | Draft |
| REQ-UM-003 | Secondary Role with end date, auto-expiry | 7.2.3, 8.1 | Assign Secondary Role | TC-UM-003 | Draft |
| REQ-UM-004 | Approval letter for secondary role | 8.1 | Assign Secondary Role | TC-UM-004 | Draft |
| REQ-UM-005 | Primary role change with reason and letter | 7.2.2, 8.1 | Change Primary Role | TC-UM-005 | Draft |
| REQ-UM-006 | Future-dated role changes | 7.2.1, 8.1 | Future-dated change | TC-UM-006 | Draft |
| REQ-UM-007 | Session role selection | 7.3.1, 8.2 | Session role picker | TC-UM-007 | Draft |
| REQ-UM-008 | Dynamic role switching | 7.3.2, 8.2 | Role switcher | TC-UM-008 | Draft |
| REQ-UM-009 | Peer/subordinate role editing toggle | 7.3.3, 8.2 | Admin toggle | TC-UM-009 | Draft |
| REQ-UM-010 | No password authentication | 7.4.1, 8.3 | Login | TC-UM-010 | Draft |
| REQ-UM-011 | User ID + OTP + Captcha login | 7.4.1, 8.3 | Login | TC-UM-011 | Draft |
| REQ-UM-012 | Biometric login option | 7.4.2, 8.3 | Biometric login | TC-UM-012 | Draft |
| REQ-UM-013 | Biometric re-registration every 5 years | 7.4.2, 8.3 | Biometric re-registration | TC-UM-013 | Draft |
| REQ-UM-014 | Dynamic role creation | 7.5.1, 8.4 | Add Role | TC-UM-014 | Draft |
| REQ-UM-015 | Role Name, Abbreviation, Acronym | 8.4 | Add / Edit Role | TC-UM-015 | Draft |
| REQ-UM-016 | Abbreviation displayed in UI | 8.4 | All screens | TC-UM-016 | Draft |
| REQ-UM-017 | Hierarchy configuration | 7.1.1, 8.4 | Hierarchy config | TC-UM-017 | Draft |
| REQ-UM-018 | Auto Joining / Relieving letters | 7.6, 8.5 | Letter preview | TC-UM-018 | Draft |
| REQ-UM-019 | Official letter templates | 8.5 | Letter preview | TC-UM-019 | Draft |
| REQ-UM-020 | Daily login report | 7.7, 8.6 | Daily login report | TC-UM-020 | Draft |
| REQ-UM-021 | Report segmented by session role | 7.7, 8.6 | Daily login report | TC-UM-021 | Draft |
| NFR-UM-01 | Security and audit logging | 15.2 | Audit export | TC-UM-NFR-01 | Draft |
| NFR-UM-02 | OTP delivery ≤ 5 seconds | 15.1 | Login | TC-UM-NFR-02 | Draft |

## 14. Acceptance and sign-off

| Role | Name | Signature / Date | Comments |
|------|------|------------------|----------|
| Product Owner | Prashanth | | |
| Domain Expert | Prabhakar Naik | | |
| IGR nominee | | | |
| AIGR Computers / Kaveri IT Cell | | | |
| Business Analyst | Nandha Kumar | | |
| Security reviewer | | | |

**UAT scope:** Test scenarios derived from REQ-UM-001 through REQ-UM-021 and NFR-UM-01 / NFR-UM-02 covering: instant user creation; primary/secondary role assignment and expiry; session role selection and switching; passwordless login (OTP + Captcha); biometric login and 5-year re-registration; dynamic role creation; hierarchy configuration; letter generation; daily login MIS; audit trail.

**Go-live gate:** User Management passwordless login operational; primary/secondary role model enforced; session role selection available; consuming modules read session role claims.

## 15. Non-functional requirements

### 15.1 Performance (NFR-UM-02)

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| NFR-UM-02 | OTP delivery for passwordless authentication must be dispatched within 5 seconds of the request to ensure a smooth login experience | Must | 95th percentile OTP dispatch ≤ 5 s in load test |

### 15.2 Security and audit (NFR-UM-01)

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| NFR-UM-01 | Every action within the User Management module (role change, end-date expiration, letter generation) must be logged with a timestamp, IP address, and the ID of the official performing the action | Must | Audit record for each action; exportable; immutable |

### 15.3 System availability

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| NFR-UM-03 | User Management authentication service shall be available 99.5% during business hours | Must | Monitoring dashboard |
| NFR-UM-04 | Scheduled jobs (secondary role expiry, future-dated changes) shall run at least once per hour | Must | Job execution logs |

### 15.4 Security audit and compliance

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| NFR-UM-05 | System shall comply with MeitY / CERT-In / STQC / GIGW security norms | Must | VAPT clearance before go-live |
| NFR-UM-06 | Biometric data shall be stored and transmitted per UIDAI and department security guidelines | Must | Security design sign-off |

## 16. Risk and Mitigation Strategy

| Risk ID | Risk | Mitigation | Related requirements |
|---------|------|------------|---------------------|
| RS-UM-001 | Officers with multiple roles select wrong session role and perform actions under incorrect authority | Prominent session-role indicator in header; role abbreviation always visible; audit of role switches | REQ-UM-007, REQ-UM-008, REQ-UM-016 |
| RS-UM-002 | OTP delivery failure blocks all logins | Dual channel (SMS + email); retry queue; admin break-glass with audit | REQ-UM-011, NFR-UM-02 |
| RS-UM-003 | Secondary role not removed on expiry due to scheduler failure | Hourly expiry job with alert on failure; manual revoke fallback | REQ-UM-003, NFR-UM-04 |
| RS-UM-004 | Biometric template degradation over 5 years causes false rejections | Proactive re-registration prompt 30 days before expiry; admin override with audit | REQ-UM-013 |

## 17. System Fallbacks & Error Handling

| Req ID | Requirement | Priority | Acceptance criteria |
|--------|-------------|----------|---------------------|
| FB-UM-001 | If OTP gateway is unreachable, system shall queue OTP and retry; display clear message to user | Must | User sees "OTP delayed — retrying"; no silent failure |
| FB-UM-002 | If Captcha validation service fails, system shall present alternate Captcha challenge | Must | Login not blocked by single Captcha failure |
| FB-UM-003 | If biometric device unavailable, user shall fall back to OTP + Captcha login | Must | Biometric path shows fallback link |
| FB-UM-004 | If letter template rendering fails, system shall log error and allow admin to retry generation | Must | Role change not rolled back; letter retry available |

## 18. Training and Change Management

### 18.1 Target audience

- Super Admins and IGR office staff (role creation, hierarchy configuration).
- DIGR / DR / SRO admins (user creation, primary/secondary role assignment).
- All departmental users (passwordless login, session role selection, role switching).

### 18.2 Training delivery

- Classroom and e-learning modules covering passwordless login, session role selection, and role switching.
- Admin training for instant user creation, approval letter upload, and letter generation.
- Quick-reference cards for session role indicator and role switcher.

### 18.3 Change management

- Communicate removal of password-based login before cutover.
- Pilot with one division before statewide rollout.
- Helpdesk scripts updated for OTP and biometric issues (not password reset).

### 18.4 Post-Go-Live support

- Hypercare for first 30 days with dedicated UM support line.
- Daily login MIS reviewed by KPMU for adoption monitoring.

## Appendix A — References

- BR Discussion Prep Pack — User Management (24 August 2026)
- User Management KAVERI 2.0_v0.3.pdf — Requirement Discussions/Kaveri2.0/
- Marriage BRD v1.9 (section pattern) — Finalized BRD/Marriage/RFP/BRD_Marriage_v1.9.docx
- Information Technology Act, 2000; Aadhaar Act, 2016; Indian Registration Act, 1908
- MeitY / CERT-In / STQC / GIGW guidance
- DSR Organizational Chart (official)

## Appendix B — DSR organizational hierarchy (seed roles)

| Division | Roles (seed) |
|----------|-------------|
| Top Management | IGR |
| Division 1 — Admin, Law & Computers | DIGR (Admin, Law & Computers), AIGR (Admin), HQA (Admin), SRO (Admin), FDA, SDA |
| Division 2 — Vigilance | DIGR (Vigilance), Law Officer, HQA (RTI) |
| Division 3 — Computers | AIGR (Computers), System Integrator, PMU, Application Developer, SRO (Comp) |
| Division 4 — Enforcement | DIGR (Enforcement), DRO, HQA, SRO, FDA, SDA |
| Division 5 — Intelligence & Audit | DIGR (Intelligence), AIGR (Audit), HQA (Audit), Superintendent (Audit) |
| Division 6 — CVC | DIGR CVC, JD Town Planning |

Super Admins may add unlimited additional roles (REQ-UM-014). Hierarchy levels and reporting relationships are configured via REQ-UM-017.

## Appendix C — Open questions and decision log

### C.1 Open questions

| Q ID | Question | Options / notes | Needed from | Due |
|------|----------|-----------------|-------------|-----|
| OQ-UM-01 | Login User ID: official email, KGID, or both accepted? | Impacts REQ-UM-011 | Security, PO | |
| OQ-UM-02 | Biometric mandatory for all users or optional alternate to OTP? | REQ-UM-012 says "option" | Security, PO | |
| OQ-UM-03 | Letter templates: Word/PDF template upload vs in-system editor? | REQ-UM-019 | Domain Expert | |
| OQ-UM-04 | Daily login report: real-time dashboard vs end-of-day batch? | REQ-UM-020 | PO, Ops | |
| OQ-UM-05 | Peer/subordinate role editing: which roles are "elevated" by default? | REQ-UM-009 | Domain Expert | |

### C.2 Decisions

| Dec ID | Decision | Date | Approver | Impact |
|--------|----------|------|----------|--------|
| DEC-UM-001 | KAVERI 2.0 User Management removes password authentication entirely | 2026-08-28 | PO (to confirm) | REQ-UM-010 |
| DEC-UM-002 | Primary / Secondary role model with session role selection adopted | 2026-08-28 | PO (to confirm) | REQ-UM-002–008 |
| DEC-UM-003 | DSR organizational hierarchy is seed data; Super Admin can extend | 2026-08-28 | Domain Expert (to confirm) | §7.1, REQ-UM-014, REQ-UM-017 |
| DEC-UM-004 | Joining / Relieving letters generated in-app using department templates | 2026-08-28 | PO (to confirm) | REQ-UM-018, REQ-UM-019 |

*End of BRD — User Management & RBAC Module, KAVERI 2.0.*
