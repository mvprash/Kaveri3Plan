# Low-Level Design (LLD)

## User Management — Platform Service

| Field | Value |
|--------|--------|
| **Document ID** | LLD-K3-UM-001 |
| **Version** | 1.0 (Draft) |
| **Status** | Draft for Tech Lead / Architecture review |
| **Module** | User Management & RBAC |
| **Parent HLD** | Platform HLD (TBD) — this service is Phase-1 platform foundation |
| **Source BRD** | `Finalized BRD/User Management/BRD_User_Management_v4.16.docx` (BRD-K3-UM-001) |
| **Source ERD** | `Finalized BRD/User Management/ERD_User_Management_v2.0.docx` (ERD-K3-UM-001) |
| **Process diagrams** | `Finalized BRD/User Management/ProcessDiagrams/User_Management/` (P-01 … P-13, S-01 … S-06) |
| **Audience** | Tech Leads, Backend/Frontend engineers, QA, Integration, Security |
| **Last updated** | 2026-09-01 |

---

## Document control

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 2026-09-01 | Architecture | Initial LLD — single `user-management-service` + `db_um`; derived from BRD v4.16 and ERD v2.0 |

**Related documents**

| ID | Title |
|----|--------|
| BRD-K3-UM-001 v4.16 | Business Requirements — User Management |
| ERD-K3-UM-001 v2.0 | Logical Entity-Relationship Diagram |
| LLD-K3-UM-001 | This document |

---

## 1. Scope

### 1.1 In scope

Low-level design for the **User Management platform microservice** as a **single deployable service** with **one dedicated database** (`db_um`):

- Citizen self-registration (P-01), departmental user creation (DSR / Other Department)
- Passwordless authentication: Username + Captcha + OTP (+ Biometrics for departmental users)
- Session management (one active session, idle 15 min, absolute 8 h — FR-UM-074–FR-UM-076)
- DSR post selection at login (FR-UM-052), additional charge (FR-UM-053), header display (FR-UM-054)
- Unified Role Master, Posts Master, Office Hierarchy, Division Master, Sanctioned Posts
- Post–Role mapping, Post–Office-Type validation (FR-UM-078)
- Transfer Out / Relieving (FR-UM-057–FR-UM-058), Transfer In (FR-UM-060–FR-UM-061, FR-UM-067)
- Temporary Absence and Temporary Charge (FR-UM-079–FR-UM-084)
- RBAC: Module Master, Module Function, Resource Master, Role–Module–Function mapping
- Runtime access enforcement (FR-UM-041) — deny-by-default unless `is_public`
- Application Admin maintenance APIs (FR-UM-042, FR-UM-051)
- Citizen lost-mobile reset (FR-UM-056); departmental mobile change (FR-UM-065)
- Occupancy refresh midnight job (FR-UM-068); Other Department auto-deactivate (FR-UM-033)
- Audit log (7-year retention); MIS/reporting read APIs (BRD §8)

### 1.2 Out of scope

- SSO / third-party IdP (BRD §1.4 — future phase)
- Domain module business data (Marriage, Document Registration, etc.)
- Khajane-II / Treasury DDO tables
- UI pixel layouts / Figma (BRD UI section)
- Separate audit-compliance microservice in Phase 1 — audit is stored in `db_um.audit_log`; optional async fan-out to platform SIEM later
- Password storage — explicitly forbidden (FR-UM-009)

### 1.3 Architecture decision — one service, one database

| Decision | Rationale |
|----------|-----------|
| **Single microservice** `user-management-service` | BRD mandates one User Master and one Role Master (FR-UM-016, FR-UM-028); occupancy, RBAC, and auth share transactional invariants (capacity, session claims, audit) |
| **Single database** `db_um` | ERD v2.0 logical model maps to one PostgreSQL schema; cross-entity FK integrity (Post–Role, Sanctioned Post, Occupancy) requires ACID within one DB |
| **Modular monolith internally** | Service is split into **internal packages** (§4) for maintainability; no inter-package network calls |
| **Platform consumption** | Other Kaveri services validate JWT issued by this service; optional embedded auth middleware library shares FR-UM-041 resource-matching logic |

---

## 2. Microservices architecture (platform context)

### 2.1 Container view

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  Edge: WAF / API Gateway (TLS 1.3)                                          │
└─────────────────────────────────────────────────────────────────────────────┘
         │                    │                         │
         ▼                    ▼                         ▼
┌─────────────────┐  ┌─────────────────┐    ┌─────────────────────┐
│ Citizen Portal  │  │ Officer Workbench│    │ Admin / App Admin UI │
└────────┬────────┘  └────────┬─────────┘    └──────────┬──────────┘
         │                    │                         │
         ▼                    ▼                         ▼
┌─────────────────┐  ┌─────────────────┐    ┌─────────────────────┐
│ citizen-bff     │  │ officer-bff     │    │ admin-bff           │
│ (thin aggregate)│  │ (thin aggregate)│    │ (thin aggregate)    │
└────────┬────────┘  └────────┬─────────┘    └──────────┬──────────┘
         │                    │                         │
         └────────────────────┼─────────────────────────┘
                              ▼
              ┌───────────────────────────────────┐
              │   user-management-service         │  ◄── THIS LLD
              │   (AuthN, AuthZ, Users, RBAC,    │
              │    Org, Occupancy, Audit)         │
              └───────────────┬───────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
   ┌──────────┐        ┌──────────┐         ┌─────────────┐
   │  db_um   │        │  Redis   │         │ Object Store│
   │ Postgres │        │ sessions │         │ (photos,    │
   │   (HA)   │        │ OTP lock │         │  orders,    │
   └──────────┘        └──────────┘         │  letters)   │
                                            └─────────────┘

External adapters (HTTP / SDK):
  SMS Gateway ──► OTP dispatch (FR-UM-010, NFR-UM-02 ≤ 5 s)
  Email Gateway ► registration / reset PIN / notifications
  Captcha       ► internal or vendor
  Biometric SDK ► UIDAI-compliant verify (FR-UM-006/007)
  notification-service (optional async) ◄── domain events
```

### 2.2 Downstream consumers (other Kaveri microservices)

| Consumer | Integration | What it needs from UM |
|----------|-------------|------------------------|
| Marriage, Document Reg, EC, … | JWT validation + optional introspection | `sub`, `userCategory`, `roles[]`, `officeCode`, `postCode`, `functionClaims[]`, `officeSpan[]` |
| API Gateway | JWT verify + resource policy cache | Public resource list from `resource_master` |
| MIS / reporting | Read APIs or event subscription | Audit, occupancy, login reports (BRD §8) |
| notification-service | Events `UserAccountCreated`, … | SMS/email templates (FR-UM-023) |

**No other service owns user identity, roles, posts, or sessions.**

### 2.3 Service catalogue (Phase 1 — User Management slice)

| # | Service | Role | Database |
|---|---------|------|----------|
| 1 | **user-management-service** | Identity, auth, RBAC, org masters, occupancy | **db_um** |
| 2 | citizen-bff | Portal auth/registration/profile proxy | — |
| 3 | officer-bff | DSR login, post pick, transfer workflows | — |
| 4 | admin-bff | User admin, masters, Application Admin | — |
| 5 | notification-service *(platform)* | SMS/email delivery | db_notify |
| 6 | integration-gateway *(optional)* | SMS/email/captcha circuit breakers | — |

---

## 3. Design conventions

| Convention | Rule |
|------------|------|
| IDs | UUID v4 for `user_id`, `session_id`, `occupancy_id`, `audit_id`; business keys: `username`, `post_code`, `office_code`, `role_id` (surrogate), `module_code` |
| Time | Store `TIMESTAMPTZ` (UTC); business rules evaluated in **Asia/Kolkata (IST)** — FR-UM-061, FR-UM-068, FR-UM-084 |
| Locale | API error messages EN + KN |
| Auth | Bearer JWT (RS256); gateway validates signature; claims in §3.1 |
| Idempotency | Header `Idempotency-Key` on POST creating users, occupancies, transfers |
| Correlation | Header `X-Correlation-Id` → `audit_log.correlation_id` |
| Errors | Problem+JSON (`type`, `title`, `status`, `detail`, `errorCode`, `traceId`) |
| Pagination | `page`, `size`, `sort` on list APIs |
| Soft delete | `is_active` on masters; user **deactivate** not delete; `audit_log` append-only |
| PII | Mask mobile in logs; never store OTP/PIN/security answers clear |

### 3.1 JWT access token claims (issued after successful login)

```json
{
  "sub": "uuid-user-id",
  "username": "citizen123",
  "userCategory": "CITIZEN | DSR_OFFICER | OTHER_DEPARTMENT",
  "sessionId": "uuid",
  "roles": ["Citizen"],
  "officeCode": "OFF-SRO-YESH",
  "officeName": "Sub-Registrar Office Yeshwanthapura",
  "postCode": "POST-SR",
  "postName": "Sub-Registrar (SR)",
  "assignedOccupancyId": "uuid",
  "additionalCharge": {
    "active": false,
    "postCode": null,
    "officeCode": null
  },
  "temporaryCharge": {
    "active": false,
    "coveredPostCode": null,
    "coveredOfficeCode": null
  },
  "functionClaims": ["MARRIAGE_REG:VIEW", "MARRIAGE_REG:ADD"],
  "officeSpan": ["OFF-SRO-YESH", "OFF-SRO-JAYA"],
  "jurisdictionIds": ["OFF-SRO-YESH"],
  "iat": 0,
  "exp": 0
}
```

- **Citizen / Other Department:** `postCode`, `assignedOccupancyId` null; roles from `user_role`.
- **DSR Officer:** roles resolved from `post_role_map` for selected occupancy (FR-UM-052); if additional charge active, `functionClaims` from additional-charge post only (FR-UM-038); if temporary charge selected at login (FR-UM-083), claims from covered post.
- Token TTL = min(session absolute expiry, 15 min sliding refresh window).

---

## 4. Internal component design (`user-management-service`)

Single deployable; **hexagonal / layered** per package:

```text
user-management-service/
├── api/                    REST controllers (public, citizen, officer, admin, internal)
├── application/            Use-cases / command handlers
├── domain/
│   ├── identity/           User, UserRole, SecurityAnswer
│   ├── auth/               Login, OTP, Session, Captcha, Lockout
│   ├── org/                Division, OfficeType, OfficeHierarchy, Posts, OfficerHierarchy
│   ├── establishment/      SanctionedPost, PostRoleMap, PostOfficeTypeAllowed
│   ├── occupancy/          PostOccupancy, Transfer, Relieving, TempAbsence, TempCharge
│   ├── rbac/               Role, Module, ModuleFunction, Resource, RoleModuleFunction
│   └── audit/              AuditLog
├── ports/                  Repository & adapter interfaces
└── adapters/
    ├── persistence/        JPA / jOOQ → db_um
    ├── redis/              Session cache, rate limits
    ├── sms/                SMS OTP adapter
    ├── email/              Email OTP / PIN adapter
    ├── captcha/            Captcha verify
    ├── biometric/          UIDAI SDK wrapper
    └── events/             Outbox → Kafka (optional)
```

### 4.1 Package responsibilities

| Package | Owns | Key FRs |
|---------|------|---------|
| `identity` | Registration, profile, user CRUD, USER_ROLE | FR-UM-001–004, FR-UM-013–014, FR-UM-020–021, FR-UM-029, FR-UM-033–035, FR-UM-055, FR-UM-062–065 |
| `auth` | Login flow, OTP challenge, session, logout, lockout | FR-UM-005–012, FR-UM-052–054, FR-UM-069–076 |
| `org` | Division, Office, Posts, Officer hierarchy | FR-UM-043–044, FR-UM-046, FR-UM-049, FR-UM-059, FR-UM-077–078 |
| `establishment` | Sanctioned strength, Post–Role, capacity display | FR-UM-024–027, FR-UM-047–048, FR-UM-050, FR-UM-066 |
| `occupancy` | Assign, transfer, relieve, temp absence/charge | FR-UM-017, FR-UM-026, FR-UM-030, FR-UM-045, FR-UM-057–061, FR-UM-067, FR-UM-079–084 |
| `rbac` | Masters + runtime enforcement middleware | FR-UM-016, FR-UM-018, FR-UM-036–042, FR-UM-050–051 |
| `audit` | Append-only audit | FR-UM-022, NFR-UM-01 |
| `jobs` | Schedulers | FR-UM-033, FR-UM-068, FR-UM-084 |

### 4.2 BFF responsibilities (thin — no business logic)

| BFF | Routes prefix | Aggregates |
|-----|---------------|------------|
| `citizen-bff` | `/api/citizen/um` | Registration wizard, login, profile, lost-mobile reset |
| `officer-bff` | `/api/officer/um` | Login, post selection, additional charge, transfer workflows, temp absence |
| `admin-bff` | `/api/admin/um` | User search, create/edit DSR/OD, masters, reports, Application Admin RBAC config |

---

## 5. Authentication & session flows

### 5.1 Login state machine (all categories)

```text
CAPTCHA_REQUIRED
  → USERNAME_LOOKUP
  → [locked?] ACCOUNT_LOCKED (FR-UM-073)
  → OTP_DISPATCHED
  → OTP_VERIFY
  → [DSR/OD] BIOMETRIC_REQUIRED
  → [DSR multi-occupancy] POST_SELECTION (FR-UM-052)
  → [DSR temp charge options] TEMP_CHARGE_SELECTION (FR-UM-083)
  → SESSION_ACTIVE
```

### 5.2 Citizen registration (P-01)

```text
Citizen → citizen-bff → POST /registration/start
  → OTP email + mobile (parallel, FR-UM-063)
  → POST /registration/verify-otps
  → POST /registration/security-answers (5 distinct, FR-UM-055)
  → POST /registration/complete → USER_MASTER + USER_ROLE + AUDIT
  → notify UserAccountCreated
```

### 5.3 DSR login post selection (P-05)

After OTP + biometric:

1. Load `post_occupancy` where `status IN (Active)` and `joining_date <= today IST` and not blocked by temp absence (FR-UM-080).
2. Include temporary-charge options where applicable (FR-UM-083).
3. If count = 1 → auto-select; if > 1 → officer picks (label: `Role — Post Name — Office Name (Office Code)`).
4. Persist `user_session.assigned_occupancy_id`; compute JWT claims.

### 5.4 Additional charge (P-06, session-only)

- **Not** a `post_occupancy` row (FR-UM-053).
- Query subordinate posts from `officer_hierarchy_node` where same `office_code` as session and `sanctioned_post.occupied_count = 0` (FR-UM-066(b)).
- Store on `user_session.add_charge_post_code` + `add_charge_office_code`.
- Switch-back clears additional charge on session; audit `AdditionalChargeCleared`.

### 5.5 Session rules

| Rule | Implementation |
|------|----------------|
| One active session per username (FR-UM-076) | `user_session.user_id` unique among active; new login invalidates prior + Redis pub/sub kick |
| Idle 15 min (FR-UM-074) | `last_activity_at` updated per request; job or filter expires |
| Absolute 8 h (FR-UM-075) | `expires_at = login_at + 8h IST` |
| Last-login-wins | Transaction: end old session → create new |

---

## 6. RBAC runtime enforcement (FR-UM-041)

### 6.1 Algorithm (shared library + gateway plugin)

```text
1. If resource.is_public → ALLOW
2. Resolve HTTP method + path → resource_master (longest path_pattern match)
3. If no match → DENY (non-public)
4. Resolve module_function from resource.function_id
5. Collect session role IDs:
     Citizen/OD → user_role
     DSR → post_role_map(assigned post) OR additional-charge post OR temp-charge covered post
6. If any role has role_module_function for that function_id → ALLOW
7. Else if Application Admin principal (FN-UM-ADMIN) → ALLOW admin routes only
8. Else → DENY + audit AccessDenied
```

### 6.2 Application Admin (FR-UM-051)

- Seeded deployment principal — **not** in `role_master`, **not** created via User Master workflow.
- Authenticates via break-glass / cert / configured system account (environment-specific).
- Holds `FN-UM-ADMIN` function claim outside normal RMF seeding.
- Maintains Module / Function / Resource / Role–Module–Function masters (FR-UM-042).

---

## 7. API design

Base paths:

- Citizen BFF: `/api/citizen/um`
- Officer BFF: `/api/officer/um`
- Admin BFF: `/api/admin/um`
- Internal (mTLS): `/internal/um/v1`

### 7.1 Authentication APIs

#### POST `/api/citizen/um/auth/login/start`

```json
{ "username": "citizen123", "captchaToken": "...", "captchaAnswer": "..." }
```

→ Validates captcha (FR-UM-011); dispatches login OTP to mobile only (FR-UM-010).

Response:

```json
{
  "challengeId": "uuid",
  "maskedMobile": "******3210",
  "expiresInSeconds": 300,
  "resendAvailableInSeconds": 30
}
```

#### POST `/api/citizen/um/auth/login/verify`

```json
{ "challengeId": "uuid", "otp": "123456" }
```

→ `200` + `{ "accessToken", "refreshToken", "sessionId", "user" }` or `401` increment fail count (FR-UM-071, FR-UM-073).

#### POST `/api/officer/um/auth/login/verify`

Same as citizen + biometric payload:

```json
{
  "challengeId": "uuid",
  "otp": "123456",
  "biometricTransactionId": "uidai-txn-ref"
}
```

#### POST `/api/officer/um/auth/login/select-post`

```json
{ "sessionId": "uuid", "occupancyId": "uuid" }
```

or for temporary charge (FR-UM-083):

```json
{ "sessionId": "uuid", "temporaryChargeId": "uuid" }
```

#### POST `/api/officer/um/auth/additional-charge/activate`

```json
{ "postCode": "POST-FDA-ENF", "officeCode": "OFF-SRO-YESH" }
```

Guard: subordinate post; `occupied_count = 0`; same office.

#### POST `/api/*/um/auth/logout`

Terminates session (FR-UM-008).

### 7.2 Registration & recovery

#### POST `/api/citizen/um/registration/start`

Headers: `Idempotency-Key`

#### POST `/api/citizen/um/registration/verify-contacts`

Dual OTP verify (FR-UM-063).

#### POST `/api/citizen/um/registration/complete`

Includes 5 security Q&A pairs (FR-UM-055).

#### POST `/api/citizen/um/recovery/lost-mobile/start`

Citizen only (FR-UM-056).

#### POST `/api/citizen/um/recovery/lost-mobile/verify-questions`

3 of 5 random questions.

#### POST `/api/citizen/um/recovery/lost-mobile/verify-pin`

PIN sent to registered email; then new mobile OTP.

### 7.3 Profile

#### GET `/api/citizen/um/profile`

#### PATCH `/api/citizen/um/profile`

Citizen may update mobile/email (FR-UM-013); new mobile requires OTP.

#### PATCH `/api/admin/um/users/{userId}/mobile`

Departmental mobile change (FR-UM-065) — admin only, reason required.

### 7.4 User administration

#### GET `/api/admin/um/users`

Query: `username`, `userCategory`, `status`, `officeCode`, `roleId`, `page`, `size` (FR-UM-021).

#### POST `/api/admin/um/users/dsr`

Create DSR officer (FR-UM-002) with step-by-step role/post assignment (FR-UM-032).

#### POST `/api/admin/um/users/other-department`

Create OD user — exactly one role (FR-UM-029), optional `accountEndDate` (FR-UM-033).

#### PATCH `/api/admin/um/users/{userId}/status`

Suspend / deactivate with reason (FR-UM-020).

### 7.5 Organisation & establishment masters

| Method | Path | FR |
|--------|------|-----|
| CRUD | `/api/admin/um/masters/divisions` | FR-UM-077 |
| CRUD | `/api/admin/um/masters/office-types` | FR-UM-059 |
| CRUD | `/api/admin/um/masters/offices` | FR-UM-059 |
| CRUD | `/api/admin/um/masters/posts` | FR-UM-046, FR-UM-049 |
| CRUD | `/api/admin/um/masters/officer-hierarchy` | FR-UM-043–044 |
| CRUD | `/api/admin/um/masters/post-office-type-allowed` | FR-UM-078 |
| CRUD | `/api/admin/um/masters/sanctioned-posts` | FR-UM-024–025, FR-UM-048 |
| CRUD | `/api/admin/um/masters/post-role-map` | FR-UM-047, FR-UM-050 |
| GET | `/api/admin/um/masters/sanctioned-posts/{postCode}/{officeCode}/capacity` | FR-UM-027, FR-UM-066 |

### 7.6 Occupancy & transfer

#### POST `/api/officer/um/occupancies/assign`

Initial assignment at user creation or new post (FR-UM-017, FR-UM-030).

#### POST `/api/officer/um/occupancies/transfer-out`

Relieving (FR-UM-057); retains mapping through relieving date EOD IST (FR-UM-058).

#### POST `/api/officer/um/occupancies/transfer-in`

Transfer In (FR-UM-060); supports reserved capacity (FR-UM-067).

#### POST `/api/officer/um/temporary-absence`

Record absence (FR-UM-079); blocks login (FR-UM-080).

#### POST `/api/officer/um/temporary-charge`

Assign temp charge (FR-UM-082).

### 7.7 RBAC masters (Application Admin)

| Method | Path | FR |
|--------|------|-----|
| CRUD | `/api/admin/um/rbac/roles` | FR-UM-016, FR-UM-035 |
| CRUD | `/api/admin/um/rbac/modules` | FR-UM-036 |
| CRUD | `/api/admin/um/rbac/module-functions` | FR-UM-039 |
| CRUD | `/api/admin/um/rbac/resources` | FR-UM-040 |
| CRUD | `/api/admin/um/rbac/role-module-functions` | FR-UM-037, FR-UM-050 |
| POST | `/api/admin/um/rbac/enforcement/check` | Internal simulate FR-UM-041 |

### 7.8 Internal service APIs (for other microservices)

#### GET `/internal/um/v1/sessions/validate`

Headers: `Authorization: Bearer`

Returns current claims + `active: true|false`.

#### GET `/internal/um/v1/users/{userId}/summary`

For display in domain modules.

#### GET `/internal/um/v1/offices/{officeCode}/span`

Returns descendant office codes (FR-UM-059) for jurisdiction filtering.

### 7.9 Reporting APIs (BRD §8)

| GET path | Report |
|----------|--------|
| `/api/admin/um/reports/users` | Active / inactive / suspended users |
| `/api/admin/um/reports/login-attempts` | Login success/fail by date range |
| `/api/admin/um/reports/role-assignments` | Role permissions across users |
| `/api/admin/um/reports/post-occupancy` | Sanctioned vs occupied (FR-UM-066) |
| `/api/admin/um/reports/role-module-map` | Role → module functions |
| `/api/admin/um/reports/contact-changes` | FR-UM-056 + FR-UM-065 + email changes |
| `/api/admin/um/reports/additional-charge` | FR-UM-053 audit |
| `/api/admin/um/reports/temporary-absence-charge` | FR-UM-079–084 |
| `/api/admin/um/reports/occupancy-refresh` | FR-UM-068 job runs |
| `/api/admin/um/reports/transfer-history` | FR-UM-057–061, FR-UM-067 |
| `/api/admin/um/reports/officer-service-history` | Per-officer occupancy timeline |

---

## 8. Database design — `db_um`

Physical PostgreSQL 15+ schema. Logical entity names from ERD v2.0 preserved; snake_case tables.

**Database:** `db_um` (single schema `um`).

### 8.1 Organisation

```sql
CREATE TABLE um.division_master (
  division_code   VARCHAR(32) PRIMARY KEY,
  division_name   VARCHAR(128) NOT NULL UNIQUE,
  display_order   INT NOT NULL,
  is_active       BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE um.office_type (
  office_type     VARCHAR(32) PRIMARY KEY,
  display_name    VARCHAR(128) NOT NULL
);

CREATE TABLE um.office_hierarchy (
  office_code         VARCHAR(32) PRIMARY KEY,
  office_name         VARCHAR(256) NOT NULL,
  office_type         VARCHAR(32) NOT NULL REFERENCES um.office_type(office_type),
  parent_office_code  VARCHAR(32) REFERENCES um.office_hierarchy(office_code),
  is_active           BOOLEAN NOT NULL DEFAULT TRUE
);
```

### 8.2 Establishment

```sql
CREATE TABLE um.posts_master (
  post_code       VARCHAR(32) PRIMARY KEY,
  post_name       VARCHAR(128) NOT NULL UNIQUE,
  division_code   VARCHAR(32) NOT NULL REFERENCES um.division_master(division_code),
  is_active       BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE um.officer_hierarchy_node (
  node_id           UUID PRIMARY KEY,
  post_code         VARCHAR(32) NOT NULL UNIQUE REFERENCES um.posts_master(post_code),
  parent_node_id    UUID REFERENCES um.officer_hierarchy_node(node_id),
  display_order     INT,
  is_active         BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE um.post_office_type_allowed (
  post_code     VARCHAR(32) REFERENCES um.posts_master(post_code),
  office_type   VARCHAR(32) REFERENCES um.office_type(office_type),
  PRIMARY KEY (post_code, office_type)
);

CREATE TABLE um.role_master (
  role_id         UUID PRIMARY KEY,
  role_name       VARCHAR(128) NOT NULL UNIQUE,
  role_category   VARCHAR(32) NOT NULL CHECK (role_category IN ('Citizen','DSR','Other Department')),
  division_code   VARCHAR(32) REFERENCES um.division_master(division_code),
  description     TEXT,
  is_active       BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE um.post_role_map (
  post_code   VARCHAR(32) REFERENCES um.posts_master(post_code),
  role_id     UUID REFERENCES um.role_master(role_id),
  PRIMARY KEY (post_code, role_id)
);

CREATE TABLE um.sanctioned_post (
  post_code             VARCHAR(32),
  office_code           VARCHAR(32),
  sanctioned_strength   INT NOT NULL CHECK (sanctioned_strength >= 0),
  occupied_count        INT NOT NULL DEFAULT 0 CHECK (occupied_count >= 0),
  PRIMARY KEY (post_code, office_code),
  FOREIGN KEY (post_code) REFERENCES um.posts_master(post_code),
  FOREIGN KEY (office_code) REFERENCES um.office_hierarchy(office_code),
  CHECK (occupied_count <= sanctioned_strength)
);
-- remaining_capacity = sanctioned_strength - occupied_count (computed or generated column)
```

### 8.3 Identity

```sql
CREATE TABLE um.user_master (
  user_id               UUID PRIMARY KEY,
  username              VARCHAR(64) NOT NULL UNIQUE,
  user_category         VARCHAR(32) NOT NULL CHECK (user_category IN ('Public (Citizen)','DSR Officer','Other Department')),
  first_name            VARCHAR(128) NOT NULL,
  middle_name           VARCHAR(128),
  last_name             VARCHAR(128) NOT NULL,
  email                 VARCHAR(256),
  mobile                VARCHAR(16) NOT NULL,
  parent_department     VARCHAR(256),
  designation           VARCHAR(256),
  account_end_date      DATE,
  status                VARCHAR(32) NOT NULL DEFAULT 'Active',
  lockout_until         TIMESTAMPTZ,
  reset_lockout_until   TIMESTAMPTZ,
  biometric_ref         VARCHAR(256),
  photo_ref             VARCHAR(512),
  id_proof_ref          VARCHAR(512),
  authorisation_letter_ref VARCHAR(512),
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE um.user_role (
  user_id   UUID REFERENCES um.user_master(user_id),
  role_id   UUID REFERENCES um.role_master(role_id),
  PRIMARY KEY (user_id, role_id)
);

CREATE TABLE um.security_question (
  question_id     UUID PRIMARY KEY,
  question_text   TEXT NOT NULL,
  is_active       BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE um.user_security_answer (
  user_id       UUID REFERENCES um.user_master(user_id),
  question_id   UUID REFERENCES um.security_question(question_id),
  answer_hash   VARCHAR(256) NOT NULL,
  PRIMARY KEY (user_id, question_id)
);

CREATE TABLE um.official_email_domain (
  domain      VARCHAR(128) PRIMARY KEY,
  is_active   BOOLEAN NOT NULL DEFAULT TRUE
);
```

### 8.4 Occupancy & transfer

```sql
CREATE TABLE um.post_occupancy (
  occupancy_id            UUID PRIMARY KEY,
  user_id                 UUID NOT NULL REFERENCES um.user_master(user_id),
  post_code               VARCHAR(32) NOT NULL,
  office_code             VARCHAR(32) NOT NULL,
  status                  VARCHAR(16) NOT NULL CHECK (status IN ('Active','Reserved','Ended')),
  joining_date            DATE NOT NULL,
  relieving_date          DATE,
  relieving_order_no        VARCHAR(64),
  relieving_document_ref    VARCHAR(512),
  transfer_order_no         VARCHAR(64),
  transfer_document_ref     VARCHAR(512),
  end_date                  DATE,
  deputation_reason         VARCHAR(64),
  reserved_flag             BOOLEAN NOT NULL DEFAULT FALSE,
  created_by                UUID,
  created_at                TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  FOREIGN KEY (post_code, office_code) REFERENCES um.sanctioned_post(post_code, office_code)
);

CREATE TABLE um.temporary_absence (
  absence_id        UUID PRIMARY KEY,
  occupancy_id      UUID NOT NULL REFERENCES um.post_occupancy(occupancy_id),
  absence_type      VARCHAR(32) NOT NULL,
  reason            TEXT NOT NULL,
  from_date         DATE NOT NULL,
  to_date           DATE NOT NULL,
  recorded_by       UUID NOT NULL,
  recorded_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE um.temporary_charge (
  charge_id             UUID PRIMARY KEY,
  covered_occupancy_id  UUID NOT NULL REFERENCES um.post_occupancy(occupancy_id),
  cover_user_id         UUID NOT NULL REFERENCES um.user_master(user_id),
  from_date             DATE NOT NULL,
  to_date               DATE,
  assigned_by           UUID NOT NULL,
  cleared_at            TIMESTAMPTZ,
  status                VARCHAR(16) NOT NULL DEFAULT 'Active'
);
```

### 8.5 RBAC

```sql
CREATE TABLE um.module_master (
  module_code   VARCHAR(32) PRIMARY KEY,
  module_name   VARCHAR(128) NOT NULL,
  is_active     BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE um.module_function (
  function_id     UUID PRIMARY KEY,
  module_code     VARCHAR(32) NOT NULL REFERENCES um.module_master(module_code),
  function_code   VARCHAR(32) NOT NULL,
  UNIQUE (module_code, function_code)
);

CREATE TABLE um.resource_master (
  resource_id     UUID PRIMARY KEY,
  function_id     UUID NOT NULL REFERENCES um.module_function(function_id),
  resource_type   VARCHAR(8) NOT NULL CHECK (resource_type IN ('API','URL')),
  http_method     VARCHAR(8),
  path_pattern    VARCHAR(512) NOT NULL,
  is_public       BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE um.role_module_function (
  role_id       UUID REFERENCES um.role_master(role_id),
  function_id   UUID REFERENCES um.module_function(function_id),
  PRIMARY KEY (role_id, function_id)
);
```

### 8.6 Runtime

```sql
CREATE TABLE um.user_session (
  session_id              UUID PRIMARY KEY,
  user_id                   UUID NOT NULL UNIQUE REFERENCES um.user_master(user_id), -- one active FR-UM-076
  assigned_occupancy_id     UUID REFERENCES um.post_occupancy(occupancy_id),
  temporary_charge_id       UUID REFERENCES um.temporary_charge(charge_id),
  add_charge_post_code      VARCHAR(32) REFERENCES um.posts_master(post_code),
  add_charge_office_code    VARCHAR(32) REFERENCES um.office_hierarchy(office_code),
  login_at                  TIMESTAMPTZ NOT NULL,
  last_activity_at          TIMESTAMPTZ NOT NULL,
  expires_at                TIMESTAMPTZ NOT NULL,
  ip_address                INET,
  user_agent                TEXT,
  is_active                 BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE um.otp_challenge (
  challenge_id    UUID PRIMARY KEY,
  user_id         UUID REFERENCES um.user_master(user_id),
  pending_token   VARCHAR(64),  -- pre-account registration FR-UM-063
  purpose         VARCHAR(32) NOT NULL,
  channel         VARCHAR(8) NOT NULL CHECK (channel IN ('SMS','EMAIL')),
  code_hash       VARCHAR(256) NOT NULL,
  expires_at      TIMESTAMPTZ NOT NULL,
  attempt_count   INT NOT NULL DEFAULT 0,
  resend_count    INT NOT NULL DEFAULT 0,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE um.audit_log (
  audit_id        UUID PRIMARY KEY,
  actor_id        UUID,
  actor_type      VARCHAR(32) NOT NULL,
  action          VARCHAR(64) NOT NULL,
  entity          VARCHAR(64) NOT NULL,
  entity_id       VARCHAR(64),
  before_json     JSONB,
  after_json      JSONB,
  reason          TEXT,
  artefact_id     VARCHAR(512),
  correlation_id  UUID,
  ip_address      INET,
  occurred_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- REVOKE UPDATE, DELETE ON um.audit_log FROM app_role;
```

### 8.7 Index strategy (selected)

| Table | Index | Purpose |
|-------|-------|---------|
| `user_master` | `username` UNIQUE | Login lookup |
| `user_master` | `(user_category, status)` | Admin search |
| `post_occupancy` | `(user_id, status)` | Login post list |
| `post_occupancy` | `(post_code, office_code, status)` | Occupied count job |
| `sanctioned_post` | `(office_code)` | Office reports |
| `resource_master` | `(path_pattern, http_method)` | Runtime enforcement |
| `audit_log` | `(occurred_at DESC)` | Reports |
| `otp_challenge` | `(user_id, purpose, created_at DESC)` | Rate limit |

### 8.8 Transactional invariants (enforce in application layer)

| Invariant | Rule | FR |
|-----------|------|-----|
| Capacity | `occupied_count < sanctioned_strength` before new Active/Reserved occupancy | FR-UM-066(a) |
| Unmapped post | Post must exist in `post_role_map` before sanction/assign | FR-UM-047 |
| Post–office type | `(post_code, office_type)` must exist in `post_office_type_allowed` | FR-UM-078 |
| Citizen roles | ≥ 1 Citizen role on registration | FR-UM-001 |
| OD roles | Exactly 1 Other Department role | FR-UM-029 |
| DSR roles | No `user_role` rows; roles via post | FR-UM-052 |
| Security answers | Exactly 5 per Citizen at registration | FR-UM-055 |

---

## 9. Background jobs

| Job | Schedule | Actions | FR |
|-----|----------|---------|-----|
| `OccupancyRefreshJob` | Daily **00:05 IST** | End occupancies past relieving/end date; activate Reserved where `joining_date = today`; recalc `occupied_count`; audit batch | FR-UM-058, FR-UM-061, FR-UM-068, FR-UM-084 |
| `OtherDepartmentExpiryJob` | Daily **00:10 IST** | Deactivate users where `account_end_date < today` | FR-UM-033 |
| `SessionSweepJob` | Every **5 min** | Expire idle (>15 min) and absolute (>8 h) sessions | FR-UM-074, FR-UM-075 |
| `TempAbsenceExpiryJob` | Daily **00:05 IST** | Clear expired temporary charges; lift login blocks | FR-UM-084 |

Job execution logged to `audit_log` with `actor_type = SYSTEM`.

---

## 10. Domain events

| Event | Payload (min) | Producers | Consumers |
|-------|---------------|-----------|-----------|
| `UserRegistered` | userId, category | identity | notify, audit, MIS |
| `UserAccountCreated` | userId, category, actorId | identity | notify (FR-UM-023), audit |
| `UserStatusChanged` | userId, from, to, reason | identity | notify, audit |
| `LoginSucceeded` | userId, sessionId, category | auth | audit, MIS |
| `LoginFailed` | username, reason | auth | audit, MIS |
| `OccupancyAssigned` | occupancyId, post, office | occupancy | audit |
| `TransferOutRecorded` | occupancyId, relievingDate | occupancy | audit, notify |
| `TransferInRecorded` | occupancyId, joiningDate, reserved | occupancy | audit |
| `OccupancyRefreshCompleted` | runId, changes[] | jobs | audit, MIS |
| `AdditionalChargeActivated` | sessionId, post, office | auth | audit |
| `AccessDenied` | userId, resource, path | rbac | audit |
| `RoleModuleFunctionChanged` | roleId | rbac | gateway cache invalidate |

Topic naming: `um.domain.{event}` or shared `platform.domain` with `type` header.

---

## 11. Integrations

| Integration | Direction | Adapter | SLA / notes |
|-------------|-----------|---------|-------------|
| SMS gateway | Outbound | `adapters/sms` | OTP ≤ **5 s** p95 (NFR-UM-02, FR-UM-010) |
| Email gateway | Outbound | `adapters/email` | Registration, reset PIN, notifications |
| Captcha | Inbound verify | `adapters/captcha` | Before OTP dispatch (FR-UM-011) |
| Biometric / UIDAI | Inbound | `adapters/biometric` | DSR + OD every login (FR-UM-006/007); store ref only |
| Object store | Outbound | `adapters/storage` | Photos, transfer orders, auth letters |
| notification-service | Outbound events | optional | Decouple SMS/email retries |
| API Gateway | Config push | resource cache | Public routes + JWT plugin |

---

## 12. Security controls

| Control | Implementation |
|---------|----------------|
| No passwords | FR-UM-009 — no credential table |
| OTP/PIN storage | Hash only in `otp_challenge.code_hash` |
| Security answers | bcrypt/argon2 hash; never display (FR-UM-055) |
| Login lockout | 5 fails → 15 min username lock (FR-UM-073) |
| Reset lockout | Separate 30 min lock for FR-UM-056 path |
| Session hijack | Bind session to Redis; rotate on privilege change |
| TLS | 1.3 to gateway |
| PII masking | Mobile masked in audit exports |
| Application Admin | Break-glass; not in role_master (FR-UM-051) |
| VAPT | NFR-UM-05 before go-live |
| Biometric | UIDAI-compliant transport/storage (NFR-UM-06) |

---

## 13. Non-functional requirements

| NFR | Target | LLD verification |
|-----|--------|------------------|
| NFR-UM-01 | Immutable audit with actor, IP, timestamp | `audit_log` append-only; no UPDATE/DELETE grants |
| NFR-UM-02 | OTP dispatch ≤ 5 s p95 | Async SMS adapter + timeout monitoring |
| NFR-UM-03 | Auth 99.5% business hours | HA Postgres + ≥2 UM pods + Redis sentinel |
| NFR-UM-04 | Scheduled jobs daily + session sweep | K8s CronJob / embedded scheduler with alerting |
| NFR-UM-05 | MeitY / CERT-In / STQC / GIGW | Security review checklist |
| NFR-UM-06 | Biometric per UIDAI | Adapter sign-off |
| FR-UM-069–072 | OTP policy | Enforced in `auth` package + Redis counters |
| FR-UM-074–076 | Session policy | `user_session` + Redis TTL |
| Audit retention | ≥ 7 years | Partition `audit_log` by month; archive policy |

---

## 14. Error codes (selected)

| errorCode | HTTP | When |
|-----------|------|------|
| `UM_CAPTCHA_INVALID` | 400 | Captcha failed |
| `UM_USERNAME_LOCKED` | 423 | FR-UM-073 lockout |
| `UM_OTP_EXPIRED` | 401 | FR-UM-069 |
| `UM_OTP_INVALID` | 401 | FR-UM-071 |
| `UM_BIOMETRIC_FAILED` | 401 | DSR/OD biometric |
| `UM_POST_CAPACITY_FULL` | 409 | FR-UM-066(a) |
| `UM_POST_UNMAPPED` | 409 | FR-UM-047 |
| `UM_POST_OFFICE_TYPE_INVALID` | 409 | FR-UM-078 |
| `UM_ABSENCE_LOGIN_BLOCKED` | 403 | FR-UM-080 |
| `UM_ACCESS_DENIED` | 403 | FR-UM-041 |
| `UM_SESSION_SUPERSEDED` | 401 | FR-UM-076 new login |
| `UM_SESSION_EXPIRED` | 401 | FR-UM-074/075 |

---

## 15. Test scenarios (UAT-aligned — BRD §9)

| ID | Scenario | Expected |
|----|----------|----------|
| T-UM-01 | Citizen registration dual OTP | Account only after both verify (FR-UM-063) |
| T-UM-02 | Citizen login OTP to mobile only | Never emailed (FR-UM-010) |
| T-UM-03 | DSR 2 occupancies | Post selection required (FR-UM-052) |
| T-UM-04 | Additional charge at SRO Yeshwanthapura | Only wholly unoccupied subordinates at same office (FR-UM-053) |
| T-UM-05 | Relieving date D | Active through 23:59 IST; job ends next day (FR-UM-058/068) |
| T-UM-06 | Reserved Transfer In | Counts occupied; login blocked until joining date (FR-UM-061/067) |
| T-UM-07 | OTP 5 min / 6 digit / 3 attempts | Policy enforced (FR-UM-069–071) |
| T-UM-08 | Second login | First session terminated (FR-UM-076) |
| T-UM-09 | Temp absence + temp charge | FR-UM-079–084 UAT scenario |
| T-UM-10 | Role–Module–Function complete | No role with zero unintended access |
| T-UM-11 | Lost-mobile reset | 3/5 questions + email PIN (FR-UM-056) |
| T-UM-12 | Runtime deny | Unmapped non-public API → 403 |

---

## 16. Implementation checklist

1. Flyway/Liquibase migrations for §8 schema + seed data (divisions, office types, posts, roles per BRD §6.5.3–6.5.4)
2. OpenAPI 3 specs: citizen/officer/admin BFF + `/internal/um/v1`
3. JWT issuing library (RS256 key rotation)
4. Shared `um-authz-middleware` for FR-UM-041 resource matching
5. SMS/email adapter contract tests (5 s SLA)
6. Biometric adapter mock for SIT
7. `OccupancyRefreshJob` integration tests with IST clock
8. Redis session store + pub/sub kick for FR-UM-076
9. Audit export API for 7-year retention
10. Gateway resource cache invalidation on RMF change

---

## Appendix A — ERD to physical table mapping

| ERD entity (v2.0) | Physical table |
|-------------------|----------------|
| DIVISION_MASTER | `um.division_master` |
| OFFICE_TYPE | `um.office_type` |
| OFFICE_HIERARCHY | `um.office_hierarchy` |
| POSTS_MASTER | `um.posts_master` |
| OFFICER_HIERARCHY_NODE | `um.officer_hierarchy_node` |
| POST_OFFICE_TYPE_ALLOWED | `um.post_office_type_allowed` |
| SANCTIONED_POST | `um.sanctioned_post` |
| ROLE_MASTER | `um.role_master` |
| POST_ROLE_MAP | `um.post_role_map` |
| USER_MASTER | `um.user_master` |
| USER_ROLE | `um.user_role` |
| SECURITY_QUESTION | `um.security_question` |
| USER_SECURITY_ANSWER | `um.user_security_answer` |
| OFFICIAL_EMAIL_DOMAIN | `um.official_email_domain` |
| POST_OCCUPANCY | `um.post_occupancy` |
| Temporary Absence / Charge | `um.temporary_absence`, `um.temporary_charge` |
| USER_SESSION | `um.user_session` |
| OTP_CHALLENGE | `um.otp_challenge` |
| MODULE_MASTER / MODULE_FUNCTION / RESOURCE_MASTER / ROLE_MODULE_FUNCTION | §8.5 |
| AUDIT_LOG | `um.audit_log` |
| APPLICATION_ADMIN | Not persisted — deployment config (FR-UM-051) |

## Appendix B — FR traceability (selected)

| FR | Primary component |
|----|-------------------|
| FR-UM-001–004, FR-UM-062–065 | `identity`, `auth` |
| FR-UM-005–012, FR-UM-069–076 | `auth` |
| FR-UM-052–054 | `auth` |
| FR-UM-016–018, FR-UM-028–035 | `identity`, `rbac` |
| FR-UM-036–042, FR-UM-050–051 | `rbac` |
| FR-UM-043–049, FR-UM-059, FR-UM-077–078 | `org`, `establishment` |
| FR-UM-024–027, FR-UM-047–048, FR-UM-066–068 | `establishment`, `jobs` |
| FR-UM-017, FR-UM-026, FR-UM-030, FR-UM-045, FR-UM-057–061, FR-UM-067 | `occupancy` |
| FR-UM-079–084 | `occupancy` |
| FR-UM-020–023, FR-UM-056, FR-UM-065 | `identity`, `auth`, `audit` |

---

*End of LLD User Management v1.0 — implement against BRD-K3-UM-001 v4.16 and ERD-K3-UM-001 v2.0.*
