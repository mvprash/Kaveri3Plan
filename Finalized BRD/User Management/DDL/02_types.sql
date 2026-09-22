-- =============================================================================
-- 02 · Enumerated types
-- Companion to ERD-K3-UM-001 v2.3 / BRD_User_Management_v1.0 (11-Sep-2026)
-- =============================================================================

SET search_path TO um, public;

DO $$ BEGIN
  CREATE TYPE um.user_category_t AS ENUM (
    'CITIZEN',
    'DSR_OFFICER',
    'OTHER_DEPARTMENT'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.role_category_t AS ENUM (
    'CITIZEN',
    'DSR',
    'OTHER_DEPARTMENT'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.account_status_t AS ENUM (
    'ACTIVE',
    'SUSPENDED',
    'DEACTIVATED'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- RESERVED occupancy status retired with FR-UM-061 / FR-UM-067 (v4.20 / BRD v1.0)
DO $$ BEGIN
  CREATE TYPE um.occupancy_status_t AS ENUM (
    'ACTIVE',
    'ENDED'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.relieving_reason_t AS ENUM (
    'DEPUTATION',
    'TRANSFER',
    'SUSPENSION',
    'SUPERANNUATION',
    'DEATH'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.absence_type_t AS ENUM (
    'LEAVE',
    'OOD',
    'OTHER'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.absence_status_t AS ENUM (
    'APPROVED',
    'CANCELLED',
    'ENDED'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.temp_charge_status_t AS ENUM (
    'ACTIVE',
    'CANCELLED',
    'ENDED'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.session_context_t AS ENUM (
    'ASSIGNED',
    'ADDITIONAL_CHARGE',
    'TEMPORARY_CHARGE'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.otp_purpose_t AS ENUM (
    'LOGIN',
    'REG_EMAIL',
    'REG_MOBILE',
    'RESET_PIN',
    'NEW_MOBILE',
    'NEW_EMAIL'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.otp_channel_t AS ENUM (
    'SMS',
    'EMAIL'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.ekyc_purpose_t AS ENUM (
    'REGISTRATION',
    'LOST_MOBILE'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.ekyc_status_t AS ENUM (
    'PENDING',
    'SUCCESS',
    'FAILED'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.resource_type_t AS ENUM (
    'API',
    'URL'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE um.actor_type_t AS ENUM (
    'USER',
    'APPLICATION_ADMIN',
    'SYSTEM'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
