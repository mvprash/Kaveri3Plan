# User Management — PostgreSQL DDL

Companion physical scripts for **ERD-K3-UM-001 v2.3** / BRD **User Management v1.0** (`BRD_User_Management_v1.0.pdf`, 11 September 2026 — the finalized print of the v4.23 requirements).

## Schema

All objects are created in schema **`um`**.

## Install order

| # | Script | Purpose |
|---|--------|---------|
| 00 | `00_install_all.sql` | `\i` runner (psql) |
| 01 | `01_schema.sql` | Schema + extensions |
| 02 | `02_types.sql` | Enumerated types |
| 03 | `03_tables_organisation.sql` | Division, office type, office hierarchy |
| 04 | `04_tables_establishment.sql` | Posts, hierarchy nodes, sanctioned posts, mappings |
| 05 | `05_tables_identity.sql` | User master, roles, Aadhaar e-KYC, email domains |
| 06 | `06_tables_occupancy.sql` | Occupancy, temporary absence, temporary charge |
| 07 | `07_tables_rbac.sql` | Modules, functions, resources, role–function map |
| 08 | `08_tables_runtime.sql` | Session, OTP, audit |
| 09 | `09_views.sql` | Reporting / runtime views (Section 6 coverage) |
| 10 | `10_functions_triggers.sql` | Occupancy refresh helpers, occupied_count sync |
| 11 | `11_grants.sql` | Placeholder grants |
| 12 | `12_seed_masters.sql` | Admin-maintained reference data — exact BRD seed rows (divisions, posts, office hierarchy, hierarchy nodes, post–role map, post–office-type-allowed, sanctioned posts examples, Role/Module/Function/Resource masters, Role–Module–Function examples) |
| 13 | `13_sample_transactional_data.sql` | **Illustrative demo data only** — a handful of users/occupancies/absence/charge/session/OTP/e-KYC/audit rows built from the BRD's own worked examples (SRO Yeshwanthapura / Jayanagar, DRO Bengaluru handover, US-TA-01/02). Comment out the `\i` line in `00_install_all.sql` before deploying to production. |

## What changed in v2.3 (this pass — BRD v1.0 / 11-Sep-2026)

Aligned the physical model to the finalized BRD (security questions retired, Aadhaar e-KYC, immediate Transfer In, tightened session policy):

- **Dropped** `security_question` and `user_security_answer` — FR-UM-055 retired; Citizen identity proofing is Aadhaar e-KYC (FR-UM-085, FR-UM-056).
- **Added** `ekyc_challenge` (opaque UIDAI transaction ref only — never Aadhaar number / VID) and `user_master.ekyc_verified_at`.
- **User Master:** DSR Officers do not capture official email (FR-UM-002, FR-UM-064); Other Department username is `<DepartmentCode>-<EmployeeID|KGID>`; `kgid` / `employee_id` / `department_code` columns; biometrics DSR-only (FR-UM-006 / FR-UM-007).
- **Occupancy:** removed `joining_date`, `reserved_flag`, `RESERVED` status, and deputation `end_date` (FR-UM-061, FR-UM-067, FR-UM-030 retired). Transfer In is `ACTIVE` immediately when capacity is available (FR-UM-060). Added enumerated `relieving_reason` (FR-UM-087).
- **Sanctioned post:** `occupied_count <= sanctioned_strength` (no +1 handover over-count); occupied count is ACTIVE rows only.
- **Session / OTP comments:** idle **10 minutes**, absolute **4 hours**, OTP resend cooldown **60 seconds** (FR-UM-072, FR-UM-074, FR-UM-075). DSR login is face/biometric — no login OTP.
- Occupancy refresh job no longer activates reserved Transfer In.
- Reporting views retargeted to **Section 6**; contact-change report includes e-KYC and DSR self-service mobile (FR-UM-086). Added `v_officer_hierarchy_tree` for derived hierarchy Level (Section 4.5.7).

## Notes

- Logical entity names map 1:1 to physical tables (snake_case).
- Timestamps use `timestamptz`; business dates are `date` interpreted in **Asia/Kolkata (IST)**.
- No password column exists (FR-UM-009).
- Application Admin is not a `role_master` row, and not a `user_master` row either (FR-UM-051) — audit rows it performs use `actor_type = 'APPLICATION_ADMIN'` with `actor_id NULL`.
- Run against PostgreSQL 14+ (uses `GENERATED … AS IDENTITY`, `GENERATED ALWAYS AS ( ) STORED`, partial unique indexes).

```bash
psql -v ON_ERROR_STOP=1 -f 00_install_all.sql
```
