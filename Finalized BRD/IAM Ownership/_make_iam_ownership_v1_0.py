# -*- coding: utf-8 -*-
"""Create Kaveri3_IAM_Ownership_Matrix_v1.0.docx — Kaveri application vs IAM platform roles and ownership by area."""
from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(r"Finalized BRD/IAM Ownership")
DST = OUT_DIR / "Kaveri3_IAM_Ownership_Matrix_v1.0.docx"
DIAGRAM = OUT_DIR / "IAM_Ownership_Overview_v1.0.png"

DOC_VERSION = "1.0"
DOC_DATE = "05-10-2026"
BRD_REF = "BRD_User_Management_v4.25 (BRD-K3-UM-001, version 1.2)"

NAVY = RGBColor(0x1F, 0x3A, 0x5F)
HEADER_FILL = "1F3A5F"
AREA_FILL = "D9E2F3"

KCB = "IAM (built-in)"
KCE = "IAM (extension)"
KAV = "Kaveri application"
SHR = "Shared"
RET = "Retired"
OWNER_FILL = {KCB: "DDEBF7", KCE: "E4DFEC", KAV: "E2EFDA", SHR: "FFF2CC", RET: "EDEDED"}


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------

PURPOSE = (
    "This document defines, area by area, which responsibilities of KAVERI 3.0 User Management "
    "and access control are owned by the Identity and Access Management (IAM) platform and which are owned by the "
    "KAVERI application. It is the agreed reference for solution architects, development teams, "
    "Kaveri IT Cell (operations) and security reviewers when designing, building, testing and "
    "operating identity, authentication and authorisation. Business rules themselves are defined "
    f"in the User Management BRD ({BRD_REF}); this document does not restate or change them — it "
    "assigns each of them an owner."
)

SCOPE_IN = [
    "Ownership of identity, registration, authentication, session, recovery and contact-change capabilities",
    "Ownership of role, post, occupancy, hierarchy and module-access (RBAC) capabilities and their runtime enforcement",
    "Ownership of user administration, DSR officer lifecycle, Kaveri 2.0 citizen migration, notifications, audit and reporting",
    "Data ownership (source of truth) for every user attribute, and the integration points between KAVERI and IAM",
    "Operational ownership of the IAM platform and its dependencies",
]
SCOPE_OUT = [
    "Detailed IAM configuration (realm settings, flow definitions, client settings) — covered in the IAM solution design",
    "Source code design of IAM extensions and KAVERI services",
    "Business rules — owned by the User Management BRD",
]

PRINCIPLES = [
    ["P1", "IAM owns who the user is", "Identity, Username, credentials and login factors, sessions, tokens and logout are IAM responsibilities."],
    ["P2", "KAVERI owns what the user is in the Department", "Roles, posts, sanctioned posts, occupancy, office and officer hierarchies, transfers, absence and charges, and module access mapping are KAVERI responsibilities."],
    ["P3", "One source of truth per data item", "Every data item has exactly one owner (Section 6). The other side reads it through a token claim or an API; it is never maintained in two places."],
    ["P4", "Department administrators use KAVERI screens only", "All user administration by Department actors is done in KAVERI screens, which call the IAM Admin REST API. The IAM admin console is restricted to Kaveri IT Cell."],
    ["P5", "Prefer built-in, then extension, then application", "A requirement is met by IAM built-in configuration where possible, by a IAM extension where it concerns login or credentials, and in the KAVERI application otherwise."],
    ["P6", "Tokens carry only the session context", "Access tokens carry the selected post (or charge) and the roles derived from it — never all of an officer's posts — and are re-issued whenever the context changes."],
    ["P7", "Every event is auditable in one place", "IAM authentication and admin events are forwarded to the KAVERI audit store, so that all BRD reports are produced from one place."],
]

CATEGORIES = [
    [KCB, "Met by IAM configuration only; no custom code."],
    [KCE, "Custom code (extension — authenticator, required action, protocol mapper, event listener) deployed inside the IAM platform and maintained by the KAVERI development team."],
    [KAV, "Built as KAVERI services, screens, jobs or data; IAM is not involved or only provides the user's identity."],
    [SHR, "Both are involved: one side owns the data and the other enforces it. The matrix states each side's part and the hand-off."],
]

# (id, capability, owner, kaveri responsibility, keycloak responsibility, source of truth, BRD reference)
MATRIX: list[tuple[str, list[list[str]]]] = [
    ("A1. Citizen self-registration and Aadhaar e-KYC", [
        ["A1.1", "Registration pages (preferred Username, email, mobile) and Username availability check", KCE,
         "Provide bilingual (Kannada / English), GIGW-compliant page content and branding for the IAM theme.",
         "Host the registration flow in the KAVERI theme; check Username availability across the realm and suggest alternatives.",
         "IAM", "FR-UM-001, FR-UM-062"],
        ["A1.2", "Email OTP and mobile OTP verification before account creation", KCE,
         "Provide the Notification Service used to deliver OTPs (A13).",
         "Generate, validate and expire OTPs per FR-UM-069–072; create the account only after both are verified.",
         "IAM", "FR-UM-063"],
        ["A1.3", "Aadhaar e-KYC at registration", SHR,
         "Own the e-KYC Integration Service (UIDAI AUA/KUA connectivity, consent text, Aadhaar Data Vault, e-KYC transaction audit).",
         "Registration step calls the e-KYC Integration Service; on success sets the e-KYC Status attribute and creates the account.",
         "e-KYC status: IAM; e-KYC transaction record: KAVERI", "FR-UM-085"],
        ["A1.4", "Captcha on registration", KCE,
         "Select the Captcha provider acceptable to the Department.",
         "Validate Captcha in the registration flow.",
         "—", "FR-UM-011"],
    ]),
    ("A2. Username and identity attributes", [
        ["A2.1", "Single namespace; unique Username; email and mobile not unique; Username not user-editable", KCB,
         "—",
         "Single realm for all user categories; duplicate emails allowed; login with email disabled; username editing disabled.",
         "IAM", "FR-UM-004, FR-UM-028, FR-UM-062"],
        ["A2.2", "Identity attributes: User Category, KGID, Department Code, Employee ID, e-KYC Status", SHR,
         "Supply the values from KAVERI admin screens (A10) and the migration tool (A12); maintain the Department Code list.",
         "Store the values as user-profile attributes with validation; expose them as token claims.",
         "IAM", "FR-UM-002, FR-UM-003, FR-UM-064"],
        ["A2.3", "Username derivation for DSR (KGID) and Other Department (DeptCode-EmpID/KGID)", KAV,
         "Derive and validate the Username in the user-creation screens before calling IAM.",
         "Reject a duplicate Username on create.",
         "IAM", "FR-UM-062, FR-UM-064"],
        ["A2.4", "Administrator correction of a Username with reason", SHR,
         "Correction screen, reason capture and business audit.",
         "Update the Username via Admin REST API; revoke active sessions.",
         "IAM", "FR-UM-062"],
    ]),
    ("A3. Login by user category", [
        ["A3.1", "Citizen and Other Department login: Username + Captcha + SMS OTP", KCE,
         "Provide the Notification Service (A13).",
         "Custom browser flow: Captcha, then OTP to registered mobile only, dispatched within 5 seconds.",
         "—", "FR-UM-005, FR-UM-007, FR-UM-010, FR-UM-011"],
        ["A3.2", "DSR Officer login: Username (KGID) + Captcha + face or biometric authentication (no OTP)", KCE,
         "Procure / contract the face or biometric authentication provider.",
         "Custom authenticator integrating the provider; no OTP step for DSR Officers.",
         "—", "FR-UM-006"],
        ["A3.3", "No passwords for any category", KCB,
         "—",
         "No password credential type is configured or offered; password reset and change are disabled.",
         "—", "FR-UM-009"],
        ["A3.4", "Login page language and accessibility", SHR,
         "Kannada / English text and GIGW review.",
         "Theme and message bundles.",
         "—", "Section 5 (Compliance)"],
    ]),
    ("A4. OTP, lockout and session policy", [
        ["A4.1", "OTP and PIN validity, length, attempts, resend cooldown", KCE,
         "—",
         "Configurable parameters in the OTP / PIN extension: login OTP 5 min; registration / recovery OTP and PIN 10 min; 6 digits; 3 attempts; 60 s cooldown, max 3 per 15 min.",
         "IAM configuration", "FR-UM-069–FR-UM-072"],
        ["A4.2", "Lock Username for 15 minutes after 5 failed attempts", KCB,
         "—",
         "Brute-force detection configured to 5 failures and 15-minute lock.",
         "IAM", "FR-UM-073"],
        ["A4.3", "Idle timeout 10 min; absolute session 4 h", SHR,
         "Frontends handle token expiry and redirect to login; no application-side session that outlives the IAM session.",
         "SSO Session Idle = 10 min; SSO Session Max = 4 h; token lifespans aligned.",
         "IAM", "FR-UM-074, FR-UM-075"],
        ["A4.4", "One active session per Username", KCB,
         "—",
         "User session count limiter in the login flow: a new login terminates the prior session.",
         "IAM", "FR-UM-076"],
        ["A4.5", "Logout", SHR,
         "Logout action in every frontend; clear local tokens.",
         "End the session; back-channel logout to all KAVERI clients.",
         "IAM", "FR-UM-008"],
    ]),
    ("A5. Recovery and contact changes", [
        ["A5.1", "Citizen lost-mobile reset: Aadhaar e-KYC + PIN to registered email + OTP to new mobile", KCE,
         "e-KYC Integration Service and Notification Service.",
         "Custom reset flow; rate limits and lock; updates mobile only after new-mobile OTP; notifies the registered email.",
         "IAM", "FR-UM-012, FR-UM-056"],
        ["A5.2", "Citizen mobile / email change and DSR mobile change after login", KCE,
         "Profile screen launches the change as an application-initiated action and shows the result.",
         "Custom required action verifies the new mobile or email by OTP and updates the attribute.",
         "IAM", "FR-UM-013, FR-UM-086"],
        ["A5.3", "Other Department mobile / email change by administrator only", SHR,
         "Admin screen with reason capture and business audit.",
         "Update via Admin REST API; no self-service path for this category.",
         "IAM", "FR-UM-065"],
        ["A5.4", "Profile view and profile photo", KAV,
         "Profile screen (Username read-only from token); photo stored in KAVERI document storage.",
         "Provide identity claims.",
         "Photo: KAVERI", "FR-UM-013, FR-UM-014"],
    ]),
    ("A6. DSR post selection, additional charge and temporary charge", [
        ["A6.1", "Eligible post contexts at login (active occupancies + temporary charges); login blocked during approved absence", SHR,
         "Post and Occupancy Service returns the officer's eligible contexts and absence status (internal API).",
         "Post-selection authenticator calls the service after face / biometric authentication; denies login when the officer is absent.",
         "KAVERI", "FR-UM-052, FR-UM-080, FR-UM-083"],
        ["A6.2", "Post selection screen; auto-select a single occupancy", KCE,
         "Supply display labels (Role — Post Name — Office Name (Office Code)).",
         "Render the selection step and store the selected context in the user session.",
         "IAM session", "FR-UM-052"],
        ["A6.3", "Session claims derived only from the selected post or charge", SHR,
         "Post–Role mapping and role resolution for the selected context.",
         "Protocol mapper adds selected post, office, charge type and derived roles to the access token.",
         "Roles: KAVERI; token: IAM", "FR-UM-038, FR-UM-052, FR-UM-083"],
        ["A6.4", "Additional charge of an unoccupied subordinate post after login, and switch back", SHR,
         "List eligible posts (Occupied = 0, same office), record the charge and its clearance, audit.",
         "Re-issue tokens for the new context (re-authentication via application-initiated action or token exchange — decision D3).",
         "KAVERI", "FR-UM-053, FR-UM-038"],
        ["A6.5", "Display of assigned post and charge in header / home page", KAV,
         "Read context from the access token and display it.",
         "Provide the context claims.",
         "—", "FR-UM-054"],
    ]),
    ("A7. Roles, posts and masters", [
        ["A7.1", "Unified Role Master, Role Category, Division Master, seed roles", KAV,
         "Masters, screens and seed data; source of role names placed in tokens.",
         "No role assignments maintained for DSR Officers (roles are session-derived); see decision D4.",
         "KAVERI", "FR-UM-016, FR-UM-019, FR-UM-028, FR-UM-034, FR-UM-035, FR-UM-077"],
        ["A7.2", "Posts Master, Post–Role mapping, Post–Office-Type mapping, Sanctioned Posts Master and occupancy display", KAV,
         "Masters, validation, screens and occupancy counts.",
         "—",
         "KAVERI", "FR-UM-024–FR-UM-027, FR-UM-046–FR-UM-049, FR-UM-078"],
    ]),
    ("A8. Module, function, resource masters and runtime access enforcement", [
        ["A8.1", "Module, Module Function and Resource (API / URL) masters; Role–Module–Function mapping", KAV,
         "Application Admin screens, referential-integrity validation, audit.",
         "—",
         "KAVERI", "FR-UM-036, FR-UM-037, FR-UM-039, FR-UM-040, FR-UM-042, FR-UM-050"],
        ["A8.2", "Runtime enforcement on every API / URL request", SHR,
         "Authorisation component (API gateway policy or service middleware) maps token roles → functions → resources and allows or denies (decision D2).",
         "Issue signed tokens; publish signing keys (JWKS) for token signature, expiry and audience validation.",
         "Mapping: KAVERI", "FR-UM-018, FR-UM-038, FR-UM-041"],
        ["A8.3", "Menu and screen visibility", KAV,
         "Frontends show only functions allowed for the session roles.",
         "—",
         "KAVERI", "FR-UM-041"],
    ]),
    ("A9. Office and officer hierarchies", [
        ["A9.1", "Office Hierarchy Master and office span", KAV,
         "Master, screens and span resolution used by all DSR workflows.",
         "—",
         "KAVERI", "FR-UM-059"],
        ["A9.2", "DSR Officer Hierarchy Master (reporting structure)", KAV,
         "Master, seed structure and screens.",
         "—",
         "KAVERI", "FR-UM-043, FR-UM-044"],
    ]),
    ("A10. User creation and administration", [
        ["A10.1", "Create DSR Officer users with post assignment", SHR,
         "Step-by-step screen: KGID, mobile, posts with available capacity, office-span checks; then create the user in IAM.",
         "Create the user and attributes via Admin REST API; no credential set (face / biometric enrolment per A3.2).",
         "Identity: IAM; posts: KAVERI", "FR-UM-002, FR-UM-017, FR-UM-030, FR-UM-032, FR-UM-045"],
        ["A10.2", "Create Other Department users with one role and optional End Date", SHR,
         "Screen: Department Code, Employee ID / KGID, official email (domain check), mobile, one role, End Date; daily job disables expired users.",
         "Create, and later disable, the user via Admin REST API.",
         "Identity: IAM; role and End Date: KAVERI", "FR-UM-003, FR-UM-029, FR-UM-033, FR-UM-064"],
        ["A10.3", "Edit, suspend, deactivate, reactivate with reason", SHR,
         "Screens, reason capture, business audit, notification.",
         "Enable / disable the user; revoke all active sessions immediately.",
         "Status: IAM; reason: KAVERI", "FR-UM-020"],
        ["A10.4", "Search and filter users", KAV,
         "Search screen combining IAM identity data with KAVERI category, role, office, division and status.",
         "Admin REST API user query.",
         "—", "FR-UM-021"],
        ["A10.5", "Application Admin (system-level actor)", SHR,
         "Seed the Application Admin privilege set; restrict master-maintenance screens to it.",
         "Seed the Application Admin accounts at deployment; not creatable through normal user creation.",
         "IAM + KAVERI", "FR-UM-051"],
        ["A10.6", "IAM admin console", KCB,
         "—",
         "Access restricted to named Kaveri IT Cell staff for realm configuration and support; not used by Department administrators (P4).",
         "IAM", "—"],
    ]),
    ("A11. DSR officer lifecycle", [
        ["A11.1", "Transfer Out / relieving with Relieving Reason; Transfer In with capacity check", KAV,
         "Workflows, office span and parentage checks, order references, audit.",
         "—",
         "KAVERI", "FR-UM-057, FR-UM-058, FR-UM-060, FR-UM-066, FR-UM-087"],
        ["A11.2", "Occupancy refresh job after midnight", SHR,
         "Run the job; de-allocate ended occupancies; recalculate counts.",
         "Revoke active sessions of officers whose selected context was de-allocated (requested by KAVERI via Admin REST API).",
         "KAVERI", "FR-UM-068, FR-UM-084"],
        ["A11.3", "Temporary Absence, Leave, OOD and Temporary Charge", KAV,
         "Record absence and temporary charge; expose status to A6.1.",
         "Enforced at next login via A6.1; active sessions revoked when absence starts.",
         "KAVERI", "FR-UM-079, FR-UM-081, FR-UM-082, FR-UM-084"],
    ]),
    ("A12. Kaveri 2.0 citizen migration", [
        ["A12.1", "Extract, filter (e-KYC = true), cleanse, validate, exception register, reconciliation", KAV,
         "Migration tool and process run by Kaveri IT Cell; Application Admin exception screens.",
         "—",
         "KAVERI", "FR-UM-088, FR-UM-093, FR-UM-095"],
        ["A12.2", "Load migrated citizens", SHR,
         "Call the Admin REST API (or partial import) idempotently, keyed on the Kaveri 2.0 username.",
         "Create users without credentials: Username = Kaveri 2.0 email ID, mobile, email, e-KYC Status = Completed (source Kaveri 2.0), Migration Source flag.",
         "IAM", "FR-UM-088, FR-UM-089, FR-UM-090"],
        ["A12.3", "Pending Activation and first-login activation (email OTP, consent)", KCE,
         "Report activation progress from IAM data.",
         "Required actions set on import: email OTP verification (extension) and terms acceptance (built-in); account Active when both complete.",
         "IAM", "FR-UM-091, FR-UM-092"],
        ["A12.4", "Kaveri 2.0 username ↔ IAM user ID cross-reference", KAV,
         "Store the read-only cross-reference and provide it to other module migrations.",
         "Return the IAM user ID on create.",
         "KAVERI", "FR-UM-094"],
    ]),
    ("A13. Notifications", [
        ["A13.1", "SMS and email delivery (OTP, PIN, account events, migration notices)", SHR,
         "Notification Service: SMS and email gateway integration, bilingual templates, throttling, delivery logs.",
         "Extensions call the Notification Service for OTP and PIN delivery; IAM's own SMTP is not used for citizen-facing messages.",
         "KAVERI", "FR-UM-010, FR-UM-023, FR-UM-096"],
    ]),
    ("A14. Audit and reporting", [
        ["A14.1", "Authentication events (login success / failure, OTP, lockout, session start / end, recovery)", SHR,
         "Receive and store events in the audit store with retention per Department policy.",
         "Event listener extension forwards login events to the KAVERI audit store.",
         "KAVERI audit store", "FR-UM-022, Section 5 (Auditability)"],
        ["A14.2", "Admin events in IAM", SHR,
         "Store alongside business audit.",
         "Admin events enabled and forwarded by the event listener.",
         "KAVERI audit store", "FR-UM-022"],
        ["A14.3", "Business audit (masters, assignments, transfers, absence, charges, migration)", KAV,
         "Record with actor and timestamp.",
         "—",
         "KAVERI audit store", "FR-UM-022"],
        ["A14.4", "All Section 6 reports", KAV,
         "Produce from the KAVERI audit store and masters, including forwarded IAM events.",
         "—",
         "KAVERI", "Section 6"],
    ]),
    ("A15. Non-functional and platform", [
        ["A15.1", "IAM availability, scaling and performance", SHR,
         "Kaveri IT Cell operates the cluster (Section 8); load tests include IAM at 500+ concurrent sessions.",
         "Clustered deployment with shared cache and database.",
         "—", "Section 5 (Performance)"],
        ["A15.2", "Data residency, encryption and compliance", SHR,
         "Host KAVERI services in India; DPDP Act 2023 and UIDAI compliance of KAVERI services.",
         "IAM and its database hosted in India on MeitY-empanelled infrastructure; TLS 1.2+; encrypted database.",
         "—", "Section 5 (Security, Compliance)"],
        ["A15.3", "Token signing keys and key rotation", KCB,
         "—",
         "Key generation and rotation; rotation schedule owned by Kaveri IT Cell.",
         "IAM", "Section 5 (Security)"],
    ]),
]

DATA_OWNERSHIP = [
    ["IAM user ID (sub)", "IAM", "Access token; stored by KAVERI as the link key on every KAVERI user record"],
    ["Username", "IAM", "Token claim (preferred_username); set on create by KAVERI admin screens or registration"],
    ["Mobile number, email", "IAM", "Token claims / Admin REST API; changed only through IAM flows or Admin REST API"],
    ["User Category, KGID, Department Code, Employee ID", "IAM (attributes)", "Token claims; values supplied by KAVERI admin screens"],
    ["e-KYC Status", "IAM (attribute)", "Token claim; set by registration flow, lost-mobile reset or migration"],
    ["e-KYC transaction record (UIDAI response reference, consent)", "KAVERI e-KYC Integration Service", "Not copied to IAM"],
    ["Account enabled / disabled, required actions, sessions", "IAM", "Admin REST API"],
    ["Suspension / deactivation reason and history", "KAVERI", "Not copied to IAM"],
    ["Department Code list", "KAVERI", "Used by KAVERI admin screens to validate before writing the attribute"],
    ["Role Master, Division Master, Role Category", "KAVERI", "Role names placed in the token by the protocol mapper"],
    ["Posts, Post–Role mapping, Sanctioned Posts, occupancies", "KAVERI", "Read by the post-selection authenticator at login"],
    ["Office and officer hierarchies", "KAVERI", "Not copied to IAM"],
    ["Temporary absence and temporary / additional charge", "KAVERI", "Read by the post-selection authenticator at login"],
    ["Selected post / charge for the session", "IAM (user session)", "Token claims"],
    ["Module, Function, Resource masters and Role–Module–Function mapping", "KAVERI", "Used by the KAVERI authorisation component"],
    ["Other Department End Date", "KAVERI", "Daily job disables the user in IAM"],
    ["Legacy Kaveri 2.0 username cross-reference", "KAVERI", "Not copied to IAM (Username already equals the Kaveri 2.0 email ID)"],
    ["Authentication and admin events", "IAM (origin) → KAVERI audit store (record)", "Event listener extension"],
]

INTEGRATIONS = [
    ["I1", "KAVERI admin screens → IAM Admin REST API", "Create, update, enable / disable users; set attributes", "Service account (client credentials) limited to user management in the KAVERI realm"],
    ["I2", "IAM post-selection authenticator → KAVERI Post and Occupancy Service", "Fetch eligible post contexts and absence status at login", "Internal network only; mutual TLS or service token"],
    ["I3", "IAM protocol mapper → KAVERI role resolution", "Derive roles for the selected post / charge into the access token", "Same as I2; result cached for the session"],
    ["I4", "KAVERI frontends and APIs ↔ IAM (OpenID Connect)", "Login redirect, tokens, refresh, logout; token validation with signing keys", "Authorization Code flow with PKCE for frontends"],
    ["I5", "KAVERI frontend → IAM (post switch)", "Re-issue tokens for additional charge and switch back", "Application-initiated action or token exchange (decision D3)"],
    ["I6", "IAM extensions → KAVERI Notification Service, e-KYC Integration Service, face / biometric provider", "Send OTP / PIN; Aadhaar e-KYC; DSR face / biometric verification", "Internal APIs; provider over secure channel"],
    ["I7", "IAM event listener → KAVERI audit store", "Forward authentication and admin events", "Asynchronous; no event loss on restart"],
    ["I8", "KAVERI → IAM Admin REST API (session revocation)", "Revoke sessions on suspension, deactivation, relieving, absence, Username correction", "Same service account as I1"],
    ["I9", "KAVERI migration tool → IAM Admin REST API", "Bulk load of Kaveri 2.0 citizens", "Run by Kaveri IT Cell; idempotent"],
]

OPERATIONS = [
    ["IAM hosting, clustering, database, backups, disaster recovery", "Kaveri IT Cell"],
    ["IAM version upgrades and security patching", "Kaveri IT Cell (with regression test by KAVERI development team)"],
    ["Realm configuration managed as code and promoted through environments", "Kaveri IT Cell"],
    ["Development, testing and versioning of IAM extensions (authenticators, required actions, mappers, event listener, theme)", "KAVERI development team"],
    ["Signing key rotation and TLS certificates", "Kaveri IT Cell"],
    ["SMS and email gateway contracts and availability", "Department / Kaveri IT Cell"],
    ["UIDAI AUA/KUA licence, Aadhaar Data Vault and e-KYC connectivity", "Department / Kaveri IT Cell"],
    ["Face / biometric authentication provider contract and availability", "Department / Kaveri IT Cell"],
    ["Monitoring and alerting for IAM, extensions and integrations I1–I9", "Kaveri IT Cell"],
    ["IAM admin console access control and periodic access review", "Kaveri IT Cell"],
]

DECISIONS = [
    ["D1", "Realm design", "Single realm for all user categories (recommended — required for the single Username namespace of FR-UM-004 / FR-UM-028) vs separate realms per category."],
    ["D2", "Runtime authorisation engine", "KAVERI authorisation component at the API gateway using the KAVERI Role–Module–Function mapping (recommended) vs the IAM platform's built-in authorisation services with resources and policies synchronised from KAVERI."],
    ["D3", "Post-switch mechanism", "Re-authentication through an application-initiated action that re-runs post selection (recommended) vs OAuth token exchange."],
    ["D4", "Role representation in IAM", "Roles placed in tokens by the protocol mapper only (recommended) vs also mirroring Role Master entries as IAM client roles."],
    ["D5", "Registration user interface", "IAM-hosted pages in the KAVERI theme (recommended) vs KAVERI-built pages calling IAM APIs."],
    ["D6", "Face / biometric provider", "Selection of provider and whether UIDAI face authentication is used for DSR Officers."],
    ["D7", "IAM product and support", "Selection of the IAM product, open-source vs commercially supported distribution, and supported version line."],
]

GLOSSARY = [
    ["IAM", "Identity and Access Management platform used by KAVERI 3.0 for identity, login, sessions and tokens."],
    ["Realm", "An isolated IAM space holding a set of users, login flows, clients and settings."],
    ["Client", "An application registered in IAM that uses it for login (e.g. KAVERI citizen portal, KAVERI departmental application, API gateway)."],
    ["Access token", "Signed token (JWT) issued by IAM after login and presented by frontends with every API request."],
    ["Claim", "A named value inside a token (e.g. Username, User Category, selected post, roles)."],
    ["Authenticator / login flow", "A step in a IAM login sequence (e.g. Captcha, OTP, face / biometric, post selection)."],
    ["Required action", "A task a user must complete at the next login before reaching the application (e.g. verify email, accept terms)."],
    ["Application-initiated action", "A required action started deliberately by the application (e.g. change mobile, switch post)."],
    ["Protocol mapper", "IAM component that adds claims to tokens."],
    ["Extension", "Custom code deployed into the IAM platform through its extension interfaces."],
    ["Admin REST API", "IAM's management API used by KAVERI to create and maintain users."],
    ["JWKS", "The published set of IAM public signing keys used to validate tokens."],
]

# FR-UM id -> (area, owner)
TRACE = {
    "FR-UM-001": ("A1", SHR), "FR-UM-002": ("A10", SHR), "FR-UM-003": ("A10", SHR), "FR-UM-004": ("A2", KCB),
    "FR-UM-005": ("A3", KCE), "FR-UM-006": ("A3", KCE), "FR-UM-007": ("A3", KCE), "FR-UM-008": ("A4", SHR),
    "FR-UM-009": ("A3", KCB), "FR-UM-010": ("A3", KCE), "FR-UM-011": ("A3", KCE), "FR-UM-012": ("A5", KCE),
    "FR-UM-013": ("A5", SHR), "FR-UM-014": ("A5", KAV), "FR-UM-015": ("—", RET), "FR-UM-016": ("A7", KAV),
    "FR-UM-017": ("A10", KAV), "FR-UM-018": ("A8", SHR), "FR-UM-019": ("A7", KAV), "FR-UM-020": ("A10", SHR),
    "FR-UM-021": ("A10", KAV), "FR-UM-022": ("A14", SHR), "FR-UM-023": ("A13", KAV), "FR-UM-024": ("A7", KAV),
    "FR-UM-025": ("A7", KAV), "FR-UM-026": ("A7", KAV), "FR-UM-027": ("A7", KAV), "FR-UM-028": ("A2", SHR),
    "FR-UM-029": ("A10", KAV), "FR-UM-030": ("A10", KAV), "FR-UM-031": ("—", RET), "FR-UM-032": ("A10", KAV),
    "FR-UM-033": ("A10", SHR), "FR-UM-034": ("A7", KAV), "FR-UM-035": ("A7", KAV), "FR-UM-036": ("A8", KAV),
    "FR-UM-037": ("A8", KAV), "FR-UM-038": ("A6", SHR), "FR-UM-039": ("A8", KAV), "FR-UM-040": ("A8", KAV),
    "FR-UM-041": ("A8", SHR), "FR-UM-042": ("A8", KAV), "FR-UM-043": ("A9", KAV), "FR-UM-044": ("A9", KAV),
    "FR-UM-045": ("A10", KAV), "FR-UM-046": ("A7", KAV), "FR-UM-047": ("A7", KAV), "FR-UM-048": ("A7", KAV),
    "FR-UM-049": ("A7", KAV), "FR-UM-050": ("A8", KAV), "FR-UM-051": ("A10", SHR), "FR-UM-052": ("A6", SHR),
    "FR-UM-053": ("A6", SHR), "FR-UM-054": ("A6", KAV), "FR-UM-055": ("—", RET), "FR-UM-056": ("A5", KCE),
    "FR-UM-057": ("A11", KAV), "FR-UM-058": ("A11", KAV), "FR-UM-059": ("A9", KAV), "FR-UM-060": ("A11", KAV),
    "FR-UM-061": ("—", RET), "FR-UM-062": ("A2", SHR), "FR-UM-063": ("A1", KCE), "FR-UM-064": ("A10", KAV),
    "FR-UM-065": ("A5", SHR), "FR-UM-066": ("A11", KAV), "FR-UM-067": ("—", RET), "FR-UM-068": ("A11", SHR),
    "FR-UM-069": ("A4", KCE), "FR-UM-070": ("A4", KCE), "FR-UM-071": ("A4", KCE), "FR-UM-072": ("A4", KCE),
    "FR-UM-073": ("A4", KCB), "FR-UM-074": ("A4", SHR), "FR-UM-075": ("A4", SHR), "FR-UM-076": ("A4", KCB),
    "FR-UM-077": ("A7", KAV), "FR-UM-078": ("A7", KAV), "FR-UM-079": ("A11", KAV), "FR-UM-080": ("A6", SHR),
    "FR-UM-081": ("A11", KAV), "FR-UM-082": ("A11", KAV), "FR-UM-083": ("A6", SHR), "FR-UM-084": ("A11", KAV),
    "FR-UM-085": ("A1", SHR), "FR-UM-086": ("A5", KCE), "FR-UM-087": ("A11", KAV), "FR-UM-088": ("A12", SHR),
    "FR-UM-089": ("A12", SHR), "FR-UM-090": ("A12", KCB), "FR-UM-091": ("A12", KCE), "FR-UM-092": ("A12", KCE),
    "FR-UM-093": ("A12", KAV), "FR-UM-094": ("A12", KAV), "FR-UM-095": ("A12", KAV), "FR-UM-096": ("A13", KAV),
}

TRACE_TITLES = {
    "FR-UM-001": "Citizen self-registration", "FR-UM-002": "DSR Officer creation", "FR-UM-003": "Other Department user creation",
    "FR-UM-004": "Unique Username, single namespace", "FR-UM-005": "Citizen login (OTP)", "FR-UM-006": "DSR login (face / biometric)",
    "FR-UM-007": "Other Department login (OTP)", "FR-UM-008": "Logout", "FR-UM-009": "No passwords",
    "FR-UM-010": "Login OTP to mobile only", "FR-UM-011": "Captcha before OTP", "FR-UM-012": "Citizen-only recovery",
    "FR-UM-013": "Profile view / update", "FR-UM-014": "Profile photo", "FR-UM-015": "Retired",
    "FR-UM-016": "Unified Role Master", "FR-UM-017": "DSR post assignment", "FR-UM-018": "Access restricted by role",
    "FR-UM-019": "Divisions and DSR roles", "FR-UM-020": "Create / suspend / deactivate users", "FR-UM-021": "Search users",
    "FR-UM-022": "Log admin actions", "FR-UM-023": "Account notifications", "FR-UM-024": "Sanctioned Posts Master",
    "FR-UM-025": "Configure sanctioned strength", "FR-UM-026": "Assign only sanctioned posts", "FR-UM-027": "Occupancy display",
    "FR-UM-028": "Single Role and User Master", "FR-UM-029": "Other Department single role", "FR-UM-030": "At least one post at creation",
    "FR-UM-031": "Retired", "FR-UM-032": "Role assignment workflows", "FR-UM-033": "Other Department End Date",
    "FR-UM-034": "Roles filtered by category", "FR-UM-035": "Seed roles", "FR-UM-036": "Module Master",
    "FR-UM-037": "Role–Module–Function mapping", "FR-UM-038": "Effective session access", "FR-UM-039": "Module Function Master",
    "FR-UM-040": "Resource Master", "FR-UM-041": "Runtime access enforcement", "FR-UM-042": "Application Admin maintains masters",
    "FR-UM-043": "DSR Officer Hierarchy Master", "FR-UM-044": "Hierarchy seed structure", "FR-UM-045": "Multiple concurrent posts",
    "FR-UM-046": "Posts Master", "FR-UM-047": "Post–Role mapping", "FR-UM-048": "Sanctioned Posts references",
    "FR-UM-049": "Division-specific posts", "FR-UM-050": "Mapping referential integrity", "FR-UM-051": "Application Admin actor",
    "FR-UM-052": "Login post selection", "FR-UM-053": "Additional charge after login", "FR-UM-054": "Post / charge display",
    "FR-UM-055": "Retired", "FR-UM-056": "Citizen lost-mobile reset", "FR-UM-057": "Transfer Out / relieving",
    "FR-UM-058": "Occupancy retained to Relieving Date", "FR-UM-059": "Office Hierarchy Master", "FR-UM-060": "Transfer In",
    "FR-UM-061": "Retired", "FR-UM-062": "Username derivation", "FR-UM-063": "Registration email + mobile OTP",
    "FR-UM-064": "KGID / Department Code validation", "FR-UM-065": "Admin-only mobile change (Other Dept)", "FR-UM-066": "Vacancy tests",
    "FR-UM-067": "Retired", "FR-UM-068": "Occupancy refresh job", "FR-UM-069": "OTP / PIN validity",
    "FR-UM-070": "OTP / PIN length", "FR-UM-071": "OTP / PIN attempts", "FR-UM-072": "Resend cooldown",
    "FR-UM-073": "Username lockout", "FR-UM-074": "Idle timeout", "FR-UM-075": "Absolute session limit",
    "FR-UM-076": "One session per Username", "FR-UM-077": "Division Master", "FR-UM-078": "Post–Office-Type mapping",
    "FR-UM-079": "Record temporary absence", "FR-UM-080": "Login blocked during absence", "FR-UM-081": "Absence keeps occupancy",
    "FR-UM-082": "Assign temporary charge", "FR-UM-083": "Temporary charge at login", "FR-UM-084": "Absence end",
    "FR-UM-085": "Aadhaar e-KYC", "FR-UM-086": "DSR mobile change after login", "FR-UM-087": "Relieving Reason",
    "FR-UM-088": "Citizen migration scope", "FR-UM-089": "Migrated Username = email ID", "FR-UM-090": "Migrated e-KYC status",
    "FR-UM-091": "First-login activation", "FR-UM-092": "Migrated lost mobile", "FR-UM-093": "Migration validation",
    "FR-UM-094": "Kaveri 2.0 cross-reference", "FR-UM-095": "Migration runs and reconciliation", "FR-UM-096": "Activation notification",
}


# ---------------------------------------------------------------------------
# Diagram
# ---------------------------------------------------------------------------

def make_diagram(path: Path) -> None:
    W, H = 2000, 1300
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    f_title = ImageFont.truetype(r"C:\Windows\Fonts\calibrib.ttf", 34)
    f_box = ImageFont.truetype(r"C:\Windows\Fonts\calibri.ttf", 23)
    f_boxb = ImageFont.truetype(r"C:\Windows\Fonts\calibrib.ttf", 24)
    f_lbl = ImageFont.truetype(r"C:\Windows\Fonts\calibrib.ttf", 21)

    def box(x0, y0, x1, y1, title, body, fill, outline):
        d.rounded_rectangle((x0, y0, x1, y1), radius=12, fill=fill, outline=outline, width=3)
        lines = [(title, f_boxb)] + [(t, f_box) for t in body]
        total = sum(28 for _ in lines)
        y = (y0 + y1) / 2 - total / 2
        for text, font in lines:
            w = d.textlength(text, font=font)
            d.text(((x0 + x1) / 2 - w / 2, y), text, font=font, fill="black")
            y += 28

    def arrow(p0, p1, label, both=False, label_at=0.5):
        d.line((p0, p1), fill="#404040", width=3)
        import math

        def head(a, b):
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            pts = [b, (b[0] - 18 * math.cos(ang - 0.4), b[1] - 18 * math.sin(ang - 0.4)),
                   (b[0] - 18 * math.cos(ang + 0.4), b[1] - 18 * math.sin(ang + 0.4))]
            d.polygon(pts, fill="#404040")

        head(p0, p1)
        if both:
            head(p1, p0)
        if not label:
            return
        mx = p0[0] + (p1[0] - p0[0]) * label_at
        my = p0[1] + (p1[1] - p0[1]) * label_at
        lines = label.split("\n")
        widths = [d.textlength(t, font=f_lbl) for t in lines]
        bw, bh = max(widths) + 14, 25 * len(lines) + 8
        d.rectangle((mx - bw / 2, my - bh / 2, mx + bw / 2, my + bh / 2), fill="white", outline="#808080")
        for i, t in enumerate(lines):
            d.text((mx - widths[i] / 2, my - bh / 2 + 4 + 25 * i), t, font=f_lbl, fill="#1F3A5F")

    # Containers
    d.rounded_rectangle((30, 30, 790, 1120), radius=18, fill="#F3F9EF", outline="#548235", width=4)
    d.text((50, 45), "KAVERI 3.0 application", font=f_title, fill="#375623")
    d.rounded_rectangle((1210, 30, 1970, 1120), radius=18, fill="#EEF4FB", outline="#2F5597", width=4)
    d.text((1230, 45), "IAM platform", font=f_title, fill="#1F3A5F")

    g_fill, g_out = "#E2EFDA", "#70AD47"
    b_fill, b_out = "#DDEBF7", "#5B9BD5"
    LX0, LX1, RX0, RX1 = 70, 750, 1250, 1930
    rows = {"r1": (110, 210), "r2": (240, 340), "r3": (370, 470), "r4": (500, 600),
            "r5": (630, 750), "r6": (780, 880), "r7": (910, 1010), "r8": (1030, 1100)}

    box(LX0, rows["r1"][0], LX1, rows["r1"][1], "Frontends", ["Citizen portal, departmental application"], g_fill, g_out)
    box(LX0, rows["r2"][0], LX1, rows["r2"][1], "API gateway + authorisation", ["Role → Module Function → Resource (A8)"], g_fill, g_out)
    box(LX0, rows["r3"][0], LX1, rows["r3"][1], "User admin screens", ["DSR, Other Department, Application Admin (A10)"], g_fill, g_out)
    box(LX0, rows["r4"][0], LX1, rows["r4"][1], "Migration tool", ["Kaveri 2.0 → 3.0 citizens (A12)"], g_fill, g_out)
    box(LX0, rows["r5"][0], LX1, rows["r5"][1], "Post and Occupancy Service", ["Roles, posts, occupancy, hierarchy,", "absence, charges (A6, A7, A9, A11)"], g_fill, g_out)
    box(LX0, rows["r6"][0], LX1, rows["r6"][1], "Notification Service", ["SMS and email (A13)"], g_fill, g_out)
    box(LX0, rows["r7"][0], LX1, rows["r7"][1], "e-KYC Integration Service", ["UIDAI connectivity, Aadhaar Data Vault (A1)"], g_fill, g_out)
    box(LX0, rows["r8"][0], LX1, rows["r8"][1], "Audit store and reports (A14)", [], g_fill, g_out)

    box(RX0, rows["r1"][0], RX1, rows["r2"][1], "OpenID Connect, sessions, tokens", ["Login redirect, access tokens, signing keys", "Idle 10 min, max 4 h, one session (A4)"], b_fill, b_out)
    box(RX0, rows["r3"][0], RX1, rows["r3"][1], "Admin REST API", ["Users, attributes, enable / disable, sessions"], b_fill, b_out)
    box(RX0, rows["r4"][0], RX1, rows["r4"][1], "User store (single realm)", ["Username, mobile, email, attributes (A2)"], b_fill, b_out)
    box(RX0, rows["r5"][0], RX1, rows["r7"][1], "Login flows and extensions",
        ["Captcha, SMS OTP, face / biometric (A3)", "Aadhaar e-KYC step, lost-mobile reset (A1, A5)",
         "Post selection + claims mapper (A6)", "Required actions: activation, contact change", "(A5, A12)"], b_fill, b_out)
    box(RX0, rows["r8"][0], RX1, rows["r8"][1], "Event listener (A14)", [], b_fill, b_out)

    def cy(r):
        return (rows[r][0] + rows[r][1]) / 2

    arrow((LX1, cy("r1")), (RX0, cy("r1")), "I4 Login / tokens\nI5 Post switch", both=True)
    arrow((LX1, cy("r2")), (RX0, cy("r2")), "I4 Validate token (keys)")
    arrow((LX1, cy("r3")), (RX0, cy("r3")), "I1 Manage users\nI8 Revoke sessions")
    arrow((LX1, cy("r4")), (RX0, cy("r3") + 30), "I9 Bulk load", label_at=0.45)
    arrow((RX0, cy("r5")), (LX1, cy("r5")), "I2 / I3 Posts, absence,\nroles at login")
    arrow((RX0, cy("r6")), (LX1, cy("r6")), "I6 Send OTP / PIN")
    arrow((RX0, cy("r7")), (LX1, cy("r7")), "I6 Aadhaar e-KYC")
    arrow((RX0, cy("r8")), (LX1, cy("r8")), "I7 Auth and admin events")

    # External systems
    ext = [(70, "SMS / email gateways", "called by Notification Service"),
           (430, "UIDAI (Aadhaar e-KYC)", "called by e-KYC Integration Service"),
           (1250, "Face / biometric provider", "called by DSR login extension")]
    for x, label, sub in ext:
        box(x, 1165, x + 330, 1265, label, [sub], "#F2F2F2", "#7F7F7F")
    arrow((235, 1120), (235, 1165), "")
    arrow((595, 1120), (595, 1165), "")
    arrow((1415, 1120), (1415, 1165), "")
    img.save(path)


# ---------------------------------------------------------------------------
# Document helpers
# ---------------------------------------------------------------------------

def shade(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def repeat_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    tr_pr.append(el)


def cell_text(cell, text: str, bold=False, size=9, color: RGBColor | None = None) -> None:
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = color


def add_table(doc, header: list[str], rows: list[list[str]], widths_cm: list[float], owner_col: int | None = None):
    table = doc.add_table(rows=1, cols=len(header))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(header):
        c = table.rows[0].cells[i]
        cell_text(c, h, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
        shade(c, HEADER_FILL)
    repeat_header(table.rows[0])
    for values in rows:
        cells = table.add_row().cells
        for i, v in enumerate(values):
            cell_text(cells[i], v, bold=(owner_col == i))
            if owner_col == i and v in OWNER_FILL:
                shade(cells[i], OWNER_FILL[v])
    for row in table.rows:
        for i, w in enumerate(widths_cm):
            row.cells[i].width = Cm(w)
    doc.add_paragraph()
    return table


def add_matrix(doc) -> None:
    header = ["ID", "Capability", "Owner", "KAVERI application responsibility", "IAM responsibility", "Source of truth", "BRD reference"]
    widths = [1.3, 3.8, 2.3, 6.1, 6.1, 2.8, 2.6]
    table = doc.add_table(rows=1, cols=len(header))
    table.style = "Table Grid"
    for i, h in enumerate(header):
        c = table.rows[0].cells[i]
        cell_text(c, h, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
        shade(c, HEADER_FILL)
    repeat_header(table.rows[0])
    for area, rows in MATRIX:
        cells = table.add_row().cells
        merged = cells[0].merge(cells[-1])
        cell_text(merged, area, bold=True, size=10, color=NAVY)
        shade(merged, AREA_FILL)
        for values in rows:
            cells = table.add_row().cells
            for i, v in enumerate(values):
                cell_text(cells[i], v, bold=(i == 2))
            shade(cells[2], OWNER_FILL[values[2]])
    for row in table.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Cm(w)
    doc.add_paragraph()


def heading(doc, text: str, level: int) -> None:
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = NAVY


def para(doc, text: str) -> None:
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)


def bullets(doc, items: list[str]) -> None:
    for item in items:
        doc.add_paragraph(item, style="List Bullet")


def set_landscape(section) -> None:
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width, section.page_height = Cm(29.7), Cm(21.0)
    for side in ("left_margin", "right_margin"):
        setattr(section, side, Cm(1.8))
    section.top_margin = section.bottom_margin = Cm(1.8)


def set_portrait(section) -> None:
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width, section.page_height = Cm(21.0), Cm(29.7)
    section.left_margin = section.right_margin = Cm(2.0)
    section.top_margin = section.bottom_margin = Cm(2.0)


def header_footer(section) -> None:
    hp = section.header.paragraphs[0]
    hp.text = "Kaveri 3.0  |  IAM Ownership Matrix  |  KAVERI application and IAM"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for r in hp.runs:
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    fp = section.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = fp.add_run()
    for tag, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), tag)
            run._r.append(fc)
        else:
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = text
            run._r.append(it)
    run.font.size = Pt(9)


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    make_diagram(DIAGRAM)

    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10.5)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

    sec = doc.sections[0]
    set_portrait(sec)
    header_footer(sec)

    heading(doc, "Kaveri 3.0 — Identity and Access Management Ownership Matrix", 0)
    para(doc, "KAVERI application and IAM: roles and ownership by area")

    heading(doc, "Document Control", 2)
    add_table(doc, ["Field", "Value"], [
        ["Document ID", "DD-K3-IAM-001"],
        ["Version", DOC_VERSION],
        ["Status", "Draft for review"],
        ["Related document", BRD_REF],
        ["Author (BA)", "Nandha Kumar"],
        ["Product Owner", "M V Prashanth"],
        ["Domain expert / reviewer", "Prabhakar Naik"],
        ["Target audience", "Solution architects, KAVERI development teams, Kaveri IT Cell, security reviewers"],
        ["Last updated", DOC_DATE],
    ], [5.0, 12.0])

    heading(doc, "Version History", 2)
    add_table(doc, ["Version", "Date", "Author", "Description"], [
        [DOC_VERSION, DOC_DATE, "Nandha Kumar", "Initial version: ownership principles, responsibility matrix (areas A1–A15), data ownership, integration points, operational ownership, open decisions and BRD traceability."],
    ], [2.0, 2.5, 3.0, 9.5])

    heading(doc, "1. Purpose and Scope", 1)
    heading(doc, "1.1 Purpose", 2)
    para(doc, PURPOSE)
    heading(doc, "1.2 Scope", 2)
    para(doc, "In scope:")
    bullets(doc, SCOPE_IN)
    para(doc, "Out of scope:")
    bullets(doc, SCOPE_OUT)
    heading(doc, "1.3 Platform constraint", 2)
    para(doc, (
        "A dedicated Identity and Access Management (IAM) platform is used for KAVERI 3.0. All user "
        "identities of all categories — Citizens, DSR Officers and Other Department users — are held "
        "in the IAM platform, and all KAVERI frontends and APIs rely on it for login, sessions and "
        "tokens. Requirements that the IAM platform does not meet through configuration are met by "
        "IAM extensions or by KAVERI services integrated with the IAM platform, as assigned in this "
        "document."
    ))

    heading(doc, "2. Ownership Principles", 1)
    add_table(doc, ["#", "Principle", "Meaning"], [list(p) for p in PRINCIPLES], [1.2, 5.0, 10.8])

    heading(doc, "3. Ownership Categories", 1)
    add_table(doc, ["Owner", "Meaning"], [list(c) for c in CATEGORIES], [4.0, 13.0], owner_col=0)

    heading(doc, "4. Overview", 1)
    para(doc, (
        "The figure shows the KAVERI application components (left) and the IAM components (right), "
        "the integration points I1–I9 between them (Section 7), and the external providers. Area codes "
        "(A1–A15) refer to the responsibility matrix in Section 5."
    ))
    doc.add_picture(str(DIAGRAM), width=Cm(17.0))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    set_landscape(sec)
    heading(doc, "5. Responsibility Matrix by Area", 1)
    para(doc, "Owner colours: blue = IAM (built-in); purple = IAM (extension); green = KAVERI application; amber = Shared.")
    add_matrix(doc)

    heading(doc, "6. Data Ownership (Source of Truth)", 1)
    add_table(doc, ["Data item", "Source of truth (owner)", "How the other side obtains it"],
              DATA_OWNERSHIP, [7.5, 6.0, 12.0])

    heading(doc, "7. Integration Points", 1)
    add_table(doc, ["#", "Direction", "Purpose", "Security / notes"], INTEGRATIONS, [1.2, 9.0, 8.0, 7.3])

    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    set_portrait(sec)
    heading(doc, "8. Operational Ownership", 1)
    add_table(doc, ["Responsibility", "Owner"], OPERATIONS, [11.5, 5.5])

    heading(doc, "9. Open Decisions", 1)
    para(doc, "Recommended options are marked; each decision shall be closed by the Product Owner and Kaveri IT Cell before IAM solution design is baselined.")
    add_table(doc, ["#", "Decision", "Options"], DECISIONS, [1.2, 4.3, 11.5])

    heading(doc, "10. Glossary", 1)
    add_table(doc, ["Term", "Definition"], GLOSSARY, [4.5, 12.5])

    heading(doc, "Appendix A. BRD Traceability", 1)
    para(doc, f"Every functional requirement of {BRD_REF} with its responsibility area and owner. Retired requirements are listed for completeness.")
    trace_rows = [[fr, TRACE_TITLES[fr], area, owner] for fr, (area, owner) in sorted(TRACE.items())]
    add_table(doc, ["Req ID", "Requirement (short title)", "Area", "Owner"], trace_rows, [2.6, 8.4, 1.8, 4.2], owner_col=3)

    heading(doc, "Approval", 1)
    para(doc, "By signing below, the stakeholders confirm they have reviewed and approved this document.")
    add_table(doc, ["Name", "Role", "Signature", "Date"], [
        ["M V Prashanth", "Product Owner", "", ""],
        ["Prabhakar Naik", "Domain expert / reviewer", "", ""],
        ["", "Kaveri IT Cell", "", ""],
        ["", "Solution Architect", "", ""],
    ], [4.5, 5.0, 4.0, 3.5])

    doc.save(str(DST))
    print(f"Saved {DST}")


if __name__ == "__main__":
    main()
