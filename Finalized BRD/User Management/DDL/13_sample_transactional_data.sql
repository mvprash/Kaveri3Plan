-- =============================================================================
-- 13 · Illustrative SAMPLE / DEMO data — NOT for production
-- Companion to ERD-K3-UM-001 v2.2 / BRD_User_Management_v4.18
-- Purpose: exercise the schema end-to-end and back the ERD "Sample Records"
-- sections with data traceable to the BRD's own worked examples. Safe to run
-- once against a fresh/dev database only — re-running will duplicate rows
-- (no ON CONFLICT — these are not natural-keyed reference rows).
-- =============================================================================

SET search_path TO um, public;

-- -----------------------------------------------------------------------------
-- Security questions must already exist (12_seed_masters.sql) — Citizen answers
-- reference the first five by display_order.
-- -----------------------------------------------------------------------------

-- =====================================================================
-- USER_MASTER — one Citizen, one DSR Officer (assigned + covering), one
-- DSR Officer being relieved/transferred (handover example), one Other
-- Department user, one Application-tier admin actor for audit rows.
-- =====================================================================
INSERT INTO um.user_master
  (username, user_category, first_name, last_name, email, mobile,
   parent_department, designation, status, created_at)
VALUES
  ('ravi.citizen1', 'CITIZEN', 'Ravi', 'Kumar', 'ravi.kumar@example.com', '9900011111',
   NULL, NULL, 'ACTIVE', now() - interval '90 days'),
  ('KGID10234501', 'DSR_OFFICER', 'Anitha', 'Rao', 'anitha.rao@karnataka.gov.in', '9900022222',
   NULL, NULL, 'ACTIVE', now() - interval '400 days'),
  ('KGID10234599', 'DSR_OFFICER', 'Suresh', 'Patil', 'suresh.patil@karnataka.gov.in', '9900033333',
   NULL, NULL, 'ACTIVE', now() - interval '600 days'),
  ('KGID10234610', 'DSR_OFFICER', 'Manjunath', NULL, 'manjunath@karnataka.gov.in', '9900044444',
   NULL, NULL, 'ACTIVE', now() - interval '30 days'),
  ('KGID10234650', 'DSR_OFFICER', 'Kavya', 'Iyer', 'kavya.iyer@karnataka.gov.in', '9900066666',
   NULL, NULL, 'ACTIVE', now() - interval '500 days'),
  ('KGID20111001', 'OTHER_DEPARTMENT', 'Deepa', 'Shetty', 'deepa.shetty@revenue.karnataka.gov.in', '9900055555',
   'Revenue', 'Revenue Inspector', 'ACTIVE', now() - interval '200 days')
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
WHERE u.username = 'KGID20111001';

-- =====================================================================
-- USER_SECURITY_ANSWER — 5 hashed answers for the Citizen (FR-UM-055)
-- =====================================================================
INSERT INTO um.user_security_answer (user_id, question_id, answer_hash)
SELECT u.user_id, q.question_id, encode(digest('sample-answer-' || q.question_id::text, 'sha256'), 'hex')
FROM um.user_master u
JOIN um.security_question q ON q.display_order <= 5
WHERE u.username = 'ravi.citizen1';

-- =====================================================================
-- POST_OCCUPANCY
--   1) Anitha Rao — Sub-Registrar @ SRO Yeshwanthapura (ACTIVE, assigned post)
--   2) Suresh Patil — Sub-Registrar @ SRO Jayanagar (ACTIVE) — being relieved
--      (DRO Bengaluru handover example, Section 6.6.4)
--   3) Manjunath — District Registrar @ DRO Bengaluru (RESERVED Transfer-In,
--      Joining Date 01-Sep-2026, reserved against Suresh's relieving)
-- =====================================================================
INSERT INTO um.post_occupancy
  (user_id, post_code, office_code, status, joining_date,
   transfer_order_no, relieving_date, relieving_order_no, created_by, created_at)
SELECT u.user_id, 'POST-SR', 'OFF-SRO-YESH', 'ACTIVE', NULL,
       NULL, NULL, NULL, u.user_id, now() - interval '400 days'
FROM um.user_master u WHERE u.username = 'KGID10234501';

INSERT INTO um.post_occupancy
  (user_id, post_code, office_code, status, joining_date,
   transfer_order_no, relieving_date, relieving_order_no, created_by, created_at)
SELECT u.user_id, 'POST-DRO', 'OFF-DRO-BLR', 'ACTIVE', NULL,
       NULL, DATE '2026-08-31', 'RO/2026/0891', u.user_id, now() - interval '600 days'
FROM um.user_master u WHERE u.username = 'KGID10234599';

INSERT INTO um.post_occupancy
  (user_id, post_code, office_code, status, joining_date,
   transfer_order_no, relieving_date, relieving_order_no, reserved_flag, created_by, created_at)
SELECT u.user_id, 'POST-DRO', 'OFF-DRO-BLR', 'RESERVED', DATE '2026-09-01',
       'TO/2026/1123', NULL, NULL, true, u.user_id, now() - interval '5 days'
FROM um.user_master u WHERE u.username = 'KGID10234610';

-- 4) Kavya Iyer — Sub-Registrar @ SRO Jayanagar (ACTIVE) — SR peer who will
--    cover Anitha Rao's post as Temporary Charge below (Section 6.6.6 example)
INSERT INTO um.post_occupancy
  (user_id, post_code, office_code, status, joining_date,
   transfer_order_no, relieving_date, relieving_order_no, created_by, created_at)
SELECT u.user_id, 'POST-SR', 'OFF-SRO-JAY', 'ACTIVE', NULL,
       NULL, NULL, NULL, u.user_id, now() - interval '500 days'
FROM um.user_master u WHERE u.username = 'KGID10234650';

-- =====================================================================
-- TEMPORARY_ABSENCE — US-TA-01: DRO Bengaluru records Leave for SR of
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
-- USER_SESSION — one Citizen session, one DSR ASSIGNED session
-- =====================================================================
INSERT INTO um.user_session
  (user_id, is_active, session_context, assigned_occupancy_id, login_at, last_activity_at, expires_at)
SELECT u.user_id, true, NULL, NULL, now() - interval '10 minutes', now() - interval '1 minutes', now() + interval '7 hours 50 minutes'
FROM um.user_master u WHERE u.username = 'ravi.citizen1';

INSERT INTO um.user_session
  (user_id, is_active, session_context, assigned_occupancy_id, login_at, last_activity_at, expires_at)
SELECT u.user_id, true, 'ASSIGNED', po.occupancy_id, now() - interval '25 minutes', now() - interval '2 minutes', now() + interval '7 hours 35 minutes'
FROM um.user_master u
JOIN um.post_occupancy po ON po.user_id = u.user_id AND po.post_code = 'POST-SR' AND po.office_code = 'OFF-SRO-YESH'
WHERE u.username = 'KGID10234501';

-- =====================================================================
-- OTP_CHALLENGE — a consumed login OTP and a consumed registration OTP
-- =====================================================================
INSERT INTO um.otp_challenge
  (user_id, purpose, channel, destination, code_hash, expires_at, attempt_count, consumed_at, created_at)
SELECT u.user_id, 'LOGIN', 'SMS', '9900022222', encode(digest('123456','sha256'),'hex'),
       now() - interval '20 minutes', 1, now() - interval '25 minutes', now() - interval '25 minutes'
FROM um.user_master u WHERE u.username = 'KGID10234501';

INSERT INTO um.otp_challenge
  (user_id, purpose, channel, destination, code_hash, expires_at, attempt_count, consumed_at, created_at)
SELECT u.user_id, 'REG_MOBILE', 'SMS', '9900011111', encode(digest('654321','sha256'),'hex'),
       now() - interval '85 days', 1, now() - interval '90 days', now() - interval '90 days'
FROM um.user_master u WHERE u.username = 'ravi.citizen1';

-- =====================================================================
-- AUDIT_LOG — representative entries for each report view
-- =====================================================================
INSERT INTO um.audit_log (actor_id, actor_type, action, entity, entity_id, after_json, reason, occurred_at)
SELECT u.user_id, 'USER', 'LOGIN_SUCCESS', 'SESSION', u.user_id::text,
       jsonb_build_object('result','SUCCESS','channel','SMS'), NULL, now() - interval '25 minutes'
FROM um.user_master u WHERE u.username = 'KGID10234501';

INSERT INTO um.audit_log (actor_id, actor_type, action, entity, entity_id, after_json, reason, occurred_at)
SELECT u.user_id, 'USER', 'ADD_CHARGE_TAKEN', 'SESSION', u.user_id::text,
       jsonb_build_object('assigned_post_code','POST-SR','additional_charge_post_code','POST-DEO','office_code','OFF-SRO-YESH'),
       NULL, now() - interval '15 minutes'
FROM um.user_master u WHERE u.username = 'KGID10234501';

INSERT INTO um.audit_log (actor_id, actor_type, action, entity, entity_id, reason, occurred_at)
SELECT u.user_id, 'USER', 'CITIZEN_LOST_MOBILE_RESET', 'USER_CONTACT', u.user_id::text,
       'Lost registered mobile — 3 of 5 security questions + email PIN verified', now() - interval '40 days'
FROM um.user_master u WHERE u.username = 'ravi.citizen1';

INSERT INTO um.audit_log (actor_id, actor_type, action, entity, entity_id, after_json, reason, occurred_at)
VALUES
  (NULL, 'SYSTEM', 'OCCUPANCY_REFRESH', 'JOB', to_char(now(),'YYYY-MM-DD'),
   jsonb_build_object('ended_occupancies',1,'ended_absences',0,'ended_charges',0,'as_of',to_char(now(),'YYYY-MM-DD')),
   'FR-UM-068 / FR-UM-084 midnight refresh', now() - interval '6 hours');
