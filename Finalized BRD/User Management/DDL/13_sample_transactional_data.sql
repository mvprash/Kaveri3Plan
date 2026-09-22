-- =============================================================================
-- 13 · Illustrative SAMPLE / DEMO data — NOT for production
-- Companion to ERD-K3-UM-001 v2.3 / BRD_User_Management_v1.0 (11-Sep-2026)
-- Purpose: exercise the schema end-to-end and back the ERD "Sample Records"
-- sections with data traceable to the BRD's own worked examples. Safe to run
-- once against a fresh/dev database only — re-running will duplicate rows
-- (no ON CONFLICT — these are not natural-keyed reference rows).
-- =============================================================================

SET search_path TO um, public;

-- =====================================================================
-- USER_MASTER — one Citizen (e-KYC verified), DSR Officers (no email),
-- one Other Department user (DeptCode-EmpID username).
-- =====================================================================
INSERT INTO um.user_master
  (username, user_category, first_name, last_name, email, mobile,
   kgid, employee_id, department_code, parent_department, designation,
   status, ekyc_verified_at, created_at)
VALUES
  ('ravi.citizen1', 'CITIZEN', 'Ravi', 'Kumar', 'ravi.kumar@example.com', '9900011111',
   NULL, NULL, NULL, NULL, NULL,
   'ACTIVE', now() - interval '90 days', now() - interval '90 days'),
  ('KGID10234501', 'DSR_OFFICER', 'Anitha', 'Rao', NULL, '9900022222',
   'KGID10234501', NULL, NULL, NULL, NULL,
   'ACTIVE', NULL, now() - interval '400 days'),
  ('KGID10234599', 'DSR_OFFICER', 'Suresh', 'Patil', NULL, '9900033333',
   'KGID10234599', NULL, NULL, NULL, NULL,
   'ACTIVE', NULL, now() - interval '600 days'),
  ('KGID10234610', 'DSR_OFFICER', 'Manjunath', NULL, NULL, '9900044444',
   'KGID10234610', NULL, NULL, NULL, NULL,
   'ACTIVE', NULL, now() - interval '30 days'),
  ('KGID10234650', 'DSR_OFFICER', 'Kavya', 'Iyer', NULL, '9900066666',
   'KGID10234650', NULL, NULL, NULL, NULL,
   'ACTIVE', NULL, now() - interval '500 days'),
  ('REV-20111001', 'OTHER_DEPARTMENT', 'Deepa', 'Shetty', 'deepa.shetty@revenue.karnataka.gov.in', '9900055555',
   NULL, '20111001', 'REV', 'Revenue', 'Revenue Inspector',
   'ACTIVE', NULL, now() - interval '200 days')
;
-- NOTE: Application Admin is a system-level / deployment-seeded actor and is
-- deliberately NOT a user_master row (FR-UM-051). Audit rows it performs use
-- actor_type = 'APPLICATION_ADMIN' with actor_id NULL — see audit_log inserts.

-- Convenience: user_id lookups are done via subqueries below by username so
-- this script is order-independent of IDENTITY values.

-- =====================================================================
-- USER_ROLE — Citizen role(s); Other Department exactly one role
-- =====================================================================
INSERT INTO um.user_role (user_id, role_id)
SELECT u.user_id, r.role_id
FROM um.user_master u
JOIN um.role_master r ON r.role_name = 'Citizen'
WHERE u.username = 'ravi.citizen1';

INSERT INTO um.user_role (user_id, role_id)
SELECT u.user_id, r.role_id
FROM um.user_master u
JOIN um.role_master r ON r.role_name = 'Revenue Verification Officer'
WHERE u.username = 'REV-20111001';

-- =====================================================================
-- EKYC_CHALLENGE — successful Citizen registration e-KYC (FR-UM-085)
-- =====================================================================
INSERT INTO um.ekyc_challenge
  (user_id, purpose, uidai_txn_ref, status, consent_captured_at, completed_at, created_at)
SELECT u.user_id, 'REGISTRATION', 'UIDAI-TXN-SAMPLE-001', 'SUCCESS',
       now() - interval '90 days', now() - interval '90 days', now() - interval '90 days'
FROM um.user_master u WHERE u.username = 'ravi.citizen1';

-- =====================================================================
-- POST_OCCUPANCY
--   1) Anitha Rao — Sub-Registrar @ SRO Yeshwanthapura (ACTIVE)
--   2) Suresh Patil — District Registrar @ DRO Bengaluru — ENDED after
--      relieving (handover: FR-UM-058 then FR-UM-060, no reserved step)
--   3) Manjunath — District Registrar @ DRO Bengaluru (ACTIVE Transfer In
--      after capacity freed — FR-UM-060, no Joining Date)
--   4) Kavya Iyer — Sub-Registrar @ SRO Jayanagar (ACTIVE) — cover officer
-- =====================================================================
INSERT INTO um.post_occupancy
  (user_id, post_code, office_code, status,
   transfer_order_no, relieving_date, relieving_reason, relieving_order_no, created_by, created_at)
SELECT u.user_id, 'POST-SR', 'OFF-SRO-YESH', 'ACTIVE',
       NULL, NULL, NULL, NULL, u.user_id, now() - interval '400 days'
FROM um.user_master u WHERE u.username = 'KGID10234501';

INSERT INTO um.post_occupancy
  (user_id, post_code, office_code, status,
   transfer_order_no, relieving_date, relieving_reason, relieving_order_no,
   created_by, created_at, ended_at)
SELECT u.user_id, 'POST-DRO', 'OFF-DRO-BLR', 'ENDED',
       NULL, DATE '2026-08-31', 'TRANSFER', 'RO/2026/0891',
       u.user_id, now() - interval '600 days', timestamptz '2026-09-01 00:05:00+05:30'
FROM um.user_master u WHERE u.username = 'KGID10234599';

INSERT INTO um.post_occupancy
  (user_id, post_code, office_code, status,
   transfer_order_no, created_by, created_at)
SELECT u.user_id, 'POST-DRO', 'OFF-DRO-BLR', 'ACTIVE',
       'TO/2026/1123', u.user_id, timestamptz '2026-09-01 09:15:00+05:30'
FROM um.user_master u WHERE u.username = 'KGID10234610';

INSERT INTO um.post_occupancy
  (user_id, post_code, office_code, status,
   transfer_order_no, created_by, created_at)
SELECT u.user_id, 'POST-SR', 'OFF-SRO-JAY', 'ACTIVE',
       NULL, u.user_id, now() - interval '500 days'
FROM um.user_master u WHERE u.username = 'KGID10234650';

-- =====================================================================
-- TEMPORARY_ABSENCE — US-TA-01: DRO records Leave for SR of
-- SRO Yeshwanthapura, 01-Sep-2026 to 05-Sep-2026
-- =====================================================================
INSERT INTO um.temporary_absence
  (occupancy_id, absence_type, reason_code, from_date, to_date, order_ref, recorded_by, created_at)
SELECT po.occupancy_id, 'LEAVE', 'PERSONAL', DATE '2026-09-01', DATE '2026-09-05',
       NULL, recorder.user_id, now() - interval '3 days'
FROM um.post_occupancy po
JOIN um.user_master occ ON occ.user_id = po.user_id AND occ.username = 'KGID10234501'
JOIN um.user_master recorder ON recorder.username = 'KGID10234599'
WHERE po.post_code = 'POST-SR' AND po.office_code = 'OFF-SRO-YESH';

-- =====================================================================
-- TEMPORARY_CHARGE — US-TA-02: DRO Bengaluru (superior) gives temporary
-- charge of SR@Yeshwanthapura to the Sub-Registrar of SRO Jayanagar
-- =====================================================================
INSERT INTO um.temporary_charge
  (absence_id, cover_user_id, covered_post_code, covered_office_code,
   from_date, to_date, assigned_by, order_ref, created_at)
SELECT ta.absence_id, cover.user_id, 'POST-SR', 'OFF-SRO-YESH',
       ta.from_date, ta.to_date, assigner.user_id, NULL, now() - interval '3 days'
FROM um.temporary_absence ta
JOIN um.user_master cover ON cover.username = 'KGID10234650'
JOIN um.user_master assigner ON assigner.username = 'KGID10234599'
WHERE ta.reason_code = 'PERSONAL';

-- =====================================================================
-- USER_SESSION — Citizen (OTP login) and DSR ASSIGNED (face/biometric, no OTP)
-- Idle 10 min / absolute 4 h (FR-UM-074, FR-UM-075)
-- =====================================================================
INSERT INTO um.user_session
  (user_id, is_active, session_context, assigned_occupancy_id, login_at, last_activity_at, expires_at)
SELECT u.user_id, true, NULL, NULL, now() - interval '10 minutes', now() - interval '1 minutes', now() + interval '3 hours 50 minutes'
FROM um.user_master u WHERE u.username = 'ravi.citizen1';

INSERT INTO um.user_session
  (user_id, is_active, session_context, assigned_occupancy_id, login_at, last_activity_at, expires_at)
SELECT u.user_id, true, 'ASSIGNED', po.occupancy_id, now() - interval '25 minutes', now() - interval '2 minutes', now() + interval '3 hours 35 minutes'
FROM um.user_master u
JOIN um.post_occupancy po ON po.user_id = u.user_id AND po.post_code = 'POST-SR' AND po.office_code = 'OFF-SRO-YESH'
WHERE u.username = 'KGID10234501';

-- =====================================================================
-- OTP_CHALLENGE — Citizen login OTP; Citizen registration OTP; DSR new-mobile
-- (FR-UM-086). DSR login does not use OTP (FR-UM-006).
-- =====================================================================
INSERT INTO um.otp_challenge
  (user_id, purpose, channel, destination, code_hash, expires_at, attempt_count, consumed_at, created_at)
SELECT u.user_id, 'LOGIN', 'SMS', '9900011111', encode(digest('123456','sha256'),'hex'),
       now() - interval '20 minutes', 1, now() - interval '25 minutes', now() - interval '25 minutes'
FROM um.user_master u WHERE u.username = 'ravi.citizen1';

INSERT INTO um.otp_challenge
  (user_id, purpose, channel, destination, code_hash, expires_at, attempt_count, consumed_at, created_at)
SELECT u.user_id, 'REG_MOBILE', 'SMS', '9900011111', encode(digest('654321','sha256'),'hex'),
       now() - interval '85 days', 1, now() - interval '90 days', now() - interval '90 days'
FROM um.user_master u WHERE u.username = 'ravi.citizen1';

INSERT INTO um.otp_challenge
  (user_id, purpose, channel, destination, code_hash, expires_at, attempt_count, consumed_at, created_at)
SELECT u.user_id, 'NEW_MOBILE', 'SMS', '9900022299', encode(digest('111222','sha256'),'hex'),
       now() - interval '2 days', 1, now() - interval '2 days', now() - interval '2 days'
FROM um.user_master u WHERE u.username = 'KGID10234501';

-- =====================================================================
-- AUDIT_LOG — representative entries for each report view
-- =====================================================================
INSERT INTO um.audit_log (actor_id, actor_type, action, entity, entity_id, after_json, reason, occurred_at)
SELECT u.user_id, 'USER', 'LOGIN_SUCCESS', 'SESSION', u.user_id::text,
       jsonb_build_object('result','SUCCESS','channel','FACE'), NULL, now() - interval '25 minutes'
FROM um.user_master u WHERE u.username = 'KGID10234501';

INSERT INTO um.audit_log (actor_id, actor_type, action, entity, entity_id, after_json, reason, occurred_at)
SELECT u.user_id, 'USER', 'ADD_CHARGE_TAKEN', 'SESSION', u.user_id::text,
       jsonb_build_object('assigned_post_code','POST-SR','additional_charge_post_code','POST-DEO','office_code','OFF-SRO-YESH'),
       NULL, now() - interval '15 minutes'
FROM um.user_master u WHERE u.username = 'KGID10234501';

INSERT INTO um.audit_log (actor_id, actor_type, action, entity, entity_id, after_json, reason, occurred_at)
SELECT u.user_id, 'USER', 'CITIZEN_LOST_MOBILE_RESET', 'USER_CONTACT', u.user_id::text,
       jsonb_build_object('channel','MOBILE','outcome','SUCCESS'),
       'Lost registered mobile — Aadhaar e-KYC + email PIN + new-mobile OTP verified', now() - interval '40 days'
FROM um.user_master u WHERE u.username = 'ravi.citizen1';

INSERT INTO um.audit_log (actor_id, actor_type, action, entity, entity_id, after_json, reason, occurred_at)
SELECT u.user_id, 'USER', 'DSR_MOBILE_CHANGE_SELF', 'USER_CONTACT', u.user_id::text,
       jsonb_build_object('channel','MOBILE','outcome','SUCCESS','old_value_masked','******2222','new_value_masked','******2299'),
       'FR-UM-086 self-service mobile change after login', now() - interval '2 days'
FROM um.user_master u WHERE u.username = 'KGID10234501';

INSERT INTO um.audit_log (actor_id, actor_type, action, entity, entity_id, after_json, reason, occurred_at)
VALUES
  (NULL, 'SYSTEM', 'OCCUPANCY_REFRESH', 'JOB', to_char(now(),'YYYY-MM-DD'),
   jsonb_build_object('ended_occupancies',1,'ended_absences',0,'ended_charges',0,'as_of',to_char(now(),'YYYY-MM-DD')),
   'FR-UM-068 / FR-UM-084 midnight refresh', now() - interval '6 hours');
