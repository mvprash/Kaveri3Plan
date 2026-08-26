# Low-Level Design (LLD)

## Hindu Marriage — Online Channel

| Field | Value |
|--------|--------|
| **Document ID** | LLD-K3-MRG-HMA-ONLINE-001 |
| **Version** | 1.0 (Draft) |
| **Status** | Draft for Tech Lead / Architecture review |
| **Module** | Marriage Registration — Hindu Marriage Online |
| **Parent HLD** | `HLD/HLD_Marriage_Registration_v1.0` (HLD-K3-MRG-001) |
| **Source BRD** | `BRD_Marriage_v1.9.docx` (BRD-K3-MRG-HMA-001) |
| **Process definition** | `HMA_ONLINE_v1` |
| **Process diagram** | `Finalized BRD/Marriage/RFP/Process Diagrams/hindu marriage Online.png` |
| **Audience** | Tech Leads, Backend/Frontend engineers, QA, Integration |
| **Last updated** | 2026-08-27 |

---

## Document control

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 2026-08-27 | Architecture | Initial LLD for Hindu Marriage Online derived from HLD v1.0 + BRD v1.9 |

**Related documents**

| ID | Title |
|----|--------|
| BRD-K3-MRG-HMA-001 v1.9 | Business Requirements |
| HLD-K3-MRG-001 | Marriage Registration HLD |
| LLD-K3-MRG-HMA-ONLINE-001 | This document |

---

## 1. Scope

### 1.1 In scope

Low-level design for **Hindu Marriage Online** end-to-end:

- Needs-Based Wizard → `HMA_REG` + channel `ONLINE`
- Prerequisite + declaration, details capture with Bride e-KYC / Face Auth
- Office selection + summary, Form I & Form IA generation + eSign
- Single-stage SR verification, pay-after-approve, SR DSC, Form II-A download
- Notifications, audit, MIS projections for Online statuses

### 1.2 Out of scope (separate LLDs)

- Hindu Marriage Offline (appointment, DEO, Stage 2)
- Special Marriage Notice / Registration
- Platform Identity / Master-Data / Notification internals (contracts only)
- UI pixel layouts / Figma (BRD §10)

### 1.3 Services touched (Online)

| # | Service | Role in Online |
|---|---------|----------------|
| 1 | identity-access-service | AuthN/AuthZ |
| 2 | master-data-service | Offices, fees, reason codes |
| 3 | service-routing-service | Needs wizard → `HMA_REG` |
| 4 | application-intake-service | Application aggregate |
| 5 | workflow-orchestrator | `HMA_ONLINE_v1` state machine |
| 6 | document-form-service | Forms, uploads, signed PDFs |
| 7 | ekyc-adapter-service | Bride e-KYC / Face Auth |
| 8 | esign-adapter-service | Citizen eSign |
| 9 | verification-service | Single-stage SR decision |
| 10 | payment-fee-service | Post-approval fee |
| 11 | register-certificate-service | Serial + Form II-A |
| 12 | dsc-signing-adapter | SR DSC |
| 13 | notification-service | SMS/email |
| 14 | audit-compliance-service | Immutable audit |
| 15 | mis-reporting-service | Async projections |
| 16 | integration-gateway | Optional façade to PG/eSign/DSC/eKYC |

**Not used Online:** `deo-task-service`, `appointment-service`, `notice-publication-service`, `objection-service`.

---

## 2. Design conventions

| Convention | Rule |
|------------|------|
| IDs | UUID v4 for entities; human `applicationNumber` = `HMA-ON-{YYYY}-{seq}` |
| Time | Store UTC; display Asia/Kolkata |
| Locale | All citizen/officer messages EN + KN |
| Auth | Bearer JWT; claims: `sub`, `roles[]`, `officeId?`, `jurisdictionIds[]` |
| Idempotency | Header `Idempotency-Key` required on all POSTs that create side effects |
| Correlation | Header `X-Correlation-Id` propagated; written to audit |
| Errors | Problem+JSON (`type`, `title`, `status`, `detail`, `errorCode`, `traceId`) |
| Pagination | `page`, `size`, `sort` on list APIs |
| Soft delete | Forbidden for register/certificate/verification/audit |

---

## 3. Status model (`HMA_ONLINE_v1`)

### 3.1 Status enum

```text
DRAFT
CHANNEL_SELECTED
PREREQ_DECLARATION_COMPLETED
DETAILS_CAPTURED
OFFICE_SELECTED_SUMMARY_REVIEWED
FORM_I_IA_SUBMITTED
ESIGN_PENDING
PENDING_SR_VERIFICATION
REJECTED_DATA_CORRECTION
APPROVED_FOR_PAYMENT
PAYMENT_IN_PROGRESS          # technical (PG initiated / polling)
PAYMENT_COMPLETED
PENDING_SR_DIGITAL_SIGNATURE
REGISTERED
CERTIFICATE_ISSUED
CLOSED
```

> Offline-only statuses (appointment, DEO, Stage 2) are **invalid** for `channel=ONLINE` and must be rejected by workflow.

### 3.2 Transition table

| From | Event | Guard | To | Owner service |
|------|-------|-------|-----|---------------|
| — | `ApplicationCreated` | wizard=`HMA_REG` | DRAFT | routing + intake |
| DRAFT | `ChannelSelected(ONLINE)` | — | CHANNEL_SELECTED | intake |
| CHANNEL_SELECTED | `PrereqAccepted` | ack recorded | PREREQ_DECLARATION_COMPLETED | intake |
| PREREQ_DECLARATION_COMPLETED | `DetailsSaved` | validations + Bride eKYC OK | DETAILS_CAPTURED | intake + ekyc |
| DETAILS_CAPTURED | `OfficeSummaryConfirmed` | office in jurisdiction | OFFICE_SELECTED_SUMMARY_REVIEWED | intake + master |
| OFFICE_SELECTED_SUMMARY_REVIEWED | `FormsSubmitted` | Form I+IA artefacts exist | FORM_I_IA_SUBMITTED → ESIGN_PENDING | document + workflow |
| ESIGN_PENDING | `EsignCompleted` | all required signatories | PENDING_SR_VERIFICATION | esign + workflow |
| ESIGN_PENDING | `EsignFailed/Abandoned` | — | ESIGN_PENDING (retry) | esign |
| PENDING_SR_VERIFICATION | `SrApproved` | stage=`ONLINE` | APPROVED_FOR_PAYMENT | verification |
| PENDING_SR_VERIFICATION | `SrRejected` | reason + order | REJECTED_DATA_CORRECTION | verification |
| REJECTED_DATA_CORRECTION | `DetailsSaved` | citizen edit | DETAILS_CAPTURED | intake |
| APPROVED_FOR_PAYMENT | `PaymentInitiated` | prior approve | PAYMENT_IN_PROGRESS | payment |
| PAYMENT_IN_PROGRESS | `PaymentSucceeded` | reconciled | PAYMENT_COMPLETED | payment |
| PAYMENT_IN_PROGRESS | `PaymentFailed` | terminal fail | APPROVED_FOR_PAYMENT | payment |
| PAYMENT_COMPLETED | `ReadyForDsc` | auto | PENDING_SR_DIGITAL_SIGNATURE | workflow |
| PENDING_SR_DIGITAL_SIGNATURE | `DscCompleted` | DSC valid + pay OK | REGISTERED | dsc + register |
| REGISTERED | `CertificateReady` | Form II-A stored | CERTIFICATE_ISSUED | register |
| CERTIFICATE_ISSUED | `Close` | — | CLOSED | workflow |

Hard gates (must enforce in workflow):

- BR-HMA-010 / FR-HMA-022 — no payment before SR approve  
- BR-HMA-011 / FR-HMA-057 — no SR queue before eSign complete  
- FR-HMA-058 — Bride e-KYC success before office/summary  
- FR-HMA-024 / FR-HMA-078–080 — no certificate without pay reconcile + DSC  

---

## 4. Component / package design

### 4.1 Citizen BFF (`citizen-bff-mrg`)

| Package | Responsibility |
|---------|----------------|
| `wizard` | Proxy to routing; cache path result in session |
| `application` | Compose intake + document + workflow reads |
| `ekyc` | Start/poll eKYC; map fallback UX |
| `esign` | Start/callback eSign |
| `payment` | Initiate/status; enforce UI lock while polling |
| `tracker` | Read-model of status + next actions |
| `certificate` | Download URL / stream |

### 4.2 Officer BFF (`officer-bff-mrg`)

| Package | Responsibility |
|---------|----------------|
| `queue` | Filter `servicePath=HMA_REG`, `channel=ONLINE`, `stage=ONLINE` |
| `verification` | Approve/reject + refusal PDF trigger |
| `dsc` | DSC session + completion |
| `applicationView` | Aggregate intake + docs + pay status |

### 4.3 Domain service internal layers (each)

```text
api (REST controllers)
  → application (use-cases / command handlers)
    → domain (entities, invariants)
    → ports (repositories, clients)
      → adapters (JPA/SQL, Kafka, HTTP partners)
```

---

## 5. End-to-end sequence (happy path)

```text
Citizen                Citizen-BFF         Routing   Intake    Workflow   eKYC     Document   eSign    Verify   Payment   DSC    Register   Notify   Audit
  |                         |                 |         |          |         |         |         |        |         |       |        |         |        |
  |-- login --------------->| identity ...                                                                                                      |        |
  |-- wizard resolve ------>|---------------->|-------->|--------->|                                                                                     |
  |                         |                 | write  | create   | start                                                                                 |
  |                         |                 | db_mrg_ | db_mrg_  | db_mrg_                                                                               |
  |                         |                 | routing | intake   | workflow                                                                              |
  |-- channel ONLINE ------>|-------------------------->|--------->|                                                                                     |
  |-- prereq ack ---------->|-------------------------->|--------->|------------------------------------------------------------------------------------>|
  |-- save details -------->|-------------------------->|          |         |                                                                           |
  |-- start ekyc Bride ---->|-------------------------------------->|-------->|                                                                          |
  |                         |                                   |  |         | Aadhaar                                                                   |
  |-- confirm office ------->|-------------------------->|--------->|         |                                                                           |
  |-- submit Form I/IA ----->|-------------------------------------->|-------->|---------->|                                                              |
  |                         |                                   |  |         | generate |                                                                |
  |-- esign start ---------->|------------------------------------------------------->|-------->|                                                        |
  |                         |                                                   |  | store  | provider                                                   |
  |                         |                                                   |  | signed |                                                            |
  |                         |                                                   |  ESIGN→PENDING_SR                                                      |
  |                         |                                                   |  |        |         notify SR ---------------------------------------->|
  | SR open queue ---------->| officer-bff ---------------------------------------------->|-------->|                                                    |
  | SR approve ------------->|---------------------------------------------------------->|--------->|-------->|                                          |
  |                         |                                                   |  APPROVED_FOR_PAYMENT                                                   |
  |-- pay initiate --------->|---------------------------------------------------------------------->|-------->|                                         |
  |                         |                                                                            | PG  |                                         |
  |                         |                                                                            | poll|                                         |
  |                         |                                                   |  PAYMENT_COMPLETED                                                     |
  |                         |                                                   |  → PENDING_DSC                                                         |
  | SR DSC ----------------->|------------------------------------------------------------------------------>|-------->|-------->|                       |
  |                         |                                                                                      | allocate|                         |
  |                         |                                                                                      | II-A    |                         |
  |                         |                                                   |  CERTIFICATE_ISSUED -------------------------------------------------->|
  |-- download cert -------->|--------------------------------------------------------------------------------------------->|                            |
```

### 5.1 Reject path (Online)

```text
PENDING_SR_VERIFICATION --SrRejected--> REJECTED_DATA_CORRECTION
  → verification writes decision + refusal PDF (document-form)
  → notify citizen
  → unlock editable sections on intake
  → citizen DetailsSaved → DETAILS_CAPTURED → (re-office/summary if needed) → re-submit → eSign → SR again
```

Payment is **not** rolled back because it has not occurred yet.

---

## 6. API design

Base paths:

- Citizen BFF: `/api/citizen/mrg/hma/online`
- Officer BFF: `/api/officer/mrg/hma/online`
- Internal service APIs: `/internal/{service}/v1/...` (mTLS)

### 6.1 Wizard & application bootstrap

#### POST `/api/citizen/mrg/wizard/resolve`

**Request**

```json
{
  "marriageStatus": "ALREADY_SOLEMNIZED",
  "customaryForm": "HINDU",
  "answers": { "religion": "HINDU", "solemnized": true }
}
```

**Response**

```json
{
  "servicePath": "HMA_REG",
  "routingDecisionId": "uuid",
  "allowedChannels": ["ONLINE", "OFFLINE"]
}
```

#### POST `/api/citizen/mrg/hma/online/applications`

Headers: `Idempotency-Key`

**Response** `201`

```json
{
  "applicationId": "uuid",
  "applicationNumber": "HMA-ON-2026-000123",
  "status": "DRAFT",
  "servicePath": "HMA_REG",
  "channel": null
}
```

#### POST `/applications/{id}/channel`

```json
{ "channel": "ONLINE" }
```

→ status `CHANNEL_SELECTED`

#### POST `/applications/{id}/prerequisite`

```json
{
  "acknowledged": true,
  "declarationsAccepted": ["SEC8_VALID", "SEC5_CONDITIONS", "PARTICULARS_TRUE"],
  "locale": "EN"
}
```

→ status `PREREQ_DECLARATION_COMPLETED`; audit required (FR-HMA-046)

### 6.2 Details & e-KYC

#### PUT `/applications/{id}/details`

```json
{
  "marriage": {
    "marriageDate": "2025-12-01",
    "place": { "addressLine": "...", "districtCode": "BNG", "stateCode": "KA" },
    "ceremonyDescription": "..."
  },
  "bridegroom": { "...": "Form I fields" },
  "bride": { "...": "Form I fields", "ekycSessionId": "uuid" },
  "witnesses": [ { "...": "w1" }, { "...": "w2" }, { "...": "w3" } ],
  "jurisdictionBasis": "PLACE_OF_MARRIAGE"
}
```

**Validations (server):**

| Rule | ErrorCode |
|------|-----------|
| marriageDate ≤ today | `HMA_DATE_FUTURE` |
| groom age ≥ 21, bride ≥ 18 at marriage | `HMA_AGE_MIN` |
| exactly 3 witnesses | `HMA_WITNESS_COUNT` |
| Bride eKYC success for Online | `HMA_EKYC_REQUIRED` |
| marital status present | `HMA_MARITAL_STATUS` |

#### POST `/applications/{id}/ekyc/bride/start`

→ `ekyc-adapter`; returns `{ "ekycSessionId", "redirectUrl" }`

#### GET `/applications/{id}/ekyc/bride/{sessionId}`

Statuses: `IN_PROGRESS` | `SUCCESS` | `FAILED` | `FALLBACK_MANUAL`

On `FAILED`: block progress with bilingual message; optional manual+docs only if PO enables RS-MRG-002 fallback for HMA Online (default = hard stop per FR-HMA-058).

### 6.3 Office, forms, eSign

#### PUT `/applications/{id}/office`

```json
{ "officeId": "uuid", "summaryConfirmed": true }
```

→ `OFFICE_SELECTED_SUMMARY_REVIEWED`

#### POST `/applications/{id}/documents/joint-photo` (multipart)

#### POST `/applications/{id}/documents/proofs` (multipart checklist)

#### POST `/applications/{id}/forms/submit`

Generates Form I + Form IA for selected office; stores artefacts; → `ESIGN_PENDING`

#### POST `/applications/{id}/esign/start`

```json
{ "artefactTypes": ["FORM_I", "FORM_IA"] }
```

#### POST `/applications/{id}/esign/callback` *(provider → integration-gateway → esign)*

On all required signatures complete → `PENDING_SR_VERIFICATION`

### 6.4 Payment

#### POST `/applications/{id}/payments/initiate`

Allowed only if status=`APPROVED_FOR_PAYMENT`

```json
{ "purpose": "HMA_REG" }
```

Response:

```json
{
  "paymentId": "uuid",
  "amount": 0,
  "currency": "INR",
  "redirectUrl": "...",
  "status": "INITIATED"
}
```

→ status `PAYMENT_IN_PROGRESS`; **UI pay button locked** (NFR-MRG-PAY-001 / FB-MRG-001)

#### GET `/applications/{id}/payments/current`

Returns terminal or polling status. Backend poller queries Treasury until Success/Failed.

### 6.5 Officer APIs

#### GET `/api/officer/mrg/hma/online/queues`

Query: `officeId` (from token), `status=PENDING_SR_VERIFICATION|PENDING_SR_DIGITAL_SIGNATURE`

#### POST `/applications/{id}/verifications`

```json
{
  "stage": "ONLINE",
  "decision": "APPROVE",
  "reasonCode": null,
  "reasonText": null
}
```

or `REJECT` with mandatory reason → generates refusal order PDF + notify.

#### POST `/applications/{id}/dsc/sign`

Guard: status=`PENDING_SR_DIGITAL_SIGNATURE`; DSC not expired (FR-HMA-079)

On success → register allocates serial → Form II-A → `CERTIFICATE_ISSUED`

#### GET `/applications/{id}/certificate`

Citizen/officer download; Online delivery mode=`PORTAL`

---

## 7. Database design (Online-relevant)

### 7.1 `db_mrg_routing`

```sql
routing_decision (
  id UUID PK,
  citizen_id UUID NOT NULL,
  answers_json JSONB NOT NULL,
  service_path VARCHAR(32) NOT NULL,  -- HMA_REG
  created_at TIMESTAMPTZ NOT NULL
)
```

### 7.2 `db_mrg_intake`

```sql
application (
  id UUID PK,
  application_number VARCHAR(32) UNIQUE NOT NULL,
  citizen_id UUID NOT NULL,
  routing_decision_id UUID,
  service_path VARCHAR(32) NOT NULL,   -- HMA_REG
  channel VARCHAR(16),                 -- ONLINE
  status VARCHAR(64) NOT NULL,         -- denormalized cache of workflow
  office_id UUID,
  jurisdiction_basis VARCHAR(32),
  prereq_ack_at TIMESTAMPTZ,
  version INT NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
)

marriage_event (
  application_id UUID PK REFERENCES application(id),
  marriage_date DATE NOT NULL,
  place_json JSONB NOT NULL,
  ceremony_description TEXT
)

party (
  id UUID PK,
  application_id UUID NOT NULL REFERENCES application(id),
  role VARCHAR(16) NOT NULL,           -- BRIDE | BRIDEGROOM
  salutation VARCHAR(16),
  full_name VARCHAR(200) NOT NULL,
  father_name VARCHAR(200),
  mother_name VARCHAR(200),
  dob DATE,
  age_at_marriage INT,
  current_address JSONB,
  permanent_address JSONB,
  marital_status VARCHAR(32),
  mobile VARCHAR(15),
  email VARCHAR(200),
  ekyc_session_id UUID,
  ekyc_status VARCHAR(32)
)

witness (
  id UUID PK,
  application_id UUID NOT NULL,
  seq SMALLINT NOT NULL CHECK (seq BETWEEN 1 AND 3),
  full_name VARCHAR(200) NOT NULL,
  relation VARCHAR(100),
  age INT,
  current_address JSONB,
  permanent_address JSONB,
  mobile VARCHAR(15),
  UNIQUE(application_id, seq)
)

UNIQUE: exactly 3 witnesses enforced in application service before DETAILS_CAPTURED
```

### 7.3 `db_mrg_workflow`

```sql
process_instance (
  id UUID PK,
  application_id UUID UNIQUE NOT NULL,
  definition_key VARCHAR(64) NOT NULL, -- HMA_ONLINE_v1
  status VARCHAR(64) NOT NULL,
  started_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ
)

process_transition (
  id UUID PK,
  instance_id UUID NOT NULL,
  from_status VARCHAR(64),
  to_status VARCHAR(64) NOT NULL,
  event VARCHAR(64) NOT NULL,
  actor_id UUID,
  correlation_id VARCHAR(64),
  created_at TIMESTAMPTZ NOT NULL
)
```

Redis keys: `lock:app:{applicationId}`, `paylock:{paymentId}`

### 7.4 `db_mrg_document` + object store

```sql
document_asset (
  id UUID PK,
  application_id UUID NOT NULL,
  doc_type VARCHAR(32) NOT NULL,  -- JOINT_PHOTO, AGE_PROOF, FORM_I, FORM_IA, FORM_II_A, REFUSAL_ORDER, ESIGN_META
  version INT NOT NULL,
  storage_uri TEXT NOT NULL,
  checksum VARCHAR(128) NOT NULL,
  mime_type VARCHAR(64),
  uploaded_by UUID,
  uploaded_by_role VARCHAR(16),
  immutable BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL
)
```

Object key pattern: `mrg/hma/{applicationId}/{docType}/v{version}/{uuid}`

Reject password-protected PDF / bad MIME before persist (FB-MRG-003).

### 7.5 `db_mrg_verification`

```sql
verification_decision (
  id UUID PK,
  application_id UUID NOT NULL,
  stage VARCHAR(16) NOT NULL,      -- ONLINE
  decision VARCHAR(16) NOT NULL,   -- APPROVE | REJECT
  reason_code VARCHAR(32),
  reason_text TEXT,
  actor_id UUID NOT NULL,
  refusal_document_id UUID,
  created_at TIMESTAMPTZ NOT NULL
)
-- append-only; no UPDATE/DELETE
```

### 7.6 `db_mrg_payment`

```sql
payment_intent (
  id UUID PK,
  application_id UUID NOT NULL,
  purpose VARCHAR(16) NOT NULL,    -- HMA_REG
  amount NUMERIC(12,2) NOT NULL,
  status VARCHAR(32) NOT NULL,     -- INITIATED|PENDING|POLLING|SUCCESS|FAILED
  pg_ref VARCHAR(64),
  receipt_no VARCHAR(64),
  idempotency_key VARCHAR(64) UNIQUE NOT NULL,
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ
)
```

Only one non-terminal intent per application at a time.

### 7.7 `db_mrg_register`

```sql
office_register_cursor (
  office_id UUID PK,
  volume_no INT NOT NULL,
  page_no INT NOT NULL,
  serial_no INT NOT NULL
)

register_entry (
  id UUID PK,
  application_id UUID UNIQUE NOT NULL,
  office_id UUID NOT NULL,
  serial_no INT NOT NULL,
  page_no INT NOT NULL,
  volume_no INT NOT NULL,
  registered_at TIMESTAMPTZ NOT NULL,
  dsc_document_id UUID NOT NULL
)

certificate (
  id UUID PK,
  application_id UUID UNIQUE NOT NULL,
  form_type VARCHAR(16) NOT NULL,  -- II_A
  document_id UUID NOT NULL,
  integrity_token VARCHAR(128) NOT NULL,
  delivery_mode VARCHAR(16) NOT NULL, -- PORTAL
  issued_at TIMESTAMPTZ NOT NULL
)
```

Serial allocation: `SELECT ... FOR UPDATE` on `office_register_cursor` inside transaction + outbox event `CertificateIssued`.

---

## 8. Domain events (Online)

| Event | Payload (min) | Producers | Consumers |
|-------|---------------|-----------|-----------|
| `ServicePathResolved` | routingId, path | routing | intake, workflow, audit, MIS |
| `ChannelSelected` | appId, ONLINE | intake | workflow, audit, MIS |
| `PrereqAcknowledged` | appId, at | intake | audit |
| `BrideEkycCompleted` | appId, sessionId | ekyc | intake, audit |
| `FormsSubmitted` | appId, formIId, formIAId | document | workflow |
| `EsignCompleted` | appId, artefactIds[] | esign | workflow, document, notify, audit |
| `VerificationDecisionRecorded` | appId, decision, stage | verification | workflow, notify, audit, MIS |
| `PaymentSucceeded` | appId, paymentId, receipt | payment | workflow, notify, audit, MIS |
| `PaymentFailed` | appId, paymentId | payment | workflow, notify, audit |
| `DscCompleted` | appId, dscDocId | dsc | register, workflow |
| `CertificateIssued` | appId, certId | register | notify, MIS, DigiLocker(optional), audit |
| `ApplicationStatusChanged` | appId, from, to, event | workflow | intake cache, tracker, audit, MIS |

Kafka topic naming (suggested): `mrg.hma.online.{event}` or shared `mrg.domain` with `type` header.

---

## 9. Error handling & fallbacks

| Scenario | Behaviour | Codes |
|----------|-----------|-------|
| eSign fail / abandon | Stay `ESIGN_PENDING`; retry signing only (FB-MRG-002) | `ESIGN_RETRYABLE` |
| PG timeout | Poll PG; keep `PAYMENT_IN_PROGRESS`; lock UI (FB-MRG-001) | `PAY_POLLING` |
| PG terminal fail | Back to `APPROVED_FOR_PAYMENT`; allow new intent | `PAY_FAILED` |
| DSC expired | Block issue; message to SR (FR-HMA-079) | `DSC_EXPIRED` |
| eKYC fail | Block Online progress (FR-HMA-058) unless fallback enabled | `EKYC_FAILED` |
| Bad upload | Reject before persist; bilingual message (FB-MRG-003) | `DOC_INVALID` |
| Notify gateway down | Queue locally; do **not** block cert/status (FB-MRG-004) | `NOTIFY_QUEUED` |
| Illegal transition | HTTP 409 | `WF_ILLEGAL_TRANSITION` |

---

## 10. Security controls (Online)

| Control | Implementation |
|---------|----------------|
| Citizen can only access own applications | `citizen_id = token.sub` |
| SR queue scoped to office | `office_id ∈ token.jurisdictionIds` |
| DEO role | No Online queue actions (deny) |
| PII in logs | Mask Aadhaar / ekyc refs (NFR-MRG-PRIV-001) |
| TLS | 1.3 end-to-end to gateway |
| eSign/DSC artefacts | `immutable=true`; no overwrite |
| VAPT | Covered by module NFR-MRG-VAPT-* |

---

## 11. Non-functional checks (Online slice)

| NFR | LLD verification |
|-----|------------------|
| UI ≤ 2s p95 | BFF aggregates; masters cached |
| External API ≤ 5s | eSign/PG/eKYC timeouts + async poll |
| 5k citizen concurrency | Stateless pods; DB pool sizing on intake/payment |
| 3× surge | HPA on citizen-bff, intake, payment, document |
| No double debit | Idempotency key + pay UI lock + single non-terminal intent |

---

## 12. Test scenarios (must pass before Online UAT exit)

| ID | Scenario | Expected |
|----|----------|----------|
| T-ON-01 | Wizard solemnized+Hindu → HMA Online | `servicePath=HMA_REG` |
| T-ON-02 | Channel before prereq | status order enforced |
| T-ON-03 | Future marriage date | blocked |
| T-ON-04 | Bride eKYC missing | cannot confirm office |
| T-ON-05 | Submit without eSign | not in SR queue |
| T-ON-06 | eSign abandon + retry | no data re-entry |
| T-ON-07 | SR reject | back to details; reason visible; refusal PDF |
| T-ON-08 | Pay before approve | HTTP 409 |
| T-ON-09 | PG timeout | poll; no second debit |
| T-ON-10 | DSC success | serial allocated once; II-A downloadable |
| T-ON-11 | DSC expired | no certificate |
| T-ON-12 | Notify down at issue | certificate still issued; notify queued |
| T-ON-13 | Audit | every status change + verify + pay + DSC present |

---

## 13. Implementation checklist (engineering)

1. Flyway/Liquibase scripts for schemas in §7  
2. OpenAPI 3 specs for Citizen BFF + Officer BFF + internal services  
3. Workflow definition `HMA_ONLINE_v1` (Camunda/Temporal/FSM) matching §3.2  
4. Form I / IA / II-A template pack EN+KN with Legal sign-off  
5. Contract tests for eSign, PG poll, eKYC, DSC adapters  
6. Outbox publisher for domain events  
7. Tracker read-model projector  
8. Load test profile for Online path only  

---

## Appendix A — Online status cheat-sheet (citizen next action)

| Status | Citizen next action |
|--------|---------------------|
| DRAFT | Select channel |
| CHANNEL_SELECTED | Accept prerequisite |
| PREREQ_DECLARATION_COMPLETED | Enter details + Bride eKYC |
| DETAILS_CAPTURED | Select office + confirm summary |
| OFFICE_SELECTED_SUMMARY_REVIEWED | Submit Form I & IA |
| ESIGN_PENDING | Complete eSign |
| PENDING_SR_VERIFICATION | Wait / track |
| REJECTED_DATA_CORRECTION | Correct details |
| APPROVED_FOR_PAYMENT | Pay fee |
| PAYMENT_IN_PROGRESS | Wait (button locked) |
| PAYMENT_COMPLETED / PENDING_SR_DIGITAL_SIGNATURE | Wait for SR DSC |
| CERTIFICATE_ISSUED | Download Form II-A |
| CLOSED | Done |

## Appendix B — Traceability (Online FR → components)

| FR | Primary components |
|----|-------------------|
| FR-HMA-001–014 | routing, intake, ekyc |
| FR-HMA-015–019, 083–087 | document-form, esign |
| FR-HMA-046–058, 086–087 | intake, ekyc, esign, workflow |
| FR-HMA-020–025 | payment-fee, workflow |
| FR-HMA-026–030, 070, 073, 075–076 | verification, document, notify |
| FR-HMA-078–082 | dsc, register-certificate |
| FB-MRG-001–004 | payment, esign, document, notification |

---

*End of LLD Hindu Marriage Online v1.0 — implement against HLD-K3-MRG-001 and BRD v1.9.*
