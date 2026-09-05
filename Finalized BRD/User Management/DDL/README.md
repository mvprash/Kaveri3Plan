# User Management — PostgreSQL DDL

Companion physical scripts for **ERD-K3-UM-001 v2.2** / BRD **User Management v4.18**.

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
| 05 | `05_tables_identity.sql` | User master, roles, security Q&A, email domains |
| 06 | `06_tables_occupancy.sql` | Occupancy, temporary absence, temporary charge |
| 07 | `07_tables_rbac.sql` | Modules, functions, resources, role–function map |
| 08 | `08_tables_runtime.sql` | Session, OTP, audit |
| 09 | `09_views.sql` | Reporting / runtime views (17 views — full Section 8 coverage) |
| 10 | `10_functions_triggers.sql` | Occupancy refresh helpers, occupied_count sync |
| 11 | `11_grants.sql` | Placeholder grants |
| 12 | `12_seed_masters.sql` | Admin-maintained reference data — exact BRD seed rows (divisions, posts, office hierarchy, hierarchy nodes, post–role map, post–office-type-allowed, sanctioned posts examples, Role/Module/Function/Resource masters, Role–Module–Function examples, security questions) |
| 13 | `13_sample_transactional_data.sql` | **Illustrative demo data only** — a handful of users/occupancies/absence/charge/session/OTP/audit rows built from the BRD's own worked examples (SRO Yeshwanthapura / Jayanagar, DRO Bengaluru handover, US-TA-01/02). Comment out the `\i` line in `00_install_all.sql` before deploying to production. |

## What changed in v2.2 (this pass)

- `officer_hierarchy_node`: added `division_code`, `effective_from`, `effective_to` — attributes listed in BRD Section 6.5.7 but missing from v2.1.
- `sanctioned_post`: added persisted `remaining_capacity` and `is_wholly_unoccupied` generated columns (FR-UM-068(3) says the job must "persist" these, not only `occupied_count`); `remaining_capacity` floors at 0 during an FR-UM-067 handover transient over-count, matching `v_sanctioned_post_capacity`.
- `user_master.last_name`: made nullable — single-name citizens are common; only `first_name` is mandatory.
- `module_master`: added `description`. `module_function`: added `function_name` (short verb, e.g. `VIEW`) distinct from the globally-unique `function_code`. `resource_master`: added `resource_code` (Section 6.5.6 attribute list) and relaxed `function_id` to nullable with a check requiring it unless `is_public`.
- `09_views.sql`: added 8 views closing every remaining Section 8 (Reporting Requirements) bullet — user status, login audit, effective roles, contact-change/recovery, additional-charge, occupancy-refresh, transfer history, officer posting history.
- Added `12_seed_masters.sql` and `13_sample_transactional_data.sql`.
- Full install verified end-to-end against PostgreSQL 16 (`psql -v ON_ERROR_STOP=1 -f 00_install_all.sql`) with zero errors.

## Notes

- Logical entity names map 1:1 to physical tables (snake_case).
- Timestamps use `timestamptz`; business dates are `date` interpreted in **Asia/Kolkata (IST)**.
- No password column exists (FR-UM-009).
- Application Admin is not a `role_master` row, and not a `user_master` row either (FR-UM-051) — audit rows it performs use `actor_type = 'APPLICATION_ADMIN'` with `actor_id NULL`.
- Run against PostgreSQL 14+ (uses `GENERATED … AS IDENTITY`, `GENERATED ALWAYS AS ( ) STORED`, partial unique indexes).

```bash
psql -v ON_ERROR_STOP=1 -f 00_install_all.sql
```
