-- =============================================================================
-- 10 · Functions and triggers — occupancy refresh, occupied_count, absence end
-- =============================================================================

SET search_path TO um, public;

-- Recalculate occupied_count for one Post+Office (Active + Reserved)
CREATE OR REPLACE FUNCTION um.fn_refresh_occupied_count(
  p_post_code   varchar,
  p_office_code varchar
) RETURNS integer
LANGUAGE plpgsql
AS $$
DECLARE
  v_count integer;
BEGIN
  SELECT count(*)::integer INTO v_count
  FROM um.post_occupancy
  WHERE post_code = p_post_code
    AND office_code = p_office_code
    AND status IN ('ACTIVE', 'RESERVED');

  UPDATE um.sanctioned_post
  SET occupied_count = v_count,
      updated_at = now()
  WHERE post_code = p_post_code
    AND office_code = p_office_code;

  RETURN v_count;
END;
$$;

COMMENT ON FUNCTION um.fn_refresh_occupied_count IS
  'Recount Active+Reserved occupancies; Temporary Absence does not change count (FR-UM-081)';

-- Trigger: keep occupied_count in sync on occupancy status changes
CREATE OR REPLACE FUNCTION um.tg_post_occupancy_sync_occupied()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    PERFORM um.fn_refresh_occupied_count(NEW.post_code, NEW.office_code);
    RETURN NEW;
  ELSIF TG_OP = 'UPDATE' THEN
    PERFORM um.fn_refresh_occupied_count(NEW.post_code, NEW.office_code);
    IF NEW.post_code IS DISTINCT FROM OLD.post_code
       OR NEW.office_code IS DISTINCT FROM OLD.office_code THEN
      PERFORM um.fn_refresh_occupied_count(OLD.post_code, OLD.office_code);
    END IF;
    RETURN NEW;
  ELSIF TG_OP = 'DELETE' THEN
    PERFORM um.fn_refresh_occupied_count(OLD.post_code, OLD.office_code);
    RETURN OLD;
  END IF;
  RETURN NULL;
END;
$$;

DROP TRIGGER IF EXISTS trg_post_occupancy_sync_occupied ON um.post_occupancy;
CREATE TRIGGER trg_post_occupancy_sync_occupied
  AFTER INSERT OR UPDATE OF status, post_code, office_code OR DELETE
  ON um.post_occupancy
  FOR EACH ROW
  EXECUTE PROCEDURE um.tg_post_occupancy_sync_occupied();

-- Occupancy refresh job body (FR-UM-068 / FR-UM-084) — call shortly after midnight IST
CREATE OR REPLACE FUNCTION um.fn_occupancy_refresh_job(
  p_as_of date DEFAULT (timezone('Asia/Kolkata', now()))::date
) RETURNS TABLE (
  ended_occupancies integer,
  ended_absences    integer,
  ended_charges     integer
)
LANGUAGE plpgsql
AS $$
DECLARE
  v_ended_occ integer := 0;
  v_ended_abs integer := 0;
  v_ended_chg integer := 0;
BEGIN
  -- End relieved occupancies after Relieving Date (retain through that calendar day)
  WITH closed AS (
    UPDATE um.post_occupancy
    SET status = 'ENDED',
        ended_at = now(),
        updated_at = now()
    WHERE status IN ('ACTIVE', 'RESERVED')
      AND relieving_date IS NOT NULL
      AND relieving_date < p_as_of
    RETURNING occupancy_id
  )
  SELECT count(*)::integer INTO v_ended_occ FROM closed;

  -- End deputation by End Date (FR-UM-030)
  WITH closed AS (
    UPDATE um.post_occupancy
    SET status = 'ENDED',
        ended_at = now(),
        updated_at = now()
    WHERE status IN ('ACTIVE', 'RESERVED')
      AND end_date IS NOT NULL
      AND end_date < p_as_of
    RETURNING occupancy_id
  )
  SELECT v_ended_occ + count(*)::integer INTO v_ended_occ FROM closed;

  -- Activate reserved Transfer In on Joining Date (FR-UM-061)
  UPDATE um.post_occupancy
  SET status = 'ACTIVE',
      reserved_flag = false,
      updated_at = now()
  WHERE status = 'RESERVED'
    AND joining_date IS NOT NULL
    AND joining_date <= p_as_of;

  -- End temporary absences after to_date (FR-UM-084)
  WITH closed AS (
    UPDATE um.temporary_absence
    SET status = 'ENDED',
        updated_at = now()
    WHERE status = 'APPROVED'
      AND to_date < p_as_of
    RETURNING absence_id
  )
  SELECT count(*)::integer INTO v_ended_abs FROM closed;

  -- End linked temporary charges
  WITH closed AS (
    UPDATE um.temporary_charge tc
    SET status = 'ENDED',
        cancelled_at = COALESCE(tc.cancelled_at, now())
    WHERE tc.status = 'ACTIVE'
      AND (
        tc.to_date < p_as_of
        OR EXISTS (
          SELECT 1 FROM um.temporary_absence ta
          WHERE ta.absence_id = tc.absence_id
            AND ta.status IN ('CANCELLED', 'ENDED')
        )
      )
    RETURNING temp_charge_id
  )
  SELECT count(*)::integer INTO v_ended_chg FROM closed;

  -- Deactivate Other Department accounts past account_end_date (FR-UM-033)
  UPDATE um.user_master
  SET status = 'DEACTIVATED',
      status_reason = COALESCE(status_reason, 'Account End Date reached'),
      updated_at = now()
  WHERE user_category = 'OTHER_DEPARTMENT'
    AND status = 'ACTIVE'
    AND account_end_date IS NOT NULL
    AND account_end_date < p_as_of;

  INSERT INTO um.audit_log (actor_type, action, entity, entity_id, after_json, reason)
  VALUES (
    'SYSTEM',
    'OCCUPANCY_REFRESH',
    'JOB',
    p_as_of::text,
    jsonb_build_object(
      'ended_occupancies', v_ended_occ,
      'ended_absences', v_ended_abs,
      'ended_charges', v_ended_chg,
      'as_of', p_as_of
    ),
    'FR-UM-068 / FR-UM-084 midnight refresh'
  );

  ended_occupancies := v_ended_occ;
  ended_absences := v_ended_abs;
  ended_charges := v_ended_chg;
  RETURN NEXT;
END;
$$;

COMMENT ON FUNCTION um.fn_occupancy_refresh_job IS
  'Scheduled shortly after midnight IST — relieving, joining, absence/charge end, OD end-date (FR-UM-068, FR-UM-084)';

-- Login eligibility check (FR-UM-080)
CREATE OR REPLACE FUNCTION um.fn_user_has_effective_absence(p_user_id bigint)
RETURNS boolean
LANGUAGE sql
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1
    FROM um.v_effective_absence ea
    WHERE ea.user_id = p_user_id
  );
$$;

COMMENT ON FUNCTION um.fn_user_has_effective_absence IS
  'True when any Approved absence covers current IST day for any of the user''s posts (FR-UM-080)';

-- Optional: pg_cron schedule example (commented — enable in ops)
-- SELECT cron.schedule(
--   'um-occupancy-refresh-ist',
--   '5 18 * * *',  -- 00:05 IST ≈ 18:35 UTC previous day depending on DST; prefer timezone-aware runner
--   $$SELECT * FROM um.fn_occupancy_refresh_job()$$
-- );
