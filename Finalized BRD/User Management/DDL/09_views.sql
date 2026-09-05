-- =============================================================================
-- 09 · Views — reporting and runtime helpers
-- =============================================================================

SET search_path TO um, public;

-- Current IST calendar date helper expression used in views:
-- (timezone('Asia/Kolkata', now()))::date

-- Sanctioned post capacity (FR-UM-066)
CREATE OR REPLACE VIEW um.v_sanctioned_post_capacity AS
SELECT
  sp.post_code,
  pm.post_name,
  sp.office_code,
  oh.office_name,
  oh.office_type_code,
  sp.sanctioned_strength,
  sp.occupied_count,
  GREATEST(sp.sanctioned_strength - sp.occupied_count, 0) AS remaining_capacity,
  (sp.occupied_count < sp.sanctioned_strength)            AS has_available_capacity,  -- FR-UM-066(a)
  (sp.occupied_count = 0)                                 AS is_wholly_unoccupied    -- FR-UM-066(b)
FROM um.sanctioned_post sp
JOIN um.posts_master pm ON pm.post_code = sp.post_code
JOIN um.office_hierarchy oh ON oh.office_code = sp.office_code;

COMMENT ON VIEW um.v_sanctioned_post_capacity IS
  'Available capacity vs wholly unoccupied vacancy tests (FR-UM-066)';

-- Effective absences for current IST day (FR-UM-080)
CREATE OR REPLACE VIEW um.v_effective_absence AS
SELECT
  ta.absence_id,
  ta.occupancy_id,
  po.user_id,
  u.username,
  u.first_name,
  u.last_name,
  po.post_code,
  po.office_code,
  ta.absence_type,
  ta.reason_code,
  ta.from_date,
  ta.to_date,
  ta.status,
  ta.recorded_by
FROM um.temporary_absence ta
JOIN um.post_occupancy po ON po.occupancy_id = ta.occupancy_id
JOIN um.user_master u ON u.user_id = po.user_id
WHERE ta.status = 'APPROVED'
  AND (timezone('Asia/Kolkata', now()))::date BETWEEN ta.from_date AND ta.to_date;

COMMENT ON VIEW um.v_effective_absence IS
  'Approved absences covering current IST calendar day — blocks login (FR-UM-080)';

-- Users currently blocked from login due to effective absence
CREATE OR REPLACE VIEW um.v_login_blocked_by_absence AS
SELECT DISTINCT
  user_id,
  username,
  first_name,
  last_name,
  max(to_date) AS blocked_until,
  string_agg(DISTINCT absence_type::text, ', ' ORDER BY absence_type::text) AS absence_types
FROM um.v_effective_absence
GROUP BY user_id, username, first_name, last_name;

-- Active temporary charges selectable at FR-UM-052 / FR-UM-083
CREATE OR REPLACE VIEW um.v_active_temporary_charge AS
SELECT
  tc.temp_charge_id,
  tc.absence_id,
  tc.cover_user_id,
  cover.username AS cover_username,
  cover.first_name || ' ' || cover.last_name AS cover_name,
  tc.covered_post_code,
  pm.post_name AS covered_post_name,
  tc.covered_office_code,
  oh.office_name AS covered_office_name,
  absentee.user_id AS absent_user_id,
  absentee.first_name || ' ' || absentee.last_name AS absent_officer_name,
  tc.from_date,
  tc.to_date,
  tc.status,
  ta.absence_type
FROM um.temporary_charge tc
JOIN um.temporary_absence ta ON ta.absence_id = tc.absence_id
JOIN um.post_occupancy po ON po.occupancy_id = ta.occupancy_id
JOIN um.user_master absentee ON absentee.user_id = po.user_id
JOIN um.user_master cover ON cover.user_id = tc.cover_user_id
JOIN um.posts_master pm ON pm.post_code = tc.covered_post_code
JOIN um.office_hierarchy oh ON oh.office_code = tc.covered_office_code
WHERE tc.status = 'ACTIVE'
  AND ta.status = 'APPROVED'
  AND (timezone('Asia/Kolkata', now()))::date BETWEEN tc.from_date AND tc.to_date;

COMMENT ON VIEW um.v_active_temporary_charge IS
  'Rows listed at FR-UM-052 for cover officers (FR-UM-083)';

-- DSR login post-selection candidates for a user (occupancies + temp charges)
CREATE OR REPLACE VIEW um.v_dsr_login_post_options AS
SELECT
  po.user_id,
  'ASSIGNED'::um.session_context_t AS option_type,
  po.occupancy_id,
  NULL::bigint AS temp_charge_id,
  po.post_code,
  pm.post_name,
  po.office_code,
  oh.office_name,
  NULL::text AS absent_officer_name,
  po.status AS occupancy_status,
  po.joining_date
FROM um.post_occupancy po
JOIN um.posts_master pm ON pm.post_code = po.post_code
JOIN um.office_hierarchy oh ON oh.office_code = po.office_code
WHERE po.status = 'ACTIVE'
  AND (po.joining_date IS NULL
       OR po.joining_date <= (timezone('Asia/Kolkata', now()))::date)
UNION ALL
SELECT
  tc.cover_user_id AS user_id,
  'TEMPORARY_CHARGE'::um.session_context_t,
  NULL::bigint,
  tc.temp_charge_id,
  tc.covered_post_code,
  tc.covered_post_name,
  tc.covered_office_code,
  tc.covered_office_name,
  tc.absent_officer_name,
  NULL::um.occupancy_status_t,
  NULL::date
FROM um.v_active_temporary_charge tc;

-- Active session privilege path — roles for current context (simplified)
CREATE OR REPLACE VIEW um.v_session_role_claims AS
SELECT
  s.session_id,
  s.user_id,
  s.session_context,
  r.role_id,
  r.role_name,
  r.role_category
FROM um.user_session s
-- Citizen / OD: direct USER_ROLE
LEFT JOIN um.user_role ur
  ON ur.user_id = s.user_id
 AND s.session_context IS NULL
LEFT JOIN um.role_master r_direct ON r_direct.role_id = ur.role_id
-- DSR ASSIGNED: occupancy → post_role_map
LEFT JOIN um.post_occupancy po
  ON po.occupancy_id = s.assigned_occupancy_id
 AND s.session_context = 'ASSIGNED'
LEFT JOIN um.post_role_map prm_a
  ON prm_a.post_code = po.post_code
 AND s.session_context = 'ASSIGNED'
-- DSR ADDITIONAL_CHARGE
LEFT JOIN um.post_role_map prm_ac
  ON prm_ac.post_code = s.add_charge_post_code
 AND s.session_context = 'ADDITIONAL_CHARGE'
-- DSR TEMPORARY_CHARGE
LEFT JOIN um.temporary_charge tc
  ON tc.temp_charge_id = s.temp_charge_id
 AND s.session_context = 'TEMPORARY_CHARGE'
LEFT JOIN um.post_role_map prm_tc
  ON prm_tc.post_code = tc.covered_post_code
 AND s.session_context = 'TEMPORARY_CHARGE'
LEFT JOIN um.role_master r ON r.role_id = COALESCE(
  r_direct.role_id,
  prm_a.role_id,
  prm_ac.role_id,
  prm_tc.role_id
)
WHERE s.is_active
  AND r.role_id IS NOT NULL;

-- Role → Module Function report
CREATE OR REPLACE VIEW um.v_role_module_function AS
SELECT
  r.role_id,
  r.role_name,
  r.role_category,
  m.module_code,
  m.module_name,
  mf.function_id,
  mf.function_code
FROM um.role_master r
JOIN um.role_module_function rmf ON rmf.role_id = r.role_id
JOIN um.module_function mf ON mf.function_id = rmf.function_id
JOIN um.module_master m ON m.module_code = mf.module_code
WHERE r.is_active AND m.is_active AND mf.is_active;

-- Absence / temporary-charge report (FR-UM-084)
CREATE OR REPLACE VIEW um.v_absence_charge_report AS
SELECT
  ta.absence_id,
  ta.absence_type,
  ta.reason_code,
  ta.from_date,
  ta.to_date,
  ta.status AS absence_status,
  po.post_code,
  po.office_code,
  absent.user_id AS absent_user_id,
  absent.username AS absent_username,
  absent.first_name || ' ' || absent.last_name AS absent_name,
  recorder.username AS recorded_by_username,
  ta.created_at AS absence_created_at,
  tc.temp_charge_id,
  tc.status AS charge_status,
  cover.username AS cover_username,
  cover.first_name || ' ' || cover.last_name AS cover_name,
  tc.from_date AS charge_from,
  tc.to_date AS charge_to,
  assigner.username AS assigned_by_username
FROM um.temporary_absence ta
JOIN um.post_occupancy po ON po.occupancy_id = ta.occupancy_id
JOIN um.user_master absent ON absent.user_id = po.user_id
JOIN um.user_master recorder ON recorder.user_id = ta.recorded_by
LEFT JOIN um.temporary_charge tc ON tc.absence_id = ta.absence_id
LEFT JOIN um.user_master cover ON cover.user_id = tc.cover_user_id
LEFT JOIN um.user_master assigner ON assigner.user_id = tc.assigned_by;

-- Office descendants (recursive) — office span FR-UM-059
CREATE OR REPLACE VIEW um.v_office_descendants AS
WITH RECURSIVE tree AS (
  SELECT
    office_code AS root_office_code,
    office_code AS descendant_office_code,
    0 AS depth
  FROM um.office_hierarchy
  UNION ALL
  SELECT
    t.root_office_code,
    c.office_code,
    t.depth + 1
  FROM tree t
  JOIN um.office_hierarchy c ON c.parent_office_code = t.descendant_office_code
)
SELECT * FROM tree;

COMMENT ON VIEW um.v_office_descendants IS
  'Root office plus all descendants — used for office-span checks (FR-UM-059)';

-- =============================================================================
-- Additional reporting views — Section 8 (Reporting Requirements) coverage
-- =============================================================================

-- Report: all active, inactive, and suspended users
CREATE OR REPLACE VIEW um.v_user_status_report AS
SELECT
  u.user_id,
  u.username,
  u.user_category,
  u.first_name || COALESCE(' ' || u.last_name, '') AS full_name,
  u.email,
  u.mobile,
  u.status,
  u.status_reason,
  u.account_end_date,
  u.created_at,
  u.updated_at
FROM um.user_master u;

COMMENT ON VIEW um.v_user_status_report IS
  'Section 8 bullet 1 — report of all active, inactive, and suspended users';

-- Report: audit log of login attempts (successful and failed) over a date range
CREATE OR REPLACE VIEW um.v_login_audit_report AS
SELECT
  a.audit_id,
  a.actor_id AS user_id,
  u.username,
  a.action,
  a.occurred_at,
  a.after_json ->> 'result'  AS result,
  a.after_json ->> 'channel' AS channel,
  a.reason,
  a.ip_address,
  a.user_agent
FROM um.audit_log a
LEFT JOIN um.user_master u ON u.user_id = a.actor_id
WHERE a.entity = 'SESSION'
  AND a.action IN ('LOGIN_SUCCESS', 'LOGIN_FAILURE', 'OTP_VERIFY_FAILURE', 'LOGIN_LOCKOUT');

COMMENT ON VIEW um.v_login_audit_report IS
  'Section 8 bullet 2 — login attempt audit report over a selected date range';

-- Report: role and permission assignments across all users
CREATE OR REPLACE VIEW um.v_user_effective_roles AS
SELECT
  u.user_id, u.username, u.user_category,
  r.role_id, r.role_name, r.role_category,
  NULL::varchar AS post_code, NULL::varchar AS office_code,
  'DIRECT'::text AS source
FROM um.user_master u
JOIN um.user_role ur ON ur.user_id = u.user_id
JOIN um.role_master r ON r.role_id = ur.role_id
UNION ALL
SELECT
  u.user_id, u.username, u.user_category,
  r.role_id, r.role_name, r.role_category,
  po.post_code, po.office_code,
  'POST_OCCUPANCY'::text AS source
FROM um.user_master u
JOIN um.post_occupancy po ON po.user_id = u.user_id AND po.status IN ('ACTIVE', 'RESERVED')
JOIN um.post_role_map prm ON prm.post_code = po.post_code
JOIN um.role_master r ON r.role_id = prm.role_id;

COMMENT ON VIEW um.v_user_effective_roles IS
  'Section 8 bullet 3 — role and permission assignments across all users (direct + post-derived)';

-- Report: Citizen lost-mobile / security-question recovery, admin mobile change, email changes
CREATE OR REPLACE VIEW um.v_contact_change_recovery_report AS
SELECT
  a.audit_id,
  a.action,
  a.actor_id                    AS actor_user_id,
  actor.username                 AS actor_username,
  (a.entity_id)::bigint          AS user_id,
  u.username,
  a.reason,
  a.after_json ->> 'channel'     AS channel,
  a.after_json ->> 'outcome'     AS outcome,
  a.after_json ->> 'old_value_masked' AS old_value_masked,
  a.after_json ->> 'new_value_masked' AS new_value_masked,
  a.occurred_at
FROM um.audit_log a
LEFT JOIN um.user_master u     ON u.user_id::text = a.entity_id
LEFT JOIN um.user_master actor ON actor.user_id = a.actor_id
WHERE a.entity = 'USER_CONTACT'
  AND a.action IN ('CITIZEN_LOST_MOBILE_RESET', 'ADMIN_MOBILE_CHANGE', 'EMAIL_CHANGE', 'MOBILE_CHANGE_SELF');

COMMENT ON VIEW um.v_contact_change_recovery_report IS
  'Section 8 bullet 6 — single contact-change and recovery report (FR-UM-056, FR-UM-065, email changes)';

-- Report: additional charge taken / cleared (FR-UM-053)
CREATE OR REPLACE VIEW um.v_additional_charge_report AS
SELECT
  a.audit_id,
  a.actor_id                                       AS officer_user_id,
  officer.username                                 AS officer_username,
  a.action,
  a.after_json ->> 'assigned_post_code'             AS assigned_post_code,
  a.after_json ->> 'additional_charge_post_code'    AS additional_charge_post_code,
  a.after_json ->> 'office_code'                    AS office_code,
  a.occurred_at
FROM um.audit_log a
LEFT JOIN um.user_master officer ON officer.user_id = a.actor_id
WHERE a.entity = 'SESSION'
  AND a.action IN ('ADD_CHARGE_TAKEN', 'ADD_CHARGE_CLEARED', 'ADD_CHARGE_SWITCH_BACK');

COMMENT ON VIEW um.v_additional_charge_report IS
  'Section 8 bullet 7 — additional charge taken/cleared report (FR-UM-053)';

-- Report: occupancy-refresh job runs (FR-UM-068)
CREATE OR REPLACE VIEW um.v_occupancy_refresh_report AS
SELECT
  a.audit_id                                        AS run_id,
  a.occurred_at                                      AS run_at,
  (a.after_json ->> 'as_of')::date                   AS as_of_date,
  (a.after_json ->> 'ended_occupancies')::int         AS ended_occupancies,
  (a.after_json ->> 'ended_absences')::int            AS ended_absences,
  (a.after_json ->> 'ended_charges')::int             AS ended_charges
FROM um.audit_log a
WHERE a.entity = 'JOB' AND a.action = 'OCCUPANCY_REFRESH'
ORDER BY a.occurred_at DESC;

COMMENT ON VIEW um.v_occupancy_refresh_report IS
  'Section 8 bullet 9 — occupancy-refresh job run report (FR-UM-068)';

-- Report: Transfer Out / Transfer In history (FR-UM-057–FR-UM-061, FR-UM-067)
CREATE OR REPLACE VIEW um.v_transfer_history_report AS
SELECT
  po.occupancy_id,
  po.user_id,
  u.username,
  u.first_name || COALESCE(' ' || u.last_name, '') AS officer_name,
  po.post_code,
  pm.post_name,
  po.office_code,
  oh.office_name,
  po.status,
  po.reserved_flag,
  po.joining_date,
  po.transfer_order_no,
  po.relieving_date,
  po.relieving_order_no,
  po.created_at AS occupancy_created_at,
  po.ended_at
FROM um.post_occupancy po
JOIN um.user_master u       ON u.user_id = po.user_id
JOIN um.posts_master pm     ON pm.post_code = po.post_code
JOIN um.office_hierarchy oh ON oh.office_code = po.office_code
ORDER BY po.created_at DESC;

COMMENT ON VIEW um.v_transfer_history_report IS
  'Section 8 bullet 10 — Transfer Out / Transfer In history report';

-- Report: officer posting and service history (chronological per officer)
CREATE OR REPLACE VIEW um.v_officer_posting_history AS
SELECT
  po.user_id,
  u.username,
  u.first_name || COALESCE(' ' || u.last_name, '') AS officer_name,
  po.occupancy_id,
  po.post_code,
  pm.post_name,
  po.office_code,
  oh.office_name,
  po.status,
  po.joining_date,
  po.relieving_date,
  po.end_date,
  po.deputation_reason,
  po.created_at,
  po.ended_at
FROM um.post_occupancy po
JOIN um.user_master u       ON u.user_id = po.user_id
JOIN um.posts_master pm     ON pm.post_code = po.post_code
JOIN um.office_hierarchy oh ON oh.office_code = po.office_code
ORDER BY po.user_id, po.created_at;

COMMENT ON VIEW um.v_officer_posting_history IS
  'Section 8 bullet 11 — officer posting and service history report';
